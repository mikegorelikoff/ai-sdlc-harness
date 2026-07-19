#!/usr/bin/env python3
"""Tests for layered policy, protected rules, decisions, profiles, and waivers."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-policy/scripts/policy.py"


class PolicyTests(unittest.TestCase):
    """Exercise deterministic policy control and exception boundaries."""

    def cli(self, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["python3", str(SCRIPT), str(repository), *args], cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def context(self, repository: Path, subject: str = "change:add-audit", **values: object) -> Path:
        path = repository / "context.json"
        path.write_text(json.dumps({"subject": subject, **values}), encoding="utf-8")
        return path

    def rule(self, rule_id: str, action: str, effect: str = "require", gates: list[str] | None = None, protected: bool = False, waivable: bool = True) -> dict[str, object]:
        return {"id": rule_id, "actions": [action], "effect": effect, "when": [], "required_gates": gates or [], "protected": protected, "waivable": waivable, "description": f"Policy for {action}."}

    def layer(self, repository: Path, scope: str, rules: list[dict[str, object]], name: str | None = None) -> Path:
        path = repository / f"{name or scope}.json"
        path.write_text(json.dumps({"schema": "ai-sdlc-policy-layer/v1", "id": name or scope, "version": "1.0.0", "scope": scope, "rules": rules}), encoding="utf-8")
        return path

    def waiver(self, repository: Path, rule_id: str, expires_at: str, action: str = "deploy.preview", subject: str = "change:add-audit") -> Path:
        path = repository / f"{rule_id}-waiver.json"
        path.write_text(json.dumps({"schema": "ai-sdlc-policy-waiver/v1", "id": f"waive-{rule_id}", "rule_id": rule_id, "actions": [action], "subject": subject, "constraints": {"risk": "accepted"}, "owner": "Delivery", "approved_by": "Security", "decision_ref": "DEC-100", "reason": "Bounded migration window.", "issued_at": "2026-07-18T00:00:00Z", "expires_at": expires_at}), encoding="utf-8")
        return path

    def test_profile_resolution_is_deterministic_with_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            first = self.cli(repository, "--resolve", "--profile", "high-assurance", "--write", "--format", "json")
            second = self.cli(repository, "--resolve", "--profile", "high-assurance", "--format", "json")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            resolution = json.loads(first.stdout)
            self.assertEqual(resolution["schema"], "ai-sdlc-policy-resolution/v1")
            self.assertTrue(any(rule["provenance"].startswith("organization:high-assurance") for rule in resolution["rules"]))
            self.assertIn("base-change-apply", resolution["protected_rules"])
            toon = (repository / "_ai_sdlc/policy-resolution.toon").read_text(encoding="utf-8")
            self.assertIn("rules[", toon)
            self.assertIn("required_gates[", toon)

    def test_protected_rule_cannot_be_weakened_or_rescoped(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            weaker = self.rule("base-change-apply", "change.other", "allow", protected=False, waivable=True)
            project = self.layer(repository, "project", [weaker])
            result = self.cli(repository, "--resolve", "--project", str(project))
            self.assertEqual(result.returncode, 1)
            self.assertIn("weakens protected rule base-change-apply", result.stdout)
            self.assertIn("action scope changed", result.stdout)
            self.assertIn("effect require -> allow", result.stdout)

    def test_high_assurance_apply_requires_union_of_gates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            context = self.context(repository)
            result = self.cli(repository, "--evaluate", "change.apply", "--context", str(context), "--profile", "high-assurance", "--as-of", "2026-07-19T00:00:00Z", "--format", "json")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            decision = json.loads(result.stdout)
            self.assertEqual(decision["result"], "require")
            self.assertEqual(decision["required_gates"], ["delta-validation", "fresh-evidence", "owner-approval", "policy-evaluation", "security-review"])
            self.assertEqual(len(decision["matched_rules"]), 2)

    def test_deny_precedence_and_unknown_action_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            context = self.context(repository)
            denied = json.loads(self.cli(repository, "--explain", "command.destructive", "--context", str(context), "--as-of", "2026-07-19T00:00:00Z", "--format", "json").stdout)
            self.assertEqual(denied["result"], "deny")
            unknown = json.loads(self.cli(repository, "--evaluate", "future.unknown", "--context", str(context), "--as-of", "2026-07-19T00:00:00Z", "--format", "json").stdout)
            self.assertEqual(unknown["result"], "deny")
            self.assertIn("unknown-action", unknown["reason_codes"])

    def test_current_waiver_applies_but_expired_and_nonwaivable_do_not(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            organization = self.layer(repository, "organization", [self.rule("org-preview-review", "deploy.preview")])
            context = self.context(repository, risk="accepted")
            current = self.waiver(repository, "org-preview-review", "2026-07-20T00:00:00Z")
            allowed = json.loads(self.cli(repository, "--evaluate", "deploy.preview", "--context", str(context), "--organization", str(organization), "--waiver", str(current), "--as-of", "2026-07-19T00:00:00Z", "--format", "json").stdout)
            self.assertEqual(allowed["result"], "allow")
            self.assertEqual(allowed["waivers"][0]["status"], "applied")
            expired = self.waiver(repository, "org-preview-review", "2026-07-18T12:00:00Z")
            required = json.loads(self.cli(repository, "--evaluate", "deploy.preview", "--context", str(context), "--organization", str(organization), "--waiver", str(expired), "--as-of", "2026-07-19T00:00:00Z", "--format", "json").stdout)
            self.assertEqual(required["result"], "require")
            self.assertEqual(required["waivers"][0]["reason"], "expired")
            base_waiver = self.waiver(repository, "base-change-apply", "2026-07-20T00:00:00Z", action="change.apply")
            rejected = json.loads(self.cli(repository, "--evaluate", "change.apply", "--context", str(context), "--waiver", str(base_waiver), "--as-of", "2026-07-19T00:00:00Z", "--format", "json").stdout)
            self.assertEqual(rejected["waivers"][0]["reason"], "rule-not-waivable")

    def test_regulated_profile_adds_controls_and_conditional_deny(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            context = self.context(repository, purpose="ai-context")
            data = json.loads(self.cli(repository, "--evaluate", "data.production.read", "--context", str(context), "--profile", "regulated", "--as-of", "2026-07-19T00:00:00Z", "--format", "json").stdout)
            self.assertEqual(data["result"], "deny")
            release = json.loads(self.cli(repository, "--evaluate", "release.publish", "--context", str(context), "--profile", "regulated", "--as-of", "2026-07-19T00:00:00Z", "--format", "json").stdout)
            self.assertIn("audit-evidence", release["required_gates"])
            self.assertIn("privacy-review", release["required_gates"])
            self.assertIn("signed-provenance", release["required_gates"])


if __name__ == "__main__":
    unittest.main()
