#!/usr/bin/env python3
"""Create and validate isolated AI SDLC change workspaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import encode_toon
from ai_sdlc_safe_io import bounded_path, ensure_directory


SCHEMA = "ai-sdlc-change-set/v1"
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_ARTIFACTS = {
    "proposal": "proposal.md",
    "design": "design.md",
    "tasks": "tasks.md",
    "deltas": "deltas/index.md",
    "evidence": "evidence/index.md",
    "record": "_ai_sdlc/change-set.json",
}
REQUIRED_PROPOSAL_HEADINGS = (
    "Goal",
    "Motivation",
    "Scope",
    "Out of Scope",
    "Canonical Targets",
    "Authority And Approval",
    "Assumptions And Open Questions",
)


def flow_mode(args: argparse.Namespace) -> str:
    """Resolve flow precedence."""
    return "full" if args.full_flow else "quick" if args.quick_flow else "default"


def safe_target(value: str) -> str | None:
    """Return a normalized safe repository-relative target or none."""
    if not value or "\\" in value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return None
    normalized = path.as_posix()
    if path.parts[0] == "changes":
        return None
    return normalized


def fingerprint(record: dict[str, Any]) -> str:
    """Hash the semantic record without its self-referential fingerprint."""
    payload = {key: value for key, value in record.items() if key != "contract_fingerprint"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def validate_inputs(
    change_id: str,
    title: str | None,
    summary: str | None,
    owner: str | None,
    targets: list[str],
    require_content: bool,
) -> tuple[list[str], list[str]]:
    """Validate creation inputs and return normalized targets."""
    errors: list[str] = []
    if not ID_PATTERN.fullmatch(change_id):
        errors.append("change_id must use lowercase letters, digits, and single hyphens")
    if require_content:
        for field, value in (("title", title), ("summary", summary), ("owner", owner)):
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{field} is required")
        if not targets:
            errors.append("at least one canonical target is required")
    normalized: list[str] = []
    for target in targets:
        safe = safe_target(target)
        if safe is None:
            errors.append(f"unsafe canonical target: {target}")
        else:
            normalized.append(safe)
    if len(normalized) != len(set(normalized)):
        errors.append("canonical targets must be unique")
    return errors, sorted(set(normalized))


def build_record(args: argparse.Namespace, targets: list[str]) -> dict[str, Any]:
    """Build one deterministic machine record."""
    stamp = args.date or date.today().isoformat()
    try:
        date.fromisoformat(stamp)
    except ValueError as exc:
        raise ValueError("date must use YYYY-MM-DD") from exc
    record: dict[str, Any] = {
        "schema": SCHEMA,
        "change_id": args.change_id,
        "title": args.title.strip(),
        "summary": args.summary.strip(),
        "status": "draft",
        "owner": args.owner.strip(),
        "flow_mode": flow_mode(args),
        "created_at": stamp,
        "updated_at": stamp,
        "canonical_targets": targets,
        "artifacts": REQUIRED_ARTIFACTS,
        "authority": {
            "canonical_mutation_allowed": False,
            "policy_mutation_allowed": False,
            "requires_preview": True,
            "requires_approval": True,
        },
    }
    record["contract_fingerprint"] = fingerprint(record)
    return record


def yaml_list(values: list[str], indent: str = "  ") -> list[str]:
    """Render a stable quoted YAML list."""
    return [f'{indent}- {json.dumps(value, ensure_ascii=False)}' for value in values]


def metadata(record: dict[str, Any], artifact: str, relative: str) -> str:
    """Render artifact metadata shared by workspace Markdown."""
    lines = [
        "---",
        "artifact_metadata:",
        '  schema: "ai-sdlc-change-set-metadata/v1"',
        f'  change_id: {json.dumps(record["change_id"])}',
        f'  artifact: {json.dumps(artifact)}',
        f'  path: {json.dumps("changes/" + record["change_id"] + "/" + relative)}',
        f'  status: {json.dumps(record["status"])}',
        f'  owner: {json.dumps(record["owner"])}',
        f'  created_at: {json.dumps(record["created_at"])}',
        f'  updated_at: {json.dumps(record["updated_at"])}',
        "  canonical_targets:",
        *yaml_list(record["canonical_targets"], "    "),
        "  metatags:",
        '    - "ai-sdlc"',
        '    - "change-set"',
        '    - "proposal"',
        '    - "draft"',
        "---",
    ]
    return "\n".join(lines)


def render_files(record: dict[str, Any]) -> dict[str, str]:
    """Render every required workspace artifact."""
    targets = "\n".join(f"- `{target}`" for target in record["canonical_targets"])
    prefix = metadata(record, "proposal.md", "proposal.md")
    proposal = f"""{prefix}

# Change Proposal: {record['title']}

## Goal

{record['summary']}

## Motivation

Document the evidence and user value that justify this change.

## Scope

- Define the intended behavior change without editing canonical targets.

## Out of Scope

- Canonical mutation, approval, release, and deployment.

## Canonical Targets

{targets}

## Authority And Approval

- Owner: {record['owner']}
- Status: draft
- Canonical mutation allowed: no
- Required next gates: delta validation, impact preview, policy evaluation, approval.

## Assumptions And Open Questions

- Record unresolved assumptions and assign owners before apply.
"""
    design = f"""{metadata(record, 'design.md', 'design.md')}

# Change Design

## Current State

Pending evidence-backed analysis.

## Proposed Design

Pending delta authoring and technical review.

## Compatibility And Migration

No canonical change has been approved.

## Validation Strategy

Define validation before apply.
"""
    tasks = f"""{metadata(record, 'tasks.md', 'tasks.md')}

# Change Tasks

## Planning

- [ ] Author and validate requirement deltas.
- [ ] Review impact, policy gates, compatibility, and migration needs.
- [ ] Obtain required approval before apply.

## Implementation

- [ ] Add implementation tasks after preview confirms scope.
"""
    deltas = f"""{metadata(record, 'deltas/index.md', 'deltas/index.md')}

# Delta Index

No requirement deltas have been authored. Add delta documents only through the
semantic delta workflow.
"""
    evidence = f"""{metadata(record, 'evidence/index.md', 'evidence/index.md')}

# Evidence Index

No evidence has been registered. Evidence entries must retain source identity,
locator, freshness, credibility, and trace targets.
"""
    return {
        "proposal.md": proposal.rstrip() + "\n",
        "design.md": design.rstrip() + "\n",
        "tasks.md": tasks.rstrip() + "\n",
        "deltas/index.md": deltas.rstrip() + "\n",
        "evidence/index.md": evidence.rstrip() + "\n",
        "_ai_sdlc/change-set.json": json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        "_ai_sdlc/change-set.toon": encode_toon(record),
    }


def atomic_create(repository: Path, destination: Path, files: dict[str, str]) -> None:
    """Create a complete workspace without exposing partial output."""
    destination = bounded_path(repository, destination)
    if destination.exists():
        raise FileExistsError(f"workspace already exists: {destination}")
    ensure_directory(repository, destination.parent)
    temp = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent))
    try:
        for relative, content in files.items():
            path = temp / relative
            ensure_directory(temp, path.parent)
            path.write_text(content, encoding="utf-8")
        os.replace(temp, destination)
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


def load_record(workspace: Path) -> tuple[dict[str, Any], list[str]]:
    """Load a workspace record with actionable errors."""
    path = workspace / REQUIRED_ARTIFACTS["record"]
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read change-set record: {exc}"]
    if not isinstance(value, dict):
        return {}, ["change-set record must be a JSON object"]
    return value, []


def validate_record(record: dict[str, Any], expected_id: str) -> list[str]:
    """Validate the versioned record without third-party dependencies."""
    errors: list[str] = []
    required = {
        "schema", "change_id", "title", "summary", "status", "owner",
        "flow_mode", "created_at", "updated_at", "canonical_targets",
        "artifacts", "authority", "contract_fingerprint",
    }
    missing = sorted(required - set(record))
    if missing:
        errors.append("record missing fields: " + ", ".join(missing))
        return errors
    optional = {"applied_at", "archived_at", "preview_fingerprint", "approval", "archive_path"}
    if set(record) - required - optional:
        errors.append("record contains unsupported fields: " + ", ".join(sorted(set(record) - required - optional)))
    if record.get("schema") != SCHEMA:
        errors.append(f"record schema must be {SCHEMA}")
    if record.get("change_id") != expected_id or not isinstance(record.get("change_id"), str) or not ID_PATTERN.fullmatch(record["change_id"]):
        errors.append("record change_id does not match the safe workspace ID")
    for field in ("title", "summary", "owner"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            errors.append(f"record {field} is required")
    if record.get("status") not in {"draft", "applied", "archived"}:
        errors.append("record status must be draft, applied, or archived")
    if record.get("status") in {"applied", "archived"}:
        for field_name in ("applied_at", "preview_fingerprint", "approval"):
            if not record.get(field_name):
                errors.append(f"record {field_name} is required after apply")
    if record.get("status") == "archived" and (not record.get("archived_at") or not record.get("archive_path")):
        errors.append("record archived_at and archive_path are required after archive")
    if record.get("flow_mode") not in {"default", "quick", "full"}:
        errors.append("record flow_mode is invalid")
    for field in ("created_at", "updated_at"):
        try:
            date.fromisoformat(record.get(field, ""))
        except (TypeError, ValueError):
            errors.append(f"record {field} must use YYYY-MM-DD")
    targets = record.get("canonical_targets")
    if not isinstance(targets, list) or not targets or not all(isinstance(item, str) for item in targets):
        errors.append("record canonical_targets must be a non-empty string array")
    else:
        normalized = [safe_target(item) for item in targets]
        if any(item is None for item in normalized):
            errors.append("record contains an unsafe canonical target")
        if targets != sorted(set(targets)):
            errors.append("record canonical_targets must be sorted and unique")
    if record.get("artifacts") != REQUIRED_ARTIFACTS:
        errors.append("record artifacts do not match the required workspace contract")
    expected_authority = {
        "canonical_mutation_allowed": False,
        "policy_mutation_allowed": False,
        "requires_preview": True,
        "requires_approval": True,
    }
    if record.get("authority") != expected_authority:
        errors.append("record authority must preserve preview and approval boundaries")
    if record.get("contract_fingerprint") != fingerprint(record):
        errors.append("record contract_fingerprint is stale or invalid")
    return errors


def validate_workspace(workspace: Path, change_id: str) -> tuple[dict[str, Any], list[str]]:
    """Validate required files, record, metadata, and proposal headings."""
    errors = [f"missing required artifact: {relative}" for relative in REQUIRED_ARTIFACTS.values() if not (workspace / relative).is_file()]
    toon_path = workspace / "_ai_sdlc/change-set.toon"
    if not toon_path.is_file():
        errors.append("missing required artifact: _ai_sdlc/change-set.toon")
    if errors:
        return {}, errors
    record, load_errors = load_record(workspace)
    errors.extend(load_errors)
    if load_errors:
        return {}, errors
    errors.extend(validate_record(record, change_id))
    if toon_path.read_text(encoding="utf-8") != encode_toon(record):
        errors.append("change-set TOON projection is stale or invalid")
    for name, relative in REQUIRED_ARTIFACTS.items():
        if name == "record":
            continue
        text = (workspace / relative).read_text(encoding="utf-8")
        if 'schema: "ai-sdlc-change-set-metadata/v1"' not in text:
            errors.append(f"{relative}: missing change-set metadata")
        if f'change_id: "{change_id}"' not in text:
            errors.append(f"{relative}: change_id metadata mismatch")
        if f'owner: {json.dumps(record.get("owner", ""))}' not in text:
            errors.append(f"{relative}: owner metadata mismatch")
        if f'status: {json.dumps(record.get("status", ""))}' not in text:
            errors.append(f"{relative}: status metadata mismatch")
        for target in record.get("canonical_targets", []):
            if json.dumps(target) not in text:
                errors.append(f"{relative}: canonical target metadata mismatch: {target}")
    proposal = (workspace / "proposal.md").read_text(encoding="utf-8")
    for heading in REQUIRED_PROPOSAL_HEADINGS:
        if f"## {heading}" not in proposal:
            errors.append(f"proposal.md: missing heading {heading}")
    return record, errors


def render_toon(record: dict[str, Any], workspace: Path, valid: bool) -> str:
    """Render the complete machine result as TOON."""
    return encode_toon({"workspace": workspace.as_posix(), "valid": valid, **record})


def emit_result(record: dict[str, Any], workspace: Path, valid: bool, output_format: str) -> None:
    """Print deterministic human or machine output."""
    if output_format == "json":
        print(json.dumps({"workspace": workspace.as_posix(), "valid": valid, **record}, indent=2, sort_keys=True, ensure_ascii=False))
    elif output_format == "toon":
        print(render_toon(record, workspace, valid), end="")
    else:
        print(f"Change set: {record.get('change_id', '')}")
        print(f"Workspace: {workspace}")
        print(f"Status: {record.get('status', '')}")
        print(f"Owner: {record.get('owner', '')}")
        print("Targets: " + ", ".join(record.get("canonical_targets", [])))
        print(f"Fingerprint: {record.get('contract_fingerprint', '')}")
        print(f"Validation: {'passed' if valid else 'failed'}")


def main() -> int:
    """Create, emit, or validate one isolated change workspace."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--change-id", required=True)
    parser.add_argument("--title")
    parser.add_argument("--summary")
    parser.add_argument("--owner")
    parser.add_argument("--target", action="append", default=[])
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--emit", action="store_true")
    actions.add_argument("--create", action="store_true")
    actions.add_argument("--validate", action="store_true")
    parser.add_argument("--format", choices=("markdown", "json", "toon"), default="toon")
    parser.add_argument("--date", help="Override the creation date for deterministic fixtures")
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
        print("ERROR: change workspace intake cannot mutate feature lifecycle state")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir():
        print(f"ERROR: repository does not exist: {repository}")
        return 1
    workspace = repository / "changes" / args.change_id

    if args.validate:
        input_errors, _ = validate_inputs(args.change_id, None, None, None, [], False)
        if input_errors:
            for error in input_errors:
                print(f"ERROR: {error}")
            return 1
        record, errors = validate_workspace(workspace, args.change_id)
        for error in errors:
            print(f"ERROR: {error}")
        if not errors:
            emit_result(record, workspace, True, args.format)
        return 1 if errors else 0

    errors, targets = validate_inputs(args.change_id, args.title, args.summary, args.owner, args.target, True)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    try:
        record = build_record(args, targets)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    if args.create:
        try:
            atomic_create(repository, workspace, render_files(record))
        except (FileExistsError, OSError, ValueError) as exc:
            print(f"ERROR: {exc}")
            return 1
        validated, workspace_errors = validate_workspace(workspace, args.change_id)
        if workspace_errors:
            for error in workspace_errors:
                print(f"ERROR: {error}")
            return 1
        record = validated
    emit_result(record, workspace, True, args.format)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
