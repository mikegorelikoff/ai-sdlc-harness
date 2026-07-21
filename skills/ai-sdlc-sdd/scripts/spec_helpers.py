#!/usr/bin/env python3
"""Shared helpers for AI SDLC SDD spec parsing and active-spec resolution.

The SDD scripts share this module so path resolution, Markdown parsing, and
traceability parsing stay consistent across status, clarify, checklist, analyze,
and validation gates.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_paths import first_existing, internal_dir


def workspace_root(script_path: Path = Path(__file__)) -> Path:
    """Return the consumer/source repository root for either distribution layout."""
    candidate = script_path.resolve().parents[3]
    return candidate.parent if candidate.name == ".agents" else candidate


ROOT = workspace_root()
FEATURE_SPEC_DIR_RE = re.compile(r"^\d{3}-")
ACCEPTANCE_ID_RE = re.compile(r"\bAC-\d{3}\b")
TEST_CASE_ID_RE = re.compile(r"\bTC-\d{3}\b")
TASK_LINE_RE = re.compile(r"^- \[[ xX]\]\s+((?:\d+|T\d{3}))(?:\.|\b)")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
COMPLETE_STAGE_STATUSES = {"done", "skipped", "not_applicable"}

SDD_ARTIFACT_SECTIONS = {
    "requirements": [
        "Goal",
        "Problem Statement",
        "Scope",
        "Actors",
        "Inputs",
        "Outputs",
        "Functional Requirements",
        "Non-Functional Requirements",
        "Constraints",
        "Acceptance Criteria",
        "Out of Scope",
        "Assumptions",
        "Open Questions",
        "Decision Status",
    ],
    "design": [
        "Overview",
        "Architecture",
        "Components",
        "Interfaces and Contracts",
        "Data Model",
        "Error Handling",
        "Security Considerations",
        "Observability",
        "Risks and Tradeoffs",
        "Validation Strategy",
        "Migration Notes",
    ],
    "test-cases": ["Scope", "Scenario Matrix", "Layer Mapping", "Automation Plan", "Open Gaps"],
    "qa": [
        "Change Summary",
        "Acceptance Scenarios",
        "Regression Targets",
        "Risk Notes",
        "Validation Commands",
        "Manual Checks",
        "Signoff",
    ],
    "tasks": ["Implementation", "Testing", "Documentation"],
}

SDD_ARTIFACT_TITLES = {
    "requirements": "Requirements",
    "design": "Design",
    "test-cases": "Test Cases",
    "qa": "QA",
    "tasks": "Tasks",
}


@dataclass(frozen=True)
class TaskEntry:
    """Parsed task row plus the metadata lines attached to it."""

    task_id: str
    line: str
    output: str | None
    refs: list[str]
    depends_on: list[str]


@dataclass(frozen=True)
class ResolveResult:
    """Resolved feature spec directory and the signal that selected it."""

    spec_dir: Path
    source: str


def unique(items: list[str]) -> list[str]:
    """Deduplicate strings while preserving first-seen order."""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def run_git(*args: str) -> str:
    """Run a git command from the repository root and return stdout."""
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
    """Return numbered feature spec directories under `specs/`."""
    specs_dir = root / "specs"
    if not specs_dir.is_dir():
        return []
    return sorted(path for path in specs_dir.iterdir() if path.is_dir() and FEATURE_SPEC_DIR_RE.match(path.name))


def is_feature_spec_name(name: str) -> bool:
    """Return true for numbered feature spec folder names like `123-feature`."""
    return bool(FEATURE_SPEC_DIR_RE.match(name))


def changed_files(root: Path = ROOT) -> list[str]:
    """Return changed and untracked paths for active-spec inference."""
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
    """Return the current git branch name, or raw git output on detached HEAD."""
    return run_git("rev-parse", "--abbrev-ref", "HEAD")


def feature_spec_dirs_from_files(files: list[str]) -> list[str]:
    """Extract feature spec folder names referenced by changed file paths."""
    spec_dirs: list[str] = []
    for file in files:
        parts = Path(file).parts
        if len(parts) >= 3 and parts[0] == "specs" and is_feature_spec_name(parts[1]):
            spec_dirs.append(parts[1])
    return unique(spec_dirs)


def normalize_spec_arg(spec: str | Path, root: Path = ROOT) -> Path:
    """Resolve explicit spec input as absolute, repo-relative, or `specs/<name>`."""
    spec_path = Path(spec)
    if spec_path.is_absolute():
        candidate = spec_path
    else:
        candidate = root / spec_path
        if not candidate.exists():
            candidate = root / "specs" / str(spec_path)
    return candidate


def resolve_from_explicit(spec: str | Path, root: Path = ROOT) -> ResolveResult:
    """Resolve a user-supplied spec path and fail if it is not a feature spec."""
    candidate = normalize_spec_arg(spec, root=root)
    if candidate.is_dir() and is_feature_spec_name(candidate.name):
        return ResolveResult(spec_dir=candidate, source="explicit")
    raise ValueError(f"explicit spec path does not resolve to a feature spec directory: {spec}")


def resolve_from_branch(branch: str, root: Path = ROOT) -> ResolveResult:
    """Resolve from branch name when it exactly contains one feature spec slug."""
    matches = [spec_dir for spec_dir in candidate_spec_dirs(root) if spec_dir.name == branch or spec_dir.name in branch]
    if len(matches) == 1:
        return ResolveResult(spec_dir=matches[0], source="branch")
    if len(matches) > 1:
        names = ", ".join(spec_dir.name for spec_dir in matches)
        raise ValueError(f"branch matches multiple feature specs: {names}")
    raise ValueError(f"branch does not match a feature spec: {branch}")


def resolve_from_files(files: list[str], root: Path = ROOT) -> ResolveResult:
    """Resolve from changed files when they reference exactly one spec folder."""
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
    """Resolve the active spec by explicit input, changed files, branch, then repo diff."""
    errors: list[str] = []
    # Explicit user input is authoritative and should not be overridden by branch
    # or changed-file heuristics.
    if explicit is not None:
        return resolve_from_explicit(explicit, root=root)

    if files:
        # Provided file lists are stronger than branch names, but ambiguity is
        # retained so the final error can explain every failed signal.
        try:
            return resolve_from_files(files, root=root)
        except ValueError as exc:
            errors.append(str(exc))

    branch_name = branch or current_branch(root)
    if branch_name and branch_name != "HEAD":
        # Branch inference is convenient for implementation work on feature
        # branches, but it must match one and only one spec.
        try:
            return resolve_from_branch(branch_name, root=root)
        except ValueError as exc:
            errors.append(str(exc))

    if files is None:
        # Last resort: inspect the current worktree for spec paths when no file
        # list was supplied by the caller.
        repo_files = changed_files(root)
        if repo_files:
            try:
                return resolve_from_files(repo_files, root=root)
            except ValueError as exc:
                errors.append(str(exc))

    detail = "; ".join(unique(errors)) if errors else "no explicit spec, changed-spec, or branch match"
    raise ValueError(f"could not resolve active feature spec: {detail}")


def headings(markdown: str) -> set[str]:
    """Return second-level Markdown headings used by SDD templates."""
    return {match.group(1).strip() for match in HEADING_RE.finditer(markdown)}


def markdown_body(markdown: str) -> str:
    """Return visible Markdown without generated YAML frontmatter."""
    if not markdown.startswith("---\n"):
        return markdown
    end = markdown.find("\n---", 4)
    if end == -1:
        return markdown
    return markdown[end + len("\n---") :].lstrip("\r\n")


def section_text(markdown: str, heading: str) -> str:
    """Return text inside a second-level Markdown section."""
    marker = f"## {heading}"
    if marker not in markdown:
        return ""
    after = markdown.split(marker, 1)[1]
    if "\n## " in after:
        after = after.split("\n## ", 1)[0]
    return after.strip()


def meaningful_lines(text: str) -> list[str]:
    """Return non-empty, non-heading lines for section content checks."""
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
    """Return true when a section contains at least one meaningful line."""
    return bool(meaningful_lines(section_text(markdown, heading)))


def parse_acceptance_ids(markdown: str) -> list[str]:
    """Extract AC IDs from the Acceptance Criteria section only."""
    return unique(ACCEPTANCE_ID_RE.findall(section_text(markdown, "Acceptance Criteria")))


def parse_test_case_ids(markdown: str) -> list[str]:
    """Extract TC IDs from any test-case artifact text."""
    return unique(TEST_CASE_ID_RE.findall(markdown))


def parse_test_case_acceptance_links(markdown: str) -> dict[str, list[str]]:
    """Map each test case to the acceptance IDs declared on its own row."""
    links: dict[str, list[str]] = {}
    for line in markdown.splitlines():
        ids = TEST_CASE_ID_RE.findall(line)
        if not ids:
            continue
        test_id = ids[0]
        acceptance = unique(ACCEPTANCE_ID_RE.findall(line))
        if acceptance:
            links[test_id] = acceptance
    return links


def plan_required_sections() -> list[str]:
    """Return canonical plan.md sections used by SDD gates."""
    return [
        "Upstream Refinement Sources",
        "SDD Artifact Links",
        "Cross-Artifact Trace Map",
        "Task Execution Plan",
        "Task Dependencies",
        "Validation Sequence",
        "Open Links And Blockers",
    ]


def parse_plan_toon_rows(text: str) -> dict[str, dict[str, str]]:
    """Parse plan.toon task rows keyed by task ID.

    The parser intentionally supports only the compact task table shape emitted
    by plan_links.py. Keeping it narrow makes gates deterministic and avoids
    spending tokens on free-form plan interpretation.
    """
    rows: dict[str, dict[str, str]] = {}
    in_tasks = False
    columns = ("id", "status", "refs", "tests", "depends_on", "artifact", "decision_ref")
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("tasks["):
            in_tasks = True
            continue
        if in_tasks and not line.startswith("  "):
            in_tasks = False
        if not in_tasks or not line.startswith("  "):
            continue
        parts = [part.strip() for part in line.strip().split(",")]
        parts.extend([""] * (len(columns) - len(parts)))
        row = {column: parts[index] for index, column in enumerate(columns)}
        if row.get("id"):
            rows[row["id"]] = row
    return rows


def completed_plan_task_ids(plan_toon: str) -> set[str]:
    """Return task IDs marked complete in plan.toon."""
    complete_statuses = {"done", "closed", "complete", "completed", "validated"}
    return {
        task_id
        for task_id, row in parse_plan_toon_rows(plan_toon).items()
        if row.get("status", "").lower() in complete_statuses
    }


def feature_slug_from_spec(spec_dir: Path, explicit_feature: str = "") -> str:
    """Infer the refinement feature slug from an implementation spec folder."""
    if explicit_feature and explicit_feature != "<feature-name>":
        return explicit_feature
    name = spec_dir.name
    if is_feature_spec_name(name):
        return name.split("-", 1)[1]
    return name


def parse_state_rows(text: str) -> list[dict[str, str]]:
    """Parse compact state.toon stage rows needed by SDD full-flow gates."""
    rows: list[dict[str, str]] = []
    in_stages = False
    columns = ("id", "skill", "status", "workspace", "artifacts", "decision_ref")
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("stages["):
            in_stages = True
            continue
        if line.startswith("skips["):
            in_stages = False
            continue
        if not in_stages or not line.startswith("  "):
            continue
        parts = [part.strip() for part in line.strip().split(",")]
        parts.extend([""] * (len(columns) - len(parts)))
        rows.append({column: parts[index] for index, column in enumerate(columns)})
    return rows


def upstream_refinement_errors(spec_dir: Path, explicit_feature: str = "") -> list[str]:
    """Return full-flow blockers when required upstream refinement is incomplete."""
    feature = feature_slug_from_spec(spec_dir, explicit_feature)
    local_refinement_root = spec_dir.parent / "specs-refiniment"
    refinement_root = local_refinement_root if local_refinement_root.is_dir() else ROOT / "specs-refiniment"
    refinement_dir = refinement_root / feature
    state_file = first_existing(
        internal_dir(refinement_dir) / "state.toon",
        refinement_dir / "state.toon",
    )
    errors: list[str] = []

    if not state_file.is_file():
        return [f"missing upstream refinement state for full flow: {state_file}"]

    rows = parse_state_rows(state_file.read_text(encoding="utf-8"))
    by_stage = {row.get("id", ""): row for row in rows}
    for stage_id in ("delivery_spec", "qa_traceability"):
        row = by_stage.get(stage_id)
        if not row:
            errors.append(f"upstream refinement state missing stage: {stage_id}")
            continue
        if row.get("status") not in COMPLETE_STAGE_STATUSES:
            errors.append(f"upstream refinement stage not complete for full flow: {stage_id}={row.get('status')}")
        if row.get("status") in {"skipped", "not_applicable"} and not row.get("decision_ref"):
            errors.append(f"upstream refinement skip missing decision_ref: {stage_id}")

    for artifact in ("delivery-spec.md", "qa-readiness.md"):
        if not (refinement_dir / artifact).is_file():
            errors.append(f"missing upstream refinement artifact for full flow: {refinement_dir / artifact}")
    return errors


def parse_task_entries(markdown: str) -> list[TaskEntry]:
    """Parse checkbox task rows and their following metadata lines."""
    tasks: list[TaskEntry] = []
    lines = markdown.splitlines()
    index = 0
    while index < len(lines):
        match = TASK_LINE_RE.match(lines[index])
        if not match:
            index += 1
            continue

        # A task owns the contiguous metadata lines until the next task or
        # section heading. This keeps the Markdown format simple and readable.
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
