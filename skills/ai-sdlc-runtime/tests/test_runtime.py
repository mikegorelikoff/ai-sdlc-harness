#!/usr/bin/env python3
"""Tests for resumable journaled runtime state transitions."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-runtime/scripts/runtime.py"
HASH_A = "a" * 64
HASH_B = "b" * 64


class RuntimeTests(unittest.TestCase):
    """Exercise readiness, idempotency, retries, budgets, commits, and recovery."""

    def cli(self, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["python3", str(SCRIPT), str(repository), *args, "--format", "json"], cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def plan(self, repository: Path, *, attempts: int = 2, steps: int = 10, failures: int = 5, tokens: int = 1000, two_tasks: bool = True, commit_boundary: bool = True) -> Path:
        tasks = [{"id": "T001", "depends_on": [], "action": "implement", "input_fingerprint": HASH_A, "max_attempts": attempts, "commit_boundary": commit_boundary}]
        if two_tasks:
            tasks.append({"id": "T002", "depends_on": ["T001"], "action": "validate", "input_fingerprint": HASH_B, "max_attempts": 1, "commit_boundary": False})
        value = {"schema": "ai-sdlc-run-plan/v1", "id": "fixture", "version": "1.0.0", "budgets": {"max_steps": steps, "max_failures": failures, "max_tokens": tokens}, "tasks": tasks}
        path = repository / "plan.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def start(self, repository: Path, plan: Path) -> dict[str, object]:
        result = self.cli(repository, "--start", "--run-id", "run-1", "--plan", str(plan))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_dependency_readiness_and_completion(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository))
            first = json.loads(self.cli(repository, "--next", "--run-id", "run-1").stdout)
            self.assertEqual(first["state"]["running_task"], "T001")
            self.assertNotIn("T002", first["state"]["ready_tasks"])
            self.assertIn("running_task: T001", (repository / "_ai_sdlc/runs/run-1/state.toon").read_text(encoding="utf-8"))
            success = json.loads(self.cli(repository, "--record", "--run-id", "run-1", "--task", "T001", "--outcome", "succeeded", "--result-fingerprint", HASH_A, "--tokens", "10", "--commit", "abcdef1").stdout)
            self.assertEqual(success["state"]["ready_tasks"], ["T002"])
            self.cli(repository, "--next", "--run-id", "run-1")
            completed = json.loads(self.cli(repository, "--record", "--run-id", "run-1", "--task", "T002", "--outcome", "succeeded", "--result-fingerprint", HASH_B, "--tokens", "5").stdout)
            self.assertEqual(completed["state"]["status"], "completed")
            self.assertEqual(completed["state"]["stop_reason"], "all-tasks-succeeded")

    def test_next_and_success_record_are_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, two_tasks=False))
            first = json.loads(self.cli(repository, "--next", "--run-id", "run-1").stdout)
            second = json.loads(self.cli(repository, "--next", "--run-id", "run-1").stdout)
            self.assertTrue(second["idempotent"])
            self.assertEqual(first["state"]["sequence"], second["state"]["sequence"])
            args = ("--record", "--run-id", "run-1", "--task", "T001", "--outcome", "succeeded", "--result-fingerprint", HASH_A, "--tokens", "10", "--commit", "abcdef1")
            recorded = json.loads(self.cli(repository, *args).stdout)
            repeated = json.loads(self.cli(repository, *args).stdout)
            self.assertTrue(repeated["idempotent"])
            self.assertEqual(recorded["state"]["sequence"], repeated["state"]["sequence"])

    def test_retry_exhaustion_and_blocked_retry_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, attempts=2, two_tasks=False))
            self.cli(repository, "--next", "--run-id", "run-1")
            first = json.loads(self.cli(repository, "--record", "--run-id", "run-1", "--task", "T001", "--outcome", "failed", "--tokens", "1", "--reason", "test failed").stdout)
            self.assertEqual(first["state"]["status"], "running")
            self.cli(repository, "--next", "--run-id", "run-1")
            second = json.loads(self.cli(repository, "--record", "--run-id", "run-1", "--task", "T001", "--outcome", "failed", "--tokens", "1", "--reason", "test failed again").stdout)
            self.assertEqual(second["state"]["stop_reason"], "retry-exhausted:T001")
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, attempts=2, two_tasks=False))
            self.cli(repository, "--next", "--run-id", "run-1")
            blocked = json.loads(self.cli(repository, "--record", "--run-id", "run-1", "--task", "T001", "--outcome", "blocked", "--reason", "owner input", "--tokens", "0").stdout)
            self.assertEqual(blocked["state"]["status"], "paused")
            retry = json.loads(self.cli(repository, "--retry", "T001", "--run-id", "run-1", "--reason", "owner replied").stdout)
            self.assertEqual(retry["state"]["status"], "running")
            self.assertEqual(retry["state"]["ready_tasks"], ["T001"])

    def test_step_failure_and_token_budgets_have_distinct_stops(self) -> None:
        cases = (({"steps": 1}, "step-budget-exhausted"), ({"failures": 1}, "failure-budget-exhausted"), ({"tokens": 10}, "token-budget-exhausted"))
        for overrides, expected in cases:
            with self.subTest(expected), tempfile.TemporaryDirectory() as temp:
                repository = Path(temp)
                self.start(repository, self.plan(repository, **overrides))
                self.cli(repository, "--next", "--run-id", "run-1")
                if expected == "failure-budget-exhausted":
                    result = json.loads(self.cli(repository, "--record", "--run-id", "run-1", "--task", "T001", "--outcome", "failed", "--tokens", "1", "--reason", "failure").stdout)
                else:
                    result = json.loads(self.cli(repository, "--record", "--run-id", "run-1", "--task", "T001", "--outcome", "succeeded", "--result-fingerprint", HASH_A, "--tokens", "10", "--commit", "abcdef1").stdout)
                    if expected == "step-budget-exhausted":
                        result = json.loads(self.cli(repository, "--next", "--run-id", "run-1").stdout)
                self.assertEqual(result["state"]["stop_reason"], expected)

    def test_commit_boundary_rejects_missing_evidence_without_journal_event(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, two_tasks=False))
            self.cli(repository, "--next", "--run-id", "run-1")
            rejected = self.cli(repository, "--record", "--run-id", "run-1", "--task", "T001", "--outcome", "succeeded", "--result-fingerprint", HASH_A, "--tokens", "2")
            self.assertEqual(rejected.returncode, 1)
            self.assertIn("commit evidence", rejected.stdout)
            status = json.loads(self.cli(repository, "--status", "--run-id", "run-1").stdout)
            self.assertEqual(status["state"]["sequence"], 2)
            self.assertEqual(status["state"]["running_task"], "T001")

    def test_resume_repairs_state_from_valid_journal(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, two_tasks=False))
            self.cli(repository, "--next", "--run-id", "run-1")
            state_path = repository / "_ai_sdlc/runs/run-1/state.json"
            state_path.write_text('{"corrupt": true}\n', encoding="utf-8")
            toon_path = repository / "_ai_sdlc/runs/run-1/state.toon"
            toon_path.write_text("corrupt\n", encoding="utf-8")
            resumed = json.loads(self.cli(repository, "--resume", "--run-id", "run-1").stdout)
            self.assertTrue(resumed["recovered"])
            self.assertEqual(resumed["state"]["running_task"], "T001")
            self.assertEqual(json.loads(state_path.read_text(encoding="utf-8"))["fingerprint"], resumed["state"]["fingerprint"])
            self.assertIn(resumed["state"]["fingerprint"], toon_path.read_text(encoding="utf-8"))

    def test_corrupt_journal_and_duplicate_start_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan = self.plan(repository, two_tasks=False)
            self.start(repository, plan)
            duplicate = self.cli(repository, "--start", "--run-id", "run-1", "--plan", str(plan))
            self.assertEqual(duplicate.returncode, 1)
            journal = repository / "_ai_sdlc/runs/run-1/journal.jsonl"
            event = json.loads(journal.read_text(encoding="utf-8").splitlines()[0])
            event["payload"]["run_id"] = "tampered"
            journal.write_text(json.dumps(event) + "\n", encoding="utf-8")
            resumed = self.cli(repository, "--resume", "--run-id", "run-1")
            self.assertEqual(resumed.returncode, 1)
            self.assertIn("hash chain", resumed.stdout)

    def test_symlinked_runtime_parent_cannot_escape_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            repository = Path(temp)
            (repository / "_ai_sdlc").symlink_to(Path(outside), target_is_directory=True)
            plan = self.plan(repository, two_tasks=False)
            result = self.cli(repository, "--start", "--run-id", "run-1", "--plan", str(plan))
            self.assertEqual(result.returncode, 1)
            self.assertIn("symlink", result.stdout)
            self.assertFalse((Path(outside) / "runs/run-1/state.json").exists())

    def test_result_discloses_local_unauthenticated_trust(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            started = self.start(repository, self.plan(repository, two_tasks=False))
            self.assertEqual(started["evidence_trust"], "local-structural-not-authenticated")


if __name__ == "__main__":
    unittest.main()
