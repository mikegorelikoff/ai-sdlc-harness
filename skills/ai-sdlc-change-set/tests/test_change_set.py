#!/usr/bin/env python3
"""Tests for isolated change workspace creation and validation."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-change-set/scripts/change_set.py"


class ChangeSetTests(unittest.TestCase):
    """Workspace shape, safety, authority, and fingerprint tests."""

    def run_cli(self, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run the change-set CLI."""
        return subprocess.run(
            ["python3", str(SCRIPT), str(repository), *args],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def create(self, repository: Path, change_id: str = "add-session-timeout") -> subprocess.CompletedProcess[str]:
        """Create a deterministic valid fixture."""
        return self.run_cli(
            repository,
            "--change-id", change_id,
            "--title", "Add session timeout",
            "--summary", "Expire inactive sessions.",
            "--owner", "Security",
            "--target", "specs/auth/requirements.md",
            "--target", "docs/security.md",
            "--date", "2026-07-19",
            "--create",
            "--full-flow",
            "--format", "json",
        )

    def test_create_writes_complete_isolated_workspace(self) -> None:
        """Creation writes the contract and preserves canonical target bytes."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            target = repository / "specs/auth/requirements.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Canonical\n", encoding="utf-8")
            before = target.read_bytes()
            result = self.create(repository)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            workspace = repository / "changes/add-session-timeout"
            required = {
                "proposal.md", "design.md", "tasks.md", "deltas/index.md",
                "evidence/index.md", "_ai_sdlc/change-set.json", "_ai_sdlc/change-set.toon",
            }
            self.assertEqual(required, {path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file()})
            self.assertEqual(target.read_bytes(), before)
            record = json.loads((workspace / "_ai_sdlc/change-set.json").read_text(encoding="utf-8"))
            self.assertEqual(record["schema"], "ai-sdlc-change-set/v1")
            self.assertFalse(record["authority"]["canonical_mutation_allowed"])
            self.assertEqual(record["canonical_targets"], ["docs/security.md", "specs/auth/requirements.md"])
            toon = (workspace / "_ai_sdlc/change-set.toon").read_text(encoding="utf-8")
            self.assertIn("canonical_targets[2]: docs/security.md,specs/auth/requirements.md", toon)
            self.assertIn("authority:\n  canonical_mutation_allowed: false", toon)

    def test_emit_is_deterministic_and_non_mutating(self) -> None:
        """Emit produces stable identity without creating changes/."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            args = (
                "--change-id", "add-session-timeout",
                "--title", "Add session timeout",
                "--summary", "Expire inactive sessions.",
                "--owner", "Security",
                "--target", "specs/auth/requirements.md",
                "--date", "2026-07-19",
                "--emit", "--quick-flow", "--format", "json",
            )
            first = self.run_cli(repository, *args)
            second = self.run_cli(repository, *args)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            self.assertFalse((repository / "changes").exists())

    def test_unsafe_ids_and_targets_are_rejected(self) -> None:
        """Workspace and target paths cannot escape authority boundaries."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            for change_id, target in (("../escape", "specs/a.md"), ("safe-id", "../../policy.md"), ("safe-id", "changes/other/proposal.md")):
                with self.subTest(change_id=change_id, target=target):
                    result = self.run_cli(
                        repository,
                        "--change-id", change_id,
                        "--title", "Unsafe",
                        "--summary", "Must fail.",
                        "--owner", "Security",
                        "--target", target,
                        "--emit",
                    )
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("ERROR:", result.stdout)

    def test_existing_workspace_is_never_overwritten(self) -> None:
        """Repeated creation fails without changing workspace content."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            first = self.create(repository)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            proposal = repository / "changes/add-session-timeout/proposal.md"
            before = proposal.read_bytes()
            second = self.create(repository)
            self.assertEqual(second.returncode, 1)
            self.assertIn("already exists", second.stdout)
            self.assertEqual(proposal.read_bytes(), before)

    def test_validation_rejects_stale_fingerprint(self) -> None:
        """Hand-edited machine state fails deterministic identity validation."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            created = self.create(repository)
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            workspace = repository / "changes/add-session-timeout"
            record_path = workspace / "_ai_sdlc/change-set.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["owner"] = "Unknown"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = self.run_cli(repository, "--change-id", "add-session-timeout", "--validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("contract_fingerprint is stale", result.stdout)
            self.assertIn("owner metadata mismatch", result.stdout)

    def test_validation_rejects_missing_artifact(self) -> None:
        """Required-file drift fails with a scoped diagnostic."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            created = self.create(repository)
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            workspace = repository / "changes/add-session-timeout"
            (workspace / "tasks.md").unlink()
            result = self.run_cli(repository, "--change-id", "add-session-timeout", "--validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing required artifact: tasks.md", result.stdout)

    def test_validation_accepts_untouched_workspace(self) -> None:
        """A generated workspace validates independently of creation input."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            created = self.create(repository)
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            result = self.run_cli(repository, "--change-id", "add-session-timeout", "--validate", "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("valid: true", result.stdout)
            self.assertIn("schema: ai-sdlc-change-set/v1", result.stdout)


if __name__ == "__main__":
    unittest.main()
