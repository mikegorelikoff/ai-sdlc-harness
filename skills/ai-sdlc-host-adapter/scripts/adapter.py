#!/usr/bin/env python3
"""Validate host adapters and negotiate portable operations safely."""

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

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import encode_toon

ADAPTER_SCHEMA = "ai-sdlc-host-adapter/v1"
REQUEST_SCHEMA = "ai-sdlc-capability-request/v1"
RESULT_SCHEMA = "ai-sdlc-capability-negotiation/v1"
ADAPTER_FIELDS = {"schema", "id", "version", "host", "harness_api", "capabilities", "operations", "limits"}
REQUEST_FIELDS = {"schema", "operations", "capabilities", "concurrency", "isolation_required"}
OPERATION_FIELDS = {"portable", "host_operation", "semantics"}
NAME = re.compile(r"^[a-z][a-z0-9_-]*(?:\.[a-z][a-z0-9_-]*)*$")

FALLBACKS = {
    "task.parallel": {"requires_operation": "task.execute", "operation": "task.execute", "strategy": "sequential-wave"},
    "hook.lifecycle": {"requires_operation": "task.execute", "operation": "task.execute", "strategy": "explicit-hook-step"},
    "approval.request": {"requires_operation": "user.prompt", "operation": "user.prompt", "strategy": "manual-approval-gate"},
}


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


def semver(value: Any) -> tuple[int, int, int] | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        return None
    return tuple(int(item) for item in value.split("."))


def names(value: Any, field: str, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value) or not all(isinstance(item, str) and NAME.fullmatch(item) for item in value):
        return [f"{field} must be a{' non-empty' if not allow_empty else ''} valid identifier array"]
    return [f"{field} must be unique"] if len(value) != len(set(value)) else []


def validate_adapter(value: Any) -> list[str]:
    if not isinstance(value, dict) or set(value) != ADAPTER_FIELDS:
        return [f"adapter fields must match {ADAPTER_SCHEMA}"]
    errors: list[str] = []
    if value["schema"] != ADAPTER_SCHEMA:
        errors.append(f"schema must be {ADAPTER_SCHEMA}")
    if not isinstance(value["id"], str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value["id"]):
        errors.append("adapter id is invalid")
    if semver(value["version"]) is None:
        errors.append("adapter version must use x.y.z")
    if not isinstance(value["host"], str) or not value["host"].strip():
        errors.append("host is required")
    api = value["harness_api"]
    if not isinstance(api, dict) or set(api) != {"min", "max_exclusive"} or semver(api.get("min")) is None or semver(api.get("max_exclusive")) is None:
        errors.append("harness_api range is invalid")
    elif semver(api["min"]) >= semver(api["max_exclusive"]):
        errors.append("harness_api range is empty")
    errors.extend(names(value["capabilities"], "capabilities"))
    if not isinstance(value["operations"], list):
        errors.append("operations must be an array")
    else:
        portable: list[str] = []
        for index, operation in enumerate(value["operations"]):
            if not isinstance(operation, dict) or set(operation) != OPERATION_FIELDS:
                errors.append(f"operation {index} fields are invalid")
                continue
            portable.append(operation["portable"] if isinstance(operation["portable"], str) else "")
            if not all(isinstance(operation[field], str) and NAME.fullmatch(operation[field]) for field in ("portable", "host_operation")):
                errors.append(f"operation {index} identifiers are invalid")
            if operation["semantics"] != "equivalent":
                errors.append(f"operation {index} semantics must be equivalent")
        if len(portable) != len(set(portable)):
            errors.append("portable operation mappings must be unique")
    limits = value["limits"]
    if not isinstance(limits, dict) or set(limits) != {"max_concurrency", "isolation"} or not isinstance(limits.get("max_concurrency"), int) or isinstance(limits.get("max_concurrency"), bool) or not 1 <= limits.get("max_concurrency", 0) <= 64 or not isinstance(limits.get("isolation"), bool):
        errors.append("limits are invalid")
    return errors


def validate_request(value: Any) -> list[str]:
    if not isinstance(value, dict) or set(value) != REQUEST_FIELDS:
        return [f"request fields must match {REQUEST_SCHEMA}"]
    errors: list[str] = []
    if value["schema"] != REQUEST_SCHEMA:
        errors.append(f"request schema must be {REQUEST_SCHEMA}")
    errors.extend(names(value["operations"], "request operations", False))
    errors.extend(names(value["capabilities"], "request capabilities"))
    if not isinstance(value["concurrency"], int) or isinstance(value["concurrency"], bool) or not 1 <= value["concurrency"] <= 64:
        errors.append("request concurrency must be 1..64")
    if not isinstance(value["isolation_required"], bool):
        errors.append("request isolation_required must be boolean")
    return errors


def negotiate(adapter: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    native = {item["portable"]: item for item in adapter["operations"]}
    mappings: list[dict[str, str]] = []
    unsupported: list[str] = []
    fallbacks: list[dict[str, str]] = []
    for operation in request["operations"]:
        if operation in native:
            mappings.append({"portable": operation, "host_operation": native[operation]["host_operation"], "mode": "native", "strategy": "equivalent"})
            continue
        fallback = FALLBACKS.get(operation)
        if fallback and fallback["requires_operation"] in native:
            host_operation = native[fallback["operation"]]["host_operation"]
            mappings.append({"portable": operation, "host_operation": host_operation, "mode": "fallback", "strategy": fallback["strategy"]})
            fallbacks.append({"subject": operation, "reason": f"fallback:{fallback['strategy']}"})
        else:
            unsupported.append(operation)
    missing = sorted(set(request["capabilities"]) - set(adapter["capabilities"]))
    effective_concurrency = min(request["concurrency"], adapter["limits"]["max_concurrency"])
    isolation = adapter["limits"]["isolation"]
    if effective_concurrency < request["concurrency"]:
        fallbacks.append({"subject": "concurrency", "reason": "host-concurrency-clamped"})
    if request["isolation_required"] and not isolation:
        effective_concurrency = 1
        fallbacks.append({"subject": "isolation", "reason": "sequential-isolation-fallback"})
    reasons = [f"unsupported-operation:{item}" for item in unsupported] + [f"missing-capability:{item}" for item in missing]
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "adapter": {"id": adapter["id"], "version": adapter["version"], "host": adapter["host"], "fingerprint": digest(adapter)},
        "request_fingerprint": digest(request),
        "compatible": not unsupported and not missing,
        "mappings": mappings,
        "unsupported_operations": unsupported,
        "missing_capabilities": missing,
        "fallbacks": fallbacks,
        "limits": {"requested_concurrency": request["concurrency"], "effective_concurrency": effective_concurrency, "isolation_requested": request["isolation_required"], "isolation_native": isolation},
        "reason_codes": reasons or (["compatible-with-fallbacks"] if fallbacks else ["compatible-native"]),
    }
    result["fingerprint"] = digest(result)
    return result


def markdown(value: dict[str, Any]) -> str:
    lines = ["# Host Capability Negotiation", "", f"Adapter: `{value['adapter']['id']}@{value['adapter']['version']}`", f"Compatible: **{str(value['compatible']).lower()}**", f"Fingerprint: `{value['fingerprint']}`", "", "## Mappings", ""]
    lines.extend(f"- `{item['portable']}` -> `{item['host_operation']}` ({item['mode']}: {item['strategy']})" for item in value["mappings"])
    lines.extend(["", "## Reasons", ""])
    lines.extend(f"- `{item}`" for item in value["reason_codes"])
    return "\n".join(lines) + "\n"


def load(path: Path, label: str) -> tuple[Any, str | None]:
    try:
        return json.loads(path.resolve().read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as exc:
        return {}, f"cannot read {label}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--adapter", type=Path, required=True)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--validate", action="store_true")
    actions.add_argument("--negotiate", action="store_true")
    parser.add_argument("--request", type=Path)
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
        print("ERROR: adapter negotiation cannot mutate feature lifecycle state")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir():
        print("ERROR: repository does not exist")
        return 1
    adapter, error = load(args.adapter, "adapter")
    errors = [error] if error else validate_adapter(adapter)
    if args.negotiate and args.request is None:
        errors.append("--request is required for negotiation")
    request: Any = {}
    if args.request:
        request, error = load(args.request, "request")
        errors.extend([error] if error else validate_request(request))
    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        return 1
    if args.validate:
        value = {"schema": RESULT_SCHEMA, "adapter": {"id": adapter["id"], "version": adapter["version"], "host": adapter["host"], "fingerprint": digest(adapter)}, "valid": True}
        value["fingerprint"] = digest(value)
    else:
        value = negotiate(adapter, request)
    if args.write and args.negotiate:
        output = repository / f"_ai_sdlc/adapters/{adapter['id']}/negotiation.json"
        atomic_write(output, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        atomic_write(output.with_suffix(".toon"), encode_toon(value))
        atomic_write(output.with_suffix(".md"), markdown(value))
    if args.format == "json":
        print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))
    elif args.format == "markdown" and args.negotiate:
        print(markdown(value), end="")
    else:
        print(encode_toon(value), end="")
    return 0 if args.validate or value["compatible"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
