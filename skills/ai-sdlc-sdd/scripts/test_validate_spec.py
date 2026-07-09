#!/usr/bin/env python3
"""Deterministic tests for the AI SDLC SDD spec validator."""

from __future__ import annotations

import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
VALIDATOR = ROOT / ".codex" / "skills" / "ai-sdlc-sdd" / "scripts" / "validate_spec.py"


def write(path: Path, text: str) -> None:
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


class ValidateSpecTests(unittest.TestCase):
    def test_five_file_spec_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "171-example"
            spec_dir.mkdir()
            write(
                spec_dir / "requirements.md",
                """
                # Requirements
                ## Goal
                ## Problem Statement
                ## Scope
                ## Actors
                ## Inputs
                ## Outputs
                ## Functional Requirements
                ## Non-Functional Requirements
                ## Constraints
                ## Acceptance Criteria
                ## Out of Scope
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
                - [ ] 1. Example
                ## Testing
                - [ ] 2. Example
                ## Documentation
                - [ ] 3. Example
                """,
            )
            write(
                spec_dir / "test-cases.md",
                """
                # Test Cases
                ## Scope
                ## Scenario Matrix
                ## Layer Mapping
                ## Automation Plan
                ## Open Gaps
                """,
            )
            write(
                spec_dir / "qa.md",
                """
                # QA
                ## Change Summary
                ## Acceptance Scenarios
                ## Regression Targets
                ## Risk Notes
                ## Validation Commands
                ## Manual Checks
                ## Signoff
                """,
            )
            result = subprocess.run(
                ["python3", str(VALIDATOR), str(spec_dir)],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_t_id_tasks_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "171-example"
            spec_dir.mkdir()
            write(
                spec_dir / "requirements.md",
                """
                # Requirements
                ## Goal
                ## Problem Statement
                ## Scope
                ## Actors
                ## Inputs
                ## Outputs
                ## Functional Requirements
                ## Non-Functional Requirements
                ## Constraints
                ## Acceptance Criteria
                ## Out of Scope
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
                - [ ] T001. Example
                Output: Done.
                Refs: AC-001
                ## Testing
                - [ ] T002. Example
                Output: Done.
                Refs: AC-001
                ## Documentation
                - [ ] T003. Example
                Output: Done.
                Refs: AC-001
                """,
            )
            write(
                spec_dir / "test-cases.md",
                """
                # Test Cases
                ## Scope
                ## Scenario Matrix
                ## Layer Mapping
                ## Automation Plan
                ## Open Gaps
                """,
            )
            write(
                spec_dir / "qa.md",
                """
                # QA
                ## Change Summary
                ## Acceptance Scenarios
                ## Regression Targets
                ## Risk Notes
                ## Validation Commands
                ## Manual Checks
                ## Signoff
                """,
            )
            result = subprocess.run(
                ["python3", str(VALIDATOR), str(spec_dir)],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_three_file_spec_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "171-example"
            spec_dir.mkdir()
            write(
                spec_dir / "requirements.md",
                """
                # Requirements
                ## Goal
                ## Problem Statement
                ## Scope
                ## Actors
                ## Inputs
                ## Outputs
                ## Functional Requirements
                ## Non-Functional Requirements
                ## Constraints
                ## Acceptance Criteria
                ## Out of Scope
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
                - [ ] 1. Example
                ## Testing
                - [ ] 2. Example
                ## Documentation
                - [ ] 3. Example
                """,
            )
            result = subprocess.run(
                ["python3", str(VALIDATOR), str(spec_dir)],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing", result.stderr)
            self.assertIn("test-cases.md", result.stderr)
            self.assertIn("qa.md", result.stderr)


if __name__ == "__main__":
    unittest.main()
