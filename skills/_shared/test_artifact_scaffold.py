#!/usr/bin/env python3
"""Focused tests for stdin-driven Markdown artifact assembly."""

from __future__ import annotations

import unittest
import subprocess
import sys
import tempfile
from pathlib import Path

from ai_sdlc_artifact_helper import (
    EMPTY_SECTION_MARKER,
    markdown_section_spans,
    replace_or_insert_section,
    refreshed_artifact_metadata,
    scaffold_body,
    unfinished_sections,
    upsert_decision_row,
    validate_section_content,
)


class ArtifactScaffoldTests(unittest.TestCase):
    """Validate section parsing, patching, and decision row behavior."""

    def test_profile_write_rejects_symlinked_feature_directory(self) -> None:
        root = Path(__file__).resolve().parents[2]
        script = root / "skills/ai-sdlc-qa/scripts/qa_plan_scaffold.py"
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp); repository = parent / "repo"; outside = parent / "outside"
            (repository / "specs-refiniment").mkdir(parents=True); outside.mkdir()
            (repository / "specs-refiniment/demo").symlink_to(outside, target_is_directory=True)
            result = subprocess.run(
                [sys.executable, str(script), "--feature", "demo", "--quick-flow", "--emit-template", "--write"],
                cwd=repository, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(outside.iterdir()), [])
            self.assertNotIn("Traceback", result.stderr)

    def test_content_accepts_nested_headings_and_fenced_h2(self) -> None:
        content = """Summary.\n\n### Detail\n\n```markdown\n## Example\n```"""
        self.assertEqual(validate_section_content(content), content)

    def test_content_rejects_top_level_headings_and_unclosed_fence(self) -> None:
        with self.assertRaisesRegex(ValueError, "H1 or H2"):
            validate_section_content("## Goal\nBody")
        with self.assertRaisesRegex(ValueError, "unclosed"):
            validate_section_content("```text\nvalue")

    def test_section_patch_preserves_other_and_custom_sections(self) -> None:
        sections = ["Goal", "Scope"]
        text = scaffold_body("artifact.md", sections) + "\n## Custom\nKeep this.\n"
        updated = replace_or_insert_section(text, "Goal", "New goal.", sections)
        self.assertIn("## Goal\nNew goal.", updated)
        self.assertIn(f"## Scope\n{EMPTY_SECTION_MARKER}", updated)
        self.assertIn("## Custom\nKeep this.", updated)
        self.assertEqual(unfinished_sections(updated, sections), ["Scope"])

    def test_section_parser_ignores_fenced_h2(self) -> None:
        text = "## Goal\n```markdown\n## Not A Section\n```\n\n## Scope\nBody\n"
        self.assertEqual([span[0] for span in markdown_section_spans(text)], ["Goal", "Scope"])

    def test_decision_row_appends_and_replaces_by_id(self) -> None:
        log = """# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
"""
        first = "| DEC-001 | 2026-07-10 | proposed | BA | Use scaffold | request | manual; script | artifact.md | AC-001 |"
        updated = upsert_decision_row(log, first)
        replacement = "| DEC-001 | 2026-07-10 | accepted | BA | Use stdin | tests | files; stdin | artifact.md | TC-001 |"
        updated = upsert_decision_row(updated, replacement)
        self.assertNotIn("Use scaffold", updated)
        self.assertEqual(updated.count("DEC-001"), 1)
        self.assertIn("Use stdin", updated)

    def test_decision_row_rejects_invalid_shape(self) -> None:
        with self.assertRaisesRegex(ValueError, "9 cells"):
            upsert_decision_row("# Decision Log\n", "| DEC-001 | too few |")

    def test_refreshed_metadata_drops_trace_ids_absent_from_body(self) -> None:
        text = """---
artifact_metadata:
  trace_ids:
    - "AC-001"
    - "AC-999"
---
# Tasks

## Implementation
- [x] T001. Deliver AC-001.
"""
        updated = refreshed_artifact_metadata(
            text=text,
            feature="001-demo",
            artifact_name="tasks.md",
            artifact_path="specs/001-demo/tasks.md",
            workspace="implementation",
            skill_name="ai-sdlc-sdd",
            flow_mode="quick",
            decision_log_path="specs/001-demo/decision-log.md",
            state_file_path="specs/001-demo/_ai_sdlc/state.toon",
            state_args=None,
            status="review",
        )
        self.assertIn('    - "AC-001"', updated)
        self.assertNotIn("AC-999", updated)


if __name__ == "__main__":
    unittest.main()
