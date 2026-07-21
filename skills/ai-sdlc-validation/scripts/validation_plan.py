#!/usr/bin/env python3
"""Suggest focused AI SDLC validation commands from changed files.

The validation skill uses this script to turn a changed-file list into a small,
repeatable command plan. It is intentionally heuristic: it avoids expensive
analysis and focuses the agent on commands that are cheap and relevant to the
changed surface.
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


def git_changed_files() -> list[str]:
    """Return tracked and untracked paths when the user did not pass files."""
    # Combine tracked diff and untracked files so pre-commit work is not missed.
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
    """Map Go source files to package-level `go test` targets."""
    p = Path(path)
    if p.suffix != ".go":
        return None
    if "internal" in p.parts or "cmd" in p.parts:
        return "./" + str(p.parent)
    return None


def unique(items: list[str]) -> list[str]:
    """Deduplicate while preserving first-seen order for stable output."""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def feature_spec_dirs(files: list[str]) -> list[str]:
    """Extract numbered SDD spec folder names from changed spec paths."""
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
    """Return changed Python helper scripts that should be py-compiled."""
    return unique(
        [
            file
            for file in files
            if file.startswith("skills/") and file.endswith(".py") and Path(file).is_file()
        ]
    )


def main() -> int:
    """Parse files/flow flags and print a deterministic validation command plan."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*")
    parser.add_argument("--quick-flow", action="store_true", help="Suggest only focused, cheap validation commands")
    parser.add_argument("--full-flow", action="store_true", help="Suggest broader validation and governance commands")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()

    state_rc = run_state_action(args, "ai-sdlc-validation", "implementation")
    if state_rc:
        return state_rc

    files = args.files or git_changed_files()
    commands: list[str] = []

    # Language/package checks are inferred first because they are usually the
    # highest-signal validation for code changes.
    packages = unique([pkg for file in files if (pkg := package_for(file))])
    for pkg in packages:
        commands.append(f"GOCACHE=/tmp/ai-sdlc-go-cache go test {pkg}")

    if any(file.startswith("internal/platform/anchorage/") for file in files):
        commands.append("GOCACHE=/tmp/ai-sdlc-go-cache go test ./internal/platform/anchorage")
    if any(file.startswith("internal/platform/coinmetric/") for file in files):
        commands.append("GOCACHE=/tmp/ai-sdlc-go-cache go test ./internal/platform/coinmetric")
    if any(file.startswith("db/queries/") or file == "sqlc.yaml" for file in files):
        commands.append("sqlc generate")
    if any(file.startswith("skills/") for file in files):
        # Skill changes always need the manifest file to exist, and Python helper
        # changes should compile without relying on __pycache__ writes in-tree.
        changed_skills = sorted({Path(file).parts[1] for file in files if file.startswith("skills/") and len(Path(file).parts) > 1})
        for skill in changed_skills:
            if skill == "_shared":
                continue
            commands.append(f"test -f skills/{skill}/SKILL.md")
        if "_shared" in changed_skills:
            commands.append("python3 skills/_shared/sync_installed_runtime.py --check")
    compile_targets = python_compile_targets(files)
    if compile_targets:
        commands.append(
            "PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-harness-pycache python3 -m py_compile " + " ".join(compile_targets)
        )
    if not args.quick_flow and any(
        file.startswith("specs/")
        or file.startswith("skills/")
        or file in {"AGENTS.md", "CLAUDE.md"}
        for file in files
    ):
        # Broader flows include diff hygiene for docs/spec/governance surfaces.
        commands.append("git diff --check")
    for spec_dir in feature_spec_dirs(files):
        # SDD validation receives the same flow flag as the validation planner so
        # downstream gates follow the requested risk level.
        flow_arg = " --full-flow" if args.full_flow else " --quick-flow" if args.quick_flow else ""
        commands.append(f"python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/{spec_dir}{flow_arg}")
    if (args.full_flow or not args.quick_flow) and any(
        file == "AGENTS.md"
        or file == "CLAUDE.md"
        or file == "specs/spec-registry.md"
        or file.startswith("skills/")
        or file.startswith("specs/documentation/")
        for file in files
    ):
        # Skill/governance changes get an additional structure listing in
        # non-quick modes so the agent can spot missing skill files.
        commands.append("find skills -name SKILL.md -maxdepth 2")
    if any(file.startswith("specs/") or file == "AGENTS.md" for file in files):
        commands.append("git diff --check")
    for spec_dir in feature_spec_dirs(files):
        if args.full_flow:
            # Full flow expands SDD validation into the ordered gate sequence used
            # before implementation or handoff.
            commands.append(f"python3 skills/ai-sdlc-sdd/scripts/check_clarify.py specs/{spec_dir} --full-flow")
            commands.append(f"python3 skills/ai-sdlc-sdd/scripts/check_checklist.py specs/{spec_dir} --full-flow")
            commands.append(f"python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py specs/{spec_dir} --full-flow")
            commands.append(f"python3 skills/ai-sdlc-sdd/scripts/sdd_status.py --spec specs/{spec_dir} --full-flow")

    commands = unique(commands)
    if not commands:
        commands.append("git diff --check")

    mode = "full" if args.full_flow else "quick" if args.quick_flow else "default"
    print(f"Suggested validation commands ({mode} flow):")
    for command in commands:
        print(f"- {command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
