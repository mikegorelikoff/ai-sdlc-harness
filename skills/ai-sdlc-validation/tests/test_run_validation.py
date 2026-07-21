#!/usr/bin/env python3
"""Tests for executed validation receipts and stale/failure rejection."""

from __future__ import annotations

import json
import hashlib
import subprocess
import tempfile
import unittest
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-validation/scripts/run_validation.py"


class ValidationReceiptTests(unittest.TestCase):
    def cli(self, repository: Path, plan: Path, output: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), "--root", str(repository), "--plan", str(plan),
             "--output", str(output), *extra], check=False, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def fixture(self, repository: Path, exit_code: int) -> tuple[Path, Path]:
        subprocess.run(["git", "init"], cwd=repository, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        (repository / "tracked.txt").write_text("current\n", encoding="utf-8")
        script = repository / "validation_check.py"
        script.write_text(f"raise SystemExit({exit_code})\n", encoding="utf-8")
        spec = repository / "specs/demo"
        spec.mkdir(parents=True)
        (spec / "test-cases.md").write_text("# Tests\n\n- TC-001: validation fixture.\n", encoding="utf-8")
        subprocess.run(["git", "add", "tracked.txt", "validation_check.py", "specs/demo/test-cases.md"], cwd=repository, check=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "-c", "commit.gpgsign=false", "commit", "-m", "fixture"], cwd=repository, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        plan = spec / "_ai_sdlc/validation-plan.json"
        plan.parent.mkdir(parents=True, exist_ok=True)
        plan.write_text(json.dumps({"schema": "ai-sdlc-validation-command-plan/v1", "commands": [{"id": "V001", "argv": ["python3", "validation_check.py"], "trace_ids": ["TC-001"]}]}), encoding="utf-8")
        return plan, repository / "specs/demo/_ai_sdlc/validation-receipt.json"

    def test_success_is_current_then_source_change_makes_receipt_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan, output = self.fixture(repository, 0)
            created = self.cli(repository, plan, output)
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            verified = self.cli(repository, plan, output, "--verify")
            self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)
            (repository / "tracked.txt").write_text("changed\n", encoding="utf-8")
            stale = self.cli(repository, plan, output, "--verify")
            self.assertEqual(stale.returncode, 1)
            self.assertIn("workspace fingerprint is stale", stale.stdout)

    def test_derived_state_and_review_evidence_do_not_stale_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan, output = self.fixture(repository, 0)
            validation = repository / "specs/demo/validation.md"
            validation.write_text("# Validation\n\nFinalized before execution.\n", encoding="utf-8")
            self.assertEqual(self.cli(repository, plan, output).returncode, 0)
            (repository / "specs/demo/_ai_sdlc/state.toon").write_text("current_stage: validation\n", encoding="utf-8")
            (repository / "specs/demo/code-review.md").write_text("# Review\n\nNo findings.\n", encoding="utf-8")
            verified = self.cli(repository, plan, output, "--verify")
            self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)

    def test_nonzero_command_is_recorded_and_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan, output = self.fixture(repository, 99)
            created = self.cli(repository, plan, output)
            self.assertEqual(created.returncode, 1)
            receipt = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(receipt["commands"][0]["exit_code"], 99)
            verified = self.cli(repository, plan, output, "--verify")
            self.assertEqual(verified.returncode, 1)
            self.assertIn("exit=99", verified.stdout)

    def test_dangerous_command_forms_are_rejected_without_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            subprocess.run(["git", "init"], cwd=repository, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            output = repository / "receipt.json"
            for index, argv in enumerate((
                ["python3", "-c", "open('owned','w').write('x')"],
                ["/tmp/evil/python3", "safe.py"],
                ["git", "reset", "--hard"],
                ["npx", "unreviewed-package"],
                ["make", "dangerous-target"],
            )):
                with self.subTest(argv=argv):
                    plan = repository / f"plan-{index}.json"
                    plan.write_text(json.dumps({"schema": "ai-sdlc-validation-command-plan/v1", "commands": [{"id": "V001", "argv": argv, "trace_ids": []}]}), encoding="utf-8")
                    result = self.cli(repository, plan, output)
                    self.assertEqual(result.returncode, 1)
            self.assertFalse((repository / "owned").exists())
            self.assertFalse(output.exists())

    def test_non_git_root_fails_closed_without_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            script = repository / "validation_check.py"
            script.write_text("raise SystemExit(0)\n", encoding="utf-8")
            spec = repository / "specs/demo"
            (spec / "_ai_sdlc").mkdir(parents=True)
            (spec / "test-cases.md").write_text("- TC-001: check\n", encoding="utf-8")
            plan = spec / "_ai_sdlc/validation-plan.json"
            plan.write_text(json.dumps({"schema": "ai-sdlc-validation-command-plan/v1", "commands": [{"id": "V001", "argv": ["python3", "validation_check.py"], "trace_ids": ["TC-001"]}]}), encoding="utf-8")
            output = spec / "_ai_sdlc/validation-receipt.json"
            result = self.cli(repository, plan, output)
            self.assertEqual(result.returncode, 1)
            self.assertIn("valid HEAD", result.stdout)
            self.assertFalse(output.exists())

    def test_plan_change_invalidates_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan, output = self.fixture(repository, 0)
            self.assertEqual(self.cli(repository, plan, output).returncode, 0)
            value = json.loads(plan.read_text(encoding="utf-8"))
            value["commands"][0]["id"] = "V002"
            plan.write_text(json.dumps(value), encoding="utf-8")
            result = self.cli(repository, plan, output, "--verify")
            self.assertEqual(result.returncode, 1)
            self.assertIn("plan digest mismatch", result.stdout)

    def test_output_limit_terminates_noisy_process(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan, output = self.fixture(repository, 0)
            (repository / "validation_check.py").write_text("print('x' * 1000000)\n", encoding="utf-8")
            result = self.cli(repository, plan, output, "--max-output-bytes", "1024")
            self.assertEqual(result.returncode, 1)
            receipt = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(receipt["commands"][0]["exit_code"], 125)
            self.assertTrue(receipt["commands"][0]["output_limited"])

    def test_untracked_symlink_and_oversized_file_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            repository = parent / "repo"
            repository.mkdir()
            plan, output = self.fixture(repository, 0)
            outside = parent / "outside.txt"
            outside.write_text("external", encoding="utf-8")
            (repository / "outside-link").symlink_to(outside)
            linked = self.cli(repository, plan, output)
            self.assertEqual(linked.returncode, 1)
            self.assertIn("untracked symlink", linked.stdout)
            (repository / "outside-link").unlink()
            (repository / "large.bin").write_bytes(b"x" * 20_000_001)
            oversized = self.cli(repository, plan, output)
            self.assertEqual(oversized.returncode, 1)
            self.assertIn("exceeds 20000000 bytes", oversized.stdout)

    def test_timeout_terminates_descendant_process_group(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan, output = self.fixture(repository, 0)
            (repository / "validation_check.py").write_text(
                "import subprocess, sys, time\n"
                "subprocess.Popen([sys.executable, '-c', \"import time, pathlib; time.sleep(1.5); pathlib.Path('escaped').write_text('x')\"])\n"
                "time.sleep(10)\n",
                encoding="utf-8",
            )
            result = self.cli(repository, plan, output, "--timeout", "1")
            self.assertEqual(result.returncode, 1)
            receipt = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(receipt["commands"][0]["exit_code"], 124)
            time.sleep(1)
            self.assertFalse((repository / "escaped").exists())

    def test_receipt_discloses_that_local_fingerprint_is_not_authentication(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan, output = self.fixture(repository, 0)
            self.assertEqual(self.cli(repository, plan, output).returncode, 0)
            receipt = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(receipt["evidence_trust"], "local-structural-not-authenticated")
            receipt["executed_at"] = "forged-by-workspace-writer"
            body = {key: value for key, value in receipt.items() if key != "receipt_fingerprint"}
            receipt["receipt_fingerprint"] = hashlib.sha256(
                json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
            ).hexdigest()
            output.write_text(json.dumps(receipt), encoding="utf-8")
            forged = self.cli(repository, plan, output, "--verify")
            self.assertEqual(forged.returncode, 0, forged.stdout + forged.stderr)

    def test_trace_ids_must_be_nonempty_and_declared_in_spec(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan, output = self.fixture(repository, 0)
            value = json.loads(plan.read_text(encoding="utf-8"))
            value["commands"][0]["trace_ids"] = []
            plan.write_text(json.dumps(value), encoding="utf-8")
            empty = self.cli(repository, plan, output)
            self.assertEqual(empty.returncode, 1)
            value["commands"][0]["trace_ids"] = ["TC-999"]
            plan.write_text(json.dumps(value), encoding="utf-8")
            unknown = self.cli(repository, plan, output)
            self.assertEqual(unknown.returncode, 1)
            self.assertIn("not declared", unknown.stdout)
            self.assertFalse(output.exists())

    def test_runner_rejects_premature_state_completion(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan, output = self.fixture(repository, 0)
            result = self.cli(
                repository,
                plan,
                output,
                "--complete-state",
                "--feature",
                "demo",
                "--quick-flow",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("cannot complete lifecycle state while it is still executing", result.stdout)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
