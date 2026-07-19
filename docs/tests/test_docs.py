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
    navigation_paths,
    parse_frontmatter,
    validate_links,
    validate_navigation,
)


class DocumentationValidationTests(unittest.TestCase):
    def test_parse_material_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.md"
            path.write_text("---\ntitle: Test\ndescription: Useful\n---\n\nBody text.", encoding="utf-8")
            page = parse_frontmatter(path)
            self.assertEqual(page.metadata["title"], "Test")
            self.assertEqual(page.body, "Body text.")

    def test_navigation_paths_preserve_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mkdocs.yml"
            path.write_text(
                "nav:\n  - Home: index.md\n  - Guides:\n      - Install: how-to/install.md\n",
                encoding="utf-8",
            )
            self.assertEqual(navigation_paths(path), ["index.md", "how-to/install.md"])

    def test_relative_markdown_links_are_detected(self) -> None:
        page = Page(Path("docs/source.md"), {}, "[Target](reference/target.md#contract)")
        self.assertEqual(internal_links(page), {"reference/target.md#contract"})

    def test_broken_internal_link_reports_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            source_path = docs / "source.md"
            source_path.write_text("", encoding="utf-8")
            source = Page(source_path, {}, "[Missing](missing.md)")
            errors = validate_links([source], docs)
            self.assertEqual(len(errors), 1)
            self.assertIn("broken internal link missing.md", errors[0])

    def test_root_absolute_link_is_rejected(self) -> None:
        page = Page(Path("docs/source.md"), {}, '<a href="/missing/">Missing</a>')
        errors = validate_links([page], Path("docs"))
        self.assertTrue(any("root-absolute" in error for error in errors))

    def test_duplicate_navigation_page_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            page_path = docs / "index.md"
            page_path.write_text("---\ntitle: Home\ndescription: Home\n---\n", encoding="utf-8")
            config = root / "mkdocs.yml"
            config.write_text("nav:\n  - Home: index.md\n  - Again: index.md\n", encoding="utf-8")
            pages = [Page(page_path, {"title": "Home", "description": "Home"}, "Body")]
            errors = validate_navigation(pages, docs, config)
            self.assertTrue(any("duplicate pages" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
