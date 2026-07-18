#!/usr/bin/env python3
"""Tests for explainable adaptive rigor selection."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "skills" / "_shared" / "ai_sdlc_rigor.py"
SPEC = importlib.util.spec_from_file_location("ai_sdlc_rigor", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules["ai_sdlc_rigor"] = MODULE
SPEC.loader.exec_module(MODULE)


def factors(**overrides: int) -> dict[str, int]:
    """Build a complete factor map."""
    values = {name: 0 for name in MODULE.FACTOR_NAMES}
    values.update(overrides)
    return values


class RigorTests(unittest.TestCase):
    """Adaptive policy behavior tests."""

    def test_low_risk_is_patch(self) -> None:
        """Local reversible work should use patch rigor."""
        decision = MODULE.decide(factors(ambiguity=1))
        self.assertEqual(decision.effective_profile, "patch")

    def test_elevated_combined_risk_is_assured(self) -> None:
        """Several elevated factors should require assured rigor."""
        decision = MODULE.decide(factors(blast_radius=2, ambiguity=2, external_dependencies=2))
        self.assertEqual(decision.effective_profile, "assured")

    def test_compliance_is_regulated(self) -> None:
        """Material compliance exposure should require regulated rigor."""
        decision = MODULE.decide(factors(compliance=2))
        self.assertEqual(decision.effective_profile, "regulated")

    def test_quick_flow_cannot_downgrade_critical_risk(self) -> None:
        """Quick flow should be raised when automatic risk is stricter."""
        decision = MODULE.decide(factors(security_data=3), quick_flow=True)
        self.assertEqual(decision.requested_profile, "patch")
        self.assertEqual(decision.effective_profile, "regulated")
        self.assertTrue(any("raised" in reason for reason in decision.reasons))

    def test_full_flow_and_minimum_never_downgrade(self) -> None:
        """Full flow and organization minimums should preserve stricter rigor."""
        decision = MODULE.decide(factors(), full_flow=True, minimum="regulated")
        self.assertEqual(decision.requested_profile, "assured")
        self.assertEqual(decision.effective_profile, "regulated")

    def test_identical_inputs_are_deterministic(self) -> None:
        """The same factor map should produce the same full decision."""
        values = factors(blast_radius=1, rollout_complexity=2)
        self.assertEqual(MODULE.decide(values), MODULE.decide(values))


if __name__ == "__main__":
    unittest.main()
