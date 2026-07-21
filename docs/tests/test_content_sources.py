from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from learning_structure import destination_alignment_errors, load_sources, source_usage_errors  # noqa: E402


def source_record(**updates: object) -> dict[str, object]:
    record: dict[str, object] = {
        "source_id": "SOURCE-ONE",
        "title": "A source",
        "publisher_or_owner": "Owner",
        "canonical_url": "https://example.com/source",
        "source_type": "web-guidance",
        "version_release_tag_or_commit": "reviewed-2026-07-21",
        "reviewed_date": "2026-07-21",
        "verified_license": "Copyright; reference only",
        "license_url": "https://example.com/license",
        "reuse_class": "reference-only",
        "material_consulted": ["Topic index"],
        "adopted_concepts": ["Topic coverage"],
        "excluded_material": ["Wording and examples"],
        "destination_pages": ["docs/learn/ai-foundations.md"],
        "adaptation_summary": "The topic was checked, expressed in harness terms, and replaced with an original repository example.",
        "attribution_requirement": "Link and identify owner.",
        "reviewer": "Documentation maintainer",
        "review_status": "verified",
    }
    record.update(updates)
    return record


class ContentSourceTests(unittest.TestCase):
    def write_registry(self, record: dict[str, object]) -> Path:
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / "sources.yml"
        path.write_text(yaml.safe_dump({"sources": [record]}, sort_keys=False), encoding="utf-8")
        return path

    def test_unknown_source_id(self) -> None:
        errors = source_usage_errors(Path("lesson.md"), [{"source_id": "UNKNOWN", "mode": "reference"}], "## Sources and adaptation notes\nUNKNOWN", {})
        self.assertTrue(any("unknown source_id" in error for error in errors))

    def test_missing_source_version(self) -> None:
        _, errors = load_sources(self.write_registry(source_record(version_release_tag_or_commit="")))
        self.assertTrue(any("version_release_tag_or_commit" in error for error in errors))

    def test_missing_review_date(self) -> None:
        _, errors = load_sources(self.write_registry(source_record(reviewed_date="")))
        self.assertTrue(any("reviewed_date" in error for error in errors))

    def test_reference_only_cannot_be_adapted(self) -> None:
        record = source_record()
        errors = source_usage_errors(Path("lesson.md"), [{"source_id": "SOURCE-ONE", "mode": "adapted"}], "## Sources and adaptation notes\nSOURCE-ONE", {"SOURCE-ONE": record})
        self.assertTrue(any("reference-only" in error for error in errors))

    def test_visible_source_notes_are_required(self) -> None:
        record = source_record()
        errors = source_usage_errors(Path("lesson.md"), [{"source_id": "SOURCE-ONE", "mode": "reference"}], "No source section here.", {"SOURCE-ONE": record})
        self.assertTrue(any("absent or malformed" in error for error in errors))

    def test_source_id_only_note_is_rejected(self) -> None:
        record = source_record()
        body = "## Sources and adaptation notes\n- **SOURCE-ONE** — A source."
        errors = source_usage_errors(Path("lesson.md"), [{"source_id": "SOURCE-ONE", "mode": "reference"}], body, {"SOURCE-ONE": record})
        self.assertTrue(any("malformed" in error for error in errors))

    def test_visible_note_metadata_must_match_registry(self) -> None:
        record = source_record()
        body = (
            "## Sources and adaptation notes\n"
            "- **SOURCE-ONE** — [A source](https://example.com/source). Owner: Owner; "
            "revision: `reviewed-2026-07-21`; reuse: `adaptable-with-verification`; "
            "mode: `reference`. Informed: scope. Transformed: original example. Limitation: no copied text."
        )
        errors = source_usage_errors(Path("lesson.md"), [{"source_id": "SOURCE-ONE", "mode": "reference"}], body, {"SOURCE-ONE": record})
        self.assertTrue(any("visible reuse" in error for error in errors))

    def test_directory_destination_is_rejected(self) -> None:
        _, errors = load_sources(self.write_registry(source_record(destination_pages=["docs/learn"])))
        self.assertTrue(any("exact Markdown paths" in error for error in errors))

    def test_reverse_destination_mismatch_is_rejected(self) -> None:
        record = source_record(destination_pages=["docs/learn/ai-foundations.md"])
        errors = destination_alignment_errors(
            {"SOURCE-ONE": record},
            {"SOURCE-ONE": set()},
            {"docs/learn/ai-foundations.md"},
            Path("sources.yml"),
        )
        self.assertTrue(any("destinations differ" in error for error in errors))

    def test_extra_structured_visible_note_is_rejected(self) -> None:
        record = source_record()
        note = (
            "- **SOURCE-ONE** — [A source](https://example.com/source). Owner: Owner; "
            "revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. "
            "Informed: scope. Transformed: original example. Limitation: no copied text."
        )
        extra = note.replace("SOURCE-ONE", "SOURCE-TWO")
        errors = source_usage_errors(Path("lesson.md"), [{"source_id": "SOURCE-ONE", "mode": "reference"}], f"## Sources and adaptation notes\n{note}\n{extra}", {"SOURCE-ONE": record})
        self.assertTrue(any("not declared in source_usage" in error for error in errors))

    def test_duplicate_structured_visible_note_is_rejected(self) -> None:
        record = source_record()
        note = (
            "- **SOURCE-ONE** — [A source](https://example.com/source). Owner: Owner; "
            "revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. "
            "Informed: scope. Transformed: original example. Limitation: no copied text."
        )
        errors = source_usage_errors(Path("lesson.md"), [{"source_id": "SOURCE-ONE", "mode": "reference"}], f"## Sources and adaptation notes\n{note}\n{note}", {"SOURCE-ONE": record})
        self.assertTrue(any("duplicate visible source note" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
