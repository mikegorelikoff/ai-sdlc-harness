#!/usr/bin/env python3
"""Apply approved change previews with rollback, then archive evidence."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from change_preview import apply_virtual, build_preview, digest
from change_set import REQUIRED_ARTIFACTS, fingerprint, validate_workspace
from spec_delta import analyze_delta_set


APPROVAL_SCHEMA = "ai-sdlc-change-approval/v1"
RECOVERY_SCHEMA = "ai-sdlc-change-recovery/v1"


def now() -> str:
    """Return an auditable UTC timestamp."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def atomic_write(path: Path, content: str) -> None:
    """Replace one repository file atomically on its own filesystem."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    """Write deterministic JSON atomically."""
    atomic_write(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def load_approval(path: Path, change_id: str, preview: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Validate explicit approval against the current preview and gates."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read approval: {exc}"]
    if not isinstance(value, dict):
        return {}, ["approval must be a JSON object"]
    required = {"schema", "change_id", "preview_fingerprint", "decision", "owner", "decided_at", "decision_ref", "approved_gates"}
    errors: list[str] = []
    if set(value) != required:
        errors.append("approval fields must match the versioned contract exactly")
    if value.get("schema") != APPROVAL_SCHEMA:
        errors.append(f"approval schema must be {APPROVAL_SCHEMA}")
    if value.get("change_id") != change_id:
        errors.append("approval change_id mismatch")
    if value.get("preview_fingerprint") != preview.get("preview_fingerprint"):
        errors.append("approval preview_fingerprint is stale")
    if value.get("decision") != "accepted":
        errors.append("approval decision must be accepted")
    for field in ("owner", "decision_ref"):
        if not isinstance(value.get(field), str) or not value[field].strip():
            errors.append(f"approval {field} is required")
    timestamp = value.get("decided_at")
    try:
        datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
    except ValueError:
        errors.append("approval decided_at must be an ISO timestamp")
    approved = value.get("approved_gates")
    if not isinstance(approved, list) or not approved or not all(isinstance(item, str) and item for item in approved) or len(approved) != len(set(approved)):
        errors.append("approval approved_gates must be a unique non-empty string array")
    else:
        required_gates = {item["gate"] for item in preview.get("required_gates", [])}
        missing = sorted(required_gates - set(approved))
        if missing:
            errors.append("approval missing required gates: " + ", ".join(missing))
    return value, errors


def update_metadata(workspace: Path, status: str, updated_at: str) -> None:
    """Keep required human artifact lifecycle metadata aligned."""
    for name, relative in REQUIRED_ARTIFACTS.items():
        if name == "record":
            continue
        path = workspace / relative
        text = path.read_text(encoding="utf-8")
        text, status_count = re.subn(r'(?m)^  status: "(?:draft|applied|archived)"$', f'  status: "{status}"', text, count=1)
        text, date_count = re.subn(r'(?m)^  updated_at: "[^"]+"$', f'  updated_at: "{updated_at[:10]}"', text, count=1)
        if status_count != 1 or date_count != 1:
            raise ValueError(f"{relative}: cannot update lifecycle metadata")
        atomic_write(path, text)


def compile_after_states(repository: Path, change_id: str, preview: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    """Recompile exact after-state content and verify preview hashes."""
    delta, errors = analyze_delta_set(repository, change_id)
    if errors:
        return {}, errors
    after_states: dict[str, str] = {}
    preview_targets = {item["target"]: item for item in preview["targets"]}
    for target in sorted(preview_targets):
        path = repository / target
        if path.is_symlink():
            errors.append(f"{target}: apply refuses symlink targets")
            continue
        before = path.read_text(encoding="utf-8") if path.is_file() else ""
        operations = [item for item in delta["operations"] if item["target"] == target]
        after, conflicts = apply_virtual(before, operations, target)
        if conflicts:
            errors.extend(f"{item['code']}: {target}#{item['requirement_id']}" for item in conflicts)
            continue
        expected = preview_targets[target]
        if digest(before) != expected["before_sha256"] or digest(after) != expected["after_sha256"]:
            errors.append(f"{target}: target or virtual after-state drifted after preview")
        after_states[target] = after
    return after_states, errors


def rollback(repository: Path, workspace: Path, manifest: dict[str, Any]) -> list[str]:
    """Restore every recorded applied target in reverse order."""
    errors: list[str] = []
    targets = {item["target"]: item for item in manifest.get("targets", [])}
    for target in reversed(manifest.get("applied", [])):
        item = targets.get(target, {})
        path = repository / target
        try:
            if item.get("existed"):
                backup = workspace / item["backup"]
                descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".rollback.", dir=path.parent)
                os.close(descriptor)
                shutil.copyfile(backup, temporary)
                os.replace(temporary, path)
            elif path.exists():
                path.unlink()
        except OSError as exc:
            errors.append(f"{target}: rollback failed: {exc}")
    manifest["status"] = "rollback_failed" if errors else "rolled_back"
    manifest["rollback_errors"] = errors
    manifest["updated_at"] = now()
    atomic_json(workspace / "_ai_sdlc/recovery-manifest.json", manifest)
    return errors


def recover_incomplete(repository: Path, workspace: Path) -> list[str]:
    """Recover an interrupted prior transaction before any new apply."""
    path = workspace / "_ai_sdlc/recovery-manifest.json"
    if not path.is_file():
        return []
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot inspect recovery manifest: {exc}"]
    if manifest.get("status") not in {"in_progress", "rollback_failed"}:
        return []
    errors = rollback(repository, workspace, manifest)
    return errors or ["recovered an incomplete prior transaction; review evidence and rerun apply"]


def apply_change(repository: Path, change_id: str, approval_path: Path, simulate_failure_after: int | None) -> tuple[dict[str, Any], list[str]]:
    """Apply one approved ready preview with fail-safe rollback."""
    workspace = repository / "changes" / change_id
    record, errors = validate_workspace(workspace, change_id)
    if errors:
        return {}, errors
    if record["status"] != "draft":
        return {}, [f"change status must be draft before apply; got {record['status']}"]
    recovery_errors = recover_incomplete(repository, workspace)
    if recovery_errors:
        return {}, recovery_errors
    preview, preview_errors = build_preview(repository, change_id)
    errors.extend(preview_errors)
    if preview and preview["status"] != "ready":
        errors.append("current preview is blocked")
    approval, approval_errors = load_approval(approval_path, change_id, preview)
    errors.extend(approval_errors)
    after_states, compile_errors = compile_after_states(repository, change_id, preview) if preview else ({}, [])
    errors.extend(compile_errors)
    if errors:
        return {}, errors

    staging_root = workspace / "_ai_sdlc/staging"
    targets: list[dict[str, Any]] = []
    for target, after in sorted(after_states.items()):
        path = repository / target
        existed = path.is_file()
        backup = Path("_ai_sdlc/backups") / target
        staging = Path("_ai_sdlc/staging") / target
        if existed:
            backup_path = workspace / backup
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            backup_path.write_bytes(path.read_bytes())
        staging_path = workspace / staging
        staging_path.parent.mkdir(parents=True, exist_ok=True)
        staging_path.write_text(after, encoding="utf-8")
        targets.append({"target": target, "existed": existed, "backup": backup.as_posix() if existed else "", "staging": staging.as_posix(), "before_sha256": next(item["before_sha256"] for item in preview["targets"] if item["target"] == target), "after_sha256": digest(after)})

    manifest: dict[str, Any] = {"schema": RECOVERY_SCHEMA, "change_id": change_id, "status": "in_progress", "preview_fingerprint": preview["preview_fingerprint"], "created_at": now(), "updated_at": now(), "targets": targets, "applied": [], "rollback_errors": []}
    manifest_path = workspace / "_ai_sdlc/recovery-manifest.json"
    atomic_json(manifest_path, manifest)
    atomic_json(workspace / "evidence/approval.json", approval)
    try:
        for index, item in enumerate(targets, start=1):
            target_path = repository / item["target"]
            target_path.parent.mkdir(parents=True, exist_ok=True)
            os.replace(workspace / item["staging"], target_path)
            manifest["applied"].append(item["target"])
            manifest["updated_at"] = now()
            atomic_json(manifest_path, manifest)
            if simulate_failure_after is not None and index >= simulate_failure_after:
                raise OSError(f"simulated failure after {index} target replacements")
        applied_at = now()
        update_metadata(workspace, "applied", applied_at)
        record.update({"status": "applied", "updated_at": applied_at[:10], "applied_at": applied_at, "preview_fingerprint": preview["preview_fingerprint"], "approval": {"owner": approval["owner"], "decision_ref": approval["decision_ref"], "decided_at": approval["decided_at"], "approved_gates": sorted(approval["approved_gates"])}})
        record["contract_fingerprint"] = fingerprint(record)
        atomic_json(workspace / "_ai_sdlc/change-set.json", record)
    except (OSError, ValueError) as exc:
        rollback_errors = rollback(repository, workspace, manifest)
        try:
            update_metadata(workspace, "draft", record["updated_at"])
        except (OSError, ValueError) as metadata_exc:
            rollback_errors.append(f"workspace metadata rollback failed: {metadata_exc}")
        return {}, [f"apply failed and rollback was attempted: {exc}", *rollback_errors]
    manifest["status"] = "complete"
    manifest["updated_at"] = now()
    atomic_json(manifest_path, manifest)
    shutil.rmtree(staging_root, ignore_errors=True)
    return {"schema": "ai-sdlc-change-apply-result/v1", "change_id": change_id, "status": "applied", "preview_fingerprint": preview["preview_fingerprint"], "targets": [item["target"] for item in targets], "recovery_manifest": manifest_path.relative_to(repository).as_posix()}, []


def archive_change(repository: Path, change_id: str, archive_date: str | None) -> tuple[dict[str, Any], list[str]]:
    """Move a completely applied workspace into immutable history."""
    workspace = repository / "changes" / change_id
    if not workspace.is_dir():
        matches = sorted((repository / "changes/archive").glob(f"*-{change_id}"))
        return {}, [f"active change is absent; archived copies: {', '.join(path.name for path in matches) or 'none'}"]
    record, errors = validate_workspace(workspace, change_id)
    if errors:
        return {}, errors
    if record["status"] != "applied":
        return {}, [f"change status must be applied before archive; got {record['status']}"]
    manifest_path = workspace / "_ai_sdlc/recovery-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read recovery manifest: {exc}"]
    if manifest.get("status") != "complete":
        return {}, ["recovery manifest must be complete before archive"]
    stamp = archive_date or datetime.now(timezone.utc).date().isoformat()
    try:
        datetime.fromisoformat(stamp)
    except ValueError:
        return {}, ["archive date must use YYYY-MM-DD"]
    destination = repository / "changes/archive" / f"{stamp}-{change_id}"
    if destination.exists():
        return {}, [f"archive destination already exists: {destination}"]
    archived_at = now()
    prior = dict(record)
    try:
        update_metadata(workspace, "archived", archived_at)
        record.update({"status": "archived", "updated_at": archived_at[:10], "archived_at": archived_at, "archive_path": destination.relative_to(repository).as_posix()})
        record["contract_fingerprint"] = fingerprint(record)
        atomic_json(workspace / "_ai_sdlc/change-set.json", record)
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.replace(workspace, destination)
    except (OSError, ValueError) as exc:
        if workspace.exists():
            try:
                update_metadata(workspace, "applied", prior["updated_at"])
                atomic_json(workspace / "_ai_sdlc/change-set.json", prior)
            except (OSError, ValueError):
                pass
        return {}, [f"archive failed: {exc}"]
    return {"schema": "ai-sdlc-change-archive-result/v1", "change_id": change_id, "status": "archived", "archive_path": destination.relative_to(repository).as_posix(), "preview_fingerprint": record["preview_fingerprint"]}, []


def main() -> int:
    """Apply or archive a controlled change."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--change-id", required=True)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--apply", action="store_true")
    actions.add_argument("--archive", action="store_true")
    parser.add_argument("--approval", type=Path)
    parser.add_argument("--archive-date")
    parser.add_argument("--format", choices=("markdown", "json", "toon"), default="markdown")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    parser.add_argument("--simulate-failure-after", type=int, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        print("ERROR: controlled apply owns change state, not feature lifecycle state")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir():
        print(f"ERROR: repository does not exist: {repository}")
        return 1
    if args.apply:
        if args.approval is None:
            print("ERROR: --approval is required for apply")
            return 1
        if args.simulate_failure_after is not None and args.simulate_failure_after < 1:
            print("ERROR: simulated failure position must be positive")
            return 1
        result, errors = apply_change(repository, args.change_id, args.approval.resolve(), args.simulate_failure_after)
    else:
        result, errors = archive_change(repository, args.change_id, args.archive_date)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    elif args.format == "toon":
        print("\n".join(f"{key}: {value if not isinstance(value, list) else '/'.join(value)}" for key, value in result.items()))
    else:
        print(f"Change: {result['change_id']}")
        print(f"Status: {result['status']}")
        print(f"Preview: {result['preview_fingerprint']}")
        print(f"Evidence: {result.get('recovery_manifest') or result.get('archive_path')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
