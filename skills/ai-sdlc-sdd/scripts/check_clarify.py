#!/usr/bin/env python3
"""Validate clarify-gate requirements for an AI SDLC SDD spec.

The clarify gate ensures ambiguity is made explicit before implementation:
assumptions, open questions, and decision status must all be present and useful.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_state_machine import add_state_arguments, run_state_action
from spec_helpers import ROOT, meaningful_lines, section_text


REQUIRED_SECTIONS = ("Assumptions", "Open Questions", "Decision Status")


def validate(spec_dir: Path) -> list[str]:
    """Return clarify-gate errors for one spec directory."""
    requirements = spec_dir / "requirements.md"
    if not requirements.is_file():
        return [f"missing {requirements}"]

    markdown = requirements.read_text(encoding="utf-8")
    errors: list[str] = []
    # All clarify sections must contain meaningful non-heading content; a heading
    # alone is not enough to prove ambiguity was handled.
    for section in REQUIRED_SECTIONS:
        content = meaningful_lines(section_text(markdown, section))
        if not content:
            errors.append(f"requirements.md missing meaningful clarify section: {section}")

    decision_lines = " ".join(meaningful_lines(section_text(markdown, "Decision Status"))).lower()
    if decision_lines and not any(
        token in decision_lines
        for token in ("resolved", "todo(dm):", "accepted assumption", "all blocking decisions")
    ):
        # Decision Status must say how blockers were resolved or transferred,
        # otherwise downstream work cannot distinguish facts from assumptions.
        errors.append(
            "requirements.md Decision Status must record resolved blockers, accepted assumptions, or TODO(dm) handoff"
        )

    # Open questions can contain TODO(dm) ownership markers but not generic TODOs.
    open_question_lines = meaningful_lines(section_text(markdown, "Open Questions"))
    if open_question_lines and any("todo(" in line.lower() and "todo(dm):" not in line.lower() for line in open_question_lines):
        errors.append("Open Questions may use TODO(dm): but not generic TODO/TBD markers")

    return errors


def main() -> int:
    """Run the clarify gate and print normalized errors."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", type=Path)
    parser.add_argument("--quick-flow", action="store_true", help="Accept quick-flow calls; clarify gate remains deterministic")
    parser.add_argument("--full-flow", action="store_true", help="Accept full-flow calls; clarify gate remains deterministic")
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

    print(f"Clarify gate passed: {spec_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
