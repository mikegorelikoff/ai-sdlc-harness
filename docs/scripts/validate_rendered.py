#!/usr/bin/env python3
"""Validate links, assets, search, and Material contracts in built documentation."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Targets(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        wanted = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else None
        if wanted is None:
            return
        for name, value in attrs:
            if name == wanted and value:
                self.values.append(value)


def target_path(source: Path, target: str, site: Path) -> Path | None:
    if target.startswith(("http://", "https://", "mailto:", "javascript:", "data:", "#")):
        return None
    path_text = unquote(urlsplit(target).path)
    if not path_text:
        return None
    site_prefix = "/ai-sdlc-harness/"
    if path_text.startswith(site_prefix):
        candidate = (site / path_text.removeprefix(site_prefix)).resolve()
    elif path_text.startswith("/"):
        return site / "__invalid_root_absolute_target__"
    else:
        candidate = (source.parent / path_text).resolve()
    if path_text.endswith("/") or candidate.is_dir():
        candidate /= "index.html"
    return candidate


def validate(site: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    html_files = sorted(site.rglob("*.html"))
    if len(html_files) < 44:
        errors.append(f"rendered page count is {len(html_files)}; expected at least 44 including 404")
    checked = 0
    for source in html_files:
        parser = Targets()
        parser.feed(source.read_text(encoding="utf-8"))
        for target in parser.values:
            resolved = target_path(source, target, site)
            if resolved is None:
                continue
            checked += 1
            if not resolved.exists():
                errors.append(f"{source.relative_to(site)}: broken rendered target {target}")
    index = site / "index.html"
    if index.exists():
        text = index.read_text(encoding="utf-8")
        for token in (
            "mkdocs-material-9.7.7",
            'data-md-component="search"',
            'data-md-color-scheme="default"',
            'id="the-problem-in-one-minute"',
            'id="choose-your-path"',
        ):
            if token not in text:
                errors.append(f"index.html: missing rendered Material contract {token}")
        if 'class="hero"' in text:
            errors.append("index.html: removed homepage hero block is still rendered")
    for relative in ("search/search_index.json", "assets/stylesheets/extra.css"):
        if not (site / relative).exists():
            errors.append(f"rendered asset missing: {relative}")
    return errors, checked


def main() -> int:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()
    if not site.is_dir():
        print(f"ERROR: rendered site directory missing: {site}")
        return 1
    errors, checked = validate(site)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Rendered site valid: {len(list(site.rglob('*.html')))} HTML pages, {checked} local targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
