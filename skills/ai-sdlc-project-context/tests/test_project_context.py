#!/usr/bin/env python3
"""Tests for evidence-backed project context generation."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "ai-sdlc-project-context" / "scripts" / "project_context.py"


class ProjectContextTests(unittest.TestCase):
    """Project context output and drift tests."""

    def run_context(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run the generator against a fixture."""
        return subprocess.run(["python3", str(SCRIPT), "--root", str(root), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_write_produces_matching_markdown_and_toon(self) -> None:
        """A write should create both canonical outputs with shared identity."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            (root / "README.md").write_text("Run npm test\n", encoding="utf-8")
            (root / "package.json").write_text('{"scripts":{"test":"npm test"}}\n', encoding="utf-8")
            result = self.run_context(root, "--write", "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "project-context.md").is_file())
            self.assertTrue((root / "_ai_sdlc/project-context.toon").is_file())
            self.assertIn("Node.js", result.stdout)
            self.assertIn("README.md", result.stdout)

    def test_check_detects_and_clears_drift(self) -> None:
        """Evidence changes should fail check until context is regenerated."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            readme = root / "README.md"
            readme.write_text("Run make test\n", encoding="utf-8")
            self.assertEqual(self.run_context(root, "--write", "--format", "toon").returncode, 0)
            self.assertEqual(self.run_context(root, "--check", "--format", "toon").returncode, 0)
            readme.write_text("Run make test\nRun make lint\n", encoding="utf-8")
            drift = self.run_context(root, "--check", "--format", "toon")
            self.assertEqual(drift.returncode, 1)
            self.assertIn("drift: yes", drift.stdout)

    def test_secret_named_sources_are_excluded(self) -> None:
        """Secret-named files must never become context evidence."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("Safe guidance\n", encoding="utf-8")
            (root / ".env").write_text("TOKEN=do-not-read\n", encoding="utf-8")
            result = self.run_context(root, "--emit", "--format", "toon")
            self.assertEqual(result.returncode, 0)
            self.assertNotIn("do-not-read", result.stdout)
            self.assertNotIn(".env", result.stdout)

    def test_credential_content_in_named_source_is_excluded(self) -> None:
        """Credential-shaped content in an ordinary source must not be emitted."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text(
                "ACME_PROD_API_KEY=synthetic-value-123\nRun python3 -m unittest\n",
                encoding="utf-8",
            )
            result = self.run_context(root, "--emit", "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("synthetic-value-123", result.stdout)
            self.assertNotIn("README.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
