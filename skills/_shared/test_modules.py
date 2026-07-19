#!/usr/bin/env python3
"""Tests for optional module discovery and compatibility."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/_shared/ai_sdlc_modules.py"


def module(root: Path, module_id: str, kind: str, skill: str, api_min: str = "1.0.0", api_max: str = "2.0.0", requires: list[str] | None = None) -> None:
    """Write one module and its skill fixture."""
    skill_path = root / "skills" / skill
    skill_path.mkdir(parents=True, exist_ok=True)
    (skill_path / "SKILL.md").write_text(f"---\nname: {skill}\ndescription: fixture\n---\n", encoding="utf-8")
    manifest = root / "modules" / module_id / "module.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({"schema": "ai-sdlc-module/v1", "id": module_id, "version": "1.0.0", "kind": kind, "harness_api": {"min": api_min, "max_exclusive": api_max}, "requires": requires or [], "description": "fixture", "skills": [{"name": skill, "path": f"skills/{skill}"}]}), encoding="utf-8")


class ModuleTests(unittest.TestCase):
    """Manifest validation, compatibility, and optionality tests."""

    def run_modules(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run discovery with captured output."""
        return subprocess.run(["python3", str(SCRIPT), "--root", str(root), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_repo_core_manifest_is_valid(self) -> None:
        """The shipped core registry should discover every listed skill."""
        result = self.run_modules(ROOT, "--format", "toon")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("core,1.8.0,core,yes,yes", result.stdout)
        self.assertIn("ai-sdlc-change-set", result.stdout)
        self.assertIn("ai-sdlc-delivery-graph", result.stdout)
        self.assertIn("ai-sdlc-policy", result.stdout)
        self.assertIn("ai-sdlc-runtime", result.stdout)
        self.assertIn("ai-sdlc-workflow", result.stdout)
        self.assertIn("ai-sdlc-host-adapter", result.stdout)
        self.assertIn("ai-sdlc-navigator", result.stdout)

    def test_optional_compatible_skill_is_listed_without_core_dependency(self) -> None:
        """Optional discovery should not make core require the module."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            module(root, "core", "core", "ai-sdlc-core")
            module(root, "architecture", "optional", "ai-sdlc-architecture", requires=["core"])
            result = self.run_modules(root, "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("architecture,1.0.0,optional,yes,no,core", result.stdout)
            self.assertIn("architecture,ai-sdlc-architecture", result.stdout)

    def test_incompatible_enabled_module_fails(self) -> None:
        """Enabled modules must support the current harness API."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            module(root, "core", "core", "ai-sdlc-core")
            module(root, "future", "optional", "ai-sdlc-future", api_min="2.0.0", api_max="3.0.0", requires=["core"])
            result = self.run_modules(root, "--enable", "future")
            self.assertEqual(result.returncode, 1)
            self.assertIn("unavailable or incompatible: future", result.stdout)

    def test_duplicate_skill_ownership_is_rejected(self) -> None:
        """A skill must have one unambiguous module owner."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            module(root, "core", "core", "shared-skill")
            module(root, "extra", "optional", "shared-skill", requires=["core"])
            result = self.run_modules(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("duplicate skill ownership", result.stdout)

    def test_missing_dependency_is_rejected(self) -> None:
        """Dependency closure must be complete in discovered manifests."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            module(root, "core", "core", "ai-sdlc-core")
            module(root, "research", "optional", "ai-sdlc-research", requires=["evidence"])
            result = self.run_modules(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("requires missing module evidence", result.stdout)


if __name__ == "__main__":
    unittest.main()
