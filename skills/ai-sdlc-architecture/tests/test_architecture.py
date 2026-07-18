#!/usr/bin/env python3
"""Tests for the optional architecture capability."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-architecture/scripts/architecture.py"


class ArchitectureTests(unittest.TestCase):
    """Traceability, strict coverage, and routing tests."""

    def value(self) -> dict[str, object]:
        """Return a valid full-flow architecture input."""
        return {"schema": "ai-sdlc-architecture-input/v1", "context": "Introduce a bounded retry coordinator.", "constraints": [{"id": "ARC-C01", "statement": "No synchronous dependency on billing.", "trace_targets": ["NFR-004"]}], "components": [{"name": "retry-coordinator", "responsibility": "Schedule bounded retries.", "dependencies": ["queue"]}], "interfaces": [{"name": "retry-command", "from": "api", "to": "retry-coordinator", "contract": "Idempotent command.", "trace_targets": ["AC-007"]}], "decisions": [{"id": "DEC-021", "statement": "Use durable queue scheduling.", "rationale": "Survives process restarts.", "alternatives": ["in-memory timers"], "consequences": ["queue operations required"], "trace_targets": ["AC-007", "NFR-004"]}], "risks": [{"id": "RISK-009", "statement": "Duplicate delivery.", "mitigation": "Idempotency key.", "owner": "Dev", "trace_targets": ["TC-020"]}], "validation": [{"check": "Restart recovery integration test", "evidence": "TC-020", "status": "planned"}]}

    def run_arch(self, root: Path, input_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run architecture finalization."""
        return subprocess.run(["python3", str(SCRIPT), str(root), "--input", str(input_path), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_full_architecture_writes_routed_pair(self) -> None:
        """Valid design should write human and machine artifacts."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_path = root / "input.json"
            input_path.write_text(json.dumps(self.value()), encoding="utf-8")
            result = self.run_arch(root, input_path, "--write", "--full-flow", "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("schema: ai-sdlc-architecture/v1", result.stdout)
            self.assertIn("DEC-021", result.stdout)
            self.assertTrue((root / "architecture.md").is_file())
            self.assertTrue((root / "_ai_sdlc/architecture.toon").is_file())

    def test_decision_requires_alternatives_and_consequences(self) -> None:
        """Architecture decisions must expose tradeoffs."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = self.value()
            value["decisions"][0]["alternatives"] = []  # type: ignore[index]
            path = root / "input.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_arch(root, path, "--full-flow")
            self.assertEqual(result.returncode, 1)
            self.assertIn("alternatives must be non-empty", result.stdout)

    def test_full_flow_requires_risk_and_validation(self) -> None:
        """Strict design cannot omit operational challenge and proof."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = self.value()
            value["risks"], value["validation"] = [], []
            path = root / "input.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_arch(root, path, "--full-flow")
            self.assertEqual(result.returncode, 1)
            self.assertIn("full flow requires at least one risks entry", result.stdout)
            self.assertIn("full flow requires at least one validation entry", result.stdout)


if __name__ == "__main__":
    unittest.main()
