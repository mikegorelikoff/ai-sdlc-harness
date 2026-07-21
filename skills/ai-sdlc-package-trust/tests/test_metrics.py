#!/usr/bin/env python3
"""Tests for content-free local metrics."""
from __future__ import annotations
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-package-trust/scripts/metrics.py"
class MetricsTests(unittest.TestCase):
    def cli(self, repository: Path, *args: str) -> subprocess.CompletedProcess[str]: return subprocess.run(["python3", str(SCRIPT), str(repository), "--generate", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    def test_empty_metrics_are_explicit_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp); first = self.cli(repository, "--format", "json"); second = self.cli(repository, "--format", "json")
            self.assertEqual(first.stdout, second.stdout); self.assertEqual(json.loads(first.stdout)["status"], "insufficient-data")
    def test_aggregates_runs_and_evidence_without_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp); run = repository / "_ai_sdlc/runs/run-secret"; run.mkdir(parents=True)
            state = {"schema":"ai-sdlc-run-state/v1","status":"completed","budgets":{"used_steps":2,"used_failures":1,"used_tokens":55},"tasks":[{"status":"succeeded","attempts":2},{"status":"succeeded","attempts":1}],"fingerprint":"a"*64,"secret_payload":"DO-NOT-COLLECT"}
            (run / "state.json").write_text(json.dumps(state), encoding="utf-8")
            ledger = {"schema":"ai-sdlc-evidence-ledger/v1","fingerprint":"b"*64,"coverage":{"requirements":3,"requirements_with_fresh_evidence":2,"evidence_records":2,"fresh_records":1},"records":[{"status":"fresh","content":"SECRET"},{"status":"stale","content":"SECRET2"}]}
            ledger_path = repository / "_ai_sdlc/evidence-ledger.json"; ledger_path.parent.mkdir(exist_ok=True); ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
            result = self.cli(repository, "--write", "--format", "json"); self.assertEqual(result.returncode, 0, result.stdout + result.stderr); value = json.loads(result.stdout)
            self.assertEqual(value["runs"]["completed"], 1); self.assertEqual(value["tasks"]["retries"], 1); self.assertEqual(value["quality"]["stale_records"], 1); self.assertNotIn("SECRET", result.stdout); self.assertNotIn("DO-NOT-COLLECT", result.stdout)
            self.assertTrue((repository / "_ai_sdlc/metrics/local.toon").is_file())
    def test_write_rejects_symlinked_repository_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp); repository = parent / "repo"; outside = parent / "outside"
            repository.mkdir(); outside.mkdir(); (repository / "_ai_sdlc").symlink_to(outside, target_is_directory=True)
            result = self.cli(repository, "--write", "--format", "json")
            self.assertEqual(result.returncode, 1)
            self.assertIn("symlink", result.stdout)
            self.assertFalse((outside / "metrics/local.json").exists())
if __name__ == "__main__": unittest.main()
