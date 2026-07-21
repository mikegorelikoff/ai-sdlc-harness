#!/usr/bin/env python3
"""Deterministic tests for portable commit-readiness checks."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHECK_COMMIT_READY = ROOT / "skills" / "ai-sdlc-commit-prep" / "scripts" / "check_commit_ready.py"


def load_checker():
    """Load the checker so path-resolution helpers can be tested directly."""
    spec = importlib.util.spec_from_file_location("check_commit_ready", CHECK_COMMIT_READY)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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
    write(
        spec_dir / "plan.md",
        """
        # Plan
        ## Upstream Refinement Sources
        - Quick-flow fixture.
        ## SDD Artifact Links
        - requirements.md, design.md, test-cases.md, qa.md, tasks.md, _ai_sdlc/plan.toon, decision-log.md
        ## Cross-Artifact Trace Map
        - AC-001 -> TC-001 -> T001, T002, T003
        ## Task Execution Plan
        - [x] T001: Example
        - [x] T002: Example
        - [x] T003: Example
        ## Task Dependencies
        - T001: none
        - T002: T001
        - T003: T001
        ## Validation Sequence
        - validate_spec.py
        ## Open Links And Blockers
        - None.
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
          T001,done,AC-001,TC-001,none,Done.,DEC-001
          T002,done,AC-001,TC-001,T001,Done.,DEC-001
          T003,done,AC-001,TC-001,T001,Done.,DEC-001
        validation_sequence[1]{step,command}:
          1,validate_spec.py --quick-flow
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
    def test_installed_layout_resolves_consumer_workspace_root(self) -> None:
        """Installed commit prep must not resolve relative specs below `.agents`."""
        checker = load_checker()
        with tempfile.TemporaryDirectory() as temp_dir:
            consumer = Path(temp_dir) / "consumer"
            installed_script = (
                consumer / ".agents/skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py"
            )
            self.assertEqual(checker.workspace_root(installed_script), consumer.resolve())

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

    def test_selected_complete_task_allows_incremental_commit(self) -> None:
        """A completed selected task should not be blocked by later pending tasks."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            spec_dir = root / "specs" / "187-example"
            spec_dir.mkdir(parents=True)
            write_spec(spec_dir)
            for relative, old, new in (
                ("tasks.md", "- [x] T003.", "- [ ] T003."),
                ("plan.md", "- [x] T003", "- [ ] T003"),
                ("_ai_sdlc/plan.toon", "T003,done", "T003,pending"),
            ):
                path = spec_dir / relative
                path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
            write(root / "README.md", "example\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            result = subprocess.run(
                [
                    "python3",
                    str(CHECK_COMMIT_READY),
                    "--spec",
                    str(spec_dir),
                    "--task",
                    "T001",
                    "--quick-flow",
                    "--allow-unstaged",
                ],
                cwd=root,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stderr)

    def test_selected_incomplete_task_is_blocked(self) -> None:
        """Task-scoped readiness must fail when the selected task is pending."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            spec_dir = root / "specs" / "188-example"
            spec_dir.mkdir(parents=True)
            write_spec(spec_dir)
            tasks = spec_dir / "tasks.md"
            tasks.write_text(tasks.read_text(encoding="utf-8").replace("- [x] T003.", "- [ ] T003."), encoding="utf-8")
            plan = spec_dir / "plan.md"
            plan.write_text(plan.read_text(encoding="utf-8").replace("- [x] T003", "- [ ] T003"), encoding="utf-8")
            plan_toon = spec_dir / "_ai_sdlc/plan.toon"
            plan_toon.write_text(plan_toon.read_text(encoding="utf-8").replace("T003,done", "T003,pending"), encoding="utf-8")
            write(root / "README.md", "example\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            result = subprocess.run(
                [
                    "python3",
                    str(CHECK_COMMIT_READY),
                    "--spec",
                    str(spec_dir),
                    "--task",
                    "T003",
                    "--quick-flow",
                    "--allow-unstaged",
                ],
                cwd=root,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("selected task is incomplete", result.stderr)


if __name__ == "__main__":
    unittest.main()
