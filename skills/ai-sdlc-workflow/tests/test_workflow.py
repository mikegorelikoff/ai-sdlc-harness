#!/usr/bin/env python3
"""Tests for declarative workflow validation and safe wave planning."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-workflow/scripts/workflow.py"


class WorkflowTests(unittest.TestCase):
    def step(self, step_id: str, dependencies: list[str], step_type: str = "task", isolation: str = "workspace", condition: object = None) -> dict[str, object]:
        return {"id": step_id, "type": step_type, "depends_on": dependencies, "action": f"delivery.{step_id}", "capabilities": ["filesystem.read"], "condition": condition, "isolation": isolation, "approval_owner": "Delivery" if step_type == "approval" else ""}

    def value(self) -> dict[str, object]:
        return {
            "schema": "ai-sdlc-workflow/v1", "id": "ship-feature", "version": "1.0.0", "capabilities": ["filesystem.read"],
            "steps": [self.step("prepare", []), self.step("build-a", ["prepare"]), self.step("build-b", ["prepare"]), self.step("approve", ["build-a", "build-b"], "approval", "none")],
            "hooks": [{"id": "record-result", "phase": "after", "target": "build-a", "action": "evidence.record", "capabilities": ["filesystem.read"]}],
        }

    def cli(self, repository: Path, value: dict[str, object], *args: str) -> subprocess.CompletedProcess[str]:
        path = repository / "workflow.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return subprocess.run(["python3", str(SCRIPT), str(repository), "--workflow", str(path), *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

    def test_parallel_wave_gates_hooks_and_toon_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            result = self.cli(repository, self.value(), "--plan", "--concurrency", "4", "--isolation-supported", "--write", "--format", "json")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            plan = json.loads(result.stdout)
            self.assertEqual([wave["steps"] for wave in plan["waves"]], [["prepare"], ["build-a", "build-b"], ["approve"]])
            self.assertEqual(plan["waves"][1]["mode"], "parallel")
            self.assertEqual(plan["gates"][0]["owner"], "Delivery")
            self.assertEqual(plan["hooks"][0]["id"], "record-result")
            toon = repository / "_ai_sdlc/workflows/ship-feature/plan.toon"
            self.assertTrue(toon.is_file())
            self.assertIn("step_decisions[4]", toon.read_text(encoding="utf-8"))

    def test_sequential_fallback_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            first = self.cli(repository, self.value(), "--plan", "--format", "json")
            second = self.cli(repository, self.value(), "--plan", "--format", "json")
            self.assertEqual(first.stdout, second.stdout)
            plan = json.loads(first.stdout)
            self.assertIn("host-concurrency-unavailable", [item["reason"] for item in plan["fallbacks"]])
            self.assertFalse(any(wave["mode"] == "parallel" for wave in plan["waves"]))

    def test_conditions_match_skip_and_defer(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            value = self.value()
            value["steps"][0]["condition"] = {"field": "release.enabled", "operator": "eq", "value": True}
            deferred = self.cli(repository, value, "--plan", "--format", "json")
            self.assertEqual(deferred.returncode, 2)
            self.assertFalse(json.loads(deferred.stdout)["executable"])
            context = repository / "context.json"
            context.write_text(json.dumps({"release": {"enabled": False}}), encoding="utf-8")
            skipped = self.cli(repository, value, "--plan", "--context", str(context), "--format", "json")
            self.assertEqual(skipped.returncode, 0)
            self.assertEqual(json.loads(skipped.stdout)["step_decisions"][0]["status"], "skipped")

    def test_cycles_and_undeclared_capabilities_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            cyclic = self.value()
            cyclic["steps"][0]["depends_on"] = ["approve"]
            result = self.cli(repository, cyclic, "--validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("dependency cycle", result.stdout)
            undeclared = self.value()
            undeclared["hooks"][0]["capabilities"] = ["network.access"]
            result = self.cli(repository, undeclared, "--validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("undeclared capabilities", result.stdout)


if __name__ == "__main__":
    unittest.main()
