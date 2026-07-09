#!/usr/bin/env python3
"""Check AI SDLC commit readiness signals."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CHECK_CLARIFY = ROOT / ".codex" / "skills" / "ai-sdlc-sdd" / "scripts" / "check_clarify.py"
CHECK_CHECKLIST = ROOT / ".codex" / "skills" / "ai-sdlc-sdd" / "scripts" / "check_checklist.py"
ANALYZE_SPEC = ROOT / ".codex" / "skills" / "ai-sdlc-sdd" / "scripts" / "analyze_spec.py"
VALIDATE_SPEC = ROOT / ".codex" / "skills" / "ai-sdlc-sdd" / "scripts" / "validate_spec.py"
CODEX_AI_LINT = ROOT / ".codex" / "scripts" / "codex_ai_lint.py"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def has_unstaged_changes() -> bool:
    return run(["git", "diff", "--quiet"]).returncode != 0


def has_staged_changes() -> bool:
    return run(["git", "diff", "--cached", "--quiet"]).returncode != 0


def spec_tasks_complete(spec_dir: Path) -> list[str]:
    tasks = spec_dir / "tasks.md"
    if not tasks.is_file():
        return [f"missing {tasks}"]
    lines = tasks.read_text(encoding="utf-8").splitlines()
    return [line for line in lines if line.startswith("- [ ]")]


def run_spec_gate(script: Path, spec_dir: Path) -> list[str]:
    result = run(["python3", str(script), str(spec_dir)])
    if result.returncode == 0:
        return []

    details = [f"{script.name} failed"]
    if result.stderr.strip():
        details.extend(result.stderr.strip().splitlines())
    elif result.stdout.strip():
        details.extend(result.stdout.strip().splitlines())
    return details


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--allow-unstaged", action="store_true")
    parser.add_argument("--no-require-staged", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []

    diff_check = run(["git", "diff", "--check"])
    if diff_check.returncode != 0:
        errors.append("git diff --check failed")
        if diff_check.stdout:
            errors.append(diff_check.stdout.strip())
        if diff_check.stderr:
            errors.append(diff_check.stderr.strip())

    if not args.no_require_staged and not has_staged_changes():
        errors.append("no staged changes")
    if has_unstaged_changes() and not args.allow_unstaged:
        errors.append("unstaged changes remain; stage intentionally or pass --allow-unstaged")

    if args.spec:
        spec_dir = args.spec if args.spec.is_absolute() else ROOT / args.spec
        incomplete = spec_tasks_complete(spec_dir)
        if incomplete:
            errors.append(f"incomplete spec tasks in {args.spec}:")
            errors.extend(incomplete)
        for script in (VALIDATE_SPEC, CHECK_CLARIFY, CHECK_CHECKLIST, ANALYZE_SPEC):
            errors.extend(run_spec_gate(script, spec_dir))
        lint_result = run(["python3", str(CODEX_AI_LINT), "--mode", "strict", "--format", "text", "--spec", str(spec_dir)])
        if lint_result.returncode != 0:
            errors.append("codex_ai_lint.py failed")
            if lint_result.stderr.strip():
                errors.extend(lint_result.stderr.strip().splitlines())
            elif lint_result.stdout.strip():
                errors.extend(lint_result.stdout.strip().splitlines())

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Commit readiness checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
