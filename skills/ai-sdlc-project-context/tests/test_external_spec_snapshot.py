#!/usr/bin/env python3
"""Security and behavior tests for external specification snapshots."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-project-context/scripts/external_spec_snapshot.py"


class ExternalSpecSnapshotTests(unittest.TestCase):
    def run_snapshot(self, repository: Path, source: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), "--root", str(repository), "--source-root", str(source), "--source-id", "product-specs@pilot", "--feature", "payments", *args],
            check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def setup_roots(self, base: Path) -> tuple[Path, Path]:
        repository, source = base / "consumer", base / "product-specs"
        repository.mkdir()
        source.mkdir()
        subprocess.run(["git", "init"], cwd=source, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-m", "source"], cwd=source, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return repository, source

    def test_write_and_check_create_portable_hashed_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository, source = self.setup_roots(Path(temp))
            (source / "requirements").mkdir()
            (source / "requirements/payments.md").write_text("# Payments\n\nAC-001: Retry once.\n", encoding="utf-8")
            (source / "api.md").write_text("# API\n\nPOST /payments\n", encoding="utf-8")
            written = self.run_snapshot(repository, source, "--write", "--source", "requirements/payments.md", "--source", "api.md")
            self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
            manifest_path = repository / "specs-refiniment/payments/external-specs.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertNotIn(source.as_posix(), manifest_path.read_text(encoding="utf-8"))
            self.assertEqual([row["source"] for row in manifest["files"]], ["api.md", "requirements/payments.md"])
            self.assertTrue((repository / "specs-refiniment/payments/external-api.md").is_file())
            self.assertTrue((repository / "specs-refiniment/payments/external-requirements-payments.md").is_file())
            checked = self.run_snapshot(repository, source, "--check")
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            self.assertEqual(json.loads(checked.stdout)["status"], "current")

    def test_check_reports_source_drift_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository, source = self.setup_roots(Path(temp))
            item = source / "requirements.md"
            item.write_text("# Before\n", encoding="utf-8")
            self.assertEqual(self.run_snapshot(repository, source, "--write", "--source", "requirements.md").returncode, 0)
            destination = repository / "specs-refiniment/payments/external-requirements.md"
            before = destination.read_text(encoding="utf-8")
            item.write_text("# After\n", encoding="utf-8")
            checked = self.run_snapshot(repository, source, "--check")
            self.assertEqual(checked.returncode, 1)
            self.assertIn("source drifted: requirements.md", checked.stdout)
            self.assertEqual(destination.read_text(encoding="utf-8"), before)

    def test_unsafe_sources_fail_before_any_snapshot_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            repository, source = self.setup_roots(base)
            (base / "outside.md").write_text("# Outside\n", encoding="utf-8")
            (source / "secret.md").write_text("ACME_API_KEY=synthetic-value-123\n", encoding="utf-8")
            (source / "real.md").write_text("# Safe\n", encoding="utf-8")
            (source / "linked.md").symlink_to(source / "real.md")
            (source / "notes.txt").write_text("not Markdown\n", encoding="utf-8")
            (source / "large.md").write_text("x" * 1_048_577, encoding="utf-8")
            for unsafe in ("../outside.md", "secret.md", "linked.md", "notes.txt", "large.md"):
                result = self.run_snapshot(repository, source, "--write", "--source", unsafe)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertFalse((repository / "specs-refiniment/payments").exists())

    def test_collision_and_unowned_destination_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository, source = self.setup_roots(Path(temp))
            (source / "a-b.md").write_text("# One\n", encoding="utf-8")
            (source / "a_b.md").write_text("# Two\n", encoding="utf-8")
            collision = self.run_snapshot(repository, source, "--write", "--source", "a-b.md", "--source", "a_b.md")
            self.assertEqual(collision.returncode, 1)
            self.assertIn("destination collision", collision.stdout)
            feature = repository / "specs-refiniment/payments"
            feature.mkdir(parents=True)
            (feature / "external-a-b.md").write_text("# Project owned\n", encoding="utf-8")
            unowned = self.run_snapshot(repository, source, "--write", "--source", "a-b.md")
            self.assertEqual(unowned.returncode, 1)
            self.assertIn("without matching snapshot ownership", unowned.stdout)
            self.assertEqual((feature / "external-a-b.md").read_text(encoding="utf-8"), "# Project owned\n")

    def test_omitting_previous_source_requires_manual_disposition(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository, source = self.setup_roots(Path(temp))
            (source / "one.md").write_text("# One\n", encoding="utf-8")
            (source / "two.md").write_text("# Two\n", encoding="utf-8")
            self.assertEqual(self.run_snapshot(repository, source, "--write", "--source", "one.md", "--source", "two.md").returncode, 0)
            result = self.run_snapshot(repository, source, "--write", "--source", "one.md")
            self.assertEqual(result.returncode, 1)
            self.assertIn("implicit deletion", result.stdout)
            self.assertTrue((repository / "specs-refiniment/payments/external-two.md").is_file())


if __name__ == "__main__":
    unittest.main()
