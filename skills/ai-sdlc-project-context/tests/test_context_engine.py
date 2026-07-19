#!/usr/bin/env python3
"""Tests for repository topology and bounded task context packs."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ENGINE = ROOT / "skills/ai-sdlc-project-context/scripts/context_engine.py"
CONTEXT = ROOT / "skills/ai-sdlc-project-context/scripts/project_context.py"


class ContextEngineTests(unittest.TestCase):
    """Exercise topology, selection, budgets, secrets, freshness, and validation."""

    def cli(self, script: Path, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["python3", str(script), "--root", str(repository), *args], cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def setup_repository(self, repository: Path) -> None:
        (repository / ".github").mkdir(parents=True)
        (repository / ".github/CODEOWNERS").write_text("src/*.py @payments-team\n", encoding="utf-8")
        (repository / "src").mkdir()
        (repository / "src/payments.py").write_text("def pay():\n    return True\n", encoding="utf-8")
        (repository / "tests").mkdir()
        (repository / "tests/test_payments.py").write_text("def test_pay():\n    assert True\n", encoding="utf-8")
        (repository / "README.md").write_text("# Fixture\n\n```bash\npython3 -m unittest\n```\n", encoding="utf-8")
        (repository / "AGENTS.md").write_text("# Guidance\n\nRun focused tests.\n", encoding="utf-8")
        (repository / "pyproject.toml").write_text("[project]\nname='fixture'\n", encoding="utf-8")

    def selector_config(self, repository: Path, selectors: list[dict[str, object]], exclusions: list[str] | None = None) -> Path:
        path = repository / "selectors.json"
        path.write_text(json.dumps({"schema": "ai-sdlc-context-selectors/v2", "selectors": selectors, "exclusions": exclusions or []}), encoding="utf-8")
        return path

    def selector(self, selector_id: str, include: list[str], tag: str = "security") -> dict[str, object]:
        return {"id": selector_id, "when": {"task": "T*", "paths_any": [], "tags_any": [tag]}, "include": include, "priority": 95, "max_tokens": 200, "reason": "Security task evidence."}

    def test_topology_maps_owners_and_related_tests(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            result = self.cli(ENGINE, repository, "--topology", "--format", "json")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            topology = json.loads(result.stdout)
            source = next(row for row in topology["files"] if row["path"] == "src/payments.py")
            self.assertEqual(source["owners"], ["@payments-team"])
            self.assertEqual(source["tests"], ["tests/test_payments.py"])
            self.assertIn("python3 -m unittest", topology["commands"])

    def test_pack_is_deterministic_and_never_exceeds_budget(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            (repository / "src/payments.py").write_text("x = 1\n" * 1000, encoding="utf-8")
            args = ("--build-pack", "--task", "T009", "--goal", "Bound the context.", "--path", "src/payments.py", "--budget", "128", "--write", "--format", "json")
            first = self.cli(ENGINE, repository, *args)
            second = self.cli(ENGINE, repository, *args)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            pack = json.loads(first.stdout)
            self.assertLessEqual(pack["budget"]["used_tokens"], 128)
            self.assertEqual(pack["budget"]["used_tokens"] + pack["budget"]["remaining_tokens"], 128)
            self.assertTrue(any(item["truncated"] for item in pack["selected"]))
            self.assertEqual((repository / "_ai_sdlc/context/task-packs/T009.json").read_text(encoding="utf-8"), second.stdout)
            toon = (repository / "_ai_sdlc/context/task-packs/T009.toon").read_text(encoding="utf-8")
            self.assertIn("selected[", toon)
            self.assertIn("selected[2]{content,", toon)

    def test_conditional_selector_explains_match_and_skip(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            (repository / "docs").mkdir()
            (repository / "docs/security.md").write_text("# Security review\n", encoding="utf-8")
            config = self.selector_config(repository, [self.selector("security-docs", ["docs/*.md"]), self.selector("release-docs", ["README.md"], tag="release")])
            result = self.cli(ENGINE, repository, "--build-pack", "--task", "T009", "--goal", "Review security.", "--tag", "security", "--selector-config", str(config), "--budget", "500", "--format", "json")
            pack = json.loads(result.stdout)
            self.assertIn("docs/security.md", [item["path"] for item in pack["selected"]])
            statuses = {item["id"]: item["status"] for item in pack["selectors"]}
            self.assertEqual(statuses, {"release-docs": "tag-condition-not-matched", "security-docs": "matched"})

    def test_secret_named_and_credential_content_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            (repository / ".env").write_text("TOKEN=secret-value\n", encoding="utf-8")
            (repository / "docs").mkdir()
            (repository / "docs/config.md").write_text("api_key=supersecret123\n", encoding="utf-8")
            config = self.selector_config(repository, [self.selector("unsafe", [".env", "docs/config.md"])])
            result = self.cli(ENGINE, repository, "--build-pack", "--task", "T009", "--goal", "Keep secrets out.", "--tag", "security", "--selector-config", str(config), "--budget", "500", "--format", "json")
            pack = json.loads(result.stdout)
            selected = {item["path"] for item in pack["selected"]}
            self.assertNotIn(".env", selected)
            self.assertNotIn("docs/config.md", selected)
            exclusions = {item["path"]: item["reason"] for item in pack["exclusions"]}
            self.assertEqual(exclusions[".env"], "secret-named-path")
            self.assertEqual(exclusions["docs/config.md"], "credential-like-content")

    def test_project_context_and_evidence_staleness_warn_selected_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            written = self.cli(CONTEXT, repository, "--write", "--quick-flow")
            self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
            (repository / "README.md").write_text("# Changed fixture\n", encoding="utf-8")
            ledger_dir = repository / "_ai_sdlc"
            ledger_dir.mkdir(exist_ok=True)
            (ledger_dir / "evidence-ledger.json").write_text(json.dumps({"schema": "ai-sdlc-evidence-ledger/v1", "fingerprint": "a" * 64, "records": [{"id": "readme-proof", "status": "stale", "files": [{"path": "README.md"}]}]}), encoding="utf-8")
            result = self.cli(ENGINE, repository, "--build-pack", "--task", "T009", "--goal", "Use current docs.", "--path", "README.md", "--budget", "500", "--format", "json")
            pack = json.loads(result.stdout)
            self.assertEqual(pack["freshness"]["project_context"], "stale")
            codes = [item["code"] for item in pack["freshness"]["warnings"]]
            self.assertIn("project-context-stale", codes)
            self.assertIn("selected-evidence-not-fresh", codes)

    def test_unsafe_selector_and_invalid_budget_fail_before_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.setup_repository(repository)
            config = self.selector_config(repository, [self.selector("escape", ["../secret.txt"])])
            unsafe = self.cli(ENGINE, repository, "--build-pack", "--task", "T009", "--goal", "Reject escape.", "--selector-config", str(config))
            self.assertEqual(unsafe.returncode, 1)
            self.assertIn("safe globs", unsafe.stdout)
            budget = self.cli(ENGINE, repository, "--build-pack", "--task", "T009", "--goal", "Reject budget.", "--budget", "10")
            self.assertEqual(budget.returncode, 1)
            self.assertIn("128..32000", budget.stdout)


if __name__ == "__main__":
    unittest.main()
