#!/usr/bin/env python3
"""Validate and render reusable evidence-backed quality-lens reports."""

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


SKILL_DIR = Path(__file__).resolve().parents[1]
REGISTRY_PATH = SKILL_DIR / "references" / "quality-lenses.json"
SEVERITIES = ("critical", "high", "medium", "low", "info")
STATUSES = ("open", "accepted", "mitigated", "rejected", "deferred")
ARTIFACT_KINDS = ("requirements", "design", "plan", "tasks", "tests", "change", "ux", "research", "release", "general")


def load_registry() -> dict[str, Any]:
    """Load the bundled versioned registry."""
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def lens_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index registry entries by stable identifier."""
    return {item["id"]: item for item in registry["lenses"]}


def toon(value: object) -> str:
    """Escape one value for the repository TOON subset."""
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def select_lenses(registry: dict[str, Any], requested: list[str], artifact_kind: str, full_flow: bool) -> tuple[list[str], list[str]]:
    """Resolve selected lenses and return semantic errors."""
    available = lens_map(registry)
    selected = list(dict.fromkeys(requested))
    if full_flow:
        selected = [item["id"] for item in registry["lenses"] if artifact_kind in item["applies_to"]]
    elif not selected:
        selected = list(registry["default_quick_lenses"])
    errors: list[str] = []
    for lens in selected:
        if lens not in available:
            errors.append(f"unknown lens: {lens}")
        elif artifact_kind not in available[lens]["applies_to"]:
            errors.append(f"lens {lens} does not apply to artifact kind {artifact_kind}")
    return selected, errors


def load_findings(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Load a findings JSON array without raising user-facing tracebacks."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [f"cannot read findings: {exc}"]
    if not isinstance(value, list):
        return [], ["findings root must be a JSON array"]
    if not all(isinstance(item, dict) for item in value):
        return [], ["every finding must be a JSON object"]
    return value, []


def validate_findings(findings: list[dict[str, Any]], selected: list[str], registry: dict[str, Any]) -> list[str]:
    """Validate the mandatory traceable finding contract."""
    errors: list[str] = []
    known = lens_map(registry)
    seen: set[str] = set()
    for position, finding in enumerate(findings, start=1):
        prefix = f"finding {position}"
        finding_id = finding.get("id")
        if not isinstance(finding_id, str) or not finding_id.strip():
            errors.append(f"{prefix}: id is required")
        elif finding_id in seen:
            errors.append(f"{prefix}: duplicate id {finding_id}")
        else:
            seen.add(finding_id)
        lens = finding.get("lens")
        if lens not in known:
            errors.append(f"{prefix}: lens is not registered")
        elif lens not in selected:
            errors.append(f"{prefix}: lens {lens} was not selected")
        evidence = finding.get("evidence")
        if not isinstance(evidence, dict):
            errors.append(f"{prefix}: evidence object is required")
        else:
            evidence_path = evidence.get("path")
            if not isinstance(evidence_path, str) or not evidence_path.strip():
                errors.append(f"{prefix}: evidence.path is required")
            elif Path(evidence_path).is_absolute() or ".." in Path(evidence_path).parts:
                errors.append(f"{prefix}: evidence.path must be repository-relative")
            if not isinstance(evidence.get("line"), int) or evidence.get("line", 0) < 1:
                errors.append(f"{prefix}: evidence.line must be a positive integer")
            if not isinstance(evidence.get("detail"), str) or not evidence.get("detail", "").strip():
                errors.append(f"{prefix}: evidence.detail is required")
        if finding.get("severity") not in SEVERITIES:
            errors.append(f"{prefix}: severity must be one of {', '.join(SEVERITIES)}")
        targets = finding.get("trace_targets")
        if not isinstance(targets, list) or not targets or not all(isinstance(item, str) and item.strip() for item in targets):
            errors.append(f"{prefix}: trace_targets must be a non-empty string list")
        elif len(targets) != len(set(targets)):
            errors.append(f"{prefix}: trace_targets must be unique")
        if not isinstance(finding.get("owner"), str) or not finding.get("owner", "").strip():
            errors.append(f"{prefix}: owner is required")
        if finding.get("resolution_status") not in STATUSES:
            errors.append(f"{prefix}: resolution_status must be one of {', '.join(STATUSES)}")
        if not isinstance(finding.get("next_action"), str) or not finding.get("next_action", "").strip():
            errors.append(f"{prefix}: next_action is required")
    return errors


def render_markdown(artifact: str, artifact_kind: str, feature: str, flow_mode: str, selected: list[str], findings: list[dict[str, Any]], registry: dict[str, Any]) -> str:
    """Render human-readable Markdown with repository metadata."""
    traces = sorted({target for item in findings for target in item["trace_targets"]})
    severities = Counter(item["severity"] for item in findings)
    statuses = Counter(item["resolution_status"] for item in findings)
    lines = [
        "---", "artifact_metadata:", '  schema: "ai-sdlc-quality-report-metadata/v1"',
        f'  feature: "{toon(feature)}"', f'  source_artifact: "{toon(artifact)}"',
        f'  artifact_kind: "{artifact_kind}"', f'  registry_version: "{registry["version"]}"',
        f'  flow_mode: "{flow_mode}"', f'  updated_at: "{date.today().isoformat()}"', "  trace_ids:",
    ]
    lines.extend(f'    - "{toon(item)}"' for item in traces)
    lines.extend(["  metatags:", '    - "ai-sdlc"', '    - "quality-lens"', '    - "evidence-backed"'])
    lines.extend(f'    - "{lens}"' for lens in selected)
    lines.extend(["---", "", "# Quality Lens Report", "", f"- Source artifact: `{artifact}`", f"- Artifact kind: `{artifact_kind}`", f"- Registry version: `{registry['version']}`", f"- Flow mode: `{flow_mode}`", f"- Selected lenses: {', '.join(f'`{item}`' for item in selected)}", f"- Findings: `{len(findings)}`", "", "## Summary", "", "| Dimension | Value | Count |", "| --- | --- | ---: |"])
    for severity in SEVERITIES:
        lines.append(f"| Severity | {severity} | {severities[severity]} |")
    for status in STATUSES:
        lines.append(f"| Status | {status} | {statuses[status]} |")
    lines.extend(["", "## Findings"])
    if not findings:
        lines.extend(["", "No evidence-backed findings were identified by the selected lenses."])
    for item in findings:
        evidence = item["evidence"]
        lines.extend(["", f"### {item['id']} — {item['lens']}", "", f"- Evidence: `{evidence['path']}:{evidence['line']}` — {evidence['detail']}", f"- Severity: `{item['severity']}`", f"- Trace targets: {', '.join(f'`{target}`' for target in item['trace_targets'])}", f"- Owner: `{item['owner']}`", f"- Resolution status: `{item['resolution_status']}`", f"- Next action: {item['next_action']}"])
    return "\n".join(lines).rstrip() + "\n"


def render_toon(artifact: str, artifact_kind: str, feature: str, flow_mode: str, selected: list[str], findings: list[dict[str, Any]], registry: dict[str, Any]) -> str:
    """Render compact machine-readable TOON."""
    severities = Counter(item["severity"] for item in findings)
    statuses = Counter(item["resolution_status"] for item in findings)
    lines = ["schema: ai-sdlc-quality-report/v1", f"registry_version: {registry['version']}", f"feature: {toon(feature)}", f"artifact: {toon(artifact)}", f"artifact_kind: {artifact_kind}", f"flow_mode: {flow_mode}", "", f"selected_lenses[{len(selected)}]{{id}}:"]
    lines.extend(f"  {item}" for item in selected)
    lines.extend(["", f"summary[{len(SEVERITIES) + len(STATUSES)}]{{dimension,value,count}}:"])
    lines.extend(f"  severity,{value},{severities[value]}" for value in SEVERITIES)
    lines.extend(f"  status,{value},{statuses[value]}" for value in STATUSES)
    lines.extend(["", f"findings[{len(findings)}]{{id,lens,evidence_path,evidence_line,evidence_detail,severity,trace_targets,owner,resolution_status,next_action}}:"])
    for item in findings:
        evidence = item["evidence"]
        values = (item["id"], item["lens"], evidence["path"], evidence["line"], evidence["detail"], item["severity"], "/".join(item["trace_targets"]), item["owner"], item["resolution_status"], item["next_action"])
        lines.append("  " + ",".join(toon(value) for value in values))
    return "\n".join(lines).rstrip() + "\n"


def list_lenses(registry: dict[str, Any], output_format: str) -> str:
    """Render the registry for discovery."""
    if output_format == "toon":
        lines = [f"schema: {registry['schema']}", f"version: {registry['version']}", "", f"lenses[{len(registry['lenses'])}]{{id,name,applies_to,prompt}}:"]
        lines.extend("  " + ",".join((item["id"], toon(item["name"]), "/".join(item["applies_to"]), toon(item["prompt"]))) for item in registry["lenses"])
        return "\n".join(lines) + "\n"
    lines = ["# Quality Lens Registry", "", f"Version: `{registry['version']}`", ""]
    lines.extend(f"- `{item['id']}` — {item['name']}: {item['prompt']}" for item in registry["lenses"])
    return "\n".join(lines) + "\n"


def atomic_write(path: Path, content: str) -> None:
    """Write one report atomically."""
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
    """Parse arguments, validate findings, and emit a canonical report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--artifact-kind", choices=ARTIFACT_KINDS, default="general")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--findings", type=Path)
    parser.add_argument("--lens", action="append", default=[])
    parser.add_argument("--list-lenses", action="store_true")
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--format", choices=("markdown", "toon"), default="markdown")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    args = parser.parse_args()

    registry = load_registry()
    if args.begin_state or args.complete_state:
        print("ERROR: quality report finalization is read-only; lifecycle transitions belong to the owning workflow")
        return 1
    if args.list_lenses:
        print(list_lenses(registry, args.format), end="")
        return 0
    if not args.artifact or not args.findings:
        print("ERROR: --artifact and --findings are required unless --list-lenses is used")
        return 1
    if not args.artifact.is_file():
        print(f"ERROR: artifact does not exist: {args.artifact}")
        return 1
    selected, errors = select_lenses(registry, args.lens, args.artifact_kind, args.full_flow)
    findings, load_errors = load_findings(args.findings)
    errors.extend(load_errors)
    if not load_errors:
        errors.extend(validate_findings(findings, selected, registry))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    flow_mode = "full" if args.full_flow else "quick" if args.quick_flow else "default"
    artifact = args.artifact.as_posix()
    markdown = render_markdown(artifact, args.artifact_kind, args.feature, flow_mode, selected, findings, registry)
    machine = render_toon(artifact, args.artifact_kind, args.feature, flow_mode, selected, findings, registry)
    if args.write:
        output_root = args.output_root or args.artifact.parent
        atomic_write(output_root / "quality-lens-report.md", markdown)
        atomic_write(output_root / "_ai_sdlc" / "quality-lens-report.toon", machine)
    print(machine if args.format == "toon" else markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
