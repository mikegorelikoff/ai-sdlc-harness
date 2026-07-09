#!/usr/bin/env python3
"""Print Asana project, section, and assignee instructions for AI SDLC tasks."""

from __future__ import annotations

import argparse
import json


AI_SDLC_PROJECT_ID = "1213092419088959"

SECTION_BY_STATE = {
    "backlog": ("1213161266359939", "Backlog"),
    "todo": ("1213161266359940", "To do"),
    "on-hold": ("1213669404768992", "On Hold"),
    "in-progress": ("1213161266359941", "In progress"),
    "code-review": ("1213161266359949", "Code review"),
    "ready-for-test": ("1213161266359950", "Ready for test"),
    "testing": ("1213161266359951", "Testing"),
    "ready-for-release": ("1213161266359953", "Ready for release"),
    "released": ("1213161266359954", "Released"),
    "done": ("1213161266359955", "Done"),
    "out-of-scope": ("1213776259909542", "Out of Scope"),
    "inbound": ("1214125643704563", "Inbound"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="Asana task GID")
    parser.add_argument(
        "--state",
        required=True,
        choices=sorted(SECTION_BY_STATE),
        help="Workflow state to map to an AI SDLC 2.0 section",
    )
    parser.add_argument(
        "--assignee",
        default="me",
        help='Assignee identifier for mcp__asana__update_tasks; default: "me". Use "none" to omit.',
    )
    args = parser.parse_args()

    section_id, section_name = SECTION_BY_STATE[args.state]
    task_update = {
        "task": args.task,
        "add_projects": [
            {
                "project_id": AI_SDLC_PROJECT_ID,
                "section_id": section_id,
            }
        ],
    }
    if args.assignee.lower() != "none":
        task_update["assignee"] = args.assignee

    payload = {
        "tasks": [task_update]
    }

    print(f"Project: AI SDLC 2.0 ({AI_SDLC_PROJECT_ID})")
    print(f"Section: {section_name} ({section_id})")
    if args.assignee.lower() != "none":
        print(f"Assignee: {args.assignee}")
    print("Use mcp__asana__update_tasks with:")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
