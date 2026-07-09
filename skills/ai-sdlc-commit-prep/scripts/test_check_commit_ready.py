#!/usr/bin/env python3
"""Deterministic tests for AI SDLC commit-readiness checks."""

from __future__ import annotations

import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHECK_COMMIT_READY = ROOT / ".codex" / "skills" / "ai-sdlc-commit-prep" / "scripts" / "check_commit_ready.py"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def full_spec(task_block: str) -> str:
    return textwrap.dedent(
        f"""
        # Requirements
        ## Goal
        Goal.
        ## Problem Statement
        Problem.
        ## Scope
        Scope.
        ## Actors
        - Codex
        ## Inputs
        - Request
        ## Outputs
        - Spec
        ## Functional Requirements
        - Requirement.
        ## Non-Functional Requirements
        - Deterministic.
        ## Constraints
        - Local only.
        ## Assumptions
        - Accepted assumption.
        ## Open Questions
        - None for this slice.
        ## Decision Status
        - All blocking decisions resolved.
        ## Acceptance Criteria
        - AC-001: Given a spec, when validation runs, then it passes.
        ## Out of Scope
        - Unrelated work.
        """
    )


class CheckCommitReadyTests(unittest.TestCase):
    def test_fails_when_new_sdd_gate_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            spec_dir = root / "specs" / "185-example"
            spec_dir.mkdir(parents=True)
            write(
                spec_dir / "requirements.md",
                """
                # Requirements
                ## Goal
                Goal.
                ## Problem Statement
                Problem.
                ## Scope
                Scope.
                ## Actors
                - Codex
                ## Inputs
                - Request
                ## Outputs
                - Spec
                ## Functional Requirements
                - Requirement.
                ## Non-Functional Requirements
                - Deterministic.
                ## Constraints
                - Local only.
                ## Acceptance Criteria
                - Works correctly.
                ## Out of Scope
                - None
                """,
            )
            write(
                spec_dir / "design.md",
                """
                # Design
                ## Overview
                ## Architecture
                ## Components
                ## Interfaces and Contracts
                ## Data Model
                ## Error Handling
                ## Security Considerations
                ## Observability
                ## Risks and Tradeoffs
                ## Validation Strategy
                ## Migration Notes
                """,
            )
            write(
                spec_dir / "tasks.md",
                """
                # Tasks
                ## Implementation
                - [x] T001. Example
                Output: Done.
                Refs: AC-001
                ## Testing
                - [x] T002. Example
                Output: Done.
                Refs: AC-001
                ## Documentation
                - [x] T003. Example
                Output: Done.
                Refs: AC-001
                """,
            )
            write(
                spec_dir / "test-cases.md",
                """
                # Test Cases
                ## Scope
                Covered.
                ## Scenario Matrix
                | ID | Spec ref | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
                | --- | --- | --- | --- | --- | --- | --- | --- |
                | TC-001 | AC-001 | Scenario | Setup | Trigger | Outcome | unit | command |
                ## Layer Mapping
                Mapped.
                ## Automation Plan
                Planned.
                ## Open Gaps
                None.
                """,
            )
            write(
                spec_dir / "qa.md",
                """
                # QA
                ## Change Summary
                Summary.
                ## Acceptance Scenarios
                Scenario.
                ## Regression Targets
                Targets.
                ## Risk Notes
                Risks.
                ## Validation Commands
                - command
                ## Manual Checks
                - check
                ## Signoff
                Pending.
                """,
            )
            write(root / "README.md", "example\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            result = subprocess.run(
                ["python3", str(CHECK_COMMIT_READY), "--spec", str(spec_dir), "--allow-unstaged"],
                cwd=root,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("check_clarify.py failed", result.stderr)

    def test_fails_when_strict_ai_lint_reports_blocking_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "config", "user.email", "codex@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Codex"], cwd=root, check=True)
            spec_dir = root / "specs" / "187-example"
            spec_dir.mkdir(parents=True)
            write(spec_dir / "requirements.md", full_spec("unused"))
            write(
                spec_dir / "design.md",
                """
                # Design
                ## Overview
                Overview.
                ## Architecture
                Architecture.
                ## Components
                Components.
                ## Interfaces and Contracts
                Contracts.
                ## Data Model
                No model changes.
                ## Error Handling
                Deterministic errors.
                ## Security Considerations
                Local only.
                ## Observability
                Local artifacts.
                ## Risks and Tradeoffs
                Risks.
                ## Validation Strategy
                Tests.
                ## Migration Notes
                None.
                """,
            )
            write(
                spec_dir / "tasks.md",
                """
                # Tasks
                ## Implementation
                - [x] T001. Example
                Output: Done.
                Refs: AC-001
                ## Testing
                - [x] T002. Example
                Output: Done.
                Refs: AC-001
                ## Documentation
                - [x] T003. Example
                Output: Done.
                Refs: AC-001
                """,
            )
            write(
                spec_dir / "test-cases.md",
                """
                # Test Cases
                ## Scope
                Covered.
                ## Scenario Matrix
                | ID | Spec ref | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
                | --- | --- | --- | --- | --- | --- | --- | --- |
                | TC-001 | AC-001 | Scenario | Setup | Trigger | Outcome | unit | command |
                ## Layer Mapping
                Mapped.
                ## Automation Plan
                Planned.
                ## Open Gaps
                None.
                """,
            )
            write(
                spec_dir / "qa.md",
                """
                # QA
                ## Change Summary
                Summary.
                ## Acceptance Scenarios
                Scenario.
                ## Regression Targets
                Targets.
                ## Risk Notes
                Risks.
                ## Validation Commands
                - command
                ## Manual Checks
                - check
                ## Signoff
                Pending.
                """,
            )
            write(root / "README.md", "example\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "commit", "--no-gpg-sign", "-m", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            write(root / "internal" / "service" / "order_service.go", "package service\n")

            result = subprocess.run(
                ["python3", str(CHECK_COMMIT_READY), "--spec", str(spec_dir), "--allow-unstaged", "--no-require-staged"],
                cwd=root,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("codex_ai_lint.py failed", result.stderr)


if __name__ == "__main__":
    unittest.main()
