#!/usr/bin/env python3
"""Write SDD artifact sections from stdin and finalize deterministic Markdown."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_artifact_helper import emit_profile_report
from ai_sdlc_context import positive_int
from ai_sdlc_state_machine import add_state_arguments
from spec_helpers import SDD_ARTIFACT_SECTIONS, SDD_ARTIFACT_TITLES, is_feature_spec_name


def main() -> int:
    """Parse one stdin-driven SDD scaffold action."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", type=Path)
    parser.add_argument("--artifact", choices=sorted(SDD_ARTIFACT_SECTIONS))
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--section", help="Read one named section body from stdin")
    action.add_argument("--finalize", action="store_true", help="Validate and finalize the selected artifact")
    action.add_argument("--decision-row", action="store_true", help="Read one decision-log table row from stdin")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--artifact-status")
    parser.add_argument("--artifact-owner")
    parser.add_argument("--artifact-tag", action="append", default=[])
    parser.add_argument("--max-artifact-tokens", type=positive_int, default=24000)
    add_state_arguments(parser)
    args = parser.parse_args()

    if not args.artifact and not args.decision_row:
        parser.error("--artifact is required with --section or --finalize")

    spec_dir = args.spec_dir.resolve()
    if spec_dir.parent.name != "specs" or not is_feature_spec_name(spec_dir.name):
        parser.error("spec_dir must match specs/NNN-feature-name")

    args.feature = spec_dir.name
    args.files = []
    args.summary_limit = 5
    args.emit_template = False
    args.emit_decision_log_entry = False
    args.write = False

    # The shared router writes under `specs/<feature>` relative to the workspace root.
    os.chdir(spec_dir.parent.parent)
    artifact = args.artifact or "requirements"
    return emit_profile_report(
        title=f"SDD {SDD_ARTIFACT_TITLES[artifact]}: {args.feature}",
        files=[],
        required_sections=SDD_ARTIFACT_SECTIONS[artifact],
        keywords=[],
        prompts=[],
        summary_limit=args.summary_limit,
        flow_mode="full" if args.full_flow else "quick" if args.quick_flow else "default",
        feature=args.feature,
        artifact_name=f"{artifact}.md",
        workspace="implementation",
        emit_template=False,
        emit_decision_log_entry=False,
        write=False,
        skill_name="ai-sdlc-sdd",
        state_args=args,
        document_title=SDD_ARTIFACT_TITLES[artifact],
    )


if __name__ == "__main__":
    raise SystemExit(main())
