#!/usr/bin/env python3
"""Tests for release compatibility and roadmap commit auditing."""

from __future__ import annotations

import json
import os
import shutil
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

    def git_executable_args(self) -> tuple[str, str]:
        """Return the reviewed absolute Git path required by history audits."""
        path = shutil.which("git")
        self.assertIsNotNone(path)
        return "--git-executable", str(Path(path or "").resolve())

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

    def test_target_python_is_inspected_but_never_executed(self) -> None:
        """An attacker-controlled target script cannot run during compatibility."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / "skills" / "probe"
            shared = root / "skills" / "_shared"
            mirror = root / "skills" / "ai-sdlc-shared-runtime" / "scripts"
            for path in (skill / "scripts", shared, mirror, root / "modules"):
                path.mkdir(parents=True, exist_ok=True)
            (skill / "SKILL.md").write_text("---\nname: probe\n---\n", encoding="utf-8")
            marker = root / "EXECUTED"
            (skill / "scripts" / "probe.py").write_text(
                "from pathlib import Path\n"
                f"Path({str(marker)!r}).write_text('unsafe')\n"
                "from argparse import ArgumentParser\n"
                "p = ArgumentParser()\n"
                "p.add_argument('--quick-flow')\n"
                "p.add_argument('--full-flow')\n"
                "p.add_argument('--state-check')\n"
                "p.add_argument('--begin-state')\n"
                "p.add_argument('--complete-state')\n",
                encoding="utf-8",
            )
            config = root / "config.json"
            config.write_text('{"schema":"fixture/v1"}', encoding="utf-8")
            for path in (
                root / "README.md",
                root / "docs/reference/artifact-routing.md",
                root / "docs/how-to/install.md",
                root / "docs/how-to/update.md",
                root / "guide.md",
            ):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("npx skills add compatibility update rollback\n", encoding="utf-8")
            baseline = {
                "schema": "ai-sdlc-compatibility-baseline/v1",
                "release": "fixture",
                "harness_api_version": "1.0.0",
                "required_skill_names": ["probe"],
                "required_cli_flags": ["--quick-flow", "--full-flow", "--state-check", "--begin-state", "--complete-state"],
                "skill_doc_contract": [],
                "routes": {},
                "config": {"schema": "fixture/v1", "defaults": "config.json"},
                "modules": {"schema": "ai-sdlc-module/v1", "ids": []},
                "install_update_guide": "guide.md",
            }
            baseline_path = root / "baseline.json"
            baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
            result = subprocess.run(
                ["python3", str(SCRIPT), "--root", str(root), "--baseline", str(baseline_path), "--skip-git-audit"],
                cwd=ROOT,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "PYTHONPYCACHEPREFIX": "/tmp/ai-sdlc-pyc"},
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(marker.exists(), "compatibility validator executed target-root Python")

    def test_git_audit_requires_an_explicit_executable(self) -> None:
        """History validation cannot silently select Git through PATH."""
        result = self.run_check("--format", "toon")
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires --git-executable", result.stdout)

    def test_git_audit_rejects_an_executable_inside_target_root(self) -> None:
        """The inspected repository cannot supply the Git binary used on it."""
        result = self.run_check("--git-executable", str(SCRIPT), "--format", "toon")
        self.assertEqual(result.returncode, 1)
        self.assertIn("must not be inside the inspected target root", result.stdout)

    def test_roadmap_audit_allows_completed_roadmap_and_maintenance(self) -> None:
        """The roadmap sequence may omit only its not-yet-created release commit."""
        result = self.run_check("--allow-pending-last", "--format", "toon", *self.git_executable_args())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_roadmap_audit_allows_post_release_maintenance_only_after_sequence(self) -> None:
        """Later maintenance is valid but cannot replace or interrupt the sequence."""
        import importlib.util

        spec = importlib.util.spec_from_file_location("compatibility_audit", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        self.assertTrue(module.audit_subjects(["one", "two"], ["one", "two"]))
        self.assertTrue(module.audit_subjects(["one", "two", "maintenance"], ["one", "two"]))
        self.assertFalse(module.audit_subjects(["one", "maintenance", "two"], ["one", "two"]))
        self.assertFalse(module.audit_subjects(["one", "one", "two"], ["one", "two"]))
        self.assertTrue(module.audit_subjects(["one"], ["one", "two"], allow_pending_last=True))
        self.assertFalse(module.audit_subjects(["prefix", "one"], ["one"], allow_pending_last=True))


if __name__ == "__main__":
    unittest.main()
