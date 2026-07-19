#!/usr/bin/env python3
"""Resolve the active AI SDLC feature spec from explicit, changed, or branch context.

This small CLI exposes `spec_helpers.resolve_active_spec` so agents can resolve
the intended SDD folder without loading all helper code into context.
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
from spec_helpers import ROOT, resolve_active_spec


def main() -> int:
    """Parse resolution hints and print the selected spec plus source signal."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", nargs="?", help="Explicit spec directory or path")
    parser.add_argument("--branch", help="Branch name override")
    parser.add_argument("--files", nargs="*", help="Changed-file context override")
    parser.add_argument("--quick-flow", action="store_true", help="Prefer fast resolution from explicit inputs")
    parser.add_argument("--full-flow", action="store_true", help="Prefer stricter ambiguity reporting")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()

    state_rc = run_state_action(args, "ai-sdlc-sdd", "implementation")
    if state_rc:
        return state_rc

    try:
        # Resolution precedence lives in spec_helpers; this CLI only translates
        # command-line hints into that shared API.
        result = resolve_active_spec(
            root=ROOT,
            explicit=args.spec,
            files=args.files,
            branch=args.branch,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    # Output is intentionally one line so callers can consume it in compact
    # planning output.
    relative = result.spec_dir.relative_to(ROOT)
    print(f"{relative} [{result.source}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
