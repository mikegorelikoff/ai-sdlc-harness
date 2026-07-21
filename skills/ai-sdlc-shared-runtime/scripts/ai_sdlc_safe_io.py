#!/usr/bin/env python3
"""Repository-bounded path and atomic-write helpers with symlink rejection."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


def bounded_path(root: Path, path: Path) -> Path:
    """Return an absolute path below root, rejecting every symlink component."""
    lexical_root = Path(os.path.abspath(root))
    resolved_root = root.resolve(strict=True)
    candidate = path if path.is_absolute() else lexical_root / path
    candidate = Path(os.path.abspath(candidate))
    try:
        relative = candidate.relative_to(lexical_root)
    except ValueError:
        try:
            relative = candidate.relative_to(resolved_root)
        except ValueError:
            try:
                relative = candidate.resolve(strict=False).relative_to(resolved_root)
            except ValueError as exc:
                raise ValueError(f"output path escapes repository root: {path}") from exc
    root = resolved_root
    candidate = root / relative
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"output path contains symlink component: {current}")
    try:
        candidate.resolve(strict=False).relative_to(root)
    except ValueError as exc:
        raise ValueError(f"resolved output path escapes repository root: {path}") from exc
    return candidate


def ensure_directory(root: Path, path: Path) -> Path:
    """Create a bounded directory and verify it again after creation."""
    candidate = bounded_path(root, path)
    candidate.mkdir(parents=True, exist_ok=True)
    candidate = bounded_path(root, candidate)
    if not candidate.is_dir():
        raise ValueError(f"output directory is not a directory: {candidate}")
    return candidate


def atomic_write_text(root: Path, path: Path, content: str) -> None:
    """Atomically replace a bounded regular file without following symlinks."""
    candidate = bounded_path(root, path)
    parent = ensure_directory(root, candidate.parent)
    candidate = bounded_path(root, candidate)
    descriptor, temporary = tempfile.mkstemp(prefix=candidate.name + ".", dir=parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        bounded_path(root, candidate)
        os.replace(temporary, candidate)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
