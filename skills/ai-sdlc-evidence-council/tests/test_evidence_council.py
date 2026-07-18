#!/usr/bin/env python3
"""Tests for authority-safe evidence council reports."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-evidence-council/scripts/evidence_council.py"


class CouncilTests(unittest.TestCase):
    """Mode, evidence, authority, and synthesis tests."""

    def value(self, mode: str = "independent") -> dict[str, object]:
        """Return valid full-flow council input."""
        panel = [{"id": "REV-ARCH", "role": "architecture", "execution": mode, "execution_id": "run-a" if mode == "independent" else "sim-a"}, {"id": "REV-QA", "role": "qa", "execution": mode, "execution_id": "run-b" if mode == "independent" else "sim-b"}, {"id": "REV-UX", "role": "ux", "execution": mode, "execution_id": "run-c" if mode == "independent" else "sim-c"}]
        return {"schema": "ai-sdlc-evidence-council-input/v1", "topic": "Approve retry recovery design", "mode": mode, "authority": {"owner": "Delivery", "authoritative_artifacts": ["requirements.md"]}, "panel": panel, "evidence": [{"id": "EV-001", "path": "requirements.md", "line": 2, "detail": "AC-007 requires durable retry.", "trace_targets": ["AC-007"]}], "agreements": [{"id": "AGR-001", "statement": "Durable scheduling is required.", "reviewers": ["REV-ARCH", "REV-QA"], "evidence_ids": ["EV-001"]}], "conflicts": [{"id": "CON-001", "statement": "Retry visibility depth differs.", "positions": ["event history", "latest status only"], "reviewers": ["REV-QA", "REV-UX"], "evidence_ids": ["EV-001"], "owner": "PM", "next_action": "Choose visibility scope."}], "proposals": [{"id": "PRO-001", "statement": "Add bounded retry history.", "reviewers": ["REV-UX"], "evidence_ids": ["EV-001"], "owner": "PM", "status": "review-needed", "next_action": "Review with users."}], "unresolved_questions": [{"id": "QUE-001", "question": "What retention is permitted?", "reviewers": ["REV-ARCH"], "evidence_ids": ["EV-001"], "owner": "Security", "next_action": "Confirm policy."}]}

    def run_council(self, root: Path, path: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run council finalization."""
        return subprocess.run(["python3", str(SCRIPT), str(root), "--input", str(path), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def fixture(self, root: Path, mode: str = "independent") -> Path:
        """Write authority evidence and input."""
        (root / "requirements.md").write_text("# Requirements\nAC-007 requires durable retry.\n", encoding="utf-8")
        path = root / "council.json"
        path.write_text(json.dumps(self.value(mode)), encoding="utf-8")
        return path

    def test_independent_report_writes_routed_pair(self) -> None:
        """Valid isolated panel records should synthesize all outcome types."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.fixture(root)
            result = self.run_council(root, path, "--write", "--full-flow", "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for section in ("agreements[1]", "conflicts[1]", "proposals[1]", "unresolved_questions[1]"):
                self.assertIn(section, result.stdout)
            self.assertTrue((root / "evidence-council.md").is_file())
            self.assertTrue((root / "_ai_sdlc/evidence-council.toon").is_file())

    def test_independent_mode_rejects_duplicate_execution_ids(self) -> None:
        """Role labels alone must not masquerade as independent execution."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = self.value()
            for reviewer in value["panel"]:  # type: ignore[index]
                reviewer["execution_id"] = "same-run"
            (root / "requirements.md").write_text("# R\nAC-007\n", encoding="utf-8")
            path = root / "council.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_council(root, path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("execution IDs must be unique", result.stdout)

    def test_council_cannot_accept_proposal(self) -> None:
        """Council recommendations cannot claim owner acceptance."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = self.value("simulated")
            value["proposals"][0]["status"] = "accepted"  # type: ignore[index]
            (root / "requirements.md").write_text("# R\nAC-007\n", encoding="utf-8")
            path = root / "council.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_council(root, path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("cannot imply acceptance", result.stdout)

    def test_write_preserves_authoritative_artifact(self) -> None:
        """Finalization may write reports but never panel source targets."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.fixture(root, "simulated")
            authority = root / "requirements.md"
            before = authority.read_bytes()
            result = self.run_council(root, path, "--write", "--quick-flow")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(authority.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
