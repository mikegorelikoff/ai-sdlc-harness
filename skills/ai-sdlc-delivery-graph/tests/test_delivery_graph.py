#!/usr/bin/env python3
"""Tests for deterministic lifecycle indexing and graph queries."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py"


class DeliveryGraphTests(unittest.TestCase):
    """Exercise nodes, edges, paths, gaps, orphans, and deterministic writes."""

    def cli(self, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["python3", str(SCRIPT), str(repository), *args], cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def git(self, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", *args], cwd=repository, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def fixture(self, repository: Path, second_feature: bool = False) -> None:
        """Create representative lifecycle artifacts plus traceable Git data."""
        feature = repository / "specs/payments"
        feature.mkdir(parents=True)
        (feature / "requirements.md").write_text(
            "# Requirements\n\n- FR-001: Payments are accepted.\n- AC-001: Accepted payments are recorded.\n",
            encoding="utf-8",
        )
        (feature / "tasks.md").write_text(
            "# Tasks\n\n- [x] T001. Store accepted payments.\n  Refs: AC-001\n",
            encoding="utf-8",
        )
        (feature / "test-cases.md").write_text(
            "# Tests\n\n- TC-001 / AC-001: accepted payment persists.\n",
            encoding="utf-8",
        )
        (feature / "design.md").write_text(
            "# Design\n\nComponent: `src/payments.py` -> T001\nEvidence: `evidence/payment.json` -> TC-001\n",
            encoding="utf-8",
        )
        (feature / "decision-log.md").write_text("# Decisions\n\n| DEC-001 | Retry provider later |\n", encoding="utf-8")
        if second_feature:
            other = repository / "specs/orders"
            other.mkdir(parents=True)
            (other / "requirements.md").write_text("# Requirements\n\n- AC-001: Orders are durable.\n", encoding="utf-8")
        self.git(repository, "init", "-q")
        self.git(repository, "config", "user.email", "test@example.com")
        self.git(repository, "config", "user.name", "Test")
        self.git(repository, "add", ".")
        self.git(repository, "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "feat(payments): store accepted payment\n\nSpec: specs/payments\nTask: T001")
        self.git(repository, "tag", "v1.0.0")

    def test_index_is_deterministic_and_writes_versioned_graph(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.fixture(repository)
            first = self.cli(repository, "--index", "--write", "--format", "json")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            second = self.cli(repository, "--index", "--write", "--format", "json")
            self.assertEqual(first.stdout, second.stdout)
            graph = json.loads(first.stdout)
            self.assertEqual(graph["schema"], "ai-sdlc-delivery-graph/v1")
            self.assertEqual(graph["coverage"]["requirement_declarations"], 2)
            self.assertEqual(graph["coverage"]["acceptance_criteria_with_tasks"], 1)
            self.assertEqual(graph["coverage"]["acceptance_criteria_with_tests"], 1)
            self.assertIn("trace:payments:DEC-001", graph["orphans"])
            self.assertEqual((repository / "_ai_sdlc/delivery-graph.json").read_text(encoding="utf-8"), second.stdout)
            self.assertTrue((repository / "_ai_sdlc/delivery-graph.md").is_file())
            toon = (repository / "_ai_sdlc/delivery-graph.toon").read_text(encoding="utf-8")
            self.assertIn("nodes[", toon)
            self.assertIn("edges[", toon)

    def test_end_to_end_requirement_commit_and_release_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.fixture(repository)
            commit_query = self.cli(repository, "--trace", "AC-001", "--to", "T001", "--format", "json")
            self.assertEqual(commit_query.returncode, 0, commit_query.stdout + commit_query.stderr)
            path = json.loads(commit_query.stdout)
            self.assertEqual([node["key"] for node in path["nodes"]], ["AC-001", "T001"])
            reachable = json.loads(self.cli(repository, "--trace", "AC-001", "--format", "json").stdout)
            self.assertTrue(any(node.startswith("commit:") for node in reachable["reachable"]))
            self.assertTrue(any(node.startswith("release:") for node in reachable["reachable"]))

    def test_gap_and_orphan_queries_report_missing_semantic_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.fixture(repository)
            requirements = repository / "specs/payments/requirements.md"
            requirements.write_text(requirements.read_text(encoding="utf-8") + "- AC-002: Declined payments are explained.\n", encoding="utf-8")
            gaps = json.loads(self.cli(repository, "--gaps", "--format", "json").stdout)
            self.assertIn({"code": "acceptance-criterion-without-task", "node": "trace:payments:AC-002"}, gaps["gaps"])
            self.assertNotIn({"code": "acceptance-criterion-without-task", "node": "trace:payments:FR-001"}, gaps["gaps"])
            orphans = json.loads(self.cli(repository, "--orphans", "--format", "json").stdout)
            self.assertIn("trace:payments:FR-001", orphans["orphans"])
            self.assertIn("trace:payments:DEC-001", orphans["orphans"])

    def test_generated_workspace_index_does_not_create_repository_trace_nodes(self) -> None:
        """Generated human indexes must not be treated as authoritative features."""
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.fixture(repository)
            (repository / "specs/specs-index.md").write_text(
                "# Generated index\n\nAC-777 TC-777 T777\n", encoding="utf-8"
            )
            graph = json.loads(self.cli(repository, "--index", "--format", "json").stdout)
            self.assertFalse(any(node["id"].startswith("trace:repository:") for node in graph["nodes"]))
            self.assertFalse(any(node["id"] == "artifact:specs/specs-index.md" for node in graph["nodes"]))

    def test_ambiguous_short_id_requires_scoped_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.fixture(repository, second_feature=True)
            result = self.cli(repository, "--trace", "AC-001", "--format", "json")
            self.assertEqual(result.returncode, 1)
            self.assertIn("ambiguous", result.stdout)
            scoped = self.cli(repository, "--trace", "trace:payments:AC-001", "--to", "T001", "--format", "json")
            self.assertEqual(scoped.returncode, 0, scoped.stdout + scoped.stderr)

    def test_missing_trace_and_invalid_to_fail_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.fixture(repository)
            missing = self.cli(repository, "--trace", "AC-999", "--format", "json")
            self.assertEqual(missing.returncode, 1)
            self.assertIn("not found", missing.stdout)
            invalid = self.cli(repository, "--gaps", "--to", "T001")
            self.assertEqual(invalid.returncode, 1)
            self.assertFalse((repository / "_ai_sdlc").exists())


if __name__ == "__main__":
    unittest.main()
