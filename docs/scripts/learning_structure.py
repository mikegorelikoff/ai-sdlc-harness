#!/usr/bin/env python3
"""Validate Learn page contracts, source provenance, ordering, and anchors."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml

from learning_tokens import learn_navigation, load_config


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
SOURCE_REGISTRY = DOCS / "_data" / "content_sources.yml"
REQUIRED_META = {
    "title",
    "description",
    "learning_level",
    "audience",
    "estimated_time",
    "prerequisites",
    "content_type",
    "last_reviewed",
    "source_usage",
}
SOURCE_FIELDS = {
    "source_id",
    "title",
    "publisher_or_owner",
    "canonical_url",
    "source_type",
    "version_release_tag_or_commit",
    "reviewed_date",
    "verified_license",
    "license_url",
    "reuse_class",
    "material_consulted",
    "adopted_concepts",
    "excluded_material",
    "destination_pages",
    "adaptation_summary",
    "attribution_requirement",
    "reviewer",
    "review_status",
}
SOURCE_MODES = {"original", "synthesized", "adapted", "quoted", "reference"}
REUSE_CLASSES = {
    "internal-authority",
    "adaptable-with-verification",
    "reference-only",
    "unavailable-or-unclear",
}
REQUIRED_VISIBLE = (
    "## At a glance",
    "**Level:**",
    "**Audience:**",
    "**Estimated time:**",
    "**Prerequisites:**",
    "## Expected outcome",
    "## What experienced readers may skip",
    "## Why this matters",
    "## On this page",
    "## Observable learning objectives",
    "Can explain",
    "Can do",
    "Can prove",
    "## Core concepts",
    "## Important distinctions",
    "Worked example",
    "Weak example",
    "Corrected example",
    "## Harness connection",
    "## Role perspectives",
    "## Practice exercise",
    "### Permitted actions",
    "### Prohibited actions",
    "## Check your understanding",
    "<details>",
    "## Common failure modes",
    "## Recovery guidance",
    "## Evidence of completion",
    "## Mid-page recap",
    "## Completion checklist",
    "## Previous learning step",
    "## Next learning step",
    "## Sources and adaptation notes",
)
EXPECTED_LEVELS = {
    "start.md": 0,
    "learn/ai-foundations.md": 0,
    "learn/prompt-engineering.md": 1,
    "learn/context-and-verification.md": 1,
    "learn/agents-tools-and-subagents.md": 2,
    "learn/multi-role-review.md": 2,
    "learn/ai-sdlc-and-sdd.md": 3,
    "learn/harness-essentials.md": 4,
    "learn/guided-practice.md": 5,
    "learn/role-learning-paths.md": 6,
}
ROLE_ANCHORS = (
    "pm-or-po",
    "business-analyst",
    "qa",
    "developer",
    "architecture-and-security",
    "delivery-and-vp",
    "head-of-ai-practice",
    "harness-maintainer",
)
REQUIRED_FIXTURES = (
    "assets/learning-fixtures/verification-evidence.txt",
    "assets/learning-fixtures/delegation-link-scope.txt",
    "assets/learning-fixtures/multi-role-review-snapshot.txt",
    "assets/learning-fixtures/multi-role-curriculum-draft.txt",
    "assets/learning-fixtures/stale-evidence-recovery.txt",
    "assets/learning-fixtures/conflicting-artifacts.txt",
    "assets/learning-fixtures/subscription-pause-source-pack.txt",
    "assets/learning-fixtures/first-30-minutes-consumer.txt",
    "assets/learning-fixtures/existing-project-adoption-pack.txt",
)
SOURCE_NOTE_RE = re.compile(
    r"^- \*\*(?P<source_id>[^*]+)\*\* — \[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)\. "
    r"Owner: (?P<owner>.*?); revision: `(?P<revision>[^`]+)`; "
    r"reuse: `(?P<reuse>[^`]+)`; mode: `(?P<mode>[^`]+)`\. "
    r"Informed: (?P<informed>.+?) Transformed: (?P<transformed>.+?) Limitation: (?P<limitation>.+)$"
)


def learning_order_errors(paths: list[str], levels: list[int]) -> list[str]:
    """Validate the canonical Learn inventory and nondecreasing level order."""
    errors: list[str] = []
    if paths != list(EXPECTED_LEVELS):
        errors.append("Learn page order or inventory differs from the canonical ten-page curriculum")
    expected = [EXPECTED_LEVELS[path] for path in paths if path in EXPECTED_LEVELS]
    if levels != expected or levels != sorted(levels):
        errors.append("Learn learning levels are missing or not in the intended order")
    return errors


def missing_role_anchors(text: str) -> list[str]:
    """Return required role-path anchors absent from a Learn role page."""
    heading_anchors = {
        heading_slug(match.group(1))
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    }
    return [
        anchor
        for anchor in ROLE_ANCHORS
        if f'id="{anchor}"' not in text and anchor not in heading_anchors
    ]


def read_markdown(path: Path) -> tuple[dict[str, Any], str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: malformed UTF-8") from exc
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML front matter")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError(f"{path}: unterminated YAML front matter")
    meta = yaml.safe_load(parts[0][4:])
    if not isinstance(meta, dict):
        raise ValueError(f"{path}: front matter must be a mapping")
    return meta, parts[1]


def heading_slug(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value).strip().lower()
    value = re.sub(r"[`*_]", "", value)
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def heading_errors(path: Path, body: str) -> list[str]:
    errors: list[str] = []
    prior = 0
    for line_number, line in enumerate(body.splitlines(), start=1):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        level = len(match.group(1))
        if prior and level > prior + 1:
            errors.append(f"{path}: line {line_number} skips heading level H{prior} to H{level}")
        prior = level
    return errors


def load_sources(path: Path = SOURCE_REGISTRY) -> tuple[dict[str, dict[str, Any]], list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return {}, [f"{path}: missing content source registry"]
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    records = value.get("sources") if isinstance(value, dict) else None
    if not isinstance(records, list):
        return {}, [f"{path}: sources must be a list"]
    indexed: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        label = f"{path}: source record {index + 1}"
        if not isinstance(record, dict):
            errors.append(f"{label} must be a mapping")
            continue
        missing = sorted(field for field in SOURCE_FIELDS if field not in record or record[field] in (None, "", []))
        if missing:
            errors.append(f"{label} missing fields: {', '.join(missing)}")
        source_id = record.get("source_id")
        if not isinstance(source_id, str):
            continue
        if source_id in indexed:
            errors.append(f"{path}: duplicate source_id {source_id}")
        indexed[source_id] = record
        reuse = record.get("reuse_class")
        if reuse not in REUSE_CLASSES:
            errors.append(f"{label} has invalid reuse_class {reuse!r}")
        if reuse == "unavailable-or-unclear" and record.get("destination_pages"):
            errors.append(f"{label} unavailable source cannot have destination pages")
        if record.get("source_type") == "git-repository":
            revision = str(record.get("version_release_tag_or_commit", ""))
            if not re.fullmatch(r"[0-9a-f]{40}|v?\d[^\s]*", revision):
                errors.append(f"{label} Git source is not pinned to a commit, release, or tag")
        destinations = record.get("destination_pages", [])
        if isinstance(destinations, list):
            for destination in destinations:
                if not isinstance(destination, str) or not destination.endswith(".md"):
                    errors.append(f"{label} destination_pages must contain exact Markdown paths, not {destination!r}")
    return indexed, errors


def _links(body: str) -> list[str]:
    return re.findall(r"\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)", body)


def source_usage_errors(
    path: Path,
    usage: Any,
    body: str,
    sources: dict[str, dict[str, Any]],
) -> list[str]:
    """Validate one page source declaration against the registry."""
    errors: list[str] = []
    if not isinstance(usage, list) or not usage:
        return [f"{path}: source_usage must be a non-empty list"]
    if "## Sources and adaptation notes" not in body:
        notes = ""
    else:
        notes = body.split("## Sources and adaptation notes", 1)[1]
    parsed_notes: dict[str, dict[str, str]] = {}
    for line in notes.splitlines():
        match = SOURCE_NOTE_RE.fullmatch(line.strip())
        if not match:
            continue
        source_id = match.group("source_id")
        if source_id in parsed_notes:
            errors.append(f"{path}: duplicate visible source note {source_id}")
        parsed_notes[source_id] = match.groupdict()
    declared_ids: set[str] = set()
    for item in usage:
        if not isinstance(item, dict) or set(item) != {"source_id", "mode"}:
            errors.append(f"{path}: each source_usage item must contain only source_id and mode")
            continue
        source_id, mode = item["source_id"], item["mode"]
        declared_ids.add(source_id)
        if mode not in SOURCE_MODES:
            errors.append(f"{path}: invalid source mode {mode!r}")
        record = sources.get(source_id)
        if record is None:
            errors.append(f"{path}: unknown source_id {source_id}")
        elif record.get("reuse_class") == "reference-only" and mode in {"adapted", "quoted"}:
            errors.append(f"{path}: reference-only source {source_id} cannot use mode {mode}")
        elif record.get("reuse_class") == "unavailable-or-unclear":
            errors.append(f"{path}: unavailable source {source_id} cannot be used")
        note = parsed_notes.get(source_id)
        if note is None:
            errors.append(f"{path}: source {source_id} is absent or malformed in visible adaptation notes")
        elif record is not None:
            expected = {
                "title": str(record.get("title")),
                "url": str(record.get("canonical_url")),
                "owner": str(record.get("publisher_or_owner")),
                "revision": str(record.get("version_release_tag_or_commit")),
                "reuse": str(record.get("reuse_class")),
                "mode": str(mode),
            }
            for field, value in expected.items():
                if note.get(field) != value:
                    errors.append(
                        f"{path}: source {source_id} visible {field} {note.get(field)!r} does not match {value!r}"
                    )
    extras = sorted(set(parsed_notes) - declared_ids)
    if extras:
        errors.append(f"{path}: visible source notes are not declared in source_usage: {', '.join(extras)}")
    return errors


def destination_alignment_errors(
    sources: dict[str, dict[str, Any]],
    usage_by_source: dict[str, set[str]],
    learn_set: set[str],
    registry_path: Path = SOURCE_REGISTRY,
) -> list[str]:
    """Require exact bidirectional agreement for source use on Learn pages."""
    errors: list[str] = []
    for source_id, record in sources.items():
        registered = {value for value in record.get("destination_pages", []) if value in learn_set}
        actual = usage_by_source.get(source_id, set())
        if registered != actual:
            errors.append(
                f"{registry_path}: source {source_id} Learn destinations differ; "
                f"registered={sorted(registered)!r}, declared={sorted(actual)!r}"
            )
    return errors


def anchor_errors(path: Path, body: str, docs: Path = DOCS) -> list[str]:
    errors: list[str] = []
    for target in _links(body):
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith(("mailto:", "#")) or not parsed.fragment:
            if target.startswith("#"):
                target_path = path
                fragment = target[1:]
            else:
                continue
        else:
            target_path = (path.parent / unquote(parsed.path)).resolve()
            fragment = unquote(parsed.fragment)
        if not target_path.is_file() or target_path.suffix != ".md":
            continue
        try:
            _, target_body = read_markdown(target_path)
        except ValueError:
            continue
        anchors = {heading_slug(match.group(1)) for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", target_body, re.MULTILINE)}
        anchors.update(re.findall(r"<a\s+(?:[^>]*?\s)?id=['\"]([^'\"]+)['\"]", target_body))
        if fragment not in anchors:
            errors.append(f"{path}: unresolved heading anchor {target}")
    return errors


def validate_learning_structure(root: Path = ROOT) -> list[str]:
    config_path = root / "mkdocs.yml"
    docs = root / "docs"
    errors: list[str] = []
    try:
        config = load_config(config_path)
        top_level = [next(iter(item)) for item in config.get("nav", []) if isinstance(item, dict) and item]
        if top_level != ["Home", "Learn", "Reference", "Use", "Adopt", "About"]:
            errors.append(f"{config_path}: top-level navigation must be Home, Learn, Reference, Use, Adopt, About")
    except ValueError as exc:
        errors.append(str(exc))
    try:
        paths = learn_navigation(config_path)
    except ValueError as exc:
        return [str(exc)]
    order_errors = learning_order_errors(paths, [EXPECTED_LEVELS[path] for path in paths if path in EXPECTED_LEVELS])
    errors.extend(f"{config_path}: {error}" for error in order_errors)
    sources, source_errors = load_sources(docs / "_data" / "content_sources.yml")
    errors.extend(source_errors)
    levels: list[int] = []
    usage_by_source: dict[str, set[str]] = {source_id: set() for source_id in sources}
    summary_owners: dict[str, Path] = {}
    for relative in paths:
        path = docs / relative
        if not path.is_file():
            errors.append(f"{config_path}: missing Learn page {relative}")
            continue
        try:
            meta, body = read_markdown(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        missing_meta = sorted(REQUIRED_META - meta.keys())
        if missing_meta:
            errors.append(f"{path}: missing Learn front matter: {', '.join(missing_meta)}")
        level = meta.get("learning_level")
        if level != EXPECTED_LEVELS.get(relative):
            errors.append(f"{path}: learning_level {level!r} does not match expected {EXPECTED_LEVELS.get(relative)!r}")
        if isinstance(level, int):
            levels.append(level)
        if meta.get("content_type") not in {"lesson", "lab", "learning_hub", "role_paths"}:
            errors.append(f"{path}: invalid Learn content_type {meta.get('content_type')!r}")
        for token in REQUIRED_VISIBLE:
            if token not in body:
                errors.append(f"{path}: missing Learn page contract marker {token!r}")
        if body.count("Worked example") < 2:
            errors.append(f"{path}: requires at least two original worked examples")
        for summary in re.findall(r"<summary>([^<]+)</summary>", body):
            prior_owner = summary_owners.get(summary)
            if prior_owner is not None:
                errors.append(f"{path}: duplicate collapsible summary {summary!r} also used in {prior_owner}")
            summary_owners[summary] = path
        errors.extend(source_usage_errors(path, meta.get("source_usage"), body, sources))
        for item in meta.get("source_usage", []) if isinstance(meta.get("source_usage"), list) else []:
            if not isinstance(item, dict) or item.get("source_id") not in sources:
                continue
            destinations = sources[item["source_id"]].get("destination_pages", [])
            expected = f"docs/{relative}"
            usage_by_source[item["source_id"]].add(expected)
            if expected not in destinations:
                errors.append(f"{path}: source {item['source_id']} registry destinations do not include this page")
        errors.extend(heading_errors(path, body))
        errors.extend(anchor_errors(path, body, docs))
    level_errors = learning_order_errors(paths, levels)
    errors.extend(f"{config_path}: {error}" for error in level_errors if "levels" in error)
    hub = docs / "start.md"
    hub_text = hub.read_text(encoding="utf-8") if hub.is_file() else ""
    for relative in paths[1:]:
        if relative not in hub_text:
            errors.append(f"{hub}: learning hub does not link to {relative}")
    roles = docs / "learn" / "role-learning-paths.md"
    role_text = roles.read_text(encoding="utf-8") if roles.is_file() else ""
    for anchor in missing_role_anchors(role_text):
        errors.append(f"{roles}: missing bookmarkable role path {anchor}")
    if "../reference/skills-by-role.md" not in role_text:
        errors.append(f"{roles}: missing canonical skills-by-role link")
    learn_set = {f"docs/{relative}" for relative in paths}
    errors.extend(destination_alignment_errors(sources, usage_by_source, learn_set))
    for fixture in REQUIRED_FIXTURES:
        if not (docs / fixture).is_file():
            errors.append(f"{docs / fixture}: missing required Learn exercise fixture")
    return errors
