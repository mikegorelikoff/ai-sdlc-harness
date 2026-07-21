#!/usr/bin/env python3
"""Validate cross-artifact consistency for an AI SDLC SDD spec.

The analyze gate checks traceability across requirements, test cases, tasks,
and QA evidence. It is intentionally stricter than structural validation.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_paths import first_existing, legacy_plan_toon_path, plan_toon_path
from ai_sdlc_state_machine import add_state_arguments, run_state_action
from ai_sdlc_validation_receipt import validate_receipt
from spec_helpers import ROOT, parse_acceptance_ids, parse_task_entries, parse_test_case_ids


def validate(spec_dir: Path) -> list[str]:
    """Return cross-artifact consistency errors for one spec directory."""
    requirements = spec_dir / "requirements.md"
    test_cases = spec_dir / "test-cases.md"
    tasks = spec_dir / "tasks.md"
    qa = spec_dir / "qa.md"
    plan = spec_dir / "plan.md"
    plan_toon = first_existing(plan_toon_path(spec_dir), legacy_plan_toon_path(spec_dir))

    missing = [path for path in (requirements, test_cases, tasks, qa, plan, plan_toon) if not path.is_file()]
    if missing:
        return [f"missing {path}" for path in missing]

    # Read all artifacts once; later checks search in-memory text so the output
    # stays deterministic and cheap.
    requirements_md = requirements.read_text(encoding="utf-8")
    test_cases_md = test_cases.read_text(encoding="utf-8")
    tasks_md = tasks.read_text(encoding="utf-8")
    qa_md = qa.read_text(encoding="utf-8")
    plan_md = plan.read_text(encoding="utf-8")

    acceptance_ids = parse_acceptance_ids(requirements_md)
    test_case_ids = parse_test_case_ids(test_cases_md)
    task_entries = parse_task_entries(tasks_md)
    errors: list[str] = []

    if not acceptance_ids:
        errors.append("requirements.md has no AC-### identifiers to analyze")

    for acceptance_id in acceptance_ids:
        # Every acceptance criterion must be represented both in tests and in
        # implementation task refs for end-to-end traceability.
        if acceptance_id not in test_cases_md:
            errors.append(f"acceptance criterion not covered by test-cases.md: {acceptance_id}")
        if acceptance_id not in tasks_md:
            errors.append(f"acceptance criterion not covered by tasks.md refs: {acceptance_id}")
        if acceptance_id not in plan_md:
            errors.append(f"acceptance criterion not covered by plan.md: {acceptance_id}")

    for test_case_id in test_case_ids:
        if test_case_id not in plan_md:
            errors.append(f"test case not covered by plan.md: {test_case_id}")

    if not task_entries:
        errors.append("tasks.md has no parseable checkbox tasks")

    for entry in task_entries:
        # Task metadata makes implementation work reviewable without re-reading
        # the whole spec.
        if not entry.output:
            errors.append(f"task missing Output: metadata: {entry.task_id}")
        if not entry.refs:
            errors.append(f"task missing Refs: metadata: {entry.task_id}")
        if entry.task_id not in plan_md:
            errors.append(f"task not covered by plan.md: {entry.task_id}")

    if "## Validation Commands" not in qa_md:
        errors.append("qa.md missing Validation Commands section")
    execution_claim = re.search(r"(?im)^\s*(?:-\s*)?PASS\s*(?::|-|\.)", qa_md)
    if execution_claim:
        receipt = spec_dir / "_ai_sdlc/validation-receipt.json"
        receipt_errors = validate_receipt(receipt, ROOT)
        if receipt_errors:
            errors.append("qa.md contains PASS claims without a current executed validation receipt")
            errors.extend(receipt_errors)

    for required_link in ("requirements.md", "design.md", "test-cases.md", "qa.md", "tasks.md", "_ai_sdlc/plan.toon", "decision-log.md"):
        if required_link not in plan_md:
            errors.append(f"plan.md missing SDD artifact link: {required_link}")

    return errors


def main() -> int:
    """Run the analyze gate and print normalized errors."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", type=Path)
    parser.add_argument("--quick-flow", action="store_true", help="Accept quick-flow calls; analysis remains deterministic")
    parser.add_argument("--full-flow", action="store_true", help="Accept full-flow calls; analysis remains deterministic")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()

    spec_dir = args.spec_dir
    if not spec_dir.is_absolute():
        spec_dir = ROOT / spec_dir

    state_rc = run_state_action(args, "ai-sdlc-sdd", "implementation", str(spec_dir))
    if state_rc:
        return state_rc

    errors = validate(spec_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Analyze gate passed: {spec_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
