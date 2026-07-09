#!/usr/bin/env python3
"""Deterministic tests for portable commit-readiness checks."""

from __future__ import annotations

import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHECK_COMMIT_READY = ROOT / "skills" / "ai-sdlc-commit-prep" / "scripts" / "check_commit_ready.py"


def write(path: Path, text: str) -> None:
    """Write dedented fixture text with parent directories created."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def write_spec(spec_dir: Path, *, bad_acceptance: bool = False, decision_log: bool = False) -> None:
    """Create a portable SDD fixture for commit-readiness tests."""
    write(
        spec_dir / "requirements.md",
        f"""
        # Requirements
        ## Goal
        Goal.
        ## Problem Statement
        Problem.
        ## Scope
        Scope.
        ## Actors
        - AI assistant
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
        - None.
        ## Decision Status
        - All blocking decisions resolved.
        ## Acceptance Criteria
        - {"Works correctly." if bad_acceptance else "AC-001: Given a spec, when validation runs, then it passes."}
        ## Out of Scope
        - Unrelated work.
        """,
    )
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
        None.
        ## Error Handling
        Deterministic.
        ## Security Considerations
        Local only.
        ## Observability
        Local output.
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
    if decision_log:
        write(
            spec_dir / "decision-log.md",
            """
            # Decision Log

            | ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
            | --- | --- | --- | --- | --- | --- | --- | --- | --- |
            | DEC-001 | 2026-07-09 | accepted | Dev | Use local scripts | Existing repository layout | local scripts | tasks.md | validate_spec.py |
            """,
        )


class CheckCommitReadyTests(unittest.TestCase):
    """Behavior tests for the commit-readiness helper CLI."""

    def test_quick_flow_runs_portable_spec_validation(self) -> None:
        """Quick flow should pass with a valid staged spec and lean gates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            spec_dir = root / "specs" / "185-example"
            spec_dir.mkdir(parents=True)
            write_spec(spec_dir)
            write(root / "README.md", "example\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            result = subprocess.run(
                ["python3", str(CHECK_COMMIT_READY), "--spec", str(spec_dir), "--quick-flow", "--allow-unstaged"],
                cwd=root,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Commit readiness checks passed.", result.stdout)

    def test_full_flow_requires_decision_log(self) -> None:
        """Full flow should block when decision-log traceability is absent."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            spec_dir = root / "specs" / "186-example"
            spec_dir.mkdir(parents=True)
            write_spec(spec_dir)
            write(root / "README.md", "example\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            result = subprocess.run(
                ["python3", str(CHECK_COMMIT_READY), "--spec", str(spec_dir), "--full-flow", "--allow-unstaged"],
                cwd=root,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing decision log for full flow", result.stderr)


if __name__ == "__main__":
    unittest.main()
