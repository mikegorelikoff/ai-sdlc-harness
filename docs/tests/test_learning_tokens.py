from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import tiktoken

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from learning_tokens import count_is_valid, count_markdown_bytes, learn_navigation, measure_learn_pages, normalize_markdown_bytes  # noqa: E402


class LearningTokenTests(unittest.TestCase):
    def test_exact_boundaries(self) -> None:
        self.assertFalse(count_is_valid(5999, 6000, 8000))
        self.assertTrue(count_is_valid(6000, 6000, 8000))
        self.assertTrue(count_is_valid(7000, 6000, 8000))
        self.assertTrue(count_is_valid(8000, 6000, 8000))
        self.assertFalse(count_is_valid(8001, 6000, 8000))

    def test_yaml_front_matter_is_excluded(self) -> None:
        self.assertEqual(
            count_markdown_bytes(b"---\ntitle: Ignored\n---\nVisible body.\n"),
            count_markdown_bytes(b"Visible body.\n"),
        )

    def test_html_maintainer_comment_is_excluded(self) -> None:
        self.assertEqual(
            count_markdown_bytes(b"Visible.<!-- maintainer-only -->\n"),
            count_markdown_bytes(b"Visible.\n"),
        )

    def test_html_comment_syntax_inside_fenced_code_is_included(self) -> None:
        raw = b"before\n```html\n<!-- rendered example -->\n```\nafter\n"
        self.assertEqual(
            count_markdown_bytes(raw),
            len(tiktoken.get_encoding("o200k_base").encode(raw.decode("utf-8"))),
        )

    def test_code_blocks_are_included(self) -> None:
        self.assertGreater(
            count_markdown_bytes(b"Visible.\n```python\nprint('measured')\n```\n"),
            count_markdown_bytes(b"Visible.\n"),
        )

    def test_unicode_is_supported(self) -> None:
        self.assertGreater(count_markdown_bytes("Проверка 日本語 café".encode("utf-8")), 0)

    def test_malformed_utf8_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "malformed UTF-8"):
            normalize_markdown_bytes(b"\xff", "bad.md")

    def test_duplicate_navigation_page_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "mkdocs.yml"
            config.write_text("nav:\n  - Learn:\n      - A: missing.md\n      - Again: missing.md\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicated Learn pages"):
                learn_navigation(config)

    def test_missing_learn_page_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "mkdocs.yml"
            config.write_text("nav:\n  - Learn:\n      - Missing: missing.md\n", encoding="utf-8")
            (root / "docs").mkdir()
            with self.assertRaisesRegex(ValueError, "missing Learn page"):
                measure_learn_pages(config)


if __name__ == "__main__":
    unittest.main()
