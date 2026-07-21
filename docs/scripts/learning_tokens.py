#!/usr/bin/env python3
"""Measure and validate Markdown pages listed under the visible Learn navigation."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import tiktoken
import yaml


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class TokenResult:
    """One normalized Learn page and its measured token count."""

    path: str
    count: int


def load_config(path: Path) -> dict[str, Any]:
    """Load a MkDocs YAML file and require a mapping at the document root."""
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: malformed UTF-8") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path}: configuration root must be a mapping")
    return value


def _markdown_paths(value: Any) -> Iterable[str]:
    if isinstance(value, str) and value.endswith(".md"):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _markdown_paths(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _markdown_paths(item)


def learn_navigation(config_path: Path) -> list[str]:
    """Return the recursively ordered Markdown inventory under visible Learn."""
    config = load_config(config_path)
    nav = config.get("nav")
    if not isinstance(nav, list):
        raise ValueError(f"{config_path}: nav must be a list")
    matches = [item["Learn"] for item in nav if isinstance(item, dict) and "Learn" in item]
    if len(matches) != 1:
        raise ValueError(f"{config_path}: expected exactly one visible Learn navigation section")
    paths = list(_markdown_paths(matches[0]))
    duplicates = sorted({path for path in paths if paths.count(path) > 1})
    if duplicates:
        raise ValueError(f"{config_path}: duplicated Learn pages: {', '.join(duplicates)}")
    if not paths:
        raise ValueError(f"{config_path}: Learn navigation contains no Markdown pages")
    return paths


def normalize_markdown_bytes(raw: bytes, path: str = "<memory>") -> str:
    """Apply the project token-measurement normalization contract."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: malformed UTF-8") from exc
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.startswith("---\n"):
        lines = text.splitlines(keepends=True)
        closing = next((index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
        if closing is None:
            raise ValueError(f"{path}: unterminated YAML front matter")
        text = "".join(lines[closing + 1 :])
    return _remove_maintainer_comments(text)


def _remove_maintainer_comments(text: str) -> str:
    """Remove HTML comments outside fenced code while preserving rendered examples."""
    output: list[str] = []
    in_comment = False
    fence: tuple[str, int] | None = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^[ \t]{0,3}(`{3,}|~{3,})", line)
        if not in_comment and marker:
            candidate = marker.group(1)
            if fence is None:
                fence = (candidate[0], len(candidate))
            elif candidate[0] == fence[0] and len(candidate) >= fence[1]:
                fence = None
            output.append(line)
            continue
        if fence is not None:
            output.append(line)
            continue

        position = 0
        visible: list[str] = []
        while position < len(line):
            if in_comment:
                end = line.find("-->", position)
                if end < 0:
                    position = len(line)
                    continue
                in_comment = False
                position = end + 3
                continue
            start = line.find("<!--", position)
            if start < 0:
                visible.append(line[position:])
                break
            visible.append(line[position:start])
            in_comment = True
            position = start + 4
        output.append("".join(visible))
    return "".join(output)


def count_markdown_bytes(raw: bytes, encoding_name: str = "o200k_base", path: str = "<memory>") -> int:
    """Return the exact token count for normalized Markdown bytes."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(normalize_markdown_bytes(raw, path)))


def count_is_valid(count: int, minimum: int, maximum: int) -> bool:
    """Return whether an already measured count is within inclusive bounds."""
    return minimum <= count <= maximum


def measure_learn_pages(
    config_path: Path,
    encoding_name: str = "o200k_base",
    docs_dir: Path | None = None,
) -> list[TokenResult]:
    """Measure every Learn page, rejecting missing files and malformed input."""
    docs_dir = docs_dir or config_path.parent / "docs"
    results: list[TokenResult] = []
    for relative in learn_navigation(config_path):
        page = docs_dir / relative
        if not page.is_file():
            raise ValueError(f"{config_path}: missing Learn page: {relative}")
        results.append(
            TokenResult(
                relative,
                count_markdown_bytes(page.read_bytes(), encoding_name, page.as_posix()),
            )
        )
    return results


def validate_learn_tokens(
    config_path: Path,
    encoding_name: str = "o200k_base",
    minimum: int = 6000,
    maximum: int = 8000,
    docs_dir: Path | None = None,
) -> tuple[list[TokenResult], list[str]]:
    """Measure Learn pages and return exact, file-scoped range failures."""
    try:
        results = measure_learn_pages(config_path, encoding_name, docs_dir)
    except ValueError as exc:
        return [], [str(exc)]
    errors = [
        f"docs/{item.path}: {item.count} {encoding_name} tokens; required {minimum}-{maximum} inclusive"
        for item in results
        if not count_is_valid(item.count, minimum, maximum)
    ]
    return results, errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "mkdocs.yml")
    parser.add_argument("--encoding", default="o200k_base")
    parser.add_argument("--minimum", type=int, default=6000)
    parser.add_argument("--maximum", type=int, default=8000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.minimum < 0 or args.maximum < args.minimum:
        print("ERROR: token bounds must satisfy 0 <= minimum <= maximum")
        return 2
    results, errors = validate_learn_tokens(args.config, args.encoding, args.minimum, args.maximum)
    print(f"Learn token report ({args.encoding}; required {args.minimum}-{args.maximum} inclusive)")
    for item in results:
        status = "PASS" if count_is_valid(item.count, args.minimum, args.maximum) else "FAIL"
        print(f"{status:4} {item.count:5}  docs/{item.path}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
