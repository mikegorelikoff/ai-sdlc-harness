#!/usr/bin/env python3
"""Build compact TOON and human Markdown indexes for spec workspaces.

The index lets an agent discover feature folders, current lifecycle state, and
artifact metadata without spending tokens opening every Markdown file. The same
scan also writes a readable Markdown table for humans who want to browse the
workspace directly.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from ai_sdlc_paths import (
    INDEX_TOON,
    INTERNAL_DIR,
    first_existing,
    index_toon_path,
    legacy_state_path,
    state_path,
    atomic_write_text,
    authority_root,
    write_lock,
)
from ai_sdlc_state_machine import csv_escape, from_toon


WORKSPACE_ROOTS = ("specs-refiniment", "specs")
INDEX_MD = "specs-index.md"


@dataclass(frozen=True)
class ArtifactEntry:
    """Normalized metadata for one Markdown artifact."""

    feature: str
    workspace: str
    path: str
    artifact: str
    skill: str
    status: str
    flow_mode: str
    updated_at: str
    trace_ids: tuple[str, ...]
    metatags: tuple[str, ...]


@dataclass(frozen=True)
class FeatureEntry:
    """Compact summary of one feature folder."""

    feature: str
    workspace: str
    current_stage: str
    active_skill: str
    flow_mode: str
    updated_at: str
    artifact_count: int
    decision_log: str
    state_file: str
    metatags: tuple[str, ...]


def workspace_for_root(root: Path) -> str:
    """Map a specs root folder to the metadata workspace value."""
    return "implementation" if root.name == "specs" else "refinement"


def parse_scalar(line: str) -> str:
    """Parse a simple YAML scalar from generated metadata frontmatter."""
    value = line.split(":", 1)[1].strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return value


def parse_inline_list(line: str) -> tuple[str, ...]:
    """Parse generated one-line YAML arrays such as `trace_ids: []`."""
    value = line.split(":", 1)[1].strip()
    if value == "[]":
        return ()
    if value.startswith("[") and value.endswith("]"):
        return tuple(item.strip().strip('"') for item in value[1:-1].split(",") if item.strip())
    return ()


def parse_artifact_metadata(text: str) -> dict[str, object]:
    """Extract the repository metadata block from one Markdown artifact."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    block = text[4:end].splitlines()
    if not any(line.strip() == "artifact_metadata:" for line in block):
        return {}

    metadata: dict[str, object] = {"metatags": (), "trace_ids": ()}
    active_list: str | None = None
    for raw_line in block:
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped == "artifact_metadata:":
            continue
        if stripped.startswith("- ") and active_list:
            values = list(metadata.get(active_list, ()))
            values.append(stripped[2:].strip().strip('"'))
            metadata[active_list] = tuple(values)
            continue
        active_list = None
        if ":" not in stripped:
            continue
        key = stripped.split(":", 1)[0]
        if key in {"metatags", "trace_ids", "related_artifacts", "validation"}:
            inline = parse_inline_list(stripped)
            metadata[key] = inline
            if not inline and not stripped.endswith("[]"):
                active_list = key
            continue
        metadata[key] = parse_scalar(stripped)
    return metadata


def trace_ids_from_text(text: str) -> tuple[str, ...]:
    """Fallback trace ID extraction when metadata has not been filled yet."""
    pattern = re.compile(
        r"\b(?:REQ|AC|US|TC|DEC|TASK|RISK|EPIC|GOAL|CAP|WF|BR|SC|NFR|DEP)-\d{2,4}\b",
        re.IGNORECASE,
    )
    return tuple(sorted({match.group(0).upper() for match in pattern.finditer(text)}))


def artifact_entry(path: Path, workspace_root: Path, feature: str) -> ArtifactEntry:
    """Build one artifact index row from Markdown metadata plus fallbacks."""
    text = path.read_text(encoding="utf-8", errors="replace")
    metadata = parse_artifact_metadata(text)
    rel_path = path.resolve().relative_to(workspace_root.parent.resolve()).as_posix()
    workspace = str(metadata.get("workspace") or workspace_for_root(workspace_root))
    tags = tuple(metadata.get("metatags", ())) or ("unindexed",)
    trace_ids = tuple(metadata.get("trace_ids", ())) or trace_ids_from_text(text)
    return ArtifactEntry(
        feature=str(metadata.get("feature") or feature),
        workspace=workspace,
        path=rel_path,
        artifact=str(metadata.get("artifact") or path.name),
        skill=str(metadata.get("skill") or "unknown"),
        status=str(metadata.get("status") or "unknown"),
        flow_mode=str(metadata.get("flow_mode") or "unknown"),
        updated_at=str(metadata.get("updated_at") or ""),
        trace_ids=trace_ids,
        metatags=tags,
    )


def feature_entry(feature_dir: Path, workspace_root: Path, artifacts: list[ArtifactEntry]) -> FeatureEntry:
    """Build a feature summary row from state.toon and artifact entries."""
    workspace = workspace_for_root(workspace_root)
    canonical_state = state_path(feature_dir.name, workspace, workspace_root.parent)
    state_file = first_existing(
        canonical_state,
        legacy_state_path(feature_dir.name, workspace, workspace_root.parent),
    )
    state: dict[str, object] = {}
    if state_file.exists():
        state = from_toon(state_file.read_text(encoding="utf-8"))
    tags = tuple(sorted({tag for artifact in artifacts for tag in artifact.metatags}))
    return FeatureEntry(
        feature=str(state.get("feature") or feature_dir.name),
        workspace=str(state.get("workspace") or workspace),
        current_stage=str(state.get("current_stage") or ""),
        active_skill=str(state.get("active_skill") or ""),
        flow_mode=str(state.get("flow_mode") or ""),
        updated_at=str(state.get("updated_at") or ""),
        artifact_count=len(artifacts),
        decision_log=str(state.get("decision_log") or (feature_dir / "decision-log.md").resolve().relative_to(workspace_root.parent.resolve()).as_posix()),
        state_file=state_file.resolve().relative_to(workspace_root.parent.resolve()).as_posix(),
        metatags=tags,
    )


def scan_workspace(workspace_root: Path) -> tuple[list[FeatureEntry], list[ArtifactEntry]]:
    """Scan one specs workspace and return feature plus artifact rows."""
    features: list[FeatureEntry] = []
    artifacts: list[ArtifactEntry] = []
    if not workspace_root.exists():
        return features, artifacts

    for feature_dir in sorted(
        path for path in workspace_root.iterdir() if path.is_dir() and path.name != INTERNAL_DIR
    ):
        feature_artifacts = [
            artifact_entry(path, workspace_root, feature_dir.name)
            for path in sorted(feature_dir.glob("*.md"))
            if path.name not in {INDEX_MD, INDEX_TOON}
        ]
        artifacts.extend(feature_artifacts)
        features.append(feature_entry(feature_dir, workspace_root, feature_artifacts))
    return features, artifacts


def join_values(values: tuple[str, ...]) -> str:
    """Serialize repeated metadata fields in one TOON-safe cell."""
    return ";".join(values)


def render_toon(workspace_root: Path, features: list[FeatureEntry], artifacts: list[ArtifactEntry]) -> str:
    """Render a compact LLM-oriented specs index in TOON."""
    lines = [
        f"workspace: {workspace_for_root(workspace_root)}",
        f"root: {workspace_root.resolve().relative_to(workspace_root.parent.resolve()).as_posix()}",
        f"updated_at: {date.today().isoformat()}",
        "",
        f"features[{len(features)}]{{feature,workspace,current_stage,active_skill,flow_mode,updated_at,artifact_count,decision_log,state_file,metatags}}:",
    ]
    for feature in features:
        lines.append(
            "  "
            + ",".join(
                csv_escape(value)
                for value in (
                    feature.feature,
                    feature.workspace,
                    feature.current_stage,
                    feature.active_skill,
                    feature.flow_mode,
                    feature.updated_at,
                    feature.artifact_count,
                    feature.decision_log,
                    feature.state_file,
                    join_values(feature.metatags),
                )
            )
        )
    lines.append("")
    lines.append("artifacts[%d]{feature,path,artifact,skill,status,flow_mode,updated_at,trace_ids,metatags}:" % len(artifacts))
    for artifact in artifacts:
        lines.append(
            "  "
            + ",".join(
                csv_escape(value)
                for value in (
                    artifact.feature,
                    artifact.path,
                    artifact.artifact,
                    artifact.skill,
                    artifact.status,
                    artifact.flow_mode,
                    artifact.updated_at,
                    join_values(artifact.trace_ids),
                    join_values(artifact.metatags),
                )
            )
        )
    return "\n".join(lines).rstrip() + "\n"


def md_cell(value: object) -> str:
    """Escape Markdown table cell separators."""
    return str(value).replace("|", "\\|")


def render_markdown(workspace_root: Path, features: list[FeatureEntry], artifacts: list[ArtifactEntry]) -> str:
    """Render a human-readable specs index in Markdown."""
    lines = [
        "# Specs Index",
        "",
        f"- Workspace: `{workspace_for_root(workspace_root)}`",
        f"- Root: `{workspace_root.resolve().relative_to(workspace_root.parent.resolve()).as_posix()}`",
        f"- Updated: `{date.today().isoformat()}`",
        "",
        "## Feature Summary",
        "",
        "| Feature | Current Stage | Active Skill | Flow | Artifacts | Decision Log | State | Tags |",
        "| --- | --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for feature in features:
        lines.append(
            "| "
            + " | ".join(
                md_cell(value)
                for value in (
                    feature.feature,
                    feature.current_stage or "-",
                    feature.active_skill or "-",
                    feature.flow_mode or "-",
                    feature.artifact_count,
                    f"`{feature.decision_log}`",
                    f"`{feature.state_file}`",
                    join_values(feature.metatags) or "-",
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Artifact Index",
            "",
            "| Feature | Artifact | Status | Skill | Flow | Updated | Trace IDs | Tags |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for artifact in artifacts:
        lines.append(
            "| "
            + " | ".join(
                md_cell(value)
                for value in (
                    artifact.feature,
                    f"`{artifact.path}`",
                    artifact.status,
                    artifact.skill,
                    artifact.flow_mode,
                    artifact.updated_at or "-",
                    join_values(artifact.trace_ids) or "-",
                    join_values(artifact.metatags) or "-",
                )
            )
            + " |"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_workspace_index(workspace_root: Path) -> tuple[Path, Path]:
    """Write TOON and Markdown indexes for one workspace root."""
    from ai_sdlc_migrate import migrate_workspace

    root = authority_root(workspace_root)
    from ai_sdlc_safe_io import ensure_directory
    workspace_root = ensure_directory(root, workspace_root)
    migrate_workspace(root, workspace_for_root(workspace_root), apply=True)
    toon_path = index_toon_path(workspace_root)
    md_path = workspace_root / INDEX_MD
    with write_lock(workspace_root / INTERNAL_DIR):
        features, artifacts = scan_workspace(workspace_root)
        atomic_write_text(toon_path, render_toon(workspace_root, features, artifacts))
        atomic_write_text(md_path, render_markdown(workspace_root, features, artifacts))
    return toon_path, md_path


def write_indexes_for_roots(roots: list[Path] | None = None) -> list[tuple[Path, Path]]:
    """Write indexes for every requested workspace root."""
    selected_roots = roots or [Path(root) for root in WORKSPACE_ROOTS]
    return [write_workspace_index(root) for root in selected_roots]


def main() -> int:
    """Parse CLI flags and write specs indexes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        choices=["all", "refinement", "implementation"],
        default="all",
        help="Workspace root to index",
    )
    parser.add_argument("--quick-flow", action="store_true", help="Write indexes with compact local scanning")
    parser.add_argument("--full-flow", action="store_true", help="Write indexes and report both generated files")
    args = parser.parse_args()

    if args.workspace == "refinement":
        roots = [Path("specs-refiniment")]
    elif args.workspace == "implementation":
        roots = [Path("specs")]
    else:
        roots = [Path(root) for root in WORKSPACE_ROOTS]

    for toon_path, md_path in write_indexes_for_roots(roots):
        print(f"Wrote {toon_path}")
        if args.full_flow:
            print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
