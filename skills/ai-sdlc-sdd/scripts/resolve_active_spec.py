#!/usr/bin/env python3
"""Resolve the active AI SDLC feature spec from explicit, changed, or branch context."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from spec_helpers import ROOT, resolve_active_spec


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", nargs="?", help="Explicit spec directory or path")
    parser.add_argument("--branch", help="Branch name override")
    parser.add_argument("--files", nargs="*", help="Changed-file context override")
    args = parser.parse_args()

    try:
        result = resolve_active_spec(
            root=ROOT,
            explicit=args.spec,
            files=args.files,
            branch=args.branch,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    relative = result.spec_dir.relative_to(ROOT)
    print(f"{relative} [{result.source}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
