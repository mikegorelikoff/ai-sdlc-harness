#!/usr/bin/env python3
"""Validate and render evidence-backed retrospective learning reports."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


SCHEMA = "ai-sdlc-retrospective-input/v1"
CATEGORIES = ("worked", "friction", "escape", "surprise")
STATUSES = ("proposed", "accepted", "rejected", "deferred")


def toon(value: object) -> str:
    """Escape one TOON scalar."""
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def load_input(path: Path) -> tuple[dict[str, Any], list[str]]:
    """Load a retrospective input without user-facing tracebacks."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read retrospective input: {exc}"]
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        return {}, [f"input schema must be {SCHEMA}"]
    if not isinstance(value.get("observations"), list) or not isinstance(value.get("proposals"), list):
        return {}, ["observations and proposals must be arrays"]
    return value, []


def safe_evidence(root: Path, evidence: object, prefix: str) -> list[str]:
    """Validate one exact feature-local evidence anchor."""
    if not isinstance(evidence, dict):
        return [f"{prefix}: evidence object is required"]
    path_value = evidence.get("path")
    if not isinstance(path_value, str) or not path_value.strip():
        return [f"{prefix}: evidence.path is required"]
    relative = Path(path_value)
    if relative.is_absolute() or ".." in relative.parts:
        return [f"{prefix}: evidence.path must be feature-relative"]
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return [f"{prefix}: evidence.path escapes feature root"]
    if not path.is_file():
        return [f"{prefix}: evidence.path does not exist"]
    line = evidence.get("line")
    if not isinstance(line, int) or line < 1:
        return [f"{prefix}: evidence.line must be a positive integer"]
    if line > len(path.read_text(encoding="utf-8", errors="replace").splitlines()):
        return [f"{prefix}: evidence.line is outside the file"]
    if not isinstance(evidence.get("detail"), str) or not evidence.get("detail", "").strip():
        return [f"{prefix}: evidence.detail is required"]
    return []


def validate(root: Path, value: dict[str, Any]) -> list[str]:
    """Validate observation/proposal separation and governance."""
    errors: list[str] = []
    observation_ids: set[str] = set()
    proposal_ids: set[str] = set()
    for position, item in enumerate(value["observations"], start=1):
        prefix = f"observation {position}"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            errors.append(f"{prefix}: id is required")
        elif item_id in observation_ids:
            errors.append(f"{prefix}: duplicate id {item_id}")
        else:
            observation_ids.add(item_id)
        if item.get("category") not in CATEGORIES:
            errors.append(f"{prefix}: category must be one of {', '.join(CATEGORIES)}")
        if not isinstance(item.get("statement"), str) or not item.get("statement", "").strip():
            errors.append(f"{prefix}: statement is required")
        errors.extend(safe_evidence(root, item.get("evidence"), prefix))
    for position, item in enumerate(value["proposals"], start=1):
        prefix = f"proposal {position}"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            errors.append(f"{prefix}: id is required")
        elif item_id in proposal_ids:
            errors.append(f"{prefix}: duplicate id {item_id}")
        else:
            proposal_ids.add(item_id)
        based_on = item.get("based_on")
        if not isinstance(based_on, list) or not based_on or not all(ref in observation_ids for ref in based_on):
            errors.append(f"{prefix}: based_on must contain known observation IDs")
        for field in ("target", "change", "owner", "next_action"):
            if not isinstance(item.get(field), str) or not item.get(field, "").strip():
                errors.append(f"{prefix}: {field} is required")
        status = item.get("status")
        if status not in STATUSES:
            errors.append(f"{prefix}: status must be one of {', '.join(STATUSES)}")
        if status == "accepted" and (not isinstance(item.get("decision_ref"), str) or not item.get("decision_ref", "").strip()):
            errors.append(f"{prefix}: accepted status requires decision_ref")
    return errors


def render_toon(root: Path, flow: str, value: dict[str, Any]) -> str:
    """Render compact machine output."""
    observations = value["observations"]
    proposals = value["proposals"]
    lines = ["schema: ai-sdlc-retrospective/v1", f"feature_root: {toon(root.as_posix())}", f"flow_mode: {flow}", "", f"observations[{len(observations)}]{{id,category,statement,evidence_path,evidence_line,evidence_detail}}:"]
    for item in observations:
        evidence = item["evidence"]
        lines.append("  " + ",".join(toon(v) for v in (item["id"], item["category"], item["statement"], evidence["path"], evidence["line"], evidence["detail"])))
    lines.extend(["", f"proposals[{len(proposals)}]{{id,based_on,target,change,owner,status,decision_ref,next_action}}:"])
    for item in proposals:
        lines.append("  " + ",".join(toon(v) for v in (item["id"], "/".join(item["based_on"]), item["target"], item["change"], item["owner"], item["status"], item.get("decision_ref", ""), item["next_action"])))
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(root: Path, flow: str, value: dict[str, Any]) -> str:
    """Render human output with repository artifact metadata."""
    observations = value["observations"]
    proposals = value["proposals"]
    decisions = sorted({item.get("decision_ref", "") for item in proposals if item.get("decision_ref")})
    statuses = Counter(item["status"] for item in proposals)
    workspace = "implementation" if root.parent.name == "specs" else "refinement" if root.parent.name == "specs-refiniment" else "unknown"
    lines = ["---", "artifact_metadata:", '  schema: "ai-sdlc-retrospective-metadata/v1"', f'  feature: "{toon(root.name)}"', '  artifact: "retrospective.md"', f'  path: "{toon((root / "retrospective.md").as_posix())}"', f'  workspace: "{workspace}"', '  skill: "ai-sdlc-retrospective"', f'  flow_mode: "{flow}"', '  status: "review"', f'  updated_at: "{date.today().isoformat()}"', "  trace_ids:"]
    lines.extend(f'    - "{toon(item)}"' for item in decisions)
    lines.extend(["  metatags:", '    - "ai-sdlc"', '    - "retrospective"', '    - "learning"'])
    lines.extend(f'    - "{status}"' for status in sorted(statuses))
    lines.extend(["---", "", "# Retrospective", "", f"- Feature root: `{root.as_posix()}`", f"- Flow mode: `{flow}`", f"- Observations: `{len(observations)}`", f"- Proposals: `{len(proposals)}`", "", "## Observations"])
    for item in observations:
        evidence = item["evidence"]
        lines.append(f"- `{item['id']}` `{item['category']}` — {item['statement']} Evidence: `{evidence['path']}:{evidence['line']}` — {evidence['detail']}")
    if not observations:
        lines.append("- None.")
    lines.extend(["", "## Improvement Proposals"])
    for item in proposals:
        decision = f"; decision `{item['decision_ref']}`" if item.get("decision_ref") else ""
        lines.append(f"- `{item['id']}` `{item['status']}` from {', '.join(f'`{ref}`' for ref in item['based_on'])}; target `{item['target']}`; owner `{item['owner']}`{decision}. Change: {item['change']} Next: {item['next_action']}")
    if not proposals:
        lines.append("- None.")
    return "\n".join(lines).rstrip() + "\n"


def atomic_write(path: Path, content: str) -> None:
    """Write one output atomically without touching proposal targets."""
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
    """Validate learning evidence and render governed proposals."""
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
        print("ERROR: retrospective finalization is read-only; it cannot change lifecycle state")
        return 1
    if not root.is_dir():
        print(f"ERROR: feature root does not exist: {root}")
        return 1
    if args.state_check and not (root / "_ai_sdlc/state.toon").is_file():
        print("ERROR: canonical state is missing")
        return 1
    value, errors = load_input(args.input)
    if not errors:
        errors.extend(validate(root, value))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    flow = "full" if args.full_flow else "quick" if args.quick_flow else "default"
    markdown = render_markdown(root, flow, value)
    machine = render_toon(root, flow, value)
    if args.write:
        atomic_write(root / "retrospective.md", markdown)
        atomic_write(root / "_ai_sdlc/retrospective.toon", machine)
    print(machine if args.format == "toon" else markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
