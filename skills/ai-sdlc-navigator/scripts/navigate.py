#!/usr/bin/env python3
"""Recommend the next evidence-backed AI SDLC action for a repository."""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


COMPLETE_STATUSES = {"done", "skipped", "not_applicable"}
DEFAULT_BASE_BRANCHES = {"dev", "main", "master"}


@dataclass(frozen=True)
class Action:
    """One required or optional navigator recommendation."""

    skill: str
    reason: str
    command: str
    expected_artifact: str


@dataclass(frozen=True)
class FeatureState:
    """One discovered feature state record."""

    feature: str
    workspace: str
    path: Path
    state: dict[str, object]


def load_state(path: Path) -> dict[str, object]:
    """Parse the portable subset of feature state TOON used for navigation."""
    state: dict[str, object] = {"stages": []}
    in_stages = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("stages["):
            in_stages = True
            continue
        if line.startswith("skips["):
            in_stages = False
            continue
        if in_stages and line.startswith("  "):
            values = [value.strip() for value in line.strip().split(",")]
            values.extend([""] * (6 - len(values)))
            state["stages"].append(dict(zip(("id", "skill", "status", "workspace", "artifacts", "decision_ref"), values)))  # type: ignore[union-attr]
            continue
        if not line.startswith("  ") and ":" in line:
            key, value = line.split(":", 1)
            state[key.strip()] = value.strip()
    return state


INTENT_ROUTES: tuple[tuple[tuple[str, ...], Action], ...] = (
    (("commit", "stage changes"), Action("ai-sdlc-commit-prep", "The intent asks to prepare or create a commit.", "Use $ai-sdlc-commit-prep for the current change.", "commit")),
    (("security", "owasp", "authz", "abuse case"), Action("ai-sdlc-security-testing", "The intent is security-focused.", "Use $ai-sdlc-security-testing for the target surface.", "security-review.md")),
    (("code review", "review diff", "review pr"), Action("ai-sdlc-code-review", "The intent asks for implementation review.", "Use $ai-sdlc-code-review for the current diff.", "code-review.md")),
    (("test", "qa", "regression"), Action("ai-sdlc-qa-requirements-gap-review", "The intent is primarily about testability or QA coverage.", "Use $ai-sdlc-qa-requirements-gap-review for the relevant artifacts.", "qa-gap-review.md")),
    (("story", "backlog", "epic"), Action("ai-sdlc-user-story-decomposition", "The intent asks to decompose delivery scope.", "Use $ai-sdlc-user-story-decomposition for the feature.", "user-stories.md")),
    (("idea", "customer problem", "product", "discover"), Action("ai-sdlc-working-backwards-discovery", "The intent begins with an idea or customer problem.", "Use $ai-sdlc-working-backwards-discovery for the initiative.", "discovery.md")),
    (("bug", "fix", "implement", "refactor", "api", "architecture"), Action("ai-sdlc-sdd", "The intent requests a repository implementation or design change.", "Use $ai-sdlc-sdd to classify and specify the change.", "specs/<feature>")),
)


def git_output(root: Path, *args: str) -> str:
    """Return best-effort Git output without making repository changes."""
    result = subprocess.run(
        ["git", *args], cwd=root, check=False, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    return result.stdout.strip()


def display_root(path: Path, root: Path) -> str:
    """Return a useful repository-relative or explicit external root label."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix() or "."
    except ValueError:
        return path.resolve().as_posix()


def discover_skills(root: Path) -> tuple[set[str], list[str]]:
    """Return skills and roots visible to this packaged navigator process."""
    discovered: set[str] = set()
    roots: list[str] = []
    candidates = (
        ("source", root / "skills"),
        ("project", root / ".agents" / "skills"),
        ("packaged", Path(__file__).resolve().parents[2]),
    )
    seen_roots: set[str] = set()
    for label, skills in candidates:
        key = skills.resolve().as_posix()
        if key in seen_roots:
            continue
        seen_roots.add(key)
        if not skills.is_dir():
            continue
        names = {
            path.name
            for path in skills.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        }
        if not names:
            continue
        discovered.update(names)
        roots.append(f"{label}={display_root(skills, root)}")
    return discovered, roots


def discover_states(root: Path) -> tuple[list[FeatureState], list[str]]:
    """Discover canonical state records and unreadable-state diagnostics."""
    records: list[FeatureState] = []
    errors: list[str] = []
    for workspace, base in (("refinement", "specs-refiniment"), ("implementation", "specs")):
        workspace_root = root / base
        if not workspace_root.is_dir():
            continue
        for path in sorted(workspace_root.glob("*/_ai_sdlc/state.toon")):
            try:
                state = load_state(path)
            except (OSError, ValueError) as exc:
                errors.append(f"unable to read feature state {path}: {exc}")
                continue
            records.append(FeatureState(str(state.get("feature") or path.parents[1].name), workspace, path, state))
    return records, errors


def select_feature(records: list[FeatureState], explicit: str | None, branch: str) -> tuple[FeatureState | None, list[str]]:
    """Select one feature by the documented signal precedence."""
    blockers: list[str] = []
    if explicit:
        matches = [record for record in records if record.feature == explicit]
        if not matches:
            return None, [f"explicit feature state not found: {explicit}"]
        active_matches = [record for record in matches if str(record.state.get("active_skill", "")).strip()]
        if active_matches:
            return sorted(active_matches, key=lambda item: item.workspace)[0], blockers
        matches.sort(key=lambda item: item.workspace == "implementation", reverse=True)
        return matches[0], blockers
    active = [record for record in records if str(record.state.get("active_skill", "")).strip()]
    if active:
        return sorted(active, key=lambda item: item.feature)[0], blockers
    branch_matches = [record for record in records if record.feature in branch]
    if branch_matches:
        branch_matches.sort(key=lambda item: item.workspace == "implementation", reverse=True)
        return branch_matches[0], blockers
    if records:
        return sorted(records, key=lambda item: (str(item.state.get("updated_at", "")), item.feature, item.workspace), reverse=True)[0], blockers
    return None, blockers


def next_state_action(record: FeatureState) -> tuple[Action | None, list[str]]:
    """Return the active or first incomplete action from a feature state."""
    blockers: list[str] = []
    active = str(record.state.get("active_skill", "")).strip()
    stages = [stage for stage in record.state.get("stages", []) if isinstance(stage, dict)]
    if active:
        stage = next((item for item in stages if item.get("skill") == active), {})
        if stage.get("status") == "blocked":
            blockers.append(f"active lifecycle stage is blocked: {active}")
        return Action(active, f"Feature {record.feature} already has this active lifecycle skill.", f"Resume ${active} for {record.feature}.", str(stage.get("artifacts", "none"))), blockers
    for stage in stages:
        if stage.get("workspace") != record.workspace:
            continue
        if str(stage.get("status", "")) not in COMPLETE_STATUSES:
            skill = str(stage.get("skill", ""))
            return Action(skill, f"Feature {record.feature} has incomplete stage {stage.get('id', '')}.", f"Use ${skill} for {record.feature}.", str(stage.get("artifacts", "none"))), blockers
    return None, blockers


def intent_action(intent: str, root: Path) -> Action:
    """Choose a fallback action from natural-language intent and repo shape."""
    normalized = intent.lower()
    for keywords, action in INTENT_ROUTES:
        if any(keyword in normalized for keyword in keywords):
            return action
    if any((root / marker).exists() for marker in ("go.mod", "package.json", "pyproject.toml", "Cargo.toml")):
        return Action("ai-sdlc-sdd", "An established codebase was detected but no active feature state exists.", "Use $ai-sdlc-sdd to classify the requested repository change.", "specs/<feature>")
    return Action("ai-sdlc-working-backwards-discovery", "No active feature state or established codebase signal was detected.", "Use $ai-sdlc-working-backwards-discovery to clarify the initiative.", "discovery.md")


def optional_actions(required: Action, installed: set[str]) -> list[Action]:
    """Return small, non-mandatory follow-up choices."""
    candidates = [
        Action("ai-sdlc-validation", "Run focused deterministic checks when implementation evidence exists.", "Use $ai-sdlc-validation for the changed surface.", "validation evidence"),
        Action("ai-sdlc-security-testing", "Add a security lens when data, auth, or trust boundaries are involved.", "Use $ai-sdlc-security-testing for the target surface.", "security-review.md"),
    ]
    return [action for action in candidates if action.skill != required.skill and action.skill in installed]


def toon_value(value: object) -> str:
    """Escape a scalar for the repository TOON subset."""
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def render_markdown(context: dict[str, object], required: Action, optional: list[Action], blockers: list[str]) -> str:
    """Render a human-facing navigator report."""
    lines = ["# AI SDLC Navigator", "", "## Detected Context"]
    lines.extend(f"- {key.replace('_', ' ').title()}: `{value}`" for key, value in context.items())
    lines.extend(["", "## Next Required", f"- Skill: `{required.skill}`", f"- Reason: {required.reason}", f"- Command: `{required.command}`", f"- Expected artifact: `{required.expected_artifact}`", "", "## Next Optional"])
    lines.extend(
        f"- `{action.skill}` — {action.reason} Command: `{action.command}` Expected: `{action.expected_artifact}`"
        for action in optional
    )
    if not optional:
        lines.append("- None.")
    lines.extend(["", "## Blockers"])
    lines.extend(f"- {blocker}" for blocker in blockers)
    if not blockers:
        lines.append("- None.")
    return "\n".join(lines).rstrip() + "\n"


def render_toon(context: dict[str, object], required: Action, optional: list[Action], blockers: list[str]) -> str:
    """Render a compact machine-facing navigator report."""
    lines = ["schema: ai-sdlc-navigator/v1"]
    lines.extend(f"{key}: {toon_value(value)}" for key, value in context.items())
    lines.extend(["", "next_required[1]{skill,reason,command,expected_artifact}:", "  " + ",".join(toon_value(value) for value in (required.skill, required.reason, required.command, required.expected_artifact)), "", f"next_optional[{len(optional)}]{{skill,reason,command,expected_artifact}}:"])
    lines.extend("  " + ",".join(toon_value(value) for value in (action.skill, action.reason, action.command, action.expected_artifact)) for action in optional)
    lines.extend(["", f"blockers[{len(blockers)}]{{message}}:"])
    lines.extend(f"  {toon_value(blocker)}" for blocker in blockers)
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """Inspect repository signals and print ranked next actions."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--feature")
    parser.add_argument("--intent", default="")
    parser.add_argument("--format", choices=("markdown", "toon"), default="markdown")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--state-check", action="store_true", help="Verify selected state without mutating it")
    parser.add_argument("--begin-state", action="store_true", help="Unsupported mutation flag; reported as a blocker")
    parser.add_argument("--complete-state", action="store_true", help="Unsupported mutation flag; reported as a blocker")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    args = parser.parse_args()

    root = args.root.resolve()
    installed, skill_roots = discover_skills(root)
    states, state_errors = discover_states(root)
    branch = git_output(root, "rev-parse", "--abbrev-ref", "HEAD") or "not-a-git-repository"
    selected, blockers = select_feature(states, args.feature, branch)
    if args.begin_state or args.complete_state:
        blockers.append("navigator is read-only and cannot begin or complete lifecycle state")
    if args.full_flow:
        blockers.extend(state_errors)
        active_features = sorted({record.feature for record in states if str(record.state.get("active_skill", "")).strip()})
        if not args.feature and len(active_features) > 1:
            blockers.append("multiple features have active skills: " + "/".join(active_features))
        if selected:
            index_base = "specs" if selected.workspace == "implementation" else "specs-refiniment"
            if not (root / index_base / "_ai_sdlc" / "specs-index.toon").is_file():
                blockers.append(f"workspace index not found: {index_base}/_ai_sdlc/specs-index.toon")
    required: Action | None = None
    if selected:
        required, state_blockers = next_state_action(selected)
        blockers.extend(state_blockers)
    if required is None:
        required = intent_action(args.intent, root)
    if required.skill == "ai-sdlc-sdd" and branch in DEFAULT_BASE_BRANCHES:
        required = Action(
            "ai-sdlc-branching",
            f"Repository-tracked specification and implementation work must not start on shared base branch {branch}.",
            "Use $ai-sdlc-branching to create a task branch before SDD writes.",
            "task branch",
        )
    if required.skill not in installed:
        blockers.append(f"recommended skill is not installed: {required.skill}")

    dirty = [line for line in git_output(root, "status", "--short").splitlines() if line]
    context: dict[str, object] = {
        "repository": root.as_posix(),
        "branch": branch,
        "installed_skill_count": len(installed),
        "skill_roots": ";".join(skill_roots) or "none",
        "features": "/".join(sorted({record.feature for record in states})) or "none",
        "selected_feature": selected.feature if selected else "none",
        "workspace": selected.workspace if selected else "none",
        "current_stage": str(selected.state.get("current_stage", "none")) if selected else "none",
        "active_skill": str(selected.state.get("active_skill", "none")) or "none" if selected else "none",
        "dirty_change_count": len(dirty),
        "flow_mode": "full" if args.full_flow else "quick" if args.quick_flow else "default",
    }
    optional = optional_actions(required, installed)
    renderer = render_toon if args.format == "toon" else render_markdown
    print(renderer(context, required, optional, blockers), end="")
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
