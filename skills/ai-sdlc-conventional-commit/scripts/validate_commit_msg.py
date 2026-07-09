#!/usr/bin/env python3
"""Validate AI SDLC Conventional Commit messages."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HEADER_RE = re.compile(
    r"^(feat|fix|docs|test|refactor|chore|ci|build|perf|revert)"
    r"(\([a-z0-9][a-z0-9-]*\))?!?: .+"
)


def read_message(path: str | None, inline: str | None) -> str:
    if inline is not None:
        return inline
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def validate(message: str, require_traceability: bool) -> list[str]:
    errors: list[str] = []
    stripped = message.strip("\n")
    if not stripped:
        return ["commit message is empty"]

    lines = stripped.splitlines()
    subject = lines[0]
    if not HEADER_RE.match(subject):
        errors.append("subject must match Conventional Commit format")
    if len(subject) > 72:
        errors.append("subject should be 72 characters or fewer")
    if subject.endswith("."):
        errors.append("subject should not end with a period")

    if len(lines) > 1 and lines[1] != "":
        errors.append("body must be separated from subject by a blank line")

    body = "\n".join(lines[2:]) if len(lines) > 2 else ""
    if require_traceability:
        if "Spec:" not in body:
            errors.append("body must include Spec traceability")
        if "Validation:" not in body:
            errors.append("body must include Validation summary")

    if "BREAKING CHANGE:" in body and "!" not in subject.split(": ", 1)[0]:
        errors.append("breaking changes should mark the subject with !")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?")
    parser.add_argument("--message")
    parser.add_argument("--require-traceability", action="store_true")
    args = parser.parse_args()

    message = read_message(args.path, args.message)
    errors = validate(message, args.require_traceability)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Commit message is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
