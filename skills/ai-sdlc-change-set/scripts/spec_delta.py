#!/usr/bin/env python3
"""Parse and validate semantic requirement deltas without canonical writes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

from change_set import validate_workspace

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import encode_toon
from ai_sdlc_safe_io import atomic_write_text, bounded_path


SCHEMA = "ai-sdlc-spec-delta/v1"
OPERATIONS = {"ADDED", "MODIFIED", "REMOVED", "RENAMED"}
OPERATION_HEADING = re.compile(r"^## (ADDED|MODIFIED|REMOVED|RENAMED) Requirements\s*$")
REQUIREMENT_HEADING = re.compile(r"^### Requirement:\s*(.+?)\s*$")
TARGET_LINE = re.compile(r"^Target:\s*`([^`]+)`\s*$")
ID_LINE = re.compile(r"^ID:\s*([A-Za-z][A-Za-z0-9_.-]*-[A-Za-z0-9_.-]+)\s*$")
FIELD_PATTERNS = {
    "reason": re.compile(r"^Reason:\s*(.+?)\s*$", re.MULTILINE),
    "migration": re.compile(r"^Migration:\s*(.+?)\s*$", re.MULTILINE),
    "from": re.compile(r"^From:\s*(.+?)\s*$", re.MULTILINE),
    "to": re.compile(r"^To:\s*(.+?)\s*$", re.MULTILINE),
}


def sha256_bytes(value: bytes) -> str:
    """Return a stable SHA-256 digest."""
    return hashlib.sha256(value).hexdigest()


def semantic_fingerprint(record: dict[str, Any]) -> str:
    """Hash a record without its fingerprint field."""
    payload = {key: value for key, value in record.items() if key != "contract_fingerprint"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256_bytes(encoded.encode("utf-8"))


def field(block: str, name: str) -> str:
    """Return one operation-specific field."""
    match = FIELD_PATTERNS[name].search(block)
    return match.group(1).strip() if match else ""


def scenarios(block_lines: list[str], base_line: int, prefix: str) -> tuple[list[dict[str, Any]], list[str]]:
    """Parse scenario headings and validate WHEN/THEN completeness."""
    found: list[dict[str, Any]] = []
    errors: list[str] = []
    positions = [index for index, line in enumerate(block_lines) if line.startswith("#### Scenario:")]
    for offset, start in enumerate(positions):
        end = positions[offset + 1] if offset + 1 < len(positions) else len(block_lines)
        name = block_lines[start].split(":", 1)[1].strip()
        content = "\n".join(block_lines[start + 1:end])
        when_match = re.search(r"(?im)^\s*[-*]\s*(?:\*\*)?WHEN(?:\*\*)?(?:\s|:)\s*(.+)", content)
        then_match = re.search(r"(?im)^\s*[-*]\s*(?:\*\*)?THEN(?:\*\*)?(?:\s|:)\s*(.+)", content)
        when = when_match.group(1).strip() if when_match else ""
        then = then_match.group(1).strip() if then_match else ""
        line_number = base_line + start
        if not name:
            errors.append(f"{prefix}:{line_number}: scenario name is required")
        if not when or not then:
            errors.append(f"{prefix}:{line_number}: scenario requires WHEN and THEN steps")
        found.append({"name": name, "source_line": line_number, "when": when, "then": then})
    return found, errors


def parse_delta(path: Path, workspace: Path) -> tuple[list[dict[str, Any]], dict[str, str], list[str]]:
    """Parse one Markdown delta into normalized operations."""
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [], {}, [f"{path.relative_to(workspace)}: delta must be UTF-8"]
    lines = text.splitlines()
    relative = path.relative_to(workspace).as_posix()
    target_matches = [(index + 1, match.group(1)) for index, line in enumerate(lines) if (match := TARGET_LINE.match(line))]
    errors: list[str] = []
    if len(target_matches) != 1:
        return [], {}, [f"{relative}: exactly one Target line is required"]
    target = target_matches[0][1]
    operations: list[dict[str, Any]] = []
    current_operation = ""
    index = 0
    while index < len(lines):
        operation_match = OPERATION_HEADING.match(lines[index])
        if operation_match:
            current_operation = operation_match.group(1)
            index += 1
            continue
        requirement_match = REQUIREMENT_HEADING.match(lines[index])
        if not requirement_match:
            index += 1
            continue
        start = index
        end = index + 1
        while end < len(lines) and not OPERATION_HEADING.match(lines[end]) and not REQUIREMENT_HEADING.match(lines[end]):
            end += 1
        block_lines = lines[start + 1:end]
        block = "\n".join(block_lines)
        prefix = f"{relative}:{start + 1}"
        if current_operation not in OPERATIONS:
            errors.append(f"{prefix}: requirement must follow an operation heading")
            index = end
            continue
        id_matches = [ID_LINE.match(line) for line in block_lines]
        requirement_ids = [match.group(1) for match in id_matches if match]
        if len(requirement_ids) != 1:
            errors.append(f"{prefix}: exactly one stable ID line is required")
            index = end
            continue
        parsed_scenarios, scenario_errors = scenarios(block_lines, start + 2, relative)
        errors.extend(scenario_errors)
        operation = {
            "operation": current_operation,
            "target": target,
            "requirement_id": requirement_ids[0],
            "name": requirement_match.group(1).strip(),
            "statement": block.strip(),
            "scenarios": parsed_scenarios,
            "reason": field(block, "reason"),
            "migration": field(block, "migration"),
            "from": field(block, "from"),
            "to": field(block, "to"),
            "source": relative,
            "source_line": start + 1,
            "source_hash": sha256_bytes(raw),
        }
        if current_operation in {"ADDED", "MODIFIED"}:
            if not re.search(r"\b(?:MUST|SHALL)\b", block):
                errors.append(f"{prefix}: {current_operation} requires a complete MUST or SHALL statement")
            if not parsed_scenarios:
                errors.append(f"{prefix}: {current_operation} requires at least one scenario")
        elif current_operation == "REMOVED":
            if not operation["reason"] or not operation["migration"]:
                errors.append(f"{prefix}: REMOVED requires Reason and Migration")
        elif current_operation == "RENAMED":
            if not operation["from"] or not operation["to"] or operation["from"] == operation["to"]:
                errors.append(f"{prefix}: RENAMED requires distinct From and To values")
        operations.append(operation)
        index = end
    if not operations:
        errors.append(f"{relative}: at least one requirement operation is required")
    return operations, {"path": relative, "sha256": sha256_bytes(raw)}, errors


def read_target(repository: Path, target: str) -> tuple[str | None, list[str]]:
    """Read one bounded canonical target without crossing repository scope."""
    path = repository / target
    if not path.exists():
        return None, []
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        return None, [f"{target}: cannot resolve canonical target: {exc}"]
    if not resolved.is_relative_to(repository) or not resolved.is_file():
        return None, [f"{target}: canonical target must be a repository file"]
    if resolved.stat().st_size > 2_000_000:
        return None, [f"{target}: canonical target exceeds the 2 MB validation limit"]
    try:
        return resolved.read_text(encoding="utf-8"), []
    except (OSError, UnicodeDecodeError) as exc:
        return None, [f"{target}: cannot read canonical target as UTF-8: {exc}"]


def validate_semantics(repository: Path, declared_targets: list[str], operations: list[dict[str, Any]]) -> list[str]:
    """Validate target declarations, stable IDs, and operation overlaps."""
    errors: list[str] = []
    seen: dict[tuple[str, str], str] = {}
    target_cache: dict[str, str | None] = {}
    for operation in operations:
        target = operation["target"]
        requirement_id = operation["requirement_id"]
        prefix = f"{operation['source']}:{operation['source_line']}"
        if target not in declared_targets:
            errors.append(f"{prefix}: target is not declared by the parent change set: {target}")
        key = (target, requirement_id)
        if key in seen:
            errors.append(f"{prefix}: overlapping operation for {target}#{requirement_id}; first seen at {seen[key]}")
        else:
            seen[key] = prefix
        if target not in target_cache:
            target_cache[target], target_errors = read_target(repository, target)
            errors.extend(target_errors)
        canonical = target_cache[target]
        present = bool(canonical is not None and re.search(rf"(?<![A-Za-z0-9_-]){re.escape(requirement_id)}(?![A-Za-z0-9_-])", canonical))
        if operation["operation"] == "ADDED" and present:
            errors.append(f"{prefix}: ADDED requirement already exists in {target}: {requirement_id}")
        if operation["operation"] != "ADDED" and not present:
            errors.append(f"{prefix}: {operation['operation']} requirement is missing from {target}: {requirement_id}")
    return errors


def build_projection(change_id: str, operations: list[dict[str, Any]], sources: list[dict[str, str]]) -> dict[str, Any]:
    """Build the deterministic delta-set projection."""
    ordered = sorted(operations, key=lambda item: (item["target"], item["requirement_id"], item["operation"], item["source"]))
    record: dict[str, Any] = {
        "schema": SCHEMA,
        "change_id": change_id,
        "status": "validated",
        "operations": ordered,
        "sources": sorted(sources, key=lambda item: item["path"]),
        "authority": {"canonical_mutation_allowed": False, "requires_preview": True, "requires_approval": True},
    }
    record["contract_fingerprint"] = semantic_fingerprint(record)
    return record


def atomic_write(root: Path, path: Path, content: str) -> None:
    """Replace one generated projection atomically."""
    atomic_write_text(root, path, content)


def render_toon(record: dict[str, Any]) -> str:
    """Render the complete delta projection as TOON."""
    return encode_toon(record)


def analyze_delta_set(repository: Path, change_id: str) -> tuple[dict[str, Any], list[str]]:
    """Rebuild one delta projection from authoritative Markdown."""
    workspace = repository / "changes" / change_id
    change_record, errors = validate_workspace(workspace, change_id)
    if errors:
        return {}, errors
    paths = sorted(path for path in (workspace / "deltas").glob("*.md") if path.name != "index.md")
    if not paths:
        return {}, ["no semantic delta Markdown files found"]
    operations: list[dict[str, Any]] = []
    sources: list[dict[str, str]] = []
    for path in paths:
        parsed, source, parse_errors = parse_delta(path, workspace)
        operations.extend(parsed)
        if source:
            sources.append(source)
        errors.extend(parse_errors)
    errors.extend(validate_semantics(repository, change_record["canonical_targets"], operations))
    return (build_projection(change_id, operations, sources) if not errors else {}), errors


def main() -> int:
    """Validate and optionally persist one semantic delta projection."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--change-id", required=True)
    parser.add_argument("--validate", action="store_true", required=True)
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
        print("ERROR: delta validation cannot mutate feature lifecycle state")
        return 1
    repository = args.repository.resolve()
    try:
        workspace = bounded_path(repository, repository / "changes" / args.change_id)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    record, errors = analyze_delta_set(repository, args.change_id)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.write:
        atomic_write(workspace, workspace / "_ai_sdlc/delta-set.json", json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        atomic_write(workspace, workspace / "_ai_sdlc/delta-set.toon", encode_toon(record))
    if args.format == "json":
        print(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False))
    elif args.format == "toon":
        print(render_toon(record), end="")
    else:
        print(f"Delta set: {args.change_id}")
        print(f"Operations: {len(record['operations'])}")
        print(f"Fingerprint: {record['contract_fingerprint']}")
        print("Validation: passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
