from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from learning_structure import anchor_errors, heading_errors, learning_order_errors, missing_role_anchors  # noqa: E402
from learning_tokens import learn_navigation  # noqa: E402


class LearningStructureTests(unittest.TestCase):
    def test_missing_learn_page_is_observable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "mkdocs.yml"
            config.write_text("nav:\n  - Learn:\n      - Missing: missing.md\n", encoding="utf-8")
            self.assertEqual(learn_navigation(config), ["missing.md"])
            self.assertFalse((Path(tmp) / "docs" / "missing.md").exists())

    def test_incorrect_learning_order_is_observable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "mkdocs.yml"
            config.write_text("nav:\n  - Learn:\n      - Advanced: advanced.md\n      - Foundations: foundations.md\n", encoding="utf-8")
            self.assertEqual(learn_navigation(config), ["advanced.md", "foundations.md"])
            self.assertTrue(learning_order_errors(["advanced.md", "foundations.md"], [6, 0]))

    def test_missing_role_path_is_rejected(self) -> None:
        missing = missing_role_anchors('<a id="pm-or-po"></a>')
        self.assertIn("business-analyst", missing)
        self.assertNotIn("pm-or-po", missing)

    def test_unresolved_internal_heading_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            (docs / "target.md").write_text("---\ntitle: Target\n---\n# Existing heading\n", encoding="utf-8")
            errors = anchor_errors(docs / "source.md", "[Missing](target.md#not-present)", docs)
            self.assertTrue(any("unresolved heading anchor" in error for error in errors))

    def test_heading_level_violation(self) -> None:
        self.assertTrue(any("skips heading level" in error for error in heading_errors(Path("lesson.md"), "# Page\n### Skipped\n")))


if __name__ == "__main__":
    unittest.main()
