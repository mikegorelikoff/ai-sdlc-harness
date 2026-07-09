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
import re
from datetime import date
from pathlib import Path

from ai_sdlc_specs_index import write_indexes_for_roots
from ai_sdlc_state_machine import add_state_arguments, run_state_action


# Common traceability IDs that should survive compression and remain visible to
# the agent after large source artifacts have been summarized.
ID_PATTERN = re.compile(r"\b(?:REQ|AC|US|TC|DEC|TASK|RISK|EPIC)-\d{2,4}\b", re.IGNORECASE)

# Open-work markers that usually require either a question, an assumption, or a
# decision-log entry depending on the active flow mode.
TODO_PATTERN = re.compile(r"\b(?:TODO|TBD|FIXME|OPEN QUESTION|DECISION REQUIRED|BLOCKED)\b", re.IGNORECASE)


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
) -> list[str]:
    """Build canonical frontmatter for every generated skill artifact.

    The metadata block is intentionally verbose enough to let future agents
    route, filter, validate, and trace artifacts without rereading the full
    document body. It does not replace the body, decision log, or state file.
    """
    created_at = date.today().isoformat()
    owner = getattr(state_args, "artifact_owner", "TBD") if state_args is not None else "TBD"
    status = getattr(state_args, "artifact_status", "draft") if state_args is not None else "draft"
    extra_tags = getattr(state_args, "artifact_tag", []) if state_args is not None else []
    tags = unique_tags(
        [
            "ai-sdlc",
            workspace,
            skill_name or "unknown-skill",
            Path(artifact_name).stem,
            status,
            *extra_tags,
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
        "  updated_at: " + yaml_quote(created_at),
        "  trace_ids: []",
        "  related_artifacts: []",
        "  validation: []",
        "  metatags:",
    ]
    lines.extend(f"    - {yaml_quote(tag)}" for tag in tags)
    lines.extend(["---", ""])
    return lines


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
) -> int:
    """Emit and optionally write the standardized artifact-profile report."""
    # Route outputs according to the SDLC phase: implementation artifacts go to
    # `specs/`, while refinement/planning/QA artifacts go to `specs-refiniment/`.
    base_path = namespace_from_workspace(workspace)
    artifact_path = f"{base_path}/{feature}/{artifact_name}"
    decision_log_path = f"{base_path}/{feature}/decision-log.md"
    state_file_path = f"{base_path}/{feature}/state.toon"

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
    parser.add_argument("--artifact-status", default="draft", help="Metadata status for emitted or written artifacts")
    parser.add_argument("--artifact-owner", default="TBD", help="Metadata owner for emitted or written artifacts")
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
