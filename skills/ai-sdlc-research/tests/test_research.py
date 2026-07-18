#!/usr/bin/env python3
"""Tests for the optional sourced research capability."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-research/scripts/research.py"


class ResearchTests(unittest.TestCase):
    """Citation, diversity, limitation, and routing tests."""

    def value(self) -> dict[str, object]:
        """Return valid full-flow sourced research."""
        return {"schema": "ai-sdlc-research-input/v1", "topic": "Durable retry scheduling", "scope": "mixed", "questions": [{"id": "RQ-001", "question": "Which failure modes require durable scheduling?", "trace_targets": ["DEC-022"]}], "sources": [{"id": "SRC-001", "title": "Queue service documentation", "locator": "https://docs.example/queue", "type": "official-documentation", "accessed_at": "2026-07-18", "credibility": "Primary vendor contract.", "notes": "Documents delivery guarantees."}, {"id": "SRC-002", "title": "Internal retry incident", "locator": "incidents/INC-044.md", "type": "internal-evidence", "accessed_at": "2026-07-18", "credibility": "Direct production evidence.", "notes": "Shows process restart loss."}], "findings": [{"id": "RF-001", "statement": "In-memory scheduling loses pending retries after restart.", "source_ids": ["SRC-001", "SRC-002"], "confidence": "high", "limitations": "Load behavior was not benchmarked.", "trace_targets": ["DEC-022", "NFR-004"]}], "open_questions": [{"id": "OQ-001", "question": "What queue retention meets policy?", "owner": "Architecture", "next_action": "Confirm with platform owner."}]}

    def run_research(self, root: Path, path: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run research finalization."""
        return subprocess.run(["python3", str(SCRIPT), str(root), "--input", str(path), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_full_research_writes_routed_pair(self) -> None:
        """Valid multi-source evidence should create canonical outputs."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "research.json"
            path.write_text(json.dumps(self.value()), encoding="utf-8")
            result = self.run_research(root, path, "--write", "--full-flow", "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("schema: ai-sdlc-research/v1", result.stdout)
            self.assertIn("RF-001", result.stdout)
            self.assertTrue((root / "research.md").is_file())
            self.assertTrue((root / "_ai_sdlc/research.toon").is_file())

    def test_unregistered_source_citation_is_rejected(self) -> None:
        """Findings cannot cite invented sources."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = self.value()
            value["findings"][0]["source_ids"] = ["SRC-999"]  # type: ignore[index]
            path = root / "research.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_research(root, path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("registered sources", result.stdout)

    def test_full_flow_requires_source_diversity(self) -> None:
        """Strict research must not simulate corroboration with one source type."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = self.value()
            value["sources"][1]["type"] = "official-documentation"  # type: ignore[index]
            path = root / "research.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_research(root, path, "--full-flow")
            self.assertEqual(result.returncode, 1)
            self.assertIn("at least two source types", result.stdout)

    def test_external_scope_requires_direct_web_source(self) -> None:
        """External research cannot complete from model memory or only local evidence."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = self.value()
            value["scope"] = "external"
            for source in value["sources"]:  # type: ignore[index]
                source["locator"] = "evidence/local.md"
            path = root / "research.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_research(root, path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("direct HTTP(S) source", result.stdout)


if __name__ == "__main__":
    unittest.main()
