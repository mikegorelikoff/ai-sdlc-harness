#!/usr/bin/env python3
"""Security regression tests for approval-plan normalization."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/approval_plan.py"
SPEC = importlib.util.spec_from_file_location("approval_plan", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ApprovalPlanSecurityTests(unittest.TestCase):
    def test_destructive_variants_never_receive_reusable_prefix(self) -> None:
        for command in (
            "git -C /tmp/example reset --hard", "/bin/rm -rf /tmp/example", "git --work-tree=/tmp clean -fd",
            "env FOO=1 git reset --hard", "/usr/bin/env git clean -fd", "command git reset --hard",
            "git -c 'alias.wipe=reset --hard' wipe", "git push origin +main", "git push origin :main",
        ):
            with self.subTest(command=command):
                errors, warnings = MODULE.validate(command, "Do you want to allow this destructive operation?", "git reset")
                self.assertTrue(any("prefix_rule" in item for item in errors))
                self.assertTrue(any("destructive" in item for item in warnings))

    def test_common_environment_secret_is_rejected(self) -> None:
        errors, _ = MODULE.validate(
            "AWS_SECRET_ACCESS_KEY=abcdefghijklmnopqrstuv command",
            "Do you want to run the requested external command?",
            None,
        )
        self.assertTrue(any("secret" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
