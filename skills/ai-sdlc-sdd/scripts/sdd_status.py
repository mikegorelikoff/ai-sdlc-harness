#!/usr/bin/env python3
"""Report AI SDLC SDD workflow status for the active feature spec.

The status command runs the same gates in workflow order and returns the first
state that still needs work: structural spec, clarify, checklist, analyze, or
ready-for-implementation.
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
from ai_sdlc_context import toon_row, toon_scalar
from analyze_spec import validate as analyze_validate
from check_checklist import validate as checklist_validate
from check_clarify import validate as clarify_validate
from spec_helpers import ROOT, resolve_active_spec, upstream_refinement_errors
from validate_spec import require_file, validate_sections, validate_tasks
from validate_spec import validate_plan, validate_qa, validate_test_cases, REQUIRED_DESIGN, REQUIRED_REQUIREMENTS


def structural_errors(spec_dir: Path) -> list[str]:
    """Return structural validation errors without invoking deeper gates."""
    errors: list[str] = []
    # Load required files first and only run section validators when content is
    # available. This keeps missing-file messages clear.
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
    return errors


def evaluate_status(spec_dir: Path, *, require_refinement: bool = False, feature: str = "") -> tuple[str, list[str]]:
    """Evaluate the SDD workflow state in gate order."""
    # Structural validation is first because later gates assume required files
    # and sections exist.
    errors = structural_errors(spec_dir)
    if errors:
        return "needs_spec", errors

    # Clarify, checklist, and analyze are sequential quality gates. Returning the
    # first failing state gives the agent the next concrete action.
    clarify_errors = clarify_validate(spec_dir)
    if clarify_errors:
        return "needs_clarify", clarify_errors

    checklist_errors = checklist_validate(spec_dir)
    if checklist_errors:
        return "needs_checklist", checklist_errors

    analyze_errors = analyze_validate(spec_dir)
    if analyze_errors:
        return "needs_analyze", analyze_errors

    if require_refinement:
        refinement_errors = upstream_refinement_errors(spec_dir, feature)
        if refinement_errors:
            return "needs_refinement", refinement_errors

    return "ready_for_impl", []


def main() -> int:
    """Resolve the active spec, evaluate status, and print state/reasons."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", nargs="?", help="Explicit spec directory or path")
    parser.add_argument("--spec", dest="spec_flag", help="Explicit spec directory or path")
    parser.add_argument("--branch", help="Branch name override")
    parser.add_argument("--files", nargs="*", help="Changed-file context override")
    parser.add_argument("--quick-flow", action="store_true", help="Report concise status for quick-flow use")
    parser.add_argument("--full-flow", action="store_true", help="Report stricter status for full-flow use")
    parser.add_argument("--format", choices=["toon", "text"], default="text", help="Human-readable text by default or compact TOON for agents")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()

    state_rc = run_state_action(args, "ai-sdlc-sdd", "implementation")
    if state_rc:
        return state_rc

    try:
        explicit = args.spec_flag or args.spec
        # Explicit CLI input, changed files, and branch hints all flow through the
        # shared resolver so status agrees with other SDD scripts.
        resolved = resolve_active_spec(ROOT, explicit=explicit, files=args.files, branch=args.branch)
    except ValueError as exc:
        print(f"Current workflow state: needs_spec", file=sys.stderr)
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    state, reasons = evaluate_status(resolved.spec_dir, require_refinement=args.full_flow, feature=args.feature)
    relative = resolved.spec_dir.relative_to(ROOT)
    # Non-ready states write to stderr so shell callers can distinguish blockers
    # from successful status output.
    stream = sys.stdout if state == "ready_for_impl" else sys.stderr
    if args.format == "toon":
        next_actions = {
            "needs_spec": "complete required SDD artifacts",
            "needs_clarify": "resolve blocking questions and assumptions",
            "needs_checklist": "complete the SDD checklist",
            "needs_analyze": "repair cross-artifact traceability",
            "needs_refinement": "complete upstream refinement gates",
            "ready_for_impl": "start the next implementation task from plan.toon",
        }
        print("schema: ai-sdlc-sdd-status/v1", file=stream)
        print(f"spec: {toon_scalar(relative.as_posix())}", file=stream)
        print(f"resolved_from: {resolved.source}", file=stream)
        print(f"state: {state}", file=stream)
        print(f"next_action: {toon_scalar(next_actions[state])}", file=stream)
        print(f"reasons[{len(reasons)}]{{message}}:", file=stream)
        for reason in reasons:
            print("  " + toon_row((reason,)), file=stream)
    else:
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
