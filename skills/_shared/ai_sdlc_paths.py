#!/usr/bin/env python3
"""Canonical and legacy paths for AI SDLC machine-readable artifacts."""

from __future__ import annotations

from pathlib import Path


INTERNAL_DIR = "_ai_sdlc"
INDEX_TOON = "specs-index.toon"


def workspace_base(workspace: str) -> str:
    """Return the visible artifact root for a lifecycle workspace."""
    return "specs" if workspace == "implementation" else "specs-refiniment"


def feature_dir(feature: str, workspace: str, root: Path | None = None) -> Path:
    """Return one feature's visible artifact directory."""
    prefix = root or Path()
    return prefix / workspace_base(workspace) / feature


def internal_dir(feature_root: Path) -> Path:
    """Return the feature-local directory for machine-readable artifacts."""
    return feature_root / INTERNAL_DIR


def state_path(feature: str, workspace: str, root: Path | None = None) -> Path:
    """Return the canonical lifecycle state path."""
    return internal_dir(feature_dir(feature, workspace, root)) / "state.toon"


def legacy_state_path(feature: str, workspace: str, root: Path | None = None) -> Path:
    """Return the pre-_ai_sdlc lifecycle state path."""
    return feature_dir(feature, workspace, root) / "state.toon"


def plan_toon_path(spec_dir: Path) -> Path:
    """Return the canonical SDD machine plan path."""
    return internal_dir(spec_dir) / "plan.toon"


def legacy_plan_toon_path(spec_dir: Path) -> Path:
    """Return the pre-_ai_sdlc SDD machine plan path."""
    return spec_dir / "plan.toon"


def index_toon_path(workspace_root: Path) -> Path:
    """Return the canonical workspace-level TOON index path."""
    return workspace_root / INTERNAL_DIR / INDEX_TOON


def legacy_index_toon_path(workspace_root: Path) -> Path:
    """Return the pre-_ai_sdlc workspace-level TOON index path."""
    return workspace_root / INDEX_TOON


def context_cache_path(workspace_root: Path, feature: str, skill: str) -> Path:
    """Return the canonical feature-local context-cache path."""
    return workspace_root / feature / INTERNAL_DIR / "context" / f"{skill}.toon"


def feature_context_path(workspace_root: Path, feature: str) -> Path:
    """Return the canonical feature-wide context dossier path."""
    return workspace_root / feature / INTERNAL_DIR / "feature-context.toon"


def legacy_context_cache_path(workspace_root: Path, feature: str, skill: str) -> Path:
    """Return the pre-_ai_sdlc feature-local context-cache path."""
    return workspace_root / feature / ".ai-sdlc" / "context" / f"{skill}.toon"


def first_existing(canonical: Path, *legacy: Path) -> Path:
    """Prefer the canonical path, falling back to an existing legacy path."""
    if canonical.is_file():
        return canonical
    for candidate in legacy:
        if candidate.is_file():
            return candidate
    return canonical
