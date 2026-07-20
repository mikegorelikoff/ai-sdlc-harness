#!/usr/bin/env python3
"""Tests for deterministic layered AI SDLC configuration."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/_shared/ai_sdlc_config.py"
DEFAULTS = ROOT / "config/ai-sdlc.defaults.json"


def write(path: Path, values: dict[str, object], protected: list[str] | None = None) -> None:
    """Write one configuration layer."""
    payload: dict[str, object] = {"schema": "ai-sdlc-config/v1", "values": values}
    if protected is not None:
        payload["protected"] = protected
    path.write_text(json.dumps(payload), encoding="utf-8")


class ConfigTests(unittest.TestCase):
    """Precedence, provenance, determinism, and gate safety tests."""

    def run_config(self, *args: str) -> subprocess.CompletedProcess[str]:
        """Run the resolver with captured output."""
        return subprocess.run(["python3", str(SCRIPT), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_precedence_and_provenance_are_deterministic(self) -> None:
        """User values should win normal settings with exact provenance."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            team, user = root / "team.json", root / "user.json"
            write(team, {"output": {"human": "html"}, "modules": {"enabled": ["architecture"]}})
            write(user, {"output": {"human": "markdown"}, "modules": {"enabled": ["research"]}})
            args = ("--base", str(DEFAULTS), "--team", str(team), "--user", str(user), "--format", "json")
            first, second = self.run_config(*args), self.run_config(*args)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            value = json.loads(first.stdout)
            self.assertEqual(value["values"]["modules"]["enabled"], ["research"])
            self.assertEqual(value["provenance"]["modules.enabled"], "user")

    def test_protected_boolean_cannot_be_weakened(self) -> None:
        """User configuration must not disable a required gate."""
        with tempfile.TemporaryDirectory() as temp:
            user = Path(temp) / "user.json"
            write(user, {"gates": {"require_traceability": False}})
            result = self.run_config("--base", str(DEFAULTS), "--user", str(user))
            self.assertEqual(result.returncode, 1)
            self.assertIn("weakens protected gate gates.require_traceability", result.stdout)

    def test_protected_rigor_can_strengthen_but_not_downgrade(self) -> None:
        """Strictness order should allow strengthening across layers."""
        with tempfile.TemporaryDirectory() as temp:
            team, user = Path(temp) / "team.json", Path(temp) / "user.json"
            write(team, {"rigor": {"minimum_profile": "assured"}})
            write(user, {"rigor": {"minimum_profile": "patch"}})
            blocked = self.run_config("--base", str(DEFAULTS), "--team", str(team), "--user", str(user))
            self.assertEqual(blocked.returncode, 1)
            self.assertIn("assured", blocked.stdout)
            allowed = self.run_config("--base", str(DEFAULTS), "--team", str(team), "--format", "toon")
            self.assertEqual(allowed.returncode, 0, allowed.stdout + allowed.stderr)
            self.assertIn("rigor.minimum_profile,assured,team,yes", allowed.stdout)

    def test_user_can_set_typed_interaction_preferences(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            user = Path(temp) / "user.json"
            write(user, {"interaction": {
                "enabled": True,
                "preferred_name": "Mike",
                "language": "en",
                "response_style": "concise",
                "technical_depth": "practitioner",
                "status_updates": "milestones",
            }})
            result = self.run_config("--base", str(DEFAULTS), "--user", str(user), "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("interaction.preferred_name,Mike,user,no", result.stdout)
            self.assertIn("interaction.response_style,concise,user,no", result.stdout)

    def test_invalid_interaction_preference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            user = Path(temp) / "user.json"
            invalid = [
                ({"response_style": "telepathic"}, "interaction.response_style must be one of"),
                ({"language": " en "}, "interaction.language must be auto or a simple BCP-47 language tag"),
                ({"preferred_name": " " * 81}, "interaction.preferred_name must be a control-free string"),
            ]
            for values, expected in invalid:
                with self.subTest(values=values):
                    write(user, {"interaction": {"enabled": True, **values}})
                    result = self.run_config("--base", str(DEFAULTS), "--user", str(user))
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(expected, result.stdout)

    def test_non_base_layer_cannot_redefine_protection(self) -> None:
        """Protection ownership remains in the base contract."""
        with tempfile.TemporaryDirectory() as temp:
            team = Path(temp) / "team.json"
            write(team, {}, protected=[])
            result = self.run_config("--base", str(DEFAULTS), "--team", str(team))
            self.assertEqual(result.returncode, 1)
            self.assertIn("cannot redefine protected paths", result.stdout)

    def test_explicit_missing_layer_is_not_silently_ignored(self) -> None:
        """A configured layer path must exist so provenance stays honest."""
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "team.json"
            result = self.run_config("--base", str(DEFAULTS), "--team", str(missing))
            self.assertEqual(result.returncode, 1)
            self.assertIn("team config does not exist", result.stdout)


if __name__ == "__main__":
    unittest.main()
