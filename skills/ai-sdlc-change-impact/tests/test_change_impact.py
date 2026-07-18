#!/usr/bin/env python3
"""Tests for evidence-backed change impact and lifecycle recovery."""

from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "ai-sdlc-change-impact" / "scripts" / "change_impact.py"


def write(path: Path, content: str) -> None:
    """Write one dedented fixture file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


class ChangeImpactTests(unittest.TestCase):
    """Source evidence, trace scan, and recovery plan tests."""

    def run_impact(self, root: Path, changes: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run the analyzer with captured output."""
        return subprocess.run(["python3", str(SCRIPT), str(root), "--changes", str(changes), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def fixture(self, root: Path) -> Path:
        """Create a complete feature fixture with traced downstream artifacts."""
        write(root / "requirements.md", """
        ---
        artifact_metadata:
          skill: "ai-sdlc-sdd"
        ---
        # Requirements
        - AC-007: Retry behavior is mandatory.
        """)
        write(root / "design.md", """
        ---
        artifact_metadata:
          skill: "ai-sdlc-sdd"
        ---
        # Design
        The retry queue implements AC-007 with fixed backoff.
        """)
        write(root / "validation.md", """
        ---
        artifact_metadata:
          skill: "ai-sdlc-validation"
        ---
        # Validation
        AC-007 is covered by the retry integration check.
        """)
        write(root / "_ai_sdlc/state.toon", """
        feature: retry
        workspace: implementation
        current_stage: validation
        active_skill:
        flow_mode: full
        updated_at: 2026-07-18
        decision_log: specs/retry/decision-log.md

        stages[2]{id,skill,status,workspace,artifacts,decision_ref}:
          sdd,ai-sdlc-sdd,done,implementation,specs/retry,DEC-001
          validation,ai-sdlc-validation,done,implementation,validation.md,DEC-002

        skips[0]{stage,reason,decision_ref,flow_mode}:
        """)
        changes = {"schema": "ai-sdlc-change-set/v1", "changes": [{"id": "CHG-001", "changed_ref": "AC-007", "source": {"path": "requirements.md", "line": 6, "detail": "Backoff is now configurable."}}]}
        path = root / "changes.json"
        path.write_text(json.dumps(changes), encoding="utf-8")
        return path

    def test_change_maps_stale_artifacts_and_ordered_reopen_actions(self) -> None:
        """Exact traces should produce evidence-backed stage recovery."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            changes = self.fixture(root)
            result = self.run_impact(root, changes, "--emit", "--format", "toon", "--full-flow")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("design.md", result.stdout)
            self.assertIn("validation.md", result.stdout)
            self.assertIn("sdd,ai-sdlc-sdd,done,reopen,AC-007", result.stdout)
            self.assertIn("validation,ai-sdlc-validation,done,reopen,AC-007", result.stdout)
            self.assertLess(result.stdout.index("sdd,ai-sdlc-sdd"), result.stdout.index("validation,ai-sdlc-validation"))

    def test_invalid_source_evidence_blocks_analysis(self) -> None:
        """A source line without the changed ref must fail evidence gates."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            changes = self.fixture(root)
            value = json.loads(changes.read_text(encoding="utf-8"))
            value["changes"][0]["source"]["line"] = 1
            changes.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_impact(root, changes, "--full-flow")
            self.assertEqual(result.returncode, 1)
            self.assertIn("does not contain changed_ref", result.stdout)

    def test_write_does_not_mutate_state_or_source(self) -> None:
        """Report writes must leave authoritative files unchanged."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            changes = self.fixture(root)
            state = root / "_ai_sdlc/state.toon"
            requirements = root / "requirements.md"
            before = (state.read_bytes(), requirements.read_bytes())
            result = self.run_impact(root, changes, "--write", "--quick-flow")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(before, (state.read_bytes(), requirements.read_bytes()))
            self.assertTrue((root / "change-impact.md").is_file())
            self.assertTrue((root / "_ai_sdlc/change-impact.toon").is_file())

    def test_full_flow_requires_state(self) -> None:
        """Strict analysis must not guess lifecycle ownership status."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            changes = self.fixture(root)
            (root / "_ai_sdlc/state.toon").unlink()
            result = self.run_impact(root, changes, "--full-flow")
            self.assertEqual(result.returncode, 1)
            self.assertIn("canonical state missing", result.stdout)


if __name__ == "__main__":
    unittest.main()
