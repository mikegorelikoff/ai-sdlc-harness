#!/usr/bin/env python3
"""Shared artifact compression helpers for AI SDLC skill scripts.

This module is the token-saving core used by most skill-specific wrappers.
It reads large Markdown/text inputs once, emits a compact signal report, and
optionally writes the routed artifact skeleton plus `decision-log.md`.
Generated skeletons always include canonical `artifact_metadata` frontmatter
with retrieval-oriented `metatags` so artifacts remain traceable without
requiring a full reread.

Flow behavior is centralized here so every skill interprets `--quick-flow`
and `--full-flow` consistently:

- quick flow compresses aggressively, records assumptions, and avoids
  questions except for material risk.
- full flow preserves more evidence, treats structural gaps as blockers, and
  prompts for traceability/validation before handoff.
"""

from __future__ import annotations

import argparse
import copy
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

from ai_sdlc_specs_index import parse_artifact_metadata
from ai_sdlc_specs_index import write_indexes_for_roots
from ai_sdlc_state_machine import add_state_arguments, run_state_action


# Common traceability IDs that should survive compression and remain visible to
# the agent after large source artifacts have been summarized.
ID_PATTERN = re.compile(r"\b(?:REQ|AC|US|TC|DEC|TASK|RISK|EPIC)-\d{2,4}\b", re.IGNORECASE)

# Open-work markers that usually require either a question, an assumption, or a
# decision-log entry depending on the active flow mode.
TODO_PATTERN = re.compile(r"\b(?:TODO|TBD|FIXME|OPEN QUESTION|DECISION REQUIRED|BLOCKED)\b", re.IGNORECASE)

SECTION_HEADING_PATTERN = re.compile(r"^##\s+(.+?)\s*$")
CONTENT_HEADING_PATTERN = re.compile(r"^#{1,2}\s+")
FENCE_PATTERN = re.compile(r"^\s*(`{3,}|~{3,})")
EMPTY_SECTION_MARKER = "<!-- ai-sdlc:empty -->"
DECISION_ID_PATTERN = re.compile(r"^DEC-\d{3,4}$")
LIFECYCLE_TAGS = {"draft", "review", "approved", "validated", "blocked", "superseded"}


def atomic_write_text(path: Path, text: str) -> None:
    """Atomically replace one UTF-8 text file in its target directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(text)
            temp_path = Path(handle.name)
        os.replace(temp_path, path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


def markdown_section_spans(text: str) -> list[tuple[str, int, int, int]]:
    """Return H2 section name and source spans, ignoring headings in fences."""
    headings_found: list[tuple[str, int, int]] = []
    offset = 0
    fence_char = ""
    fence_length = 0
    for line in text.splitlines(keepends=True):
        fence = FENCE_PATTERN.match(line)
        if fence:
            token = fence.group(1)
            if not fence_char:
                fence_char = token[0]
                fence_length = len(token)
            elif token[0] == fence_char and len(token) >= fence_length:
                fence_char = ""
                fence_length = 0
            offset += len(line)
            continue
        if not fence_char:
            heading = SECTION_HEADING_PATTERN.match(line.rstrip("\r\n"))
            if heading:
                headings_found.append((heading.group(1).strip(), offset, offset + len(line)))
        offset += len(line)

    spans: list[tuple[str, int, int, int]] = []
    for index, (name, start, body_start) in enumerate(headings_found):
        end = headings_found[index + 1][1] if index + 1 < len(headings_found) else len(text)
        spans.append((name, start, body_start, end))
    return spans


def validate_section_content(content: str) -> str:
    """Validate raw stdin content intended for one scaffold section."""
    normalized = content.strip()
    if not normalized:
        raise ValueError("section content from stdin is empty")
    if normalized.startswith("---\n"):
        raise ValueError("section content must not include YAML frontmatter")

    fence_char = ""
    fence_length = 0
    for line in normalized.splitlines():
        fence = FENCE_PATTERN.match(line)
        if fence:
            token = fence.group(1)
            if not fence_char:
                fence_char = token[0]
                fence_length = len(token)
            elif token[0] == fence_char and len(token) >= fence_length:
                fence_char = ""
                fence_length = 0
            continue
        if not fence_char and CONTENT_HEADING_PATTERN.match(line):
            raise ValueError("section content must not include H1 or H2 headings")
    if fence_char:
        raise ValueError("section content contains an unclosed fenced code block")
    return normalized


def yaml_quote(value: object) -> str:
    """Return a conservative YAML double-quoted scalar."""
    text = str(value)
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def tag_slug(value: object) -> str:
    """Normalize arbitrary labels into stable lowercase metadata tags."""
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "unknown"


def unique_tags(values: list[object]) -> list[str]:
    """Return metadata tags in first-seen order without duplicates."""
    tags: list[str] = []
    seen: set[str] = set()
    for value in values:
        tag = tag_slug(value)
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)
    return tags


def namespace_from_workspace(workspace: str) -> str:
    """Return the artifact root for a refinement or implementation workspace."""
    return "specs" if workspace == "implementation" else "specs-refiniment"


def artifact_metadata_lines(
    *,
    feature: str,
    artifact_name: str,
    artifact_path: str,
    workspace: str,
    skill_name: str,
    flow_mode: str,
    decision_log_path: str,
    state_file_path: str,
    state_args: argparse.Namespace | None,
    created_at: str | None = None,
    owner: str | None = None,
    status: str | None = None,
    trace_ids: list[str] | None = None,
    related_artifacts: list[str] | None = None,
    validation: list[str] | None = None,
    metatags: list[str] | None = None,
) -> list[str]:
    """Build canonical frontmatter for every generated skill artifact.

    The metadata block is intentionally verbose enough to let future agents
    route, filter, validate, and trace artifacts without rereading the full
    document body. It does not replace the body, decision log, or state file.
    """
    today = date.today().isoformat()
    created_at = created_at or today
    owner = owner or (getattr(state_args, "artifact_owner", None) if state_args is not None else None) or "TBD"
    status = status or (getattr(state_args, "artifact_status", None) if state_args is not None else None) or "draft"
    extra_tags = getattr(state_args, "artifact_tag", []) if state_args is not None else []
    tags = unique_tags(
        [
            "ai-sdlc",
            workspace,
            skill_name or "unknown-skill",
            Path(artifact_name).stem,
            status,
            *extra_tags,
            *(metatags or []),
        ]
    )

    lines = [
        "---",
        "artifact_metadata:",
        "  schema: " + yaml_quote("ai-sdlc-artifact-metadata/v1"),
        "  feature: " + yaml_quote(feature),
        "  artifact: " + yaml_quote(artifact_name),
        "  path: " + yaml_quote(artifact_path),
        "  workspace: " + yaml_quote(workspace),
        "  skill: " + yaml_quote(skill_name or "TBD"),
        "  flow_mode: " + yaml_quote(flow_mode),
        "  state_file: " + yaml_quote(state_file_path),
        "  decision_log: " + yaml_quote(decision_log_path),
        "  status: " + yaml_quote(status),
        "  owner: " + yaml_quote(owner),
        "  created_at: " + yaml_quote(created_at),
        "  updated_at: " + yaml_quote(today),
    ]
    for key, values in (
        ("trace_ids", trace_ids or []),
        ("related_artifacts", related_artifacts or []),
        ("validation", validation or []),
    ):
        if values:
            lines.append(f"  {key}:")
            lines.extend(f"    - {yaml_quote(value)}" for value in values)
        else:
            lines.append(f"  {key}: []")
    lines.append("  metatags:")
    lines.extend(f"    - {yaml_quote(tag)}" for tag in tags)
    lines.extend(["---", ""])
    return lines


def replace_frontmatter(text: str, metadata_lines: list[str]) -> str:
    """Replace generated frontmatter or add it to an older Markdown file."""
    metadata = "\n".join(metadata_lines).rstrip() + "\n\n"
    if not text.startswith("---\n"):
        return metadata + text.lstrip()
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("artifact has unterminated YAML frontmatter")
    body_start = end + len("\n---")
    while body_start < len(text) and text[body_start] in "\r\n":
        body_start += 1
    return metadata + text[body_start:]


def refreshed_artifact_metadata(
    *,
    text: str,
    feature: str,
    artifact_name: str,
    artifact_path: str,
    workspace: str,
    skill_name: str,
    flow_mode: str,
    decision_log_path: str,
    state_file_path: str,
    state_args: argparse.Namespace | None,
    status: str,
) -> str:
    """Refresh generated metadata while retaining durable user annotations."""
    existing = parse_artifact_metadata(text)
    existing_tags = [
        str(tag)
        for tag in existing.get("metatags", ())
        if str(tag) not in LIFECYCLE_TAGS
    ]
    discovered_ids = sorted({match.group(0).upper() for match in ID_PATTERN.finditer(text)})
    trace_ids = sorted({str(value) for value in existing.get("trace_ids", ())} | set(discovered_ids))
    metadata = artifact_metadata_lines(
        feature=feature,
        artifact_name=artifact_name,
        artifact_path=artifact_path,
        workspace=workspace,
        skill_name=skill_name,
        flow_mode=flow_mode,
        decision_log_path=decision_log_path,
        state_file_path=state_file_path,
        state_args=state_args,
        created_at=str(existing.get("created_at") or date.today().isoformat()),
        owner=(getattr(state_args, "artifact_owner", None) if state_args is not None else None)
        or str(existing.get("owner") or "TBD"),
        status=status,
        trace_ids=trace_ids,
        related_artifacts=[str(value) for value in existing.get("related_artifacts", ())],
        validation=[str(value) for value in existing.get("validation", ())],
        metatags=existing_tags,
    )
    return replace_frontmatter(text, metadata)


def read_text(path: Path) -> str:
    """Read text files robustly while preserving progress on bad bytes."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def headings(text: str) -> list[str]:
    """Return Markdown heading names without their leading `#` markers."""
    return [m.group(2).strip() for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", text, re.MULTILINE)]


def first_sentences(text: str, limit: int) -> list[str]:
    """Extract a compact first-pass summary without expensive NLP dependencies."""
    compact = re.sub(r"\s+", " ", text).strip()
    if not compact:
        return []
    sentences = re.split(r"(?<=[.!?])\s+", compact)
    return [s[:220] for s in sentences[:limit] if s]


def count_keywords(text: str, keywords: list[str]) -> list[tuple[str, int]]:
    """Count skill-specific signal words to guide the agent's attention."""
    lowered = text.lower()
    return [(kw, lowered.count(kw.lower())) for kw in keywords if lowered.count(kw.lower())]


def section_presence(text: str, required: list[str]) -> list[tuple[str, bool]]:
    """Compare required skill sections against headings found in input text."""
    present = {h.lower() for h in headings(text)}
    return [(section, section.lower() in present) for section in required]


def scaffold_body(artifact_name: str, required_sections: list[str], document_title: str | None = None) -> str:
    """Build the deterministic visible body for a new section-driven artifact."""
    lines = [f"# {document_title or artifact_name}", ""]
    for section in required_sections:
        lines.extend([f"## {section}", EMPTY_SECTION_MARKER, ""])
    return "\n".join(lines).rstrip() + "\n"


def canonical_section_map(text: str, required_sections: list[str]) -> dict[str, tuple[int, int, int]]:
    """Return unique canonical section spans and reject ambiguous duplicates."""
    required = set(required_sections)
    found: dict[str, tuple[int, int, int]] = {}
    for name, start, body_start, end in markdown_section_spans(text):
        if name not in required:
            continue
        if name in found:
            raise ValueError(f"artifact contains duplicate section: {name}")
        found[name] = (start, body_start, end)
    return found


def replace_or_insert_section(
    text: str,
    section: str,
    content: str,
    required_sections: list[str],
) -> str:
    """Replace one canonical section body or insert a missing section in order."""
    spans = canonical_section_map(text, required_sections)
    body = content.rstrip() + "\n\n"
    if section in spans:
        _, body_start, end = spans[section]
        return text[:body_start] + body + text[end:]

    section_index = required_sections.index(section)
    for later in required_sections[section_index + 1 :]:
        if later in spans:
            insert_at = spans[later][0]
            prefix = text[:insert_at].rstrip() + "\n\n"
            return prefix + f"## {section}\n{body}" + text[insert_at:]
    suffix = text.rstrip() + "\n\n"
    return suffix + f"## {section}\n{body}"


def unfinished_sections(text: str, required_sections: list[str]) -> list[str]:
    """Return required sections that are missing or still contain no content."""
    spans = canonical_section_map(text, required_sections)
    missing: list[str] = []
    for section in required_sections:
        if section not in spans:
            missing.append(section)
            continue
        _, body_start, end = spans[section]
        body = text[body_start:end].replace(EMPTY_SECTION_MARKER, "").strip()
        if not body:
            missing.append(section)
    return missing


def ensure_decision_log(
    *,
    path: Path,
    metadata_lines: list[str],
) -> None:
    """Create an empty canonical decision log without inventing a decision."""
    if path.exists():
        return
    lines = metadata_lines + [
        "# Decision Log",
        "",
        "| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    atomic_write_text(path, "\n".join(lines).rstrip() + "\n")


def split_markdown_table_row(row: str) -> list[str]:
    """Split one Markdown table row while honoring escaped pipe characters."""
    stripped = row.strip()
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("decision row must contain exactly one line")
    if not stripped.startswith("|") or not stripped.endswith("|"):
        raise ValueError("decision row must start and end with `|`")
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in stripped[1:-1]:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            current.append(char)
            escaped = True
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def upsert_decision_row(text: str, row: str) -> str:
    """Append or replace one validated decision-log row by DEC ID."""
    cells = split_markdown_table_row(row)
    if len(cells) != 9:
        raise ValueError(f"decision row must contain 9 cells, found {len(cells)}")
    decision_id = cells[0]
    if not DECISION_ID_PATTERN.fullmatch(decision_id):
        raise ValueError("decision row ID must match DEC-### or DEC-####")
    if any(not cell for cell in cells):
        raise ValueError("decision row cells must not be empty")

    normalized = "| " + " | ".join(cells) + " |"
    lines = text.rstrip().splitlines()
    matches: list[int] = []
    for index, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        try:
            existing_cells = split_markdown_table_row(line)
        except ValueError:
            continue
        if existing_cells and existing_cells[0] == decision_id:
            matches.append(index)
    if len(matches) > 1:
        raise ValueError(f"decision log contains duplicate ID: {decision_id}")
    if matches:
        lines[matches[0]] = normalized
    else:
        lines.append(normalized)
    return "\n".join(lines).rstrip() + "\n"


def preflight_state_action(
    state_args: argparse.Namespace | None,
    skill_name: str,
    workspace: str,
    artifact_path: str,
) -> int:
    """Validate a requested state transition without applying it yet."""
    if state_args is None or not skill_name:
        return 0
    if not any(
        getattr(state_args, name, False)
        for name in ("state_check", "begin_state", "complete_state")
    ):
        return 0
    preflight = copy.copy(state_args)
    preflight.state_check = True
    preflight.begin_state = False
    preflight.complete_state = False
    return run_state_action(preflight, skill_name, workspace, artifact_path)


def emit_profile_report(
    *,
    title: str,
    files: list[Path],
    required_sections: list[str],
    keywords: list[str],
    prompts: list[str],
    summary_limit: int,
    flow_mode: str,
    feature: str,
    artifact_name: str,
    workspace: str,
    emit_template: bool,
    emit_decision_log_entry: bool,
    write: bool,
    skill_name: str = "",
    state_args: argparse.Namespace | None = None,
    document_title: str | None = None,
) -> int:
    """Emit and optionally write the standardized artifact-profile report."""
    # Route outputs according to the SDLC phase: implementation artifacts go to
    # `specs/`, while refinement/planning/QA artifacts go to `specs-refiniment/`.
    base_path = namespace_from_workspace(workspace)
    artifact_path = f"{base_path}/{feature}/{artifact_name}"
    decision_log_path = f"{base_path}/{feature}/decision-log.md"
    state_file_path = f"{base_path}/{feature}/state.toon"

    section = getattr(state_args, "section", None) if state_args is not None else None
    finalize = bool(getattr(state_args, "finalize", False)) if state_args is not None else False
    decision_row = bool(getattr(state_args, "decision_row", False)) if state_args is not None else False
    stdin_action = bool(section or finalize or decision_row)

    if stdin_action:
        artifact_file = Path(artifact_path)
        decision_file = Path(decision_log_path)
        decision_metadata = artifact_metadata_lines(
            feature=feature,
            artifact_name="decision-log.md",
            artifact_path=decision_log_path,
            workspace=workspace,
            skill_name=skill_name,
            flow_mode=flow_mode,
            decision_log_path=decision_log_path,
            state_file_path=state_file_path,
            state_args=state_args,
        )

        try:
            if section:
                if section not in required_sections:
                    choices = ", ".join(required_sections)
                    raise ValueError(f"unknown section {section!r}; expected one of: {choices}")
                content = validate_section_content(sys.stdin.read())
                if artifact_file.exists():
                    artifact_text = read_text(artifact_file)
                else:
                    metadata = artifact_metadata_lines(
                        feature=feature,
                        artifact_name=artifact_name,
                        artifact_path=artifact_path,
                        workspace=workspace,
                        skill_name=skill_name,
                        flow_mode=flow_mode,
                        decision_log_path=decision_log_path,
                        state_file_path=state_file_path,
                        state_args=state_args,
                        status="draft",
                    )
                    artifact_text = "\n".join(metadata).rstrip() + "\n\n" + scaffold_body(
                        artifact_name, required_sections, document_title
                    )
                updated = replace_or_insert_section(artifact_text, section, content, required_sections)
                updated = refreshed_artifact_metadata(
                    text=updated,
                    feature=feature,
                    artifact_name=artifact_name,
                    artifact_path=artifact_path,
                    workspace=workspace,
                    skill_name=skill_name,
                    flow_mode=flow_mode,
                    decision_log_path=decision_log_path,
                    state_file_path=state_file_path,
                    state_args=state_args,
                    status="draft",
                )
                state_rc = preflight_state_action(state_args, skill_name, workspace, artifact_path)
                if state_rc:
                    return state_rc
                atomic_write_text(artifact_file, updated)
                ensure_decision_log(path=decision_file, metadata_lines=decision_metadata)
                if state_args is not None:
                    state_rc = run_state_action(state_args, skill_name, workspace, artifact_path)
                    if state_rc:
                        return state_rc
                remaining = unfinished_sections(updated, required_sections)
                print(f"Wrote section {section!r}: {artifact_file}")
                print("Remaining sections: " + (", ".join(remaining) if remaining else "none; run --finalize"))
                return 0

            if decision_row:
                row = sys.stdin.read().strip()
                if decision_file.exists():
                    decision_text = read_text(decision_file)
                else:
                    decision_text = "\n".join(
                        decision_metadata
                        + [
                            "# Decision Log",
                            "",
                            "| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |",
                            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                        ]
                    ).rstrip() + "\n"
                updated_decision = upsert_decision_row(decision_text, row)
                state_rc = preflight_state_action(state_args, skill_name, workspace, artifact_path)
                if state_rc:
                    return state_rc
                atomic_write_text(decision_file, updated_decision)
                if state_args is not None:
                    state_rc = run_state_action(state_args, skill_name, workspace, artifact_path)
                    if state_rc:
                        return state_rc
                print(f"Wrote decision row: {decision_file}")
                return 0

            if not artifact_file.exists():
                raise ValueError(f"cannot finalize missing artifact: {artifact_file}")
            artifact_text = read_text(artifact_file)
            remaining = unfinished_sections(artifact_text, required_sections)
            if remaining:
                raise ValueError("cannot finalize; unfinished sections: " + ", ".join(remaining))
            updated = artifact_text.replace(EMPTY_SECTION_MARKER, "")
            updated = refreshed_artifact_metadata(
                text=updated,
                feature=feature,
                artifact_name=artifact_name,
                artifact_path=artifact_path,
                workspace=workspace,
                skill_name=skill_name,
                flow_mode=flow_mode,
                decision_log_path=decision_log_path,
                state_file_path=state_file_path,
                state_args=state_args,
                status=getattr(state_args, "artifact_status", None) or "review",
            )
            state_rc = preflight_state_action(state_args, skill_name, workspace, artifact_path)
            if state_rc:
                return state_rc
            atomic_write_text(artifact_file, updated)
            ensure_decision_log(path=decision_file, metadata_lines=decision_metadata)
            write_indexes_for_roots([Path(base_path)])
            if state_args is not None:
                state_rc = run_state_action(state_args, skill_name, workspace, artifact_path)
                if state_rc:
                    return state_rc
            print(f"Finalized artifact: {artifact_file}")
            return 0
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2

    if state_args is not None and skill_name:
        state_rc = run_state_action(state_args, skill_name, workspace, artifact_path)
        if state_rc:
            return state_rc

    # Header metadata is printed first so an agent can decide where the output
    # belongs without reading the entire generated report.
    print(f"# {title}")
    print()
    print(f"- Flow mode: {flow_mode}")
    print(f"- Target artifact: {artifact_path}")
    print(f"- Decision log: {decision_log_path}")
    print(f"- State file: {state_file_path}")
    print("- Artifact metadata schema: ai-sdlc-artifact-metadata/v1")

    # Flow mode changes both summary size and missing-section semantics. Keep
    # this branch centralized so individual skills do not drift.
    if flow_mode == "quick":
        print("- Mode behavior: compress aggressively, use recommended defaults, ask only blocking-risk questions.")
        effective_summary_limit = min(summary_limit, 4)
    elif flow_mode == "full":
        print("- Mode behavior: inspect more evidence, treat missing required structure as blockers, verify traceability before finalizing.")
        effective_summary_limit = max(summary_limit, 8)
    else:
        print("- Mode behavior: default skill behavior.")
        effective_summary_limit = summary_limit
    print()

    # Input accounting gives cheap context about source size and structure
    # before the compressed summary consumes tokens.
    if not files:
        print("- Input files: none provided")
    else:
        print("## Inputs")
        for path in files:
            text = read_text(path)
            print(f"- {path}: {len(text.split())} words, {len(headings(text))} headings")
        print()

    # Combine only existing files. Missing paths remain visible through the
    # input list while keeping the report command tolerant during exploration.
    combined = "\n\n".join(read_text(path) for path in files if path.is_file())
    if combined:
        # Preserve a short narrative summary, trace IDs, open markers, and
        # keyword counts: these are the high-value tokens for downstream work.
        print("## Compact Summary")
        for sentence in first_sentences(combined, effective_summary_limit):
            print(f"- {sentence}")
        print()

        ids = sorted(set(m.group(0).upper() for m in ID_PATTERN.finditer(combined)))
        blockers = sorted(set(m.group(0).upper() for m in TODO_PATTERN.finditer(combined)))
        if ids:
            print("## Trace IDs")
            print("- " + ", ".join(ids[:50]))
            print()
        if blockers:
            print("## Open Markers")
            print("- " + ", ".join(blockers))
            print()
        hits = count_keywords(combined, keywords)
        if hits:
            print("## Keyword Signals")
            for keyword, count in hits:
                print(f"- {keyword}: {count}")
            print()

    if required_sections:
        # Required-section checks turn vague source artifacts into explicit gap
        # handling instructions for quick/full flow.
        print("## Required Structure")
        missing: list[str] = []
        if combined:
            for section, ok in section_presence(combined, required_sections):
                if not ok:
                    missing.append(section)
                print(f"- [{'x' if ok else ' '}] {section}")
        else:
            for section in required_sections:
                missing.append(section)
                print(f"- [ ] {section}")
        print()
        if missing:
            print("## Missing Section Handling")
            if flow_mode == "quick":
                print("- Use documented assumptions for missing non-blocking sections and record material assumptions in decision-log.md.")
                print("- Ask only when a missing section creates product, security, compliance, data-loss, or irreversible implementation risk.")
            elif flow_mode == "full":
                print("- Treat missing required sections as blockers until clarified, sourced, or explicitly accepted as assumptions.")
                print("- Add decision-log.md entries for accepted assumptions or scope-affecting defaults.")
            else:
                print("- Follow the skill clarification rules for missing required sections.")
            print("- Missing: " + ", ".join(missing))
            print()

    if prompts:
        # Skill wrappers provide domain-specific next actions; the helper adds
        # flow-specific closing guidance so behavior stays consistent.
        print("## Next Actions")
        for prompt in prompts:
            print(f"- {prompt}")
        if flow_mode == "quick":
            print("- Prefer a concise deliverable with explicit assumptions over a clarification loop.")
        elif flow_mode == "full":
            print("- Verify traceability, decision-log coverage, and validation evidence before final output.")
        print()

    decision_log_lines = [
        "| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        f"| DEC-001 | YYYY-MM-DD | proposed | TBD | TBD | {artifact_path} inputs | quick/default/full flow options | {artifact_path} | TBD |",
    ]
    decision_log_metadata = artifact_metadata_lines(
        feature=feature,
        artifact_name="decision-log.md",
        artifact_path=decision_log_path,
        workspace=workspace,
        skill_name=skill_name,
        flow_mode=flow_mode,
        decision_log_path=decision_log_path,
        state_file_path=state_file_path,
        state_args=state_args,
    )
    template_lines = artifact_metadata_lines(
        feature=feature,
        artifact_name=artifact_name,
        artifact_path=artifact_path,
        workspace=workspace,
        skill_name=skill_name,
        flow_mode=flow_mode,
        decision_log_path=decision_log_path,
        state_file_path=state_file_path,
        state_args=state_args,
    )
    template_lines.extend([f"# {artifact_name}", ""])
    for section in required_sections:
        # Artifact skeleton contents differ by flow so quick outputs capture
        # assumptions, while full outputs explicitly track blockers.
        template_lines.append(f"## {section}")
        if flow_mode == "quick":
            template_lines.extend(["- Assumption/default: TBD", "- Evidence: TBD"])
        elif flow_mode == "full":
            template_lines.extend(["- Confirmed facts: TBD", "- Evidence: TBD", "- Open questions/blockers: TBD"])
        else:
            template_lines.append("- TBD")
        template_lines.append("")

    if write:
        # `--write` materializes the routed artifact and creates the decision log
        # only if absent, preserving any existing traceability history.
        artifact_file = Path(artifact_path)
        artifact_file.parent.mkdir(parents=True, exist_ok=True)
        artifact_file.write_text("\n".join(template_lines).rstrip() + "\n", encoding="utf-8")
        decision_file = Path(decision_log_path)
        if not decision_file.exists():
            decision_file.write_text(
                "\n".join(decision_log_metadata).rstrip() + "\n# Decision Log\n\n" + "\n".join(decision_log_lines) + "\n",
                encoding="utf-8",
            )
        index_files = write_indexes_for_roots([Path(base_path)])
        print("## Written Files")
        print(f"- {artifact_file}")
        print(f"- {decision_file}")
        for toon_path, md_path in index_files:
            print(f"- {toon_path}")
            print(f"- {md_path}")
        print()

    if emit_decision_log_entry:
        # `--emit-decision-log-entry` is useful when the agent wants a row to
        # paste or adapt without writing files.
        print("## Decision Log Entry")
        for line in decision_log_lines:
            print(line)
        print()

    if emit_template:
        # `--emit-template` keeps skeleton generation deterministic and avoids
        # retyping the same artifact shape in prompts.
        print("## Artifact Template")
        for line in template_lines:
            print(line)
    return 0


def build_parser(description: str) -> argparse.ArgumentParser:
    """Build the common CLI shared by artifact-profile wrapper scripts."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("files", nargs="*", type=Path, help="Markdown or text artifacts to compress")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--summary-limit", type=int, default=5)
    parser.add_argument("--quick-flow", action="store_true", help="Compress aggressively and minimize questions")
    parser.add_argument("--full-flow", action="store_true", help="Use stricter gap handling and verification prompts")
    parser.add_argument("--emit-template", action="store_true", help="Emit the target Markdown artifact template")
    parser.add_argument("--emit-decision-log-entry", action="store_true", help="Emit a canonical decision-log.md row")
    parser.add_argument("--write", action="store_true", help="Write the target artifact template and create decision-log.md if missing")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--section", help="Read one named section body from stdin and write it into the routed artifact")
    action.add_argument("--finalize", action="store_true", help="Validate all required sections and finalize the routed artifact")
    action.add_argument("--decision-row", action="store_true", help="Read one nine-cell decision-log Markdown row from stdin")
    parser.add_argument("--artifact-status", help="Metadata status; finalize defaults to review")
    parser.add_argument("--artifact-owner", help="Metadata owner; updates preserve the existing owner")
    parser.add_argument("--artifact-tag", action="append", default=[], help="Extra metadata tag; repeat for multiple tags")
    add_state_arguments(parser)
    return parser


def flow_mode(args: argparse.Namespace) -> str:
    """Resolve flow precedence; full flow wins when both flags are supplied."""
    if getattr(args, "full_flow", False):
        return "full"
    if getattr(args, "quick_flow", False):
        return "quick"
    return "default"
