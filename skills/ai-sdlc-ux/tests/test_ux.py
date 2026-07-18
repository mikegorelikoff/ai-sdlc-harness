#!/usr/bin/env python3
"""Tests for the optional UX capability."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-ux/scripts/ux.py"


class UXTests(unittest.TestCase):
    """Actor, journey, state, accessibility, and routing tests."""

    def value(self) -> dict[str, object]:
        """Return valid full-flow UX input."""
        return {"schema": "ai-sdlc-ux-input/v1", "context": "Retry status for account administrators.", "actors": [{"id": "ACT-001", "name": "Administrator", "goals": ["recover failed payment"], "needs": ["clear status"]}], "journeys": [{"id": "JRN-001", "actor": "ACT-001", "goal": "Retry a failed payment", "steps": ["Open failure", "Review reason", "Confirm retry"], "acceptance": "Retry status and result are announced.", "trace_targets": ["AC-012"]}], "states": [{"surface": "retry panel", "state": "failed", "behavior": "Show reason and safe retry action.", "recovery": "Allow retry when permission and policy permit.", "trace_targets": ["AC-012", "TC-022"]}], "accessibility": [{"requirement": "Status changes use a live region.", "evidence": "Planned automated and screen-reader check.", "status": "planned", "trace_targets": ["NFR-006"]}], "content": [{"surface": "retry confirmation", "intent": "Explain irreversible effect.", "guidance": "Name payment and amount."}]}

    def run_ux(self, root: Path, path: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run UX finalization."""
        return subprocess.run(["python3", str(SCRIPT), str(root), "--input", str(path), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_full_ux_writes_routed_pair(self) -> None:
        """Valid UX input should create both canonical outputs."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "ux.json"
            path.write_text(json.dumps(self.value()), encoding="utf-8")
            result = self.run_ux(root, path, "--write", "--full-flow", "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("schema: ai-sdlc-ux/v1", result.stdout)
            self.assertIn("JRN-001,ACT-001", result.stdout)
            self.assertTrue((root / "ux-spec.md").is_file())
            self.assertTrue((root / "_ai_sdlc/ux-spec.toon").is_file())

    def test_unknown_journey_actor_is_rejected(self) -> None:
        """Journey ownership cannot point to an invented actor."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = self.value()
            value["journeys"][0]["actor"] = "ACT-999"  # type: ignore[index]
            path = root / "ux.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_ux(root, path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("known actor", result.stdout)

    def test_full_flow_requires_states_and_accessibility(self) -> None:
        """Strict UX cannot describe only the happy path."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = self.value()
            value["states"], value["accessibility"] = [], []
            path = root / "ux.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_ux(root, path, "--full-flow")
            self.assertEqual(result.returncode, 1)
            self.assertIn("full flow requires at least one states entry", result.stdout)
            self.assertIn("full flow requires at least one accessibility entry", result.stdout)


if __name__ == "__main__":
    unittest.main()
