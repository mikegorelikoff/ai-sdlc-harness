#!/usr/bin/env python3
"""Build repository topology and bounded freshness-aware context packs."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

from project_context import SECRET_PATTERN, revision, saved_identity, scan


PACK_SCHEMA = "ai-sdlc-context-pack/v2"
SELECTOR_SCHEMA = "ai-sdlc-context-selectors/v2"
TOPOLOGY_SCHEMA = "ai-sdlc-repository-topology/v2"
SOURCE_EXTENSIONS = {".c", ".cc", ".cpp", ".cs", ".go", ".java", ".js", ".jsx", ".kt", ".php", ".py", ".rb", ".rs", ".swift", ".ts", ".tsx"}
MANIFESTS = {"Cargo.toml", "Makefile", "go.mod", "package.json", "pyproject.toml", "requirements.txt"}
IGNORED_PARTS = {".git", ".venv", "__pycache__", "build", "dist", "node_modules", "site", "vendor"}
CONTENT_SECRET = re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password|private[_-]?key)\b\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{8,}")
SELECTOR_FIELDS = {"id", "when", "include", "priority", "max_tokens", "reason"}
WHEN_FIELDS = {"task", "paths_any", "tags_any"}


def canonical(value: Any) -> str:
    """Serialize normalized data for deterministic identity."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    """Return SHA-256 for text or normalized data."""
    if not isinstance(value, str):
        value = canonical(value)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def atomic_write(path: Path, content: str) -> None:
    """Atomically replace one generated output."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def git_files(root: Path) -> list[str]:
    """Return tracked and visible untracked repository-relative files."""
    result = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=root, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        values = result.stdout.splitlines()
    else:
        values = [path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()]
    return sorted({value for value in values if value and not set(PurePosixPath(value).parts) & IGNORED_PARTS})[:10000]


def unsafe_path(relative: str) -> str | None:
    """Explain a built-in path exclusion without reading bytes."""
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "\\" in relative:
        return "unsafe-path"
    if set(pure.parts) & IGNORED_PARTS:
        return "generated-or-vendor-path"
    if relative.startswith("_ai_sdlc/context/"):
        return "generated-context-output"
    if SECRET_PATTERN.search(relative):
        return "secret-named-path"
    return None


def read_safe(root: Path, relative: str) -> tuple[str | None, str | None]:
    """Read bounded text only after path, boundary, symlink, and secret checks."""
    reason = unsafe_path(relative)
    if reason:
        return None, reason
    path = root / relative
    try:
        path.resolve(strict=False).relative_to(root)
    except ValueError:
        return None, "path-escape"
    if path.is_symlink():
        return None, "symlink"
    if not path.is_file():
        return None, "missing"
    try:
        data = path.read_bytes()
    except OSError:
        return None, "unreadable"
    if len(data) > 262144:
        return None, "oversized"
    if b"\0" in data:
        return None, "binary"
    text = data.decode("utf-8", errors="replace")
    if CONTENT_SECRET.search(text):
        return None, "credential-like-content"
    return text, None


def codeowners(root: Path) -> tuple[str, list[dict[str, Any]]]:
    """Read the first canonical CODEOWNERS file and normalize its rules."""
    for relative in (".github/CODEOWNERS", "CODEOWNERS", "docs/CODEOWNERS"):
        text, error = read_safe(root, relative)
        if text is None:
            if error == "missing":
                continue
            return relative, []
        rules: list[dict[str, Any]] = []
        for line_number, raw in enumerate(text.splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                rules.append({"pattern": parts[0], "owners": parts[1:], "path": relative, "line": line_number})
        return relative, rules
    return "", []


def owner_matches(relative: str, pattern: str) -> bool:
    """Apply a deterministic conservative CODEOWNERS-style match."""
    normalized = pattern.lstrip("/")
    if normalized.endswith("/"):
        normalized += "**"
    if "/" not in normalized:
        return fnmatch.fnmatch(PurePosixPath(relative).name, normalized) or fnmatch.fnmatch(relative, f"**/{normalized}")
    return fnmatch.fnmatch(relative, normalized)


def owners_for(relative: str, rules: list[dict[str, Any]]) -> list[str]:
    """Use owners from the last matching ownership rule."""
    owners: list[str] = []
    for rule in rules:
        if owner_matches(relative, rule["pattern"]):
            owners = list(rule["owners"])
    return owners


def test_stem(path: str) -> str:
    """Normalize common test filename conventions."""
    stem = Path(path).stem
    stem = re.sub(r"^(?:test_|spec_)", "", stem)
    stem = re.sub(r"(?:_test|_spec|\.test|\.spec)$", "", stem)
    return stem


def file_kind(relative: str) -> str:
    """Classify bounded topology files."""
    path = PurePosixPath(relative)
    name = path.name
    if name in MANIFESTS:
        return "manifest"
    if name == "CODEOWNERS":
        return "ownership"
    if path.suffix.lower() in SOURCE_EXTENSIONS:
        parts = {part.lower() for part in path.parts}
        if "tests" in parts or "test" in parts or name.startswith(("test_", "spec_")) or re.search(r"(?:_test|_spec|\.test|\.spec)\.[^.]+$", name):
            return "test"
        return "source"
    return "other"


def build_topology(root: Path) -> dict[str, Any]:
    """Build ownership, source/test, stack, and command topology."""
    files = git_files(root)
    owner_path, ownership = codeowners(root)
    tests = [relative for relative in files if file_kind(relative) == "test" and not unsafe_path(relative)]
    test_by_stem: dict[str, list[str]] = {}
    for relative in tests:
        test_by_stem.setdefault(test_stem(relative), []).append(relative)
    rows: list[dict[str, Any]] = []
    for relative in files:
        kind = file_kind(relative)
        if kind not in {"source", "test", "manifest", "ownership"} or unsafe_path(relative):
            continue
        related = sorted(test_by_stem.get(Path(relative).stem, [])) if kind == "source" else []
        rows.append({"path": relative, "kind": kind, "owners": owners_for(relative, ownership), "tests": related})
    _, stack, commands, context_fingerprint = scan(root)
    topology: dict[str, Any] = {"schema": TOPOLOGY_SCHEMA, "revision": revision(root), "ownership_source": owner_path, "ownership": ownership, "files": rows, "stack": stack, "commands": commands, "project_context_fingerprint": context_fingerprint}
    topology["fingerprint"] = digest(topology)
    return topology


def safe_glob(pattern: Any) -> bool:
    """Validate a repository-relative selector glob."""
    return isinstance(pattern, str) and bool(pattern) and not PurePosixPath(pattern).is_absolute() and ".." not in PurePosixPath(pattern).parts and "\\" not in pattern


def load_selectors(path: Path | None) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    """Load strict optional selector configuration."""
    if path is None:
        return [], [], []
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [], [f"cannot read selector config: {exc}"]
    errors: list[str] = []
    if not isinstance(value, dict) or set(value) != {"schema", "selectors", "exclusions"} or value.get("schema") != SELECTOR_SCHEMA:
        return [], [], [f"selector config must match {SELECTOR_SCHEMA}"]
    exclusions = value["exclusions"]
    if not isinstance(exclusions, list) or not all(safe_glob(item) for item in exclusions) or len(exclusions) != len(set(exclusions)):
        errors.append("selector exclusions must be unique safe globs")
        exclusions = []
    selectors = value["selectors"]
    if not isinstance(selectors, list):
        return [], exclusions, errors + ["selectors must be an array"]
    ids: list[str] = []
    valid: list[dict[str, Any]] = []
    for index, selector in enumerate(selectors):
        prefix = f"selector {index}"
        if not isinstance(selector, dict) or set(selector) != SELECTOR_FIELDS:
            errors.append(f"{prefix}: fields are invalid")
            continue
        ids.append(selector["id"] if isinstance(selector["id"], str) else "")
        when = selector["when"]
        if not isinstance(selector["id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", selector["id"]):
            errors.append(f"{prefix}: id is invalid")
        if not isinstance(when, dict) or set(when) != WHEN_FIELDS:
            errors.append(f"{prefix}: when fields are invalid")
        elif not isinstance(when["task"], str) or not isinstance(when["paths_any"], list) or not all(safe_glob(item) for item in when["paths_any"]) or not isinstance(when["tags_any"], list) or not all(isinstance(item, str) and item for item in when["tags_any"]):
            errors.append(f"{prefix}: when values are invalid")
        if not isinstance(selector["include"], list) or not selector["include"] or not all(safe_glob(item) for item in selector["include"]):
            errors.append(f"{prefix}: include must contain safe globs")
        if not isinstance(selector["priority"], int) or not 0 <= selector["priority"] <= 100:
            errors.append(f"{prefix}: priority must be 0..100")
        if not isinstance(selector["max_tokens"], int) or not 16 <= selector["max_tokens"] <= 4000:
            errors.append(f"{prefix}: max_tokens must be 16..4000")
        if not isinstance(selector["reason"], str) or not selector["reason"].strip():
            errors.append(f"{prefix}: reason is required")
        valid.append(selector)
    if len(ids) != len(set(ids)):
        errors.append("duplicate selector ids")
    return valid, exclusions, errors


def selector_matches(selector: dict[str, Any], task: str, paths: list[str], tags: list[str]) -> tuple[bool, str]:
    """Evaluate declared task, path, and tag conditions."""
    when = selector["when"]
    if when["task"] and not fnmatch.fnmatch(task, when["task"]):
        return False, "task-condition-not-matched"
    if when["paths_any"] and not any(fnmatch.fnmatch(path, pattern) for path in paths for pattern in when["paths_any"]):
        return False, "path-condition-not-matched"
    if when["tags_any"] and not set(tags) & set(when["tags_any"]):
        return False, "tag-condition-not-matched"
    return True, "matched"


def add_candidate(candidates: dict[str, dict[str, Any]], path: str, priority: int, max_tokens: int, reason: str) -> None:
    """Merge candidate reasons while preserving strongest priority and cap."""
    current = candidates.get(path)
    if current is None:
        candidates[path] = {"path": path, "priority": priority, "max_tokens": max_tokens, "reasons": [reason]}
    else:
        current["priority"] = max(current["priority"], priority)
        current["max_tokens"] = max(current["max_tokens"], max_tokens)
        if reason not in current["reasons"]:
            current["reasons"].append(reason)


def candidate_set(root: Path, topology: dict[str, Any], task: str, paths: list[str], tags: list[str], selectors: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    """Build explained built-in and custom candidate sources."""
    candidates: dict[str, dict[str, Any]] = {}
    selector_rows: list[dict[str, str]] = []
    available = git_files(root)
    for relative in ("AGENTS.md", "project-context.md", "README.md"):
        if relative in available:
            add_candidate(candidates, relative, 100 if relative == "AGENTS.md" else 75, 500, "repository-guidance")
    for relative in paths:
        add_candidate(candidates, relative, 100, 1200, "requested-path")
        pure = PurePosixPath(relative)
        if len(pure.parts) >= 2 and pure.parts[0] in {"specs", "specs-refiniment"}:
            prefix = "/".join(pure.parts[:2]) + "/"
            for item in available:
                if item.startswith(prefix) and item.endswith(".md"):
                    add_candidate(candidates, item, 90, 700, "owning-feature-spec")
    task_pattern = re.compile(rf"\b{re.escape(task)}\b", re.IGNORECASE)
    for relative in available:
        if relative.startswith(("specs/", "specs-refiniment/")) and relative.endswith(".md"):
            text, error = read_safe(root, relative)
            if text is not None and task_pattern.search(text):
                prefix = relative.rsplit("/", 1)[0] + "/"
                for item in available:
                    if item.startswith(prefix) and item.endswith(".md"):
                        add_candidate(candidates, item, 92, 700, "task-trace")
    for relative in available:
        if PurePosixPath(relative).name in MANIFESTS:
            add_candidate(candidates, relative, 55, 300, "repository-manifest")
    if topology["ownership_source"]:
        add_candidate(candidates, topology["ownership_source"], 70, 300, "ownership-topology")
    file_rows = {row["path"]: row for row in topology["files"]}
    for relative in paths:
        for test in file_rows.get(relative, {}).get("tests", []):
            add_candidate(candidates, test, 85, 600, f"related-test:{relative}")
    for selector in selectors:
        matched, status = selector_matches(selector, task, paths, tags)
        selector_rows.append({"id": selector["id"], "status": status, "reason": selector["reason"]})
        if matched:
            for pattern in selector["include"]:
                for item in available:
                    if fnmatch.fnmatch(item, pattern):
                        add_candidate(candidates, item, selector["priority"], selector["max_tokens"], f"selector:{selector['id']}")
    return candidates, selector_rows


def excluded_by_config(path: str, exclusions: list[str]) -> bool:
    """Match explicit exclusions."""
    return any(fnmatch.fnmatch(path, pattern) for pattern in exclusions)


def token_estimate(text: str) -> int:
    """Apply a deterministic conservative character approximation."""
    return max(1, (len(text) + 3) // 4)


def freshness(root: Path, selected_paths: set[str], current_context_fingerprint: str) -> dict[str, Any]:
    """Report saved project context drift and non-fresh evidence intersections."""
    warnings: list[dict[str, str]] = []
    saved_revision, saved_fingerprint = saved_identity(root / "_ai_sdlc/project-context.toon")
    current_revision = revision(root)
    if not saved_fingerprint:
        context_status = "missing"
        warnings.append({"code": "project-context-missing", "detail": "Generate project context before relying on repository memory."})
    elif (saved_revision, saved_fingerprint) != (current_revision, current_context_fingerprint):
        context_status = "stale"
        warnings.append({"code": "project-context-stale", "detail": "Saved project context identity differs from current repository evidence."})
    else:
        context_status = "current"
    ledger_path = root / "_ai_sdlc/evidence-ledger.json"
    ledger_status = "missing"
    ledger_fingerprint = ""
    if ledger_path.is_file() and not ledger_path.is_symlink():
        try:
            ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
            ledger_fingerprint = str(ledger.get("fingerprint", ""))
            ledger_status = "available" if ledger.get("schema") == "ai-sdlc-evidence-ledger/v1" else "invalid"
            for record in ledger.get("records", []):
                if record.get("status") == "fresh":
                    continue
                affected = sorted(selected_paths & {item.get("path") for item in record.get("files", []) if isinstance(item, dict)})
                for path in affected:
                    warnings.append({"code": "selected-evidence-not-fresh", "detail": f"{path} is referenced by {record.get('id')} with status {record.get('status')}."})
        except (OSError, json.JSONDecodeError):
            ledger_status = "invalid"
    if ledger_status == "missing":
        warnings.append({"code": "evidence-ledger-missing", "detail": "Freshness coverage is unavailable."})
    elif ledger_status == "invalid":
        warnings.append({"code": "evidence-ledger-invalid", "detail": "Evidence ledger cannot be trusted."})
    return {"project_context": context_status, "evidence_ledger": ledger_status, "evidence_ledger_fingerprint": ledger_fingerprint, "warnings": sorted(warnings, key=lambda item: (item["code"], item["detail"]))}


def build_pack(root: Path, topology: dict[str, Any], task: str, goal: str, paths: list[str], tags: list[str], budget: int, selectors: list[dict[str, Any]], configured_exclusions: list[str]) -> dict[str, Any]:
    """Select, clip, and fingerprint one bounded task context pack."""
    candidates, selector_rows = candidate_set(root, topology, task, paths, tags, selectors)
    selected: list[dict[str, Any]] = []
    exclusions: list[dict[str, str]] = []
    used = 0
    for candidate in sorted(candidates.values(), key=lambda item: (-item["priority"], item["path"])):
        relative = candidate["path"]
        if excluded_by_config(relative, configured_exclusions):
            exclusions.append({"path": relative, "reason": "configured-exclusion"})
            continue
        content, error = read_safe(root, relative)
        if content is None:
            exclusions.append({"path": relative, "reason": error or "excluded"})
            continue
        remaining = budget - used
        if remaining <= 0:
            exclusions.append({"path": relative, "reason": "budget-exhausted"})
            continue
        allowed = min(candidate["max_tokens"], remaining)
        clipped = content[: allowed * 4]
        tokens = token_estimate(clipped)
        if tokens > remaining:
            clipped = clipped[: remaining * 4]
            tokens = token_estimate(clipped)
        used += tokens
        selected.append({"path": relative, "start_line": 1, "end_line": clipped.count("\n") + (0 if clipped.endswith("\n") else 1), "priority": candidate["priority"], "reason": "; ".join(sorted(candidate["reasons"])), "estimated_tokens": tokens, "sha256": digest(content), "truncated": len(clipped) < len(content), "content": clipped})
    _, _, _, context_fingerprint = scan(root)
    pack: dict[str, Any] = {"schema": PACK_SCHEMA, "task": {"id": task, "goal": goal, "paths": sorted(set(paths)), "tags": sorted(set(tags))}, "repository": {"revision": revision(root), "topology_fingerprint": topology["fingerprint"]}, "budget": {"limit_tokens": budget, "used_tokens": used, "remaining_tokens": budget - used, "estimate": "ceil(utf8-characters/4)"}, "selectors": selector_rows, "selected": selected, "exclusions": sorted(exclusions, key=lambda item: (item["path"], item["reason"])), "freshness": freshness(root, {item["path"] for item in selected}, context_fingerprint)}
    pack["fingerprint"] = digest(pack)
    return pack


def markdown(value: dict[str, Any]) -> str:
    """Render topology or a task pack for human review."""
    if value["schema"] == TOPOLOGY_SCHEMA:
        lines = ["# Repository Topology", "", f"Fingerprint: `{value['fingerprint']}`", f"Revision: `{value['revision']}`", "", "| Path | Kind | Owners | Tests |", "| --- | --- | --- | --- |"]
        lines.extend(f"| `{row['path']}` | {row['kind']} | {', '.join(row['owners'])} | {', '.join(row['tests'])} |" for row in value["files"])
        return "\n".join(lines) + "\n"
    lines = ["# Task Context Pack", "", f"Task: `{value['task']['id']}`", f"Goal: {value['task']['goal']}", f"Fingerprint: `{value['fingerprint']}`", f"Budget: {value['budget']['used_tokens']} / {value['budget']['limit_tokens']} estimated tokens", "", "## Selected context", ""]
    for item in value["selected"]:
        lines.extend([f"### `{item['path']}`", "", f"Reason: {item['reason']}", "", "```text", item["content"].rstrip(), "```", ""])
    lines.extend(["## Freshness warnings", ""])
    lines.extend(f"- `{item['code']}`: {item['detail']}" for item in value["freshness"]["warnings"])
    if not value["freshness"]["warnings"]:
        lines.append("- None")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """Build topology or one bounded task pack."""
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--topology", action="store_true")
    actions.add_argument("--build-pack", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--task")
    parser.add_argument("--goal")
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--budget", type=int, default=2000)
    parser.add_argument("--selector-config", type=Path)
    parser.add_argument("--write", action="store_true")
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
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        print("ERROR: context packs cannot mutate feature lifecycle state")
        return 1
    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR: repository does not exist: {root}")
        return 1
    if args.build_pack and (not args.task or not args.goal):
        print("ERROR: --task and --goal are required for --build-pack")
        return 1
    if args.task and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.task):
        print("ERROR: task id is unsafe")
        return 1
    if not 128 <= args.budget <= 32000:
        print("ERROR: budget must be 128..32000 estimated tokens")
        return 1
    for relative in args.path:
        if unsafe_path(relative):
            print(f"ERROR: unsafe requested path: {relative}")
            return 1
    selectors, configured_exclusions, errors = load_selectors(args.selector_config.resolve() if args.selector_config else None)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    topology = build_topology(root)
    if args.build_pack:
        value = build_pack(root, topology, args.task, args.goal, args.path, args.tag, args.budget, selectors, configured_exclusions)
        output_path = root / f"_ai_sdlc/context/task-packs/{args.task}.json"
    else:
        value = topology
        output_path = root / "_ai_sdlc/context/topology.json"
    if args.write:
        atomic_write(output_path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        atomic_write(output_path.with_suffix(".md"), markdown(value))
    if args.format == "json":
        print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))
    elif args.format == "toon":
        print(f"schema: {value['schema']}")
        print(f"fingerprint: {value['fingerprint']}")
        if value["schema"] == PACK_SCHEMA:
            print(f"task: {value['task']['id']}")
            print(f"budget: {value['budget']['used_tokens']}/{value['budget']['limit_tokens']}")
            print(f"selected: {len(value['selected'])}")
            print(f"exclusions: {len(value['exclusions'])}")
            print(f"freshness_warnings: {len(value['freshness']['warnings'])}")
        else:
            print(f"files: {len(value['files'])}")
            print(f"ownership_rules: {len(value['ownership'])}")
    else:
        print(markdown(value), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
