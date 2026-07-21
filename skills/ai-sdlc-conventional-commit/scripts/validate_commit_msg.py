#!/usr/bin/env python3
"""Validate AI SDLC Conventional Commit messages.

The script checks the cheap deterministic parts of commit-message quality:
Conventional Commit header shape, subject hygiene, body spacing, optional SDD
traceability, and breaking-change consistency.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

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
        and (candidate / "ai_sdlc_state_machine.py").is_file()
    ),
    None,
)
if _SHARED is None:
    raise ImportError("trusted AI SDLC shared runtime was not found under the installed skills root")
sys.path.insert(0, str(_SHARED))
from ai_sdlc_state_machine import add_state_arguments, run_state_action


HEADER_RE = re.compile(
    r"^(feat|fix|docs|test|refactor|chore|ci|build|perf|revert)"
    r"(\([a-z0-9][a-z0-9-]*\))?!?: .+"
)
TASK_TRAILER_RE = re.compile(r"(?m)^Task: T\d{3}(?:, T\d{3})*$")


def read_message(path: str | None, inline: str | None) -> str:
    """Read a commit message from `--message`, a file path, or stdin."""
    if inline is not None:
        return inline
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def validate(message: str, require_traceability: bool) -> list[str]:
    """Return validation errors for a candidate commit message."""
    errors: list[str] = []
    stripped = message.strip("\n")
    if not stripped:
        return ["commit message is empty"]

    # Header checks mirror the Conventional Commit shape used by the repo while
    # keeping the subject short enough for git log and release-note tooling.
    lines = stripped.splitlines()
    subject = lines[0]
    if not HEADER_RE.match(subject):
        errors.append("subject must match Conventional Commit format")
    if len(subject) > 72:
        errors.append("subject should be 72 characters or fewer")
    if subject.endswith("."):
        errors.append("subject should not end with a period")

    # Conventional Commit bodies must be separated by a blank line to keep
    # parsers from treating body text as part of the subject.
    if len(lines) > 1 and lines[1] != "":
        errors.append("body must be separated from subject by a blank line")

    body = "\n".join(lines[2:]) if len(lines) > 2 else ""
    if require_traceability:
        # Full flow requires evidence that the commit maps back to a spec, one
        # or more completed SDD tasks, and a validation command/result.
        if "Spec:" not in body:
            errors.append("body must include Spec traceability")
        if not TASK_TRAILER_RE.search(body):
            errors.append("body must include Task traceability as Task: TNNN")
        if "Validation:" not in body:
            errors.append("body must include Validation summary")

    # Breaking-change bodies and `!` headers should agree so downstream release
    # tooling does not miss a compatibility break.
    if "BREAKING CHANGE:" in body and "!" not in subject.split(": ", 1)[0]:
        errors.append("breaking changes should mark the subject with !")

    return errors


def main() -> int:
    """Parse CLI arguments, apply flow semantics, and print validation status."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?")
    parser.add_argument("--message")
    parser.add_argument("--require-traceability", action="store_true")
    parser.add_argument("--quick-flow", action="store_true", help="Validate the commit format only unless traceability is explicitly required")
    parser.add_argument("--full-flow", action="store_true", help="Require traceability metadata")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()

    state_rc = run_state_action(args, "ai-sdlc-conventional-commit", "implementation")
    if state_rc:
        return state_rc

    message = read_message(args.path, args.message)
    errors = validate(message, args.require_traceability or args.full_flow)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Commit message is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
