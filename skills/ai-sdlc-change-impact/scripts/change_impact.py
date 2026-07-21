#!/usr/bin/env python3
"""Trace changed references to stale artifacts and safe recovery actions."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


SKILLS_DIR = Path(__file__).resolve().parents[2]
_SHARED = SKILLS_DIR / "_shared"
if not _SHARED.is_dir():
    _SHARED = SKILLS_DIR / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))

from ai_sdlc_state_machine import COMPLETE_STATUSES, STAGES, STAGE_BY_SKILL, from_toon  # noqa: E402


SCHEMA = "ai-sdlc-change-set/v1"
REPORT_MD = "change-impact.md"
REPORT_TOON = "_ai_sdlc/change-impact.toon"
SKILL_PATTERN = re.compile(r'^\s+skill:\s+["\']?([^"\']+)["\']?\s*$')


@dataclass(frozen=True)
class Impact:
    """One changed reference occurrence in a downstream artifact."""

    change_id: str
    changed_ref: str
    artifact: str
    line: int
    detail: str
    skill: str
    stage: str
    stage_status: str


def toon(value: object) -> str:
    """Escape one scalar for the repository TOON subset."""
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def load_change_set(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Load and structurally validate a change set."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [f"cannot read change set: {exc}"]
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        return [], [f"change set schema must be {SCHEMA}"]
    changes = value.get("changes")
    if not isinstance(changes, list) or not changes:
        return [], ["change set requires a non-empty changes array"]
    if not all(isinstance(item, dict) for item in changes):
        return [], ["every change must be an object"]
    return changes, []


def safe_relative_path(root: Path, value: object) -> Path | None:
    """Resolve a path only when it stays beneath the feature root."""
    if not isinstance(value, str) or not value.strip():
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def validate_changes(root: Path, changes: list[dict[str, Any]]) -> list[str]:
    """Validate stable IDs and exact changed-source evidence."""
    errors: list[str] = []
    seen: set[str] = set()
    for position, change in enumerate(changes, start=1):
        prefix = f"change {position}"
        change_id = change.get("id")
        if not isinstance(change_id, str) or not change_id.strip():
            errors.append(f"{prefix}: id is required")
        elif change_id in seen:
            errors.append(f"{prefix}: duplicate id {change_id}")
        else:
            seen.add(change_id)
        changed_ref = change.get("changed_ref")
        if not isinstance(changed_ref, str) or not changed_ref.strip():
            errors.append(f"{prefix}: changed_ref is required")
        source = change.get("source")
        if not isinstance(source, dict):
            errors.append(f"{prefix}: source object is required")
            continue
        source_path = safe_relative_path(root, source.get("path"))
        if source_path is None or not source_path.is_file():
            errors.append(f"{prefix}: source.path must identify a feature file")
            continue
        line_number = source.get("line")
        if not isinstance(line_number, int) or line_number < 1:
            errors.append(f"{prefix}: source.line must be a positive integer")
        else:
            lines = source_path.read_text(encoding="utf-8", errors="replace").splitlines()
            if line_number > len(lines):
                errors.append(f"{prefix}: source.line is outside the source file")
            elif isinstance(changed_ref, str) and not re.search(rf"(?<![A-Za-z0-9_-]){re.escape(changed_ref)}(?![A-Za-z0-9_-])", lines[line_number - 1]):
                errors.append(f"{prefix}: source evidence line does not contain changed_ref {changed_ref}")
        if not isinstance(source.get("detail"), str) or not source.get("detail", "").strip():
            errors.append(f"{prefix}: source.detail is required")
    return errors


def artifact_skill(text: str, path: Path) -> str:
    """Read artifact owner skill from metadata with SDD filename fallback."""
    for line in text.splitlines()[:80]:
        match = SKILL_PATTERN.match(line)
        if match:
            return match.group(1).strip()
    if path.name in {"requirements.md", "design.md", "tasks.md", "test-cases.md", "qa.md", "plan.md"}:
        return "ai-sdlc-sdd"
    return "unknown"


def load_state(root: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    """Return stage rows indexed by ID and state blockers."""
    path = root / "_ai_sdlc" / "state.toon"
    if not path.is_file():
        return {}, [f"canonical state missing: {path.as_posix()}"]
    try:
        state = from_toon(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return {}, [f"cannot read state: {exc}"]
    rows = {str(row.get("id")): row for row in state.get("stages", []) if isinstance(row, dict)}
    return rows, []


def scan_impacts(root: Path, changes: list[dict[str, Any]], state_rows: dict[str, dict[str, str]]) -> list[Impact]:
    """Find exact downstream trace occurrences and their owning stages."""
    impacts: list[Impact] = []
    excluded = {REPORT_MD, REPORT_TOON}
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root).as_posix()
        if relative in excluded or any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        skill = artifact_skill(text, path)
        stage_def = STAGE_BY_SKILL.get(skill)
        stage = stage_def.stage_id if stage_def else "unknown"
        status = state_rows.get(stage, {}).get("status", "unknown")
        for change in changes:
            source_path = str(change["source"]["path"])
            if relative == Path(source_path).as_posix():
                continue
            changed_ref = str(change["changed_ref"])
            pattern = re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(changed_ref)}(?![A-Za-z0-9_-])")
            for line_number, line in enumerate(lines, start=1):
                if pattern.search(line):
                    impacts.append(Impact(str(change["id"]), changed_ref, relative, line_number, line.strip(), skill, stage, status))
                    break
    return impacts


def action_for_status(status: str) -> str:
    """Choose the safe non-mutating recovery proposal."""
    if status in COMPLETE_STATUSES:
        return "reopen"
    if status == "in_progress":
        return "revalidate-active"
    if status == "not_started":
        return "validate-before-start"
    return "manual-route"


def stage_order(stage: str) -> int:
    """Return canonical lifecycle order with unknown stages last."""
    for index, item in enumerate(STAGES):
        if item.stage_id == stage:
            return index
    return len(STAGES)


def grouped_actions(impacts: list[Impact]) -> list[dict[str, str]]:
    """Collapse impacts into ordered stage/change recovery actions."""
    groups: dict[tuple[str, str], list[Impact]] = defaultdict(list)
    for impact in impacts:
        groups[(impact.stage, impact.changed_ref)].append(impact)
    actions: list[dict[str, str]] = []
    for (stage, changed_ref), rows in sorted(groups.items(), key=lambda item: (stage_order(item[0][0]), item[0][1])):
        first = rows[0]
        artifacts = "/".join(sorted({row.artifact for row in rows}))
        actions.append({"stage": stage, "skill": first.skill, "status": first.stage_status, "action": action_for_status(first.stage_status), "changed_ref": changed_ref, "reason": f"{len(rows)} downstream artifact(s) retain trace {changed_ref}", "evidence_path": first.artifact, "evidence_line": str(first.line), "expected_artifact": artifacts})
    return actions


def render_toon(root: Path, flow: str, changes: list[dict[str, Any]], impacts: list[Impact], actions: list[dict[str, str]], blockers: list[str]) -> str:
    """Render compact machine impact output."""
    lines = ["schema: ai-sdlc-change-impact/v1", f"feature_root: {toon(root.as_posix())}", f"flow_mode: {flow}", "", f"changes[{len(changes)}]{{id,changed_ref,source_path,source_line,detail}}:"]
    for item in changes:
        source = item["source"]
        lines.append("  " + ",".join(toon(value) for value in (item["id"], item["changed_ref"], source["path"], source["line"], source["detail"])))
    lines.extend(["", f"affected_artifacts[{len(impacts)}]{{change_id,changed_ref,artifact,line,evidence,skill,stage,stage_status}}:"])
    for item in impacts:
        lines.append("  " + ",".join(toon(value) for value in (item.change_id, item.changed_ref, item.artifact, item.line, item.detail, item.skill, item.stage, item.stage_status)))
    lines.extend(["", f"reopen_actions[{len(actions)}]{{stage,skill,stage_status,action,changed_ref,reason,evidence_path,evidence_line,expected_artifact}}:"])
    for item in actions:
        lines.append("  " + ",".join(toon(item[key]) for key in ("stage", "skill", "status", "action", "changed_ref", "reason", "evidence_path", "evidence_line", "expected_artifact")))
    lines.extend(["", f"blockers[{len(blockers)}]{{message}}:"])
    lines.extend(f"  {toon(item)}" for item in blockers)
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(root: Path, flow: str, changes: list[dict[str, Any]], impacts: list[Impact], actions: list[dict[str, str]], blockers: list[str]) -> str:
    """Render human-readable impact output with artifact metadata."""
    refs = sorted({str(item["changed_ref"]) for item in changes})
    stages = sorted({item["stage"] for item in actions}, key=stage_order)
    workspace = "implementation" if root.parent.name == "specs" else "refinement" if root.parent.name == "specs-refiniment" else "unknown"
    lines = ["---", "artifact_metadata:", '  schema: "ai-sdlc-change-impact-metadata/v1"', f'  feature: "{toon(root.name)}"', '  artifact: "change-impact.md"', f'  path: "{toon((root / REPORT_MD).as_posix())}"', f'  workspace: "{workspace}"', '  skill: "ai-sdlc-change-impact"', f'  flow_mode: "{flow}"', f'  state_file: "{toon((root / "_ai_sdlc/state.toon").as_posix())}"', '  status: "review"', f'  updated_at: "{date.today().isoformat()}"', "  trace_ids:"]
    lines.extend(f'    - "{toon(item)}"' for item in refs)
    lines.extend(["  metatags:", '    - "ai-sdlc"', '    - "change-impact"', '    - "recovery"'])
    lines.extend(f'    - "{toon(item)}"' for item in stages)
    lines.extend(["---", "", "# Change Impact", "", f"- Feature root: `{root.as_posix()}`", f"- Flow mode: `{flow}`", f"- Changed references: {', '.join(f'`{item}`' for item in refs)}", f"- Affected artifacts: `{len(impacts)}`", f"- Affected stages: `{len(stages)}`", "", "## Blockers"])
    lines.extend(f"- {item}" for item in blockers)
    if not blockers:
        lines.append("- None.")
    lines.extend(["", "## Affected Artifacts"])
    if not impacts:
        lines.append("- No downstream exact trace occurrences found.")
    for item in impacts:
        lines.append(f"- `{item.artifact}:{item.line}` — `{item.changed_ref}`; owner `{item.skill}`; stage `{item.stage}` (`{item.stage_status}`); evidence: {item.detail}")
    lines.extend(["", "## Recovery Actions"])
    if not actions:
        lines.append("- Run a targeted trace review; no evidence-backed lifecycle reopen is currently justified.")
    for item in actions:
        lines.append(f"- `{item['action']}` stage `{item['stage']}` via `{item['skill']}` because {item['reason']}; evidence `{item['evidence_path']}:{item['evidence_line']}`; expected artifact(s): `{item['expected_artifact']}`.")
    return "\n".join(lines).rstrip() + "\n"


def atomic_write(path: Path, content: str) -> None:
    """Write one output atomically."""
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
    """Validate changes, scan impacts, and render recovery proposals."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feature_root", type=Path)
    parser.add_argument("--changes", type=Path, required=True)
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
        print("ERROR: change-impact analysis is read-only; owning workflows authorize lifecycle changes")
        return 1
    if not root.is_dir():
        print(f"ERROR: feature root does not exist: {root}")
        return 1
    changes, errors = load_change_set(args.changes)
    if not errors:
        errors.extend(validate_changes(root, changes))
    state_rows, state_blockers = load_state(root)
    if args.state_check and state_blockers:
        errors.extend(state_blockers)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    impacts = scan_impacts(root, changes, state_rows)
    actions = grouped_actions(impacts)
    blockers = list(state_blockers)
    unknown = sorted({item.artifact for item in impacts if item.stage == "unknown"})
    if unknown:
        blockers.append("unmapped artifact owner: " + ", ".join(unknown))
    if args.full_flow and blockers:
        for blocker in blockers:
            print(f"ERROR: {blocker}")
        return 1
    flow = "full" if args.full_flow else "quick" if args.quick_flow else "default"
    markdown = render_markdown(root, flow, changes, impacts, actions, blockers)
    machine = render_toon(root, flow, changes, impacts, actions, blockers)
    if args.write:
        atomic_write(root / REPORT_MD, markdown)
        atomic_write(root / REPORT_TOON, machine)
    print(machine if args.format == "toon" else markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
