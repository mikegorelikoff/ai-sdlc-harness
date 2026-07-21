#!/usr/bin/env python3
"""Create and verify validation evidence tied to actual process outcomes."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any
from ai_sdlc_safe_io import bounded_path


RECEIPT_SCHEMA = "ai-sdlc-validation-receipt/v1"
TRACE_ID_RE = re.compile(r"\b(?:(?:REQ|AC|US|TC|TASK|RISK|DEC|EPIC|GOAL|CAP|WF|BR|SC|NFR|DEP)-\d{2,4}|T\d{3,4})\b", re.IGNORECASE)
MAX_UNTRACKED_FILE_BYTES = 20_000_000


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def workspace_fingerprint(root: Path, exclude: Path | None = None) -> str:
    """Hash the review surface while excluding derived downstream evidence."""
    root = root.resolve()
    excluded: set[Path] = set()
    if exclude:
        receipt = exclude.resolve()
        excluded.add(receipt)
        # A validation receipt binds validation.md and the product/docs diff,
        # but lifecycle state and downstream review/commit records are derived
        # after the run. Excluding them prevents an accepted receipt from
        # invalidating itself while preserving staleness for source changes.
        if receipt.parent.name == "_ai_sdlc":
            feature_root = receipt.parent.parent
            excluded.update(
                {
                    receipt.parent / "state.toon",
                    feature_root / "code-review.md",
                    feature_root / "security-review.md",
                    feature_root / "commit-readiness.md",
                    feature_root / "commit-message.md",
                }
            )
            workspace = feature_root.parent
            excluded.update(
                {
                    workspace / "specs-index.md",
                    workspace / "_ai_sdlc" / "specs-index.toon",
                }
            )
    pathspec_excludes: list[str] = []
    for path in sorted(excluded):
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError:
            continue
        pathspec_excludes.append(f":(exclude){relative}")
    digest = hashlib.sha256()
    for command in (
        ["git", "diff", "--binary", "HEAD", "--", ".", *pathspec_excludes],
        ["git", "diff", "--cached", "--binary", "HEAD", "--", ".", *pathspec_excludes],
    ):
        result = subprocess.run(command, cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(f"cannot fingerprint Git workspace: {result.stderr.decode(errors='replace').strip()}")
        digest.update(result.stdout)
        digest.update(b"\0")
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if untracked.returncode != 0:
        raise RuntimeError(f"cannot enumerate untracked files: {untracked.stderr.decode(errors='replace').strip()}")
    for raw in sorted(item for item in untracked.stdout.split(b"\0") if item):
        relative = raw.decode("utf-8", errors="surrogateescape")
        lexical = root / relative
        if lexical.is_symlink():
            raise RuntimeError(f"validation review surface contains an untracked symlink: {relative}")
        try:
            path = bounded_path(root, lexical)
        except ValueError as exc:
            raise RuntimeError(f"validation review surface is unsafe: {relative}: {exc}") from exc
        if path in excluded:
            continue
        digest.update(relative.encode("utf-8", errors="surrogateescape"))
        digest.update(b"\0")
        if path.is_file():
            size = path.stat().st_size
            if size > MAX_UNTRACKED_FILE_BYTES:
                raise RuntimeError(f"untracked validation file exceeds {MAX_UNTRACKED_FILE_BYTES} bytes: {relative}")
            file_digest = hashlib.sha256()
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(65536), b""):
                    file_digest.update(chunk)
            digest.update(file_digest.digest())
        digest.update(b"\0")
    return digest.hexdigest()


def revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=False, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    value = result.stdout.strip()
    if result.returncode != 0 or not re.fullmatch(r"[a-f0-9]{40}", value):
        raise RuntimeError(f"validation requires a Git work tree with a valid HEAD: {result.stderr.strip()}")
    return value


def receipt_fingerprint(value: dict[str, Any]) -> str:
    body = {key: item for key, item in value.items() if key != "receipt_fingerprint"}
    return hashlib.sha256(canonical(body).encode("utf-8")).hexdigest()


def declared_trace_ids(spec_dir: Path) -> set[str]:
    """Return canonical trace identifiers declared by primary spec evidence."""
    declared: set[str] = set()
    if spec_dir.is_dir():
        for source in ("requirements.md", "test-cases.md", "tasks.md", "qa.md"):
            source_path = spec_dir / source
            if source_path.is_file():
                declared.update(
                    match.group(0).upper()
                    for match in TRACE_ID_RE.finditer(
                        source_path.read_text(encoding="utf-8", errors="replace")
                    )
                )
    return declared


def validate_receipt(path: Path, root: Path) -> list[str]:
    """Validate schema, process outcomes, integrity, revision, and current diff."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read validation receipt: {exc}"]
    errors: list[str] = []
    if not isinstance(value, dict) or value.get("schema") != RECEIPT_SCHEMA:
        return [f"validation receipt schema must be {RECEIPT_SCHEMA}"]
    if value.get("evidence_trust") != "local-structural-not-authenticated":
        errors.append("validation receipt must disclose local unauthenticated evidence trust")
    if value.get("receipt_fingerprint") != receipt_fingerprint(value):
        errors.append("validation receipt fingerprint mismatch")
    expected_plan = path.parent / "validation-plan.json"
    try:
        relative_plan = expected_plan.resolve(strict=True).relative_to(root.resolve()).as_posix()
        plan_digest = hashlib.sha256(expected_plan.read_bytes()).hexdigest()
    except (OSError, ValueError) as exc:
        errors.append(f"canonical validation plan is unavailable: {exc}")
        relative_plan, plan_digest = "", ""
    if value.get("plan_path") != relative_plan:
        errors.append("validation receipt plan path mismatch")
    if value.get("plan_sha256") != plan_digest:
        errors.append("validation receipt plan digest mismatch")
    commands = value.get("commands")
    if not isinstance(commands, list) or not commands:
        errors.append("validation receipt has no executed commands")
    else:
        for item in commands:
            if not isinstance(item, dict) or not isinstance(item.get("argv"), list):
                errors.append("validation receipt command is malformed")
            elif item.get("exit_code") != 0:
                errors.append(f"validation command failed: {item.get('id', 'unknown')} exit={item.get('exit_code')}")
            trace_ids = item.get("trace_ids") if isinstance(item, dict) else None
            if not isinstance(trace_ids, list) or not trace_ids:
                errors.append(f"validation command lacks trace IDs: {item.get('id', 'unknown') if isinstance(item, dict) else 'unknown'}")
    spec_dir = path.parent.parent
    declared_ids = declared_trace_ids(spec_dir)
    if isinstance(commands, list):
        for item in commands:
            if not isinstance(item, dict) or not isinstance(item.get("trace_ids"), list):
                continue
            for trace_id in item["trace_ids"]:
                if isinstance(trace_id, str) and trace_id.upper() not in declared_ids:
                    errors.append(f"validation trace ID is not declared in the spec: {trace_id}")
    try:
        if value.get("revision") != revision(root):
            errors.append("validation receipt revision is stale")
        if value.get("workspace_fingerprint") != workspace_fingerprint(root, path):
            errors.append("validation receipt workspace fingerprint is stale")
    except RuntimeError as exc:
        errors.append(str(exc))
    return errors
