#!/usr/bin/env python3
"""Per-skill script contract tests."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "skills" / "_shared" / "skill_script_contract.py"


class SkillScriptContractTests(unittest.TestCase):
    """Per-skill wrapper around the shared script contract."""

    def test_skill_scripts_follow_contract(self) -> None:
        """Verify this skill's runtime scripts follow the repository contract."""
        result = subprocess.run(
            [sys.executable, str(CONTRACT), str(SKILL_DIR)],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
