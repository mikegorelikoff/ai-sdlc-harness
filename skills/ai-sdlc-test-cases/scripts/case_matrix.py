#!/usr/bin/env python3
"""Compress requirements into executable test-case matrix signals."""

from __future__ import annotations

import sys
from pathlib import Path

# Resolve the shared helper relative to this skill directory so the script stays
# portable when called from any working directory.
_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_artifact_helper import build_parser, emit_profile_report, flow_mode


def main() -> int:
    """Parse CLI flags and emit this skill-specific artifact profile."""
    # The shared parser owns common inputs, flow flags, template emission, and
    # routed file creation so every skill exposes the same command shape.
    parser = build_parser(__doc__ or "")
    args = parser.parse_args()

    # Only this profile block is skill-specific: it declares required sections,
    # keywords, prompts, artifact name, and SDLC workspace routing.
    return emit_profile_report(
        title=f"Test Case Matrix Signals: {args.feature}",
        files=args.files,
        required_sections=["Scenario Matrix", "Preconditions", "Steps", "Expected Results", "Layer Mapping", "Automation Plan"],
        keywords=["given", "when", "then", "scenario", "expected", "automation", "fixture"],
        prompts=["Create test cases only for observable behavior.", "Use structured decisions for silent expected behavior."],
        summary_limit=args.summary_limit,
        flow_mode=flow_mode(args),
        feature=args.feature,
        artifact_name="test-cases.md",
        workspace="refinement",
        emit_template=args.emit_template,
        emit_decision_log_entry=args.emit_decision_log_entry,
        write=args.write,
        skill_name="ai-sdlc-test-cases",
        state_args=args,
    )


if __name__ == "__main__":
    raise SystemExit(main())
