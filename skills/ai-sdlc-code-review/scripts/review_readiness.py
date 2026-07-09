#!/usr/bin/env python3
"""Check AI SDLC code-review readiness signals."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def changed_files(base: str | None, full_repo: bool) -> list[str]:
    if full_repo:
        result = run(["git", "ls-files"])
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(detail or "unable to list repository files")
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]

    if base:
        result = run(["git", "diff", "--name-only", f"{base}...HEAD"])
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(detail or "unable to list changed files")
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]

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
    errors: list[str] = []
    required = ["requirements.md", "design.md", "test-cases.md", "qa.md", "tasks.md"]
    for name in required:
        if not (spec_dir / name).is_file():
            errors.append(f"missing {spec_dir / name}")

    tasks = spec_dir / "tasks.md"
    if tasks.is_file():
        task_text = tasks.read_text(encoding="utf-8")
        if "- [ ]" in task_text:
            errors.append(f"{tasks} has incomplete tasks")
        if "- [x]" not in task_text and "- [X]" not in task_text:
            errors.append(f"{tasks} has no completed tasks")
    return errors


def collect_diff_check_errors(base: str | None, full_repo: bool) -> list[str]:
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
    if full_repo:
        return []

    warnings: list[str] = []
    changed_skills = sorted(
        {
            Path(file).parts[2]
            for file in files
            if file.startswith(".codex/skills/") and len(Path(file).parts) > 2
        }
    )
    for skill in changed_skills:
        skill_dir = Path(".codex/skills") / skill
        if not (skill_dir / "SKILL.md").is_file():
            warnings.append(f"skill change detected but {skill_dir / 'SKILL.md'} is missing")
        if not (skill_dir / "agents" / "openai.yaml").is_file():
            warnings.append(f"skill change detected but {skill_dir / 'agents/openai.yaml'} is missing")
        warnings.append(
            "skill change detected; run "
            f"python3 .codex/scripts/quick_validate_skill.py {skill_dir}"
        )
    return warnings


def surface_warnings(files: list[str], spec_provided: bool, full_repo: bool) -> list[str]:
    warnings: list[str] = []

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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Base branch or commit for branch review")
    parser.add_argument("--full-repo", action="store_true", help="Prepare for a broader repository review instead of a diff-scoped review")
    parser.add_argument("--spec", type=Path, help="Relevant SDD spec folder")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    if args.base and args.full_repo:
        errors.append("--base and --full-repo cannot be used together")

    errors.extend(collect_diff_check_errors(args.base, args.full_repo))

    try:
        files = changed_files(args.base, args.full_repo)
    except RuntimeError as exc:
        errors.append(str(exc))
        files = []

    if not files:
        warnings.append("no files detected for the selected review target")

    if args.spec:
        errors.extend(spec_errors(args.spec))

    warnings.extend(surface_warnings(files, spec_provided=args.spec is not None, full_repo=args.full_repo))
    warnings.extend(skill_metadata_warnings(files, args.full_repo))

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
