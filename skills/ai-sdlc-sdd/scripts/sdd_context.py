#!/usr/bin/env python3
"""Emit a bounded TOON context pack for one implementation SDD package."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_context import emit_context_pack, positive_int
from ai_sdlc_paths import (
    first_existing,
    internal_dir,
    legacy_plan_toon_path,
    plan_toon_path,
)
from ai_sdlc_state_machine import add_state_arguments, run_state_action
from spec_helpers import ROOT, is_feature_spec_name


def main() -> int:
    """Resolve the SDD package and emit exact cross-artifact evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", type=Path)
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--budget-tokens", type=positive_int)
    parser.add_argument("--cache-context", action="store_true")
    parser.add_argument("--refresh-context", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()

    spec_dir = args.spec_dir if args.spec_dir.is_absolute() else ROOT / args.spec_dir
    if not spec_dir.is_dir() or not is_feature_spec_name(spec_dir.name):
        parser.error("spec_dir must resolve to specs/NNN-feature-name")
    feature = args.feature if args.feature != "<feature-name>" else spec_dir.name
    args.feature = feature
    flow = "full" if args.full_flow else "quick" if args.quick_flow else "default"
    budget = args.budget_tokens or (4000 if flow == "quick" else 24000)

    state_rc = run_state_action(args, "ai-sdlc-sdd", "implementation", str(spec_dir))
    if state_rc:
        return state_rc
    files = (
        spec_dir / "requirements.md",
        spec_dir / "design.md",
        spec_dir / "test-cases.md",
        spec_dir / "qa.md",
        spec_dir / "tasks.md",
        first_existing(plan_toon_path(spec_dir), legacy_plan_toon_path(spec_dir)),
        spec_dir / "decision-log.md",
        first_existing(
            internal_dir(spec_dir) / "state.toon",
            spec_dir / "state.toon",
        ),
    )
    output = emit_context_pack(
        files=list(files),
        feature=feature,
        skill="ai-sdlc-sdd",
        workspace="implementation",
        flow_mode=flow,
        budget_tokens=budget,
        required_sections=[],
        keywords=["acceptance", "interface", "risk", "validation", "depends", "decision"],
        cache=args.cache_context or args.refresh_context,
        refresh=args.refresh_context,
        root=ROOT,
        persist_dossier=spec_dir.parent.name == "specs",
    )
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
