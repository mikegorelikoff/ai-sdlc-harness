#!/usr/bin/env python3
"""Tests for release compatibility and roadmap commit auditing."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/_shared/ai_sdlc_compatibility.py"
BASELINE = ROOT / "compatibility/baseline-v1.json"


class CompatibilityTests(unittest.TestCase):
    """Baseline, breaking fixture, and Git audit tests."""

    def run_check(self, *args: str) -> subprocess.CompletedProcess[str]:
        """Run compatibility validation with captured output."""
        return subprocess.run(["python3", str(SCRIPT), "--root", str(ROOT), *args], cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_current_release_matches_baseline(self) -> None:
        """The default complete TOON result should expose protected contracts."""
        result = self.run_check("--skip-git-audit")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("result: compatible", result.stdout)
        self.assertIn("protected_skill_names", result.stdout)
        self.assertIn("protected_cli_flags", result.stdout)
        self.assertIn("protected_routes", result.stdout)
        expected = len(list((ROOT / "skills").glob("*/SKILL.md")))
        self.assertIn(f"skills: {expected}", result.stdout)

    def test_missing_skill_breaks_baseline(self) -> None:
        """A required skill rename or removal must fail mechanically."""
        with tempfile.TemporaryDirectory() as temp:
            baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
            baseline["required_skill_names"].append("ai-sdlc-removed")
            baseline["required_skill_names"].sort()
            path = Path(temp) / "baseline.json"
            path.write_text(json.dumps(baseline), encoding="utf-8")
            result = self.run_check("--baseline", str(path), "--skip-git-audit")
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing required skills: ai-sdlc-removed", result.stdout)

    def test_new_required_flag_breaks_baseline(self) -> None:
        """A declared CLI contract must exist on every skill CLI."""
        with tempfile.TemporaryDirectory() as temp:
            baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
            baseline["required_cli_flags"].append("--future-required-flag")
            path = Path(temp) / "baseline.json"
            path.write_text(json.dumps(baseline), encoding="utf-8")
            result = self.run_check("--baseline", str(path), "--skip-git-audit")
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing stable flag --future-required-flag", result.stdout)

    def test_roadmap_audit_allows_completed_roadmap_and_maintenance(self) -> None:
        """The roadmap sequence may omit only its not-yet-created release commit."""
        result = self.run_check("--allow-pending-last", "--format", "toon")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_roadmap_audit_rejects_extra_terminal_commit(self) -> None:
        """A matching sequence in the middle must not pass as a release audit."""
        import importlib.util

        spec = importlib.util.spec_from_file_location("compatibility_audit", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        self.assertTrue(module.audit_subjects(["one", "two"], ["one", "two"]))
        self.assertFalse(module.audit_subjects(["one", "two", "extra"], ["one", "two"]))
        self.assertTrue(module.audit_subjects(["one"], ["one", "two"], allow_pending_last=True))
        self.assertFalse(module.audit_subjects(["prefix", "one"], ["one"], allow_pending_last=True))


if __name__ == "__main__":
    unittest.main()
