#!/usr/bin/env python3
"""Deterministic tests for AI SDLC SDD workflow helper scripts."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_DIR = ROOT / ".codex" / "skills" / "ai-sdlc-sdd" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SPEC_HELPERS = load_module(SCRIPTS_DIR / "spec_helpers.py", "spec_helpers")
CHECK_CLARIFY = load_module(SCRIPTS_DIR / "check_clarify.py", "check_clarify")
CHECK_CHECKLIST = load_module(SCRIPTS_DIR / "check_checklist.py", "check_checklist")
ANALYZE_SPEC = load_module(SCRIPTS_DIR / "analyze_spec.py", "analyze_spec")
SDD_STATUS = load_module(SCRIPTS_DIR / "sdd_status.py", "sdd_status")


def write_full_design(spec_dir: Path) -> None:
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
        Data model.
        ## Error Handling
        Errors.
        ## Security Considerations
        Security.
        ## Observability
        Observability.
        ## Risks and Tradeoffs
        Risks.
        ## Validation Strategy
        Validation.
        ## Migration Notes
        None.
        """,
    )


def write_full_qa(spec_dir: Path) -> None:
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


def write_full_test_cases(spec_dir: Path, include_ac: bool = True) -> None:
    spec_ref = "AC-001" if include_ac else "AC-999"
    write(
        spec_dir / "test-cases.md",
        f"""
        # Test Cases
        ## Scope
        Covered.
        ## Scenario Matrix
        | ID | Spec ref | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
        | --- | --- | --- | --- | --- | --- | --- | --- |
        | TC-001 | {spec_ref} | Scenario | Setup | Trigger | Outcome | unit | command |
        ## Layer Mapping
        Mapped.
        ## Automation Plan
        Planned.
        ## Open Gaps
        None.
        """,
    )


def write_full_tasks(spec_dir: Path, include_refs: bool = True, include_output: bool = True) -> None:
    refs_line = "Refs: AC-001" if include_refs else ""
    output_line = "Output: Done." if include_output else ""
    write(
        spec_dir / "tasks.md",
        f"""
        # Tasks
        ## Implementation
        - [ ] T001. Example
        {output_line}
        {refs_line}
        ## Testing
        - [ ] T002. Example
        {output_line}
        {refs_line}
        ## Documentation
        - [ ] T003. Example
        {output_line}
        {refs_line}
        """,
    )


def write_requirements(
    spec_dir: Path,
    *,
    include_clarify: bool = True,
    measurable_acceptance: bool = True,
    explicit_out_of_scope: bool = True,
) -> None:
    sections = [
        "# Requirements",
        "## Goal",
        "Goal.",
        "- `1215120493851958`",
        "## Problem Statement",
        "Problem.",
        "## Scope",
        "Scope.",
        "## Actors",
        "- Codex",
        "## Inputs",
        "- Request",
        "## Outputs",
        "- Spec",
        "## Functional Requirements",
        "- Requirement.",
        "## Non-Functional Requirements",
        "- Deterministic.",
        "## Constraints",
        "- Local only.",
    ]
    if include_clarify:
        sections.extend(
            [
                "## Assumptions",
                "- Accepted assumption.",
                "## Open Questions",
                "- None for this slice.",
                "## Decision Status",
                "- All blocking decisions resolved.",
            ]
        )
    sections.extend(
        [
            "## Acceptance Criteria",
            "- AC-001: Given a spec, when validation runs, then it passes."
            if measurable_acceptance
            else "- Works correctly.",
            "## Out of Scope",
            "- Unrelated work." if explicit_out_of_scope else "- None",
        ]
    )
    write(spec_dir / "requirements.md", "\n".join(sections))


class ResolveActiveSpecTests(unittest.TestCase):
    def test_resolves_explicit_spec(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            spec_dir = root / "specs" / "185-example"
            spec_dir.mkdir(parents=True)
            result = SPEC_HELPERS.resolve_active_spec(root=root, explicit="specs/185-example")
            self.assertEqual(result.spec_dir, spec_dir)
            self.assertEqual(result.source, "explicit")

    def test_resolves_unique_changed_spec(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            spec_dir = root / "specs" / "185-example"
            spec_dir.mkdir(parents=True)
            result = SPEC_HELPERS.resolve_active_spec(
                root=root,
                files=["specs/185-example/requirements.md", "internal/service/example.go"],
                branch="dev",
            )
            self.assertEqual(result.spec_dir, spec_dir)
            self.assertEqual(result.source, "changed-files")

    def test_ambiguous_changed_specs_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "specs" / "185-a").mkdir(parents=True)
            (root / "specs" / "186-b").mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, "multiple feature specs"):
                SPEC_HELPERS.resolve_from_files(
                    ["specs/185-a/requirements.md", "specs/186-b/design.md"],
                    root=root,
                )


class GateTests(unittest.TestCase):
    def test_clarify_gate_fails_without_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir, include_clarify=False)
            errors = CHECK_CLARIFY.validate(spec_dir)
            self.assertTrue(any("Assumptions" in error for error in errors))

    def test_checklist_gate_fails_without_measurable_acceptance(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir, measurable_acceptance=False, explicit_out_of_scope=False)
            errors = CHECK_CHECKLIST.validate(spec_dir)
            self.assertTrue(any("AC-###" in error or "observable" in error or "Out of Scope" in error for error in errors))

    def test_analyze_gate_fails_without_task_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir, include_refs=False)
            write_full_qa(spec_dir)
            errors = ANALYZE_SPEC.validate(spec_dir)
            self.assertTrue(any("task missing Refs:" in error for error in errors))


class StatusTests(unittest.TestCase):
    def test_status_reports_needs_clarify(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir, include_clarify=False)
            write_full_design(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir)
            write_full_qa(spec_dir)
            state, reasons = SDD_STATUS.evaluate_status(spec_dir)
            self.assertEqual(state, "needs_clarify")
            self.assertTrue(reasons)

    def test_status_reports_needs_checklist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir, measurable_acceptance=False)
            write_full_design(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir)
            write_full_qa(spec_dir)
            state, _ = SDD_STATUS.evaluate_status(spec_dir)
            self.assertEqual(state, "needs_checklist")

    def test_status_reports_needs_analyze(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir)
            write_full_design(spec_dir)
            write_full_test_cases(spec_dir, include_ac=False)
            write_full_tasks(spec_dir)
            write_full_qa(spec_dir)
            state, _ = SDD_STATUS.evaluate_status(spec_dir)
            self.assertEqual(state, "needs_analyze")

    def test_status_reports_ready_for_impl(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir)
            write_full_design(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir)
            write_full_qa(spec_dir)
            state, reasons = SDD_STATUS.evaluate_status(spec_dir)
            self.assertEqual(state, "ready_for_impl")
            self.assertEqual(reasons, [])


if __name__ == "__main__":
    unittest.main()
