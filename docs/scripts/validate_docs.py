#!/usr/bin/env python3
"""Validate GitHub Pages source, navigation, links, catalogs, and workflow."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from build_catalog import DOCS, ROOT, generate


REQUIRED_META = {"layout", "title", "description", "permalink", "nav_order"}
REQUIRED_FILES = {
    "_config.yml",
    "_data/navigation.yml",
    "_layouts/default.html",
    "_includes/header.html",
    "_includes/sidebar.html",
    "assets/css/style.scss",
    "assets/js/site.js",
}
MODE_MINIMUMS = {"tutorials": 4, "how-to": 13, "explanation": 13, "reference": 10}
GENERATED_CONTENT_ROUTES = {"/reference/skills/", "/reference/modules/"}


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
    sources = sorted(docs.rglob("*.md")) + [docs / "404.html"]
    for path in sources:
        if not path.exists():
            continue
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


def navigation_urls(path: Path) -> list[str]:
    urls = re.findall(r"^\s*url:\s*([^\s#]+)\s*$", path.read_text(encoding="utf-8"), re.MULTILINE)
    return [value.strip('"\'') for value in urls]


def internal_links(page: Page) -> set[str]:
    links: set[str] = set()
    liquid = re.findall(r"(?:href=[\"']|\]\()\{\{\s*[\"'](/[^\"']+)[\"']\s*\|\s*relative_url\s*\}\}", page.body)
    links.update(liquid)
    for target in re.findall(r"(?:href=[\"']|\]\()(/[^\"')\s]+)", page.body):
        links.add(target)
    return links


def validate_links(pages: list[Page]) -> list[str]:
    errors: list[str] = []
    permalinks = {page.metadata.get("permalink") for page in pages}
    for page in pages:
        for target in sorted(internal_links(page)):
            route = target.split("#", 1)[0]
            if route and route not in permalinks:
                errors.append(f"{display_path(page.path)}: broken internal link {target}")
    return errors


def validate_navigation(pages: list[Page], docs: Path = DOCS) -> list[str]:
    errors: list[str] = []
    urls = navigation_urls(docs / "_data" / "navigation.yml")
    duplicate_urls = sorted({url for url in urls if urls.count(url) > 1})
    if duplicate_urls:
        errors.append("navigation has duplicate URLs: " + ", ".join(duplicate_urls))
    public = [page.metadata.get("permalink") for page in pages if page.metadata.get("permalink") != "/404.html"]
    if len(public) < 38:
        errors.append(f"public documentation depth is {len(public)} pages; expected at least 38")
    duplicate_pages = sorted({url for url in public if public.count(url) > 1})
    if duplicate_pages:
        errors.append("multiple pages claim the same permalink: " + ", ".join(duplicate_pages))
    missing = sorted(set(public) - set(urls))
    unknown = sorted(set(urls) - set(public))
    if missing:
        errors.append("public pages missing from navigation: " + ", ".join(missing))
    if unknown:
        errors.append("navigation targets missing pages: " + ", ".join(unknown))
    for mode, minimum in MODE_MINIMUMS.items():
        count = len(list((docs / mode).glob("*.md")))
        if count < minimum:
            errors.append(f"{mode} contains {count} pages; expected at least {minimum}")
    return errors


def validate_content(pages: list[Page]) -> list[str]:
    errors: list[str] = []
    for page in pages:
        route = page.metadata.get("permalink", "")
        if route in {"/", "/404.html"} | GENERATED_CONTENT_ROUTES or route.endswith("/index/"):
            continue
        if page.path.name == "index.md":
            continue
        words = re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]+", re.sub(r"<[^>]+>", " ", page.body))
        if len(words) < 70:
            errors.append(f"{display_path(page.path)}: only {len(words)} content words; expected at least 70")
    return errors


def validate_shell(docs: Path = DOCS, pages: Optional[list[Page]] = None) -> list[str]:
    errors: list[str] = []
    for relative in sorted(REQUIRED_FILES):
        if not (docs / relative).exists():
            errors.append(f"docs/{relative}: required site file missing")
    shell_sources = [
        path
        for path in docs.rglob("*")
        if path.is_file()
        and path.suffix in {".md", ".html", ".scss", ".js"}
        and "scripts" not in path.parts
        and "tests" not in path.parts
    ]
    joined = "\n".join(path.read_text(encoding="utf-8") for path in shell_sources)
    for token in ("skip-link", "menu-toggle", "page-outline", "prefers-reduced-motion", "relative_url"):
        if token not in joined:
            errors.append(f"site shell missing contract token: {token}")
    root_absolute = re.findall(r"(?:href|src)=[\"']/[^\"']*", joined)
    if root_absolute:
        errors.append("root-absolute asset/link paths bypass baseurl: " + ", ".join(sorted(set(root_absolute))[:5]))
    if pages is not None:
        permalinks = {page.metadata.get("permalink") for page in pages}
        shell = Page(docs / "_layouts/default.html", {}, joined)
        for target in sorted(internal_links(shell)):
            route = target.split("#", 1)[0]
            if route and route not in permalinks and not route.startswith("/assets/"):
                errors.append(f"shared shell has broken internal link {target}")
    return errors


def validate_workflow(root: Path = ROOT) -> list[str]:
    path = root / ".github" / "workflows" / "pages.yml"
    if not path.exists():
        return [".github/workflows/pages.yml: missing Pages workflow"]
    text = path.read_text(encoding="utf-8")
    tokens = (
        "actions/checkout@v6",
        "actions/configure-pages@v5",
        "actions/jekyll-build-pages@v1",
        "actions/upload-pages-artifact@v4",
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
    errors.extend(validate_navigation(pages, docs))
    errors.extend(validate_links(pages))
    errors.extend(validate_content(pages))
    errors.extend(validate_shell(docs, pages))
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
    print(f"Documentation valid: {len(pages) - 1} public pages, 35 skills, 5 modules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
