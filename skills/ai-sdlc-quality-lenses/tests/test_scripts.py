#!/usr/bin/env python3
"""Per-skill script contract tests."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "skills" / "_shared" / "skill_script_contract.py"


class SkillScriptContractTests(unittest.TestCase):
    """Verify quality-lens scripts follow repository contracts."""

    def test_skill_scripts_follow_contract(self) -> None:
        """Run the shared script contract."""
        spec = importlib.util.spec_from_file_location("skill_script_contract", CONTRACT)
        module = importlib.util.module_from_spec(spec)
        assert spec is not None and spec.loader is not None
        sys.modules["skill_script_contract"] = module
        spec.loader.exec_module(module)
        module.run_skill_script_contract(SKILL_DIR)


if __name__ == "__main__":
    unittest.main()
