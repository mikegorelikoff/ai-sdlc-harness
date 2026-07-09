#!/usr/bin/env python3
"""Validate requirement-quality checklist rules for an AI SDLC SDD spec."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from spec_helpers import ROOT, meaningful_lines, parse_acceptance_ids, section_text


PLACEHOLDER_TOKENS = {"tbd", "todo", "to do", "works correctly", "make it better"}


def validate(spec_dir: Path) -> list[str]:
    requirements = spec_dir / "requirements.md"
    if not requirements.is_file():
        return [f"missing {requirements}"]

    markdown = requirements.read_text(encoding="utf-8")
    errors: list[str] = []

    for section in ("Goal", "Problem Statement", "Scope", "Actors", "Constraints", "Out of Scope"):
        if not meaningful_lines(section_text(markdown, section)):
            errors.append(f"requirements.md checklist section is empty: {section}")

    acceptance_section = section_text(markdown, "Acceptance Criteria")
    acceptance_lines = meaningful_lines(acceptance_section)
    acceptance_ids = parse_acceptance_ids(markdown)
    if not acceptance_lines:
        errors.append("Acceptance Criteria is empty")
    if not acceptance_ids:
        errors.append("Acceptance Criteria must use AC-### identifiers")

    lowered_acceptance = " ".join(line.lower() for line in acceptance_lines)
    if acceptance_lines and not any(token in lowered_acceptance for token in ("given ", "when ", "then ", "must ", "includes ", "reports ")):
        errors.append("Acceptance Criteria must use observable pass/fail wording, not only generic prose")

    out_of_scope_lines = meaningful_lines(section_text(markdown, "Out of Scope"))
    if out_of_scope_lines and any(line.lower() in {"none", "- none", "* none"} for line in out_of_scope_lines):
        errors.append("Out of Scope must describe explicit exclusions, not only `None`")

    weak_lines = [line for line in acceptance_lines + out_of_scope_lines if line.lower() in PLACEHOLDER_TOKENS]
    if weak_lines:
        errors.append("requirements.md contains placeholder checklist language: " + "; ".join(weak_lines))

    if re.search(r"\bTBD\b|\bTODO\b", markdown) and "TODO(dm):" not in markdown:
        errors.append("requirements.md may not use generic TODO/TBD markers outside TODO(dm)")

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

    print(f"Checklist gate passed: {spec_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
