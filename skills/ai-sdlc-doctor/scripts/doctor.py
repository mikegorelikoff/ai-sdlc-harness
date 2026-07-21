#!/usr/bin/env python3
"""Diagnose harness installations and preview safe upgrade plans."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import encode_toon

REPORT_SCHEMA = "ai-sdlc-doctor-report/v1"
INVENTORY_SCHEMA = "ai-sdlc-upgrade-inventory/v1"
PLAN_SCHEMA = "ai-sdlc-upgrade-plan/v1"
INVENTORY_FIELDS = {"schema", "version", "harness_api", "files"}
FILE_FIELDS = {"path", "sha256", "schema"}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256((value if isinstance(value, str) else canonical(value)).encode()).hexdigest()


def atomic_write(path: Path, content: str) -> None:
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


def check(code: str, passed: bool, evidence: str, remediation: str) -> dict[str, str]:
    return {"code": code, "status": "pass" if passed else "fail", "evidence": evidence, "remediation": "" if passed else remediation}


def doctor(repository: Path) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    python_ok = sys.version_info >= (3, 9)
    checks.append(check("python-version", python_ok, f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", "Install Python 3.9 or newer."))
    git = shutil.which("git")
    checks.append(check("git-available", git is not None, git or "not found", "Install Git and make it available on PATH."))
    required = ["README.md", "skills", "modules", "docs", "mkdocs.yml"]
    missing = [item for item in required if not (repository / item).exists()]
    checks.append(check("repository-layout", not missing, "missing=" + (",".join(missing) or "none"), "Restore required harness paths: " + ", ".join(missing)))
    module_errors: list[str] = []
    module_ids: list[str] = []
    registered: list[tuple[str, str]] = []
    for path in sorted((repository / "modules").glob("*/module.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            module_errors.append(f"{path.parent.name}:unreadable")
            continue
        if value.get("schema") != "ai-sdlc-module/v1" or not isinstance(value.get("id"), str) or not isinstance(value.get("skills"), list):
            module_errors.append(f"{path.parent.name}:invalid")
            continue
        module_ids.append(value["id"])
        registered.extend((value["id"], item.get("path", "")) for item in value["skills"] if isinstance(item, dict))
    if len(module_ids) != len(set(module_ids)):
        module_errors.append("duplicate-module-id")
    checks.append(check("module-contracts", bool(module_ids) and not module_errors, "modules=" + str(len(module_ids)) + ";errors=" + (",".join(module_errors) or "none"), "Repair invalid or duplicate module manifests."))
    missing_skills = sorted(f"{module}:{path}" for module, path in registered if not path or not (repository / path / "SKILL.md").is_file())
    checks.append(check("skill-registration", bool(registered) and not missing_skills, "registered=" + str(len(registered)) + ";missing=" + (",".join(missing_skills) or "none"), "Restore registered skill packages or update their module manifests."))
    docs_missing = [item for item in ("mkdocs.yml", "requirements-docs.txt") if not (repository / item).is_file()]
    checks.append(check("docs-configuration", not docs_missing, "missing=" + (",".join(docs_missing) or "none"), "Restore documentation configuration files."))
    report: dict[str, Any] = {"schema": REPORT_SCHEMA, "repository": repository.as_posix(), "status": "healthy" if all(item["status"] == "pass" for item in checks) else "unhealthy", "checks": checks}
    report["fingerprint"] = digest(report)
    return report


def semver(value: Any) -> tuple[int, int, int] | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        return None
    return tuple(int(item) for item in value.split("."))


def safe_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and all(part not in {"", "."} for part in path.parts)


def validate_inventory(value: Any, label: str) -> list[str]:
    if not isinstance(value, dict) or set(value) != INVENTORY_FIELDS:
        return [f"{label} fields must match {INVENTORY_SCHEMA}"]
    errors: list[str] = []
    if value["schema"] != INVENTORY_SCHEMA or semver(value["version"]) is None:
        errors.append(f"{label} schema or version is invalid")
    api = value["harness_api"]
    if not isinstance(api, dict) or set(api) != {"min", "max_exclusive"} or semver(api.get("min")) is None or semver(api.get("max_exclusive")) is None or semver(api["min"]) >= semver(api["max_exclusive"]):
        errors.append(f"{label} harness_api range is invalid")
    if not isinstance(value["files"], list):
        return errors + [f"{label} files must be an array"]
    paths: list[str] = []
    for index, item in enumerate(value["files"]):
        if not isinstance(item, dict) or set(item) != FILE_FIELDS:
            errors.append(f"{label} file {index} fields are invalid")
            continue
        paths.append(item["path"] if isinstance(item["path"], str) else "")
        if not safe_path(item["path"]):
            errors.append(f"{label} file {index} path is unsafe")
        if not isinstance(item["sha256"], str) or not re.fullmatch(r"[a-f0-9]{64}", item["sha256"]):
            errors.append(f"{label} file {index} sha256 is invalid")
        if not isinstance(item["schema"], str):
            errors.append(f"{label} file {index} schema must be a string")
    if len(paths) != len(set(paths)):
        errors.append(f"{label} file paths must be unique")
    return errors


def api_compatible(inventory: dict[str, Any], active: tuple[int, int, int]) -> bool:
    return semver(inventory["harness_api"]["min"]) <= active < semver(inventory["harness_api"]["max_exclusive"])


def upgrade_plan(current: dict[str, Any], target: dict[str, Any], upgrade_id: str, active_api: tuple[int, int, int]) -> dict[str, Any]:
    before = {item["path"]: item for item in current["files"]}
    after = {item["path"]: item for item in target["files"]}
    changes: list[dict[str, str]] = []
    backups: list[dict[str, str]] = []
    migrations: list[dict[str, str]] = []
    rollback: list[dict[str, str]] = []
    for path in sorted(set(before) | set(after)):
        old, new = before.get(path), after.get(path)
        if old is None:
            action = "add"
        elif new is None:
            action = "remove"
        elif old["sha256"] != new["sha256"]:
            action = "modify"
        else:
            action = "unchanged"
        changes.append({"path": path, "action": action, "before_sha256": old["sha256"] if old else "", "after_sha256": new["sha256"] if new else "", "before_schema": old["schema"] if old else "", "after_schema": new["schema"] if new else ""})
        if action in {"modify", "remove"}:
            backup = f"_ai_sdlc/backups/{upgrade_id}/{path}"
            backups.append({"path": path, "destination": backup, "sha256": old["sha256"]})
            rollback.append({"path": path, "action": "restore", "source": backup, "sha256": old["sha256"]})
        elif action == "add":
            rollback.append({"path": path, "action": "remove", "source": "", "sha256": new["sha256"]})
        if old and new and old["schema"] != new["schema"]:
            migrations.append({"path": path, "from": old["schema"], "to": new["schema"], "status": "required"})
    blockers = [] if api_compatible(target, active_api) else ["target-harness-api-incompatible"]
    plan: dict[str, Any] = {"schema": PLAN_SCHEMA, "upgrade_id": upgrade_id, "from_version": current["version"], "to_version": target["version"], "active_harness_api": ".".join(map(str, active_api)), "compatible": not blockers, "changes": changes, "migrations": migrations, "backups": backups, "rollback": list(reversed(rollback)), "blockers": blockers, "current_fingerprint": digest(current), "target_fingerprint": digest(target)}
    plan["fingerprint"] = digest(plan)
    return plan


def markdown(value: dict[str, Any]) -> str:
    if value["schema"] == REPORT_SCHEMA:
        lines = ["# Installation Doctor", "", f"Status: **{value['status']}**", f"Fingerprint: `{value['fingerprint']}`", "", "| Check | Status | Evidence |", "| --- | --- | --- |"]
        lines.extend(f"| `{item['code']}` | {item['status']} | {item['evidence']} |" for item in value["checks"])
        return "\n".join(lines) + "\n"
    lines = ["# Upgrade Plan", "", f"Upgrade: `{value['from_version']}` -> `{value['to_version']}`", f"Compatible: **{str(value['compatible']).lower()}**", f"Fingerprint: `{value['fingerprint']}`", "", "| Path | Action |", "| --- | --- |"]
    lines.extend(f"| `{item['path']}` | {item['action']} |" for item in value["changes"])
    return "\n".join(lines) + "\n"


def load(path: Path, label: str) -> tuple[Any, list[str]]:
    try:
        return json.loads(path.resolve().read_text(encoding="utf-8")), []
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read {label}: {exc}"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--doctor", action="store_true")
    actions.add_argument("--upgrade", action="store_true")
    parser.add_argument("--current", type=Path)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--upgrade-id")
    parser.add_argument("--harness-api", default="1.0.0")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--format", choices=("toon", "json", "markdown"), default="toon")
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
        print("ERROR: diagnostics cannot mutate feature lifecycle state")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir():
        print("ERROR: repository does not exist")
        return 1
    if args.doctor:
        value = doctor(repository)
        output = repository / "_ai_sdlc/doctor/report.json"
        exit_code = 0 if value["status"] == "healthy" else 2
    else:
        if not args.current or not args.target or not args.upgrade_id or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.upgrade_id):
            print("ERROR: upgrade requires --current, --target, and safe --upgrade-id")
            return 1
        active_api = semver(args.harness_api)
        if active_api is None:
            print("ERROR: --harness-api must use x.y.z")
            return 1
        current, errors = load(args.current, "current inventory")
        target, target_errors = load(args.target, "target inventory")
        errors.extend(target_errors)
        errors.extend(validate_inventory(current, "current") if not errors else [])
        errors.extend(validate_inventory(target, "target") if not target_errors else [])
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        value = upgrade_plan(current, target, args.upgrade_id, active_api)
        output = repository / f"_ai_sdlc/upgrades/{args.upgrade_id}/plan.json"
        exit_code = 0 if value["compatible"] else 2
    if args.write:
        atomic_write(output, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        atomic_write(output.with_suffix(".toon"), encode_toon(value))
        atomic_write(output.with_suffix(".md"), markdown(value))
    if args.format == "json":
        print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))
    elif args.format == "markdown":
        print(markdown(value), end="")
    else:
        print(encode_toon(value), end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
