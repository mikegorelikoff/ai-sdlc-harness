#!/usr/bin/env python3
"""Validate MkDocs Material source, navigation, links, catalogs, and workflow."""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlsplit

from build_catalog import DOCS, ROOT, generate

sys.path.insert(0, str(ROOT / "skills" / "_shared"))
from ai_sdlc_artifact_profiles import PROFILES  # noqa: E402


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
CANONICAL_INSTALL = "DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0 --all"
FLOW_PAGES = {
    "flows/index.md",
    "flows/refinement.md",
    "flows/implementation.md",
    "flows/control-plane.md",
    "flows/recovery.md",
}
REFINEMENT_STAGES = tuple(profile.stage_id for profile in PROFILES)
TUTORIAL_NAVIGATOR_INTENT = "Implement GET /health behavior while preserving existing route behavior."
IMPLEMENTATION_CONTRACT = (
    ("branch", "ai-sdlc-branching", "feature/<slug>"),
    ("sdd", "ai-sdlc-sdd", "specs/<feature>/"),
    ("task_context", "ai-sdlc-project-context", "task-packs/<task>"),
    ("implement", "Host coding agent", "Code, tests"),
    ("validate", "ai-sdlc-validation", "Exact command outcomes"),
    ("review", "ai-sdlc-code-review", "Evidence-ranked findings"),
    ("commit_prep", "ai-sdlc-commit-prep", "traceable commit"),
    ("release_handoff", "ai-sdlc-validation", "ai-sdlc-handoff/v1"),
)
CONTROL_PLANE_CONTRACT = (
    ("controlled_change", "ai-sdlc-change-set", "changes/<change-id>/"),
    ("change_impact", "ai-sdlc-change-impact", "change-impact.md"),
    ("delivery_graph", "ai-sdlc-delivery-graph", "delivery-graph.{toon,json,md}"),
    ("evidence_freshness", "ai-sdlc-delivery-graph", "evidence-ledger.{toon,json,md}"),
    ("policy_waiver", "ai-sdlc-policy", "policy-resolution.{toon,json}"),
    ("context_pack", "ai-sdlc-project-context", "project-context.md"),
    ("runtime", "ai-sdlc-runtime", "journal.jsonl"),
    ("workflow_plan", "ai-sdlc-workflow", "plan.{toon,json,md}"),
    ("host_adapter", "ai-sdlc-host-adapter", "negotiation.{toon,json,md}"),
    ("doctor", "ai-sdlc-doctor", "doctor/report.{toon,json,md}"),
    ("upgrade", "ai-sdlc-doctor", "upgrades/<id>/plan.{toon,json,md}"),
    ("package_trust", "ai-sdlc-package-trust", "decision.{toon,json,md}"),
    ("local_metrics", "ai-sdlc-package-trust", "metrics/local.{toon,json,md}"),
)
CONTRACT_HEADERS = (
    "Predecessor / entry",
    "Accountable owner",
    "Required input",
    "Exact capability",
    "Artifact / result",
    "Exit gate",
    "Next consumer / handoff",
    "Reopen condition",
)
T006_PAGES = {
    "adoption/index.md",
    "adoption/pilot.md",
    "adoption/metrics.md",
    "adoption/rollout.md",
    "onboarding/role-paths.md",
    "operations/index.md",
    "operations/operating-model.md",
    "operations/governance.md",
    "operations/troubleshooting.md",
    "explanation/maturity-limitations.md",
    "maintainers/index.md",
    "maintainers/extend.md",
    "maintainers/release.md",
}
ROLLOUT_STAGES = ("Pilot", "Limited cohort", "Broader cohort", "Standard or hold")
ROLE_PATHS = (
    "New or junior engineer",
    "PM or product owner",
    "Business analyst",
    "QA or test owner",
    "Developer or engineering lead",
    "Architecture or platform",
    "Security, privacy, or compliance",
    "Delivery, release, or operations",
    "Harness maintainer",
    "Engineering manager or VP",
)
PM_REFINEMENT_STAGE_IDS = (
    "discovery",
    "prfaq",
    "requirements_readiness",
    "goal_epic_mapping",
    "backlog_decomposition",
    "release_slicing",
)
RACI_GATES = (
    "Problem/value accepted",
    "Requirements ready",
    "UX/architecture accepted",
    "QA strategy ready",
    "Release slice approved",
    "Branch/task start",
    "SDD ready",
    "Implementation accepted",
    "Security/privacy accepted",
    "Validation complete",
    "Review findings resolved",
    "Policy/waiver accepted",
    "Commit ready",
    "Release/deployment approved",
    "Incident contained/resumed",
    "Pilot scale/stop decision",
)
PILOT_STAGES = ("Baseline", "Kickoff", "Week 1", "Midpoint", "Final")
TROUBLESHOOTING_FAILURES = (
    "Install command fails",
    "Helper import fails after install",
    "Invalid or corrupt state",
    "Stale specs index",
    "State/artifact contradiction",
    "Interrupted write",
    "Divergent refinement/implementation paths",
    "Predecessor blocked",
    "Dirty Git worktree",
    "Unsupported host/capability",
    "Exhausted runtime budget",
    "Non-zero helper exit",
)
GOVERNANCE_HEADINGS = (
    "## Authority hierarchy",
    "## Data and secrets",
    "## Permissions and sandbox",
    "## Package and supply-chain trust",
    "## Policy, waivers, and exceptions",
    "## Retention and deletion",
    "## Enforcement map",
    "## Incident response",
    "## Regulatory and contractual boundary",
)
MATURITY_HEADINGS = (
    "## What is verified today",
    "## Expected but not yet proven generally",
    "## Known limitations",
    "## Support boundary",
    "## Non-goals",
    "## External governance context",
    "## How to make a defensible claim",
)
MAINTAINER_TOKENS = (
    "SKILL.md",
    "module.json",
    "skills/_shared",
    "sync_installed_runtime.py",
    "build_catalog.py",
    "compatibility",
    "Deprecation",
    "rollback",
    "one-task/one-commit",
)


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


def markdown_table(text: str, heading: str) -> list[list[str]]:
    """Return one Markdown table below an exact level-two heading."""
    match = re.search(
        rf"^{re.escape(heading)}\s*$\n\s*\n((?:^\|.*\|\s*$\n?)+)",
        text,
        re.MULTILINE,
    )
    if not match:
        return []
    return [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in match.group(1).splitlines()
        if line.strip()
    ]


def plain_cell(value: str) -> str:
    """Normalize inline-code markers for exact contract comparisons."""
    return value.replace("`", "").strip()


def contains_contract_token(text: str, token: str) -> bool:
    """Match a skill/artifact token without accepting a longer fake identifier."""
    return bool(
        re.search(
            rf"(?<![A-Za-z0-9_-]){re.escape(token)}(?![A-Za-z0-9_-])",
            text,
        )
    )


def validate_refinement_contract(text: str) -> list[str]:
    """Bind every canonical refinement stage to its ordered table record."""
    errors: list[str] = []
    table = markdown_table(text, "## Exact stage contract")
    if len(table) < 3:
        return ["docs/flows/refinement.md: missing parseable exact stage table"]
    rows = table[2:]
    actual_order = [plain_cell(row[1]) for row in rows if len(row) == 7]
    if actual_order != list(REFINEMENT_STAGES):
        errors.append("docs/flows/refinement.md: canonical stage order does not match PROFILES")
    if len(rows) != len(PROFILES):
        errors.append(
            "docs/flows/refinement.md: expected "
            f"{len(PROFILES)} stage rows but found {len(rows)}"
        )
    for number, profile in enumerate(PROFILES, start=1):
        if number > len(rows):
            break
        row = rows[number - 1]
        if len(row) != 7:
            errors.append(
                f"docs/flows/refinement.md: stage row {number} must contain seven fields"
            )
            continue
        predecessors = ", ".join(profile.predecessors) or "none"
        actual = (
            plain_cell(row[0]),
            plain_cell(row[1]),
            plain_cell(row[2]),
            plain_cell(row[3]),
            plain_cell(row[5]),
        )
        expected = (
            str(number),
            profile.stage_id,
            profile.skill,
            predecessors,
            profile.artifact_name,
        )
        if actual != expected:
            errors.append(
                "docs/flows/refinement.md: mis-associated canonical profile "
                f"{profile.stage_id}; expected {expected}, found {actual}"
            )
    return errors


def validate_full_lifecycle_contract(text: str) -> list[str]:
    """Bind each ordered tutorial heading to its exact skill and artifact."""
    errors: list[str] = []
    matches = list(
        re.finditer(r"^### Stage (\d+) — `([^`]+)`(?:,.*)?\s*$", text, re.MULTILINE)
    )
    actual = [(int(match.group(1)), match.group(2)) for match in matches]
    expected = [(number, profile.stage_id) for number, profile in enumerate(PROFILES, start=1)]
    if actual != expected:
        errors.append("docs/tutorials/full-lifecycle.md: canonical stage heading order does not match PROFILES")
    for index, profile in enumerate(PROFILES):
        if index >= len(matches):
            break
        start = matches[index].end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[start:end]
        if not contains_contract_token(section, profile.skill) or not contains_contract_token(
            section, profile.artifact_name
        ):
            errors.append(
                "docs/tutorials/full-lifecycle.md: mis-associated stage contract "
                f"{profile.stage_id}/{profile.skill}/{profile.artifact_name}"
            )
    return errors


def validate_contract_matrix(
    text: str,
    heading: str,
    label: str,
    expected: tuple[tuple[str, str, str], ...],
) -> list[str]:
    """Validate ordered implementation/control branch records and all fields."""
    errors: list[str] = []
    table = markdown_table(text, heading)
    if len(table) < 3:
        return [f"{label}: missing parseable contract matrix"]
    header = tuple(plain_cell(value) for value in table[0][1:])
    if header != CONTRACT_HEADERS:
        errors.append(f"{label}: contract matrix headers are incomplete")
    rows = table[2:]
    actual_order = [plain_cell(row[0]) for row in rows if len(row) == 9]
    if actual_order != [item[0] for item in expected]:
        errors.append(f"{label}: branch order/inventory does not match the canonical contract")
    if len(rows) != len(expected):
        errors.append(f"{label}: expected {len(expected)} branch rows but found {len(rows)}")
    for index, (branch_id, capability, artifact) in enumerate(expected):
        if index >= len(rows):
            break
        row = rows[index]
        if len(row) != 9 or any(not plain_cell(value) for value in row):
            errors.append(f"{label}: branch {branch_id} must populate all nine fields")
            continue
        if plain_cell(row[0]) != branch_id or capability not in row[4] or artifact not in row[5]:
            errors.append(
                f"{label}: mis-associated branch contract {branch_id}/{capability}/{artifact}"
            )
    return errors


def validate_flows(root: Path = ROOT) -> list[str]:
    """Validate lifecycle closure and runnable tutorial semantics."""
    errors: list[str] = []
    docs = root / "docs"
    missing = sorted(relative for relative in FLOW_PAGES if not (docs / relative).is_file())
    if missing:
        errors.append("missing workflow journey pages: " + ", ".join(missing))

    refinement = docs / "flows/refinement.md"
    if refinement.is_file():
        text = refinement.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        errors.extend(validate_refinement_contract(text))
        if "`--full-flow`" not in text and "full-flow" not in text:
            errors.append("docs/flows/refinement.md: missing full-flow semantics")
        if "strengthens only that skill and never starts the next one" not in normalized:
            errors.append("docs/flows/refinement.md: full-flow must be distinguished from the 18-stage sequence")

    implementation = docs / "flows/implementation.md"
    if implementation.is_file():
        errors.extend(
            validate_contract_matrix(
                implementation.read_text(encoding="utf-8"),
                "## Exact implementation contract",
                "docs/flows/implementation.md",
                IMPLEMENTATION_CONTRACT,
            )
        )

    control_plane = docs / "flows/control-plane.md"
    if control_plane.is_file():
        errors.extend(
            validate_contract_matrix(
                control_plane.read_text(encoding="utf-8"),
                "## Exact control-plane branch contract",
                "docs/flows/control-plane.md",
                CONTROL_PLANE_CONTRACT,
            )
        )

    first_feature = docs / "tutorials/first-feature.md"
    if first_feature.is_file():
        text = first_feature.read_text(encoding="utf-8")
        required = (
            "Tell your agent",
            "Run in terminal",
            "Agent does automatically",
            "Human checkpoint",
            "Expected tree",
            "deliberate regression",
            "ai-sdlc-handoff/v1",
            "python3 -m unittest -v",
            "git diff --check",
            "feature/001-health-endpoint",
            "test_deliberate_unknown_route_regression.py",
            "ai-sdlc-navigator/v1",
            TUTORIAL_NAVIGATOR_INTENT,
        )
        for token in required:
            if token.lower() not in text.lower():
                errors.append(f"docs/tutorials/first-feature.md: missing runnable tutorial contract {token}")
        handoffs = re.findall(r"```toon\n(schema: ai-sdlc-handoff/v1.*?)(?:\n```)", text, re.DOTALL)
        if not handoffs:
            errors.append("docs/tutorials/first-feature.md: missing parseable handoff example")
        for handoff in handoffs:
            for contract in (
                "result: complete",
                "summary:",
                "blockers[",
                "next_required[1]{skill,reason,command,expected_artifact}:",
                "next_optional[",
            ):
                if contract not in handoff:
                    errors.append(f"docs/tutorials/first-feature.md: invalid handoff example missing {contract}")
            required_row = handoff.split("next_required[1]{skill,reason,command,expected_artifact}:", 1)[-1].split("next_optional[", 1)[0]
            values = [item.strip() for item in required_row.strip().split(",")]
            if len(values) != 4 or not all(values):
                errors.append("docs/tutorials/first-feature.md: handoff next_required must contain four populated columns")
        for source in (
            root / "skills/_shared/ai_sdlc_install_smoke.py",
            root / "skills/ai-sdlc-navigator/tests/test_navigate.py",
        ):
            if not source.is_file() or TUTORIAL_NAVIGATOR_INTENT not in source.read_text(encoding="utf-8"):
                errors.append(
                    f"{display_path(source, root)}: tutorial navigator intent is not exercised exactly"
                )

    fixture = root / "examples" / "onboarding-health-service"
    failure_probe = fixture / "deliberate_unknown_route_regression.py.disabled"
    if not failure_probe.is_file():
        errors.append("examples/onboarding-health-service: missing deterministic failure fixture")
    elif (fixture / "test_app.py").is_file():
        failed = subprocess.run(
            [sys.executable, str(failure_probe)],
            cwd=fixture,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        failed_output = failed.stderr + failed.stdout
        if failed.returncode == 0 or "FAILED" not in failed_output or "deliberate probe" not in failed_output:
            errors.append("examples/onboarding-health-service: deliberate failure probe must fail deterministically")
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "-v"],
            cwd=fixture,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode or "Ran 2 tests" not in result.stderr + result.stdout:
            errors.append("examples/onboarding-health-service: starting fixture tests must pass exactly two cases")

    full_lifecycle = docs / "tutorials/full-lifecycle.md"
    if full_lifecycle.is_file():
        text = full_lifecycle.read_text(encoding="utf-8")
        errors.extend(validate_full_lifecycle_contract(text))
        for token in (
            "feature/organization-sso",
            "refinement_status.py",
            "test-environment-resolution.md",
            "rm /tmp/ai-sdlc-sso-demo/test-environment-resolution.md",
            "cp /tmp/ai-sdlc-sso-test-environment-resolution.md test-environment-resolution.md",
            "result is `blocked`",
            "Stage 13 — resume",
            "18/18",
            "Never edit",
        ):
            if token not in text:
                errors.append(
                    "docs/tutorials/full-lifecycle.md: missing lifecycle proof "
                    f"{token}"
                )

    sso_fixture = root / "examples" / "onboarding-sso"
    for name in ("scenario.md", "decisions.md", "test-environment-resolution.md"):
        if not (sso_fixture / name).is_file():
            errors.append(f"examples/onboarding-sso: missing lifecycle fixture {name}")
    return errors


def validate_role_paths(text: str) -> list[str]:
    """Require one explicit onboarding route for every target persona."""
    errors = [
        f"docs/onboarding/role-paths.md: missing persona path {role}"
        for role in ROLE_PATHS
        if f"## {role}" not in text
    ]
    profiles = {profile.stage_id: profile for profile in PROFILES}
    for stage_id in PM_REFINEMENT_STAGE_IDS:
        artifact = profiles[stage_id].artifact_name
        if f"`{artifact}`" not in text:
            errors.append(
                "docs/onboarding/role-paths.md: PM path missing canonical refinement "
                f"artifact {stage_id}/{artifact}"
            )
    normalized = " ".join(text.split())
    for token in (
        "BRD) is a section inside `prfaq.md`",
        "`specs/<feature>/requirements.md`",
        "not a refinement output",
    ):
        if token not in normalized:
            errors.append(f"docs/onboarding/role-paths.md: missing artifact boundary {token}")
    if "`brd.md`" in text:
        errors.append("docs/onboarding/role-paths.md: invents standalone refinement artifact brd.md")
    return errors


def validate_raci_contract(text: str) -> list[str]:
    """Validate the ordered gate-level human/agent authority matrix."""
    table = markdown_table(text, "## Lifecycle gate matrix")
    if len(table) < 3:
        return ["docs/operations/operating-model.md: missing parseable lifecycle gate matrix"]
    errors: list[str] = []
    expected_header = (
        "Gate",
        "Accountable (A)",
        "Responsible (R)",
        "Consulted (C)",
        "Informed (I)",
        "Agent may",
        "Agent must not",
        "Required evidence",
        "Escalation owner",
    )
    if tuple(plain_cell(cell) for cell in table[0]) != expected_header:
        errors.append("docs/operations/operating-model.md: RACI headers are incomplete")
    rows = table[2:]
    actual = [plain_cell(row[0]) for row in rows if len(row) == 9]
    if actual != list(RACI_GATES):
        errors.append("docs/operations/operating-model.md: gate inventory/order is incomplete")
    for gate, row in zip(RACI_GATES, rows):
        if len(row) != 9 or any(not plain_cell(cell) for cell in row):
            errors.append(f"docs/operations/operating-model.md: gate {gate} must populate R, A, C, I, agent boundaries, evidence, and escalation")
    return errors


def validate_pilot_contract(text: str) -> list[str]:
    """Validate baseline-to-scale pilot decision records."""
    table = markdown_table(text, "## Pilot decision contract")
    if len(table) < 3:
        return ["docs/adoption/pilot.md: missing parseable pilot decision contract"]
    errors: list[str] = []
    expected_header = (
        "Stage",
        "Evidence",
        "Threshold / trigger",
        "Accountable owner",
        "Allowed result",
    )
    if tuple(plain_cell(cell) for cell in table[0]) != expected_header:
        errors.append("docs/adoption/pilot.md: pilot decision headers are incomplete")
    rows = table[2:]
    actual = [plain_cell(row[0]) for row in rows if len(row) == 5]
    if actual != list(PILOT_STAGES):
        errors.append("docs/adoption/pilot.md: pilot stage inventory/order is incomplete")
    for stage, row in zip(PILOT_STAGES, rows):
        if len(row) != 5 or any(not plain_cell(cell) for cell in row):
            errors.append(f"docs/adoption/pilot.md: stage {stage} must populate all five fields")
    for token in ("two to four weeks", "one team", "one repository", "Roll back", "Stop", "Scale"):
        if token.lower() not in text.lower():
            errors.append(f"docs/adoption/pilot.md: missing pilot contract {token}")
    return errors


def validate_rollout_contract(text: str) -> list[str]:
    """Require reversible cohort promotion after a bounded pilot."""
    table = markdown_table(text, "## Rollout contract")
    if len(table) < 3:
        return ["docs/adoption/rollout.md: missing parseable rollout contract"]
    errors: list[str] = []
    actual = [plain_cell(row[0]) for row in table[2:] if row]
    if actual != list(ROLLOUT_STAGES):
        errors.append("docs/adoption/rollout.md: rollout stage inventory/order is incomplete")
    required = ("Accountable", "Entry", "Capacity", "Observation", "Rollback", "Decision")
    for token in required:
        if token.lower() not in text.lower():
            errors.append(f"docs/adoption/rollout.md: missing rollout contract field {token}")
    for token in ("limited cohort", "broader cohort", "standard or hold", "does not automatically generalize", "observation window"):
        if token.lower() not in text.lower():
            errors.append(f"docs/adoption/rollout.md: missing rollout boundary {token}")
    return errors


def validate_troubleshooting_contract(text: str) -> list[str]:
    """Validate every required safe diagnosis and recovery class."""
    table = markdown_table(text, "## Failure matrix")
    if len(table) < 3:
        return ["docs/operations/troubleshooting.md: missing parseable failure matrix"]
    errors: list[str] = []
    expected_header = (
        "Failure",
        "Diagnose safely",
        "Safe repair or blocker",
        "Validate / expected result",
        "Do not do",
        "Escalate when",
    )
    if tuple(plain_cell(cell) for cell in table[0]) != expected_header:
        errors.append("docs/operations/troubleshooting.md: recovery headers are incomplete")
    rows = table[2:]
    actual = [plain_cell(row[0]) for row in rows if len(row) == 6]
    missing = [failure for failure in TROUBLESHOOTING_FAILURES if failure not in actual]
    if missing:
        errors.append(
            "docs/operations/troubleshooting.md: missing failure classes "
            + ", ".join(missing)
        )
    for row in rows:
        if len(row) != 6 or any(not plain_cell(cell) for cell in row):
            errors.append("docs/operations/troubleshooting.md: every failure must populate diagnosis, repair/blocker, validation, do-not, and escalation")
            continue
        failure, diagnose, repair, verify, prohibited, _escalation = row
        if "`" not in diagnose and "](" not in diagnose:
            errors.append(f"docs/operations/troubleshooting.md: {failure} diagnosis lacks an exact command or guide")
        if "`" not in verify and "](" not in verify:
            errors.append(f"docs/operations/troubleshooting.md: {failure} validation lacks an exact command or guide")
        if "expected" not in verify.lower():
            errors.append(f"docs/operations/troubleshooting.md: {failure} validation lacks an expected result")
        if "`" not in repair and "](" not in repair and "blocker" not in repair.lower():
            errors.append(f"docs/operations/troubleshooting.md: {failure} repair lacks an executable path or explicit blocker")
        if not prohibited.strip().startswith("Do not"):
            errors.append(f"docs/operations/troubleshooting.md: {failure} lacks explicit do-not guidance")
    if "Never delete an authoritative artifact" not in text:
        errors.append("docs/operations/troubleshooting.md: missing authoritative-evidence protection")
    return errors


def validate_governance_contract(text: str) -> list[str]:
    """Require every governance and enforcement topic."""
    return [
        f"docs/operations/governance.md: missing governance topic {heading}"
        for heading in GOVERNANCE_HEADINGS
        if heading not in text
    ]


def validate_maturity_contract(text: str) -> list[str]:
    """Keep proof, hypotheses, limitations, support, and non-goals explicit."""
    return [
        f"docs/explanation/maturity-limitations.md: missing maturity topic {heading}"
        for heading in MATURITY_HEADINGS
        if heading not in text
    ]


def validate_maintainer_contract(text: str) -> list[str]:
    """Require the complete extension-to-release lifecycle."""
    return [
        f"maintainer path missing lifecycle contract {token}"
        for token in MAINTAINER_TOKENS
        if token not in text
    ]


def validate_root_source_text(text: str, label: str) -> list[str]:
    """Validate one internal authoring note's public-docs marker."""
    errors: list[str] = []
    if not text.startswith("<!-- public-docs-canonical: ../docs/index.md -->"):
        errors.append(f"{label}: missing non-canonical source marker")
    if "../docs/" not in "\n".join(text.splitlines()[:8]):
        errors.append(f"{label}: missing canonical public destination")
    return errors


def validate_canonical_sources(root: Path = ROOT) -> list[str]:
    """Keep root authoring notes explicitly subordinate to public docs."""
    errors: list[str] = []
    for folder in ("concepts", "guides"):
        for path in sorted((root / folder).glob("*.md")):
            text = path.read_text(encoding="utf-8")
            errors.extend(validate_root_source_text(text, display_path(path, root)))
    pages, _ = collect_pages(root / "docs")
    for page in pages:
        for target in internal_links(page):
            path_text = unquote(urlsplit(target).path)
            if not path_text:
                continue
            resolved = (page.path.parent / path_text).resolve()
            for folder in (root / "concepts", root / "guides"):
                try:
                    resolved.relative_to(folder.resolve())
                except ValueError:
                    continue
                errors.append(
                    f"{display_path(page.path, root)}: public docs depend on non-canonical {folder.name} target {target}"
                )
    return errors


def validate_section_index(page: Page, folder: Path, label: str) -> list[str]:
    """Validate one section landing page against its sibling pages."""
    linked: set[str] = set()
    for target in internal_links(page):
        path_text = unquote(urlsplit(target).path)
        if not path_text:
            continue
        resolved = (page.path.parent / path_text).resolve()
        if resolved.parent == folder.resolve() and resolved.suffix == ".md":
            linked.add(resolved.name)
    expected = {path.name for path in folder.glob("*.md") if path.name != "index.md"}
    missing = sorted(expected - linked)
    return [f"{label}: missing sibling links " + ", ".join(missing)] if missing else []


def validate_section_indexes(root: Path = ROOT) -> list[str]:
    """Require section landing pages to expose every sibling public page."""
    errors: list[str] = []
    for relative in ("adoption", "operations", "maintainers", "onboarding", "how-to", "explanation"):
        folder = root / "docs" / relative
        index = folder / "index.md"
        if not index.is_file():
            errors.append(f"docs/{relative}/index.md: missing section index")
            continue
        page = parse_frontmatter(index)
        errors.extend(validate_section_index(page, folder, f"docs/{relative}/index.md"))
    return errors


def validate_adoption_operations(root: Path = ROOT) -> list[str]:
    """Validate T006 persona, adoption, governance, operations, and maintainer closure."""
    docs = root / "docs"
    errors: list[str] = []
    missing = sorted(relative for relative in T006_PAGES if not (docs / relative).is_file())
    if missing:
        errors.append("missing adoption/operations pages: " + ", ".join(missing))

    def read(relative: str) -> str:
        path = docs / relative
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    errors.extend(validate_role_paths(read("onboarding/role-paths.md")))
    errors.extend(validate_raci_contract(read("operations/operating-model.md")))
    errors.extend(validate_pilot_contract(read("adoption/pilot.md")))
    errors.extend(validate_rollout_contract(read("adoption/rollout.md")))
    errors.extend(validate_troubleshooting_contract(read("operations/troubleshooting.md")))

    errors.extend(validate_governance_contract(read("operations/governance.md")))
    errors.extend(validate_maturity_contract(read("explanation/maturity-limitations.md")))
    maintainer = read("maintainers/extend.md") + read("maintainers/release.md")
    errors.extend(validate_maintainer_contract(maintainer))

    for relative in ("README.md", "docs/index.md"):
        text = (root / relative).read_text(encoding="utf-8") if (root / relative).is_file() else ""
        for target in ("adoption/index.md", "onboarding/index.md"):
            if target not in text:
                errors.append(f"{relative}: missing distinct evaluate/use route {target}")

    update = read("how-to/update.md")
    versions = read("reference/versions.md")
    for token in ("Consumer repository", "Source checkout", ".agents/skills", "skills/_shared"):
        if token not in update:
            errors.append(f"docs/how-to/update.md: missing execution-context contract {token}")
    if "source checkout" not in versions.lower() or "Consumer repositories" not in versions:
        errors.append("docs/reference/versions.md: compatibility execution context remains ambiguous")

    errors.extend(validate_canonical_sources(root))
    errors.extend(validate_section_indexes(root))
    install = read("how-to/install.md")
    if "https://www.skills.sh/docs/cli#telemetry" not in install or "DISABLE_TELEMETRY=1" not in install:
        errors.append("docs/how-to/install.md: missing third-party installer telemetry disclosure and opt-out")
    for relative in ("README.md", "docs/index.md", "docs/how-to/install.md"):
        text = (root / relative).read_text(encoding="utf-8") if (root / relative).is_file() else ""
        if "22.20.0" not in text:
            errors.append(f"{relative}: missing pinned Node.js engine floor 22.20.0")
    public_paths = ([root / "README.md"] if (root / "README.md").is_file() else [])
    if (root / "docs").is_dir():
        public_paths.extend((root / "docs").rglob("*.md"))
    for path in public_paths:
        text = path.read_text(encoding="utf-8")
        powershell_telemetry = False
        for line in text.splitlines():
            if "$env:DISABLE_TELEMETRY" in line:
                powershell_telemetry = True
            if "npx -y skills@1.5.19" in line and "DISABLE_TELEMETRY=1" not in line:
                if not powershell_telemetry:
                    errors.append(f"{display_path(path, root)}: Skills CLI command lacks telemetry opt-out")
            if not line.strip() and powershell_telemetry:
                powershell_telemetry = False
    state = root / "specs/005-guided-onboarding-documentation/_ai_sdlc/state.toon"
    if not state.is_file():
        errors.append("specs/005-guided-onboarding-documentation: authoritative state.toon is missing")
    spec_paths = (root / "specs").rglob("*.md") if (root / "specs").is_dir() else []
    for path in spec_paths:
        if "/Users/" in path.read_text(encoding="utf-8", errors="replace"):
            errors.append(f"{display_path(path, root)}: tracked metadata contains machine-specific absolute path")
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
        "python3 skills/_shared/ai_sdlc_install_smoke.py --mode npx",
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
    errors.extend(validate_flows(root))
    errors.extend(validate_adoption_operations(root))
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
