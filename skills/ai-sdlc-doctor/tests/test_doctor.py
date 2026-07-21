#!/usr/bin/env python3
"""Tests for installation diagnostics and safe upgrade planning."""
from __future__ import annotations
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills/ai-sdlc-doctor"
SCRIPT = SKILL / "scripts/doctor.py"
FIXTURES = SKILL / "references/fixtures"
class DoctorTests(unittest.TestCase):
    def cli(self, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["python3", str(SCRIPT), str(repository), *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    def test_repository_doctor_is_deterministic_and_healthy(self) -> None:
        first = self.cli(ROOT, "--doctor", "--format", "json")
        second = self.cli(ROOT, "--doctor", "--format", "json")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        value = json.loads(first.stdout)
        self.assertEqual(value["status"], "healthy")
        self.assertEqual({item["status"] for item in value["checks"]}, {"pass"})
    def test_broken_layout_has_actionable_failures_without_repair(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            result = self.cli(repository, "--doctor", "--format", "json")
            self.assertEqual(result.returncode, 2)
            value = json.loads(result.stdout)
            failed = [item for item in value["checks"] if item["status"] == "fail"]
            self.assertTrue(failed)
            self.assertTrue(all(item["remediation"] for item in failed))
            self.assertEqual(list(repository.iterdir()), [])
    def test_upgrade_plans_changes_migration_backup_and_reverse_rollback(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            args = ("--upgrade", "--current", str(FIXTURES / "current.json"), "--target", str(FIXTURES / "target.json"), "--upgrade-id", "upgrade-110", "--write", "--format", "json")
            first = self.cli(repository, *args)
            second = self.cli(repository, *args)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            value = json.loads(first.stdout)
            self.assertEqual({item["action"] for item in value["changes"]}, {"add", "modify", "remove", "unchanged"})
            self.assertEqual(value["migrations"][0]["to"], "policy/v2")
            self.assertEqual({item["path"] for item in value["backups"]}, {"config/policy.json", "skills/legacy/SKILL.md"})
            self.assertTrue((repository / "_ai_sdlc/upgrades/upgrade-110/plan.toon").is_file())
    def test_incompatible_api_and_unsafe_inventory_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            result = self.cli(repository, "--upgrade", "--current", str(FIXTURES / "current.json"), "--target", str(FIXTURES / "incompatible.json"), "--upgrade-id", "upgrade-200", "--format", "json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("target-harness-api-incompatible", json.loads(result.stdout)["blockers"])
            unsafe = json.loads((FIXTURES / "target.json").read_text(encoding="utf-8"))
            unsafe["files"][0]["path"] = "../escape"
            path = repository / "unsafe.json"
            path.write_text(json.dumps(unsafe), encoding="utf-8")
            result = self.cli(repository, "--upgrade", "--current", str(FIXTURES / "current.json"), "--target", str(path), "--upgrade-id", "unsafe")
            self.assertEqual(result.returncode, 1)
            self.assertIn("path is unsafe", result.stdout)
    def test_write_rejects_symlinked_repository_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp); repository = parent / "repo"; outside = parent / "outside"
            repository.mkdir(); outside.mkdir(); (repository / "_ai_sdlc").symlink_to(outside, target_is_directory=True)
            result = self.cli(repository, "--doctor", "--write")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((outside / "doctor/report.json").exists())
if __name__ == "__main__":
    unittest.main()
