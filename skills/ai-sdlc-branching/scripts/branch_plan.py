#!/usr/bin/env python3
"""Compress spec/task context into branch alignment signals.

The script is a thin artifact-profile wrapper with one extra responsibility:
it inspects the current git working tree and emits branch naming hints so the
branching skill can avoid wasting tokens on routine repository checks.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# Resolve the shared helper relative to this skill directory so the script stays
# portable when called from any working directory.
_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_artifact_helper import build_parser, emit_profile_report, flow_mode


def git_status(repo_root: Path | None = None) -> str:
    """Return short git status output; an empty string means clean tree."""
    result = subprocess.run(["git", "status", "--short"], cwd=repo_root, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
    return result.stdout.strip()


def git_lines(*args: str, repo_root: Path | None = None) -> list[str]:
    """Return non-empty Git output for a read-only repository probe."""
    result = subprocess.run(["git", *args], cwd=repo_root, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def resolve_base_branch(repo_root: Path | None = None) -> tuple[str, str]:
    """Resolve an explicit/configured or repository-default base branch."""
    configured = subprocess.run(
        ["git", "config", "--get", "ai-sdlc.baseBranch"], text=True,
        cwd=repo_root, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    ).stdout.strip()
    if configured:
        return configured, "repository config ai-sdlc.baseBranch"
    remote_head = git_lines("symbolic-ref", "--short", "refs/remotes/origin/HEAD", repo_root=repo_root)
    if remote_head:
        return remote_head[0].removeprefix("origin/"), "origin/HEAD"
    for candidate in ("dev", "main", "master"):
        if git_lines("show-ref", "--verify", f"refs/heads/{candidate}", repo_root=repo_root):
            return candidate, "local branch"
    return "", "no declared base branch"


def main() -> int:
    """Parse CLI flags, emit branch-profile guidance, and append git signals."""
    # The shared parser owns the common artifact-profile flags. This script adds
    # `--spec` only for branch-name derivation from an explicit spec folder.
    parser = build_parser(__doc__ or "")
    parser.add_argument("--spec", default="")
    args = parser.parse_args()

    # Capture git state before printing the profile so the final report can
    # warn about unrelated or unstaged changes.
    repo_root = Path.cwd()
    status = git_status(repo_root)
    base_branch, base_source = resolve_base_branch(repo_root)

    # Skill-specific profile: required sections and keywords describe the
    # branch-planning evidence the agent should preserve.
    rc = emit_profile_report(
        title=f"Branch Alignment Signals: {args.feature}",
        files=args.files,
        required_sections=["Implementation", "Testing", "Documentation"],
        keywords=["task", "branch", "spec", "implementation", "testing", "documentation"],
        prompts=["Create branch names from stable feature/task identifiers.", "Do not hide unrelated dirty-tree changes."],
        summary_limit=args.summary_limit,
        flow_mode=flow_mode(args),
        feature=args.feature,
        artifact_name="branch-plan.md",
        workspace="implementation",
        emit_template=args.emit_template,
        emit_decision_log_entry=args.emit_decision_log_entry,
        write=args.write,
        skill_name="ai-sdlc-branching",
        state_args=args,
    )
    print()
    print("## Git Working Tree")
    print(f"- Dirty tree: {'yes' if status else 'no'}")
    print(f"- Base branch: {base_branch or 'BLOCKED'} ({base_source})")
    if status:
        print("- Branch creation blocker: resolve related/unrelated changes before carrying them to a new branch.")
    if not base_branch:
        print("- Branch creation blocker: declare ai-sdlc.baseBranch or configure origin/HEAD before branching.")
    if status:
        # Count status rows instead of parsing porcelain details; the agent only
        # needs a cheap signal that multiple paths may require separation.
        changed = len([line for line in status.splitlines() if line.strip()])
        print(f"- Changed paths: {changed}")
    if args.spec:
        # Convert spec folder names into conservative branch-safe slugs.
        slug = re.sub(r"[^a-zA-Z0-9-]+", "-", Path(args.spec).name).strip("-").lower()
        print(f"- Suggested branch prefix: feature/{slug}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
