#!/usr/bin/env python3
"""Suggest focused AI SDLC validation commands from changed files."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def git_changed_files() -> list[str]:
    tracked = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    files = tracked.stdout.splitlines() + untracked.stdout.splitlines()
    return unique([line.strip() for line in files if line.strip()])


def package_for(path: str) -> str | None:
    p = Path(path)
    if p.suffix != ".go":
        return None
    if "internal" in p.parts or "cmd" in p.parts:
        return "./" + str(p.parent)
    return None


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def feature_spec_dirs(files: list[str]) -> list[str]:
    spec_dirs: list[str] = []
    for file in files:
        parts = Path(file).parts
        if len(parts) < 3 or parts[0] != "specs":
            continue
        spec_dir = parts[1]
        if len(spec_dir) >= 4 and spec_dir[:3].isdigit() and spec_dir[3] == "-":
            spec_dirs.append(spec_dir)
    return unique(spec_dirs)


def python_compile_targets(files: list[str]) -> list[str]:
    return unique(
        [
            file
            for file in files
            if (file.startswith(".codex/hooks/") and file.endswith(".py"))
            or (file.startswith(".codex/scripts/") and file.endswith(".py"))
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()

    files = args.files or git_changed_files()
    commands: list[str] = []

    packages = unique([pkg for file in files if (pkg := package_for(file))])
    for pkg in packages:
        commands.append(f"GOCACHE=/tmp/ai-sdlc-go-cache go test {pkg}")

    if any(file.startswith("internal/platform/anchorage/") for file in files):
        commands.append("GOCACHE=/tmp/ai-sdlc-go-cache go test ./internal/platform/anchorage")
    if any(file.startswith("internal/platform/coinmetric/") for file in files):
        commands.append("GOCACHE=/tmp/ai-sdlc-go-cache go test ./internal/platform/coinmetric")
    if any(file.startswith("db/queries/") or file == "sqlc.yaml" for file in files):
        commands.append("sqlc generate")
    if any(file.startswith(".codex/skills/") for file in files):
        for skill in sorted({Path(file).parts[2] for file in files if file.startswith(".codex/skills/")}):
            commands.append(f"python3 .codex/scripts/quick_validate_skill.py .codex/skills/{skill}")
    compile_targets = python_compile_targets(files)
    if compile_targets:
        commands.append(
            "python3 .codex/scripts/python_compile_check.py " + " ".join(compile_targets)
        )
    if any(
        file.startswith(".codex/hooks/")
        or file.startswith(".codex/scripts/")
        or file in {".codex/config.toml"}
        or file.startswith(".codex/agents/")
        for file in files
    ):
        commands.append("python3 .codex/hooks/tests/test_hook_runtime.py")
    if any(
        file.startswith(".codex/")
        or file.startswith("specs/")
        or file in {"AGENTS.md", "CLAUDE.md"}
        for file in files
    ):
        commands.append("python3 .codex/scripts/codex_ai_lint.py --format text")
    for spec_dir in feature_spec_dirs(files):
        commands.append(f"python3 .codex/skills/ai-sdlc-sdd/scripts/validate_spec.py specs/{spec_dir}")
    if any(
        file == "AGENTS.md"
        or file == "CLAUDE.md"
        or file == "specs/spec-registry.md"
        or file.startswith(".codex/")
        or file.startswith("specs/documentation/")
        for file in files
    ):
        commands.append("python3 .codex/scripts/codex_governance_audit.py")
    if any(file.startswith("specs/") or file == "AGENTS.md" for file in files):
        commands.append("git diff --check")
    for spec_dir in feature_spec_dirs(files):
        commands.append(f"python3 .codex/skills/ai-sdlc-sdd/scripts/check_clarify.py specs/{spec_dir}")
        commands.append(f"python3 .codex/skills/ai-sdlc-sdd/scripts/check_checklist.py specs/{spec_dir}")
        commands.append(f"python3 .codex/skills/ai-sdlc-sdd/scripts/analyze_spec.py specs/{spec_dir}")
        commands.append(f"python3 .codex/skills/ai-sdlc-sdd/scripts/sdd_status.py --spec specs/{spec_dir}")

    commands = unique(commands)
    if not commands:
        commands.append("git diff --check")

    print("Suggested validation commands:")
    for command in commands:
        print(f"- {command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
