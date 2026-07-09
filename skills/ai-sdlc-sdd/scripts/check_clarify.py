#!/usr/bin/env python3
"""Validate clarify-gate requirements for an AI SDLC SDD spec."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from spec_helpers import ROOT, meaningful_lines, section_text


REQUIRED_SECTIONS = ("Assumptions", "Open Questions", "Decision Status")


def validate(spec_dir: Path) -> list[str]:
    requirements = spec_dir / "requirements.md"
    if not requirements.is_file():
        return [f"missing {requirements}"]

    markdown = requirements.read_text(encoding="utf-8")
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        content = meaningful_lines(section_text(markdown, section))
        if not content:
            errors.append(f"requirements.md missing meaningful clarify section: {section}")

    decision_lines = " ".join(meaningful_lines(section_text(markdown, "Decision Status"))).lower()
    if decision_lines and not any(
        token in decision_lines
        for token in ("resolved", "todo(dm):", "accepted assumption", "all blocking decisions")
    ):
        errors.append(
            "requirements.md Decision Status must record resolved blockers, accepted assumptions, or TODO(dm) handoff"
        )

    open_question_lines = meaningful_lines(section_text(markdown, "Open Questions"))
    if open_question_lines and any("todo(" in line.lower() and "todo(dm):" not in line.lower() for line in open_question_lines):
        errors.append("Open Questions may use TODO(dm): but not generic TODO/TBD markers")

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

    print(f"Clarify gate passed: {spec_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
