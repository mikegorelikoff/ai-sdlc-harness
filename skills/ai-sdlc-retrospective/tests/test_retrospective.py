#!/usr/bin/env python3
"""Tests for governed retrospective learning."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-retrospective" / "scripts/retrospective.py"


class RetrospectiveTests(unittest.TestCase):
    """Observation, proposal, decision, and mutation safety tests."""

    def run_retro(self, root: Path, input_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run the finalizer with captured output."""
        return subprocess.run(["python3", str(SCRIPT), str(root), "--input", str(input_path), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def fixture(self, root: Path, status: str = "proposed", decision_ref: str = "") -> Path:
        """Create evidence, protected policy target, and retrospective input."""
        (root / "validation.md").write_text("# Validation\nRetry fixture failed twice before passing.\n", encoding="utf-8")
        policy = root / "policy.json"
        policy.write_text('{"retry": false}\n', encoding="utf-8")
        value = {"schema": "ai-sdlc-retrospective-input/v1", "observations": [{"id": "OBS-001", "category": "friction", "statement": "Retry behavior caused repeated manual validation.", "evidence": {"path": "validation.md", "line": 2, "detail": "Two failed attempts were recorded."}}], "proposals": [{"id": "PROP-001", "based_on": ["OBS-001"], "target": "policy.json", "change": "Add a retry fixture.", "owner": "QA", "status": status, "decision_ref": decision_ref, "next_action": "Review with the validation owner."}]}
        path = root / "retro.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_observations_and_proposals_are_separate_in_outputs(self) -> None:
        """Valid learning should retain separate report collections."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_path = self.fixture(root)
            result = self.run_retro(root, input_path, "--emit", "--format", "toon", "--quick-flow")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("observations[1]", result.stdout)
            self.assertIn("proposals[1]", result.stdout)
            self.assertIn("PROP-001,OBS-001,policy.json", result.stdout)

    def test_accepted_proposal_requires_decision(self) -> None:
        """Acceptance must never be inferred without durable authority."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_path = self.fixture(root, status="accepted")
            result = self.run_retro(root, input_path, "--full-flow")
            self.assertEqual(result.returncode, 1)
            self.assertIn("accepted status requires decision_ref", result.stdout)

    def test_write_preserves_policy_target(self) -> None:
        """Finalization must not apply even an accepted proposal."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_path = self.fixture(root, status="accepted", decision_ref="DEC-014")
            policy = root / "policy.json"
            before = policy.read_bytes()
            result = self.run_retro(root, input_path, "--write", "--full-flow")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(policy.read_bytes(), before)
            self.assertTrue((root / "retrospective.md").is_file())
            self.assertTrue((root / "_ai_sdlc/retrospective.toon").is_file())

    def test_unknown_observation_reference_is_rejected(self) -> None:
        """Every proposal must trace to observed evidence."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_path = self.fixture(root)
            value = json.loads(input_path.read_text(encoding="utf-8"))
            value["proposals"][0]["based_on"] = ["OBS-999"]
            input_path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_retro(root, input_path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("known observation IDs", result.stdout)


if __name__ == "__main__":
    unittest.main()
