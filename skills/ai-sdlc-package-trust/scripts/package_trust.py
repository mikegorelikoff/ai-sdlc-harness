#!/usr/bin/env python3
"""Verify package origin, integrity, compatibility, capabilities, and provenance."""

from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any
_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import encode_toon
from ai_sdlc_safe_io import atomic_write_text

PACKAGE_SCHEMA = "ai-sdlc-package/v1"
DECISION_SCHEMA = "ai-sdlc-package-trust-decision/v1"
FIELDS = {"schema", "id", "version", "origin", "harness_api", "capabilities", "files", "digest", "provenance"}

def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def digest(value: Any) -> str:
    return hashlib.sha256((value if isinstance(value, str) else canonical(value)).encode()).hexdigest()
def file_hash(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            value.update(chunk)
    return value.hexdigest()
def atomic_write(root: Path, path: Path, content: str) -> None:
    atomic_write_text(root, path, content)
def semver(value: Any) -> tuple[int, int, int] | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value): return None
    return tuple(int(item) for item in value.split("."))
def safe_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value: return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and all(item not in {"", "."} for item in path.parts)

def validate_manifest(value: Any) -> list[str]:
    if not isinstance(value, dict) or set(value) != FIELDS: return [f"manifest fields must match {PACKAGE_SCHEMA}"]
    errors: list[str] = []
    if value["schema"] != PACKAGE_SCHEMA or not isinstance(value["id"], str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value["id"]) or semver(value["version"]) is None: errors.append("package identity is invalid")
    origin = value["origin"]
    if not isinstance(origin, dict) or set(origin) != {"type", "reference"} or not all(isinstance(origin.get(item), str) and origin[item].strip() for item in origin): errors.append("origin is invalid")
    api = value["harness_api"]
    if not isinstance(api, dict) or set(api) != {"min", "max_exclusive"} or semver(api.get("min")) is None or semver(api.get("max_exclusive")) is None or semver(api["min"]) >= semver(api["max_exclusive"]): errors.append("harness_api range is invalid")
    if not isinstance(value["capabilities"], list) or not all(isinstance(item, str) and re.fullmatch(r"[a-z][a-z0-9_-]*(?:\.[a-z][a-z0-9_-]*)+", item) for item in value["capabilities"]) or len(value["capabilities"]) != len(set(value["capabilities"])): errors.append("capabilities are invalid")
    paths: list[str] = []
    if not isinstance(value["files"], list) or not value["files"]: errors.append("files must be non-empty")
    else:
        for index, item in enumerate(value["files"]):
            if not isinstance(item, dict) or set(item) != {"path", "sha256"}: errors.append(f"file {index} fields are invalid"); continue
            paths.append(item["path"] if isinstance(item["path"], str) else "")
            if not safe_path(item["path"]): errors.append(f"file {index} path is unsafe")
            if not isinstance(item["sha256"], str) or not re.fullmatch(r"[a-f0-9]{64}", item["sha256"]): errors.append(f"file {index} hash is invalid")
    if len(paths) != len(set(paths)): errors.append("file paths must be unique")
    if not isinstance(value["digest"], str) or not re.fullmatch(r"[a-f0-9]{64}", value["digest"]): errors.append("package digest is invalid")
    provenance = value["provenance"]
    if not isinstance(provenance, dict) or set(provenance) != {"builder", "source_digest", "attestation"} or not all(isinstance(provenance.get(item), str) for item in provenance): errors.append("provenance fields are invalid")
    return errors

def trust(package_root: Path, manifest: dict[str, Any], origins: set[str], capabilities: set[str], active_api: tuple[int, int, int], require_provenance: bool) -> dict[str, Any]:
    controls: list[dict[str, str]] = []
    def add(code: str, passed: bool, evidence: str) -> None: controls.append({"code": code, "status": "pass" if passed else "fail", "evidence": evidence})
    add("origin", manifest["origin"]["type"] in origins, manifest["origin"]["type"])
    compatible = semver(manifest["harness_api"]["min"]) <= active_api < semver(manifest["harness_api"]["max_exclusive"])
    add("compatibility", compatible, ".".join(map(str, active_api)))
    disallowed = sorted(set(manifest["capabilities"]) - capabilities)
    add("capabilities", not disallowed, "/".join(disallowed) or "allowed")
    file_failures: list[str] = []
    for item in sorted(manifest["files"], key=lambda row: row["path"]):
        path = package_root.joinpath(*PurePosixPath(item["path"]).parts)
        try:
            resolved = path.resolve(strict=True)
            bounded = resolved.is_relative_to(package_root) if hasattr(resolved, "is_relative_to") else package_root == resolved or package_root in resolved.parents
        except OSError:
            bounded = False
        if not bounded or path.is_symlink() or not path.is_file() or file_hash(path) != item["sha256"]: file_failures.append(item["path"])
    inventory = sorted(manifest["files"], key=lambda row: row["path"])
    integrity = not file_failures and digest(inventory) == manifest["digest"]
    add("integrity", integrity, "/".join(file_failures) or ("digest-match" if integrity else "package-digest-mismatch"))
    provenance = manifest["provenance"]
    provenance_ok = not require_provenance or bool(provenance["builder"].strip() and re.fullmatch(r"[a-f0-9]{64}", provenance["source_digest"]) and provenance["attestation"].strip())
    add("provenance", provenance_ok, "present" if provenance_ok else "required-evidence-missing")
    allowed = all(item["status"] == "pass" for item in controls)
    result: dict[str, Any] = {"schema": DECISION_SCHEMA, "package": {"id": manifest["id"], "version": manifest["version"], "manifest_fingerprint": digest(manifest)}, "decision": "allow" if allowed else "deny", "controls": controls, "reason_codes": [f"{item['code']}-{item['status']}" for item in controls]}
    result["fingerprint"] = digest(result)
    return result

def markdown(value: dict[str, Any]) -> str:
    lines = ["# Package Trust Decision", "", f"Package: `{value['package']['id']}@{value['package']['version']}`", f"Decision: **{value['decision']}**", f"Fingerprint: `{value['fingerprint']}`", "", "| Control | Status | Evidence |", "| --- | --- | --- |"]
    lines.extend(f"| `{item['code']}` | {item['status']} | {item['evidence']} |" for item in value["controls"])
    return "\n".join(lines) + "\n"

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path); parser.add_argument("--package-root", type=Path, required=True); parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--allowed-origin", action="append", default=[]); parser.add_argument("--allowed-capability", action="append", default=[]); parser.add_argument("--harness-api", default="1.0.0"); parser.add_argument("--require-provenance", action="store_true"); parser.add_argument("--write", action="store_true"); parser.add_argument("--format", choices=("toon", "json", "markdown"), default="toon")
    parser.add_argument("--quick-flow", action="store_true"); parser.add_argument("--full-flow", action="store_true"); parser.add_argument("--feature", default="<feature-name>"); parser.add_argument("--state-check", action="store_true"); parser.add_argument("--begin-state", action="store_true"); parser.add_argument("--complete-state", action="store_true"); parser.add_argument("--decision-ref"); parser.add_argument("--assumption"); parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    args = parser.parse_args()
    if args.begin_state or args.complete_state: print("ERROR: package trust cannot mutate feature lifecycle state"); return 1
    repository, package_root = args.repository.resolve(), args.package_root.resolve()
    active_api = semver(args.harness_api)
    if not repository.is_dir() or not package_root.is_dir() or active_api is None or not args.allowed_origin: print("ERROR: repository, package root, harness API, and allowed origin are required"); return 1
    try: manifest = json.loads(args.manifest.resolve().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: print(f"ERROR: cannot read manifest: {exc}"); return 1
    errors = validate_manifest(manifest)
    if errors:
        for error in errors: print(f"ERROR: {error}")
        return 1
    value = trust(package_root, manifest, set(args.allowed_origin), set(args.allowed_capability), active_api, args.require_provenance)
    if args.write:
        output = repository / f"_ai_sdlc/trust/{manifest['id']}/decision.json"
        try:
            atomic_write(repository, output, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"); atomic_write(repository, output.with_suffix(".toon"), encode_toon(value)); atomic_write(repository, output.with_suffix(".md"), markdown(value))
        except ValueError as exc:
            print(f"ERROR: {exc}"); return 1
    print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) if args.format == "json" else markdown(value) if args.format == "markdown" else encode_toon(value), end="" if args.format != "json" else "\n")
    return 0 if value["decision"] == "allow" else 2
if __name__ == "__main__": raise SystemExit(main())
