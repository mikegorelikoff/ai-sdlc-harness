#!/usr/bin/env python3
"""Report AI SDLC SDD workflow status for the active feature spec."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from analyze_spec import validate as analyze_validate
from check_checklist import validate as checklist_validate
from check_clarify import validate as clarify_validate
from spec_helpers import ROOT, resolve_active_spec
from validate_spec import require_file, validate_asana, validate_sections, validate_tasks
from validate_spec import validate_qa, validate_test_cases, REQUIRED_DESIGN, REQUIRED_REQUIREMENTS


def structural_errors(spec_dir: Path) -> list[str]:
    errors: list[str] = []
    _, requirements, file_errors = require_file(spec_dir, "requirements.md")
    errors.extend(file_errors)
    _, design, file_errors = require_file(spec_dir, "design.md")
    errors.extend(file_errors)
    _, tasks, file_errors = require_file(spec_dir, "tasks.md")
    errors.extend(file_errors)
    _, test_cases, file_errors = require_file(spec_dir, "test-cases.md")
    errors.extend(file_errors)
    _, qa, file_errors = require_file(spec_dir, "qa.md")
    errors.extend(file_errors)

    if requirements:
        errors.extend(validate_sections("requirements.md", requirements, REQUIRED_REQUIREMENTS))
        errors.extend(validate_asana(requirements))
    if design:
        errors.extend(validate_sections("design.md", design, REQUIRED_DESIGN))
    if tasks:
        errors.extend(validate_tasks(tasks))
    if test_cases:
        errors.extend(validate_test_cases(test_cases))
    if qa:
        errors.extend(validate_qa(qa))
    return errors


def evaluate_status(spec_dir: Path) -> tuple[str, list[str]]:
    errors = structural_errors(spec_dir)
    if errors:
        return "needs_spec", errors

    clarify_errors = clarify_validate(spec_dir)
    if clarify_errors:
        return "needs_clarify", clarify_errors

    checklist_errors = checklist_validate(spec_dir)
    if checklist_errors:
        return "needs_checklist", checklist_errors

    analyze_errors = analyze_validate(spec_dir)
    if analyze_errors:
        return "needs_analyze", analyze_errors

    return "ready_for_impl", []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", nargs="?", help="Explicit spec directory or path")
    parser.add_argument("--spec", dest="spec_flag", help="Explicit spec directory or path")
    parser.add_argument("--branch", help="Branch name override")
    parser.add_argument("--files", nargs="*", help="Changed-file context override")
    args = parser.parse_args()

    try:
        explicit = args.spec_flag or args.spec
        resolved = resolve_active_spec(ROOT, explicit=explicit, files=args.files, branch=args.branch)
    except ValueError as exc:
        print(f"Current workflow state: needs_spec", file=sys.stderr)
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    state, reasons = evaluate_status(resolved.spec_dir)
    relative = resolved.spec_dir.relative_to(ROOT)
    stream = sys.stdout if state == "ready_for_impl" else sys.stderr
    print(f"Spec: {relative}", file=stream)
    print(f"Resolved from: {resolved.source}", file=stream)
    print(f"Current workflow state: {state}", file=stream)
    if reasons:
        print("Reasons:", file=stream)
        for reason in reasons:
            print(f"- {reason}", file=stream)
    return 0 if state == "ready_for_impl" else 1


if __name__ == "__main__":
    raise SystemExit(main())
