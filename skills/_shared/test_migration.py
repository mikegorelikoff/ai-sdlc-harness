#!/usr/bin/env python3
"""Production migration and canonical-contract tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_sdlc_artifact_profiles import PROFILES, required_sections, required_tables
from ai_sdlc_migrate import MigrationConflict, migrate_feature, migrate_pair
from ai_sdlc_specs_index import write_indexes_for_roots
from ai_sdlc_state_machine import REFINEMENT_STAGES, initial_state, save_state
from refinement_status import inspect_package


class MigrationTests(unittest.TestCase):
    def test_missing_canonical_moves_legacy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            legacy = root / "feature/state.toon"
            canonical = root / "feature/_ai_sdlc/state.toon"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("feature: demo\n", encoding="utf-8")
            result = migrate_pair(canonical, legacy, apply=True)
            self.assertEqual(result.action, "move")
            self.assertTrue(canonical.is_file())
            self.assertFalse(legacy.exists())

    def test_identical_duplicate_is_removed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            canonical = root / "canonical.md"
            legacy = root / "legacy.md"
            canonical.write_text("same\n", encoding="utf-8")
            legacy.write_text("same\n", encoding="utf-8")
            result = migrate_pair(canonical, legacy, apply=True)
            self.assertEqual(result.action, "deduplicate")
            self.assertFalse(legacy.exists())

    def test_divergent_duplicate_never_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            canonical = root / "canonical.md"
            legacy = root / "legacy.md"
            canonical.write_text("canonical\n", encoding="utf-8")
            legacy.write_text("legacy\n", encoding="utf-8")
            with self.assertRaises(MigrationConflict):
                migrate_pair(canonical, legacy, apply=True)
            self.assertEqual(canonical.read_text(encoding="utf-8"), "canonical\n")
            self.assertEqual(legacy.read_text(encoding="utf-8"), "legacy\n")

    def test_refinement_contract_is_unique_and_handoff_is_last(self) -> None:
        self.assertEqual(len(PROFILES), 18)
        self.assertEqual(len({profile.stage_id for profile in PROFILES}), 18)
        self.assertEqual(len({profile.skill for profile in PROFILES}), 18)
        self.assertEqual(len({profile.artifact_name for profile in PROFILES}), 18)
        self.assertEqual(REFINEMENT_STAGES[-1].stage_id, "delivery_handoff")
        self.assertEqual(REFINEMENT_STAGES[-1].predecessors, ("delivery_spec", "qa_traceability"))

    def test_feature_migration_handles_markdown_alias(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            legacy = root / "specs-refiniment/demo/discovery-notes.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("# Discovery\n", encoding="utf-8")
            migrate_feature(root, "demo", "refinement", apply=True)
            self.assertTrue((legacy.parent / "discovery.md").is_file())
            self.assertFalse(legacy.exists())

    def test_full_eighteen_stage_package_passes_strict_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            feature = "production-ready"
            workspace_root = root / "specs-refiniment"
            feature_root = workspace_root / feature
            feature_root.mkdir(parents=True)
            state = initial_state(feature, "refinement")
            for row in state["stages"]:
                if row["workspace"] == "refinement":
                    row["status"] = "done"
            save_state(feature_root / "_ai_sdlc/state.toon", state)
            (feature_root / "decision-log.md").write_text("# Decision Log\n", encoding="utf-8")
            for profile in PROFILES:
                bodies = []
                tables = required_tables(profile)
                for section in required_sections(profile, "full"):
                    if section in tables:
                        headers = tables[section]
                        body = "\n".join((
                            "| " + " | ".join(headers) + " |",
                            "| " + " | ".join("---" for _ in headers) + " |",
                            "| " + " | ".join(f"Verified {header}" for header in headers) + " |",
                        ))
                    else:
                        body = (
                            f"- {section} contains verified feature behavior, constraints, ownership, and downstream implications.\n"
                            "- Evidence is complete; Owner: Delivery; Impact: controlled; Resolution: accepted."
                        )
                    bodies.append(f"## {section}\n{body}")
                path = feature_root / profile.artifact_name
                path.write_text(
                    "---\nartifact_metadata:\n"
                    f"  feature: \"{feature}\"\n  artifact: \"{profile.artifact_name}\"\n"
                    f"  path: \"specs-refiniment/{feature}/{profile.artifact_name}\"\n"
                    f"  workspace: \"refinement\"\n  skill: \"{profile.skill}\"\n"
                    "  flow_mode: \"full\"\n  status: \"review\"\n  related_artifacts: []\n"
                    "  metatags: []\n---\n\n# Artifact\n\n" + "\n\n".join(bodies) + "\n",
                    encoding="utf-8",
                )
            write_indexes_for_roots([workspace_root])
            issues, _, _ = inspect_package(root, feature, "full")
            self.assertEqual([issue for issue in issues if issue.severity == "error"], [])


if __name__ == "__main__":
    unittest.main()
