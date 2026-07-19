#!/usr/bin/env python3
"""Per-skill script contract tests."""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "skills" / "_shared" / "skill_script_contract.py"


def load_contract():
    """Load the shared per-skill contract without relying on package imports."""
    spec = importlib.util.spec_from_file_location("skill_script_contract", CONTRACT)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules["skill_script_contract"] = module
    spec.loader.exec_module(module)
    return module


class SkillScriptContractTests(unittest.TestCase):
    """Per-skill wrapper around the shared script contract."""

    def test_skill_scripts_follow_contract(self) -> None:
        """Verify this skill's runtime scripts follow the repository contract."""
        load_contract().run_skill_script_contract(SKILL_DIR)

    def test_base_branch_resolution_handles_main_dev_detached_and_dirty(self) -> None:
        """Branch planning resolves declared defaults and reports unsafe tree states."""
        module_spec = importlib.util.spec_from_file_location("branch_plan", SKILL_DIR / "scripts/branch_plan.py")
        module = importlib.util.module_from_spec(module_spec)
        assert module_spec and module_spec.loader
        sys.modules["branch_plan"] = module
        module_spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, stdout=subprocess.PIPE)
            subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=root, check=True)
            subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=root, check=True)
            (root / "README.md").write_text("fixture\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "base"], cwd=root, check=True, stdout=subprocess.PIPE)
            self.assertEqual(module.resolve_base_branch(root)[0], "main")
            subprocess.run(["git", "branch", "dev"], cwd=root, check=True, stdout=subprocess.PIPE)
            subprocess.run(["git", "config", "ai-sdlc.baseBranch", "dev"], cwd=root, check=True)
            self.assertEqual(module.resolve_base_branch(root)[0], "dev")
            (root / "dirty.txt").write_text("dirty\n", encoding="utf-8")
            self.assertTrue(module.git_status(root))
            subprocess.run(["git", "checkout", "--detach"], cwd=root, check=True, stdout=subprocess.PIPE)
            self.assertEqual(module.resolve_base_branch(root)[0], "dev")


if __name__ == "__main__":
    unittest.main()
