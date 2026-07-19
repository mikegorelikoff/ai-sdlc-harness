#!/usr/bin/env python3
"""Tests for evidence identity, freshness propagation, and coverage."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py"


class EvidenceLedgerTests(unittest.TestCase):
    """Exercise fresh, stale, expired, missing, propagated, and invalid evidence."""

    def cli(self, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["python3", str(SCRIPT), str(repository), *args], cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def sha(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def setup_repository(self, repository: Path, second_feature: bool = False) -> None:
        feature = repository / "specs/payments"
        feature.mkdir(parents=True)
        (feature / "requirements.md").write_text("# Requirements\n\n- AC-001: Payments persist.\n", encoding="utf-8")
        if second_feature:
            other = repository / "specs/orders"
            other.mkdir(parents=True)
            (other / "requirements.md").write_text("# Requirements\n\n- AC-001: Orders persist.\n", encoding="utf-8")
        (repository / "evidence/artifacts").mkdir(parents=True)

    def add_manifest(self, repository: Path, record_id: str, subject: str = "AC-001", depends_on: list[str] | None = None, expires_at: str | None = None, missing: bool = False) -> Path:
        artifact = repository / f"evidence/artifacts/{record_id}.txt"
        if not missing:
            artifact.write_text(f"evidence for {record_id}\n", encoding="utf-8")
            artifact_hash = self.sha(artifact)
        else:
            artifact_hash = "0" * 64
        value = {
            "schema": "ai-sdlc-evidence-source/v1",
            "id": record_id,
            "kind": "validation",
            "subjects": [subject],
            "producer": "QA",
            "captured_at": "2026-07-18T10:00:00Z",
            "artifact": {"path": f"evidence/artifacts/{record_id}.txt", "sha256": artifact_hash},
            "dependencies": [],
            "depends_on": depends_on or [],
        }
        if expires_at:
            value["expires_at"] = expires_at
        path = repository / f"evidence/{record_id}.evidence.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_fresh_evidence_coverage_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            self.add_manifest(repository, "payment-validation")
            first = self.cli(repository, "--index", "--as-of", "2026-07-19", "--write", "--format", "json")
            second = self.cli(repository, "--index", "--as-of", "2026-07-19", "--write", "--format", "json")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            ledger = json.loads(first.stdout)
            self.assertEqual(ledger["records"][0]["status"], "fresh")
            self.assertEqual(ledger["coverage"]["requirements_with_fresh_evidence"], 1)
            self.assertEqual((repository / "_ai_sdlc/evidence-ledger.json").read_text(encoding="utf-8"), second.stdout)
            toon = (repository / "_ai_sdlc/evidence-ledger.toon").read_text(encoding="utf-8")
            self.assertIn("records[1]:", toon)
            self.assertIn("depends_on[0]:", toon)

    def test_artifact_and_dependency_drift_are_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            manifest = self.add_manifest(repository, "payment-validation")
            value = json.loads(manifest.read_text(encoding="utf-8"))
            dependency = repository / "specs/payments/requirements.md"
            value["dependencies"] = [{"path": "specs/payments/requirements.md", "sha256": self.sha(dependency)}]
            manifest.write_text(json.dumps(value), encoding="utf-8")
            dependency.write_text("# Requirements\n\n- AC-001: Payments persist durably.\n", encoding="utf-8")
            result = self.cli(repository, "--index", "--as-of", "2026-07-19", "--format", "json")
            ledger = json.loads(result.stdout)
            self.assertEqual(ledger["records"][0]["status"], "stale")
            self.assertTrue(any(reason.startswith("dependency-changed:") for reason in ledger["records"][0]["reason_codes"]))
            self.assertEqual(ledger["coverage"]["requirements_with_fresh_evidence"], 0)

    def test_missing_and_expired_evidence_are_not_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            self.add_manifest(repository, "missing-proof", missing=True)
            self.add_manifest(repository, "old-proof", expires_at="2026-07-18T23:59:59Z")
            result = self.cli(repository, "--stale", "--as-of", "2026-07-19", "--format", "json")
            stale = json.loads(result.stdout)["stale_paths"]
            self.assertEqual({item["status"] for item in stale}, {"expired", "missing"})

    def test_upstream_staleness_propagates_to_fixed_point(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            self.add_manifest(repository, "root-proof")
            self.add_manifest(repository, "middle-proof", depends_on=["root-proof"])
            self.add_manifest(repository, "final-proof", depends_on=["middle-proof"])
            (repository / "evidence/artifacts/root-proof.txt").write_text("changed evidence\n", encoding="utf-8")
            ledger = json.loads(self.cli(repository, "--index", "--as-of", "2026-07-19", "--format", "json").stdout)
            records = {record["id"]: record for record in ledger["records"]}
            self.assertEqual(records["root-proof"]["status"], "stale")
            self.assertIn("upstream-not-fresh:root-proof", records["middle-proof"]["reason_codes"])
            self.assertIn("upstream-not-fresh:middle-proof", records["final-proof"]["reason_codes"])

    def test_ambiguous_subject_unknown_dependency_and_cycle_fail_closed(self) -> None:
        with self.subTest("ambiguous"), tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository, second_feature=True)
            self.add_manifest(repository, "ambiguous-proof")
            result = self.cli(repository, "--index", "--as-of", "2026-07-19")
            self.assertEqual(result.returncode, 1)
            self.assertIn("ambiguous", result.stdout)
        with self.subTest("unknown"), tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            self.add_manifest(repository, "unknown-proof", subject="trace:payments:AC-001", depends_on=["absent"])
            result = self.cli(repository, "--index", "--as-of", "2026-07-19")
            self.assertEqual(result.returncode, 1)
            self.assertIn("unknown evidence dependency", result.stdout)
        with self.subTest("cycle"), tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            self.add_manifest(repository, "proof-a", subject="trace:payments:AC-001", depends_on=["proof-b"])
            self.add_manifest(repository, "proof-b", subject="trace:payments:AC-001", depends_on=["proof-a"])
            result = self.cli(repository, "--index", "--as-of", "2026-07-19")
            self.assertEqual(result.returncode, 1)
            self.assertIn("cycle", result.stdout)


if __name__ == "__main__":
    unittest.main()
