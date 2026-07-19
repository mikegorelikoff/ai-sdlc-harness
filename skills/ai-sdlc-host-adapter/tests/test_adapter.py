#!/usr/bin/env python3
"""Tests for host adapter validation and capability negotiation."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills/ai-sdlc-host-adapter"
SCRIPT = SKILL / "scripts/adapter.py"
FIXTURES = SKILL / "references/fixtures"


class AdapterTests(unittest.TestCase):
    def request(self, repository: Path, operations: list[str], capabilities: list[str], concurrency: int = 4, isolation: bool = True) -> Path:
        path = repository / "request.json"
        path.write_text(json.dumps({"schema": "ai-sdlc-capability-request/v1", "operations": operations, "capabilities": capabilities, "concurrency": concurrency, "isolation_required": isolation}), encoding="utf-8")
        return path

    def cli(self, repository: Path, adapter: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["python3", str(SCRIPT), str(repository), "--adapter", str(FIXTURES / adapter), *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

    def test_full_host_maps_native_and_writes_complete_toon(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            request = self.request(repository, ["task.execute", "task.parallel", "hook.lifecycle", "approval.request"], ["filesystem.read"])
            result = self.cli(repository, "full-host.json", "--negotiate", "--request", str(request), "--write", "--format", "json")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            value = json.loads(result.stdout)
            self.assertTrue(value["compatible"])
            self.assertTrue(all(item["mode"] == "native" for item in value["mappings"]))
            self.assertEqual(value["limits"]["effective_concurrency"], 4)
            toon = repository / "_ai_sdlc/adapters/full-host/negotiation.toon"
            self.assertIn("mappings[4]", toon.read_text(encoding="utf-8"))

    def test_sequential_host_uses_registered_fallbacks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            request = self.request(repository, ["task.parallel", "hook.lifecycle", "approval.request"], ["filesystem.read"], 8, True)
            first = self.cli(repository, "sequential-host.json", "--negotiate", "--request", str(request), "--format", "json")
            second = self.cli(repository, "sequential-host.json", "--negotiate", "--request", str(request), "--format", "json")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            value = json.loads(first.stdout)
            self.assertTrue(value["compatible"])
            self.assertEqual(value["limits"]["effective_concurrency"], 1)
            self.assertEqual({item["strategy"] for item in value["mappings"]}, {"sequential-wave", "explicit-hook-step", "manual-approval-gate"})
            self.assertIn("sequential-isolation-fallback", [item["reason"] for item in value["fallbacks"]])

    def test_read_only_host_fails_missing_requirements(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            request = self.request(repository, ["task.execute"], ["network.access"], 1, False)
            result = self.cli(repository, "read-only-host.json", "--negotiate", "--request", str(request), "--format", "json")
            self.assertEqual(result.returncode, 2)
            value = json.loads(result.stdout)
            self.assertFalse(value["compatible"])
            self.assertEqual(value["unsupported_operations"], ["task.execute"])
            self.assertEqual(value["missing_capabilities"], ["network.access"])

    def test_invalid_semantics_and_duplicate_mapping_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            value = json.loads((FIXTURES / "full-host.json").read_text(encoding="utf-8"))
            value["operations"][0]["semantics"] = "approximate"
            value["operations"].append(dict(value["operations"][1]))
            path = repository / "invalid.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            result = subprocess.run(["python3", str(SCRIPT), str(repository), "--adapter", str(path), "--validate"], cwd=ROOT, text=True, stdout=subprocess.PIPE, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("semantics must be equivalent", result.stdout)
            self.assertIn("mappings must be unique", result.stdout)


if __name__ == "__main__":
    unittest.main()
