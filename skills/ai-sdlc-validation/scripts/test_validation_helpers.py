#!/usr/bin/env python3
"""Deterministic tests for repo-local AI validation helpers."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
QUICK_VALIDATE_HELPER = ROOT / ".codex" / "scripts" / "quick_validate_skill.py"
PYTHON_COMPILE_HELPER = ROOT / ".codex" / "scripts" / "python_compile_check.py"
VALIDATION_PLAN = ROOT / ".codex" / "skills" / "ai-sdlc-validation" / "scripts" / "validation_plan.py"
REVIEW_READINESS = ROOT / ".codex" / "skills" / "ai-sdlc-code-review" / "scripts" / "review_readiness.py"
GOVERNANCE_AUDIT = ROOT / ".codex" / "scripts" / "codex_governance_audit.py"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class QuickValidateSkillTests(unittest.TestCase):
    def test_uses_codex_home_override(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            validator = temp_root / "codex-home" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
            write(
                validator,
                """
                import sys
                print(f"validated:{sys.argv[1]}")
                """,
            )
            skill_dir = temp_root / "skill"
            skill_dir.mkdir()

            env = os.environ.copy()
            env["CODEX_HOME"] = str(temp_root / "codex-home")
            env["HOME"] = str(temp_root / "home")
            result = subprocess.run(
                [sys.executable, str(QUICK_VALIDATE_HELPER), str(skill_dir)],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f"validated:{skill_dir}", result.stdout)

    def test_fails_when_validator_cannot_be_found(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            env = os.environ.copy()
            env["CODEX_HOME"] = str(temp_root / "missing-codex-home")
            env["HOME"] = str(temp_root / "empty-home")
            result = subprocess.run(
                [sys.executable, str(QUICK_VALIDATE_HELPER), ".codex/skills/ai-sdlc-workflow"],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("could not locate quick_validate.py", result.stderr)


class PythonCompileCheckTests(unittest.TestCase):
    def test_compiles_with_explicit_pycache_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source = temp_root / "example.py"
            cache_dir = temp_root / "pycache"
            write(
                source,
                """
                VALUE = 1
                """,
            )

            env = os.environ.copy()
            env["PYTHONPYCACHEPREFIX"] = str(cache_dir)
            result = subprocess.run(
                [sys.executable, str(PYTHON_COMPILE_HELPER), str(source)],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(any(cache_dir.rglob("*.pyc")))

    def test_requires_input_files(self) -> None:
        result = subprocess.run(
            [sys.executable, str(PYTHON_COMPILE_HELPER)],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage:", result.stderr)


class ValidationPlanTests(unittest.TestCase):
    def test_ai_runtime_and_spec_changes_get_repo_local_commands(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATION_PLAN),
                ".codex/scripts/quick_validate_skill.py",
                ".codex/hooks/post_tool_use.py",
                ".codex/skills/ai-sdlc-workflow/SKILL.md",
                "specs/176-ai-setup-hardening/requirements.md",
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("python3 .codex/scripts/quick_validate_skill.py .codex/skills/ai-sdlc-workflow", result.stdout)
        self.assertIn("python3 .codex/scripts/python_compile_check.py .codex/scripts/quick_validate_skill.py .codex/hooks/post_tool_use.py", result.stdout)
        self.assertIn("python3 .codex/hooks/tests/test_hook_runtime.py", result.stdout)
        self.assertIn("python3 .codex/scripts/codex_ai_lint.py --format text", result.stdout)
        self.assertIn("python3 .codex/skills/ai-sdlc-sdd/scripts/validate_spec.py specs/176-ai-setup-hardening", result.stdout)
        self.assertIn("python3 .codex/skills/ai-sdlc-sdd/scripts/check_clarify.py specs/176-ai-setup-hardening", result.stdout)
        self.assertIn("python3 .codex/skills/ai-sdlc-sdd/scripts/check_checklist.py specs/176-ai-setup-hardening", result.stdout)
        self.assertIn("python3 .codex/skills/ai-sdlc-sdd/scripts/analyze_spec.py specs/176-ai-setup-hardening", result.stdout)
        self.assertIn("python3 .codex/skills/ai-sdlc-sdd/scripts/sdd_status.py --spec specs/176-ai-setup-hardening", result.stdout)
        self.assertIn("python3 .codex/scripts/codex_governance_audit.py", result.stdout)


class ReviewReadinessTests(unittest.TestCase):
    def test_skill_warning_uses_repo_local_helper(self) -> None:
        module = load_module(REVIEW_READINESS, "review_readiness")
        warnings = module.skill_metadata_warnings([".codex/skills/ai-sdlc-workflow/SKILL.md"], full_repo=False)
        self.assertTrue(any("python3 .codex/scripts/quick_validate_skill.py .codex/skills/ai-sdlc-workflow" in warning for warning in warnings))


class GovernanceAuditTests(unittest.TestCase):
    def test_reports_missing_files_and_todo_items(self) -> None:
        module = load_module(GOVERNANCE_AUDIT, "codex_governance_audit")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            spec_dir = temp_root / "specs" / "001-example"
            spec_dir.mkdir(parents=True)
            write(
                spec_dir / "requirements.md",
                """
                # Requirements

                ## Goal

                TODO(dm): Who owns this historical traceability decision?
                """,
            )
            write(
                temp_root / "specs" / "spec-registry.md",
                """
                # Spec Registry

                | --- | --- | --- | --- | --- | --- | --- | --- |
                """,
            )

            result = module.audit(temp_root)

            self.assertEqual(result.spec_count, 1)
            self.assertEqual(result.unregistered_specs, ["001-example"])
            self.assertIn("001-example", result.missing_files)
            self.assertTrue(any("TODO(dm)" in item for item in result.todo_dm))


if __name__ == "__main__":
    unittest.main()
