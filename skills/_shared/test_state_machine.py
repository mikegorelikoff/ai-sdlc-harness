#!/usr/bin/env python3
"""Tests for feature state.toon lifecycle enforcement."""

from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import ai_sdlc_state_machine as sm
import ai_sdlc_validation_receipt as vr


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "skills" / "_shared" / "state_machine.py"


class StateMachineTests(unittest.TestCase):
    """Unit and CLI tests for the AI SDLC state machine."""

    def test_init_rejects_symlinked_feature_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp); repository = parent / "repo"; outside = parent / "outside"
            (repository / "specs").mkdir(parents=True); outside.mkdir()
            (repository / "specs/demo").symlink_to(outside, target_is_directory=True)
            result = subprocess.run(
                [sys.executable, str(CLI), "init", "--feature", "demo", "--workspace", "implementation"],
                cwd=repository, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((outside / "_ai_sdlc/state.toon").exists())
            self.assertNotIn("Traceback", result.stderr)

    def test_toon_round_trip_preserves_stage_rows(self) -> None:
        """Serialized TOON should parse back into equivalent core fields."""
        state = sm.initial_state("demo-feature", "refinement", "discovery")
        text = sm.to_toon(state)
        parsed = sm.from_toon(text)
        self.assertEqual(parsed["feature"], "demo-feature")
        self.assertEqual(parsed["current_stage"], "discovery")
        self.assertEqual(len(parsed["stages"]), len(state["stages"]))

    def test_full_flow_blocks_missing_predecessors(self) -> None:
        """Full flow should reject a downstream skill with incomplete predecessors."""
        state = sm.initial_state("demo-feature", "refinement", "discovery")
        errors, warnings = sm.validate_transition(state, "ai-sdlc-test-scope-and-strategy-design", "full")
        self.assertTrue(errors)
        self.assertFalse(warnings)

    def test_quick_flow_allows_skip_only_with_trace(self) -> None:
        """Quick flow can skip predecessors only with assumption or decision trace."""
        state = sm.initial_state("demo-feature", "refinement", "discovery")
        errors_without_trace, _ = sm.validate_transition(state, "ai-sdlc-test-scope-and-strategy-design", "quick")
        errors_with_trace, warnings = sm.validate_transition(
            state,
            "ai-sdlc-test-scope-and-strategy-design",
            "quick",
            decision_ref="DEC-001",
        )
        self.assertTrue(errors_without_trace)
        self.assertFalse(errors_with_trace)
        self.assertTrue(warnings)

    def test_begin_and_complete_update_state(self) -> None:
        """Begin/complete should lock and then release the active skill."""
        state = sm.initial_state("demo-feature", "refinement", "discovery")
        errors, _ = sm.begin_stage(state, "ai-sdlc-working-backwards-discovery", "full")
        self.assertFalse(errors)
        self.assertEqual(state["active_skill"], "ai-sdlc-working-backwards-discovery")
        errors, _ = sm.complete_stage(
            state,
            "ai-sdlc-working-backwards-discovery",
            "specs-refiniment/demo-feature/discovery.md",
            "DEC-001",
            "full",
        )
        self.assertFalse(errors)
        self.assertEqual(state["active_skill"], "")
        self.assertEqual(sm.stage_row(state, "discovery")["status"], "done")

    def test_complete_rejects_missing_begin_and_artifact(self) -> None:
        """A caller cannot manufacture done state without active work and evidence."""
        state = sm.initial_state("demo-feature", "refinement", "discovery")
        errors, _ = sm.complete_stage(
            state, "ai-sdlc-working-backwards-discovery", "", "", "full"
        )
        self.assertTrue(any("begun" in error for error in errors))
        self.assertTrue(any("artifact" in error for error in errors))
        self.assertEqual(sm.stage_row(state, "discovery")["status"], "not_started")

    def test_full_completion_requires_existing_finalized_canonical_artifact(self) -> None:
        """Full refinement completion binds state to finalized canonical evidence."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state = sm.initial_state("demo-feature", "refinement", "discovery")
            errors, _ = sm.begin_stage(state, "ai-sdlc-working-backwards-discovery", "full")
            self.assertFalse(errors)
            relative = Path("specs-refiniment/demo-feature/discovery.md")
            self.assertTrue(sm.completion_artifact_errors(state, "ai-sdlc-working-backwards-discovery", relative.as_posix(), "full", root))
            artifact = root / relative
            artifact.parent.mkdir(parents=True)
            artifact.write_text(
                '---\nartifact_metadata:\n  schema: "ai-sdlc-artifact-metadata/v1"\n  status: "review"\n---\n# Discovery\n\nReviewed customer problem and decision evidence.\n',
                encoding="utf-8",
            )
            self.assertEqual(
                sm.completion_artifact_errors(state, "ai-sdlc-working-backwards-discovery", relative.as_posix(), "full", root),
                [],
            )

    def test_cli_init_and_status(self) -> None:
        """The CLI should create a state file and print TOON status."""
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            cwd = Path(temp_dir)
            init = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "init",
                    "--feature",
                    "cli-demo",
                    "--workspace",
                    "refinement",
                ],
                cwd=cwd,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            self.assertTrue((cwd / "specs-refiniment/cli-demo/_ai_sdlc/state.toon").is_file())

            status = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "status",
                    "--feature",
                    "cli-demo",
                    "--workspace",
                    "refinement",
                ],
                cwd=cwd,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("feature: cli-demo", status.stdout)
            self.assertIn("stages[", status.stdout)

    def test_cli_rejects_evidence_free_full_completion(self) -> None:
        """Direct CLI cannot mark a full-flow stage done without begin/artifact evidence."""
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            init = subprocess.run(
                [sys.executable, str(CLI), "init", "--feature", "no-evidence", "--workspace", "refinement"],
                cwd=temp_dir, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            complete = subprocess.run(
                [
                    sys.executable, str(CLI), "complete", "--feature", "no-evidence",
                    "--workspace", "refinement", "--skill",
                    "ai-sdlc-working-backwards-discovery", "--full-flow",
                ],
                cwd=temp_dir, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(complete.returncode, 1)
            self.assertIn("--artifacts is required", complete.stderr)
            state = sm.load_state(Path(temp_dir) / "specs-refiniment/no-evidence/_ai_sdlc/state.toon")
            self.assertEqual(sm.stage_row(state, "discovery")["status"], "not_started")

    def test_empty_canonical_sdd_directory_is_rejected(self) -> None:
        """A directory name alone is not SDD completion evidence."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state = sm.initial_state("empty-sdd", "implementation")
            spec = root / "specs/empty-sdd"
            spec.mkdir(parents=True)
            errors = sm.completion_artifact_errors(
                state, "ai-sdlc-sdd", "specs/empty-sdd", "quick", root
            )
            self.assertTrue(errors)
            self.assertTrue(any("requirements.md" in error for error in errors))

    def test_empty_canonical_stage_file_is_rejected(self) -> None:
        """An empty canonical review file cannot mark a stage complete."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state = sm.initial_state("empty-validation", "implementation")
            artifact = root / "specs/empty-validation/validation.md"
            artifact.parent.mkdir(parents=True)
            artifact.touch()
            errors = sm.completion_artifact_errors(
                state,
                "ai-sdlc-validation",
                "specs/empty-validation/validation.md",
                "quick",
                root,
            )
            self.assertTrue(any("metadata" in error for error in errors))

    def validation_fixture(self, root: Path) -> tuple[dict[str, object], Path, Path]:
        """Create current validation Markdown and receipt evidence."""
        subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        spec = root / "specs/receipt-demo"
        (spec / "_ai_sdlc").mkdir(parents=True)
        (spec / "requirements.md").write_text("# Requirements\n\n- AC-001: receipt is current.\n", encoding="utf-8")
        validation = spec / "validation.md"
        validation.write_text(
            '---\nartifact_metadata:\n  schema: "ai-sdlc-artifact-metadata/v1"\n  status: "validated"\n---\n# Validation\n\nCurrent command evidence covers AC-001 and passed.\n',
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "specs/receipt-demo/requirements.md"], cwd=root, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "-c", "commit.gpgsign=false", "commit", "-m", "fixture"],
            cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        receipt = spec / "_ai_sdlc/validation-receipt.json"
        plan = spec / "_ai_sdlc/validation-plan.json"
        plan.write_text('{"schema":"ai-sdlc-validation-command-plan/v1","commands":[]}\n', encoding="utf-8")
        value = {
            "schema": vr.RECEIPT_SCHEMA,
            "revision": vr.revision(root),
            "workspace_fingerprint": vr.workspace_fingerprint(root, receipt),
            "executed_at": "2026-07-21T00:00:00Z",
            "environment": {"python": "test", "platform": "test"},
            "evidence_trust": "local-structural-not-authenticated",
            "plan_path": plan.relative_to(root).as_posix(),
            "plan_sha256": hashlib.sha256(plan.read_bytes()).hexdigest(),
            "commands": [{"id": "V001", "argv": ["python3", "test.py"], "trace_ids": ["AC-001"], "exit_code": 0}],
        }
        value["receipt_fingerprint"] = vr.receipt_fingerprint(value)
        receipt.write_text(json.dumps(value), encoding="utf-8")
        return sm.initial_state("receipt-demo", "implementation"), validation, receipt

    def test_current_validation_receipt_allows_completion_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state, _, _ = self.validation_fixture(root)
            self.assertEqual(
                sm.completion_artifact_errors(
                    state, "ai-sdlc-validation", "specs/receipt-demo/validation.md", "quick", root
                ),
                [],
            )
            state_path = root / "specs/receipt-demo/_ai_sdlc/state.toon"
            sm.save_state(state_path, state)
            self.assertEqual(vr.validate_receipt(root / "specs/receipt-demo/_ai_sdlc/validation-receipt.json", root), [])

    def test_failed_forged_and_stale_validation_receipts_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state, _, receipt = self.validation_fixture(root)
            original = json.loads(receipt.read_text(encoding="utf-8"))

            failed = dict(original)
            failed["commands"] = [dict(original["commands"][0], exit_code=99)]
            failed["receipt_fingerprint"] = vr.receipt_fingerprint(failed)

            forged = dict(original)
            forged["receipt_fingerprint"] = "0" * 64

            stale = dict(original)
            stale["workspace_fingerprint"] = "0" * 64
            stale["receipt_fingerprint"] = vr.receipt_fingerprint(stale)

            for label, value in (("failed", failed), ("forged", forged), ("stale", stale)):
                with self.subTest(label=label):
                    receipt.write_text(json.dumps(value), encoding="utf-8")
                    errors = sm.completion_artifact_errors(
                        state, "ai-sdlc-validation", "specs/receipt-demo/validation.md", "quick", root
                    )
                    self.assertTrue(errors)

    def test_read_only_status_fails_when_state_is_missing(self) -> None:
        """Status must not synthesize evidence that was never persisted."""
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            result = subprocess.run(
                [sys.executable, str(CLI), "status", "--feature", "missing-state", "--workspace", "implementation"],
                cwd=temp_dir,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("authoritative state is missing", result.stderr)

    def test_implementation_starts_with_branching_before_sdd(self) -> None:
        """The executable lifecycle matches the public branch-first contract."""
        state = sm.initial_state("implementation-demo", "implementation")
        self.assertEqual(state["current_stage"], "branching")
        branching = sm.stage_row(state, "branching")
        sdd = sm.stage_row(state, "sdd")
        self.assertEqual(branching["status"], "not_started")
        self.assertIn("branching", sm.STAGE_BY_ID["sdd"].predecessors)

    def test_cli_reads_legacy_state_but_writes_canonical_state(self) -> None:
        """State mutations should migrate forward without overwriting legacy files."""
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            cwd = Path(temp_dir)
            legacy = cwd / "specs-refiniment/legacy-demo/state.toon"
            legacy.parent.mkdir(parents=True, exist_ok=True)
            legacy_text = sm.to_toon(sm.initial_state("legacy-demo", "refinement", "discovery"))
            legacy.write_text(legacy_text, encoding="utf-8")

            begin = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "begin",
                    "--feature",
                    "legacy-demo",
                    "--workspace",
                    "refinement",
                    "--skill",
                    "ai-sdlc-working-backwards-discovery",
                    "--full-flow",
                ],
                cwd=cwd,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(begin.returncode, 0, begin.stderr)
            canonical = cwd / "specs-refiniment/legacy-demo/_ai_sdlc/state.toon"
            self.assertTrue(canonical.is_file())
            self.assertIn("active_skill: ai-sdlc-working-backwards-discovery", canonical.read_text(encoding="utf-8"))
            self.assertFalse(legacy.exists())


if __name__ == "__main__":
    unittest.main()
