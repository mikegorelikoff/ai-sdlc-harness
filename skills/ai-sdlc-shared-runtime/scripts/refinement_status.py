#!/usr/bin/env python3
"""Report whether an end-to-end refinement package is complete."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from ai_sdlc_artifact_helper import artifact_quality_issues
from ai_sdlc_artifact_profiles import PROFILE_BY_STAGE, required_sections, required_tables
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
    severity: str = "error"


def inspect_package(root: Path, feature: str, gate: str = "default") -> tuple[list[Issue], Path, Path]:
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
        profile = PROFILE_BY_STAGE[stage.stage_id]
        readable_artifact = first_existing(
            artifact,
            *(feature_root / name for name in profile.legacy_names),
        )
        expected_paths.append(readable_artifact.relative_to(root).as_posix())
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
        if not readable_artifact.is_file():
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
        metadata = parse_artifact_metadata(
            readable_artifact.read_text(encoding="utf-8", errors="replace")
        )
        if not metadata:
            issues.append(
                Issue(
                    "missing_metadata",
                    stage.stage_id,
                    stage.skill,
                    readable_artifact.relative_to(root).as_posix(),
                    "artifact_metadata is missing",
                )
            )
            continue
        artifact_flow = str(metadata.get("flow_mode") or "")
        if artifact_flow == "quick":
            issues.append(
                Issue(
                    "compact_artifact",
                    stage.stage_id,
                    stage.skill,
                    readable_artifact.relative_to(root).as_posix(),
                    "complete refinement requires default/full self-contained context",
                )
            )
        elif artifact_flow in {"default", "full"}:
            if gate == "full" and artifact_flow != "full":
                issues.append(
                    Issue("wrong_flow", stage.stage_id, stage.skill, readable_artifact.relative_to(root).as_posix(), "full gate requires flow_mode=full")
                )
            artifact_text = readable_artifact.read_text(encoding="utf-8", errors="replace")
            relative_path = readable_artifact.relative_to(root).as_posix()
            quality_issues = artifact_quality_issues(
                text=artifact_text,
                required_sections=required_sections(profile, artifact_flow),
                flow_mode="full" if gate == "full" else artifact_flow,
                source_paths=[str(value) for value in metadata.get("related_artifacts", ())],
                artifact_path=relative_path,
                max_tokens=24000,
                required_tables=required_tables(profile),
            )
            for quality_issue in quality_issues:
                issues.append(
                    Issue(
                        "weak_artifact",
                        stage.stage_id,
                        stage.skill,
                        relative_path,
                        quality_issue.detail,
                        quality_issue.severity,
                    )
                )
        elif gate == "full":
            issues.append(
                Issue("wrong_flow", stage.stage_id, stage.skill, readable_artifact.relative_to(root).as_posix(), "full gate requires flow_mode=full")
            )
        else:
            issues.append(
                Issue("unknown_flow", stage.stage_id, stage.skill, readable_artifact.relative_to(root).as_posix(), "flow_mode is missing or unknown", "warning")
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
                    stage
                    for stage in REFINEMENT_STAGES
                    if Path(expected).name
                    in {stage.artifacts, *PROFILE_BY_STAGE[stage.stage_id].legacy_names}
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
    issues_by_stage = {issue.stage for issue in issues if issue.stage and issue.severity == "error"}
    for stage in REFINEMENT_STAGES:
        if stage.stage_id in issues_by_stage:
            return stage.skill
    return "refresh refinement decision log and indexes" if issues else "none"


def render_markdown(feature: str, issues: list[Issue], feature_root: Path) -> str:
    """Render a Codex-friendly completion summary."""
    blocking = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]
    complete_stages = len(
        {
            stage.stage_id
            for stage in REFINEMENT_STAGES
            if not any(issue.stage == stage.stage_id for issue in blocking)
        }
    )
    lines = [
        "# Refinement Status",
        "",
        f"- Feature: `{feature}`",
        f"- Package: `{feature_root}`",
        f"- Complete: `{'yes' if not blocking else 'no'}`",
        f"- Lifecycle artifacts: `{complete_stages}/{len(REFINEMENT_STAGES)}`",
        f"- Blocking issues: `{len(blocking)}`",
        f"- Warnings: `{len(warnings)}`",
        f"- Next skill: `{next_skill(blocking)}`",
    ]
    if issues:
        lines.extend(["", "## Issues"])
        lines.extend(
            f"- {issue.severity}/{issue.kind}: `{issue.path}` — {issue.detail}"
            for issue in issues
        )
    return "\n".join(lines).rstrip() + "\n"


def render_toon(feature: str, issues: list[Issue], feature_root: Path) -> str:
    """Render a compact agent-oriented completion summary."""
    blocking = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]
    complete_stages = len(
        {
            stage.stage_id
            for stage in REFINEMENT_STAGES
            if not any(issue.stage == stage.stage_id for issue in blocking)
        }
    )
    lines = [
        "schema: ai-sdlc-refinement-status/v1",
        f"feature: {toon_scalar(feature)}",
        f"package: {toon_scalar(feature_root.as_posix())}",
        f"complete: {'yes' if not blocking else 'no'}",
        f"artifact_count: {complete_stages}/{len(REFINEMENT_STAGES)}",
        f"blocking_count: {len(blocking)}",
        f"warning_count: {len(warnings)}",
        f"next_skill: {toon_scalar(next_skill(blocking))}",
        "",
        f"issues[{len(issues)}]{{severity,kind,stage,skill,path,detail}}:",
    ]
    lines.extend(
        "  " + toon_row((issue.severity, issue.kind, issue.stage, issue.skill, issue.path, issue.detail))
        for issue in issues
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """Parse arguments and print the completion summary to stdout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--format", choices=["markdown", "toon"], default="markdown")
    parser.add_argument("--gate", choices=["default", "full"], default="default")
    args = parser.parse_args()

    root = args.root.resolve()
    issues, feature_root, _ = inspect_package(root, args.feature, args.gate)
    renderer = render_toon if args.format == "toon" else render_markdown
    print(renderer(args.feature, issues, feature_root), end="")
    return 1 if any(issue.severity == "error" for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
