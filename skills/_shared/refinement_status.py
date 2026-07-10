#!/usr/bin/env python3
"""Report whether an end-to-end refinement package is complete."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from ai_sdlc_context import toon_row, toon_scalar
from ai_sdlc_paths import (
    first_existing,
    index_toon_path,
    legacy_state_path,
    state_path,
)
from ai_sdlc_specs_index import parse_artifact_metadata
from ai_sdlc_state_machine import STAGES, from_toon


REFINEMENT_STAGES = tuple(stage for stage in STAGES if stage.workspace == "refinement")


@dataclass(frozen=True)
class Issue:
    """One concrete reason the refinement package is incomplete."""

    kind: str
    stage: str
    skill: str
    path: str
    detail: str


def inspect_package(root: Path, feature: str) -> tuple[list[Issue], Path, Path]:
    """Return completeness issues plus the canonical feature and state paths."""
    workspace_root = root / "specs-refiniment"
    feature_root = workspace_root / feature
    canonical_state = state_path(feature, "refinement", root)
    readable_state = first_existing(
        canonical_state,
        legacy_state_path(feature, "refinement", root),
    )
    state: dict[str, object] = {}
    if readable_state.is_file():
        state = from_toon(readable_state.read_text(encoding="utf-8", errors="replace"))
    stage_rows = {
        str(row.get("id", "")): row
        for row in state.get("stages", [])
        if isinstance(row, dict)
    }

    issues: list[Issue] = []
    if not readable_state.is_file():
        issues.append(
            Issue("missing_state", "", "", canonical_state.as_posix(), "lifecycle state is missing")
        )

    expected_paths: list[str] = []
    for stage in REFINEMENT_STAGES:
        artifact = feature_root / stage.artifacts
        expected_paths.append(artifact.relative_to(root).as_posix())
        row = stage_rows.get(stage.stage_id)
        status = str(row.get("status", "")) if row else "missing"
        if status != "done":
            issues.append(
                Issue(
                    "incomplete_stage",
                    stage.stage_id,
                    stage.skill,
                    artifact.relative_to(root).as_posix(),
                    f"status={status}",
                )
            )
        if not artifact.is_file():
            issues.append(
                Issue(
                    "missing_artifact",
                    stage.stage_id,
                    stage.skill,
                    artifact.relative_to(root).as_posix(),
                    "required Markdown artifact is missing",
                )
            )
            continue
        metadata = parse_artifact_metadata(artifact.read_text(encoding="utf-8", errors="replace"))
        if not metadata:
            issues.append(
                Issue(
                    "missing_metadata",
                    stage.stage_id,
                    stage.skill,
                    artifact.relative_to(root).as_posix(),
                    "artifact_metadata is missing",
                )
            )

    decision_log = feature_root / "decision-log.md"
    if not decision_log.is_file():
        issues.append(
            Issue(
                "missing_decision_log",
                "",
                "",
                decision_log.relative_to(root).as_posix(),
                "decision log is missing",
            )
        )

    toon_index = index_toon_path(workspace_root)
    markdown_index = workspace_root / "specs-index.md"
    if not toon_index.is_file():
        issues.append(
            Issue(
                "missing_index",
                "",
                "",
                toon_index.relative_to(root).as_posix(),
                "canonical TOON index is missing",
            )
        )
    if not markdown_index.is_file():
        issues.append(
            Issue(
                "missing_index",
                "",
                "",
                markdown_index.relative_to(root).as_posix(),
                "Markdown index is missing",
            )
        )
    for index in (toon_index, markdown_index):
        if not index.is_file():
            continue
        index_text = index.read_text(encoding="utf-8", errors="replace")
        for expected in expected_paths:
            if expected not in index_text:
                stage = next(
                    stage for stage in REFINEMENT_STAGES if expected.endswith("/" + stage.artifacts)
                )
                issues.append(
                    Issue(
                        "stale_index",
                        stage.stage_id,
                        stage.skill,
                        index.relative_to(root).as_posix(),
                        f"missing artifact entry: {expected}",
                    )
                )

    return issues, feature_root, canonical_state


def next_skill(issues: list[Issue]) -> str:
    """Return the earliest lifecycle skill that can repair an issue."""
    issues_by_stage = {issue.stage for issue in issues if issue.stage}
    for stage in REFINEMENT_STAGES:
        if stage.stage_id in issues_by_stage:
            return stage.skill
    return "refresh refinement decision log and indexes" if issues else "none"


def render_markdown(feature: str, issues: list[Issue], feature_root: Path) -> str:
    """Render a Codex-friendly completion summary."""
    complete_stages = len(
        {
            stage.stage_id
            for stage in REFINEMENT_STAGES
            if not any(issue.stage == stage.stage_id for issue in issues)
        }
    )
    lines = [
        "# Refinement Status",
        "",
        f"- Feature: `{feature}`",
        f"- Package: `{feature_root}`",
        f"- Complete: `{'yes' if not issues else 'no'}`",
        f"- Lifecycle artifacts: `{complete_stages}/{len(REFINEMENT_STAGES)}`",
        f"- Next skill: `{next_skill(issues)}`",
    ]
    if issues:
        lines.extend(["", "## Issues"])
        lines.extend(
            f"- {issue.kind}: `{issue.path}` — {issue.detail}"
            for issue in issues
        )
    return "\n".join(lines).rstrip() + "\n"


def render_toon(feature: str, issues: list[Issue], feature_root: Path) -> str:
    """Render a compact agent-oriented completion summary."""
    complete_stages = len(
        {
            stage.stage_id
            for stage in REFINEMENT_STAGES
            if not any(issue.stage == stage.stage_id for issue in issues)
        }
    )
    lines = [
        "schema: ai-sdlc-refinement-status/v1",
        f"feature: {toon_scalar(feature)}",
        f"package: {toon_scalar(feature_root.as_posix())}",
        f"complete: {'yes' if not issues else 'no'}",
        f"artifact_count: {complete_stages}/{len(REFINEMENT_STAGES)}",
        f"next_skill: {toon_scalar(next_skill(issues))}",
        "",
        f"issues[{len(issues)}]{{kind,stage,skill,path,detail}}:",
    ]
    lines.extend(
        "  " + toon_row((issue.kind, issue.stage, issue.skill, issue.path, issue.detail))
        for issue in issues
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """Parse arguments and print the completion summary to stdout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--format", choices=["markdown", "toon"], default="markdown")
    args = parser.parse_args()

    root = args.root.resolve()
    issues, feature_root, _ = inspect_package(root, args.feature)
    renderer = render_toon if args.format == "toon" else render_markdown
    print(renderer(args.feature, issues, feature_root), end="")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
