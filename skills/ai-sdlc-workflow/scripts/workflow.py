#!/usr/bin/env python3
"""Validate and plan declarative, gated, host-safe delivery workflows."""

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

WORKFLOW_SCHEMA = "ai-sdlc-workflow/v1"
PLAN_SCHEMA = "ai-sdlc-workflow-plan/v1"
WORKFLOW_FIELDS = {"schema", "id", "version", "capabilities", "steps", "hooks"}
STEP_FIELDS = {"id", "type", "depends_on", "action", "capabilities", "condition", "isolation", "approval_owner"}
HOOK_FIELDS = {"id", "phase", "target", "action", "capabilities"}
ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
OPERATION = re.compile(r"^[a-z][a-z0-9_-]*(?:\.[a-z][a-z0-9_-]*)+$")


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


def identifier_list(value: Any, field: str, pattern: re.Pattern[str] = OPERATION) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and pattern.fullmatch(item) for item in value):
        return [f"{field} must be an array of valid identifiers"]
    return [f"{field} must be unique"] if len(value) != len(set(value)) else []


def validate_condition(value: Any, prefix: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, dict) or set(value) != {"field", "operator", "value"}:
        return [f"{prefix} condition fields are invalid"]
    errors: list[str] = []
    if not isinstance(value["field"], str) or not re.fullmatch(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*", value["field"]):
        errors.append(f"{prefix} condition field is invalid")
    if value["operator"] not in {"eq", "in", "exists"}:
        errors.append(f"{prefix} condition operator is invalid")
    if value["operator"] == "in" and not isinstance(value["value"], list):
        errors.append(f"{prefix} in condition value must be an array")
    if value["operator"] == "exists" and not isinstance(value["value"], bool):
        errors.append(f"{prefix} exists condition value must be boolean")
    return errors


def find_cycles(steps: list[dict[str, Any]]) -> list[str]:
    graph = {step["id"]: step["depends_on"] for step in steps}
    active: list[str] = []
    done: set[str] = set()
    found: set[str] = set()

    def visit(node: str) -> None:
        if node in done:
            return
        if node in active:
            found.add(" -> ".join(active[active.index(node):] + [node]))
            return
        active.append(node)
        for dependency in graph[node]:
            visit(dependency)
        active.pop()
        done.add(node)

    for node in graph:
        visit(node)
    return sorted(found)


def validate_workflow(value: Any) -> list[str]:
    if not isinstance(value, dict) or set(value) != WORKFLOW_FIELDS:
        return [f"workflow fields must match {WORKFLOW_SCHEMA}"]
    errors: list[str] = []
    if value["schema"] != WORKFLOW_SCHEMA:
        errors.append(f"schema must be {WORKFLOW_SCHEMA}")
    if not isinstance(value["id"], str) or not ID.fullmatch(value["id"]):
        errors.append("workflow id is invalid")
    if not isinstance(value["version"], str) or not re.fullmatch(r"\d+\.\d+\.\d+", value["version"]):
        errors.append("workflow version must use x.y.z")
    errors.extend(identifier_list(value["capabilities"], "workflow capabilities"))
    declared = set(value["capabilities"]) if isinstance(value["capabilities"], list) else set()
    if not isinstance(value["steps"], list) or not value["steps"]:
        return errors + ["steps must be a non-empty array"]
    ids: list[str] = []
    valid_steps: list[dict[str, Any]] = []
    for index, step in enumerate(value["steps"]):
        prefix = f"step {index}"
        if not isinstance(step, dict) or set(step) != STEP_FIELDS:
            errors.append(f"{prefix} fields are invalid")
            continue
        valid_steps.append(step)
        ids.append(step["id"] if isinstance(step["id"], str) else "")
        if not isinstance(step["id"], str) or not ID.fullmatch(step["id"]):
            errors.append(f"{prefix} id is invalid")
        if step["type"] not in {"task", "validation", "approval", "decision"}:
            errors.append(f"{prefix} type is invalid")
        if not isinstance(step["action"], str) or not OPERATION.fullmatch(step["action"]):
            errors.append(f"{prefix} action is invalid")
        errors.extend(identifier_list(step["depends_on"], f"{prefix} dependencies", ID))
        errors.extend(identifier_list(step["capabilities"], f"{prefix} capabilities"))
        undeclared = sorted(set(step["capabilities"]) - declared) if isinstance(step["capabilities"], list) else []
        if undeclared:
            errors.append(f"{prefix} uses undeclared capabilities: {', '.join(undeclared)}")
        errors.extend(validate_condition(step["condition"], prefix))
        if step["isolation"] not in {"none", "workspace"}:
            errors.append(f"{prefix} isolation is invalid")
        if step["type"] == "approval" and (not isinstance(step["approval_owner"], str) or not step["approval_owner"].strip()):
            errors.append(f"{prefix} approval owner is required")
        if step["type"] != "approval" and step["approval_owner"] != "":
            errors.append(f"{prefix} approval owner is only valid for approval steps")
    if len(ids) != len(set(ids)):
        errors.append("step ids must be unique")
    known = set(ids)
    for step in valid_steps:
        missing = sorted(set(step["depends_on"]) - known)
        if missing:
            errors.append(f"step {step['id']} has unknown dependencies: {', '.join(missing)}")
        if step["id"] in step["depends_on"]:
            errors.append(f"step {step['id']} depends on itself")
    if not errors:
        errors.extend(f"dependency cycle: {cycle}" for cycle in find_cycles(valid_steps))
    if not isinstance(value["hooks"], list):
        return errors + ["hooks must be an array"]
    hook_ids: list[str] = []
    for index, hook in enumerate(value["hooks"]):
        prefix = f"hook {index}"
        if not isinstance(hook, dict) or set(hook) != HOOK_FIELDS:
            errors.append(f"{prefix} fields are invalid")
            continue
        hook_ids.append(hook["id"] if isinstance(hook["id"], str) else "")
        if not isinstance(hook["id"], str) or not ID.fullmatch(hook["id"]):
            errors.append(f"{prefix} id is invalid")
        if hook["phase"] not in {"before", "after", "on_failure"}:
            errors.append(f"{prefix} phase is invalid")
        if hook["target"] not in known:
            errors.append(f"{prefix} target is unknown")
        if not isinstance(hook["action"], str) or not OPERATION.fullmatch(hook["action"]):
            errors.append(f"{prefix} action is invalid")
        errors.extend(identifier_list(hook["capabilities"], f"{prefix} capabilities"))
        undeclared = sorted(set(hook["capabilities"]) - declared) if isinstance(hook["capabilities"], list) else []
        if undeclared:
            errors.append(f"{prefix} uses undeclared capabilities: {', '.join(undeclared)}")
    if len(hook_ids) != len(set(hook_ids)):
        errors.append("hook ids must be unique")
    return errors


def get_field(context: dict[str, Any], field: str) -> tuple[Any, bool]:
    current: Any = context
    for part in field.split("."):
        if not isinstance(current, dict) or part not in current:
            return None, False
        current = current[part]
    return current, True


def condition_status(condition: dict[str, Any] | None, context: dict[str, Any] | None) -> tuple[str, str]:
    if condition is None:
        return "eligible", "unconditional"
    if context is None:
        return "deferred", "condition-context-missing"
    actual, exists = get_field(context, condition["field"])
    operator, expected = condition["operator"], condition["value"]
    matched = exists is expected if operator == "exists" else exists and (actual == expected if operator == "eq" else actual in expected)
    return ("eligible", "condition-matched") if matched else ("skipped", "condition-not-matched")


def dependency_waves(steps: list[dict[str, Any]], statuses: dict[str, str]) -> list[list[str]]:
    pending = {step["id"] for step in steps if statuses[step["id"]] == "eligible"}
    completed = {step["id"] for step in steps if statuses[step["id"]] == "skipped"}
    order = {step["id"]: index for index, step in enumerate(steps)}
    by_id = {step["id"]: step for step in steps}
    waves: list[list[str]] = []
    while pending:
        ready = sorted((item for item in pending if set(by_id[item]["depends_on"]) <= completed), key=lambda item: (order[item], item))
        if not ready:
            break
        waves.append(ready)
        pending -= set(ready)
        completed |= set(ready)
    return waves


def plan_workflow(workflow: dict[str, Any], context: dict[str, Any] | None, concurrency: int, isolation_supported: bool) -> dict[str, Any]:
    decisions: list[dict[str, str]] = []
    statuses: dict[str, str] = {}
    for step in workflow["steps"]:
        status, reason = condition_status(step["condition"], context)
        statuses[step["id"]] = status
        decisions.append({"id": step["id"], "type": step["type"], "status": status, "reason": reason})
    by_id = {step["id"]: step for step in workflow["steps"]}
    waves: list[dict[str, Any]] = []
    fallbacks: list[dict[str, str]] = []
    for candidate in dependency_waves(workflow["steps"], statuses):
        safe = all(by_id[item]["type"] in {"task", "validation"} and by_id[item]["isolation"] == "workspace" for item in candidate)
        parallel = len(candidate) > 1 and concurrency > 1 and isolation_supported and safe
        if len(candidate) > 1 and not parallel:
            reason = "host-concurrency-unavailable" if concurrency <= 1 else "host-isolation-unavailable" if not isolation_supported else "wave-contains-exclusive-or-unisolated-step"
            fallbacks.append({"candidate": "/".join(candidate), "reason": reason})
            for item in candidate:
                waves.append({"index": len(waves) + 1, "mode": "sequential", "steps": [item]})
        else:
            waves.append({"index": len(waves) + 1, "mode": "parallel" if parallel else "sequential", "steps": candidate})
    plan: dict[str, Any] = {
        "schema": PLAN_SCHEMA,
        "workflow": {"id": workflow["id"], "version": workflow["version"], "fingerprint": digest(workflow)},
        "host": {"concurrency": concurrency, "isolation_supported": isolation_supported},
        "step_decisions": decisions,
        "waves": waves,
        "gates": [{"step": step["id"], "owner": step["approval_owner"], "action": step["action"], "status": "required"} for step in workflow["steps"] if step["type"] == "approval" and statuses[step["id"]] == "eligible"],
        "hooks": sorted(workflow["hooks"], key=lambda item: (item["target"], item["phase"], item["id"])),
        "fallbacks": fallbacks,
        "executable": not any(item["status"] == "deferred" for item in decisions),
    }
    plan["fingerprint"] = digest(plan)
    return plan


def markdown(plan: dict[str, Any]) -> str:
    lines = ["# Workflow Plan", "", f"Workflow: `{plan['workflow']['id']}@{plan['workflow']['version']}`", f"Fingerprint: `{plan['fingerprint']}`", f"Executable: `{str(plan['executable']).lower()}`", "", "## Waves", ""]
    lines.extend(f"- {wave['index']}. **{wave['mode']}**: {', '.join(f'`{item}`' for item in wave['steps'])}" for wave in plan["waves"])
    lines.extend(["", "## Fallbacks", ""])
    lines.extend(f"- `{item['reason']}`: {item['candidate']}" for item in plan["fallbacks"])
    if not plan["fallbacks"]:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--workflow", type=Path, required=True)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--validate", action="store_true")
    actions.add_argument("--plan", action="store_true")
    parser.add_argument("--context", type=Path)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--isolation-supported", action="store_true")
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
        print("ERROR: workflow planning cannot mutate feature lifecycle state")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir() or not 1 <= args.concurrency <= 64:
        print("ERROR: repository must exist and concurrency must be 1..64")
        return 1
    try:
        workflow = json.loads(args.workflow.resolve().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read workflow: {exc}")
        return 1
    errors = validate_workflow(workflow)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    context: dict[str, Any] | None = None
    if args.context:
        try:
            context = json.loads(args.context.resolve().read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: cannot read context: {exc}")
            return 1
        if not isinstance(context, dict):
            print("ERROR: context must be a JSON object")
            return 1
    plan = plan_workflow(workflow, context, args.concurrency, args.isolation_supported)
    if args.write:
        output = repository / f"_ai_sdlc/workflows/{workflow['id']}/plan.json"
        atomic_write(output, json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        atomic_write(output.with_suffix(".toon"), encode_toon(plan))
        atomic_write(output.with_suffix(".md"), markdown(plan))
    if args.format == "json":
        print(json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False))
    elif args.format == "markdown":
        print(markdown(plan), end="")
    else:
        print(encode_toon(plan), end="")
    return 0 if args.validate or plan["executable"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
