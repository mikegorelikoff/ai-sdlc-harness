#!/usr/bin/env python3
"""Shared helpers for AI SDLC SDD spec parsing and active-spec resolution."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
FEATURE_SPEC_DIR_RE = re.compile(r"^\d{3}-")
ACCEPTANCE_ID_RE = re.compile(r"\bAC-\d{3}\b")
TEST_CASE_ID_RE = re.compile(r"\bTC-\d{3}\b")
TASK_LINE_RE = re.compile(r"^- \[[ xX]\]\s+((?:\d+|T\d{3}))(?:\.|\b)")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class TaskEntry:
    task_id: str
    line: str
    output: str | None
    refs: list[str]
    depends_on: list[str]


@dataclass(frozen=True)
class ResolveResult:
    spec_dir: Path
    source: str


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return result.stdout.strip()


def candidate_spec_dirs(root: Path = ROOT) -> list[Path]:
    specs_dir = root / "specs"
    if not specs_dir.is_dir():
        return []
    return sorted(path for path in specs_dir.iterdir() if path.is_dir() and FEATURE_SPEC_DIR_RE.match(path.name))


def is_feature_spec_name(name: str) -> bool:
    return bool(FEATURE_SPEC_DIR_RE.match(name))


def changed_files(root: Path = ROOT) -> list[str]:
    tracked = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return unique([line.strip() for line in tracked.stdout.splitlines() + untracked.stdout.splitlines() if line.strip()])


def current_branch(root: Path = ROOT) -> str:
    return run_git("rev-parse", "--abbrev-ref", "HEAD")


def feature_spec_dirs_from_files(files: list[str]) -> list[str]:
    spec_dirs: list[str] = []
    for file in files:
        parts = Path(file).parts
        if len(parts) >= 3 and parts[0] == "specs" and is_feature_spec_name(parts[1]):
            spec_dirs.append(parts[1])
    return unique(spec_dirs)


def normalize_spec_arg(spec: str | Path, root: Path = ROOT) -> Path:
    spec_path = Path(spec)
    if spec_path.is_absolute():
        candidate = spec_path
    else:
        candidate = root / spec_path
        if not candidate.exists():
            candidate = root / "specs" / str(spec_path)
    return candidate


def resolve_from_explicit(spec: str | Path, root: Path = ROOT) -> ResolveResult:
    candidate = normalize_spec_arg(spec, root=root)
    if candidate.is_dir() and is_feature_spec_name(candidate.name):
        return ResolveResult(spec_dir=candidate, source="explicit")
    raise ValueError(f"explicit spec path does not resolve to a feature spec directory: {spec}")


def resolve_from_branch(branch: str, root: Path = ROOT) -> ResolveResult:
    matches = [spec_dir for spec_dir in candidate_spec_dirs(root) if spec_dir.name == branch or spec_dir.name in branch]
    if len(matches) == 1:
        return ResolveResult(spec_dir=matches[0], source="branch")
    if len(matches) > 1:
        names = ", ".join(spec_dir.name for spec_dir in matches)
        raise ValueError(f"branch matches multiple feature specs: {names}")
    raise ValueError(f"branch does not match a feature spec: {branch}")


def resolve_from_files(files: list[str], root: Path = ROOT) -> ResolveResult:
    spec_dirs = feature_spec_dirs_from_files(files)
    if len(spec_dirs) == 1:
        return ResolveResult(spec_dir=root / "specs" / spec_dirs[0], source="changed-files")
    if len(spec_dirs) > 1:
        raise ValueError(f"changed files reference multiple feature specs: {', '.join(spec_dirs)}")
    raise ValueError("changed files do not reference a feature spec")


def resolve_active_spec(
    root: Path = ROOT,
    explicit: str | Path | None = None,
    files: list[str] | None = None,
    branch: str | None = None,
) -> ResolveResult:
    errors: list[str] = []
    if explicit is not None:
        return resolve_from_explicit(explicit, root=root)

    if files:
        try:
            return resolve_from_files(files, root=root)
        except ValueError as exc:
            errors.append(str(exc))

    branch_name = branch or current_branch(root)
    if branch_name and branch_name != "HEAD":
        try:
            return resolve_from_branch(branch_name, root=root)
        except ValueError as exc:
            errors.append(str(exc))

    if files is None:
        repo_files = changed_files(root)
        if repo_files:
            try:
                return resolve_from_files(repo_files, root=root)
            except ValueError as exc:
                errors.append(str(exc))

    detail = "; ".join(unique(errors)) if errors else "no explicit spec, changed-spec, or branch match"
    raise ValueError(f"could not resolve active feature spec: {detail}")


def headings(markdown: str) -> set[str]:
    return {match.group(1).strip() for match in HEADING_RE.finditer(markdown)}


def section_text(markdown: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in markdown:
        return ""
    after = markdown.split(marker, 1)[1]
    if "\n## " in after:
        after = after.split("\n## ", 1)[0]
    return after.strip()


def meaningful_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        lines.append(line)
    return lines


def section_has_meaningful_content(markdown: str, heading: str) -> bool:
    return bool(meaningful_lines(section_text(markdown, heading)))


def parse_acceptance_ids(markdown: str) -> list[str]:
    return unique(ACCEPTANCE_ID_RE.findall(section_text(markdown, "Acceptance Criteria")))


def parse_test_case_ids(markdown: str) -> list[str]:
    return unique(TEST_CASE_ID_RE.findall(markdown))


def parse_task_entries(markdown: str) -> list[TaskEntry]:
    tasks: list[TaskEntry] = []
    lines = markdown.splitlines()
    index = 0
    while index < len(lines):
        match = TASK_LINE_RE.match(lines[index])
        if not match:
            index += 1
            continue

        task_id = match.group(1)
        line = lines[index].strip()
        output: str | None = None
        refs: list[str] = []
        depends_on: list[str] = []
        index += 1

        while index < len(lines):
            current = lines[index].strip()
            if current.startswith("## "):
                break
            if TASK_LINE_RE.match(lines[index]):
                break
            if current.startswith("Output:"):
                output = current.split("Output:", 1)[1].strip()
            elif current.startswith("Refs:"):
                refs = [value.strip() for value in current.split("Refs:", 1)[1].split(",") if value.strip()]
            elif current.startswith("Depends on:"):
                depends_on = [value.strip() for value in current.split("Depends on:", 1)[1].split(",") if value.strip()]
            index += 1

        tasks.append(TaskEntry(task_id=task_id, line=line, output=output, refs=refs, depends_on=depends_on))
    return tasks
