#!/usr/bin/env python3
"""Render a normalized AI SDLC post-workflow handoff report."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class NextAction:
    """A required or optional downstream action."""

    skill: str
    reason: str
    command: str
    expected_artifact: str


def parse_action(value: str) -> NextAction:
    """Parse a pipe-delimited next-action value."""
    parts = [part.strip() for part in value.split("|", 3)]
    if len(parts) != 4 or not all(parts):
        raise argparse.ArgumentTypeError("action must be skill|reason|command|expected_artifact")
    return NextAction(*parts)


def toon(value: object) -> str:
    """Escape one scalar for the repository TOON subset."""
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def validate(result: str, blockers: list[str], required: NextAction | None) -> list[str]:
    """Return semantic handoff errors."""
    errors: list[str] = []
    if result == "blocked" and not blockers:
        errors.append("blocked result requires at least one blocker")
    if result in {"complete", "partial"} and required is None:
        errors.append(f"{result} result requires next_required; use ai-sdlc-navigator when no downstream action is known")
    return errors


def render_markdown(result: str, summary: str, blockers: list[str], required: NextAction, optional: list[NextAction]) -> str:
    """Render a human-readable handoff."""
    lines = ["# AI SDLC Workflow Handoff", "", f"- Result: `{result}`", f"- Summary: {summary}", "", "## Blockers"]
    lines.extend(f"- {item}" for item in blockers)
    if not blockers:
        lines.append("- None.")
    lines.extend(["", "## Next Required", f"- Skill: `{required.skill}`", f"- Reason: {required.reason}", f"- Command: `{required.command}`", f"- Expected artifact: `{required.expected_artifact}`", "", "## Next Optional"])
    lines.extend(f"- `{item.skill}` — {item.reason}; command: `{item.command}`; expected: `{item.expected_artifact}`" for item in optional)
    if not optional:
        lines.append("- None.")
    return "\n".join(lines).rstrip() + "\n"


def render_toon(result: str, summary: str, blockers: list[str], required: NextAction, optional: list[NextAction]) -> str:
    """Render a compact machine-readable handoff."""
    lines = ["schema: ai-sdlc-handoff/v1", f"result: {toon(result)}", f"summary: {toon(summary)}", "", f"blockers[{len(blockers)}]{{message}}:"]
    lines.extend(f"  {toon(item)}" for item in blockers)
    lines.extend(["", "next_required[1]{skill,reason,command,expected_artifact}:", "  " + ",".join(toon(value) for value in (required.skill, required.reason, required.command, required.expected_artifact)), "", f"next_optional[{len(optional)}]{{skill,reason,command,expected_artifact}}:"])
    lines.extend("  " + ",".join(toon(value) for value in (item.skill, item.reason, item.command, item.expected_artifact)) for item in optional)
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """Validate and render one workflow handoff."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", choices=("complete", "partial", "blocked"), required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--blocker", action="append", default=[])
    parser.add_argument("--next-required", type=parse_action, required=True)
    parser.add_argument("--next-optional", type=parse_action, action="append", default=[])
    parser.add_argument("--format", choices=("markdown", "toon"), default="markdown")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    args = parser.parse_args()

    errors = validate(args.result, args.blocker, args.next_required)
    if args.begin_state or args.complete_state:
        errors.append("handoff emitter is read-only; lifecycle transitions belong to the owning workflow")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    renderer = render_toon if args.format == "toon" else render_markdown
    print(renderer(args.result, args.summary, args.blocker, args.next_required, args.next_optional), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
