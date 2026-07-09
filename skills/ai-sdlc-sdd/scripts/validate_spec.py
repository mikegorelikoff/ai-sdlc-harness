#!/usr/bin/env python3
"""Validate an AI SDLC SDD spec folder."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_REQUIREMENTS = [
    "Goal",
    "Problem Statement",
    "Scope",
    "Actors",
    "Inputs",
    "Outputs",
    "Functional Requirements",
    "Non-Functional Requirements",
    "Constraints",
    "Acceptance Criteria",
    "Out of Scope",
]

REQUIRED_DESIGN = [
    "Overview",
    "Architecture",
    "Components",
    "Interfaces and Contracts",
    "Data Model",
    "Error Handling",
    "Security Considerations",
    "Observability",
    "Risks and Tradeoffs",
    "Validation Strategy",
    "Migration Notes",
]

REQUIRED_TEST_CASES = [
    "Scope",
    "Scenario Matrix",
    "Layer Mapping",
    "Automation Plan",
    "Open Gaps",
]

REQUIRED_QA = [
    "Change Summary",
    "Acceptance Scenarios",
    "Regression Targets",
    "Risk Notes",
    "Validation Commands",
    "Manual Checks",
    "Signoff",
]


def headings(markdown: str) -> set[str]:
    return {
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", markdown, re.MULTILINE)
    }


def require_file(spec_dir: Path, name: str) -> tuple[Path, str, list[str]]:
    path = spec_dir / name
    if not path.is_file():
        return path, "", [f"missing {path}"]
    return path, path.read_text(encoding="utf-8"), []


def validate_sections(label: str, markdown: str, required: list[str]) -> list[str]:
    present = headings(markdown)
    return [f"{label} missing section: {section}" for section in required if section not in present]


def validate_tasks(markdown: str) -> list[str]:
    errors: list[str] = []
    if "## Implementation" not in markdown:
        errors.append("tasks.md missing section: Implementation")
    if "## Testing" not in markdown:
        errors.append("tasks.md missing section: Testing")
    if "## Documentation" not in markdown:
        errors.append("tasks.md missing section: Documentation")
    if not re.search(r"^- \[[ xX]\]\s+(?:\d+\.|T\d{3}\b)", markdown, re.MULTILINE):
        errors.append("tasks.md has no parseable checkbox tasks")
    return errors


def validate_test_cases(markdown: str) -> list[str]:
    return validate_sections("test-cases.md", markdown, REQUIRED_TEST_CASES)


def validate_qa(markdown: str) -> list[str]:
    return validate_sections("qa.md", markdown, REQUIRED_QA)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", type=Path)
    args = parser.parse_args()

    spec_dir = args.spec_dir
    errors: list[str] = []
    if not spec_dir.is_dir():
        print(f"not a spec directory: {spec_dir}", file=sys.stderr)
        return 2

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
    if design:
        errors.extend(validate_sections("design.md", design, REQUIRED_DESIGN))
    if tasks:
        errors.extend(validate_tasks(tasks))
    if test_cases:
        errors.extend(validate_test_cases(test_cases))
    if qa:
        errors.extend(validate_qa(qa))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"SDD spec is valid: {spec_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
