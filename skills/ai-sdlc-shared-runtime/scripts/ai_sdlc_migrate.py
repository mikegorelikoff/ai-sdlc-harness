#!/usr/bin/env python3
"""Check or apply safe migrations from legacy AI SDLC paths to canonical paths."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from ai_sdlc_artifact_profiles import PROFILES
from ai_sdlc_paths import (
    INTERNAL_DIR,
    index_toon_path,
    legacy_index_toon_path,
    legacy_plan_toon_path,
    legacy_state_path,
    plan_toon_path,
    state_path,
)
from ai_sdlc_safe_io import bounded_path


@dataclass(frozen=True)
class MigrationResult:
    action: str
    canonical: Path
    legacy: Path
    detail: str


class MigrationConflict(ValueError):
    """Raised when canonical and legacy files diverge."""


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def migrate_pair(canonical: Path, legacy: Path, *, apply: bool) -> MigrationResult | None:
    """Migrate one file without ever overwriting divergent content."""
    if not legacy.is_file():
        return None
    if canonical.is_file():
        if _digest(canonical) != _digest(legacy):
            raise MigrationConflict(f"divergent canonical/legacy files: {canonical} <> {legacy}")
        if apply:
            legacy.unlink()
        return MigrationResult("deduplicate", canonical, legacy, "content is identical")
    if apply:
        canonical.parent.mkdir(parents=True, exist_ok=True)
        os.replace(legacy, canonical)
    return MigrationResult("move", canonical, legacy, "canonical file is missing")


def migrate_feature(root: Path, feature: str, workspace: str, *, apply: bool) -> list[MigrationResult]:
    """Check or migrate one feature's known legacy machine and Markdown paths."""
    root = root.resolve()
    results: list[MigrationResult] = []
    pairs = [(state_path(feature, workspace, root), legacy_state_path(feature, workspace, root))]
    feature_root = root / ("specs" if workspace == "implementation" else "specs-refiniment") / feature
    if workspace == "implementation":
        pairs.append((plan_toon_path(feature_root), legacy_plan_toon_path(feature_root)))
    else:
        for profile in PROFILES:
            for legacy_name in profile.legacy_names:
                pairs.append((feature_root / profile.artifact_name, feature_root / legacy_name))
    for canonical, legacy in pairs:
        bounded_path(root, canonical)
        bounded_path(root, legacy)
        result = migrate_pair(canonical, legacy, apply=apply)
        if result:
            results.append(result)

    legacy_context = feature_root / ".ai-sdlc" / "context"
    canonical_context = feature_root / INTERNAL_DIR / "context"
    if legacy_context.is_dir():
        for legacy in sorted(legacy_context.glob("*.toon")):
            result = migrate_pair(canonical_context / legacy.name, legacy, apply=apply)
            if result:
                results.append(result)
        if apply and legacy_context.exists() and not any(legacy_context.iterdir()):
            legacy_context.rmdir()
            parent = legacy_context.parent
            if parent.exists() and not any(parent.iterdir()):
                parent.rmdir()
    return results


def migrate_workspace(root: Path, workspace: str, *, apply: bool) -> list[MigrationResult]:
    """Check or migrate an entire workspace, including its TOON index."""
    workspace_root = root / ("specs" if workspace == "implementation" else "specs-refiniment")
    results: list[MigrationResult] = []
    result = migrate_pair(index_toon_path(workspace_root), legacy_index_toon_path(workspace_root), apply=apply)
    if result:
        results.append(result)
    if workspace_root.is_dir():
        for feature_dir in sorted(path for path in workspace_root.iterdir() if path.is_dir() and path.name != INTERNAL_DIR):
            results.extend(migrate_feature(root, feature_dir.name, workspace, apply=apply))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--workspace", choices=["all", "refinement", "implementation"], default="all")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    workspaces = ("refinement", "implementation") if args.workspace == "all" else (args.workspace,)
    try:
        results = [item for workspace in workspaces for item in migrate_workspace(args.root.resolve(), workspace, apply=args.apply)]
    except MigrationConflict as exc:
        print(f"MIGRATION CONFLICT: {exc}", file=sys.stderr)
        return 2
    for result in results:
        print(f"{result.action}: {result.legacy} -> {result.canonical} ({result.detail})")
    print(f"Migration {'applied' if args.apply else 'check'}: {len(results)} action(s)")
    return 1 if args.check and results else 0


if __name__ == "__main__":
    raise SystemExit(main())
