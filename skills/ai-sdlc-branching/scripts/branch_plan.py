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


def git_status() -> str:
    """Return short git status output; an empty string means clean tree."""
    result = subprocess.run(["git", "status", "--short"], text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
    return result.stdout.strip()


def main() -> int:
    """Parse CLI flags, emit branch-profile guidance, and append git signals."""
    # The shared parser owns the common artifact-profile flags. This script adds
    # `--spec` only for branch-name derivation from an explicit spec folder.
    parser = build_parser(__doc__ or "")
    parser.add_argument("--spec", default="")
    args = parser.parse_args()

    # Capture git state before printing the profile so the final report can
    # warn about unrelated or unstaged changes.
    status = git_status()

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
