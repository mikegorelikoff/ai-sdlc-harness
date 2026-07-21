"""Forward tests for the installable AI SDLC shared runtime."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "skills"
SYNC = SKILLS / "_shared" / "sync_installed_runtime.py"
INSTALL_SMOKE = SKILLS / "_shared" / "ai_sdlc_install_smoke.py"


class InstalledRuntimeTests(unittest.TestCase):
    """Prove scripts work after skill-only installation, without source shared."""

    def test_generated_runtime_matches_canonical_helpers(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SYNC), "--check"],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("20 canonical helpers", result.stdout)

    def test_sdd_scaffold_runs_from_skill_only_installation(self) -> None:
        result = subprocess.run(
            [sys.executable, str(INSTALL_SMOKE), "--mode", "emulated"],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("installed runtime, complete SDD gates, and commit readiness passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
