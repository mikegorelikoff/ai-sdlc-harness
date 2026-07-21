#!/usr/bin/env python3
"""Build a deterministic dependency-aware evidence freshness ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from delivery_graph import build_graph, digest, resolve

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import encode_toon


SOURCE_SCHEMA = "ai-sdlc-evidence-source/v1"
LEDGER_SCHEMA = "ai-sdlc-evidence-ledger/v1"
KINDS = {"test", "validation", "approval", "review", "research", "release"}


def atomic_write(path: Path, content: str) -> None:
    """Atomically replace one generated ledger output."""
    if any(component.is_symlink() for component in (path, *list(path.parents)[:4])):
        raise SystemExit(f"ERROR: output path contains symlink component: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def file_hash(path: Path) -> str | None:
    """Hash file bytes or return none when evidence is absent."""
    if not path.is_file() or path.is_symlink():
        return None
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            value.update(chunk)
    return value.hexdigest()


def safe_path(repository: Path, value: Any) -> tuple[Path | None, str | None]:
    """Resolve a repository-relative evidence path without boundary escape."""
    if not isinstance(value, str) or not value or "\\" in value:
        return None, "path must be a non-empty repository-relative POSIX path"
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or value.startswith("_ai_sdlc/evidence-ledger"):
        return None, f"unsafe evidence path: {value}"
    path = repository.joinpath(*pure.parts)
    try:
        path.resolve(strict=False).relative_to(repository)
    except ValueError:
        return None, f"evidence path escapes repository: {value}"
    return path, None


def iso_timestamp(value: Any, field: str) -> str | None:
    """Validate one timezone-aware ISO timestamp."""
    if not isinstance(value, str):
        return f"{field} must be an ISO timestamp"
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return f"{field} must be an ISO timestamp"
    if parsed.tzinfo is None:
        return f"{field} must include a timezone"
    return None


def validate_source(repository: Path, path: Path, value: Any) -> list[str]:
    """Validate the strict source contract before reading evidence files."""
    prefix = path.relative_to(repository).as_posix()
    errors: list[str] = []
    required = {"schema", "id", "kind", "subjects", "producer", "captured_at", "artifact", "dependencies", "depends_on"}
    optional = {"expires_at"}
    if not isinstance(value, dict):
        return [f"{prefix}: manifest must be a JSON object"]
    if not required.issubset(value) or set(value) - required - optional:
        errors.append(f"{prefix}: fields must match {SOURCE_SCHEMA}")
    if value.get("schema") != SOURCE_SCHEMA:
        errors.append(f"{prefix}: schema must be {SOURCE_SCHEMA}")
    if not isinstance(value.get("id"), str) or not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", value["id"]):
        errors.append(f"{prefix}: id must use lowercase letters, digits, dots, or hyphens")
    if value.get("kind") not in KINDS:
        errors.append(f"{prefix}: unsupported evidence kind")
    for field in ("subjects", "depends_on"):
        items = value.get(field)
        if not isinstance(items, list) or (field == "subjects" and not items) or not all(isinstance(item, str) and item for item in items) or len(items) != len(set(items)):
            errors.append(f"{prefix}: {field} must be a unique string array")
    if not isinstance(value.get("producer"), str) or not value["producer"].strip():
        errors.append(f"{prefix}: producer is required")
    timestamp_error = iso_timestamp(value.get("captured_at"), "captured_at")
    if timestamp_error:
        errors.append(f"{prefix}: {timestamp_error}")
    if "expires_at" in value:
        timestamp_error = iso_timestamp(value["expires_at"], "expires_at")
        if timestamp_error:
            errors.append(f"{prefix}: {timestamp_error}")
        elif not timestamp_error and not iso_timestamp(value.get("captured_at"), "captured_at"):
            captured = datetime.fromisoformat(value["captured_at"].replace("Z", "+00:00"))
            expires = datetime.fromisoformat(value["expires_at"].replace("Z", "+00:00"))
            if expires <= captured:
                errors.append(f"{prefix}: expires_at must be after captured_at")
    identities = [value.get("artifact"), *(value.get("dependencies") if isinstance(value.get("dependencies"), list) else [])]
    for identity in identities:
        if not isinstance(identity, dict) or set(identity) != {"path", "sha256"}:
            errors.append(f"{prefix}: file identity must contain path and sha256")
            continue
        _, path_error = safe_path(repository, identity.get("path"))
        if path_error:
            errors.append(f"{prefix}: {path_error}")
        if not isinstance(identity.get("sha256"), str) or len(identity["sha256"]) != 64 or any(char not in "0123456789abcdef" for char in identity["sha256"]):
            errors.append(f"{prefix}: sha256 must be 64 lowercase hexadecimal characters")
    return errors


def manifests(repository: Path) -> list[Path]:
    """Discover evidence source manifests in bounded evidence directories."""
    found: set[Path] = set()
    for pattern in ("evidence/**/*.evidence.json", "changes/**/evidence/*.evidence.json"):
        found.update(path for path in repository.glob(pattern) if path.is_file() and not path.is_symlink())
    return sorted(found)


def cycle_errors(records: dict[str, dict[str, Any]]) -> list[str]:
    """Detect evidence dependency cycles deterministically."""
    visiting: set[str] = set()
    visited: set[str] = set()
    errors: list[str] = []

    def visit(record_id: str, trail: list[str]) -> None:
        if record_id in visiting:
            start = trail.index(record_id)
            errors.append("evidence dependency cycle: " + " -> ".join(trail[start:] + [record_id]))
            return
        if record_id in visited:
            return
        visiting.add(record_id)
        for dependency in sorted(records[record_id]["depends_on"]):
            if dependency in records:
                visit(dependency, trail + [record_id])
        visiting.remove(record_id)
        visited.add(record_id)

    for record_id in sorted(records):
        visit(record_id, [])
    return sorted(set(errors))


def build_ledger(repository: Path, as_of: date) -> tuple[dict[str, Any], list[str]]:
    """Recalculate evidence state, propagate freshness, and compute coverage."""
    graph = build_graph(repository)
    records: dict[str, dict[str, Any]] = {}
    source_hashes: list[tuple[str, str]] = []
    errors: list[str] = []
    for path in manifests(repository):
        relative = path.relative_to(repository).as_posix()
        raw = path.read_text(encoding="utf-8", errors="replace")
        source_hashes.append((relative, digest(raw)))
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        source_errors = validate_source(repository, path, value)
        if source_errors:
            errors.extend(source_errors)
            continue
        if value["id"] in records:
            errors.append(f"duplicate evidence id: {value['id']}")
            continue
        resolved_subjects: list[str] = []
        for subject in value["subjects"]:
            node_id, subject_errors = resolve(graph, subject)
            errors.extend(f"{relative}: {error}" for error in subject_errors)
            if node_id:
                node = next(item for item in graph["nodes"] if item["id"] == node_id)
                if node["kind"] == "artifact":
                    errors.append(f"{relative}: evidence subject must be a lifecycle node, not an artifact")
                else:
                    resolved_subjects.append(node_id)
        current_files: list[dict[str, Any]] = []
        reasons: list[str] = []
        identities = [("artifact", value["artifact"]), *(("dependency", item) for item in value["dependencies"])]
        for role, identity in identities:
            file_path, _ = safe_path(repository, identity["path"])
            current = file_hash(file_path) if file_path else None
            current_files.append({"role": role, "path": identity["path"], "captured_sha256": identity["sha256"], "current_sha256": current or ""})
            if current is None:
                reasons.append(f"{role}-missing:{identity['path']}")
            elif current != identity["sha256"]:
                reasons.append(f"{role}-changed:{identity['path']}")
        status = "missing" if any("-missing:" in reason for reason in reasons) else "stale" if reasons else "fresh"
        if status == "fresh" and value.get("expires_at"):
            expires = datetime.fromisoformat(value["expires_at"].replace("Z", "+00:00")).astimezone(timezone.utc).date()
            if expires < as_of:
                status = "expired"
                reasons.append(f"expired:{value['expires_at']}")
        record = {
            "schema": "ai-sdlc-evidence-record/v1",
            "id": value["id"],
            "kind": value["kind"],
            "subjects": sorted(resolved_subjects),
            "producer": value["producer"],
            "captured_at": value["captured_at"],
            "expires_at": value.get("expires_at", ""),
            "source_manifest": relative,
            "files": sorted(current_files, key=lambda item: (item["role"], item["path"])),
            "depends_on": sorted(value["depends_on"]),
            "status": status,
            "reason_codes": sorted(reasons),
            "upstream": [],
        }
        records[value["id"]] = record
    for record in records.values():
        for dependency in record["depends_on"]:
            if dependency not in records:
                errors.append(f"{record['source_manifest']}: unknown evidence dependency {dependency}")
    errors.extend(cycle_errors(records))
    if errors:
        return {}, sorted(set(errors))
    changed = True
    while changed:
        changed = False
        for record in records.values():
            upstream = [{"id": dependency, "status": records[dependency]["status"]} for dependency in record["depends_on"]]
            record["upstream"] = upstream
            not_fresh = [item["id"] for item in upstream if item["status"] != "fresh"]
            if not_fresh and record["status"] == "fresh":
                record["status"] = "stale"
                record["reason_codes"] = sorted(set(record["reason_codes"] + [f"upstream-not-fresh:{item}" for item in not_fresh]))
                changed = True
    for record in records.values():
        record["fingerprint"] = digest(record)
    record_list = sorted(records.values(), key=lambda item: item["id"])
    requirements = sorted(node["id"] for node in graph["nodes"] if node["kind"] == "requirement")
    fresh_subjects = {subject for record in record_list if record["status"] == "fresh" for subject in record["subjects"]}
    covered = sorted(set(requirements) & fresh_subjects)
    stale_paths = [
        {"evidence_id": record["id"], "status": record["status"], "subjects": record["subjects"], "reasons": record["reason_codes"], "upstream": record["upstream"]}
        for record in record_list
        if record["status"] != "fresh"
    ]
    coverage = {"requirements": len(requirements), "requirements_with_fresh_evidence": len(covered), "covered": covered, "uncovered": sorted(set(requirements) - set(covered)), "evidence_records": len(record_list), "fresh_records": sum(record["status"] == "fresh" for record in record_list)}
    ledger: dict[str, Any] = {"schema": LEDGER_SCHEMA, "as_of": as_of.isoformat(), "graph_fingerprint": graph["fingerprint"], "source_fingerprint": digest(source_hashes), "records": record_list, "coverage": coverage, "stale_paths": stale_paths}
    ledger["fingerprint"] = digest(ledger)
    return ledger, []


def markdown(ledger: dict[str, Any]) -> str:
    """Render a deterministic human ledger summary."""
    lines = ["# Evidence Ledger", "", f"As of: `{ledger['as_of']}`", f"Fingerprint: `{ledger['fingerprint']}`", "", "## Coverage", ""]
    for key in ("requirements", "requirements_with_fresh_evidence", "evidence_records", "fresh_records"):
        lines.append(f"- {key}: {ledger['coverage'][key]}")
    lines.extend(["", "## Evidence", "", "| ID | Kind | Status | Subjects |", "| --- | --- | --- | --- |"])
    for record in ledger["records"]:
        lines.append(f"| `{record['id']}` | {record['kind']} | {record['status']} | {', '.join(record['subjects'])} |")
    if not ledger["records"]:
        lines.append("| none | — | — | — |")
    return "\n".join(lines) + "\n"


def main() -> int:
    """Index or query evidence freshness."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--index", action="store_true")
    actions.add_argument("--coverage", action="store_true")
    actions.add_argument("--stale", action="store_true")
    parser.add_argument("--as-of", default=date.today().isoformat())
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
        print("ERROR: evidence indexing cannot mutate feature lifecycle state")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir():
        print(f"ERROR: repository does not exist: {repository}")
        return 1
    try:
        as_of = date.fromisoformat(args.as_of)
    except ValueError:
        print("ERROR: --as-of must use YYYY-MM-DD")
        return 1
    ledger, errors = build_ledger(repository, as_of)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.write:
        atomic_write(repository / "_ai_sdlc/evidence-ledger.json", json.dumps(ledger, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        atomic_write(repository / "_ai_sdlc/evidence-ledger.toon", encode_toon(ledger))
        atomic_write(repository / "_ai_sdlc/evidence-ledger.md", markdown(ledger))
    if args.coverage:
        value = {"schema": "ai-sdlc-evidence-coverage/v1", "ledger_fingerprint": ledger["fingerprint"], "coverage": ledger["coverage"]}
    elif args.stale:
        value = {"schema": "ai-sdlc-evidence-stale-paths/v1", "ledger_fingerprint": ledger["fingerprint"], "stale_paths": ledger["stale_paths"]}
    else:
        value = ledger
    if args.format == "json":
        print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))
    elif args.format == "toon":
        print(encode_toon(value), end="")
    elif value.get("schema") == LEDGER_SCHEMA:
        print(markdown(value), end="")
    else:
        print("```json")
        print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))
        print("```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
