#!/usr/bin/env python3
"""Validate and route traceable UX specifications."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from datetime import date
from pathlib import Path
from typing import Any


SCHEMA = "ai-sdlc-ux-input/v1"
COLLECTIONS = ("actors", "journeys", "states", "accessibility", "content")


def toon(value: object) -> str:
    """Escape one machine scalar."""
    if isinstance(value, list):
        value = "/".join(str(item) for item in value)
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def load(path: Path) -> tuple[dict[str, Any], list[str]]:
    """Load a UX input safely."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read UX input: {exc}"]
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        return {}, [f"input schema must be {SCHEMA}"]
    return value, []


def required(item: dict[str, Any], fields: tuple[str, ...], prefix: str) -> list[str]:
    """Validate required text fields."""
    return [f"{prefix}: {field} is required" for field in fields if not isinstance(item.get(field), str) or not item.get(field, "").strip()]


def traced(item: dict[str, Any], prefix: str) -> list[str]:
    """Validate trace targets."""
    refs = item.get("trace_targets")
    return [] if isinstance(refs, list) and refs and all(isinstance(ref, str) and ref.strip() for ref in refs) else [f"{prefix}: trace_targets must be non-empty"]


def validate(value: dict[str, Any], full_flow: bool) -> list[str]:
    """Validate UX actors, behavior, and evidence coverage."""
    errors: list[str] = []
    if not isinstance(value.get("context"), str) or not value.get("context", "").strip():
        errors.append("context is required")
    for name in COLLECTIONS:
        if not isinstance(value.get(name), list) or not all(isinstance(item, dict) for item in value.get(name, [])):
            errors.append(f"{name} must be an array of objects")
    if errors:
        return errors
    actor_ids: list[str] = []
    for index, item in enumerate(value["actors"], start=1):
        errors.extend(required(item, ("id", "name"), f"actors {index}"))
        actor_ids.append(str(item.get("id", "")))
        for field in ("goals", "needs"):
            if not isinstance(item.get(field), list) or not item[field]:
                errors.append(f"actors {index}: {field} must be non-empty")
    if len(actor_ids) != len(set(actor_ids)):
        errors.append("actor IDs must be unique")
    journey_ids: list[str] = []
    for index, item in enumerate(value["journeys"], start=1):
        prefix = f"journeys {index}"
        errors.extend(required(item, ("id", "actor", "goal", "acceptance"), prefix))
        errors.extend(traced(item, prefix))
        journey_ids.append(str(item.get("id", "")))
        if item.get("actor") not in actor_ids:
            errors.append(f"{prefix}: actor must reference a known actor")
        if not isinstance(item.get("steps"), list) or not item["steps"] or not all(isinstance(step, str) and step.strip() for step in item["steps"]):
            errors.append(f"{prefix}: steps must be a non-empty string array")
    if len(journey_ids) != len(set(journey_ids)):
        errors.append("journey IDs must be unique")
    for index, item in enumerate(value["states"], start=1):
        prefix = f"states {index}"
        errors.extend(required(item, ("surface", "state", "behavior", "recovery"), prefix))
        errors.extend(traced(item, prefix))
    for index, item in enumerate(value["accessibility"], start=1):
        prefix = f"accessibility {index}"
        errors.extend(required(item, ("requirement", "evidence"), prefix))
        errors.extend(traced(item, prefix))
        if item.get("status") not in {"planned", "passed", "failed", "blocked"}:
            errors.append(f"{prefix}: invalid status")
    for index, item in enumerate(value["content"], start=1):
        errors.extend(required(item, ("surface", "intent", "guidance"), f"content {index}"))
    if full_flow:
        for name in ("journeys", "states", "accessibility"):
            if not value[name]:
                errors.append(f"full flow requires at least one {name} entry")
    return errors


def render_toon(root: Path, flow: str, value: dict[str, Any]) -> str:
    """Render bounded machine UX output."""
    fields = {"actors": ("id", "name", "goals", "needs"), "journeys": ("id", "actor", "goal", "steps", "acceptance", "trace_targets"), "states": ("surface", "state", "behavior", "recovery", "trace_targets"), "accessibility": ("requirement", "evidence", "status", "trace_targets"), "content": ("surface", "intent", "guidance")}
    lines = ["schema: ai-sdlc-ux/v1", f"feature_root: {toon(root.as_posix())}", f"flow_mode: {flow}", f"context: {toon(value['context'])}"]
    for name, columns in fields.items():
        lines.extend(["", f"{name}[{len(value[name])}]{{{','.join(columns)}}}:"])
        lines.extend("  " + ",".join(toon(item.get(field, "")) for field in columns) for item in value[name])
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(root: Path, flow: str, value: dict[str, Any]) -> str:
    """Render readable UX output with metadata."""
    refs = sorted({ref for name in ("journeys", "states", "accessibility") for item in value[name] for ref in item["trace_targets"]})
    workspace = "implementation" if root.parent.name == "specs" else "refinement"
    lines = ["---", "artifact_metadata:", '  schema: "ai-sdlc-ux-metadata/v1"', f'  feature: "{toon(root.name)}"', '  artifact: "ux-spec.md"', f'  path: "{toon((root / "ux-spec.md").as_posix())}"', f'  workspace: "{workspace}"', '  skill: "ai-sdlc-ux"', f'  flow_mode: "{flow}"', f'  state_file: "{toon((root / "_ai_sdlc/state.toon").as_posix())}"', '  status: "review"', f'  updated_at: "{date.today().isoformat()}"', "  trace_ids:"]
    lines.extend(f'    - "{toon(ref)}"' for ref in refs)
    lines.extend(["  metatags:", '    - "ai-sdlc"', '    - "ux"', '    - "experience"', '    - "traceable"', "---", "", "# UX Specification", "", "## Context", "", value["context"]])
    for name in COLLECTIONS:
        lines.extend(["", f"## {name.title()}"])
        lines.extend(["", "- None."] if not value[name] else ["", *["- " + "; ".join(f"{key}: {toon(field)}" for key, field in item.items()) for item in value[name]]])
    return "\n".join(lines).rstrip() + "\n"


def atomic_write(path: Path, content: str) -> None:
    """Write one UX artifact atomically."""
    if any(component.is_symlink() for component in (path, *list(path.parents)[:4])):
        raise SystemExit(f"ERROR: output path contains symlink component: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    """Validate and route UX specifications."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feature_root", type=Path)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--write", action="store_true")
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
    root = args.feature_root.resolve()
    if args.begin_state or args.complete_state:
        print("ERROR: UX generation is read-only with respect to lifecycle state")
        return 1
    if not root.is_dir():
        print(f"ERROR: feature root does not exist: {root}")
        return 1
    if args.state_check and not (root / "_ai_sdlc/state.toon").is_file():
        print("ERROR: canonical state is missing")
        return 1
    value, errors = load(args.input)
    if not errors:
        errors.extend(validate(value, args.full_flow))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    flow = "full" if args.full_flow else "quick" if args.quick_flow else "default"
    human, machine = render_markdown(root, flow, value), render_toon(root, flow, value)
    if args.write:
        atomic_write(root / "ux-spec.md", human)
        atomic_write(root / "_ai_sdlc/ux-spec.toon", machine)
    print(machine if args.format == "toon" else human, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
