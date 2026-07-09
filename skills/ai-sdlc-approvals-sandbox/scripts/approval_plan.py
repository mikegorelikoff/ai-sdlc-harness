#!/usr/bin/env python3
"""Validate an AI SDLC sandbox approval request draft."""

from __future__ import annotations

import argparse
import re
import shlex
import sys


DESTRUCTIVE = {
    "rm",
    "rmdir",
    "git reset",
    "git clean",
    "git push --force",
    "git push -f",
}

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

SECRET_PATTERNS = [
    re.compile(r"bearer\s+[A-Za-z0-9._~+/=-]{12,}", re.IGNORECASE),
    re.compile(r"api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{12,}", re.IGNORECASE),
    re.compile(r"token\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{20,}", re.IGNORECASE),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]

SHELL_FEATURES = ["&&", "||", ";", "|", ">", "<", "$(", "`", "*", "?"]


def has_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def starts_with_destructive(command: str) -> bool:
    normalized = " ".join(command.strip().split())
    return any(normalized == item or normalized.startswith(f"{item} ") for item in DESTRUCTIVE)


def has_shell_feature(command: str) -> bool:
    return any(feature in command for feature in SHELL_FEATURES)


def prefix_first_token(prefix_rule: str) -> str:
    try:
        parts = shlex.split(prefix_rule)
    except ValueError:
        return ""
    return parts[0] if parts else ""


def validate(command: str, justification: str, prefix_rule: str | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not command.strip():
        errors.append("command is required")
    if len(justification.strip()) < 20:
        errors.append("justification must be specific and user-facing")
    if justification.strip() and not justification.strip().endswith("?"):
        warnings.append("justification should be phrased as a concise question")

    combined = " ".join(part for part in [command, justification, prefix_rule or ""] if part)
    if has_secret(combined):
        errors.append("approval request appears to contain secret material")

    if starts_with_destructive(command):
        warnings.append("destructive command detected; require explicit user confirmation and do not use prefix_rule")
        if prefix_rule:
            errors.append("prefix_rule must not be provided for destructive commands")

    if prefix_rule:
        first = prefix_first_token(prefix_rule)
        if first in BROAD_PREFIXES:
            errors.append(f"prefix_rule is too broad: {first}")
        if has_shell_feature(prefix_rule):
            errors.append("prefix_rule must not include shell operators, redirection, substitutions, or wildcards")
        if len(shlex.split(prefix_rule)) < 2 and first not in {"git", "go", "npm", "curl", "docker", "brew"}:
            warnings.append("prefix_rule may be too broad; prefer a command plus subcommand or package/path")

    if has_shell_feature(command) and prefix_rule:
        warnings.append("command contains shell features; ensure prefix_rule covers only the safe reusable segment")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", required=True)
    parser.add_argument("--justification", required=True)
    parser.add_argument("--prefix-rule")
    args = parser.parse_args()

    errors, warnings = validate(args.command, args.justification, args.prefix_rule)
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
