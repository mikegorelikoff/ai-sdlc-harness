#!/usr/bin/env python3
"""Validate cross-artifact consistency for an AI SDLC SDD spec."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from spec_helpers import ROOT, parse_acceptance_ids, parse_task_entries


def validate(spec_dir: Path) -> list[str]:
    requirements = spec_dir / "requirements.md"
    test_cases = spec_dir / "test-cases.md"
    tasks = spec_dir / "tasks.md"
    qa = spec_dir / "qa.md"

    missing = [path for path in (requirements, test_cases, tasks, qa) if not path.is_file()]
    if missing:
        return [f"missing {path}" for path in missing]

    requirements_md = requirements.read_text(encoding="utf-8")
    test_cases_md = test_cases.read_text(encoding="utf-8")
    tasks_md = tasks.read_text(encoding="utf-8")
    qa_md = qa.read_text(encoding="utf-8")

    acceptance_ids = parse_acceptance_ids(requirements_md)
    task_entries = parse_task_entries(tasks_md)
    errors: list[str] = []

    if not acceptance_ids:
        errors.append("requirements.md has no AC-### identifiers to analyze")

    for acceptance_id in acceptance_ids:
        if acceptance_id not in test_cases_md:
            errors.append(f"acceptance criterion not covered by test-cases.md: {acceptance_id}")
        if acceptance_id not in tasks_md:
            errors.append(f"acceptance criterion not covered by tasks.md refs: {acceptance_id}")

    if not task_entries:
        errors.append("tasks.md has no parseable checkbox tasks")

    for entry in task_entries:
        if not entry.output:
            errors.append(f"task missing Output: metadata: {entry.task_id}")
        if not entry.refs:
            errors.append(f"task missing Refs: metadata: {entry.task_id}")

    if "## Validation Commands" not in qa_md:
        errors.append("qa.md missing Validation Commands section")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", type=Path)
    args = parser.parse_args()

    spec_dir = args.spec_dir
    if not spec_dir.is_absolute():
        spec_dir = ROOT / spec_dir

    errors = validate(spec_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Analyze gate passed: {spec_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
