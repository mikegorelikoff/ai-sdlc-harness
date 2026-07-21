#!/usr/bin/env python3
"""Create and validate SDD `plan.md` and `_ai_sdlc/plan.toon` execution links.

`tasks.md` checkboxes are authoritative. `_ai_sdlc/plan.toon` is the compact
machine projection and `plan.md` is the human-readable projection generated
from the same task links and status.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_artifact_helper import artifact_metadata_lines
from ai_sdlc_paths import (
    first_existing,
    internal_dir,
    legacy_plan_toon_path,
    plan_toon_path,
)
from ai_sdlc_state_machine import add_state_arguments, flow_mode_from_args, run_state_action
from ai_sdlc_specs_index import write_indexes_for_roots
from spec_helpers import (
    ROOT,
    parse_acceptance_ids,
    parse_test_case_acceptance_links,
    parse_plan_toon_rows,
    parse_task_entries,
    parse_test_case_ids,
    plan_required_sections,
)


def read(path: Path) -> str:
    """Read a spec artifact if present, otherwise return empty text."""
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def csv_list(values: list[str]) -> str:
    """Return a TOON-safe slash-delimited value or `none` for empty lists."""
    return "/".join(values) if values else "none"


def toon_value(value: str) -> str:
    """Normalize one compact TOON cell so row parsing remains deterministic."""
    cleaned = " ".join(value.split()).replace(",", ";")
    return cleaned or "TBD"


def build_plan_toon(spec_dir: Path, args: argparse.Namespace) -> str:
    """Build canonical plan.toon from SDD artifacts and existing task status."""
    feature = args.feature if args.feature != "<feature-name>" else spec_dir.name
    flow = flow_mode_from_args(args)
    requirements_md = read(spec_dir / "requirements.md")
    test_cases_md = read(spec_dir / "test-cases.md")
    tasks_md = read(spec_dir / "tasks.md")
    acceptance_ids = parse_acceptance_ids(requirements_md)
    test_case_ids = parse_test_case_ids(test_cases_md)
    test_case_links = parse_test_case_acceptance_links(test_cases_md)
    task_entries = parse_task_entries(tasks_md)
    existing_plan = first_existing(plan_toon_path(spec_dir), legacy_plan_toon_path(spec_dir))
    existing = parse_plan_toon_rows(read(existing_plan))

    lines = [
        f"feature: {feature}",
        "workspace: implementation",
        f"flow_mode: {flow}",
        f"updated_at: {date.today().isoformat()}",
        "source_artifacts[6]{artifact,path}:",
        "  requirements,requirements.md",
        "  design,design.md",
        "  test_cases,test-cases.md",
        "  qa,qa.md",
        "  tasks,tasks.md",
        "  decisions,decision-log.md",
        f"trace[{len(acceptance_ids)}]{{acceptance_id,test_cases,tasks}}:",
    ]

    for acceptance_id in acceptance_ids:
        linked_tests = [test_id for test_id in test_case_ids if acceptance_id in test_case_links.get(test_id, [])]
        linked_tasks = [entry.task_id for entry in task_entries if acceptance_id in entry.refs]
        lines.append(f"  {acceptance_id},{csv_list(linked_tests)},{csv_list(linked_tasks)}")

    lines.append(f"tasks[{len(task_entries)}]{{id,status,refs,tests,depends_on,artifact,decision_ref}}:")
    for entry in task_entries:
        previous = existing.get(entry.task_id, {})
        checkbox_status = "done" if "[x]" in entry.line.lower() else "pending"
        # The checked task list is authoritative; do not preserve stale
        # pending status from an older generated TOON plan.
        status = checkbox_status
        refs = csv_list(entry.refs)
        tests = csv_list(
            [
                test_id
                for test_id in test_case_ids
                if any(acceptance_id in test_case_links.get(test_id, []) for acceptance_id in entry.refs)
            ]
        )
        depends_on = csv_list(entry.depends_on)
        prior_artifact = previous.get("artifact")
        artifact = toon_value(
            prior_artifact if prior_artifact not in {None, "", "TBD", "none"} else entry.output or "TBD"
        )
        decision_ref = toon_value(previous.get("decision_ref") or "TBD")
        lines.append(f"  {entry.task_id},{status},{refs},{tests},{depends_on},{artifact},{decision_ref}")

    lines.extend(
        [
            "validation_sequence[5]{step,command}:",
            "  1,check_refinement_context.py --full-flow",
            "  2,check_clarify.py --full-flow",
            "  3,check_checklist.py --full-flow",
            "  4,plan_links.py --check --full-flow",
            "  5,analyze_spec.py --full-flow && validate_spec.py --full-flow",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_plan(spec_dir: Path, args: argparse.Namespace) -> str:
    """Build canonical plan.md content from SDD artifacts and plan.toon."""
    feature = args.feature if args.feature != "<feature-name>" else spec_dir.name
    flow = flow_mode_from_args(args)
    artifact_path = spec_dir / "plan.md"
    decision_log = spec_dir / "decision-log.md"
    state_file = internal_dir(spec_dir) / "state.toon"

    def display_path(path: Path) -> str:
        """Prefer repository-relative paths while keeping temp-fixture tests portable."""
        try:
            return path.relative_to(ROOT).as_posix()
        except ValueError:
            return path.as_posix()

    metadata = artifact_metadata_lines(
        feature=feature,
        artifact_name="plan.md",
        artifact_path=display_path(artifact_path),
        workspace="implementation",
        skill_name="ai-sdlc-sdd",
        flow_mode=flow,
        decision_log_path=display_path(decision_log),
        state_file_path=display_path(state_file),
        state_args=args,
    )

    requirements_md = read(spec_dir / "requirements.md")
    test_cases_md = read(spec_dir / "test-cases.md")
    tasks_md = read(spec_dir / "tasks.md")
    acceptance_ids = parse_acceptance_ids(requirements_md)
    test_case_ids = parse_test_case_ids(test_cases_md)
    test_case_links = parse_test_case_acceptance_links(test_cases_md)
    task_entries = parse_task_entries(tasks_md)
    closed_task_ids = {
        entry.task_id for entry in task_entries if "[x]" in entry.line.lower()
    }

    lines = metadata + [
        "# plan.md",
        "",
        "## Upstream Refinement Sources",
        "- Refinement index: `specs-refiniment/_ai_sdlc/specs-index.toon`",
        "- Refinement state: `specs-refiniment/<feature-name>/_ai_sdlc/state.toon`",
        "- Delivery spec: `specs-refiniment/<feature-name>/delivery-spec.md`",
        "- QA readiness: `specs-refiniment/<feature-name>/qa-readiness.md`",
        "- Decision trace: `decision-log.md`",
        "",
        "## SDD Artifact Links",
        "- Requirements: `requirements.md`",
        "- Design: `design.md`",
        "- Test cases: `test-cases.md`",
        "- QA: `qa.md`",
        "- Tasks: `tasks.md`",
        "- Machine plan: `_ai_sdlc/plan.toon`",
        "- Decision log: `decision-log.md`",
        "",
        "## Cross-Artifact Trace Map",
    ]
    if acceptance_ids:
        for acceptance_id in acceptance_ids:
            matching_tests = [test_id for test_id in test_case_ids if acceptance_id in test_case_links.get(test_id, [])]
            matching_tasks = [entry.task_id for entry in task_entries if acceptance_id in entry.refs]
            lines.append(
                f"- {acceptance_id}: requirements.md -> test-cases.md ({', '.join(matching_tests) or 'TBD'}) -> "
                f"tasks.md ({', '.join(matching_tasks) or 'TBD'}) -> qa.md -> decision-log.md"
            )
    else:
        lines.append("- AC-TBD: requirements.md -> test-cases.md -> tasks.md -> qa.md -> decision-log.md")

    lines.extend(["", "## Task Execution Plan"])
    if task_entries:
        for entry in task_entries:
            checkbox = "[x]" if entry.task_id in closed_task_ids else "[ ]"
            description = re.sub(
                rf"^- \[[ xX]\] {re.escape(entry.task_id)}[.:]?\s*",
                "",
                entry.line,
            )
            lines.append(
                f"- {checkbox} {entry.task_id}: {description}; refs: {', '.join(entry.refs) or 'TBD'}; "
                f"output: {entry.output or 'TBD'}"
            )
    else:
        lines.append("- T000: TBD")

    lines.extend(["", "## Task Dependencies"])
    if task_entries:
        for entry in task_entries:
            lines.append(f"- {entry.task_id}: depends on {', '.join(entry.depends_on) or 'previous applicable task / none'}")
    else:
        lines.append("- T000: TBD")

    missing_links: list[str] = []
    for acceptance_id in acceptance_ids:
        if not any(acceptance_id in values for values in test_case_links.values()):
            missing_links.append(f"{acceptance_id} has no test-case link")
        if not any(acceptance_id in entry.refs for entry in task_entries):
            missing_links.append(f"{acceptance_id} has no task link")

    lines.extend(
        [
            "",
            "## Validation Sequence",
            "- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`",
            "- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`",
            "- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`",
            "- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`",
            f"- Generated: {date.today().isoformat()}",
            "",
            "## Open Links And Blockers",
        ]
    )
    if missing_links:
        lines.extend(f"- {item}." for item in missing_links)
    else:
        lines.append("- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.")
    return "\n".join(lines).rstrip() + "\n"


def check_plan(spec_dir: Path) -> list[str]:
    """Return plan.md/machine-plan link and coverage errors."""
    plan = spec_dir / "plan.md"
    canonical_plan_toon = plan_toon_path(spec_dir)
    plan_toon = first_existing(canonical_plan_toon, legacy_plan_toon_path(spec_dir))
    if not plan.is_file():
        return [f"missing {plan}"]
    if not plan_toon.is_file():
        return [f"missing {canonical_plan_toon}"]

    text = plan.read_text(encoding="utf-8")
    toon_text = plan_toon.read_text(encoding="utf-8")
    toon_tasks = parse_plan_toon_rows(toon_text)
    errors: list[str] = []
    for section in plan_required_sections():
        if f"## {section}" not in text:
            errors.append(f"plan.md missing section: {section}")

    requirements_md = read(spec_dir / "requirements.md")
    test_cases_md = read(spec_dir / "test-cases.md")
    tasks_md = read(spec_dir / "tasks.md")
    for acceptance_id in parse_acceptance_ids(requirements_md):
        if acceptance_id not in text:
            errors.append(f"plan.md missing acceptance link: {acceptance_id}")
    for test_case_id in parse_test_case_ids(test_cases_md):
        if test_case_id not in text:
            errors.append(f"plan.md missing test-case link: {test_case_id}")
    for entry in parse_task_entries(tasks_md):
        if entry.task_id not in text:
            errors.append(f"plan.md missing task link: {entry.task_id}")
        if entry.task_id not in toon_tasks:
            errors.append(f"plan.toon missing task row: {entry.task_id}")
            continue
        expected_status = "done" if "[x]" in entry.line.lower() else "pending"
        actual_status = toon_tasks[entry.task_id].get("status")
        if actual_status != expected_status:
            errors.append(
                f"plan.toon task {entry.task_id} status {actual_status or 'missing'} "
                f"does not match authoritative tasks.md status {expected_status}"
            )
        expected_checkbox = "x" if expected_status == "done" else " "
        if f"- [{expected_checkbox}] {entry.task_id}:" not in text:
            errors.append(
                f"plan.md task {entry.task_id} status does not match authoritative tasks.md"
            )
    test_case_links = parse_test_case_acceptance_links(test_cases_md)
    acceptance_ids = set(parse_acceptance_ids(requirements_md))
    for test_case_id, linked_acceptance in test_case_links.items():
        unknown = sorted(set(linked_acceptance) - acceptance_ids)
        if unknown:
            errors.append(f"test case {test_case_id} links unknown acceptance IDs: {', '.join(unknown)}")
    for acceptance_id in acceptance_ids:
        # Legacy fixtures may not annotate test cases yet; retain their
        # generated-plan compatibility while enforcing exact links whenever
        # explicit AC↔TC links are present.
        if not test_case_links:
            continue
        expected_tests = [test_id for test_id in parse_test_case_ids(test_cases_md) if acceptance_id in test_case_links.get(test_id, [])]
        if not expected_tests:
            errors.append(f"acceptance {acceptance_id} has no explicit test-case link")
        expected = f"- {acceptance_id}: requirements.md -> test-cases.md ({', '.join(expected_tests)})"
        legacy = f"- {acceptance_id} -> {', '.join(expected_tests)}"
        if expected not in text and legacy not in text:
            errors.append(f"plan.md trace for {acceptance_id} is not exact")
    for required_link in ("requirements.md", "design.md", "test-cases.md", "qa.md", "tasks.md", "_ai_sdlc/plan.toon", "decision-log.md"):
        if required_link not in text:
            errors.append(f"plan.md missing SDD artifact link: {required_link}")
    for required_toon_key in ("source_artifacts", "trace", "tasks", "validation_sequence"):
        if f"{required_toon_key}[" not in toon_text:
            errors.append(f"plan.toon missing block: {required_toon_key}")
    return errors


def main() -> int:
    """Parse CLI flags and emit, write, or check plan.toon/plan.md."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", type=Path)
    parser.add_argument("--check", action="store_true", help="Validate existing plan.toon and plan.md")
    parser.add_argument("--emit-template", action="store_true", help="Print canonical plan.md content")
    parser.add_argument("--emit-toon", action="store_true", help="Print canonical plan.toon content")
    parser.add_argument("--write", action="store_true", help="Write plan.toon and plan.md, then refresh specs indexes")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--artifact-status", default="draft")
    parser.add_argument("--artifact-owner", default="TBD")
    parser.add_argument("--artifact-tag", action="append", default=[])
    add_state_arguments(parser)
    args = parser.parse_args()

    spec_dir = args.spec_dir if args.spec_dir.is_absolute() else ROOT / args.spec_dir
    state_rc = run_state_action(args, "ai-sdlc-sdd", "implementation", str(spec_dir))
    if state_rc:
        return state_rc

    if args.write:
        spec_dir.mkdir(parents=True, exist_ok=True)
        machine_plan = plan_toon_path(spec_dir)
        machine_plan.parent.mkdir(parents=True, exist_ok=True)
        machine_plan.write_text(build_plan_toon(spec_dir, args), encoding="utf-8")
        (spec_dir / "plan.md").write_text(build_plan(spec_dir, args), encoding="utf-8")
        write_indexes_for_roots([ROOT / "specs"])
        print(f"Wrote {machine_plan}")
        print(f"Wrote {spec_dir / 'plan.md'}")

    if args.emit_template:
        print(build_plan(spec_dir, args), end="")

    if args.emit_toon:
        print(build_plan_toon(spec_dir, args), end="")

    if args.check:
        errors = check_plan(spec_dir)
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print(f"Plan links valid: {plan_toon_path(spec_dir)} and {spec_dir / 'plan.md'}")

    if not (args.write or args.emit_template or args.emit_toon or args.check):
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
