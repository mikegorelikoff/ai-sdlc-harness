#!/usr/bin/env python3
"""Behavior tests for the AI SDLC navigator."""

from __future__ import annotations

import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "ai-sdlc-navigator" / "scripts" / "navigate.py"


def write(path: Path, content: str) -> None:
    """Write a fixture file with parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def install_skill(root: Path, name: str) -> None:
    """Create a minimal discoverable skill fixture."""
    write(root / "skills" / name / "SKILL.md", f"---\nname: {name}\ndescription: fixture\n---")


class NavigateTests(unittest.TestCase):
    """Navigator routing contract tests."""

    def run_nav(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        """Run the navigator against a fixture repository."""
        return subprocess.run(
            ["python3", str(SCRIPT), "--root", str(root), *args],
            check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def test_empty_project_recommends_discovery(self) -> None:
        """An empty project should start with working-backwards discovery."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            install_skill(root, "ai-sdlc-working-backwards-discovery")
            result = self.run_nav(root, "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("schema: ai-sdlc-navigator/v1", result.stdout)
            self.assertIn("ai-sdlc-working-backwards-discovery", result.stdout)
            self.assertIn("blockers[0]", result.stdout)

    def test_active_feature_state_has_priority_over_intent(self) -> None:
        """An active lifecycle skill should outrank unrelated intent keywords."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            install_skill(root, "ai-sdlc-sdd")
            write(
                root / "specs" / "101-payments" / "_ai_sdlc" / "state.toon",
                """
                feature: 101-payments
                workspace: implementation
                current_stage: sdd
                active_skill: ai-sdlc-sdd
                flow_mode: quick
                updated_at: 2026-07-18
                decision_log: specs/101-payments/decision-log.md

                stages[1]{id,skill,status,workspace,artifacts,decision_ref}:
                  sdd,ai-sdlc-sdd,in_progress,implementation,specs/101-payments,DEC-001

                skips[0]{stage,reason,decision_ref,flow_mode}:
                """,
            )
            result = self.run_nav(root, "--intent", "commit this", "--format", "markdown")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Resume $ai-sdlc-sdd", result.stdout)
            self.assertNotIn("Skill: `ai-sdlc-commit-prep`", result.stdout)

    def test_explicit_missing_feature_is_a_blocker(self) -> None:
        """A missing explicit feature must not silently route to another feature."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            install_skill(root, "ai-sdlc-sdd")
            result = self.run_nav(root, "--feature", "missing", "--intent", "implement api", "--format", "toon")
            self.assertEqual(result.returncode, 1)
            self.assertIn("explicit feature state not found: missing", result.stdout)

    def test_next_incomplete_state_stage_is_recommended(self) -> None:
        """The first incomplete stage in the selected workspace should be required."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            install_skill(root, "ai-sdlc-branching")
            write(
                root / "specs" / "102-router" / "_ai_sdlc" / "state.toon",
                """
                feature: 102-router
                workspace: implementation
                current_stage: sdd
                active_skill:
                flow_mode: quick
                updated_at: 2026-07-18
                decision_log: specs/102-router/decision-log.md

                stages[2]{id,skill,status,workspace,artifacts,decision_ref}:
                  sdd,ai-sdlc-sdd,done,implementation,specs/102-router,DEC-001
                  branching,ai-sdlc-branching,not_started,implementation,branch-plan.md,

                skips[0]{stage,reason,decision_ref,flow_mode}:
                """,
            )
            result = self.run_nav(root, "--feature", "102-router", "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ai-sdlc-branching", result.stdout)
            self.assertIn("branch-plan.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
