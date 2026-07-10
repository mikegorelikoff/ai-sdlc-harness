#!/usr/bin/env python3
"""Build compact, evidence-backed TOON context packs for AI SDLC skills.

Markdown artifacts remain the source of truth.  This module creates a bounded
read projection containing exact source excerpts and precise follow-up reads;
it never summarizes prose or writes source artifacts.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path


CONTEXT_SCHEMA = "ai-sdlc-context/v1"
ID_RE = re.compile(
    r"\b(?:(?:REQ|AC|US|TC|TASK|RISK|DEC|EPIC)-\d{2,4}|T\d{3,4})\b",
    re.IGNORECASE,
)
OPEN_RE = re.compile(r"\b(?:TODO|TBD|FIXME|OPEN QUESTION|DECISION REQUIRED|BLOCKED|BLOCKER)\b", re.IGNORECASE)
SECURITY_RE = re.compile(r"\b(?:security|authorization|authentication|secret|privacy|compliance|data[- ]loss)\b", re.IGNORECASE)
VALIDATION_RE = re.compile(r"\b(?:validation|validate|test|check|signoff|evidence|passed|failed)\b", re.IGNORECASE)
DECISION_RE = re.compile(r"\b(?:accepted|approved|proposed|rejected|superseded|decision)\b", re.IGNORECASE)
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


@dataclass(frozen=True)
class SourceDocument:
    """One context source with stable content identity."""

    path: Path
    display_path: str
    text: str
    sha256: str
    status: str = "current"


@dataclass(frozen=True)
class Evidence:
    """An exact source excerpt ranked for task relevance."""

    kind: str
    identifier: str
    source: str
    section: str
    line: int
    priority: int
    text: str


@dataclass(frozen=True)
class Gap:
    """A deterministic missing/open signal."""

    kind: str
    source: str
    section: str
    blocking: str
    detail: str


def estimate_tokens(text: str) -> int:
    """Return a conservative, model-independent token estimate."""
    words = len(re.findall(r"\S+", text))
    return max(
        math.ceil(len(text) / 4),
        math.ceil(words * 4 / 3),
        math.ceil(len(text.encode("utf-8")) / 4),
    )


def toon_row(values: list[object] | tuple[object, ...]) -> str:
    """Serialize one TOON table row using CSV quoting without data loss."""
    output = io.StringIO()
    csv.writer(output, lineterminator="", quoting=csv.QUOTE_MINIMAL).writerow(
        [str(value).replace("\r", " ").replace("\n", " ") for value in values]
    )
    return output.getvalue()


def toon_scalar(value: object) -> str:
    """Serialize a scalar safely on one TOON line."""
    text = str(value).replace("\r", " ").replace("\n", " ")
    if not text or text != text.strip() or any(char in text for char in ":,#[]{}\""):
        return json.dumps(text, ensure_ascii=False)
    return text


def positive_int(value: str) -> int:
    """Argparse type for positive context budgets."""
    parsed = int(value)
    if parsed <= 0:
        raise ValueError("context budget must be positive")
    return parsed


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _source(path: Path, root: Path) -> SourceDocument:
    if not path.is_file():
        return SourceDocument(path, _display_path(path, root), "", "", "missing")
    text = path.read_text(encoding="utf-8", errors="replace")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return SourceDocument(path, _display_path(path, root), text, digest)


def _feature_aliases(feature: str) -> set[str]:
    aliases = {feature}
    if re.match(r"^\d{3}-", feature):
        aliases.add(feature.split("-", 1)[1])
    return aliases


def _index_artifact_paths(index: Path, features: set[str], root: Path) -> list[Path]:
    """Read artifact paths from the compact index without opening every body."""
    if not index.is_file():
        return []
    paths: list[Path] = []
    in_artifacts = False
    columns: list[str] = []
    for raw in index.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.rstrip()
        if line.startswith("artifacts["):
            in_artifacts = True
            header = line.split("{", 1)[1].split("}", 1)[0]
            columns = [part.strip() for part in header.split(",")]
            continue
        if in_artifacts and not line.startswith("  "):
            in_artifacts = False
        if not in_artifacts or not line.startswith("  "):
            continue
        values = next(csv.reader([line.strip()]))
        row = dict(zip(columns, values))
        if row.get("feature") not in features or not row.get("path"):
            continue
        candidate = Path(row["path"])
        paths.append(candidate if candidate.is_absolute() else root / candidate)
    return paths


def resolve_sources(
    files: list[Path], *, feature: str, workspace: str, root: Path
) -> list[SourceDocument]:
    """Resolve explicit inputs first, otherwise use indexes and feature folders."""
    candidates: list[Path] = []
    if files:
        candidates.extend(path if path.is_absolute() else root / path for path in files)
    else:
        aliases = _feature_aliases(feature)
        roots = [root / ("specs" if workspace == "implementation" else "specs-refiniment")]
        if workspace == "implementation":
            roots.append(root / "specs-refiniment")
        for workspace_root in roots:
            candidates.extend(_index_artifact_paths(workspace_root / "specs-index.toon", aliases, root))
        if not candidates:
            for workspace_root in roots:
                for alias in aliases:
                    feature_dir = workspace_root / alias
                    if feature_dir.is_dir():
                        candidates.extend(sorted(feature_dir.glob("*.md")))

    # State and decisions are cheap, high-value context even when body inputs
    # were supplied explicitly. Add only feature-local paths that exist.
    for base in ("specs" if workspace == "implementation" else "specs-refiniment",):
        for alias in _feature_aliases(feature):
            for name in ("state.toon", "decision-log.md", "plan.toon"):
                auxiliary = root / base / alias / name
                if auxiliary.is_file():
                    candidates.append(auxiliary)
    if workspace == "implementation":
        for alias in _feature_aliases(feature):
            for name in ("state.toon", "decision-log.md"):
                auxiliary = root / "specs-refiniment" / alias / name
                if auxiliary.is_file():
                    candidates.append(auxiliary)

    unique: list[Path] = []
    seen: set[str] = set()
    for path in candidates:
        key = str(path.resolve())
        if key not in seen and ".ai-sdlc" not in path.parts:
            seen.add(key)
            unique.append(path)
    return [_source(path, root) for path in unique]


def _line_sections(text: str) -> list[tuple[int, str, str]]:
    """Return source lines with their nearest Markdown section."""
    rows: list[tuple[int, str, str]] = []
    section = "document"
    fence_char = ""
    fence_length = 0
    for number, raw in enumerate(text.splitlines(), 1):
        fence = FENCE_RE.match(raw)
        if fence:
            token = fence.group(1)
            if not fence_char:
                fence_char, fence_length = token[0], len(token)
            elif token[0] == fence_char and len(token) >= fence_length:
                fence_char, fence_length = "", 0
            continue
        heading = HEADING_RE.match(raw) if not fence_char else None
        if heading:
            section = heading.group(2).strip()
            continue
        stripped = raw.strip()
        if stripped and stripped not in {"---"} and not stripped.startswith("artifact_metadata:"):
            rows.append((number, section, stripped))
    return rows


def _kind_priority(line: str, identifiers: list[str], keywords: list[str]) -> tuple[str, int] | None:
    if OPEN_RE.search(line):
        return "blocker", 0
    if DECISION_RE.search(line) and (identifiers or line.startswith("| DEC-")):
        return "decision", 1
    if SECURITY_RE.search(line):
        return "security", 2
    if VALIDATION_RE.search(line) and (identifiers or "`" in line or line.startswith("-")):
        return "validation", 2
    if identifiers:
        return "trace", 3
    lowered = line.lower()
    if any(keyword.lower() in lowered for keyword in keywords):
        return "skill_signal", 4
    return None


def extract_context(
    sources: list[SourceDocument], *, required_sections: list[str], keywords: list[str]
) -> tuple[list[Evidence], list[Gap], list[str]]:
    """Extract exact evidence, structural gaps, and the complete trace ID set."""
    evidence: list[Evidence] = []
    gaps: list[Gap] = []
    all_ids: set[str] = set()
    seen_evidence: set[tuple[str, int, str]] = set()
    for source in sources:
        if source.status != "current":
            gaps.append(Gap("missing_source", source.display_path, "document", "yes", "source file is missing"))
            continue
        rows = _line_sections(source.text)
        sections = {section.lower() for _, section, _ in rows}
        if source.path.suffix.lower() == ".md" and source.path.name != "decision-log.md":
            missing = [required for required in required_sections if required.lower() not in sections]
            if missing:
                gaps.append(
                    Gap(
                        "missing_sections",
                        source.display_path,
                        "document",
                        "no",
                        "headings not present: " + "/".join(missing),
                    )
                )
        for number, section, line in rows:
            identifiers = sorted({match.group(0).upper() for match in ID_RE.finditer(line)})
            all_ids.update(identifiers)
            signal = _kind_priority(line, identifiers, keywords)
            if signal is None:
                continue
            kind, priority = signal
            excerpt = line[:240]
            key = (source.display_path, number, kind)
            if key in seen_evidence:
                continue
            seen_evidence.add(key)
            evidence.append(
                Evidence(kind, "/".join(identifiers), source.display_path, section, number, priority, excerpt)
            )

        # Preserve one exact narrative entry per relevant section after strong
        # evidence has been collected. These are lowest priority and disappear
        # first when the budget is tight.
        seen_sections: set[str] = set()
        for number, section, line in rows:
            if section in seen_sections or section == "document":
                continue
            if required_sections and section.lower() not in {value.lower() for value in required_sections}:
                continue
            seen_sections.add(section)
            evidence.append(Evidence("section_context", "", source.display_path, section, number, 5, line[:240]))
    # Round-robin sources inside each priority tier. This prevents a long first
    # artifact from consuming the whole budget before another source appears.
    ordered: list[Evidence] = []
    for priority in sorted({item.priority for item in evidence}):
        by_source: dict[str, list[Evidence]] = {}
        for item in evidence:
            if item.priority == priority:
                by_source.setdefault(item.source, []).append(item)
        while any(by_source.values()):
            for source_name in sorted(by_source):
                if by_source[source_name]:
                    ordered.append(by_source[source_name].pop(0))
    return ordered, gaps, sorted(all_ids)


def _fingerprint(
    sources: list[SourceDocument], *, skill: str, flow_mode: str, budget_tokens: int,
    required_sections: list[str], keywords: list[str]
) -> str:
    digest = hashlib.sha256()
    for value in (CONTEXT_SCHEMA, skill, flow_mode, str(budget_tokens), *required_sections, *keywords):
        digest.update(value.encode("utf-8"))
        digest.update(b"\0")
    for source in sources:
        digest.update(source.display_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(source.sha256.encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def _render(
    *, feature: str, skill: str, workspace: str, flow_mode: str,
    budget_tokens: int, fingerprint: str, cache_status: str,
    sources: list[SourceDocument], selected: list[Evidence], omitted: list[Evidence],
    gaps: list[Gap], trace_ids: list[str], budget_status: str,
) -> str:
    lines = [
        f"schema: {CONTEXT_SCHEMA}",
        f"feature: {toon_scalar(feature)}",
        f"skill: {toon_scalar(skill)}",
        f"workspace: {workspace}",
        f"flow_mode: {flow_mode}",
        f"budget_tokens: {budget_tokens}",
        "estimated_tokens: __ESTIMATED__",
        f"budget_status: {budget_status}",
        f"cache_status: {cache_status}",
        f"fingerprint: {fingerprint}",
        f"trace_ids: {toon_scalar(';'.join(trace_ids))}",
        "",
        f"sources[{len(sources)}]{{path,sha256,status}}:",
    ]
    for source in sources:
        lines.append("  " + toon_row((source.display_path, source.sha256[:16], source.status)))
    lines.extend(["", f"anchors[{len(selected)}]{{kind,id,source,section,line,priority,text}}:"])
    for item in selected:
        lines.append(
            "  "
            + toon_row(
                (item.kind, item.identifier, item.source, item.section, item.line, item.priority, item.text)
            )
        )
    lines.extend(["", f"gaps[{len(gaps)}]{{kind,source,section,blocking,detail}}:"])
    for gap in gaps:
        lines.append("  " + toon_row((gap.kind, gap.source, gap.section, gap.blocking, gap.detail)))
    grouped_items: dict[tuple[str, str, str], list[Evidence]] = {}
    for item in omitted:
        grouped_items.setdefault((item.source, item.section, item.kind), []).append(item)
    grouped_reads: list[tuple[str, str, str, int, int, set[str]]] = []
    for (source, section, kind), items in sorted(grouped_items.items()):
        cluster_start = cluster_end = items[0].line
        cluster_ids: set[str] = set(items[0].identifier.split("/")) if items[0].identifier else set()
        for item in sorted(items[1:], key=lambda value: value.line):
            # Keep rereads precise: nearby evidence can share a range, but a
            # distant signal in the same section starts a new targeted read.
            if item.line <= cluster_end + 8:
                cluster_end = item.line
                if item.identifier:
                    cluster_ids.update(item.identifier.split("/"))
                continue
            grouped_reads.append((source, section, kind, cluster_start, cluster_end, cluster_ids))
            cluster_start = cluster_end = item.line
            cluster_ids = set(item.identifier.split("/")) if item.identifier else set()
        grouped_reads.append((source, section, kind, cluster_start, cluster_end, cluster_ids))
    lines.extend(["", f"next_reads[{len(grouped_reads)}]{{source,section,line_start,line_end,reason}}:"])
    for source, section, kind, start, end, ids in grouped_reads:
        reason = f"budget omitted {kind}" + (f" {'/'.join(sorted(ids))}" if ids else "")
        lines.append("  " + toon_row((source, section, start, end, reason)))
    text = "\n".join(lines).rstrip() + "\n"
    estimate = estimate_tokens(text.replace("__ESTIMATED__", "0"))
    return text.replace("__ESTIMATED__", str(estimate))


def build_context_pack(
    *, files: list[Path], feature: str, skill: str, workspace: str,
    flow_mode: str, budget_tokens: int, required_sections: list[str],
    keywords: list[str], root: Path | None = None, cache_status: str = "off",
) -> tuple[str, str, list[SourceDocument]]:
    """Build one bounded TOON pack and return text, fingerprint, and sources."""
    root = (root or Path.cwd()).resolve()
    sources = resolve_sources(files, feature=feature, workspace=workspace, root=root)
    evidence, gaps, trace_ids = extract_context(sources, required_sections=required_sections, keywords=keywords)
    fingerprint = _fingerprint(
        sources, skill=skill, flow_mode=flow_mode, budget_tokens=budget_tokens,
        required_sections=required_sections, keywords=keywords,
    )

    selected: list[Evidence] = []
    omitted: list[Evidence] = []
    # Greedy priority order with an exact final-size check. The full render is
    # deliberately used here because TOON headers and follow-up reads also cost
    # context tokens.
    for item in evidence:
        candidate = selected + [item]
        trial = _render(
            feature=feature, skill=skill, workspace=workspace, flow_mode=flow_mode,
            budget_tokens=budget_tokens, fingerprint=fingerprint, cache_status=cache_status,
            sources=sources, selected=candidate, omitted=omitted, gaps=gaps,
            trace_ids=trace_ids, budget_status="within_budget",
        )
        if estimate_tokens(trial) <= budget_tokens:
            selected.append(item)
        else:
            omitted.append(item)

    status = "next_reads_required" if omitted else "within_budget"
    text = _render(
        feature=feature, skill=skill, workspace=workspace, flow_mode=flow_mode,
        budget_tokens=budget_tokens, fingerprint=fingerprint, cache_status=cache_status,
        sources=sources, selected=selected, omitted=omitted, gaps=gaps,
        trace_ids=trace_ids, budget_status=status,
    )
    while selected and estimate_tokens(text) > budget_tokens:
        omitted.insert(0, selected.pop())
        status = "next_reads_required"
        text = _render(
            feature=feature, skill=skill, workspace=workspace, flow_mode=flow_mode,
            budget_tokens=budget_tokens, fingerprint=fingerprint, cache_status=cache_status,
            sources=sources, selected=selected, omitted=omitted, gaps=gaps,
            trace_ids=trace_ids, budget_status=status,
        )
    if estimate_tokens(text) > budget_tokens:
        text = text.replace(f"budget_status: {status}", "budget_status: minimum_overflow", 1)
    return text, fingerprint, sources


def context_cache_path(root: Path, workspace: str, feature: str, skill: str) -> Path:
    """Return the derived feature-local context cache path."""
    base = "specs" if workspace == "implementation" else "specs-refiniment"
    return root / base / feature / ".ai-sdlc" / "context" / f"{skill}.toon"


def emit_context_pack(
    *, files: list[Path], feature: str, skill: str, workspace: str,
    flow_mode: str, budget_tokens: int, required_sections: list[str],
    keywords: list[str], cache: bool = False, refresh: bool = False,
    root: Path | None = None,
) -> str:
    """Return a context pack, reusing a fresh explicit cache when requested."""
    root = (root or Path.cwd()).resolve()
    text, fingerprint, _ = build_context_pack(
        files=files, feature=feature, skill=skill, workspace=workspace,
        flow_mode=flow_mode, budget_tokens=budget_tokens,
        required_sections=required_sections, keywords=keywords, root=root,
        cache_status="miss" if cache else "off",
    )
    if not cache:
        return text

    path = context_cache_path(root, workspace, feature, skill)
    if not refresh and path.is_file():
        cached = path.read_text(encoding="utf-8", errors="replace")
        if f"schema: {CONTEXT_SCHEMA}" in cached and f"fingerprint: {fingerprint}" in cached:
            return re.sub(r"^cache_status: .*?$", "cache_status: hit", cached, count=1, flags=re.MULTILINE)

    path.parent.mkdir(parents=True, exist_ok=True)
    refreshed = re.sub(
        r"^cache_status: .*?$", "cache_status: refreshed", text, count=1, flags=re.MULTILINE
    )
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            handle.write(refreshed)
            temp_path = Path(handle.name)
        os.replace(temp_path, path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()
    return refreshed
