#!/usr/bin/env python3
"""Draft a structured Asana task description for AI SDLC work."""

from __future__ import annotations

import argparse


def block(title: str, text: str) -> str:
    return f"{title}:\n{text.strip()}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--problem", required=True)
    parser.add_argument("--changes", required=True)
    parser.add_argument("--requirements", required=True)
    parser.add_argument("--expected", required=True)
    parser.add_argument("--acceptance", required=True)
    args = parser.parse_args()

    notes = "\n\n".join(
        [
            block("Summary", args.summary),
            block("Description", args.problem),
            block("Proposed Changes", args.changes),
            block("Functional Requirements", args.requirements),
            block("Expected Behavior", args.expected),
            block("Acceptance Criteria", args.acceptance),
        ]
    )
    print(notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
