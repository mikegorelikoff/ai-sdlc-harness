#!/usr/bin/env python3
"""Tests for semantic specification delta parsing and validation."""

from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHANGE_SCRIPT = ROOT / "skills/ai-sdlc-change-set/scripts/change_set.py"
DELTA_SCRIPT = ROOT / "skills/ai-sdlc-change-set/scripts/spec_delta.py"


class SpecDeltaTests(unittest.TestCase):
    """Operation, scenario, target, overlap, and authority tests."""

    def run_cli(self, script: Path, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run one capability CLI."""
        return subprocess.run(
            ["python3", str(script), str(repository), *args],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def fixture(self, repository: Path) -> tuple[Path, Path]:
        """Create one change set and canonical requirements target."""
        target = repository / "specs/auth/requirements.md"
        target.parent.mkdir(parents=True)
        target.write_text(
            "# Requirements\n\n- FR-001: The system shall authenticate users.\n- FR-002: The system shall retain sessions.\n- FR-003: The system shall name sessions.\n",
            encoding="utf-8",
        )
        result = self.run_cli(
            CHANGE_SCRIPT,
            repository,
            "--change-id", "evolve-auth",
            "--title", "Evolve authentication",
            "--summary", "Update authentication behavior.",
            "--owner", "Security",
            "--target", "specs/auth/requirements.md",
            "--date", "2026-07-19",
            "--create", "--full-flow",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return repository / "changes/evolve-auth", target

    def write_delta(self, workspace: Path, name: str, body: str, target: str = "specs/auth/requirements.md") -> Path:
        """Write one readable delta fixture."""
        path = workspace / "deltas" / name
        content = f"# Specification Delta\n\nTarget: `{target}`\n\n{textwrap.dedent(body).strip()}\n"
        path.write_text(content, encoding="utf-8")
        return path

    def valid_body(self) -> str:
        """Return all four supported operations."""
        return """## ADDED Requirements

### Requirement: Session timeout
ID: FR-004

The system SHALL expire inactive sessions.

#### Scenario: Timeout reached
- WHEN inactivity reaches the configured duration
- THEN the session is invalidated

## MODIFIED Requirements

### Requirement: User authentication
ID: FR-001

The system MUST authenticate active users with a supported credential.

#### Scenario: Valid credential
- **WHEN** a valid credential is submitted
- **THEN** access is granted

## REMOVED Requirements

### Requirement: Retained sessions
ID: FR-002

Reason: Indefinite retention violates policy.
Migration: Existing sessions expire at the new maximum lifetime.

## RENAMED Requirements

### Requirement: Named user session
ID: FR-003

From: Session naming
To: Named user session
"""

    def validate(self, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Validate the fixture delta workspace."""
        return self.run_cli(DELTA_SCRIPT, repository, "--change-id", "evolve-auth", "--validate", *args)

    def test_valid_operations_write_deterministic_projection(self) -> None:
        """All operations parse, target-check, and preserve canonical bytes."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            workspace, target = self.fixture(repository)
            self.write_delta(workspace, "auth.md", self.valid_body())
            before = target.read_bytes()
            first = self.validate(repository, "--write", "--format", "json")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(target.read_bytes(), before)
            projection = json.loads((workspace / "_ai_sdlc/delta-set.json").read_text(encoding="utf-8"))
            self.assertEqual([item["operation"] for item in projection["operations"]], ["MODIFIED", "REMOVED", "RENAMED", "ADDED"])
            second = self.validate(repository, "--format", "json")
            self.assertEqual(json.loads(first.stdout)["contract_fingerprint"], json.loads(second.stdout)["contract_fingerprint"])
            self.assertFalse(projection["authority"]["canonical_mutation_allowed"])
            toon = (workspace / "_ai_sdlc/delta-set.toon").read_text(encoding="utf-8")
            self.assertIn("operations[4]:", toon)
            self.assertIn("scenarios[1]", toon)

    def test_behavior_change_requires_complete_scenario(self) -> None:
        """ADDED and MODIFIED operations require WHEN and THEN."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            workspace, _ = self.fixture(repository)
            self.write_delta(workspace, "invalid.md", """## ADDED Requirements

### Requirement: Session timeout
ID: FR-004
The system SHALL expire sessions.
#### Scenario: Missing outcome
- WHEN inactivity is reached
""")
            result = self.validate(repository)
            self.assertEqual(result.returncode, 1)
            self.assertIn("scenario requires WHEN and THEN", result.stdout)

    def test_existing_and_new_id_rules_are_enforced(self) -> None:
        """Added IDs must be absent and other operation IDs must exist."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            workspace, _ = self.fixture(repository)
            self.write_delta(workspace, "invalid.md", """## ADDED Requirements

### Requirement: Duplicate authentication
ID: FR-001
The system SHALL authenticate users.
#### Scenario: Duplicate
- WHEN a user signs in
- THEN access is checked

## REMOVED Requirements
### Requirement: Missing requirement
ID: FR-999
Reason: Not needed.
Migration: None required.
""")
            result = self.validate(repository)
            self.assertEqual(result.returncode, 1)
            self.assertIn("ADDED requirement already exists", result.stdout)
            self.assertIn("REMOVED requirement is missing", result.stdout)

    def test_overlapping_operations_are_rejected(self) -> None:
        """One target and requirement ID cannot receive two operations."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            workspace, _ = self.fixture(repository)
            block = """## MODIFIED Requirements
### Requirement: Authentication
ID: FR-001
The system MUST authenticate users.
#### Scenario: Login
- WHEN credentials are valid
- THEN access is granted
"""
            self.write_delta(workspace, "one.md", block)
            self.write_delta(workspace, "two.md", block)
            result = self.validate(repository)
            self.assertEqual(result.returncode, 1)
            self.assertIn("overlapping operation", result.stdout)

    def test_undeclared_target_is_rejected(self) -> None:
        """Delta targets must be declared by the parent change set."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            workspace, _ = self.fixture(repository)
            self.write_delta(workspace, "other.md", """## ADDED Requirements
### Requirement: Audit
ID: FR-010
The system SHALL audit access.
#### Scenario: Access
- WHEN access is granted
- THEN an audit event is stored
""", target="specs/audit/requirements.md")
            result = self.validate(repository)
            self.assertEqual(result.returncode, 1)
            self.assertIn("target is not declared", result.stdout)

    def test_no_delta_documents_is_rejected(self) -> None:
        """The intake placeholder is not a semantic delta."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.fixture(repository)
            result = self.validate(repository)
            self.assertEqual(result.returncode, 1)
            self.assertIn("no semantic delta", result.stdout)


if __name__ == "__main__":
    unittest.main()
