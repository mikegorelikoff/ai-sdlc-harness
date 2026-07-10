#!/usr/bin/env python3
"""Deterministic tests for the AI SDLC SDD spec validator."""

from __future__ import annotations

import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / "skills" / "ai-sdlc-sdd" / "scripts" / "validate_spec.py"


def write(path: Path, text: str) -> None:
    """Write dedented fixture text to a spec artifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


class ValidateSpecTests(unittest.TestCase):
    """Structural validator tests for SDD spec folders."""

    def test_complete_spec_package_passes(self) -> None:
        """A complete SDD package with required sections should pass."""
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
            write(
                spec_dir / "plan.md",
                """
                # plan.md
                ## Upstream Refinement Sources
                ## SDD Artifact Links
                ## Cross-Artifact Trace Map
                ## Task Execution Plan
                ## Task Dependencies
                ## Validation Sequence
                ## Open Links And Blockers
                """,
            )
            write(
                spec_dir / "_ai_sdlc/plan.toon",
                """
                feature: example
                workspace: implementation
                flow_mode: quick
                updated_at: 2026-07-10
                source_artifacts[6]{artifact,path}:
                  requirements,requirements.md
                  design,design.md
                  test_cases,test-cases.md
                  qa,qa.md
                  tasks,tasks.md
                  decisions,decision-log.md
                trace[0]{acceptance_id,test_cases,tasks}:
                tasks[0]{id,status,refs,tests,depends_on,artifact,decision_ref}:
                validation_sequence[1]{step,command}:
                  1,validate_spec.py --quick-flow
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
        """Task IDs using T### syntax should be accepted."""
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
            write(
                spec_dir / "plan.md",
                """
                # plan.md
                ## Upstream Refinement Sources
                ## SDD Artifact Links
                ## Cross-Artifact Trace Map
                ## Task Execution Plan
                ## Task Dependencies
                ## Validation Sequence
                ## Open Links And Blockers
                """,
            )
            write(
                spec_dir / "_ai_sdlc/plan.toon",
                """
                feature: example
                workspace: implementation
                flow_mode: quick
                updated_at: 2026-07-10
                source_artifacts[6]{artifact,path}:
                  requirements,requirements.md
                  design,design.md
                  test_cases,test-cases.md
                  qa,qa.md
                  tasks,tasks.md
                  decisions,decision-log.md
                trace[1]{acceptance_id,test_cases,tasks}:
                  AC-001,TC-001,T001/T002/T003
                tasks[3]{id,status,refs,tests,depends_on,artifact,decision_ref}:
                  T001,pending,AC-001,TC-001,none,Done.,DEC-001
                  T002,pending,AC-001,TC-001,T001,Done.,DEC-001
                  T003,pending,AC-001,TC-001,T001,Done.,DEC-001
                validation_sequence[1]{step,command}:
                  1,validate_spec.py --quick-flow
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
        """A spec missing QA and test-case artifacts should fail."""
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
            self.assertIn("plan.md", result.stderr)
            self.assertIn("_ai_sdlc/plan.toon", result.stderr)


if __name__ == "__main__":
    unittest.main()
