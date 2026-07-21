#!/usr/bin/env python3
"""Validate and route traceable architecture artifacts."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from datetime import date
from pathlib import Path
from typing import Any


SCHEMA = "ai-sdlc-architecture-input/v1"
COLLECTIONS = ("constraints", "components", "interfaces", "decisions", "risks", "validation")


def toon(value: object) -> str:
    """Escape one TOON scalar."""
    if isinstance(value, list):
        value = "/".join(str(item) for item in value)
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def load(path: Path) -> tuple[dict[str, Any], list[str]]:
    """Load architecture input safely."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read architecture input: {exc}"]
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        return {}, [f"input schema must be {SCHEMA}"]
    return value, []


def required_text(item: dict[str, Any], fields: tuple[str, ...], prefix: str) -> list[str]:
    """Validate required string fields."""
    return [f"{prefix}: {field} is required" for field in fields if not isinstance(item.get(field), str) or not item.get(field, "").strip()]


def traces(item: dict[str, Any], prefix: str) -> list[str]:
    """Validate a non-empty trace target list."""
    value = item.get("trace_targets")
    if not isinstance(value, list) or not value or not all(isinstance(ref, str) and ref.strip() for ref in value):
        return [f"{prefix}: trace_targets must be a non-empty string array"]
    return []


def validate(value: dict[str, Any], full_flow: bool) -> list[str]:
    """Validate architecture structure and strict design coverage."""
    errors: list[str] = []
    if not isinstance(value.get("context"), str) or not value.get("context", "").strip():
        errors.append("context is required")
    for name in COLLECTIONS:
        if not isinstance(value.get(name), list) or not all(isinstance(item, dict) for item in value.get(name, [])):
            errors.append(f"{name} must be an array of objects")
    if errors:
        return errors
    for name in ("constraints", "interfaces", "decisions", "risks"):
        ids: list[str] = []
        for index, item in enumerate(value[name], start=1):
            prefix = f"{name} {index}"
            errors.extend(traces(item, prefix))
            if "id" in item:
                ids.append(str(item["id"]))
        if len(ids) != len(set(ids)):
            errors.append(f"{name}: identifiers must be unique")
    for index, item in enumerate(value["constraints"], start=1):
        errors.extend(required_text(item, ("id", "statement"), f"constraints {index}"))
    for index, item in enumerate(value["components"], start=1):
        errors.extend(required_text(item, ("name", "responsibility"), f"components {index}"))
        if not isinstance(item.get("dependencies", []), list):
            errors.append(f"components {index}: dependencies must be an array")
    for index, item in enumerate(value["interfaces"], start=1):
        errors.extend(required_text(item, ("name", "from", "to", "contract"), f"interfaces {index}"))
    for index, item in enumerate(value["decisions"], start=1):
        prefix = f"decisions {index}"
        errors.extend(required_text(item, ("id", "statement", "rationale"), prefix))
        for field in ("alternatives", "consequences"):
            if not isinstance(item.get(field), list) or not item[field]:
                errors.append(f"{prefix}: {field} must be non-empty")
    for index, item in enumerate(value["risks"], start=1):
        errors.extend(required_text(item, ("id", "statement", "mitigation", "owner"), f"risks {index}"))
    for index, item in enumerate(value["validation"], start=1):
        prefix = f"validation {index}"
        errors.extend(required_text(item, ("check", "evidence"), prefix))
        if item.get("status") not in {"planned", "passed", "failed"}:
            errors.append(f"{prefix}: invalid status")
    if full_flow:
        for name in ("decisions", "risks", "validation"):
            if not value[name]:
                errors.append(f"full flow requires at least one {name} entry")
    return errors


def render_toon(root: Path, flow: str, value: dict[str, Any]) -> str:
    """Render compact architecture output."""
    lines = ["schema: ai-sdlc-architecture/v1", f"feature_root: {toon(root.as_posix())}", f"flow_mode: {flow}", f"context: {toon(value['context'])}"]
    columns = {
        "constraints": ("id", "statement", "trace_targets"),
        "components": ("name", "responsibility", "dependencies"),
        "interfaces": ("name", "from", "to", "contract", "trace_targets"),
        "decisions": ("id", "statement", "rationale", "alternatives", "consequences", "trace_targets"),
        "risks": ("id", "statement", "mitigation", "owner", "trace_targets"),
        "validation": ("check", "evidence", "status"),
    }
    for name, fields in columns.items():
        lines.extend(["", f"{name}[{len(value[name])}]{{{','.join(fields)}}}:"])
        lines.extend("  " + ",".join(toon(item.get(field, "")) for field in fields) for item in value[name])
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(root: Path, flow: str, value: dict[str, Any]) -> str:
    """Render detailed human architecture output."""
    trace_ids = sorted({ref for name in ("constraints", "interfaces", "decisions", "risks") for item in value[name] for ref in item["trace_targets"]})
    lines = ["---", "artifact_metadata:", '  schema: "ai-sdlc-architecture-metadata/v1"', f'  feature: "{toon(root.name)}"', '  artifact: "architecture.md"', f'  path: "{toon((root / "architecture.md").as_posix())}"', '  workspace: "implementation"', '  skill: "ai-sdlc-architecture"', f'  flow_mode: "{flow}"', f'  state_file: "{toon((root / "_ai_sdlc/state.toon").as_posix())}"', '  status: "review"', f'  updated_at: "{date.today().isoformat()}"', "  trace_ids:"]
    lines.extend(f'    - "{toon(ref)}"' for ref in trace_ids)
    lines.extend(["  metatags:", '    - "ai-sdlc"', '    - "architecture"', '    - "design"', '    - "traceable"', "---", "", "# Architecture", "", "## Context", "", value["context"]])
    for name in COLLECTIONS:
        lines.extend(["", f"## {name.replace('_', ' ').title()}"])
        if not value[name]:
            lines.extend(["", "- None."])
        for item in value[name]:
            lines.extend(["", "- " + "; ".join(f"{key}: {toon(field)}" for key, field in item.items())])
    return "\n".join(lines).rstrip() + "\n"


def atomic_write(path: Path, content: str) -> None:
    """Write one architecture output atomically."""
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
    """Validate and write architecture reports."""
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
        print("ERROR: architecture generation is read-only with respect to lifecycle state")
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
        atomic_write(root / "architecture.md", human)
        atomic_write(root / "_ai_sdlc/architecture.toon", machine)
    print(machine if args.format == "toon" else human, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
