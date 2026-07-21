#!/usr/bin/env python3
"""Run a bounded, journaled, resumable task state machine."""

from __future__ import annotations

import argparse
import copy
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
from ai_sdlc_safe_io import bounded_path, ensure_directory


PLAN_SCHEMA = "ai-sdlc-run-plan/v1"
EVENT_SCHEMA = "ai-sdlc-run-event/v1"
STATE_SCHEMA = "ai-sdlc-run-state/v1"
RESULT_SCHEMA = "ai-sdlc-runtime-result/v1"
PLAN_FIELDS = {"schema", "id", "version", "budgets", "tasks"}
TASK_FIELDS = {"id", "depends_on", "action", "input_fingerprint", "max_attempts", "commit_boundary"}
BUDGET_FIELDS = {"max_steps", "max_failures", "max_tokens"}
EVENT_FIELDS = {"schema", "seq", "type", "payload", "previous", "fingerprint"}
ZERO_HASH = "0" * 64


def canonical(value: Any) -> str:
    """Serialize normalized JSON for deterministic hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    """Return SHA-256 for text or normalized data."""
    if not isinstance(value, str):
        value = canonical(value)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def valid_hash(value: Any) -> bool:
    """Return whether a value is one canonical SHA-256 identity."""
    return isinstance(value, str) and bool(re.fullmatch(r"[a-f0-9]{64}", value))


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    """Atomically replace one state projection."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_text(path: Path, content: str) -> None:
    """Atomically replace one compact text projection."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def render_state_toon(state: dict[str, Any]) -> str:
    """Render the complete token-efficient agent-facing state projection."""
    return encode_toon(state)


def persist_state(run_dir: Path, state: dict[str, Any]) -> None:
    """Write exact recovery and complete agent projections."""
    atomic_json(run_dir / "state.json", state)
    atomic_text(run_dir / "state.toon", render_state_toon(state))


class RunLock:
    """Fail fast when another process is mutating the same run."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.descriptor: int | None = None

    def __enter__(self) -> "RunLock":
        try:
            self.descriptor = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise ValueError("run is locked by another mutation") from exc
        os.write(self.descriptor, str(os.getpid()).encode("ascii"))
        return self

    def __exit__(self, *_: object) -> None:
        if self.descriptor is not None:
            os.close(self.descriptor)
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def validate_plan(value: Any) -> tuple[dict[str, Any], list[str]]:
    """Validate and normalize an immutable acyclic run plan."""
    errors: list[str] = []
    if not isinstance(value, dict) or set(value) != PLAN_FIELDS:
        return {}, [f"plan fields must match {PLAN_SCHEMA}"]
    if value.get("schema") != PLAN_SCHEMA:
        errors.append(f"plan schema must be {PLAN_SCHEMA}")
    if not isinstance(value.get("id"), str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value["id"]):
        errors.append("plan id is invalid")
    if not isinstance(value.get("version"), str) or not re.fullmatch(r"\d+\.\d+\.\d+", value["version"]):
        errors.append("plan version must use x.y.z")
    budgets = value.get("budgets")
    if not isinstance(budgets, dict) or set(budgets) != BUDGET_FIELDS:
        errors.append("plan budgets must contain max_steps, max_failures, and max_tokens")
    elif not all(isinstance(budgets[key], int) and not isinstance(budgets[key], bool) and budgets[key] > 0 for key in BUDGET_FIELDS):
        errors.append("all plan budgets must be positive integers")
    tasks = value.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        errors.append("plan tasks must be a non-empty array")
        tasks = []
    ids: list[str] = []
    for index, task in enumerate(tasks):
        prefix = f"task {index}"
        if not isinstance(task, dict) or set(task) != TASK_FIELDS:
            errors.append(f"{prefix} fields are invalid")
            continue
        if not isinstance(task["id"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", task["id"]):
            errors.append(f"{prefix} id is invalid")
        else:
            ids.append(task["id"])
        if not isinstance(task["depends_on"], list) or not all(isinstance(item, str) for item in task["depends_on"]) or len(task["depends_on"]) != len(set(task["depends_on"])):
            errors.append(f"{prefix} dependencies must be a unique string array")
        if not isinstance(task["action"], str) or not task["action"]:
            errors.append(f"{prefix} action is required")
        if not valid_hash(task["input_fingerprint"]):
            errors.append(f"{prefix} input_fingerprint is invalid")
        if not isinstance(task["max_attempts"], int) or isinstance(task["max_attempts"], bool) or task["max_attempts"] < 1:
            errors.append(f"{prefix} max_attempts must be positive")
        if not isinstance(task["commit_boundary"], bool):
            errors.append(f"{prefix} commit_boundary must be boolean")
    if len(ids) != len(set(ids)):
        errors.append("plan task ids must be unique")
    known = set(ids)
    for task in tasks:
        if isinstance(task, dict) and isinstance(task.get("depends_on"), list):
            unknown = sorted(set(task["depends_on"]) - known)
            if unknown:
                errors.append(f"task {task.get('id')} has unknown dependencies: {', '.join(unknown)}")
            if task.get("id") in task["depends_on"]:
                errors.append(f"task {task.get('id')} depends on itself")
    graph = {task["id"]: list(task["depends_on"]) for task in tasks if isinstance(task, dict) and task.get("id") in known}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str, trail: list[str]) -> None:
        if task_id in visiting:
            start = trail.index(task_id)
            errors.append("plan dependency cycle: " + " -> ".join(trail[start:] + [task_id]))
            return
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in graph.get(task_id, []):
            if dependency in graph:
                visit(dependency, trail + [task_id])
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in ids:
        visit(task_id, [])
    normalized = {"schema": PLAN_SCHEMA, "id": value.get("id"), "version": value.get("version"), "budgets": {key: budgets.get(key) for key in sorted(BUDGET_FIELDS)} if isinstance(budgets, dict) else {}, "tasks": [{key: task[key] for key in sorted(TASK_FIELDS)} for task in tasks if isinstance(task, dict) and set(task) == TASK_FIELDS]}
    return normalized, sorted(set(errors))


def task_row(state: dict[str, Any], task_id: str) -> dict[str, Any] | None:
    """Find one mutable state task row."""
    return next((task for task in state["tasks"] if task["id"] == task_id), None)


def ready_tasks(state: dict[str, Any]) -> list[str]:
    """Return dependency-ready pending tasks in plan order."""
    statuses = {task["id"]: task["status"] for task in state["tasks"]}
    return [task["id"] for task in state["tasks"] if task["status"] == "pending" and task["attempts"] < task["max_attempts"] and all(statuses.get(dependency) == "succeeded" for dependency in task["depends_on"])]


def finish_state(state: dict[str, Any], sequence: int) -> dict[str, Any]:
    """Refresh derived fields and state fingerprint."""
    state["sequence"] = sequence
    state["ready_tasks"] = ready_tasks(state) if state["status"] == "running" and not state["running_task"] else []
    state.pop("fingerprint", None)
    state["fingerprint"] = digest(state)
    return state


def initial_state(payload: dict[str, Any]) -> dict[str, Any]:
    """Create summarized state from the run-started payload."""
    plan = payload["plan"]
    tasks = [{"id": item["id"], "action": item["action"], "depends_on": item["depends_on"], "input_fingerprint": item["input_fingerprint"], "max_attempts": item["max_attempts"], "commit_boundary": item["commit_boundary"], "status": "pending", "attempts": 0, "result_fingerprint": "", "commit": "", "tokens": 0, "last_reason": "", "last_record": {}} for item in plan["tasks"]]
    return {"schema": STATE_SCHEMA, "run_id": payload["run_id"], "plan": {"id": plan["id"], "version": plan["version"], "path": payload["plan_path"], "sha256": payload["plan_sha256"], "fingerprint": digest(plan)}, "status": "running", "sequence": 1, "running_task": "", "ready_tasks": [], "tasks": tasks, "budgets": {"max_steps": plan["budgets"]["max_steps"], "max_failures": plan["budgets"]["max_failures"], "max_tokens": plan["budgets"]["max_tokens"], "used_steps": 0, "used_failures": 0, "used_tokens": 0}, "stop_reason": "", "fingerprint": ""}


def apply_event(previous_state: dict[str, Any] | None, event: dict[str, Any]) -> dict[str, Any]:
    """Apply one already hash-validated journal transition."""
    event_type = event["type"]
    payload = event["payload"]
    if event_type == "run-started":
        if previous_state is not None or event["seq"] != 1:
            raise ValueError("run-started must be the first event")
        return finish_state(initial_state(payload), event["seq"])
    if previous_state is None:
        raise ValueError("journal does not start with run-started")
    state = copy.deepcopy(previous_state)
    if state["status"] in {"completed", "stopped"}:
        raise ValueError(f"event {event_type} cannot follow terminal state {state['status']}")
    task_id = payload.get("task_id", "")
    task = task_row(state, task_id) if task_id else None
    if event_type == "task-started":
        if state["status"] != "running" or state["running_task"]:
            raise ValueError("task-started requires an idle running run")
        if task is None or task_id not in ready_tasks(state):
            raise ValueError(f"task {task_id} is not ready")
        task["status"] = "running"
        task["attempts"] += 1
        state["running_task"] = task_id
        state["budgets"]["used_steps"] += 1
    elif event_type in {"task-succeeded", "task-failed", "task-blocked"}:
        if task is None or state["running_task"] != task_id or task["status"] != "running":
            raise ValueError(f"task {task_id} is not the running task")
        tokens = payload.get("tokens")
        if not isinstance(tokens, int) or isinstance(tokens, bool) or tokens < 0:
            raise ValueError("recorded tokens must be a non-negative integer")
        task["tokens"] += tokens
        state["budgets"]["used_tokens"] += tokens
        state["running_task"] = ""
        task["last_record"] = {key: payload.get(key, "") for key in ("outcome", "result_fingerprint", "tokens", "commit", "reason")}
        if event_type == "task-succeeded":
            result = payload.get("result_fingerprint")
            commit = payload.get("commit", "")
            if not valid_hash(result):
                raise ValueError("success result_fingerprint is invalid")
            if task["commit_boundary"] and not re.fullmatch(r"[a-f0-9]{7,40}", commit):
                raise ValueError("commit-boundary success requires commit evidence")
            task["status"] = "succeeded"
            task["result_fingerprint"] = result
            task["commit"] = commit
            task["last_reason"] = ""
            if all(item["status"] == "succeeded" for item in state["tasks"]):
                state["status"] = "completed"
                state["stop_reason"] = "all-tasks-succeeded"
            elif state["budgets"]["used_tokens"] >= state["budgets"]["max_tokens"]:
                state["status"] = "paused"
                state["stop_reason"] = "token-budget-exhausted"
        elif event_type == "task-failed":
            reason = payload.get("reason", "")
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError("failed outcome requires reason")
            state["budgets"]["used_failures"] += 1
            task["last_reason"] = reason
            if state["budgets"]["used_failures"] >= state["budgets"]["max_failures"]:
                task["status"] = "failed"
                state["status"] = "paused"
                state["stop_reason"] = "failure-budget-exhausted"
            elif state["budgets"]["used_tokens"] >= state["budgets"]["max_tokens"]:
                task["status"] = "failed"
                state["status"] = "paused"
                state["stop_reason"] = "token-budget-exhausted"
            elif task["attempts"] >= task["max_attempts"]:
                task["status"] = "failed"
                state["status"] = "paused"
                state["stop_reason"] = f"retry-exhausted:{task_id}"
            else:
                task["status"] = "pending"
        else:
            reason = payload.get("reason", "")
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError("blocked outcome requires reason")
            task["status"] = "blocked"
            task["last_reason"] = reason
            state["status"] = "paused"
            state["stop_reason"] = f"task-blocked:{task_id}:{reason}"
    elif event_type == "task-retry-requested":
        if task is None or task["status"] not in {"blocked", "failed"}:
            raise ValueError(f"task {task_id} is not retryable from {task['status'] if task else 'missing'}")
        if task["attempts"] >= task["max_attempts"]:
            raise ValueError(f"task {task_id} exhausted attempts")
        if state["budgets"]["used_steps"] >= state["budgets"]["max_steps"] or state["budgets"]["used_failures"] >= state["budgets"]["max_failures"] or state["budgets"]["used_tokens"] >= state["budgets"]["max_tokens"]:
            raise ValueError("run budgets do not permit retry")
        task["status"] = "pending"
        task["last_reason"] = payload.get("reason", "")
        state["status"] = "running"
        state["stop_reason"] = ""
    elif event_type == "run-stopped":
        reason = payload.get("reason", "")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("run-stopped requires reason")
        state["status"] = "stopped"
        state["stop_reason"] = f"manual:{reason}"
    elif event_type == "run-paused":
        reason = payload.get("reason", "")
        if reason not in {"step-budget-exhausted", "dependency-blocked"}:
            raise ValueError("run-paused reason is invalid")
        state["status"] = "paused"
        state["stop_reason"] = reason
    else:
        raise ValueError(f"unknown event type: {event_type}")
    return finish_state(state, event["seq"])


def read_journal(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Load and hash-check an append-only journal."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [], [f"cannot read journal: {exc}"]
    events: list[dict[str, Any]] = []
    errors: list[str] = []
    previous = ZERO_HASH
    for index, line in enumerate(lines, 1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"journal line {index} is invalid JSON: {exc}")
            continue
        if not isinstance(event, dict) or set(event) != EVENT_FIELDS:
            errors.append(f"journal line {index} fields are invalid")
            continue
        fingerprint = event.get("fingerprint")
        body = dict(event)
        body.pop("fingerprint", None)
        if event.get("schema") != EVENT_SCHEMA or event.get("seq") != index or event.get("previous") != previous or not valid_hash(fingerprint) or digest(body) != fingerprint:
            errors.append(f"journal line {index} sequence or hash chain is invalid")
        previous = fingerprint if isinstance(fingerprint, str) else previous
        events.append(event)
    return events, errors


def replay(events: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    """Replay validated events into summarized state."""
    state: dict[str, Any] | None = None
    errors: list[str] = []
    for event in events:
        try:
            state = apply_event(state, event)
        except ValueError as exc:
            errors.append(f"journal event {event.get('seq')}: {exc}")
            break
    return state or {}, errors


def load_run(run_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]], bool, list[str]]:
    """Replay journal and compare saved state projection."""
    events, errors = read_journal(run_dir / "journal.jsonl")
    state, replay_errors = replay(events)
    errors.extend(replay_errors)
    saved: Any = None
    try:
        saved = json.loads((run_dir / "state.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        pass
    try:
        saved_toon = (run_dir / "state.toon").read_text(encoding="utf-8")
    except OSError:
        saved_toon = ""
    recovered = saved != state or saved_toon != render_state_toon(state)
    return state, events, recovered, errors


def new_event(events: list[dict[str, Any]], event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Create one hash-chained transition event."""
    event: dict[str, Any] = {"schema": EVENT_SCHEMA, "seq": len(events) + 1, "type": event_type, "payload": payload, "previous": events[-1]["fingerprint"] if events else ZERO_HASH}
    event["fingerprint"] = digest(event)
    return event


def persist_event(run_dir: Path, events: list[dict[str, Any]], state: dict[str, Any], event_type: str, payload: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Append and fsync journal before atomically replacing state."""
    event = new_event(events, event_type, payload)
    next_state = apply_event(state if events else None, event)
    with (run_dir / "journal.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(canonical(event) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    persist_state(run_dir, next_state)
    return next_state, [*events, event]


def result(operation: str, state: dict[str, Any], recovered: bool = False, idempotent: bool = False) -> dict[str, Any]:
    """Wrap state with operation evidence."""
    return {
        "schema": RESULT_SCHEMA,
        "operation": operation,
        "recovered": recovered,
        "idempotent": idempotent,
        "evidence_trust": "local-structural-not-authenticated",
        "state": state,
    }


def main() -> int:
    """Start, advance, record, recover, retry, inspect, or stop a run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--start", action="store_true")
    actions.add_argument("--next", action="store_true")
    actions.add_argument("--record", action="store_true")
    actions.add_argument("--resume", action="store_true")
    actions.add_argument("--status", action="store_true")
    actions.add_argument("--retry")
    actions.add_argument("--stop", action="store_true")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--task")
    parser.add_argument("--outcome", choices=("succeeded", "failed", "blocked"))
    parser.add_argument("--result-fingerprint", default="")
    parser.add_argument("--tokens", type=int, default=0)
    parser.add_argument("--commit", default="")
    parser.add_argument("--reason", default="")
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
        print("ERROR: runtime cannot mutate feature lifecycle state")
        return 1
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.run_id):
        print("ERROR: run id is unsafe")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir():
        print(f"ERROR: repository does not exist: {repository}")
        return 1
    try:
        runs_root = bounded_path(repository, repository / "_ai_sdlc/runs")
        run_dir = bounded_path(repository, runs_root / args.run_id)
        if args.start:
            if args.plan is None:
                raise ValueError("--plan is required for --start")
            try:
                raw = args.plan.resolve().read_text(encoding="utf-8")
                source_plan = json.loads(raw)
            except (OSError, json.JSONDecodeError) as exc:
                raise ValueError(f"cannot read plan: {exc}") from exc
            plan, errors = validate_plan(source_plan)
            if errors:
                raise ValueError("; ".join(errors))
            ensure_directory(repository, runs_root)
            try:
                run_dir.mkdir()
            except FileExistsError as exc:
                raise ValueError("run already exists") from exc
            try:
                plan_path = args.plan.resolve().relative_to(repository).as_posix()
            except ValueError:
                plan_path = args.plan.resolve().as_posix()
            payload = {"run_id": args.run_id, "plan": plan, "plan_path": plan_path, "plan_sha256": digest(raw)}
            state, events = persist_event(run_dir, [], {}, "run-started", payload)
            output = result("start", state)
        else:
            for name in ("journal.jsonl", "state.json", "state.toon", ".lock"):
                bounded_path(repository, run_dir / name)
            if not run_dir.is_dir() or run_dir.is_symlink():
                raise ValueError("run does not exist or is unsafe")
            if args.status:
                state, _, recovered, errors = load_run(run_dir)
                if errors:
                    raise ValueError("; ".join(errors))
                output = result("status", state, recovered)
            else:
                with RunLock(run_dir / ".lock"):
                    state, events, recovered, errors = load_run(run_dir)
                    if errors:
                        raise ValueError("; ".join(errors))
                    if recovered:
                        persist_state(run_dir, state)
                    if args.resume:
                        output = result("resume", state, recovered)
                    elif args.next:
                        if state["status"] != "running":
                            raise ValueError(f"run is not running: {state['status']} ({state['stop_reason']})")
                        if state["running_task"]:
                            output = result("next", state, recovered, True)
                        else:
                            if state["budgets"]["used_steps"] >= state["budgets"]["max_steps"]:
                                state, events = persist_event(run_dir, events, state, "run-paused", {"reason": "step-budget-exhausted"})
                                output = result("next", state, recovered)
                            elif not state["ready_tasks"]:
                                state, events = persist_event(run_dir, events, state, "run-paused", {"reason": "dependency-blocked"})
                                output = result("next", state, recovered)
                            else:
                                state, events = persist_event(run_dir, events, state, "task-started", {"task_id": state["ready_tasks"][0]})
                                output = result("next", state, recovered)
                    elif args.record:
                        if not args.task or not args.outcome:
                            raise ValueError("--task and --outcome are required for --record")
                        task = task_row(state, args.task)
                        if task is None:
                            raise ValueError(f"unknown task: {args.task}")
                        record = {"outcome": args.outcome, "result_fingerprint": args.result_fingerprint, "tokens": args.tokens, "commit": args.commit, "reason": args.reason}
                        if task["status"] == "succeeded" and task["last_record"] == record:
                            output = result("record", state, recovered, True)
                        elif task["status"] != "running" or state["running_task"] != args.task:
                            if task["last_record"] == record:
                                output = result("record", state, recovered, True)
                            else:
                                raise ValueError(f"task {args.task} is not running")
                        else:
                            event_type = {"succeeded": "task-succeeded", "failed": "task-failed", "blocked": "task-blocked"}[args.outcome]
                            state, events = persist_event(run_dir, events, state, event_type, {"task_id": args.task, **record})
                            output = result("record", state, recovered)
                    elif args.retry:
                        if not args.reason.strip():
                            raise ValueError("--retry requires --reason")
                        state, events = persist_event(run_dir, events, state, "task-retry-requested", {"task_id": args.retry, "reason": args.reason})
                        output = result("retry", state, recovered)
                    elif args.stop:
                        if not args.reason.strip():
                            raise ValueError("--stop requires --reason")
                        state, events = persist_event(run_dir, events, state, "run-stopped", {"reason": args.reason})
                        output = result("stop", state, recovered)
                    else:
                        raise ValueError("unsupported runtime action")
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    if args.format == "json":
        print(json.dumps(output, indent=2, sort_keys=True, ensure_ascii=False))
    elif args.format == "toon":
        print(encode_toon(output), end="")
    else:
        state = output["state"]
        print("# Runtime State\n")
        print(f"- Run: `{state['run_id']}`")
        print(f"- Status: `{state['status']}`")
        print(f"- Sequence: {state['sequence']}")
        print(f"- Running task: `{state['running_task'] or 'none'}`")
        print(f"- Ready: `{', '.join(state['ready_tasks']) or 'none'}`")
        print(f"- Stop reason: `{state['stop_reason'] or 'none'}`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
