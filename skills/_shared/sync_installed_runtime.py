#!/usr/bin/env python3
"""Synchronize the installable shared-runtime skill with canonical helpers."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "skills" / "_shared"
TARGET = ROOT / "skills" / "ai-sdlc-shared-runtime" / "scripts"
EXCLUDED = {"ai_sdlc_install_smoke.py", "sync_installed_runtime.py"}


def source_files() -> list[Path]:
    """Return canonical non-test runtime helpers in stable order."""
    return sorted(
        path
        for path in SOURCE.glob("*.py")
        if not path.name.startswith("test_") and path.name not in EXCLUDED
    )


def drift() -> list[str]:
    """Return missing, stale, or unexpected mirror entries."""
    errors: list[str] = []
    expected = {path.name: path for path in source_files()}
    actual = {path.name: path for path in TARGET.glob("*.py")} if TARGET.is_dir() else {}
    for name, source in expected.items():
        target = actual.get(name)
        if target is None:
            errors.append(f"missing runtime mirror: {name}")
        elif target.read_bytes() != source.read_bytes():
            errors.append(f"stale runtime mirror: {name}")
    for name in sorted(set(actual) - set(expected)):
        errors.append(f"unexpected runtime mirror: {name}")
    return errors


def synchronize() -> None:
    """Replace the generated mirror with canonical source bytes."""
    TARGET.mkdir(parents=True, exist_ok=True)
    expected = {path.name for path in source_files()}
    for path in TARGET.glob("*.py"):
        if path.name not in expected:
            path.unlink()
    for source in source_files():
        shutil.copyfile(source, TARGET / source.name)


def main() -> int:
    """Check or write the installable shared-runtime mirror."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when generated runtime bytes drift")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    args = parser.parse_args()

    if args.begin_state or args.complete_state:
        print("ERROR: runtime synchronization cannot mutate feature state")
        return 1
    if not args.check:
        synchronize()
    errors = drift()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Installed runtime ready: {len(source_files())} canonical helpers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
