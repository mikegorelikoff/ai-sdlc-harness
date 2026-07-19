#!/usr/bin/env python3
"""Validate requirement-quality checklist rules for an AI SDLC SDD spec.

This gate catches weak requirements language before implementation starts:
empty core sections, unmeasurable acceptance criteria, vague out-of-scope text,
and generic TODO/TBD markers.
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
from ai_sdlc_state_machine import add_state_arguments, run_state_action
from spec_helpers import ROOT, markdown_body, meaningful_lines, parse_acceptance_ids, section_text


PLACEHOLDER_TOKENS = {"tbd", "todo", "to do", "works correctly", "make it better"}


def validate(spec_dir: Path) -> list[str]:
    """Return checklist-quality errors for `requirements.md`."""
    requirements = spec_dir / "requirements.md"
    if not requirements.is_file():
        return [f"missing {requirements}"]

    markdown = requirements.read_text(encoding="utf-8")
    errors: list[str] = []

    # These sections carry the minimum product framing required before design and
    # implementation can proceed safely.
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

    # `None` is too ambiguous for out-of-scope; full traceability needs explicit
    # exclusions or accepted assumptions.
    out_of_scope_lines = meaningful_lines(section_text(markdown, "Out of Scope"))
    if out_of_scope_lines and any(line.lower() in {"none", "- none", "* none"} for line in out_of_scope_lines):
        errors.append("Out of Scope must describe explicit exclusions, not only `None`")

    weak_lines = [line for line in acceptance_lines + out_of_scope_lines if line.lower() in PLACEHOLDER_TOKENS]
    if weak_lines:
        errors.append("requirements.md contains placeholder checklist language: " + "; ".join(weak_lines))

    # Generic TODO/TBD markers hide ownership. TODO(dm) is allowed because it
    # explicitly marks a decision-maker handoff.
    visible_markdown = markdown_body(markdown)
    if re.search(r"\bTBD\b|\bTODO\b", visible_markdown) and "TODO(dm):" not in visible_markdown:
        errors.append("requirements.md may not use generic TODO/TBD markers outside TODO(dm)")

    return errors


def main() -> int:
    """Run the checklist gate and print normalized errors."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", type=Path)
    parser.add_argument("--quick-flow", action="store_true", help="Accept quick-flow calls; checklist remains deterministic")
    parser.add_argument("--full-flow", action="store_true", help="Accept full-flow calls; checklist remains deterministic")
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

    print(f"Checklist gate passed: {spec_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
