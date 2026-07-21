#!/usr/bin/env python3
"""Preview specification delta application, conflicts, impact, and gates."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

from spec_delta import analyze_delta_set, semantic_fingerprint

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import encode_toon
from ai_sdlc_safe_io import atomic_write_text, bounded_path


SCHEMA = "ai-sdlc-change-preview/v1"


def digest(text: str) -> str:
    """Hash UTF-8 text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normative_statement(operation: dict[str, Any]) -> str:
    """Extract the complete normative paragraph from a parsed block."""
    lines = operation["statement"].splitlines()
    excluded = ("ID:", "Reason:", "Migration:", "From:", "To:", "#### Scenario:", "- WHEN", "- THEN", "- **WHEN", "- **THEN")
    candidates = [line.strip() for line in lines if line.strip() and not line.strip().startswith(excluded)]
    return " ".join(line for line in candidates if re.search(r"\b(?:MUST|SHALL)\b", line))


def render_requirement(operation: dict[str, Any]) -> str:
    """Render normalized canonical Markdown for an added or modified requirement."""
    lines = [f"### Requirement: {operation['name']}", f"ID: {operation['requirement_id']}", "", normative_statement(operation)]
    for scenario in operation["scenarios"]:
        lines.extend(["", f"#### Scenario: {scenario['name']}", f"- WHEN {scenario['when']}", f"- THEN {scenario['then']}"])
    return "\n".join(lines).rstrip() + "\n"


def structured_blocks(lines: list[str], requirement_id: str) -> list[tuple[int, int]]:
    """Locate structured requirement blocks by an exact ID line."""
    starts = [index for index, line in enumerate(lines) if line.startswith("### Requirement:")]
    blocks: list[tuple[int, int]] = []
    for position, start in enumerate(starts):
        next_requirement = starts[position + 1] if position + 1 < len(starts) else len(lines)
        next_section = next((index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")), len(lines))
        end = min(next_requirement, next_section)
        if any(line.strip() == f"ID: {requirement_id}" for line in lines[start:end]):
            blocks.append((start, end))
    return blocks


def inline_blocks(lines: list[str], requirement_id: str) -> list[tuple[int, int]]:
    """Locate legacy list requirements and their indented continuation."""
    pattern = re.compile(rf"^\s*[-*]\s+{re.escape(requirement_id)}\s*:")
    blocks: list[tuple[int, int]] = []
    for start, line in enumerate(lines):
        if not pattern.search(line):
            continue
        end = start + 1
        while end < len(lines) and (not lines[end].strip() or lines[end].startswith((" ", "\t"))):
            end += 1
        blocks.append((start, end))
    return blocks


def apply_virtual(content: str, operations: list[dict[str, Any]], target: str) -> tuple[str, list[dict[str, str]]]:
    """Build a virtual after-state or return precise conflicts."""
    current = content
    conflicts: list[dict[str, str]] = []
    for operation in operations:
        lines = current.splitlines(keepends=False)
        requirement_id = operation["requirement_id"]
        structured = structured_blocks(lines, requirement_id)
        inline = inline_blocks(lines, requirement_id)
        locations = structured + inline
        if operation["operation"] == "ADDED":
            if locations:
                conflicts.append({"code": "target-id-exists", "target": target, "requirement_id": requirement_id, "detail": "ADDED target ID already has a canonical requirement block."})
                continue
            separator = "" if not current else "\n" if current.endswith("\n\n") else "\n\n"
            current = current + separator + render_requirement(operation)
            continue
        if len(locations) != 1:
            conflicts.append({"code": "ambiguous-canonical-block", "target": target, "requirement_id": requirement_id, "detail": f"Expected one canonical requirement block; found {len(locations)}."})
            continue
        start, end = locations[0]
        if operation["operation"] == "REMOVED":
            replacement: list[str] = []
        elif operation["operation"] == "RENAMED":
            if locations[0] in inline:
                conflicts.append({"code": "unsupported-inline-rename", "target": target, "requirement_id": requirement_id, "detail": "RENAMED requires a structured Requirement heading."})
                continue
            replacement = lines[start:end]
            replacement[0] = f"### Requirement: {operation['to']}"
        else:
            replacement = render_requirement(operation).rstrip("\n").splitlines()
        lines[start:end] = replacement
        current = "\n".join(lines).rstrip() + "\n"
    return current, conflicts


def concurrent_conflicts(repository: Path, change_id: str, operations: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Find other validated active deltas touching the same requirement."""
    keys = {(item["target"], item["requirement_id"]) for item in operations}
    conflicts: list[dict[str, str]] = []
    for path in sorted((repository / "changes").glob("*/_ai_sdlc/delta-set.json")):
        other_id = path.parents[1].name
        if other_id == change_id:
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if value.get("status") != "validated":
            continue
        items = value.get("operations", [])
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            key = (item.get("target"), item.get("requirement_id"))
            if key in keys:
                conflicts.append({"code": "concurrent-change-overlap", "target": str(key[0]), "requirement_id": str(key[1]), "detail": f"Also changed by active change {other_id}."})
    return conflicts


def stale_references(repository: Path, operations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Find exact downstream references made stale by behavior changes."""
    changed = [item for item in operations if item["operation"] != "ADDED"]
    findings: list[dict[str, Any]] = []
    roots = [repository / "specs", repository / "specs-refiniment"]
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            if path.is_symlink() or not path.resolve().is_relative_to(repository):
                continue
            relative = path.relative_to(repository).as_posix()
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            for operation in changed:
                if relative == operation["target"]:
                    continue
                identifier = operation["requirement_id"]
                pattern = re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(identifier)}(?![A-Za-z0-9_-])")
                for line_number, line in enumerate(lines, start=1):
                    if pattern.search(line):
                        findings.append({"requirement_id": identifier, "operation": operation["operation"], "path": relative, "line": line_number, "detail": line.strip()[:240], "action": "revalidate"})
                        break
    return findings


def discover_gates(operations: list[dict[str, Any]], targets: list[dict[str, Any]], stale: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Derive conservative explainable gates from preview evidence."""
    gates = {"delta-validation": "Semantic deltas must remain current.", "owner-approval": "Canonical mutation requires accountable approval."}
    if any(item["operation"] != "ADDED" for item in operations) or stale:
        gates["change-impact-review"] = "Existing behavior or downstream trace evidence changes."
    if len(targets) > 1:
        gates["cross-artifact-review"] = "The change spans multiple canonical targets."
    if any(not item["exists"] for item in targets):
        gates["new-artifact-ownership"] = "A new canonical target needs explicit ownership."
    sensitive = re.compile(r"(?:security|auth|policy|config|permission|secret)", re.IGNORECASE)
    if any(sensitive.search(item["target"]) for item in targets):
        gates["security-policy-review"] = "A target path indicates security or protected policy scope."
    return [{"gate": key, "reason": gates[key]} for key in sorted(gates)]


def build_preview(repository: Path, change_id: str) -> tuple[dict[str, Any], list[str]]:
    """Build one deterministic non-mutating apply preview."""
    delta, errors = analyze_delta_set(repository, change_id)
    if errors:
        return {}, errors
    operations = delta["operations"]
    targets: list[dict[str, Any]] = []
    conflicts = concurrent_conflicts(repository, change_id, operations)
    for target in sorted({item["target"] for item in operations}):
        path = repository / target
        exists = path.is_file()
        before = path.read_text(encoding="utf-8") if exists else ""
        target_operations = [item for item in operations if item["target"] == target]
        after, target_conflicts = apply_virtual(before, target_operations, target)
        conflicts.extend(target_conflicts)
        diff = "".join(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True), fromfile=f"a/{target}", tofile=f"b/{target}"))
        targets.append({"target": target, "exists": exists, "before_sha256": digest(before), "after_sha256": digest(after), "before_bytes": len(before.encode("utf-8")), "after_bytes": len(after.encode("utf-8")), "diff": diff})
    stale = stale_references(repository, operations)
    record: dict[str, Any] = {
        "schema": SCHEMA,
        "change_id": change_id,
        "status": "blocked" if conflicts else "ready",
        "delta_fingerprint": delta["contract_fingerprint"],
        "targets": targets,
        "conflicts": sorted(conflicts, key=lambda item: (item["target"], item["requirement_id"], item["code"])),
        "stale_references": stale,
        "reopen_actions": sorted({item["path"] for item in stale}),
        "required_gates": discover_gates(operations, targets, stale),
        "authority": {"canonical_mutation_allowed": False, "requires_policy_evaluation": True, "requires_approval": True},
    }
    record["preview_fingerprint"] = semantic_fingerprint(record)
    return record, []


def atomic_write(root: Path, path: Path, content: str) -> None:
    """Write one preview artifact atomically."""
    atomic_write_text(root, path, content)


def render_markdown(record: dict[str, Any]) -> str:
    """Render a reviewable preview report."""
    lines = ["# Change Apply Preview", "", f"- Change: `{record['change_id']}`", f"- Status: `{record['status']}`", f"- Fingerprint: `{record['preview_fingerprint']}`", "", "## Required Gates", ""]
    lines.extend(f"- `{item['gate']}`: {item['reason']}" for item in record["required_gates"])
    lines.extend(["", "## Conflicts", ""])
    lines.extend(["- None."] if not record["conflicts"] else [f"- `{item['code']}` `{item['target']}#{item['requirement_id']}`: {item['detail']}" for item in record["conflicts"]])
    lines.extend(["", "## Stale References", ""])
    lines.extend(["- None."] if not record["stale_references"] else [f"- `{item['requirement_id']}` -> `{item['path']}:{item['line']}` ({item['action']})" for item in record["stale_references"]])
    lines.extend(["", "## Target Diffs"])
    for target in record["targets"]:
        lines.extend(["", f"### `{target['target']}`", "", "```diff", target["diff"].rstrip(), "```"])
    return "\n".join(lines).rstrip() + "\n"


def render_toon(record: dict[str, Any]) -> str:
    """Render the complete preview projection as TOON."""
    return encode_toon(record)


def main() -> int:
    """Preview one validated change without canonical mutation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--change-id", required=True)
    parser.add_argument("--preview", action="store_true", required=True)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--format", choices=("markdown", "json", "toon"), default="toon")
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
    if args.begin_state or args.complete_state:
        print("ERROR: apply preview cannot mutate feature lifecycle state")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir():
        print(f"ERROR: repository does not exist: {repository}")
        return 1
    record, errors = build_preview(repository, args.change_id)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.write:
        try:
            workspace = bounded_path(repository, repository / "changes" / args.change_id)
            atomic_write(workspace, workspace / "_ai_sdlc/apply-preview.json", json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
            atomic_write(workspace, workspace / "_ai_sdlc/apply-preview.toon", encode_toon(record))
            atomic_write(workspace, workspace / "apply-preview.md", render_markdown(record))
        except ValueError as exc:
            print(f"ERROR: {exc}")
            return 1
    if args.format == "json":
        print(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False))
    elif args.format == "toon":
        print(render_toon(record), end="")
    else:
        print(render_markdown(record), end="")
    return 2 if record["status"] == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
