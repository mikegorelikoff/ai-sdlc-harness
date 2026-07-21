#!/usr/bin/env python3
"""Tests for approved apply, rollback, repeat safety, and archive."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHANGE = ROOT / "skills/ai-sdlc-change-set/scripts/change_set.py"
PREVIEW = ROOT / "skills/ai-sdlc-change-set/scripts/change_preview.py"
APPLY = ROOT / "skills/ai-sdlc-change-set/scripts/change_apply.py"


class ChangeApplyTests(unittest.TestCase):
    """Approval, transaction, rollback, archive, and idempotency tests."""

    def cli(self, script: Path, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run one change lifecycle command."""
        return subprocess.run(["python3", str(script), str(repository), *args], cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def create_workspace(self, repository: Path, targets: list[str], change_id: str = "add-audit") -> Path:
        """Create an isolated change workspace."""
        args = ["--change-id", change_id, "--title", "Add audit", "--summary", "Add audit requirements.", "--owner", "Security", "--date", "2026-07-19", "--create", "--full-flow"]
        for target in targets:
            args.extend(["--target", target])
        result = self.cli(CHANGE, repository, *args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return repository / "changes" / change_id

    def add_delta(self, workspace: Path, name: str, target: str, requirement_id: str) -> None:
        """Add one valid requirement to a target."""
        (workspace / "deltas" / name).write_text(
            f"# Specification Delta\n\nTarget: `{target}`\n\n## ADDED Requirements\n\n### Requirement: Audit {requirement_id}\nID: {requirement_id}\n\nThe system SHALL record audit evidence.\n\n#### Scenario: Evidence recorded\n- WHEN a governed action completes\n- THEN audit evidence is stored\n",
            encoding="utf-8",
        )

    def approval(self, repository: Path, change_id: str = "add-audit", omit_gate: bool = False, stale: bool = False) -> Path:
        """Create approval tied to the current preview."""
        preview = self.cli(PREVIEW, repository, "--change-id", change_id, "--preview", "--format", "json")
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        value = json.loads(preview.stdout)
        gates = [item["gate"] for item in value["required_gates"]]
        if omit_gate:
            gates = gates[:-1]
        record = {
            "schema": "ai-sdlc-change-approval/v1",
            "change_id": change_id,
            "preview_fingerprint": "0" * 64 if stale else value["preview_fingerprint"],
            "decision": "accepted",
            "owner": "Security",
            "decided_at": "2026-07-19T12:00:00Z",
            "decision_ref": "DEC-100",
            "approved_gates": gates,
        }
        path = repository / f"{change_id}-approval.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def recovery(self, workspace: Path, target: str, *, existed: bool = False, backup: str = "") -> None:
        record = {
            "schema": "ai-sdlc-change-recovery/v1", "change_id": "add-audit", "status": "in_progress",
            "preview_fingerprint": "a" * 64, "created_at": "2026-07-19T00:00:00Z", "updated_at": "2026-07-19T00:00:00Z",
            "targets": [{"target": target, "existed": existed, "backup": backup, "staging": f"_ai_sdlc/staging/{target}", "before_sha256": "b" * 64, "after_sha256": "c" * 64}],
            "applied": [target], "rollback_errors": [],
        }
        path = workspace / "_ai_sdlc/recovery-manifest.json"
        path.write_text(json.dumps(record), encoding="utf-8")

    def test_approved_apply_and_archive_preserve_evidence(self) -> None:
        """Ready approved change applies once and archives complete evidence."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            target = repository / "specs/audit/requirements.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Audit Requirements\n", encoding="utf-8")
            workspace = self.create_workspace(repository, ["specs/audit/requirements.md"])
            self.add_delta(workspace, "audit.md", "specs/audit/requirements.md", "FR-010")
            approval = self.approval(repository)
            result = self.cli(APPLY, repository, "--change-id", "add-audit", "--apply", "--approval", str(approval), "--format", "json")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(
                json.loads(result.stdout)["approval_record_status"],
                "structurally_valid_identity_not_authenticated",
            )
            self.assertIn("FR-010", target.read_text(encoding="utf-8"))
            record = json.loads((workspace / "_ai_sdlc/change-set.json").read_text(encoding="utf-8"))
            self.assertEqual(record["status"], "applied")
            recovery = json.loads((workspace / "_ai_sdlc/recovery-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(recovery["status"], "complete")
            self.assertTrue((workspace / "evidence/approval.json").is_file())
            self.assertTrue((workspace / "evidence/approval.toon").is_file())
            self.assertIn("status: complete", (workspace / "_ai_sdlc/recovery-manifest.toon").read_text(encoding="utf-8"))
            archived = self.cli(APPLY, repository, "--change-id", "add-audit", "--archive", "--archive-date", "2026-07-19", "--format", "json")
            self.assertEqual(archived.returncode, 0, archived.stdout + archived.stderr)
            archive = repository / "changes/archive/2026-07-19-add-audit"
            self.assertTrue(archive.is_dir())
            self.assertEqual(json.loads((archive / "_ai_sdlc/change-set.json").read_text(encoding="utf-8"))["status"], "archived")
            self.assertIn("status: archived", (archive / "_ai_sdlc/change-set.toon").read_text(encoding="utf-8"))
            self.assertTrue((archive / "_ai_sdlc/backups/specs/audit/requirements.md").is_file())

    def test_stale_or_partial_approval_cannot_write_targets(self) -> None:
        """Approval must match the current preview and every required gate."""
        for mode in ("stale", "partial"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                repository = Path(temp)
                target = repository / "specs/audit/requirements.md"
                target.parent.mkdir(parents=True)
                target.write_text("# Audit Requirements\n", encoding="utf-8")
                workspace = self.create_workspace(repository, ["specs/audit/requirements.md"])
                self.add_delta(workspace, "audit.md", "specs/audit/requirements.md", "FR-010")
                before = target.read_bytes()
                approval = self.approval(repository, stale=mode == "stale", omit_gate=mode == "partial")
                result = self.cli(APPLY, repository, "--change-id", "add-audit", "--apply", "--approval", str(approval))
                self.assertEqual(result.returncode, 1)
                self.assertEqual(target.read_bytes(), before)
                self.assertFalse((workspace / "_ai_sdlc/recovery-manifest.json").exists())

    def test_multi_target_failure_rolls_back_every_applied_target(self) -> None:
        """Injected partial failure restores original bytes and draft state."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            targets = ["specs/a/requirements.md", "specs/b/requirements.md"]
            before: dict[str, bytes] = {}
            for target_name in targets:
                target = repository / target_name
                target.parent.mkdir(parents=True)
                target.write_text(f"# {target_name}\n", encoding="utf-8")
                before[target_name] = target.read_bytes()
            workspace = self.create_workspace(repository, targets)
            self.add_delta(workspace, "a.md", targets[0], "FR-010")
            self.add_delta(workspace, "b.md", targets[1], "FR-011")
            approval = self.approval(repository)
            result = self.cli(APPLY, repository, "--change-id", "add-audit", "--apply", "--approval", str(approval), "--simulate-failure-after", "1")
            self.assertEqual(result.returncode, 1)
            self.assertIn("rollback was attempted", result.stdout)
            for target_name in targets:
                self.assertEqual((repository / target_name).read_bytes(), before[target_name])
            manifest = json.loads((workspace / "_ai_sdlc/recovery-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "rolled_back")
            self.assertEqual(json.loads((workspace / "_ai_sdlc/change-set.json").read_text(encoding="utf-8"))["status"], "draft")

    def test_repeat_apply_and_archive_before_apply_are_rejected(self) -> None:
        """Lifecycle transitions cannot repeat or skip prerequisites."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            target = repository / "specs/audit/requirements.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Audit\n", encoding="utf-8")
            workspace = self.create_workspace(repository, ["specs/audit/requirements.md"])
            self.add_delta(workspace, "audit.md", "specs/audit/requirements.md", "FR-010")
            early = self.cli(APPLY, repository, "--change-id", "add-audit", "--archive")
            self.assertEqual(early.returncode, 1)
            self.assertIn("must be applied", early.stdout)
            approval = self.approval(repository)
            first = self.cli(APPLY, repository, "--change-id", "add-audit", "--apply", "--approval", str(approval))
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            after_first = target.read_bytes()
            second = self.cli(APPLY, repository, "--change-id", "add-audit", "--apply", "--approval", str(approval))
            self.assertEqual(second.returncode, 1)
            self.assertIn("status must be draft", second.stdout)
            self.assertEqual(target.read_bytes(), after_first)

    def test_tampered_recovery_traversal_cannot_delete_external_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            repository = parent / "repo"
            repository.mkdir()
            outside = parent / "outside.txt"
            outside.write_text("sentinel", encoding="utf-8")
            workspace = self.create_workspace(repository, ["docs/new.md"])
            self.recovery(workspace, "../outside.txt")
            result = self.cli(APPLY, repository, "--change-id", "add-audit", "--apply", "--approval", str(repository / "missing.json"))
            self.assertEqual(result.returncode, 1)
            self.assertEqual(outside.read_text(encoding="utf-8"), "sentinel")
            self.assertIn("not a canonical target", result.stdout)

    def test_symlinked_target_parent_is_rejected_before_recovery_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            repository = parent / "repo"
            repository.mkdir()
            outside = parent / "outside"
            outside.mkdir()
            workspace = self.create_workspace(repository, ["docs/new.md"])
            (repository / "docs").symlink_to(outside, target_is_directory=True)
            self.recovery(workspace, "docs/new.md")
            result = self.cli(APPLY, repository, "--change-id", "add-audit", "--apply", "--approval", str(repository / "missing.json"))
            self.assertEqual(result.returncode, 1)
            self.assertFalse((outside / "new.md").exists())
            self.assertIn("symlink", result.stdout)

    def test_tampered_backup_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            target = repository / "docs/existing.md"
            target.parent.mkdir(parents=True)
            target.write_text("original", encoding="utf-8")
            workspace = self.create_workspace(repository, ["docs/existing.md"])
            self.recovery(workspace, "docs/existing.md", existed=True, backup="../outside.txt")
            result = self.cli(APPLY, repository, "--change-id", "add-audit", "--apply", "--approval", str(repository / "missing.json"))
            self.assertEqual(result.returncode, 1)
            self.assertEqual(target.read_text(encoding="utf-8"), "original")
            self.assertIn("backup path is invalid", result.stdout)


if __name__ == "__main__":
    unittest.main()
