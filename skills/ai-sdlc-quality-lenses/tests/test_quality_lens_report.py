#!/usr/bin/env python3
"""Tests for the reusable quality-lens report finalizer."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "ai-sdlc-quality-lenses" / "scripts" / "quality_lens_report.py"


class QualityLensReportTests(unittest.TestCase):
    """Registry, validation, and report output tests."""

    def run_report(self, *args: str) -> subprocess.CompletedProcess[str]:
        """Run the finalizer with captured output."""
        return subprocess.run(["python3", str(SCRIPT), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def fixture(self, root: Path, findings: object) -> tuple[Path, Path]:
        """Write a source artifact and findings fixture."""
        artifact = root / "requirements.md"
        artifact.write_text("# Requirements\nTimeout behavior is not specified.\n", encoding="utf-8")
        finding_file = root / "findings.json"
        finding_file.write_text(json.dumps(findings), encoding="utf-8")
        return artifact, finding_file

    def valid_finding(self) -> dict[str, object]:
        """Return one complete finding."""
        return {"id": "QL-001", "lens": "edge-case-hunt", "evidence": {"path": "requirements.md", "line": 2, "detail": "Timeout behavior is not specified."}, "severity": "high", "trace_targets": ["AC-004", "TC-012"], "owner": "BA", "resolution_status": "open", "next_action": "Define timeout acceptance behavior."}

    def test_registry_lists_all_reusable_lenses(self) -> None:
        """Discovery should expose stable registry identifiers."""
        result = self.run_report("--list-lenses", "--format", "toon")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("schema: ai-sdlc-quality-lens-registry/v1", result.stdout)
        self.assertIn("pre-mortem", result.stdout)
        self.assertIn("operational-failure-review", result.stdout)

    def test_complete_finding_writes_canonical_pair(self) -> None:
        """A complete finding should produce Markdown and TOON."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            artifact, findings = self.fixture(root, [self.valid_finding()])
            result = self.run_report("--artifact", str(artifact), "--artifact-kind", "requirements", "--feature", "payments", "--findings", str(findings), "--lens", "edge-case-hunt", "--write", "--output-root", str(root), "--format", "toon", "--quick-flow")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("QL-001", result.stdout)
            self.assertIn("AC-004/TC-012", result.stdout)
            self.assertTrue((root / "quality-lens-report.md").is_file())
            self.assertTrue((root / "_ai_sdlc/quality-lens-report.toon").is_file())

    def test_incomplete_finding_is_rejected_without_writes(self) -> None:
        """Missing ownership and next action must block finalization."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = self.valid_finding()
            value.pop("owner")
            value.pop("next_action")
            artifact, findings = self.fixture(root, [value])
            result = self.run_report("--artifact", str(artifact), "--findings", str(findings), "--lens", "edge-case-hunt", "--write", "--output-root", str(root))
            self.assertEqual(result.returncode, 1)
            self.assertIn("owner is required", result.stdout)
            self.assertIn("next_action is required", result.stdout)
            self.assertFalse((root / "quality-lens-report.md").exists())

    def test_full_flow_selects_all_applicable_lenses(self) -> None:
        """Full flow should select the complete applicable registry subset."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            artifact, findings = self.fixture(root, [])
            result = self.run_report("--artifact", str(artifact), "--artifact-kind", "requirements", "--findings", str(findings), "--emit", "--format", "toon", "--full-flow")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("abuse-case-review", result.stdout)
            self.assertNotIn("reversibility-check", result.stdout)


if __name__ == "__main__":
    unittest.main()
