#!/usr/bin/env python3
"""Compress source notes into BA context signals."""

from __future__ import annotations

import sys
from pathlib import Path

# Resolve only one of the two packaged sibling locations. Resolving and
# bounding the directory first prevents environment input, the current working
# directory, or a symlink from redirecting the import outside the skills root.
_SKILLS_ROOT = Path(__file__).resolve().parents[2]
_CANDIDATES = (
    _SKILLS_ROOT / "_shared",
    _SKILLS_ROOT / "ai-sdlc-shared-runtime" / "scripts",
)
_SHARED = next(
    (
        candidate.resolve()
        for candidate in _CANDIDATES
        if candidate.is_dir()
        and candidate.resolve().is_relative_to(_SKILLS_ROOT)
        and (candidate / "ai_sdlc_artifact_helper.py").is_file()
    ),
    None,
)
if _SHARED is None:
    raise ImportError("trusted AI SDLC shared runtime was not found under the installed skills root")
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
        title=f"BA Context Signals: {args.feature}",
        files=args.files,
        required_sections=["Goal", "Problem", "Actors", "Current Behavior", "Desired Behavior", "Business Rules", "Acceptance Criteria", "Open Questions"],
        keywords=["actor", "workflow", "rule", "assumption", "acceptance", "constraint", "out of scope"],
        prompts=["Convert missing required sections into assumptions or open questions.", "Record material product decisions in decision-log.md."],
        summary_limit=args.summary_limit,
        flow_mode=flow_mode(args),
        feature=args.feature,
        artifact_name="business-context.md",
        workspace="refinement",
        emit_template=args.emit_template,
        emit_decision_log_entry=args.emit_decision_log_entry,
        write=args.write,
        skill_name="ai-sdlc-ba",
        state_args=args,
    )


if __name__ == "__main__":
    raise SystemExit(main())
