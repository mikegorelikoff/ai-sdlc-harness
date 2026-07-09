#!/usr/bin/env python3
"""Run every per-skill test file from a stable repository-level command.

Python's normal unittest discovery does not reliably descend into directories
whose names contain hyphens. This runner executes each skill's test file by path
so the repository has one command that validates the full per-skill layout.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class PerSkillTestFiles(unittest.TestCase):
    """Runner tests for every skill-local test file."""

    def test_every_skill_test_file_passes(self) -> None:
        """Execute every `skills/<skill>/tests/test*.py` file directly."""
        test_files = sorted((ROOT / "skills").glob("*/tests/test*.py"))
        self.assertGreaterEqual(len(test_files), 26)
        for test_file in test_files:
            with self.subTest(test_file=test_file.relative_to(ROOT)):
                # Run each test file as a script to avoid import-name issues from
                # hyphenated skill directory names.
                result = subprocess.run(
                    [sys.executable, str(test_file)],
                    cwd=ROOT,
                    check=False,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
