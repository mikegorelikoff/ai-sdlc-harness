#!/usr/bin/env python3
"""Import or verify explicit external Markdown specifications as safe local snapshots."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from project_context import credential_like_content

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_safe_io import atomic_write_text, bounded_path


SCHEMA = "ai-sdlc-external-spec-snapshot/v1"
FEATURE_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MAX_BYTES = 1_048_576
MANIFEST_FIELDS = {"schema", "feature", "source_id", "source_revision", "content_authority", "files", "fingerprint"}
ROW_FIELDS = {"source", "destination", "sha256", "size_bytes"}


def canonical(value: Any) -> str:
    """Return stable JSON used for fingerprints and durable output."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def source_revision(root: Path) -> str:
    """Return a Git revision without mutating or trusting source content."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=False, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    value = result.stdout.strip()
    return value if re.fullmatch(r"[0-9a-f]{40}", value) else "unversioned"


def safe_source_id(value: str) -> bool:
    """Accept a portable logical identity, never a filesystem path."""
    return (
        bool(value)
        and len(value) <= 160
        and value == value.strip()
        and not any(char in value for char in "\\/\r\n\0")
        and all(ord(char) >= 32 and ord(char) != 127 for char in value)
    )


def source_path(root: Path, relative: str) -> Path:
    """Resolve one regular Markdown source below an explicit non-symlink root."""
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "\\" in relative or pure.suffix.lower() != ".md":
        raise ValueError(f"source must be a safe source-relative Markdown path: {relative}")
    current = root
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"source contains a symlink component: {relative}")
    try:
        path = current.resolve(strict=True)
        path.relative_to(root)
    except (OSError, ValueError) as exc:
        raise ValueError(f"source is missing or escapes source root: {relative}") from exc
    if not path.is_file():
        raise ValueError(f"source is not a regular file: {relative}")
    return path


def destination_name(relative: str) -> str:
    """Map a source-relative path to a deterministic top-level feature file."""
    stem = PurePosixPath(relative).with_suffix("").as_posix().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    if not slug:
        raise ValueError(f"source does not produce a safe destination name: {relative}")
    if len(slug) > 96:
        slug = f"{slug[:79].rstrip('-')}-{hashlib.sha256(relative.encode()).hexdigest()[:16]}"
    return f"external-{slug}.md"


def read_source(root: Path, relative: str) -> tuple[str, str, int]:
    """Read one bounded UTF-8 source after all path and content checks."""
    path = source_path(root, relative)
    size = path.stat().st_size
    if size > MAX_BYTES:
        raise ValueError(f"source exceeds {MAX_BYTES} bytes: {relative}")
    data = path.read_bytes()
    if b"\0" in data:
        raise ValueError(f"source is binary: {relative}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"source is not UTF-8: {relative}") from exc
    if credential_like_content(text):
        raise ValueError(f"source contains credential-shaped content: {relative}")
    return text, digest_bytes(data), size


def load_manifest(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read existing snapshot manifest: {exc}") from exc
    if not isinstance(value, dict) or set(value) != MANIFEST_FIELDS or value.get("schema") != SCHEMA or not isinstance(value.get("files"), list):
        raise ValueError("existing snapshot manifest has an unsupported schema")
    if not isinstance(value.get("feature"), str) or not FEATURE_RE.fullmatch(value["feature"]):
        raise ValueError("existing snapshot manifest feature is invalid")
    if not isinstance(value.get("source_id"), str) or not safe_source_id(value["source_id"]):
        raise ValueError("existing snapshot manifest source_id is invalid")
    revision = value.get("source_revision")
    if revision != "unversioned" and (not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision)):
        raise ValueError("existing snapshot manifest source revision is invalid")
    if value.get("content_authority") != "evidence_only":
        raise ValueError("existing snapshot manifest authority must be evidence_only")
    expected = dict(value)
    fingerprint = expected.pop("fingerprint")
    if not isinstance(fingerprint, str) or fingerprint != hashlib.sha256(canonical(expected).encode("utf-8")).hexdigest():
        raise ValueError("existing snapshot manifest fingerprint is invalid")
    for row in value["files"]:
        if not isinstance(row, dict) or set(row) != ROW_FIELDS:
            raise ValueError("existing snapshot manifest contains an invalid file row")
        source = row["source"]
        destination = row["destination"]
        if not isinstance(source, str) or not isinstance(destination, str):
            raise ValueError("existing snapshot manifest paths must be strings")
        pure_destination = PurePosixPath(destination)
        expected_prefix = f"specs-refiniment/{value['feature']}/"
        if pure_destination.is_absolute() or ".." in pure_destination.parts or not destination.startswith(expected_prefix):
            raise ValueError("existing snapshot manifest contains an unsafe destination")
        if not isinstance(row["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]):
            raise ValueError("existing snapshot manifest contains an invalid hash")
        if not isinstance(row["size_bytes"], int) or isinstance(row["size_bytes"], bool) or row["size_bytes"] < 0:
            raise ValueError("existing snapshot manifest contains an invalid size")
    return value


def build_snapshot(repository: Path, source_root: Path, feature: str, source_id: str, sources: list[str]) -> tuple[dict[str, Any], dict[Path, str]]:
    """Validate a complete snapshot set and return manifest plus writes."""
    feature_root = bounded_path(repository, repository / "specs-refiniment" / feature)
    manifest_path = bounded_path(repository, feature_root / "external-specs.json")
    previous = load_manifest(manifest_path)
    if previous and (previous.get("feature") != feature or previous.get("source_id") != source_id):
        raise ValueError("existing snapshot belongs to a different feature or source_id")
    previous_rows = {row["destination"]: row["source"] for row in previous["files"]} if previous else {}
    previous_sources = set(previous_rows.values())
    missing = sorted(previous_sources - set(sources))
    if missing:
        raise ValueError("previous sources were omitted; review them manually instead of implicit deletion: " + ", ".join(missing))

    rows: list[dict[str, Any]] = []
    writes: dict[Path, str] = {}
    destinations: dict[str, str] = {}
    for relative in sorted(set(sources)):
        text, sha256, size = read_source(source_root, relative)
        name = destination_name(relative)
        if name in destinations and destinations[name] != relative:
            raise ValueError(f"destination collision: {destinations[name]} and {relative}")
        destinations[name] = relative
        destination = f"specs-refiniment/{feature}/{name}"
        target = bounded_path(repository, repository / destination)
        if target.exists() and previous_rows.get(destination) != relative:
            raise ValueError(f"destination already exists without matching snapshot ownership: {destination}")
        rows.append({"source": relative, "destination": destination, "sha256": sha256, "size_bytes": size})
        writes[target] = text
    value: dict[str, Any] = {
        "schema": SCHEMA,
        "feature": feature,
        "source_id": source_id,
        "source_revision": source_revision(source_root),
        "content_authority": "evidence_only",
        "files": rows,
    }
    value["fingerprint"] = hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()
    writes[manifest_path] = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    return value, writes


def check_snapshot(repository: Path, source_root: Path, feature: str, source_id: str) -> tuple[dict[str, Any], list[str]]:
    """Compare a durable snapshot with the current explicit source checkout."""
    manifest_path = bounded_path(repository, repository / "specs-refiniment" / feature / "external-specs.json")
    manifest = load_manifest(manifest_path)
    if manifest is None:
        return {}, ["snapshot manifest is missing"]
    errors: list[str] = []
    if manifest.get("feature") != feature:
        errors.append("snapshot feature does not match")
    if manifest.get("source_id") != source_id:
        errors.append("snapshot source_id does not match")
    if manifest.get("source_revision") != source_revision(source_root):
        errors.append("source revision drifted")
    for row in manifest.get("files", []):
        try:
            text, sha256, size = read_source(source_root, row["source"])
            destination = bounded_path(repository, repository / row["destination"])
        except (TypeError, ValueError) as exc:
            errors.append(str(exc))
            continue
        if sha256 != row["sha256"] or size != row["size_bytes"]:
            errors.append(f"source drifted: {row['source']}")
        if not destination.is_file() or destination.is_symlink():
            errors.append(f"snapshot destination is missing or unsafe: {row['destination']}")
        elif destination.read_bytes() != text.encode("utf-8"):
            errors.append(f"snapshot destination drifted: {row['destination']}")
    return manifest, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        parser.error("external snapshot management cannot mutate feature lifecycle state")
    if not FEATURE_RE.fullmatch(args.feature):
        parser.error("--feature must be a lowercase hyphenated slug")
    if not safe_source_id(args.source_id):
        parser.error("--source-id must be a portable logical identifier, not a path")
    try:
        repository = args.root.resolve(strict=True)
        source_root = args.source_root.resolve(strict=True)
    except OSError as exc:
        parser.error(str(exc))
    if not repository.is_dir() or repository.is_symlink():
        parser.error("--root must be a non-symlink directory")
    if not source_root.is_dir() or args.source_root.is_symlink():
        parser.error("--source-root must be a non-symlink directory")
    try:
        if args.write:
            if not args.source:
                parser.error("--write requires at least one --source")
            value, writes = build_snapshot(repository, source_root, args.feature, args.source_id, args.source)
            for path, content in writes.items():
                atomic_write_text(repository, path, content)
            result = {"status": "written", "manifest": f"specs-refiniment/{args.feature}/external-specs.json", **value}
            exit_code = 0
        else:
            value, errors = check_snapshot(repository, source_root, args.feature, args.source_id)
            result = {"status": "current" if not errors else "drifted", "errors": errors, **value}
            exit_code = 0 if not errors else 1
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
