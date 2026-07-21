#!/usr/bin/env python3
"""Execute a reviewed argv-only validation plan and write current evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import re
import subprocess
import sys
import tempfile
import threading
import signal
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_state_machine import add_state_arguments, run_state_action
from ai_sdlc_validation_receipt import (
    RECEIPT_SCHEMA,
    declared_trace_ids,
    receipt_fingerprint,
    revision,
    validate_receipt,
    workspace_fingerprint,
)
from ai_sdlc_safe_io import atomic_write_text, bounded_path

PLAN_SCHEMA = "ai-sdlc-validation-command-plan/v1"
ALLOWED_EXECUTABLES = {"python", "python3", "pytest", "git", "go", "npm"}
READ_ONLY_GIT = {"diff", "status", "rev-parse", "ls-files", "show", "log"}
TRACE_ID = re.compile(r"^(?:REQ|AC|US|TC|TASK|RISK|DEC|EPIC|GOAL|CAP|WF|BR|SC|NFR|DEP)-\d{2,4}$|^T\d{3,4}$", re.IGNORECASE)


def atomic_json(root: Path, path: Path, value: dict[str, Any]) -> None:
    atomic_write_text(root, path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def execute_bounded(argv: list[str], root: Path, timeout: int, limit: int) -> tuple[int, bytes, bytes, int, int, bool]:
    """Drain output while hashing at most limit bytes and terminate the process group on overflow."""
    process = subprocess.Popen(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=os.name != "nt")
    lock = threading.Lock()
    total = 0
    limited = False
    buffers = [bytearray(), bytearray()]
    sizes = [0, 0]

    def terminate() -> None:
        if process.poll() is None:
            try:
                if os.name != "nt":
                    os.killpg(process.pid, signal.SIGKILL)
                else:
                    process.kill()
            except ProcessLookupError:
                # The process may exit between poll() and termination. That is
                # already the desired state, so preserve the timeout/limit
                # result instead of converting the race into runner exit 127.
                pass

    def drain(stream: Any, index: int) -> None:
        nonlocal total, limited
        while True:
            chunk = stream.read(65536)
            if not chunk:
                return
            sizes[index] += len(chunk)
            with lock:
                remaining = max(0, limit - total)
                buffers[index].extend(chunk[:remaining])
                total += len(chunk)
                if total > limit and not limited:
                    limited = True
                    terminate()

    threads = [threading.Thread(target=drain, args=(process.stdout, 0)), threading.Thread(target=drain, args=(process.stderr, 1))]
    for thread in threads:
        thread.start()
    try:
        code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        terminate()
        process.wait()
        code = 124
    if os.name != "nt":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    for thread in threads:
        thread.join()
    if limited:
        code = 125
    return code, bytes(buffers[0]), bytes(buffers[1]), sizes[0], sizes[1], limited


def validate_argv(argv: list[str], root: Path) -> list[str]:
    """Reject command forms that turn one runner approval into arbitrary execution."""
    executable = argv[0]
    if executable != Path(executable).name or executable not in ALLOWED_EXECUTABLES:
        return [f"executable must be an allowed command name, not a path: {executable}"]
    if len(argv) < 2:
        return [f"validation command is incomplete: {executable}"]
    if executable in {"python", "python3"}:
        if argv[1] == "-m":
            if len(argv) < 3 or argv[2] not in {"unittest", "compileall"}:
                return ["Python -m is restricted to unittest or compileall"]
        elif argv[1].startswith("-"):
            return [f"Python execution flag is not allowed: {argv[1]}"]
        else:
            script = (root / argv[1]).resolve() if not Path(argv[1]).is_absolute() else Path(argv[1]).resolve()
            try:
                script.relative_to(root)
            except ValueError:
                return [f"Python script must be inside the validation root: {argv[1]}"]
            if script.suffix != ".py" or not script.is_file():
                return [f"Python script must be an existing repository .py file: {argv[1]}"]
    elif executable == "git" and argv[1] not in READ_ONLY_GIT:
        return [f"Git mutation is not allowed by the validation runner: {argv[1]}"]
    elif executable == "go" and argv[1] not in {"test", "vet"}:
        return [f"Go command is restricted to test or vet: {argv[1]}"]
    elif executable == "npm" and argv[1] not in {"test", "run"}:
        return [f"npm command is restricted to test or run: {argv[1]}"]
    return []


def execution_argv(argv: list[str]) -> list[str]:
    """Resolve approved executable names without honoring a plan-supplied path."""
    if argv[0] in {"python", "python3"}:
        return [sys.executable, *argv[1:]]
    resolved = shutil.which(argv[0])
    if not resolved:
        raise OSError(f"approved executable is unavailable: {argv[0]}")
    return [resolved, *argv[1:]]


def load_plan(path: Path, root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [f"cannot read validation plan: {exc}"]
    if not isinstance(value, dict) or set(value) != {"schema", "commands"} or value.get("schema") != PLAN_SCHEMA:
        return [], [f"plan must contain only schema={PLAN_SCHEMA} and commands"]
    commands = value.get("commands")
    if not isinstance(commands, list) or not commands:
        return [], ["validation plan commands must be a non-empty array"]
    errors: list[str] = []
    ids: list[str] = []
    for index, item in enumerate(commands):
        if not isinstance(item, dict) or set(item) != {"id", "argv", "trace_ids"}:
            errors.append(f"command {index} must contain id, argv, trace_ids")
            continue
        argv = item.get("argv")
        ids.append(str(item.get("id", "")))
        if not isinstance(argv, list) or not argv or not all(isinstance(arg, str) and arg for arg in argv):
            errors.append(f"command {index} argv must be a non-empty string array")
        else:
            errors.extend(f"command {index}: {error}" for error in validate_argv(argv, root))
        trace_ids = item.get("trace_ids")
        if not isinstance(trace_ids, list) or not trace_ids or not all(
            isinstance(ref, str) and TRACE_ID.fullmatch(ref) for ref in trace_ids
        ):
            errors.append(f"command {index} trace_ids must be a non-empty array of canonical IDs")
    if len(ids) != len(set(ids)) or any(not item for item in ids):
        errors.append("command IDs must be unique and non-empty")
    return commands, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--max-output-bytes", type=int, default=10_000_000)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()
    if args.complete_state:
        print(
            "ERROR: run_validation.py cannot complete lifecycle state while it is still executing; "
            "run it successfully, verify the receipt, write validation.md, then use state_machine.py complete"
        )
        return 1
    state_rc = run_state_action(args, "ai-sdlc-validation", "implementation")
    if state_rc:
        return state_rc
    root = args.root.resolve()
    if args.timeout < 1 or args.max_output_bytes < 1:
        print("ERROR: timeout and max-output-bytes must be positive")
        return 1
    try:
        output = bounded_path(root, args.output if args.output.is_absolute() else root / args.output)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    plan = args.plan.resolve()
    expected_plan = output.parent / "validation-plan.json"
    if plan != expected_plan:
        print(f"ERROR: --plan must be the canonical plan beside the receipt: {expected_plan}")
        return 1
    if args.verify:
        errors = validate_receipt(output, root)
        for error in errors:
            print(f"ERROR: {error}")
        if not errors:
            print(f"Validation receipt current: {output}")
        return 1 if errors else 0
    commands, errors = load_plan(plan, root)
    declared_ids = declared_trace_ids(output.parent.parent)
    for command in commands:
        for trace_id in command.get("trace_ids", []):
            if trace_id.upper() not in declared_ids:
                errors.append(f"validation trace ID is not declared in the spec: {trace_id}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    results: list[dict[str, Any]] = []
    for item in commands:
        started = time.monotonic()
        try:
            code, stdout, stderr, stdout_bytes, stderr_bytes, limited = execute_bounded(
                execution_argv(item["argv"]), root, args.timeout, args.max_output_bytes
            )
        except OSError as exc:
            code, stdout, stderr, stdout_bytes, stderr_bytes, limited = 127, b"", str(exc).encode(), 0, len(str(exc).encode()), False
        results.append({
            "id": item["id"], "argv": item["argv"], "trace_ids": item["trace_ids"],
            "exit_code": code, "duration_ms": int((time.monotonic() - started) * 1000),
            "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
            "stdout_bytes": stdout_bytes, "stderr_bytes": stderr_bytes, "output_limited": limited,
        })
    try:
        current_revision = revision(root)
        current_fingerprint = workspace_fingerprint(root, output)
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return 1
    receipt: dict[str, Any] = {
        "schema": RECEIPT_SCHEMA,
        "revision": current_revision,
        "workspace_fingerprint": current_fingerprint,
        "plan_path": plan.relative_to(root).as_posix(),
        "plan_sha256": hashlib.sha256(plan.read_bytes()).hexdigest(),
        "executed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "evidence_trust": "local-structural-not-authenticated",
        "commands": results,
    }
    receipt["receipt_fingerprint"] = receipt_fingerprint(receipt)
    atomic_json(root, output, receipt)
    failed = [item for item in results if item["exit_code"] != 0]
    print(f"Validation receipt written: {output}; commands={len(results)}; failed={len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
