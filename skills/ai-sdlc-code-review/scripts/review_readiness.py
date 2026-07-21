#!/usr/bin/env python3
"""Check AI SDLC code-review readiness signals.

This script prepares the agent for a code-review pass by collecting the review
surface, checking whitespace/diff hygiene, warning about missing spec context,
and flagging obvious test-coverage risks before the model spends tokens reading
files.
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
from ai_sdlc_paths import first_existing, legacy_plan_toon_path, plan_toon_path
from ai_sdlc_state_machine import add_state_arguments, run_state_action


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a git command and capture output without raising."""
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def changed_files(base: str | None, full_repo: bool) -> list[str]:
    """Return files in scope for review based on full-repo, branch, or worktree mode."""
    # Full-repo review should include every tracked file because there is no diff
    # boundary to derive from.
    if full_repo:
        result = run(["git", "ls-files"])
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(detail or "unable to list repository files")
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]

    # Branch review uses a symmetric range so the review surface matches what a
    # pull request would normally show.
    if base:
        result = run(["git", "diff", "--name-only", f"{base}...HEAD"])
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(detail or "unable to list changed files")
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]

    # Default mode reviews local tracked changes plus untracked files, since both
    # can affect the user's pending work even before staging.
    result = run(["git", "diff", "--name-only", "HEAD"])
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(detail or "unable to list changed files")

    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    status = run(["git", "status", "--short"])
    if status.returncode != 0:
        detail = status.stderr.strip() or status.stdout.strip()
        raise RuntimeError(detail or "unable to inspect git status")

    for line in status.stdout.splitlines():
        if line.startswith("?? "):
            path = line[3:].strip()
            path_obj = Path(path)
            if path_obj.is_dir():
                files.extend(str(child) for child in path_obj.rglob("*") if child.is_file())
            elif path:
                files.append(path)

    return sorted(set(files))


def spec_errors(spec_dir: Path) -> list[str]:
    """Validate minimum SDD evidence needed for a review-ready feature."""
    errors: list[str] = []
    required = ["requirements.md", "design.md", "test-cases.md", "qa.md", "tasks.md", "plan.md"]
    for name in required:
        if not (spec_dir / name).is_file():
            errors.append(f"missing {spec_dir / name}")
    machine_plan = first_existing(plan_toon_path(spec_dir), legacy_plan_toon_path(spec_dir))
    if not machine_plan.is_file():
        errors.append(f"missing {plan_toon_path(spec_dir)}")

    tasks = spec_dir / "tasks.md"
    if tasks.is_file():
        # Review readiness expects implementation tasks to be completed or at
        # least explicitly represented in the spec.
        task_text = tasks.read_text(encoding="utf-8")
        if "- [ ]" in task_text:
            errors.append(f"{tasks} has incomplete tasks")
        if "- [x]" not in task_text and "- [X]" not in task_text:
            errors.append(f"{tasks} has no completed tasks")
    return errors


def collect_diff_check_errors(base: str | None, full_repo: bool) -> list[str]:
    """Run `git diff --check` against the same surface selected for review."""
    checks: list[tuple[str, list[str]]] = []
    if full_repo:
        checks.extend(
            [
                ("unstaged", ["git", "diff", "--check"]),
                ("staged", ["git", "diff", "--cached", "--check"]),
            ]
        )
    elif base:
        checks.append((f"branch range {base}...HEAD", ["git", "diff", "--check", f"{base}...HEAD"]))
    else:
        checks.extend(
            [
                ("unstaged", ["git", "diff", "--check"]),
                ("staged", ["git", "diff", "--cached", "--check"]),
            ]
        )

    errors: list[str] = []
    for label, cmd in checks:
        result = run(cmd)
        if result.returncode != 0:
            errors.append(f"{label} diff --check failed")
            if result.stdout.strip():
                errors.append(result.stdout.strip())
            if result.stderr.strip():
                errors.append(result.stderr.strip())
    return errors


def skill_metadata_warnings(files: list[str], full_repo: bool) -> list[str]:
    """Warn when skill changes need metadata/script validation beyond code review."""
    if full_repo:
        return []

    warnings: list[str] = []
    changed_skills = sorted(
        {
            Path(file).parts[1]
            for file in files
            if file.startswith("skills/") and len(Path(file).parts) > 1
        }
    )
    for skill in changed_skills:
        skill_dir = Path("skills") / skill
        changed_python = sorted(
            file for file in files
            if file.startswith(f"{skill_dir}/") and file.endswith(".py") and Path(file).is_file()
        )
        if skill == "_shared":
            if changed_python:
                warnings.append(
                    "shared helper change detected; run "
                    "PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-harness-pycache python3 -m py_compile "
                    + " ".join(changed_python)
                )
            warnings.append(
                "shared helper change detected; run python3 "
                "skills/_shared/sync_installed_runtime.py --check"
            )
            continue
        if not (skill_dir / "SKILL.md").is_file():
            warnings.append(f"skill change detected but {skill_dir / 'SKILL.md'} is missing")
        else:
            warnings.append(f"skill change detected; inspect {skill_dir}/SKILL.md")
        if changed_python:
            warnings.append(
                "skill Python change detected; run "
                "PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-harness-pycache python3 -m py_compile "
                + " ".join(changed_python)
            )
    return warnings


def surface_warnings(files: list[str], spec_provided: bool, full_repo: bool) -> list[str]:
    """Produce risk hints from changed file categories."""
    warnings: list[str] = []

    # These file buckets are intentionally simple path heuristics. They are cheap
    # enough to run on every review and point the agent toward likely blind spots.
    go_files = [file for file in files if file.endswith(".go") and not file.endswith("_test.go")]
    test_files = [file for file in files if file.endswith("_test.go")]
    transport_surface = [
        file
        for file in files
        if file.startswith(("internal/transport/http/", "openapi/", "db/", "sql/"))
    ]
    workflow_surface = [
        file
        for file in files
        if file.startswith(("internal/service/", "internal/platform/", "cmd/"))
    ]

    if not full_repo and any(file.startswith(("internal/", "cmd/", "sql/", "openapi/", "db/")) for file in files) and not spec_provided:
        warnings.append(
            "backend/API changes detected without --spec; confirm this is a small change or provide the SDD folder"
        )

    if go_files and not test_files:
        warnings.append(
            "Go production files changed without Go test files in the review target; verify existing tests cover the behavior"
        )

    if transport_surface and not test_files:
        warnings.append(
            "contract-sensitive transport/schema files are in scope without obvious test coverage in the review target"
        )

    if workflow_surface and not any(file.startswith("specs/") for file in files) and not spec_provided and not full_repo:
        warnings.append(
            "service/workflow changes are in scope without spec files in the review target; confirm spec alignment manually"
        )

    if full_repo:
        warnings.append(
            "full-repo audit mode enabled; prioritize high-risk subsystems and produce a broader validation plan instead of file-by-file trivia"
        )

    return warnings


def main() -> int:
    """Parse review-scope flags, collect readiness errors, and print warnings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Base branch or commit for branch review")
    parser.add_argument("--full-repo", action="store_true", help="Prepare for a broader repository review instead of a diff-scoped review")
    parser.add_argument("--spec", type=Path, help="Relevant SDD spec folder")
    parser.add_argument("--quick-flow", action="store_true", help="Keep readiness checks diff-scoped and warning-oriented")
    parser.add_argument("--full-flow", action="store_true", help="Require stronger spec and coverage signals")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()

    state_rc = run_state_action(args, "ai-sdlc-code-review", "implementation")
    if state_rc:
        return state_rc

    errors: list[str] = []
    warnings: list[str] = []
    if args.base and args.full_repo:
        errors.append("--base and --full-repo cannot be used together")

    # Diff hygiene is a blocker because whitespace errors are deterministic and
    # cheap to catch before semantic review starts.
    errors.extend(collect_diff_check_errors(args.base, args.full_repo))

    try:
        files = changed_files(args.base, args.full_repo)
    except RuntimeError as exc:
        errors.append(str(exc))
        files = []

    if not files:
        warnings.append("no files detected for the selected review target")

    if args.full_flow and not args.spec and not args.full_repo:
        warnings.append("full flow requested without --spec; provide the relevant SDD folder or document why review is spec-free")

    if args.spec:
        errors.extend(spec_errors(args.spec))

    warnings.extend(surface_warnings(files, spec_provided=args.spec is not None, full_repo=args.full_repo))
    warnings.extend(skill_metadata_warnings(files, args.full_repo))
    if args.quick_flow:
        # Quick flow keeps review moving by suppressing broad audit guidance while
        # preserving risk warnings tied to the selected diff surface.
        warnings = [warning for warning in warnings if "full-repo audit mode" not in warning]

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        for warning in warnings:
            print(f"WARN: {warning}", file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"WARN: {warning}")
    print("Code review readiness check completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
