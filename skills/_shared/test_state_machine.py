#!/usr/bin/env python3
"""Tests for feature state.toon lifecycle enforcement."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import ai_sdlc_state_machine as sm


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "skills" / "_shared" / "state_machine.py"


class StateMachineTests(unittest.TestCase):
    """Unit and CLI tests for the AI SDLC state machine."""

    def test_toon_round_trip_preserves_stage_rows(self) -> None:
        """Serialized TOON should parse back into equivalent core fields."""
        state = sm.initial_state("demo-feature", "refinement", "discovery")
        text = sm.to_toon(state)
        parsed = sm.from_toon(text)
        self.assertEqual(parsed["feature"], "demo-feature")
        self.assertEqual(parsed["current_stage"], "discovery")
        self.assertEqual(len(parsed["stages"]), len(state["stages"]))

    def test_full_flow_blocks_missing_predecessors(self) -> None:
        """Full flow should reject a downstream skill with incomplete predecessors."""
        state = sm.initial_state("demo-feature", "refinement", "discovery")
        errors, warnings = sm.validate_transition(state, "ai-sdlc-test-scope-and-strategy-design", "full")
        self.assertTrue(errors)
        self.assertFalse(warnings)

    def test_quick_flow_allows_skip_only_with_trace(self) -> None:
        """Quick flow can skip predecessors only with assumption or decision trace."""
        state = sm.initial_state("demo-feature", "refinement", "discovery")
        errors_without_trace, _ = sm.validate_transition(state, "ai-sdlc-test-scope-and-strategy-design", "quick")
        errors_with_trace, warnings = sm.validate_transition(
            state,
            "ai-sdlc-test-scope-and-strategy-design",
            "quick",
            decision_ref="DEC-001",
        )
        self.assertTrue(errors_without_trace)
        self.assertFalse(errors_with_trace)
        self.assertTrue(warnings)

    def test_begin_and_complete_update_state(self) -> None:
        """Begin/complete should lock and then release the active skill."""
        state = sm.initial_state("demo-feature", "refinement", "discovery")
        errors, _ = sm.begin_stage(state, "ai-sdlc-working-backwards-discovery", "full")
        self.assertFalse(errors)
        self.assertEqual(state["active_skill"], "ai-sdlc-working-backwards-discovery")
        errors, _ = sm.complete_stage(
            state,
            "ai-sdlc-working-backwards-discovery",
            "specs-refiniment/demo-feature/discovery.md",
            "DEC-001",
            "full",
        )
        self.assertFalse(errors)
        self.assertEqual(state["active_skill"], "")
        self.assertEqual(sm.stage_row(state, "discovery")["status"], "done")

    def test_cli_init_and_status(self) -> None:
        """The CLI should create a state file and print TOON status."""
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            cwd = Path(temp_dir)
            init = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "init",
                    "--feature",
                    "cli-demo",
                    "--workspace",
                    "refinement",
                ],
                cwd=cwd,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            self.assertTrue((cwd / "specs-refiniment/cli-demo/state.toon").is_file())

            status = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "status",
                    "--feature",
                    "cli-demo",
                    "--workspace",
                    "refinement",
                ],
                cwd=cwd,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("feature: cli-demo", status.stdout)
            self.assertIn("stages[", status.stdout)


if __name__ == "__main__":
    unittest.main()
