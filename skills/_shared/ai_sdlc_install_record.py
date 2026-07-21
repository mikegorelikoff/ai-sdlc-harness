#!/usr/bin/env python3
"""Validate a portable harness install record and its managed inventory."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED = {"schema", "revision", "skills_cli", "agent", "selection", "inventory"}
SKILL_NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def published_inventory() -> list[str]:
    """Read the packaged full-skill inventory in source or installed layouts."""
    script = Path(__file__).resolve()
    candidates = (
        script.parents[1] / "references" / "ai-sdlc-managed-skills.txt",
        script.parents[2] / "config" / "ai-sdlc-managed-skills.txt",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8").splitlines()
    return []


def validate(record_path: Path, skills_root: Path) -> list[str]:
    try:
        value = json.loads(record_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read install record: {exc}"]
    if not isinstance(value, dict) or set(value) != REQUIRED:
        return ["install record must contain exactly schema, revision, skills_cli, agent, selection, inventory"]
    errors: list[str] = []
    if value["schema"] != "ai-sdlc-install-record/v1":
        errors.append("install record schema must be ai-sdlc-install-record/v1")
    if not isinstance(value["revision"], str) or not re.fullmatch(r"[0-9a-f]{40}", value["revision"]):
        errors.append("install record revision must be a lowercase 40-character Git SHA")
    if not isinstance(value["skills_cli"], str) or not re.fullmatch(r"\d+\.\d+\.\d+", value["skills_cli"]):
        errors.append("install record skills_cli must be an exact semantic version")
    if not isinstance(value["agent"], str) or not value["agent"].strip():
        errors.append("install record agent must be non-empty")
    if value["selection"] not in {"all-skills", "explicit-skills"}:
        errors.append("install record selection is invalid")
    if value["inventory"] != ".ai-sdlc/harness-managed-skills.txt":
        errors.append("install record inventory must be .ai-sdlc/harness-managed-skills.txt")
        return errors
    inventory_path = record_path.resolve().parent.parent / value["inventory"]
    try:
        names = inventory_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"cannot read managed inventory: {exc}")
        return errors
    if names != sorted(set(names)) or not names:
        errors.append("managed inventory must contain unique sorted skill names")
    if any(not SKILL_NAME_RE.fullmatch(name) for name in names):
        errors.append("managed inventory contains an invalid skill name")
    published = published_inventory()
    if not published:
        errors.append("packaged full-skill inventory is missing")
    elif value["selection"] == "all-skills" and names != published:
        errors.append("all-skills inventory must exactly match the packaged full-skill inventory")
    elif value["selection"] == "explicit-skills":
        unknown = sorted(set(names) - set(published))
        if unknown:
            errors.append(f"explicit-skills inventory contains unpublished skills: {', '.join(unknown)}")
        if "ai-sdlc-shared-runtime" not in names:
            errors.append("explicit-skills inventory must include ai-sdlc-shared-runtime")
    installed = sorted(path.name for path in skills_root.iterdir() if path.is_dir()) if skills_root.is_dir() else []
    missing = sorted(set(names) - set(installed))
    if missing:
        errors.append(f"managed skills are not installed: {', '.join(missing)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, default=Path(".ai-sdlc/harness-install.json"))
    parser.add_argument("--skills-root", type=Path, default=Path(".agents/skills"))
    args = parser.parse_args()
    errors = validate(args.record, args.skills_root)
    for error in errors:
        print(f"ERROR: {error}")
    if not errors:
        print(f"Harness install record valid: {args.record}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
