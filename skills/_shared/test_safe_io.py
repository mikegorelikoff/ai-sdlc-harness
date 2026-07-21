#!/usr/bin/env python3
"""Tests for repository-bounded output helpers."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_sdlc_safe_io import atomic_write_text, bounded_path


class SafeIoTests(unittest.TestCase):
    def test_regular_bounded_write_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            atomic_write_text(root, root / "_ai_sdlc/result.txt", "ok\n")
            self.assertEqual((root / "_ai_sdlc/result.txt").read_text(), "ok\n")

    def test_traversal_and_symlink_parent_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            root = Path(temp)
            with self.assertRaises(ValueError):
                bounded_path(root, root / "../outside.txt")
            (root / "_ai_sdlc").symlink_to(Path(outside), target_is_directory=True)
            with self.assertRaises(ValueError):
                atomic_write_text(root, root / "_ai_sdlc/result.txt", "unsafe\n")
            self.assertFalse((Path(outside) / "result.txt").exists())


if __name__ == "__main__":
    unittest.main()
