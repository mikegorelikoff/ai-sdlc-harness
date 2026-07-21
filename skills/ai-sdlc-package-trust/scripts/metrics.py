#!/usr/bin/env python3
"""Generate deterministic, content-free local delivery metrics."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any
_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import encode_toon
from ai_sdlc_safe_io import atomic_write_text

SCHEMA = "ai-sdlc-local-metrics/v1"
FORBIDDEN = {"content", "prompt", "command", "diff", "source", "path", "artifact", "message", "reason"}
def canonical(value: Any) -> str: return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def digest(value: Any) -> str: return hashlib.sha256((value if isinstance(value, str) else canonical(value)).encode()).hexdigest()
def atomic_write(root: Path, path: Path, content: str) -> None:
    atomic_write_text(root, path, content)
def privacy_errors(value: Any, prefix: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = key.lower().replace("-", "_")
            if any(token in normalized.split("_") for token in FORBIDDEN): errors.append(f"forbidden metrics field: {prefix + key}")
            errors.extend(privacy_errors(item, prefix + key + "."))
    elif isinstance(value, list):
        for index, item in enumerate(value): errors.extend(privacy_errors(item, f"{prefix}{index}."))
    elif not isinstance(value, (str, int, float, bool, type(None))): errors.append(f"unsupported metrics value: {prefix.rstrip('.')}")
    return errors
def generate(repository: Path) -> dict[str, Any]:
    states: list[dict[str, Any]] = []
    identities: list[str] = []
    for path in sorted((repository / "_ai_sdlc/runs").glob("*/state.json")):
        try: value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError): continue
        if isinstance(value, dict) and value.get("schema") == "ai-sdlc-run-state/v1": states.append(value); identities.append(str(value.get("fingerprint", "")))
    run_statuses = {key: 0 for key in ("running", "paused", "completed", "stopped")}
    task_statuses = {key: 0 for key in ("pending", "running", "succeeded", "failed", "blocked")}
    steps = failures = tokens = retries = 0
    for state in states:
        status = state.get("status")
        if status in run_statuses: run_statuses[status] += 1
        budget = state.get("budgets", {})
        steps += int(budget.get("used_steps", 0)); failures += int(budget.get("used_failures", 0)); tokens += int(budget.get("used_tokens", 0))
        for task in state.get("tasks", []):
            task_status = task.get("status")
            if task_status in task_statuses: task_statuses[task_status] += 1
            retries += max(0, int(task.get("attempts", 0)) - 1)
    coverage = {"requirements": 0, "requirements_with_fresh_evidence": 0, "evidence_records": 0, "fresh_records": 0, "stale_records": 0}
    ledger_file = repository / "_ai_sdlc/evidence-ledger.json"
    ledger_seen = False
    if ledger_file.is_file():
        try: ledger = json.loads(ledger_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError): ledger = {}
        if ledger.get("schema") == "ai-sdlc-evidence-ledger/v1":
            ledger_seen = True; identities.append(str(ledger.get("fingerprint", "")))
            source = ledger.get("coverage", {})
            for key in ("requirements", "requirements_with_fresh_evidence", "evidence_records", "fresh_records"): coverage[key] = int(source.get(key, 0))
            coverage["stale_records"] = sum(1 for item in ledger.get("records", []) if item.get("status") != "fresh")
    result: dict[str, Any] = {"schema": SCHEMA, "status": "available" if states or ledger_seen else "insufficient-data", "runs": {"total": len(states), **run_statuses}, "tasks": {"total": sum(task_statuses.values()), **task_statuses, "retries": retries}, "budgets": {"steps": steps, "failures": failures, "tokens": tokens}, "quality": coverage, "inputs_fingerprint": digest(sorted(identities))}
    result["fingerprint"] = digest(result)
    errors = privacy_errors(result)
    if errors: raise ValueError("; ".join(errors))
    return result
def markdown(value: dict[str, Any]) -> str:
    return f"# Local Delivery Metrics\n\nStatus: **{value['status']}**\n\n- Runs: {value['runs']['total']}\n- Tasks: {value['tasks']['total']}\n- Retries: {value['tasks']['retries']}\n- Tokens: {value['budgets']['tokens']}\n- Fresh evidence: {value['quality']['fresh_records']}\n- Fingerprint: `{value['fingerprint']}`\n"
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("repository", type=Path); parser.add_argument("--generate", action="store_true", required=True); parser.add_argument("--write", action="store_true"); parser.add_argument("--format", choices=("toon", "json", "markdown"), default="toon")
    parser.add_argument("--quick-flow", action="store_true"); parser.add_argument("--full-flow", action="store_true"); parser.add_argument("--feature", default="<feature-name>"); parser.add_argument("--state-check", action="store_true"); parser.add_argument("--begin-state", action="store_true"); parser.add_argument("--complete-state", action="store_true"); parser.add_argument("--decision-ref"); parser.add_argument("--assumption"); parser.add_argument("--state-workspace", choices=("refinement", "implementation")); args = parser.parse_args()
    if args.begin_state or args.complete_state: print("ERROR: metrics cannot mutate feature lifecycle state"); return 1
    repository = args.repository.resolve()
    if not repository.is_dir(): print("ERROR: repository does not exist"); return 1
    try: value = generate(repository)
    except ValueError as exc: print(f"ERROR: {exc}"); return 1
    if args.write:
        output = repository / "_ai_sdlc/metrics/local.json"
        try:
            atomic_write(repository, output, json.dumps(value, indent=2, sort_keys=True) + "\n"); atomic_write(repository, output.with_suffix(".toon"), encode_toon(value)); atomic_write(repository, output.with_suffix(".md"), markdown(value))
        except ValueError as exc:
            print(f"ERROR: {exc}"); return 1
    print(json.dumps(value, indent=2, sort_keys=True) if args.format == "json" else markdown(value) if args.format == "markdown" else encode_toon(value), end="" if args.format != "json" else "\n")
    return 0
if __name__ == "__main__": raise SystemExit(main())
