#!/usr/bin/env python3
"""Validate an AI SDLC sandbox approval request draft.

The approval skill uses this script before requesting escalated execution. It
keeps common safety checks deterministic: no secrets in the prompt, no reusable
prefix for destructive commands, and no overly broad prefix rules.
"""

from __future__ import annotations

import argparse
import re
import shlex
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_state_machine import add_state_arguments, run_state_action


DESTRUCTIVE = {
    "rm",
    "rmdir",
    "git reset",
    "git clean",
    "git push --force",
    "git push -f",
}

# Prefix rules matching only a generic interpreter or shell are too reusable and
# can accidentally authorize unrelated future commands.
BROAD_PREFIXES = {
    "python",
    "python3",
    "node",
    "bash",
    "zsh",
    "sh",
    "/bin/bash",
    "/bin/zsh",
    "/bin/sh",
}

# Secret-like patterns are intentionally broad. False positives are cheaper than
# sending real credentials into an approval prompt.
SECRET_PATTERNS = [
    re.compile(r"bearer\s+[A-Za-z0-9._~+/=-]{12,}", re.IGNORECASE),
    re.compile(r"api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{12,}", re.IGNORECASE),
    re.compile(r"token\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{20,}", re.IGNORECASE),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN|CLIENT_SECRET|PASSWORD|PRIVATE_KEY)\s*=\s*\S+", re.IGNORECASE),
]

# Shell features make command segmentation and prefix-rule reuse harder to reason
# about, so they are warned or rejected depending on where they appear.
SHELL_FEATURES = ["&&", "||", ";", "|", ">", "<", "$(", "`", "*", "?"]


def has_secret(text: str) -> bool:
    """Return true when text appears to contain credential material."""
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def starts_with_destructive(command: str) -> bool:
    """Detect commands that can delete data or rewrite remote history."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return True
    while tokens and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tokens[0]):
        tokens.pop(0)
    while tokens and Path(tokens[0]).name in {"env", "command", "sudo"}:
        wrapper = Path(tokens.pop(0)).name
        if wrapper in {"env", "sudo"}:
            while tokens and (tokens[0].startswith("-") or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tokens[0])):
                tokens.pop(0)
    if not tokens:
        return False
    executable = Path(tokens.pop(0)).name
    if executable in {"rm", "rmdir"}:
        return True
    if executable != "git":
        return False
    index = 0
    value_options = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
    while index < len(tokens):
        token = tokens[index]
        if token == "-c" and index + 1 < len(tokens) and tokens[index + 1].lower().startswith("alias."):
            return True
        if token in value_options:
            index += 2
        elif token.startswith(("--git-dir=", "--work-tree=", "--namespace=")):
            index += 1
        elif token.startswith("-"):
            index += 1
        else:
            break
    if index >= len(tokens):
        return False
    subcommand = tokens[index]
    remainder = tokens[index + 1:]
    return subcommand in {"reset", "clean", "rm", "restore"} or (
        subcommand == "checkout" and "--" in remainder
    ) or (
        subcommand == "push" and any(
            item in {"-f", "--force", "--force-with-lease", "--delete"}
            or item.startswith("+") or item.startswith(":")
            for item in remainder
        )
    )


def has_shell_feature(command: str) -> bool:
    """Detect shell syntax that should not be baked into reusable approvals."""
    return any(feature in command for feature in SHELL_FEATURES)


def prefix_first_token(prefix_rule: str) -> str:
    """Parse the first prefix token safely; invalid shell quoting returns empty."""
    try:
        parts = shlex.split(prefix_rule)
    except ValueError:
        return ""
    return parts[0] if parts else ""


def validate(command: str, justification: str, prefix_rule: str | None) -> tuple[list[str], list[str]]:
    """Return blocking errors and non-blocking warnings for an approval draft."""
    errors: list[str] = []
    warnings: list[str] = []

    # Basic prompt quality checks keep approval requests actionable and auditable.
    if not command.strip():
        errors.append("command is required")
    if len(justification.strip()) < 20:
        errors.append("justification must be specific and user-facing")
    if justification.strip() and not justification.strip().endswith("?"):
        warnings.append("justification should be phrased as a concise question")

    combined = " ".join(part for part in [command, justification, prefix_rule or ""] if part)
    if has_secret(combined):
        errors.append("approval request appears to contain secret material")

    # Destructive commands may still be legitimate, but never with a reusable
    # prefix rule because future commands could match the same dangerous prefix.
    if starts_with_destructive(command):
        warnings.append("destructive command detected; require explicit user confirmation and do not use prefix_rule")
        if prefix_rule:
            errors.append("prefix_rule must not be provided for destructive commands")

    if prefix_rule:
        # Prefix rules should be narrow reusable capabilities, not generic shells
        # or scripts with redirection/wildcards embedded in them.
        first = prefix_first_token(prefix_rule)
        if first in BROAD_PREFIXES or Path(first).name in {Path(item).name for item in BROAD_PREFIXES}:
            errors.append(f"prefix_rule is too broad: {first}")
        if has_shell_feature(prefix_rule):
            errors.append("prefix_rule must not include shell operators, redirection, substitutions, or wildcards")
        if len(shlex.split(prefix_rule)) < 2 and first not in {"git", "go", "npm", "curl", "docker", "brew"}:
            warnings.append("prefix_rule may be too broad; prefer a command plus subcommand or package/path")

    if has_shell_feature(command) and prefix_rule:
        warnings.append("command contains shell features; ensure prefix_rule covers only the safe reusable segment")

    return errors, warnings


def main() -> int:
    """Validate CLI input and print approval guidance for the agent."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", required=True)
    parser.add_argument("--justification", required=True)
    parser.add_argument("--prefix-rule")
    parser.add_argument("--quick-flow", action="store_true", help="Emit only blocking approval errors and high-risk warnings")
    parser.add_argument("--full-flow", action="store_true", help="Keep all warnings and strict approval guidance")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()

    state_rc = run_state_action(args, "ai-sdlc-approvals-sandbox", "refinement")
    if state_rc:
        return state_rc

    errors, warnings = validate(args.command, args.justification, args.prefix_rule)
    if args.quick_flow and not args.full_flow:
        # Quick flow keeps only warnings that change whether the agent should ask
        # for approval now or rewrite the request first.
        warnings = [warning for warning in warnings if "destructive" in warning or "secret" in warning or "too broad" in warning]
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Approval request draft is acceptable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
