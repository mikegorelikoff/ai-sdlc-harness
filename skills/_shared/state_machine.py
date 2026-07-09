#!/usr/bin/env python3
"""CLI for AI SDLC feature state.toon files."""

from __future__ import annotations

import argparse
import sys

from ai_sdlc_state_machine import (
    STAGE_BY_SKILL,
    begin_stage,
    complete_stage,
    flow_mode_from_args,
    initial_state,
    load_state,
    save_state,
    state_path,
    to_toon,
    validate_transition,
)


def load_or_init(feature: str, workspace: str) -> tuple[object, object]:
    """Load existing state or create an in-memory initial state."""
    path = state_path(feature, workspace)
    state = load_state(path) if path.exists() else initial_state(feature, workspace)
    return path, state


def print_messages(errors: list[str], warnings: list[str]) -> int:
    """Print validation messages and return a process status."""
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


def command_init(args: argparse.Namespace) -> int:
    """Create or overwrite a feature state file."""
    path = state_path(args.feature, args.workspace)
    state = initial_state(args.feature, args.workspace, args.entrypoint)
    save_state(path, state)
    print(f"Created state: {path}")
    return 0


def command_status(args: argparse.Namespace) -> int:
    """Print current feature state in TOON format."""
    path, state = load_or_init(args.feature, args.workspace)
    print(to_toon(state), end="")
    print(f"# state_path: {path}")
    return 0


def command_check(args: argparse.Namespace) -> int:
    """Validate whether a skill can run in the current feature state."""
    path, state = load_or_init(args.feature, args.workspace)
    flow = flow_mode_from_args(args)
    errors, warnings = validate_transition(state, args.skill, flow, args.decision_ref, args.assumption)
    rc = print_messages(errors, warnings)
    if rc == 0:
        print(f"State check passed: {path}")
    return rc


def command_begin(args: argparse.Namespace) -> int:
    """Mark a skill stage as in progress."""
    path, state = load_or_init(args.feature, args.workspace)
    flow = flow_mode_from_args(args)
    errors, warnings = begin_stage(state, args.skill, flow, args.decision_ref, args.assumption)
    rc = print_messages(errors, warnings)
    if rc:
        return rc
    save_state(path, state)
    print(f"State begin recorded: {path}")
    return 0


def command_complete(args: argparse.Namespace) -> int:
    """Mark a skill stage as complete."""
    path, state = load_or_init(args.feature, args.workspace)
    flow = flow_mode_from_args(args)
    errors, warnings = complete_stage(state, args.skill, args.artifacts, args.decision_ref, flow, args.assumption)
    rc = print_messages(errors, warnings)
    if rc:
        return rc
    save_state(path, state)
    print(f"State completion recorded: {path}")
    return 0


def add_common(parser: argparse.ArgumentParser) -> None:
    """Add shared state CLI flags."""
    parser.add_argument("--feature", required=True)
    parser.add_argument("--workspace", choices=["refinement", "implementation"], default="refinement")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--decision-ref", default="")
    parser.add_argument("--assumption", default="")


def main() -> int:
    """Parse subcommands and dispatch state-machine actions."""
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)

    init_parser = subcommands.add_parser("init", help="Create state.toon")
    add_common(init_parser)
    init_parser.add_argument("--entrypoint", choices=sorted(STAGE_BY_SKILL[skill].stage_id for skill in STAGE_BY_SKILL), default=None)
    init_parser.set_defaults(func=command_init)

    status_parser = subcommands.add_parser("status", help="Print state.toon")
    add_common(status_parser)
    status_parser.add_argument("--format", choices=["toon"], default="toon")
    status_parser.set_defaults(func=command_status)

    for name, func, help_text in (
        ("check", command_check, "Validate a skill transition"),
        ("begin", command_begin, "Mark a skill in progress"),
        ("complete", command_complete, "Mark a skill complete"),
    ):
        action_parser = subcommands.add_parser(name, help=help_text)
        add_common(action_parser)
        action_parser.add_argument("--skill", required=True, choices=sorted(STAGE_BY_SKILL))
        if name == "complete":
            action_parser.add_argument("--artifacts", default="")
        action_parser.set_defaults(func=func)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
