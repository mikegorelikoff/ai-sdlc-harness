#!/usr/bin/env python3
"""Tests for deterministic non-mutating change apply previews."""

from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHANGE = ROOT / "skills/ai-sdlc-change-set/scripts/change_set.py"
DELTA = ROOT / "skills/ai-sdlc-change-set/scripts/spec_delta.py"
PREVIEW = ROOT / "skills/ai-sdlc-change-set/scripts/change_preview.py"


class ChangePreviewTests(unittest.TestCase):
    """Virtual patch, conflict, impact, gate, and byte-identity tests."""

    def cli(self, script: Path, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run one change lifecycle command."""
        return subprocess.run(["python3", str(script), str(repository), *args], cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def workspace(self, repository: Path, change_id: str = "evolve-auth", target: str = "specs/auth/requirements.md") -> Path:
        """Create a full-flow change workspace."""
        result = self.cli(CHANGE, repository, "--change-id", change_id, "--title", "Evolve auth", "--summary", "Change session behavior.", "--owner", "Security", "--target", target, "--date", "2026-07-19", "--create", "--full-flow")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return repository / "changes" / change_id

    def structured_target(self, repository: Path) -> Path:
        """Write canonical structured requirements and one downstream trace."""
        target = repository / "specs/auth/requirements.md"
        target.parent.mkdir(parents=True)
        target.write_text(textwrap.dedent("""
            # Auth Requirements

            ### Requirement: Authentication
            ID: FR-001

            The system SHALL authenticate users.

            #### Scenario: Login
            - WHEN credentials are valid
            - THEN access is granted

            ### Requirement: Retained sessions
            ID: FR-002

            The system SHALL retain sessions.

            ### Requirement: Session naming
            ID: FR-003

            The system SHALL name sessions.
        """).strip() + "\n", encoding="utf-8")
        consumer = repository / "specs/consumer/design.md"
        consumer.parent.mkdir(parents=True)
        consumer.write_text("# Consumer\n\nDepends on FR-001.\n", encoding="utf-8")
        return target

    def delta(self, workspace: Path, body: str, target: str = "specs/auth/requirements.md", name: str = "auth.md") -> None:
        """Write one delta file."""
        (workspace / "deltas" / name).write_text(f"# Specification Delta\n\nTarget: `{target}`\n\n{textwrap.dedent(body).strip()}\n", encoding="utf-8")

    def valid_body(self) -> str:
        """Return a ready four-operation delta."""
        return """## ADDED Requirements
### Requirement: Session timeout
ID: FR-004
The system SHALL expire inactive sessions.
#### Scenario: Timeout
- WHEN inactivity reaches the limit
- THEN the session is invalidated

## MODIFIED Requirements
### Requirement: Strong authentication
ID: FR-001
The system MUST authenticate users with a supported credential.
#### Scenario: Login
- WHEN a valid credential is submitted
- THEN access is granted

## REMOVED Requirements
### Requirement: Retained sessions
ID: FR-002
Reason: Retention violates policy.
Migration: Existing sessions receive a maximum lifetime.

## RENAMED Requirements
### Requirement: Named session
ID: FR-003
From: Session naming
To: Named session
"""

    def preview(self, repository: Path, change_id: str = "evolve-auth", *args: str) -> subprocess.CompletedProcess[str]:
        """Run preview in JSON by default."""
        return self.cli(PREVIEW, repository, "--change-id", change_id, "--preview", "--format", "json", *args)

    def test_ready_preview_builds_diff_impact_and_gates_without_mutation(self) -> None:
        """A valid delta produces exact virtual targets and no writes to truth."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            target = self.structured_target(repository)
            workspace = self.workspace(repository)
            self.delta(workspace, self.valid_body())
            before = target.read_bytes()
            result = self.preview(repository, "evolve-auth", "--write")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            record = json.loads(result.stdout)
            self.assertEqual(record["status"], "ready")
            self.assertIn("+### Requirement: Session timeout", record["targets"][0]["diff"])
            self.assertIn("-### Requirement: Retained sessions", record["targets"][0]["diff"])
            self.assertEqual(record["reopen_actions"], ["specs/consumer/design.md"])
            self.assertIn("security-policy-review", [item["gate"] for item in record["required_gates"]])
            self.assertEqual(target.read_bytes(), before)
            self.assertTrue((workspace / "apply-preview.md").is_file())
            self.assertTrue((workspace / "_ai_sdlc/apply-preview.json").is_file())
            toon = (workspace / "_ai_sdlc/apply-preview.toon").read_text(encoding="utf-8")
            self.assertIn("targets[1]", toon)
            self.assertIn("required_gates", toon)

    def test_preview_is_deterministic(self) -> None:
        """Unchanged inputs yield the same fingerprint and output."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.structured_target(repository)
            workspace = self.workspace(repository)
            self.delta(workspace, self.valid_body())
            first = self.preview(repository)
            second = self.preview(repository)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(first.stdout, second.stdout)

    def test_ambiguous_canonical_block_is_blocked(self) -> None:
        """Duplicate canonical IDs cannot be guessed during preview."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            target = self.structured_target(repository)
            target.write_text(target.read_text(encoding="utf-8") + "\n### Requirement: Duplicate\nID: FR-001\nThe system SHALL fail.\n", encoding="utf-8")
            workspace = self.workspace(repository)
            self.delta(workspace, """## MODIFIED Requirements
### Requirement: Authentication
ID: FR-001
The system MUST authenticate users.
#### Scenario: Login
- WHEN credentials are valid
- THEN access is granted
""")
            result = self.preview(repository)
            self.assertEqual(result.returncode, 2)
            self.assertIn("ambiguous-canonical-block", result.stdout)

    def test_concurrent_active_change_overlap_is_blocked(self) -> None:
        """Another validated delta touching the same ID creates a conflict."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.structured_target(repository)
            workspace = self.workspace(repository)
            self.delta(workspace, """## MODIFIED Requirements
### Requirement: Authentication
ID: FR-001
The system MUST authenticate users.
#### Scenario: Login
- WHEN credentials are valid
- THEN access is granted
""")
            other = repository / "changes/other/_ai_sdlc"
            other.mkdir(parents=True)
            (other / "delta-set.json").write_text(json.dumps({"status": "validated", "operations": [{"target": "specs/auth/requirements.md", "requirement_id": "FR-001"}]}), encoding="utf-8")
            result = self.preview(repository)
            self.assertEqual(result.returncode, 2)
            self.assertIn("concurrent-change-overlap", result.stdout)

    def test_inline_rename_is_blocked(self) -> None:
        """A rename needs a structured canonical name boundary."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            target = repository / "specs/auth/requirements.md"
            target.parent.mkdir(parents=True)
            target.write_text("- FR-003: The system shall name sessions.\n", encoding="utf-8")
            workspace = self.workspace(repository)
            self.delta(workspace, """## RENAMED Requirements
### Requirement: Named session
ID: FR-003
From: Session naming
To: Named session
""")
            result = self.preview(repository)
            self.assertEqual(result.returncode, 2)
            self.assertIn("unsupported-inline-rename", result.stdout)

    def test_missing_target_can_be_previewed_for_added_requirements(self) -> None:
        """A new declared target produces a creation diff and ownership gate."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            workspace = self.workspace(repository, target="specs/audit/requirements.md")
            self.delta(workspace, """## ADDED Requirements
### Requirement: Audit access
ID: FR-010
The system SHALL audit access.
#### Scenario: Access granted
- WHEN access is granted
- THEN an audit event is stored
""", target="specs/audit/requirements.md")
            result = self.preview(repository)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            record = json.loads(result.stdout)
            self.assertFalse(record["targets"][0]["exists"])
            self.assertIn("new-artifact-ownership", [item["gate"] for item in record["required_gates"]])


if __name__ == "__main__":
    unittest.main()
