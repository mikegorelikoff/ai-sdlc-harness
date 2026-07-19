#!/usr/bin/env python3
"""Validate an AI SDLC SDD spec folder.

This is the structural SDD validator. It verifies required files, required
sections, and parseable task rows, but leaves deeper cross-artifact traceability
to `analyze_spec.py`.
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
from spec_helpers import SDD_ARTIFACT_SECTIONS, plan_required_sections

REQUIRED_REQUIREMENTS = SDD_ARTIFACT_SECTIONS["requirements"][:11]
REQUIRED_DESIGN = SDD_ARTIFACT_SECTIONS["design"]
REQUIRED_TEST_CASES = SDD_ARTIFACT_SECTIONS["test-cases"]
REQUIRED_QA = SDD_ARTIFACT_SECTIONS["qa"]

REQUIRED_PLAN = plan_required_sections()


def headings(markdown: str) -> set[str]:
    """Return second-level Markdown headings from a spec artifact."""
    return {
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", markdown, re.MULTILINE)
    }


def require_file(spec_dir: Path, name: str) -> tuple[Path, str, list[str]]:
    """Read a required file or return a normalized missing-file error."""
    path = (
        first_existing(plan_toon_path(spec_dir), legacy_plan_toon_path(spec_dir))
        if name == "plan.toon"
        else spec_dir / name
    )
    if not path.is_file():
        return path, "", [f"missing {path}"]
    return path, path.read_text(encoding="utf-8"), []


def validate_sections(label: str, markdown: str, required: list[str]) -> list[str]:
    """Return missing-section errors for one artifact."""
    present = headings(markdown)
    return [f"{label} missing section: {section}" for section in required if section not in present]


def validate_tasks(markdown: str) -> list[str]:
    """Validate task artifact structure and checkbox task syntax."""
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
    """Validate the test-case artifact section skeleton."""
    return validate_sections("test-cases.md", markdown, REQUIRED_TEST_CASES)


def validate_qa(markdown: str) -> list[str]:
    """Validate the QA artifact section skeleton."""
    return validate_sections("qa.md", markdown, REQUIRED_QA)


def validate_plan(markdown: str) -> list[str]:
    """Validate the execution plan and trace-map section skeleton."""
    return validate_sections("plan.md", markdown, REQUIRED_PLAN)


def main() -> int:
    """Validate one spec directory and print deterministic errors."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", type=Path)
    parser.add_argument("--quick-flow", action="store_true", help="Accept quick-flow calls; validation remains deterministic")
    parser.add_argument("--full-flow", action="store_true", help="Accept full-flow calls; validation remains deterministic")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()

    spec_dir = args.spec_dir
    errors: list[str] = []
    if not spec_dir.is_dir():
        print(f"not a spec directory: {spec_dir}", file=sys.stderr)
        return 2

    state_rc = run_state_action(args, "ai-sdlc-sdd", "implementation", str(spec_dir))
    if state_rc:
        return state_rc

    # Load every required artifact first. Section checks run only when the file
    # exists so missing-file errors stay clear and non-duplicative.
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
    _, plan, file_errors = require_file(spec_dir, "plan.md")
    errors.extend(file_errors)
    _, _plan_toon, file_errors = require_file(spec_dir, "plan.toon")
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
    if plan:
        errors.extend(validate_plan(plan))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"SDD spec is valid: {spec_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
