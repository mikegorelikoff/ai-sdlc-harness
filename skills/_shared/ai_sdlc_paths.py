#!/usr/bin/env python3
"""Canonical and legacy paths for AI SDLC machine-readable artifacts."""

from __future__ import annotations

import os
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

try:  # pragma: no cover - platform-specific import
    import fcntl
except ImportError:  # pragma: no cover
    fcntl = None  # type: ignore[assignment]
try:  # pragma: no cover - platform-specific import
    import msvcrt
except ImportError:  # pragma: no cover
    msvcrt = None  # type: ignore[assignment]


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


def atomic_write_text(path: Path, text: str) -> None:
    """Replace one UTF-8 file atomically without exposing partial content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            handle.write(text)
            temp_path = Path(handle.name)
        os.replace(temp_path, path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


@contextmanager
def write_lock(scope: Path, timeout: float = 10.0) -> Iterator[None]:
    """Serialize writers with an OS lock released automatically on process exit."""
    lock = scope / ".write.lock"
    scope.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout
    with lock.open("a+", encoding="utf-8") as handle:
        if msvcrt is not None:
            handle.seek(0)
            if not handle.read(1):
                handle.write("0")
                handle.flush()
        while True:
            try:
                if fcntl is not None:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                elif msvcrt is not None:  # pragma: no cover - Windows only
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:  # pragma: no cover
                    raise RuntimeError("no supported file-lock implementation")
                break
            except (BlockingIOError, OSError):
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"timed out waiting for write lock: {lock}")
                time.sleep(0.05)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            elif msvcrt is not None:  # pragma: no cover - Windows only
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
