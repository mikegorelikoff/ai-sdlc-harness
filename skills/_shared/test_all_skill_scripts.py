#!/usr/bin/env python3
"""Repository-wide tests for AI SDLC helper scripts.

This suite verifies the cross-skill script contract from one place: compilation,
CLI help, artifact-profile quick/full behavior, write behavior, SDD gate flags,
and specialized flow semantics for non-profile scripts.
"""

from __future__ import annotations

import os
import py_compile
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"


def write(path: Path, text: str) -> None:
    """Write dedented fixture text with parent directories created."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def script_paths() -> list[Path]:
    """Return runtime scripts and shared executable helpers covered by this suite."""
    paths = sorted((ROOT / "skills").glob("*/scripts/*.py"))
    paths.extend(sorted((ROOT / "skills" / "_shared").glob("*.py")))
    non_runtime_helpers = {"ai_sdlc_artifact_helper.py", "ai_sdlc_state_machine.py", "skill_script_contract.py"}
    return [
        path
        for path in paths
        if path.name not in non_runtime_helpers and "unittest" not in path.read_text(encoding="utf-8")
    ]


def cli_script_paths() -> list[Path]:
    """Return scripts that expose argparse help and should accept `--help`."""
    return [
        path
        for path in script_paths()
        if "ArgumentParser" in path.read_text(encoding="utf-8")
    ]


def artifact_profile_scripts() -> list[Path]:
    """Return skill wrappers using the shared artifact-profile helper."""
    return [
        path
        for path in script_paths()
        if "emit_profile_report(" in path.read_text(encoding="utf-8") and path.name != "ai_sdlc_artifact_helper.py"
    ]


def run_script(path: Path, *args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    """Run a Python helper script with captured output and temp pycache."""
    env = os.environ.copy()
    env["PYTHONPYCACHEPREFIX"] = "/tmp/ai-sdlc-harness-pycache"
    return subprocess.run(
        [sys.executable, str(path), *args],
        cwd=cwd,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def write_valid_spec(spec_dir: Path) -> None:
    """Create a complete SDD fixture that should pass all gate scripts."""
    write(
        spec_dir / "requirements.md",
        """
        # Requirements
        ## Goal
        Deliver a portable helper-script test fixture.
        ## Problem Statement
        Helper scripts need deterministic coverage.
        ## Scope
        Validate the script contract.
        ## Actors
        - AI assistant
        ## Inputs
        - Source artifacts
        ## Outputs
        - Validated reports
        ## Functional Requirements
        - REQ-001: Scripts must accept flow flags.
        ## Non-Functional Requirements
        - Deterministic and local.
        ## Constraints
        - No vendor-specific runtime path.
        ## Assumptions
        - Accepted assumption: local Python is available.
        ## Open Questions
        - None.
        ## Decision Status
        - All blocking decisions resolved.
        ## Acceptance Criteria
        - AC-001: Given a valid spec, when helper gates run, then they pass deterministically.
        ## Out of Scope
        - Networked validation.
        """,
    )
    write(
        spec_dir / "design.md",
        """
        # Design
        ## Overview
        Local helper test fixture.
        ## Architecture
        Python scripts run locally.
        ## Components
        Shared helper and skill wrappers.
        ## Interfaces and Contracts
        CLI arguments.
        ## Data Model
        Markdown files.
        ## Error Handling
        Non-zero exits for failures.
        ## Security Considerations
        Local-only execution.
        ## Observability
        Text output.
        ## Risks and Tradeoffs
        Minimal fixture scope.
        ## Validation Strategy
        Unit tests and py_compile.
        ## Migration Notes
        None.
        """,
    )
    write(
        spec_dir / "tasks.md",
        """
        # Tasks
        ## Implementation
        - [x] T001. Add portable helper tests
        Output: tests added.
        Refs: AC-001
        ## Testing
        - [x] T002. Run helper test suite
        Output: tests passed.
        Refs: AC-001
        ## Documentation
        - [x] T003. Keep script contract documented
        Output: SKILL references updated.
        Refs: AC-001
        """,
    )
    write(
        spec_dir / "test-cases.md",
        """
        # Test Cases
        ## Scope
        Helper scripts.
        ## Scenario Matrix
        | ID | Spec ref | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
        | --- | --- | --- | --- | --- | --- | --- | --- |
        | TC-001 | AC-001 | Run helper gates | Valid fixture | Execute scripts | AC-001 passes | unit | unittest |
        ## Layer Mapping
        Unit.
        ## Automation Plan
        unittest.
        ## Open Gaps
        None.
        """,
    )
    write(
        spec_dir / "qa.md",
        """
        # QA
        ## Change Summary
        Helper script coverage.
        ## Acceptance Scenarios
        AC-001.
        ## Regression Targets
        Script CLI flags.
        ## Risk Notes
        Low.
        ## Validation Commands
        - python3 skills/_shared/test_all_skill_scripts.py
        ## Manual Checks
        - Inspect generated reports.
        ## Signoff
        Pending.
        """,
    )
    write(
        spec_dir / "plan.md",
        """
        # plan.md
        ## Upstream Refinement Sources
        - Delivery spec: specs-refiniment/script-contract/delivery-spec.md
        - QA readiness: specs-refiniment/script-contract/qa-readiness.md
        ## SDD Artifact Links
        - requirements.md
        - design.md
        - test-cases.md
        - qa.md
        - tasks.md
        - plan.toon
        - decision-log.md
        ## Cross-Artifact Trace Map
        - AC-001: requirements.md -> test-cases.md (TC-001) -> tasks.md (T001, T002, T003) -> qa.md -> decision-log.md
        ## Task Execution Plan
        - T001: Add portable helper tests; refs: AC-001
        - T002: Run helper test suite; refs: AC-001
        - T003: Keep script contract documented; refs: AC-001
        ## Task Dependencies
        - T001: depends on none
        - T002: depends on T001
        - T003: depends on T001
        ## Validation Sequence
        - python3 skills/_shared/test_all_skill_scripts.py
        ## Open Links And Blockers
        - None.
        """,
    )
    write(
        spec_dir / "plan.toon",
        """
        feature: script-contract
        workspace: implementation
        flow_mode: full
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
          T001,done,AC-001,TC-001,none,tests added.,DEC-001
          T002,done,AC-001,TC-001,T001,tests passed.,DEC-001
          T003,done,AC-001,TC-001,T001,SKILL references updated.,DEC-001
        validation_sequence[5]{step,command}:
          1,check_refinement_context.py --full-flow
          2,check_clarify.py --full-flow
          3,check_checklist.py --full-flow
          4,plan_links.py --check --full-flow
          5,analyze_spec.py --full-flow && validate_spec.py --full-flow
        """,
    )
    write(
        spec_dir / "decision-log.md",
        """
        # Decision Log

        | ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
        | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        | DEC-001 | 2026-07-09 | accepted | QA | Test every helper script | helper contract | centralized suite | scripts | test_all_skill_scripts.py |
        """,
    )
    feature = spec_dir.name.split("-", 1)[1] if "-" in spec_dir.name else spec_dir.name
    refinement_dir = spec_dir.parent / "specs-refiniment" / feature
    write(
        refinement_dir / "state.toon",
        f"""
        feature: {feature}
        workspace: refinement
        current_stage: qa_traceability
        active_skill:
        flow_mode: full
        updated_at: 2026-07-10
        decision_log: specs-refiniment/{feature}/decision-log.md

        stages[2]{{id,skill,status,workspace,artifacts,decision_ref}}:
          delivery_spec,ai-sdlc-delivery-spec-synthesis,done,refinement,delivery-spec.md,DEC-001
          qa_traceability,ai-sdlc-qa-traceability-and-readiness-review,done,refinement,qa-readiness.md,DEC-001

        skips[0]{{stage,reason,decision_ref,flow_mode}}:
        """,
    )
    write(refinement_dir / "delivery-spec.md", "# Delivery Spec\n")
    write(refinement_dir / "qa-readiness.md", "# QA Readiness\n")


class ScriptContractTests(unittest.TestCase):
    """Repository-wide assertions for helper script behavior."""

    def test_every_script_compiles(self) -> None:
        """Every runtime helper must be syntactically valid Python."""
        for path in script_paths():
            with self.subTest(path=path.relative_to(ROOT)):
                cache_name = str(path.relative_to(ROOT)).replace("/", "__") + ".pyc"
                py_compile.compile(str(path), cfile=str(Path("/tmp") / "ai-sdlc-harness-pycache" / cache_name), doraise=True)

    def test_every_cli_script_has_help(self) -> None:
        """Every argparse CLI must support token-cheap usage discovery."""
        for path in cli_script_paths():
            with self.subTest(path=path.relative_to(ROOT)):
                result = run_script(path, "--help")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("usage:", result.stdout.lower())

    def test_every_cli_script_exposes_state_flags(self) -> None:
        """Every CLI helper should expose the shared feature-state flags."""
        for path in cli_script_paths():
            if path.name in {"state_machine.py", "ai_sdlc_specs_index.py"}:
                continue
            with self.subTest(path=path.relative_to(ROOT)):
                result = run_script(path, "--help")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("--state-check", result.stdout)
                self.assertIn("--begin-state", result.stdout)
                self.assertIn("--complete-state", result.stdout)

    def test_artifact_profile_scripts_expose_metadata_flags(self) -> None:
        """Artifact-profile CLIs must let agents annotate generated artifacts."""
        for path in artifact_profile_scripts():
            with self.subTest(path=path.relative_to(ROOT)):
                result = run_script(path, "--help")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("--artifact-status", result.stdout)
                self.assertIn("--artifact-owner", result.stdout)
                self.assertIn("--artifact-tag", result.stdout)

    def test_artifact_profile_scripts_materialize_quick_and_full_outputs(self) -> None:
        """Artifact-profile scripts must emit flow-specific templates and logs."""
        self.assertGreaterEqual(len(artifact_profile_scripts()), 20)
        for path in artifact_profile_scripts():
            for flag, expected in (("--quick-flow", "Assumption/default"), ("--full-flow", "Open questions/blockers")):
                with self.subTest(path=path.relative_to(ROOT), flag=flag):
                    result = run_script(
                        path,
                        "--feature",
                        "script-contract",
                        flag,
                        "--emit-template",
                        "--emit-decision-log-entry",
                        str(README),
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn(f"Flow mode: {flag.removeprefix('--').removesuffix('-flow')}", result.stdout)
                    self.assertIn("Target artifact:", result.stdout)
                    self.assertIn("Decision Log Entry", result.stdout)
                    self.assertIn("Artifact Template", result.stdout)
                    self.assertIn("artifact_metadata:", result.stdout)
                    self.assertIn("schema: \"ai-sdlc-artifact-metadata/v1\"", result.stdout)
                    self.assertIn("metatags:", result.stdout)
                    self.assertIn(expected, result.stdout)

    def test_artifact_profile_write_creates_target_files(self) -> None:
        """`--write` must create both the routed artifact and decision log."""
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            cwd = Path(temp_dir)
            script = ROOT / "skills/ai-sdlc-ba/scripts/ba_context_scaffold.py"
            input_file = cwd / "notes.md"
            write(input_file, "# Notes\n\nCustomer needs a faster workflow with AC-001.\n")

            result = run_script(
                script,
                "--feature",
                "write-contract",
                "--quick-flow",
                "--write",
                str(input_file),
                cwd=cwd,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            artifact = cwd / "specs-refiniment/write-contract/business-context.md"
            decision_log = cwd / "specs-refiniment/write-contract/decision-log.md"
            toon_index = cwd / "specs-refiniment/specs-index.toon"
            md_index = cwd / "specs-refiniment/specs-index.md"
            self.assertTrue(artifact.is_file())
            self.assertTrue(decision_log.is_file())
            self.assertTrue(toon_index.is_file())
            self.assertTrue(md_index.is_file())
            artifact_text = artifact.read_text(encoding="utf-8")
            self.assertIn("artifact_metadata:", artifact_text)
            self.assertIn("skill: \"ai-sdlc-ba\"", artifact_text)
            self.assertIn("metatags:", artifact_text)
            self.assertIn("Assumption/default", artifact_text)
            decision_log_text = decision_log.read_text(encoding="utf-8")
            self.assertIn("artifact_metadata:", decision_log_text)
            self.assertIn("artifact: \"decision-log.md\"", decision_log_text)
            self.assertIn("metatags:", decision_log_text)
            self.assertIn("DEC-001", decision_log_text)
            self.assertIn("features[1]", toon_index.read_text(encoding="utf-8"))
            self.assertIn("business-context.md", md_index.read_text(encoding="utf-8"))

    def test_specs_index_cli_writes_toon_and_markdown_indexes(self) -> None:
        """Specs index CLI must summarize features for LLMs and humans."""
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            cwd = Path(temp_dir)
            write(
                cwd / "specs-refiniment/demo/state.toon",
                """
                feature: demo
                workspace: refinement
                current_stage: ba_context
                active_skill:
                flow_mode: quick
                updated_at: 2026-07-10
                decision_log: specs-refiniment/demo/decision-log.md

                stages[1]{id,skill,status,workspace,artifacts,decision_ref}:
                  ba_context,ai-sdlc-ba,done,refinement,business-context.md,DEC-001

                skips[0]{stage,reason,decision_ref,flow_mode}:
                """,
            )
            write(
                cwd / "specs-refiniment/demo/business-context.md",
                """
                ---
                artifact_metadata:
                  schema: "ai-sdlc-artifact-metadata/v1"
                  feature: "demo"
                  artifact: "business-context.md"
                  path: "specs-refiniment/demo/business-context.md"
                  workspace: "refinement"
                  skill: "ai-sdlc-ba"
                  flow_mode: "quick"
                  state_file: "specs-refiniment/demo/state.toon"
                  decision_log: "specs-refiniment/demo/decision-log.md"
                  status: "draft"
                  owner: "BA"
                  created_at: "2026-07-10"
                  updated_at: "2026-07-10"
                  trace_ids: []
                  related_artifacts: []
                  validation: []
                  metatags:
                    - "ai-sdlc"
                    - "refinement"
                    - "ai-sdlc-ba"
                    - "business-context"
                    - "draft"
                ---

                # business-context.md
                """,
            )
            result = run_script(
                ROOT / "skills/_shared/ai_sdlc_specs_index.py",
                "--workspace",
                "refinement",
                "--full-flow",
                cwd=cwd,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            toon_index = cwd / "specs-refiniment/specs-index.toon"
            md_index = cwd / "specs-refiniment/specs-index.md"
            self.assertTrue(toon_index.is_file())
            self.assertTrue(md_index.is_file())
            self.assertIn("features[1]", toon_index.read_text(encoding="utf-8"))
            self.assertIn("artifacts[1]", toon_index.read_text(encoding="utf-8"))
            self.assertIn("business-context.md", md_index.read_text(encoding="utf-8"))

    def test_sdd_gate_scripts_accept_flow_flags_against_valid_spec(self) -> None:
        """SDD gate CLIs must accept quick/full flags against a valid spec."""
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            spec_dir = Path(temp_dir) / "999-script-contract"
            write_valid_spec(spec_dir)
            for script in [
                ROOT / "skills/ai-sdlc-sdd/scripts/validate_spec.py",
                ROOT / "skills/ai-sdlc-sdd/scripts/check_clarify.py",
                ROOT / "skills/ai-sdlc-sdd/scripts/check_checklist.py",
                ROOT / "skills/ai-sdlc-sdd/scripts/analyze_spec.py",
                ROOT / "skills/ai-sdlc-sdd/scripts/plan_links.py",
                ROOT / "skills/ai-sdlc-sdd/scripts/check_refinement_context.py",
            ]:
                with self.subTest(script=script.name):
                    extra = ("--check",) if script.name == "plan_links.py" else ()
                    result = run_script(script, str(spec_dir), "--full-flow", *extra, cwd=Path(temp_dir))
                    self.assertEqual(result.returncode, 0, result.stderr)
            status = run_script(ROOT / "skills/ai-sdlc-sdd/scripts/sdd_status.py", "--spec", str(spec_dir), "--full-flow")
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("ready_for_impl", status.stdout)
            resolved = run_script(ROOT / "skills/ai-sdlc-sdd/scripts/resolve_active_spec.py", str(spec_dir), "--quick-flow")
            self.assertEqual(resolved.returncode, 0, resolved.stderr)
            self.assertIn("explicit", resolved.stdout)

    def test_specialized_flow_semantics(self) -> None:
        """Non-profile scripts must expose the expected quick/full behavior."""
        approval = run_script(
            ROOT / "skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py",
            "--command",
            "git status",
            "--justification",
            "Do you want to inspect repository status?",
            "--quick-flow",
        )
        self.assertEqual(approval.returncode, 0, approval.stderr)

        quick_commit = run_script(
            ROOT / "skills/ai-sdlc-conventional-commit/scripts/validate_commit_msg.py",
            "--message",
            "docs: update helper scripts",
            "--quick-flow",
        )
        self.assertEqual(quick_commit.returncode, 0, quick_commit.stderr)

        full_commit = run_script(
            ROOT / "skills/ai-sdlc-conventional-commit/scripts/validate_commit_msg.py",
            "--message",
            "docs: update helper scripts",
            "--full-flow",
        )
        self.assertEqual(full_commit.returncode, 1)
        self.assertIn("Spec traceability", full_commit.stderr)

        validation = run_script(
            ROOT / "skills/ai-sdlc-validation/scripts/validation_plan.py",
            "--quick-flow",
            "skills/ai-sdlc-ba/scripts/ba_context_scaffold.py",
        )
        self.assertEqual(validation.returncode, 0, validation.stderr)
        self.assertIn("quick flow", validation.stdout)

        review = run_script(ROOT / "skills/ai-sdlc-code-review/scripts/review_readiness.py", "--quick-flow")
        self.assertIn(review.returncode, {0, 1})

    def test_every_skill_documents_feature_state_machine(self) -> None:
        """Every skill must instruct agents to honor state.toon sequencing."""
        for skill_doc in sorted((ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill_doc=skill_doc.relative_to(ROOT)):
                text = skill_doc.read_text(encoding="utf-8")
                self.assertIn("## 0.5 Feature State Machine", text)
                self.assertIn("state.toon", text)

    def test_every_skill_documents_artifact_metadata(self) -> None:
        """Every skill must require canonical artifact metadata and metatags."""
        for skill_doc in sorted((ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill_doc=skill_doc.relative_to(ROOT)):
                text = skill_doc.read_text(encoding="utf-8")
                self.assertIn("## 0.6 Artifact Metadata And Metatags", text)
                self.assertIn("artifact_metadata", text)
                self.assertIn("metatags", text)

    def test_every_skill_documents_specs_index(self) -> None:
        """Every skill must tell agents to use and refresh specs indexes."""
        for skill_doc in sorted((ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill_doc=skill_doc.relative_to(ROOT)):
                text = skill_doc.read_text(encoding="utf-8")
                self.assertIn("## 0.7 Specs Index", text)
                self.assertIn("specs-index.toon", text)
                self.assertIn("specs-index.md", text)


if __name__ == "__main__":
    unittest.main()
