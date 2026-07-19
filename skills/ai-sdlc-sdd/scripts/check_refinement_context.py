#!/usr/bin/env python3
"""Check upstream refinement context for SDD full-flow work."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_state_machine import add_state_arguments, run_state_action
from spec_helpers import ROOT, upstream_refinement_errors


def main() -> int:
    """Validate full-flow upstream refinement requirements."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", type=Path)
    parser.add_argument("--quick-flow", action="store_true", help="Do not block on missing upstream refinement")
    parser.add_argument("--full-flow", action="store_true", help="Require completed upstream refinement context")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()

    spec_dir = args.spec_dir if args.spec_dir.is_absolute() else ROOT / args.spec_dir
    state_rc = run_state_action(args, "ai-sdlc-sdd", "implementation", str(spec_dir))
    if state_rc:
        return state_rc

    if args.quick_flow and not args.full_flow:
        print("Quick flow: upstream refinement context is advisory.")
        return 0

    errors = upstream_refinement_errors(spec_dir, args.feature)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Upstream refinement context is ready: {spec_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
