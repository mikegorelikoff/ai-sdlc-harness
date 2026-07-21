#!/usr/bin/env python3
"""Check AI SDLC commit readiness signals.

The commit-prep skill uses this script as a deterministic preflight before
staging or committing. It checks git hygiene, optional SDD task completion, SDD
gate scripts, and full-flow decision-log presence.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_state_machine import add_state_arguments, run_state_action
from ai_sdlc_validation_receipt import validate_receipt

def workspace_root(script_path: Path = Path(__file__)) -> Path:
    """Return the consumer/source repository root for either distribution layout."""
    candidate = script_path.resolve().parents[3]
    return candidate.parent if candidate.name == ".agents" else candidate


ROOT = workspace_root()
SKILLS_ROOT = ROOT / "skills"
if not SKILLS_ROOT.is_dir():
    SKILLS_ROOT = ROOT / ".agents" / "skills"
SDD_SCRIPTS = SKILLS_ROOT / "ai-sdlc-sdd" / "scripts"
CHECK_CLARIFY = SDD_SCRIPTS / "check_clarify.py"
CHECK_CHECKLIST = SDD_SCRIPTS / "check_checklist.py"
ANALYZE_SPEC = SDD_SCRIPTS / "analyze_spec.py"
VALIDATE_SPEC = SDD_SCRIPTS / "validate_spec.py"
PLAN_LINKS = SDD_SCRIPTS / "plan_links.py"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a local command and capture output without raising."""
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def has_unstaged_changes() -> bool:
    """Return true when the worktree contains unstaged tracked changes."""
    return run(["git", "diff", "--quiet"]).returncode != 0


def has_staged_changes() -> bool:
    """Return true when the index contains staged changes."""
    return run(["git", "diff", "--cached", "--quiet"]).returncode != 0


def spec_tasks_complete(spec_dir: Path, selected_task: str | None = None) -> list[str]:
    """Return task-scope errors from `tasks.md`, or a missing-file error.

    Without ``selected_task`` the historical strict behavior remains: every
    task must be complete. An explicit task permits incremental, auditable
    commits from a larger SDD plan while still requiring that task to be
    present and complete.
    """
    tasks = spec_dir / "tasks.md"
    if not tasks.is_file():
        return [f"missing {tasks}"]
    lines = tasks.read_text(encoding="utf-8").splitlines()
    if selected_task:
        prefix = f"- ["
        matching = [
            line
            for line in lines
            if line.startswith(prefix) and line[6:].startswith(f"{selected_task}.")
        ]
        if not matching:
            return [f"selected task not found in {tasks}: {selected_task}"]
        if not matching[0].startswith("- [x]") and not matching[0].startswith("- [X]"):
            return [f"selected task is incomplete in {tasks}: {matching[0]}"]
        return []
    return [line for line in lines if line.startswith("- [ ]")]


def run_spec_gate(script: Path, spec_dir: Path) -> list[str]:
    """Run one SDD gate and normalize failure output into error lines."""
    result = run([sys.executable, str(script), str(spec_dir)])
    if result.returncode == 0:
        return []

    details = [f"{script.name} failed"]
    if result.stderr.strip():
        details.extend(result.stderr.strip().splitlines())
    elif result.stdout.strip():
        details.extend(result.stdout.strip().splitlines())
    return details


def main() -> int:
    """Run commit readiness checks and print blocking errors."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--task", help="Require one completed SDD task instead of all tasks")
    parser.add_argument("--allow-unstaged", action="store_true")
    parser.add_argument("--no-require-staged", action="store_true")
    parser.add_argument("--quick-flow", action="store_true", help="Skip expensive spec lint gates and report lean readiness")
    parser.add_argument("--full-flow", action="store_true", help="Run all available spec and lint gates")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()

    state_rc = run_state_action(args, "ai-sdlc-commit-prep", "implementation")
    if state_rc:
        return state_rc

    errors: list[str] = []

    # Whitespace/conflict-marker checks are cheap and deterministic, so they run
    # regardless of quick/full flow.
    diff_check = run(["git", "diff", "--check"])
    if diff_check.returncode != 0:
        errors.append("git diff --check failed")
        if diff_check.stdout:
            errors.append(diff_check.stdout.strip())
        if diff_check.stderr:
            errors.append(diff_check.stderr.strip())

    # The staging checks distinguish preflight usage from final commit readiness.
    if not args.no_require_staged and not has_staged_changes():
        errors.append("no staged changes")
    if has_unstaged_changes() and not args.allow_unstaged:
        errors.append("unstaged changes remain; stage intentionally or pass --allow-unstaged")

    if args.spec:
        spec_dir = args.spec if args.spec.is_absolute() else ROOT / args.spec
        incomplete = spec_tasks_complete(spec_dir, args.task)
        if incomplete:
            scope = f"selected task {args.task}" if args.task else "spec tasks"
            errors.append(f"incomplete {scope} in {args.spec}:")
            errors.extend(incomplete)
        # Quick flow runs the structural validator only. Full/default flow runs
        # the deeper clarify/checklist/analysis gates before commit.
        spec_gates = (VALIDATE_SPEC,) if args.quick_flow and not args.full_flow else (VALIDATE_SPEC, CHECK_CLARIFY, CHECK_CHECKLIST, ANALYZE_SPEC)
        for script in spec_gates:
            errors.extend(run_spec_gate(script, spec_dir))
        if (spec_dir / "plan.md").is_file():
            plan_result = run([sys.executable, str(PLAN_LINKS), str(spec_dir), "--check"])
            if plan_result.returncode != 0:
                errors.append("plan_links.py failed")
                if plan_result.stderr.strip():
                    errors.extend(plan_result.stderr.strip().splitlines())
        if args.full_flow and not (spec_dir / "decision-log.md").is_file():
            # Full flow needs decision traceability before an auditable commit.
            errors.append(f"missing decision log for full flow: {spec_dir / 'decision-log.md'}")
        if args.full_flow:
            errors.extend(validate_receipt(spec_dir / "_ai_sdlc/validation-receipt.json", ROOT))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Commit readiness checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
