#!/usr/bin/env python3
"""Deterministic tests for AI SDLC SDD workflow helper scripts."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = ROOT / "skills" / "ai-sdlc-sdd" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def write(path: Path, text: str) -> None:
    """Write dedented fixture text with parent directories created."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def load_module(path: Path, name: str):
    """Load a script module by path so tests work with hyphenated skill dirs."""
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
PLAN_LINKS = load_module(SCRIPTS_DIR / "plan_links.py", "plan_links")
CHECK_REFINEMENT = load_module(SCRIPTS_DIR / "check_refinement_context.py", "check_refinement_context")


def write_full_design(spec_dir: Path) -> None:
    """Create a design artifact containing every required design section."""
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
    """Create a QA artifact containing every required QA section."""
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
    """Create test-case artifact coverage for AC-001 or an intentionally wrong AC."""
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


def write_full_tasks(
    spec_dir: Path,
    include_refs: bool = True,
    include_output: bool = True,
    completed: bool = False,
) -> None:
    """Create task artifact rows with optional Refs and Output metadata."""
    refs_line = "Refs: AC-001" if include_refs else ""
    output_line = "Output: Done." if include_output else ""
    write(
        spec_dir / "tasks.md",
        f"""
        # Tasks
        ## Implementation
        - [{'x' if completed else ' '}] T001. Example
        {output_line}
        {refs_line}
        ## Testing
        - [{'x' if completed else ' '}] T002. Example
        {output_line}
        {refs_line}
        ## Documentation
        - [{'x' if completed else ' '}] T003. Example
        {output_line}
        {refs_line}
        """,
    )


def write_full_plan(spec_dir: Path, include_ac: bool = True, include_tc: bool = True, include_tasks: bool = True) -> None:
    """Create plan.md linking SDD artifacts, ACs, TCs, tasks, and decisions."""
    ac = "AC-001" if include_ac else "AC-999"
    tc = "TC-001" if include_tc else "TC-999"
    task_refs = "T001, T002, T003" if include_tasks else "T999"
    write(
        spec_dir / "plan.md",
        f"""
        # plan.md
        ## Upstream Refinement Sources
        - Delivery spec: specs-refiniment/example/delivery-spec.md
        - QA readiness: specs-refiniment/example/qa-readiness.md
        ## SDD Artifact Links
        - requirements.md
        - design.md
        - test-cases.md
        - qa.md
        - tasks.md
        - _ai_sdlc/plan.toon
        - decision-log.md
        ## Cross-Artifact Trace Map
        - {ac}: requirements.md -> test-cases.md ({tc}) -> tasks.md ({task_refs}) -> qa.md -> decision-log.md
        ## Task Execution Plan
        - T001: Implementation.
        - T002: Testing.
        - T003: Documentation.
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


def write_full_plan_toon(spec_dir: Path, status: str = "pending") -> None:
    """Create _ai_sdlc/plan.toon linking task status and trace rows for gates."""
    write(
        spec_dir / "_ai_sdlc/plan.toon",
        f"""
        feature: example
        workspace: implementation
        flow_mode: quick
        updated_at: 2026-07-10
        source_artifacts[6]{{artifact,path}}:
          requirements,requirements.md
          design,design.md
          test_cases,test-cases.md
          qa,qa.md
          tasks,tasks.md
          decisions,decision-log.md
        trace[1]{{acceptance_id,test_cases,tasks}}:
          AC-001,TC-001,T001/T002/T003
        tasks[3]{{id,status,refs,tests,depends_on,artifact,decision_ref}}:
          T001,{status},AC-001,TC-001,none,Done.,DEC-001
          T002,{status},AC-001,TC-001,T001,Done.,DEC-001
          T003,{status},AC-001,TC-001,T001,Done.,DEC-001
        validation_sequence[5]{{step,command}}:
          1,check_refinement_context.py --full-flow
          2,check_clarify.py --full-flow
          3,check_checklist.py --full-flow
          4,plan_links.py --check --full-flow
          5,analyze_spec.py --full-flow && validate_spec.py --full-flow
        """,
    )


def write_requirements(
    spec_dir: Path,
    *,
    include_clarify: bool = True,
    measurable_acceptance: bool = True,
    explicit_out_of_scope: bool = True,
) -> None:
    """Create a requirements artifact with toggles for gate-failure scenarios."""
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
                "- AI assistant",
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
    def test_installed_layout_resolves_consumer_workspace_root(self) -> None:
        """Installed scripts must resolve relative specs from the consumer root."""
        with tempfile.TemporaryDirectory() as temp_dir:
            consumer = Path(temp_dir) / "consumer"
            installed_script = (
                consumer / ".agents/skills/ai-sdlc-sdd/scripts/spec_helpers.py"
            )
            self.assertEqual(SPEC_HELPERS.workspace_root(installed_script), consumer.resolve())

    """Tests for active feature spec resolution."""

    def test_resolves_explicit_spec(self) -> None:
        """Explicit spec paths should be authoritative."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            spec_dir = root / "specs" / "185-example"
            spec_dir.mkdir(parents=True)
            result = SPEC_HELPERS.resolve_active_spec(root=root, explicit="specs/185-example")
            self.assertEqual(result.spec_dir, spec_dir)
            self.assertEqual(result.source, "explicit")

    def test_resolves_unique_changed_spec(self) -> None:
        """Changed files that reference one spec should resolve that spec."""
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
        """Changed files referencing multiple specs should be rejected."""
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
    """Tests for clarify, checklist, and analyze gates."""

    def test_clarify_gate_fails_without_sections(self) -> None:
        """Clarify gate should require assumptions/questions/decision status."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir, include_clarify=False)
            errors = CHECK_CLARIFY.validate(spec_dir)
            self.assertTrue(any("Assumptions" in error for error in errors))

    def test_checklist_gate_fails_without_measurable_acceptance(self) -> None:
        """Checklist gate should reject vague acceptance and out-of-scope text."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir, measurable_acceptance=False, explicit_out_of_scope=False)
            errors = CHECK_CHECKLIST.validate(spec_dir)
            self.assertTrue(any("AC-###" in error or "observable" in error or "Out of Scope" in error for error in errors))

    def test_analyze_gate_fails_without_task_metadata(self) -> None:
        """Analyze gate should require task Refs metadata for traceability."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir, include_refs=False)
            write_full_plan(spec_dir)
            write_full_plan_toon(spec_dir)
            write_full_qa(spec_dir)
            errors = ANALYZE_SPEC.validate(spec_dir)
            self.assertTrue(any("task missing Refs:" in error for error in errors))

    def test_analyze_gate_fails_without_plan_links(self) -> None:
        """Analyze gate should require plan.md to link AC/TC/task IDs."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir)
            write_full_plan(spec_dir, include_tc=False)
            write_full_plan_toon(spec_dir)
            write_full_qa(spec_dir)
            errors = ANALYZE_SPEC.validate(spec_dir)
            self.assertTrue(any("test case not covered by plan.md" in error for error in errors))

    def test_plan_links_generates_and_checks_plan(self) -> None:
        """Plan helper should generate a checkable execution plan."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir)
            write_full_design(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir)
            write_full_qa(spec_dir)
            args = type(
                "Args",
                (),
                {
                    "feature": "example",
                    "quick_flow": True,
                    "full_flow": False,
                    "artifact_status": "draft",
                    "artifact_owner": "TBD",
                    "artifact_tag": [],
                },
            )()
            write(spec_dir / "_ai_sdlc/plan.toon", PLAN_LINKS.build_plan_toon(spec_dir, args))
            (spec_dir / "plan.md").write_text(PLAN_LINKS.build_plan(spec_dir, args), encoding="utf-8")
            self.assertEqual(PLAN_LINKS.check_plan(spec_dir), [])

    def test_plan_links_marks_done_tasks_from_authoritative_tasks(self) -> None:
        """Plan helper should derive completion from tasks.md, not stale projections."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir)
            write_full_design(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir, completed=True)
            write_full_qa(spec_dir)
            write_full_plan_toon(spec_dir, status="done")
            args = type(
                "Args",
                (),
                {
                    "feature": "example",
                    "quick_flow": True,
                    "full_flow": False,
                    "artifact_status": "draft",
                    "artifact_owner": "TBD",
                    "artifact_tag": [],
                },
            )()
            plan_md = PLAN_LINKS.build_plan(spec_dir, args)
            self.assertIn("- [x] T001:", plan_md)
            self.assertIn("- [x] T002:", plan_md)
            self.assertIn("- [x] T003:", plan_md)

    def test_plan_check_rejects_status_drift_from_tasks(self) -> None:
        """A stale machine or human plan must not override task checkboxes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir)
            write_full_design(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir, completed=True)
            write_full_qa(spec_dir)
            write_full_plan_toon(spec_dir, status="pending")
            write_full_plan(spec_dir)
            errors = PLAN_LINKS.check_plan(spec_dir)
            self.assertTrue(any("authoritative tasks.md" in error for error in errors))

    def test_refinement_gate_blocks_full_flow_without_upstream(self) -> None:
        """Full-flow SDD should block when upstream refinement context is absent."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            errors = SPEC_HELPERS.upstream_refinement_errors(spec_dir)
            self.assertTrue(any("missing upstream refinement state" in error for error in errors))

    def test_refinement_gate_passes_completed_upstream(self) -> None:
        """Full-flow SDD should pass when delivery and QA refinement are complete."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            spec_dir = root / "185-example"
            spec_dir.mkdir()
            refinement_dir = root / "specs-refiniment" / "example"
            write(
                refinement_dir / "_ai_sdlc/state.toon",
                """
                feature: example
                workspace: refinement
                current_stage: qa_traceability
                active_skill:
                flow_mode: full
                updated_at: 2026-07-10
                decision_log: specs-refiniment/example/decision-log.md

                stages[2]{id,skill,status,workspace,artifacts,decision_ref}:
                  delivery_spec,ai-sdlc-delivery-spec-synthesis,done,refinement,delivery-spec.md,DEC-001
                  qa_traceability,ai-sdlc-qa-traceability-and-readiness-review,done,refinement,qa-readiness.md,DEC-001

                skips[0]{stage,reason,decision_ref,flow_mode}:
                """,
            )
            write(refinement_dir / "delivery-spec.md", "# Delivery Spec\n")
            write(refinement_dir / "qa-readiness.md", "# QA Readiness\n")
            self.assertEqual(SPEC_HELPERS.upstream_refinement_errors(spec_dir), [])


class StatusTests(unittest.TestCase):
    """Tests for SDD workflow state evaluation."""

    def test_status_reports_needs_clarify(self) -> None:
        """Status should stop at clarify when clarify sections are missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir, include_clarify=False)
            write_full_design(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir)
            write_full_plan(spec_dir)
            write_full_plan_toon(spec_dir)
            write_full_qa(spec_dir)
            state, reasons = SDD_STATUS.evaluate_status(spec_dir)
            self.assertEqual(state, "needs_clarify")
            self.assertTrue(reasons)

    def test_status_reports_needs_checklist(self) -> None:
        """Status should stop at checklist when requirement quality is weak."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir, measurable_acceptance=False)
            write_full_design(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir)
            write_full_plan(spec_dir)
            write_full_plan_toon(spec_dir)
            write_full_qa(spec_dir)
            state, _ = SDD_STATUS.evaluate_status(spec_dir)
            self.assertEqual(state, "needs_checklist")

    def test_status_reports_needs_analyze(self) -> None:
        """Status should stop at analyze when cross-artifact refs are missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir)
            write_full_design(spec_dir)
            write_full_test_cases(spec_dir, include_ac=False)
            write_full_tasks(spec_dir)
            write_full_plan(spec_dir)
            write_full_plan_toon(spec_dir)
            write_full_qa(spec_dir)
            state, _ = SDD_STATUS.evaluate_status(spec_dir)
            self.assertEqual(state, "needs_analyze")

    def test_status_reports_ready_for_impl(self) -> None:
        """Status should report ready when all workflow gates pass."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "185-example"
            spec_dir.mkdir()
            write_requirements(spec_dir)
            write_full_design(spec_dir)
            write_full_test_cases(spec_dir)
            write_full_tasks(spec_dir)
            write_full_plan(spec_dir)
            write_full_plan_toon(spec_dir)
            write_full_qa(spec_dir)
            state, reasons = SDD_STATUS.evaluate_status(spec_dir)
            self.assertEqual(state, "ready_for_impl")
            self.assertEqual(reasons, [])


class RepositoryProjectionTests(unittest.TestCase):
    """Keep every committed SDD plan aligned with authoritative task checkboxes."""

    def test_all_repository_plan_projections_match_tasks(self) -> None:
        checked = 0
        for spec_dir in sorted((ROOT / "specs").glob("[0-9][0-9][0-9]-*")):
            if not (spec_dir / "tasks.md").is_file():
                continue
            checked += 1
            self.assertEqual(PLAN_LINKS.check_plan(spec_dir), [], spec_dir.name)
        self.assertGreaterEqual(checked, 8)


if __name__ == "__main__":
    unittest.main()
