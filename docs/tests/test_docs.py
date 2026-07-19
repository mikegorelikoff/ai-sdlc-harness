from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_docs import (  # noqa: E402
    Page,
    internal_links,
    navigation_urls,
    parse_frontmatter,
    validate_links,
    validate_navigation,
)


class DocumentationValidationTests(unittest.TestCase):
    def test_parse_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.md"
            path.write_text(
                "---\nlayout: default\ntitle: Test\ndescription: Useful\npermalink: /test/\nnav_order: 1\n---\n\nBody text.",
                encoding="utf-8",
            )
            page = parse_frontmatter(path)
            self.assertEqual(page.metadata["permalink"], "/test/")
            self.assertEqual(page.body, "Body text.")

    def test_navigation_urls_preserve_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "navigation.yml"
            path.write_text("- title: One\n  url: /one/\n  children:\n    - title: Two\n      url: /two/\n", encoding="utf-8")
            self.assertEqual(navigation_urls(path), ["/one/", "/two/"])

    def test_liquid_relative_links_are_detected(self) -> None:
        page = Page(Path("source.md"), {"permalink": "/source/"}, "[Target]({{ '/target/' | relative_url }})")
        self.assertEqual(internal_links(page), {"/target/"})

    def test_broken_internal_link_reports_source(self) -> None:
        source = Page(Path("source.md"), {"permalink": "/source/"}, '<a href="/missing/">Missing</a>')
        errors = validate_links([source])
        self.assertEqual(len(errors), 1)
        self.assertIn("broken internal link /missing/", errors[0])

    def test_duplicate_page_permalink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            (docs / "_data").mkdir()
            (docs / "_data" / "navigation.yml").write_text("- title: Same\n  url: /same/\n", encoding="utf-8")
            pages = [
                Page(docs / "one.md", {"permalink": "/same/"}, "Body"),
                Page(docs / "two.md", {"permalink": "/same/"}, "Body"),
            ]
            errors = validate_navigation(pages, docs)
            self.assertTrue(any("same permalink" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
