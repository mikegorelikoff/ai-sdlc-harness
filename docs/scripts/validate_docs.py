#!/usr/bin/env python3
"""Validate MkDocs Material source, navigation, links, catalogs, and workflow."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlsplit

from build_catalog import DOCS, ROOT, generate


REQUIRED_META = {"title", "description"}
REQUIRED_FILES = {
    "mkdocs.yml",
    "requirements-docs.txt",
    "docs/assets/stylesheets/extra.css",
}
MODE_MINIMUMS = {"tutorials": 4, "how-to": 13, "explanation": 13, "reference": 10}
GENERATED_PAGES = {"reference/skills.md", "reference/modules.md"}
LEGACY_TOKENS = ("{%", "{{", "relative_url", "jekyll-build-pages", "layout: default")
FOUNDATION_PAGES = {
    "foundations/index.md",
    "foundations/ai-sdlc.md",
    "foundations/sdd.md",
    "foundations/why-harness.md",
    "foundations/mental-model.md",
    "foundations/responsibilities.md",
    "foundations/glossary.md",
    "onboarding/index.md",
    "onboarding/first-30-minutes.md",
}
BEGINNER_TERMS = (
    "software development lifecycle",
    "AI SDLC",
    "spec-driven development",
    "artifact",
    "evidence",
    "gate",
    "handoff",
)
CANONICAL_INSTALL = "npx -y skills@1.5.19 add mikegorelikoff/ai-sdlc-harness --all"


@dataclass(frozen=True)
class Page:
    path: Path
    metadata: dict[str, str]
    body: str


def display_path(path: Path, root: Path = ROOT) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def parse_frontmatter(path: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("unterminated YAML frontmatter")
    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        match = re.match(r"^([a-z_]+):\s*(.*?)\s*$", line)
        if match:
            metadata[match.group(1)] = match.group(2).strip('"\'')
    return Page(path=path, metadata=metadata, body=parts[2].strip())


def collect_pages(docs: Path = DOCS) -> tuple[list[Page], list[str]]:
    pages: list[Page] = []
    errors: list[str] = []
    for path in sorted(docs.rglob("*.md")):
        try:
            page = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"{display_path(path)}: {exc}")
            continue
        missing = sorted(REQUIRED_META - page.metadata.keys())
        if missing:
            errors.append(f"{display_path(path)}: missing frontmatter {', '.join(missing)}")
        pages.append(page)
    return pages, errors


def navigation_paths(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return re.findall(r"^\s*-\s+[^:#]+:\s+([A-Za-z0-9_./-]+\.md)\s*$", text, re.MULTILINE)


def internal_links(page: Page) -> set[str]:
    targets = set(re.findall(r"\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)", page.body))
    targets.update(re.findall(r"href=['\"]([^'\"]+)['\"]", page.body))
    return {
        target
        for target in targets
        if not target.startswith(("http://", "https://", "mailto:", "#"))
    }


def validate_links(pages: list[Page], docs: Path = DOCS) -> list[str]:
    errors: list[str] = []
    for page in pages:
        for target in sorted(internal_links(page)):
            parsed = urlsplit(target)
            path_text = unquote(parsed.path)
            if not path_text:
                continue
            if path_text.startswith("/"):
                errors.append(f"{display_path(page.path)}: root-absolute link bypasses site path: {target}")
                continue
            resolved = (page.path.parent / path_text).resolve()
            if path_text.endswith("/"):
                resolved /= "index.md"
            if resolved.suffix in {"", ".md"} and not resolved.exists():
                errors.append(f"{display_path(page.path)}: broken internal link {target}")
            elif resolved.suffix and resolved.suffix != ".md" and not resolved.exists():
                errors.append(f"{display_path(page.path)}: missing local asset {target}")
    return errors


def validate_navigation(pages: list[Page], docs: Path = DOCS, config: Optional[Path] = None) -> list[str]:
    errors: list[str] = []
    config = config or ROOT / "mkdocs.yml"
    nav_paths = navigation_paths(config)
    duplicate_nav = sorted({item for item in nav_paths if nav_paths.count(item) > 1})
    if duplicate_nav:
        errors.append("navigation has duplicate pages: " + ", ".join(duplicate_nav))
    public = [page.path.relative_to(docs).as_posix() for page in pages]
    if len(public) < 43:
        errors.append(f"public documentation depth is {len(public)} pages; expected at least 43")
    missing = sorted(set(public) - set(nav_paths))
    unknown = sorted(set(nav_paths) - set(public))
    if missing:
        errors.append("public pages missing from navigation: " + ", ".join(missing))
    if unknown:
        errors.append("navigation targets missing pages: " + ", ".join(unknown))
    for mode, minimum in MODE_MINIMUMS.items():
        count = len(list((docs / mode).glob("*.md")))
        if count < minimum:
            errors.append(f"{mode} contains {count} pages; expected at least {minimum}")
    return errors


def validate_content(pages: list[Page], docs: Path = DOCS) -> list[str]:
    errors: list[str] = []
    for page in pages:
        relative = page.path.relative_to(docs).as_posix()
        if relative == "index.md" or page.path.name == "index.md" or relative in GENERATED_PAGES:
            continue
        words = re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]+", re.sub(r"<[^>]+>", " ", page.body))
        if len(words) < 70:
            errors.append(f"{display_path(page.path)}: only {len(words)} content words; expected at least 70")
    return errors


def validate_onboarding(root: Path = ROOT) -> list[str]:
    """Validate the beginner-first entry path and canonical install contract."""
    errors: list[str] = []
    docs = root / "docs"
    missing = sorted(relative for relative in FOUNDATION_PAGES if not (docs / relative).is_file())
    if missing:
        errors.append("missing foundation/onboarding pages: " + ", ".join(missing))

    public_sources = [root / "README.md"] + sorted(docs.rglob("*.md"))
    for path in public_sources:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "scripts/install.sh" in text:
            errors.append(f"{display_path(path)}: references nonexistent scripts/install.sh")
        if "AI SDLC Skill Library" in text:
            errors.append(f"{display_path(path)}: uses non-canonical product name AI SDLC Skill Library")

    for relative in ("README.md", "docs/index.md", "docs/how-to/install.md"):
        path = root / relative
        if not path.is_file() or CANONICAL_INSTALL not in path.read_text(encoding="utf-8"):
            errors.append(f"{relative}: missing canonical project-scoped install command")

    foundations = "\n".join(
        (docs / relative).read_text(encoding="utf-8")
        for relative in sorted(FOUNDATION_PAGES)
        if (docs / relative).is_file()
    )
    lowered = foundations.lower()
    for term in BEGINNER_TERMS:
        if term.lower() not in lowered:
            errors.append(f"foundations missing beginner definition term: {term}")

    first_session = docs / "onboarding/first-30-minutes.md"
    if first_session.is_file():
        text = first_session.read_text(encoding="utf-8")
        for label in ("Tell your agent", "Run in terminal", "Agent does automatically", "Human checkpoint"):
            if label not in text:
                errors.append(f"docs/onboarding/first-30-minutes.md: missing action label {label}")
    return errors


def validate_material(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative in sorted(REQUIRED_FILES):
        if not (root / relative).exists():
            errors.append(f"{relative}: required site file missing")
    config = root / "mkdocs.yml"
    if config.exists():
        text = config.read_text(encoding="utf-8")
        tokens = (
            "name: material",
            "navigation.instant",
            "navigation.tabs",
            "navigation.indexes",
            "navigation.top",
            "search.suggest",
            "search.highlight",
            "content.code.copy",
            "scheme: default",
            "scheme: slate",
            "site_url: https://mikegorelikoff.github.io/ai-sdlc-harness/",
        )
        errors.extend(f"mkdocs.yml: missing Material contract {token}" for token in tokens if token not in text)
    sources = [root / "mkdocs.yml"] + sorted(DOCS.rglob("*.md"))
    for path in sources:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for token in LEGACY_TOKENS:
            if token in text:
                errors.append(f"{display_path(path)}: legacy Jekyll token remains: {token}")
    return errors


def validate_workflow(root: Path = ROOT) -> list[str]:
    path = root / ".github" / "workflows" / "pages.yml"
    if not path.exists():
        return [".github/workflows/pages.yml: missing Pages workflow"]
    text = path.read_text(encoding="utf-8")
    tokens = (
        "actions/checkout@v6",
        "actions/configure-pages@v5",
        "actions/setup-python@v6",
        "python3 -m pip install -r requirements-docs.txt",
        "mkdocs build --strict",
        "python3 docs/scripts/validate_rendered.py site",
        "actions/upload-pages-artifact@v4",
        "path: site",
        "actions/deploy-pages@v4",
        "pages: write",
        "id-token: write",
        "name: github-pages",
        "needs: build",
    )
    return [f"{path.relative_to(root)}: missing workflow contract {token}" for token in tokens if token not in text]


def validate(root: Path = ROOT) -> list[str]:
    docs = root / "docs"
    pages, errors = collect_pages(docs)
    errors.extend(validate_navigation(pages, docs, root / "mkdocs.yml"))
    errors.extend(validate_links(pages, docs))
    errors.extend(validate_content(pages, docs))
    errors.extend(validate_onboarding(root))
    errors.extend(validate_material(root))
    errors.extend(validate_workflow(root))
    return errors


def main() -> int:
    if generate(check=True):
        return 1
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    pages, _ = collect_pages()
    skill_count = len(list((ROOT / "skills").glob("*/SKILL.md")))
    module_count = len(list((ROOT / "modules").glob("*/module.json")))
    print(f"Documentation valid: {len(pages)} public pages, {skill_count} skills, {module_count} modules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
