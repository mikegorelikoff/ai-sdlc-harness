#!/usr/bin/env python3
"""Focused tests for prospective SDD commit traceability."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_commit_msg.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_commit_msg", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TraceabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def test_traced_message_requires_task(self) -> None:
        message = "feat(api): add endpoint\n\nSpec: specs/001-api\n\nValidation:\n- tests passed"
        self.assertIn(
            "body must include Task traceability as Task: TNNN",
            self.validator.validate(message, True),
        )

    def test_traced_message_accepts_one_or_more_canonical_tasks(self) -> None:
        for task_line in ("Task: T001", "Task: T001, T002"):
            with self.subTest(task_line=task_line):
                message = (
                    "feat(api): add endpoint\n\n"
                    "Spec: specs/001-api\n"
                    f"{task_line}\n\n"
                    "Validation:\n- tests passed"
                )
                self.assertEqual([], self.validator.validate(message, True))

    def test_task_reference_must_be_canonical(self) -> None:
        message = (
            "feat(api): add endpoint\n\n"
            "Spec: specs/001-api\n"
            "Task: task one\n\n"
            "Validation:\n- tests passed"
        )
        self.assertIn(
            "body must include Task traceability as Task: TNNN",
            self.validator.validate(message, True),
        )


if __name__ == "__main__":
    unittest.main()
