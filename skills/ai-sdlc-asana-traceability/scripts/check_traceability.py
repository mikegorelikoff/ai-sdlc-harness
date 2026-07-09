#!/usr/bin/env python3
"""Validate Asana traceability in an AI SDLC spec."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def related_section(requirements: str) -> str:
    marker = "## Related Asana Tickets"
    if marker not in requirements:
        return ""
    return requirements.split(marker, 1)[1].split("\n## ", 1)[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", type=Path)
    parser.add_argument("--commit-message", type=Path)
    parser.add_argument("--allow-no-ticket", action="store_true")
    args = parser.parse_args()

    requirements_path = args.spec_dir / "requirements.md"
    if not requirements_path.is_file():
        print(f"ERROR: missing {requirements_path}", file=sys.stderr)
        return 1

    requirements = requirements_path.read_text(encoding="utf-8")
    section = related_section(requirements)
    if not section:
        print("ERROR: requirements.md missing Related Asana Tickets section", file=sys.stderr)
        return 1

    asana_refs = re.findall(r"https://app\.asana\.com/[^\s)]+|`\d{10,}`", section)
    no_ticket = "No related Asana ticket found" in section
    if not asana_refs and not no_ticket:
        print("ERROR: no Asana link/GID found", file=sys.stderr)
        return 1
    if no_ticket and not args.allow_no_ticket:
        print("ERROR: no-ticket traceability is temporary; create an Asana task or pass --allow-no-ticket", file=sys.stderr)
        return 1
    if no_ticket and ("Searches performed:" not in section or "Task creation skipped:" not in section):
        print("ERROR: no-ticket traceability must list searches performed and why task creation was skipped", file=sys.stderr)
        return 1

    if args.commit_message and asana_refs:
        commit_message = args.commit_message.read_text(encoding="utf-8")
        normalized_refs = [ref.strip("`") for ref in asana_refs]
        if not any(ref in commit_message for ref in normalized_refs):
            print("ERROR: commit message does not include discovered Asana reference", file=sys.stderr)
            return 1

    if asana_refs:
        print("Asana traceability found:")
        for ref in asana_refs:
            print(f"- {ref.strip('`')}")
    else:
        print("Asana traceability records no related ticket with explicit skip.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
