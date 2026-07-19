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
CANONICAL_INSTALL = "npx -y skills@1.5.19 add mikegorelikoff/ai-sdlc-harness --all"
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
