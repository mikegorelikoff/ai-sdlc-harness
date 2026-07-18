#!/usr/bin/env python3
"""Tests for the normalized workflow handoff contract."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "_shared" / "ai_sdlc_handoff.py"


class HandoffTests(unittest.TestCase):
    """Handoff schema and adoption tests."""

    def run_handoff(self, *args: str) -> subprocess.CompletedProcess[str]:
        """Run the handoff emitter."""
        return subprocess.run(["python3", str(SCRIPT), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_complete_toon_contains_all_contract_fields(self) -> None:
        """A complete handoff should expose required and optional action fields."""
        result = self.run_handoff(
            "--result", "complete", "--summary", "Navigator delivered",
            "--next-required", "ai-sdlc-validation|Validate the diff|Use validation|validation evidence",
            "--next-optional", "ai-sdlc-security-testing|Review trust boundaries|Use security testing|security-review.md",
            "--format", "toon",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("schema: ai-sdlc-handoff/v1", result.stdout)
        self.assertIn("next_required[1]{skill,reason,command,expected_artifact}", result.stdout)
        self.assertIn("next_optional[1]{skill,reason,command,expected_artifact}", result.stdout)
        self.assertIn("blockers[0]{message}", result.stdout)

    def test_blocked_handoff_requires_a_blocker(self) -> None:
        """A blocked result without blocker evidence must fail."""
        result = self.run_handoff(
            "--result", "blocked", "--summary", "Cannot continue",
            "--next-required", "ai-sdlc-ba|Resolve context|Use BA|business-context.md",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("blocked result requires", result.stdout)

    def test_every_skill_documents_handoff_contract(self) -> None:
        """Every installed skill should expose the common post-workflow contract."""
        for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=skill):
                text = skill.read_text(encoding="utf-8")
                self.assertIn("ai-sdlc-handoff/v1", text)
                self.assertIn("next_required", text)
                self.assertIn("next_optional", text)


if __name__ == "__main__":
    unittest.main()
