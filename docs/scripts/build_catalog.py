#!/usr/bin/env python3
"""Generate deterministic human-facing skill, script, module, and coverage docs."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
SKILL_GUIDES = DOCS / "reference" / "skills"
SOURCE_URL = "https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main"
SKILL_GUIDE_HEADINGS = (
    "## Why it exists",
    "## Use it when",
    "## Do not use it when",
    "## Who is involved",
    "## Before you start",
    "## Tell your agent",
    "## What the agent reads",
    "## What it may write",
    "## Human checkpoints",
    "## Flow modes",
    "## Deterministic helpers",
    "## Success criteria",
    "## Blockers and recovery",
    "## Handoff",
    "## State, metadata, and indexes",
    "## Example",
    "## Source contract",
)

# This is the explicit cross-skill selection contract used by the public guides.
# Each capability owns execution details in its SKILL.md; this table owns the
# human question "when should I choose something else?" and must close exactly
# over the installable skill inventory.
SKILL_SELECTION_BOUNDARIES: dict[str, tuple[str, ...]] = {
    "ai-sdlc-approvals-sandbox": (
        "Do not use it to decide product, delivery, or security risk. Use the owning lifecycle skill and accountable human policy instead.",
    ),
    "ai-sdlc-architecture": (
        "Do not use it while business behavior or customer value is still unclear. Use `ai-sdlc-ba` or the appropriate refinement workflow instead.",
    ),
    "ai-sdlc-ba": (
        "Do not use it to discover an unframed customer problem. Use `ai-sdlc-working-backwards-discovery` instead.",
        "Do not use it for implementation design or code changes. Use `ai-sdlc-sdd` or `ai-sdlc-architecture` instead.",
    ),
    "ai-sdlc-backlog-decomposition-and-task-planning": (
        "Do not use it while initiative requirements still have blocking gaps. Use `ai-sdlc-backlog-requirements-gap-review` instead.",
    ),
    "ai-sdlc-backlog-requirements-gap-review": (
        "Do not use it before goals, roles, capabilities, and epics exist. Use `ai-sdlc-goal-capability-and-epic-mapping` instead.",
    ),
    "ai-sdlc-branching": (
        "Do not use branch hygiene to define behavior or design. Use `ai-sdlc-sdd` for the change contract instead.",
    ),
    "ai-sdlc-change-impact": (
        "Do not use it for an unaccepted proposal that has no baseline change set. Use `ai-sdlc-change-set` instead.",
    ),
    "ai-sdlc-change-set": (
        "Do not use it for an ordinary new feature with no accepted downstream baseline. Use `ai-sdlc-navigator` to select refinement or `ai-sdlc-sdd` instead.",
    ),
    "ai-sdlc-code-review": (
        "Do not use it when no diff and no accepted contract exist. Use the implementation path in `ai-sdlc-sdd` instead.",
        "Do not use it as a general test runner. Use `ai-sdlc-validation` instead.",
    ),
    "ai-sdlc-commit-prep": (
        "Do not use it while the task or validation evidence is incomplete. Use `ai-sdlc-validation` and finish the owning task instead.",
        "Do not use it only to word a commit subject. Use `ai-sdlc-conventional-commit` instead.",
    ),
    "ai-sdlc-conventional-commit": (
        "Do not use it to stage files or prove scope and readiness. Use `ai-sdlc-commit-prep` instead.",
    ),
    "ai-sdlc-delivery-graph": (
        "Do not use it to invent missing requirements or delivery artifacts. Use the owning producer skill instead, then rebuild the graph.",
    ),
    "ai-sdlc-delivery-handoff-review": (
        "Do not use it before delivery specification and QA readiness work are complete. Use `ai-sdlc-delivery-spec-synthesis` and the QA readiness workflow instead.",
    ),
    "ai-sdlc-delivery-package-gap-review": (
        "Do not use it when no discovery package or PRFAQ exists. Use `ai-sdlc-working-backwards-discovery` and `ai-sdlc-prfaq-package-synthesis` instead.",
    ),
    "ai-sdlc-delivery-spec-synthesis": (
        "Do not use it while user behavior and story boundaries remain unclear. Use `ai-sdlc-ba` or `ai-sdlc-user-story-decomposition` instead.",
    ),
    "ai-sdlc-doctor": (
        "Do not use it to diagnose application feature behavior. Use `ai-sdlc-validation` instead.",
        "Do not use it to apply installation or upgrade changes. Use the authorized install or update workflow instead.",
    ),
    "ai-sdlc-evidence-council": (
        "Do not use it as authoritative approval or sign-off. Use the accountable human gate instead.",
        "Do not use it to gather missing sources. Use `ai-sdlc-research` instead.",
    ),
    "ai-sdlc-goal-capability-and-epic-mapping": (
        "Do not use it while the customer problem, audience, or outcome is unclear. Use `ai-sdlc-working-backwards-discovery` instead.",
    ),
    "ai-sdlc-host-adapter": (
        "Do not use it before a validated workflow declares the host capability it needs. Use `ai-sdlc-workflow` to define that contract instead.",
    ),
    "ai-sdlc-navigator": (
        "Do not use it when the correct skill is already known and execution is requested. Use that owning skill instead; the navigator is read-only.",
    ),
    "ai-sdlc-package-trust": (
        "Do not use package verification to install, execute, publish, sign, approve, or delete a package. Use the separately authorized package lifecycle workflow instead.",
        "Do not use local metrics for content analytics or telemetry upload. Use an approved observability and privacy workflow instead.",
    ),
    "ai-sdlc-policy": (
        "Do not use policy evaluation to create requirements or product decisions. Use the owning refinement or `ai-sdlc-sdd` skill instead.",
    ),
    "ai-sdlc-prfaq-package-synthesis": (
        "Do not use it before discovery establishes the customer, problem, value, and evidence. Use `ai-sdlc-working-backwards-discovery` instead.",
    ),
    "ai-sdlc-project-context": (
        "Do not use repository context as product authority or missing requirements. Use `ai-sdlc-ba` or `ai-sdlc-sdd` instead.",
    ),
    "ai-sdlc-qa": (
        "Do not use it while expected behavior or acceptance criteria are undefined. Use the requirements readiness or business-analysis workflow instead.",
    ),
    "ai-sdlc-qa-requirements-gap-review": (
        "Do not use it when no QA scope or delivery artifact exists to review. Use `ai-sdlc-qa` instead.",
    ),
    "ai-sdlc-qa-traceability-and-readiness-review": (
        "Do not use it before executable cases and suites exist. Use `ai-sdlc-test-cases` and `ai-sdlc-test-case-and-suite-synthesis` instead.",
    ),
    "ai-sdlc-quality-lenses": (
        "Do not use a quality lens when the primary artifact is missing. Use its owning producer skill instead.",
        "Do not use a lens as formal approval. Use the accountable human review gate instead.",
    ),
    "ai-sdlc-release-slicing-and-backlog-readiness-review": (
        "Do not use it before a decomposed backlog exists. Use `ai-sdlc-backlog-decomposition-and-task-planning` instead.",
    ),
    "ai-sdlc-requirements-readiness-review": (
        "Do not use it before PRFAQ synthesis and delivery-package gap review are complete. Use those producer workflows instead.",
    ),
    "ai-sdlc-research": (
        "Do not use external research for facts already authoritative in the repository. Use `ai-sdlc-project-context` instead.",
        "Do not use research to accept a product, legal, security, or delivery decision. Route evidence to the accountable owner or `ai-sdlc-change-impact` instead.",
    ),
    "ai-sdlc-retrospective": (
        "Do not use it while the run or its evidence is still incomplete. Use `ai-sdlc-runtime` or `ai-sdlc-validation` instead.",
        "Do not use it to adopt a proposal automatically. Use `ai-sdlc-policy` and `ai-sdlc-change-set` instead.",
    ),
    "ai-sdlc-runtime": (
        "Do not use it without an accepted immutable execution plan. Use `ai-sdlc-workflow` or `ai-sdlc-sdd` instead.",
        "Do not use it for a bounded one-off task that needs no declared DAG. Use the normal owning implementation workflow instead.",
    ),
    "ai-sdlc-sdd": (
        "Do not use it while the customer problem or required behavior is still unclear. Use the relevant refinement workflow instead.",
        "Do not use it for review-only work or a trivial non-behavioral edit. Use `ai-sdlc-code-review` or the focused task workflow instead.",
    ),
    "ai-sdlc-security-testing": (
        "Do not use it for general correctness or non-security review. Use `ai-sdlc-validation` or `ai-sdlc-code-review` instead.",
        "Do not use it before trust boundaries and protected assets are defined. Use `ai-sdlc-sdd` or `ai-sdlc-architecture` instead.",
    ),
    "ai-sdlc-shared-runtime": (
        "Do not use shared helpers as a lifecycle entry point. Use `ai-sdlc-navigator` or the owning skill instead.",
        "Do not edit installed mirrors to repair packaging. Use the authorized install or update workflow and canonical `_shared` sources instead.",
    ),
    "ai-sdlc-test-case-and-suite-synthesis": (
        "Do not use it before individual test cases and QA strategy exist. Use `ai-sdlc-test-cases` and `ai-sdlc-test-scope-and-strategy-design` instead.",
    ),
    "ai-sdlc-test-cases": (
        "Do not use it while requirements or test strategy still have blocking gaps. Use `ai-sdlc-qa-requirements-gap-review` or `ai-sdlc-test-scope-and-strategy-design` instead.",
    ),
    "ai-sdlc-test-scope-and-strategy-design": (
        "Do not use it while QA-blocking requirement gaps remain. Use `ai-sdlc-qa-requirements-gap-review` instead.",
    ),
    "ai-sdlc-user-story-decomposition": (
        "Do not use it before goals, capabilities, epics, and delivery gaps are understood. Use the goal-mapping and delivery-package gap workflows instead.",
    ),
    "ai-sdlc-ux": (
        "Do not use it while actors, workflows, or business rules are unclear. Use `ai-sdlc-ba` instead.",
        "Do not use it to implement interface code. Use `ai-sdlc-sdd` instead.",
    ),
    "ai-sdlc-validation": (
        "Do not use it when expected behavior is undefined. Use `ai-sdlc-sdd` or the QA requirements workflow instead.",
        "Do not use it to produce review findings. Use `ai-sdlc-code-review` or `ai-sdlc-security-testing` instead.",
    ),
    "ai-sdlc-workflow": (
        "Do not use it for a one-off task with no reusable or declared DAG. Use the normal owning skill instead.",
        "Do not use it to execute an accepted plan. Use `ai-sdlc-runtime` instead.",
    ),
    "ai-sdlc-working-backwards-discovery": (
        "Do not use it when the problem and behavior are already accepted and implementation can start. Use `ai-sdlc-navigator` or `ai-sdlc-sdd` instead.",
        "Do not use it to synthesize the final PRFAQ package. Use `ai-sdlc-prfaq-package-synthesis` instead.",
    ),
}


def research_read_contract() -> str:
    """Return the research-specific evidence and freshness contract."""
    return """### Required reads

- `<feature-root>/_ai_sdlc/state.toon` before any durable write.
- The matching `specs/_ai_sdlc/specs-index.toon` or `specs-refiniment/_ai_sdlc/specs-index.toon` before broad repository reads.
- `/tmp/research.json`, or another explicitly supplied input file, conforming to `ai-sdlc-research-input/v1`.
- Every repository evidence path and direct source locator registered by that input.

### Optional reads

- Existing requirements, decisions, or earlier research only when their IDs are named as trace targets.
- Direct web pages opened through the host web/browser tool for `external` or `mixed` scope. Search-result pages and cached model knowledge are not evidence.

### Freshness rule

For current claims, compare the source publication date with the date the event or data applies to, record ISO `accessed_at`, search for superseding primary or official material, and preserve material contradictions and freshness limitations.

The [research input contract](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-research/references/research-contract.md) defines required fields; the [web research protocol](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-research/references/web-research-protocol.md) defines direct-source and freshness behavior. JSON is used only at this validated interoperability boundary; durable repository output remains Markdown plus TOON."""


def research_input_example() -> str:
    """Return a minimal valid research input shape for onboarding."""
    return """Create `/tmp/research.json` with the validated input shape before running the helper:

```json
{
  "schema": "ai-sdlc-research-input/v1",
  "topic": "Current payment retry requirements",
  "scope": "external",
  "questions": [
    {"id": "Q-001", "question": "What is currently required?", "trace_targets": ["REQ-014"]}
  ],
  "sources": [
    {"id": "SRC-001", "title": "Primary guidance", "locator": "https://example.org/guidance", "type": "official-guidance", "accessed_at": "2026-07-19", "credibility": "primary", "notes": "Check for superseding guidance"}
  ],
  "findings": [
    {"id": "F-001", "statement": "The current guidance requires a bounded retry policy.", "source_ids": ["SRC-001"], "confidence": "medium", "limitations": "Jurisdiction review is still required", "trace_targets": ["REQ-014"]}
  ],
  "open_questions": [
    {"id": "OQ-001", "question": "Which jurisdictions apply?", "owner": "Legal", "next_action": "Confirm scope"}
  ]
}
```

Then run the source-contract command. External or current work must use internet research to open and verify direct pages; never replace it with model memory.
"""


def package_trust_branch_guide() -> str:
    """Separate package verification from privacy-preserving local metrics."""
    return """## Choose one package-trust branch

These are independent operations. Pick exactly one branch for the current request; neither grants install, execution, upload, or approval authority.

| Branch | Choose it when | Do not choose it when | Helper | Durable output |
| --- | --- | --- | --- | --- |
| **A — Verify a package** | A package must be evaluated against origin, API, capability, integrity, and provenance policy. | You need to install, execute, publish, sign, approve, or delete it; use the separately authorized package lifecycle workflow instead. | `package_trust.py` | `_ai_sdlc/trust/<package-id>/decision.{toon,json,md}` |
| **B — Generate local metrics** | You need reproducible content-free counts, budgets, statuses, coverage, freshness, and fingerprints from local run evidence. | You need content analytics, event telemetry, or upload; use an approved observability/privacy workflow instead. | `metrics.py` | `_ai_sdlc/metrics/local.{toon,json,md}` |

### Branch A — Verify a package

**Inputs and reads.** Read the package root, versioned manifest, allowed origins, allowed capabilities, active harness API, provenance policy, and every declared regular file. Reject unsafe paths, symlinks, hash drift, incompatibility, disallowed capabilities, or missing required provenance.

**Tell your agent.**

```text
Use ai-sdlc-package-trust branch A to verify <package-root> against <manifest>,
allowed origins/capabilities, harness API <version>, and provenance policy.
Start in report mode, explain every control, and do not install or execute anything.
```

**Terminal starting point.**

```bash
python3 skills/ai-sdlc-package-trust/scripts/package_trust.py . --package-root package --manifest package.json --allowed-origin repository --allowed-capability filesystem.read --require-provenance
```

**Human checkpoint.** A security or release owner supplies the policy and reviews allow/deny evidence. An `allow` result is evidence only, never installation or execution approval.

**Modes.** Quick flow checks every required control for the declared package. Full flow additionally reviews every file, capability, origin, provenance claim, and privacy field; full flow wins when both flags appear.

**Success example.** A deny is a valid successful evaluation when a required control fails:

```toon
schema: ai-sdlc-package-trust-decision/v1
decision: deny
controls[2]{code,status,evidence}:
  integrity,pass,all declared hashes match
  provenance,fail,required evidence missing
```

**Blockers and output.** Missing package root, manifest, allowed origin, valid harness API, or readable declared files blocks evaluation. Preserve the reason and write only `_ai_sdlc/trust/<package-id>/decision.{toon,json,md}` when explicit write mode is authorized.

### Branch B — Generate local metrics

**Inputs and reads.** Read only repository-local `_ai_sdlc/runs/*/state.json` records with schema `ai-sdlc-run-state/v1` and optional `_ai_sdlc/evidence-ledger.json` with schema `ai-sdlc-evidence-ledger/v1`. Aggregate schemas, fingerprints, statuses, booleans, and numeric counts or budgets only.

**Tell your agent.**

```text
Use ai-sdlc-package-trust branch B to generate local content-free metrics for <repository>.
Do not use the network, upload data, or include content, prompts, commands, diffs,
source text, artifact paths, messages, reasons, or file bodies.
```

**Terminal starting point.**

```bash
python3 skills/ai-sdlc-package-trust/scripts/metrics.py . --generate
```

**Human checkpoint.** A delivery or privacy owner reviews the permitted field set and confirms that any later sharing or upload is outside this skill and requires separate authority.

**Modes.** Quick flow produces the same deterministic privacy-safe aggregate over available local records. Full flow additionally reviews every privacy field; neither mode changes feature state or uses the network.

**Success example.** No eligible evidence is not fabricated into activity; it produces an explicit insufficient-data result:

```toon
schema: ai-sdlc-local-metrics/v1
status: insufficient-data
runs:
  total: 0
tasks:
  total: 0
```

**Blockers and output.** A missing repository or any forbidden content-bearing field blocks the operation. Otherwise write only `_ai_sdlc/metrics/local.{toon,json,md}` in explicit write mode; the helper has no network operation and never uploads metrics.
"""


@dataclass(frozen=True)
class ScriptRecord:
    """One documented Python entry path."""

    path: Path
    owner: str
    classification: str
    purpose: str
    invocation: str
    actor: str
    repository_effect: str


def skill_frontmatter(path: Path) -> dict[str, str]:
    """Read required public identity fields from one skill contract."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path.relative_to(ROOT)}: missing frontmatter")
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key in {"name", "description"}:
            values[key] = value.strip().strip('"')
    if not values.get("name") or not values.get("description"):
        raise ValueError(f"{path.relative_to(ROOT)}: missing name or description")
    return values


def section_body(text: str, heading: str) -> str:
    """Extract one Markdown section while retaining nested headings."""
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return ""
    level = len(heading) - len(heading.lstrip("#"))
    body: list[str] = []
    for line in lines[start + 1 :]:
        match = re.match(r"^(#+)\s+", line)
        if match and len(match.group(1)) <= level:
            break
        body.append(line)
    return "\n".join(body).strip()


def skill_card(text: str, source: Path) -> dict[str, str]:
    """Parse stable labeled fields from the source Skill Card."""
    block = section_body(text, "## 0. Skill Card")
    values: dict[str, str] = {}
    active = ""
    for line in block.splitlines():
        if line.startswith("### "):
            break
        match = re.match(r"^- ([A-Za-z][A-Za-z ]+):\s*(.*)$", line)
        if match:
            active = match.group(1)
            values[active] = match.group(2).strip()
        elif active and line.strip():
            values[active] = f"{values[active]} {line.strip()}".strip()
    required = {
        "Skill name",
        "Primary audience",
        "Supporting audience",
        "SDLC stage",
        "Purpose",
        "Output",
    }
    missing = sorted(required - values.keys())
    if missing:
        raise ValueError(
            f"{source.relative_to(ROOT)}: incomplete Skill Card: {', '.join(missing)}"
        )
    return values


def load_modules() -> list[dict[str, object]]:
    """Load versioned module manifests."""
    modules: list[dict[str, object]] = []
    for path in sorted((ROOT / "modules").glob("*/module.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["manifest_path"] = path.relative_to(ROOT).as_posix()
        modules.append(data)
    return modules


def module_owners(modules: list[dict[str, object]]) -> dict[str, list[str]]:
    """Map skill IDs to their declaring modules."""
    owners: dict[str, list[str]] = {}
    for module in modules:
        for skill in module.get("skills", []):
            owners.setdefault(skill["name"], []).append(str(module["id"]))
    return owners


def skill_sources() -> list[Path]:
    """Return every installable skill contract."""
    return sorted((ROOT / "skills").glob("*/SKILL.md"))


def script_sources() -> list[Path]:
    """Return every package and source-shared Python script in documentation scope."""
    package = sorted((ROOT / "skills").glob("*/scripts/*.py"))
    shared = sorted((ROOT / "skills" / "_shared").glob("*.py"))
    return package + shared


def compact(value: str) -> str:
    """Collapse prose for table cells without losing its meaning."""
    return " ".join(value.split())


def bullet_paragraphs(value: str) -> list[str]:
    """Preserve wrapped Markdown bullets as complete single records."""
    records: list[str] = []
    active: list[str] = []
    for line in value.splitlines():
        if line.startswith("- "):
            if active:
                records.append(" ".join(active))
            active = [line]
        elif active and line.strip():
            active.append(line.strip())
        elif active:
            records.append(" ".join(active))
            active = []
    if active:
        records.append(" ".join(active))
    return records


def markdown_cell(value: str) -> str:
    """Escape a generated Markdown table cell."""
    return compact(value).replace("|", "\\|")


def source_link(path: Path, label: str | None = None) -> str:
    """Link a generated guide back to repository authority."""
    relative = path.relative_to(ROOT).as_posix()
    return f"[{label or relative}]({SOURCE_URL}/{relative})"


def has_cli_entry(source: str) -> bool:
    """Return true only for scripts that execute a real module entrypoint."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
            continue
        if not isinstance(node.test.left, ast.Name) or node.test.left.id != "__name__":
            continue
        if any(isinstance(op, ast.Eq) for op in node.test.ops) and any(
            isinstance(comparator, ast.Constant) and comparator.value == "__main__"
            for comparator in node.test.comparators
        ):
            return True
    return False


def script_record(path: Path) -> ScriptRecord:
    """Classify one script conservatively from its path and source behavior."""
    relative = path.relative_to(ROOT)
    source = path.read_text(encoding="utf-8")
    purpose = ast.get_docstring(ast.parse(source))
    if not purpose:
        raise ValueError(f"{relative}: missing module docstring")

    if relative.parts[1] == "_shared":
        owner = "shared runtime"
        if path.name.startswith("test_") or path.name == "ai_sdlc_install_smoke.py":
            classification = "repository validation runner"
            actor = "Maintainer or CI; it may create only disposable test fixtures."
        elif path.name == "sync_installed_runtime.py":
            classification = "runtime packaging helper"
            actor = "Maintainer or release automation when refreshing installed mirrors."
        else:
            classification = "canonical shared helper"
            actor = "Owning skills import it; maintainers may run a documented CLI entry."
    elif relative.parts[1] == "ai-sdlc-shared-runtime":
        owner = "ai-sdlc-shared-runtime"
        classification = "installed runtime mirror"
        actor = "Installed downstream skills import it; never edit this generated copy directly."
    else:
        owner = relative.parts[1]
        classification = "skill package helper"
        actor = f"The agent runs it through `{owner}`; humans may reproduce its documented checks."

    mutating_markers = (
        "atomic_write",
        "write_text(",
        "os.replace",
        ".mkdir(",
        '"--write"',
        '"--apply"',
        '"--create"',
        '"--execute"',
        '"--section"',
        '"--finalize"',
        '"--begin-state"',
        '"--complete-state"',
    )
    if owner == "ai-sdlc-navigator":
        effect = "Read-only router; mutation-shaped flags are rejected and reported as blockers."
    elif classification == "installed runtime mirror":
        effect = "Generated copy; repository behavior is defined by its canonical shared source."
    elif classification == "repository validation runner":
        effect = "Read-only for delivery files; may use temporary directories for deterministic checks."
    elif any(marker in source for marker in mutating_markers):
        effect = "May write only through an explicit mutation mode; start with `--help`, check, preview, or emit."
    else:
        effect = "Read-only/reporting by default; inspect `--help` and the owning skill before direct use."

    skill_usage = ""
    if classification == "skill package helper":
        contract = ROOT / "skills" / owner / "SKILL.md"
        if contract.is_file():
            relative_text = relative.as_posix()
            for line in contract.read_text(encoding="utf-8").splitlines():
                if f"python3 {relative_text}" in line:
                    command = re.search(
                        rf"python3 {re.escape(relative_text)}[^`]*",
                        line,
                    )
                    skill_usage = (
                        command.group(0).rstrip("\\").strip() if command else ""
                    )
                    break
    cli_entry = has_cli_entry(source)
    if cli_entry and "argparse.ArgumentParser" in source:
        invocation = f"python3 {relative.as_posix()} --help"
    elif skill_usage:
        invocation = skill_usage
    elif path.name.startswith("test_"):
        invocation = f"python3 {relative.as_posix()}"
    else:
        invocation = "Imported helper; use the owning skill rather than invoking it directly."
    purpose = purpose.split("\n\n", 1)[0]
    return ScriptRecord(path, owner, classification, compact(purpose), invocation, actor, effect)


def render_skill_guide(
    path: Path,
    owners: dict[str, list[str]],
    scripts: list[ScriptRecord],
) -> str:
    """Render one complete, predictable, human-facing capability guide."""
    text = path.read_text(encoding="utf-8")
    metadata = skill_frontmatter(path)
    card = skill_card(text, path)
    skill_id = metadata["name"]
    modules = " + ".join(sorted(owners.get(skill_id, []))) or "unregistered"
    required_inputs = section_body(text, "### 0.1 Required Inputs")
    clarification = section_body(text, "### 0.2 Clarification Rules")
    modes = section_body(text, "### 0.2.1 Flow Mode Flags")
    output_rules = section_body(text, "### 0.3 Output Rules")
    routing = section_body(text, "### 0.4 Artifact Routing")
    state = section_body(text, "## 0.5 Feature State Machine")
    metadata_rules = section_body(text, "## 0.6 Artifact Metadata And Metatags")
    indexes = section_body(text, "## 0.7 Specs Index")
    usage = section_body(text, "## Script Usage")
    source_inputs = section_body(text, "## Inputs")
    output_spec = section_body(text, "## Output Spec")
    examples = section_body(text, "## Examples")
    edge_cases = section_body(text, "## Edge Cases")
    selection_boundaries = SKILL_SELECTION_BOUNDARIES.get(skill_id, ())
    negative_lines = [f"- {boundary}" for boundary in selection_boundaries]
    specialized_sections = (
        package_trust_branch_guide().splitlines()
        if skill_id == "ai-sdlc-package-trust"
        else []
    )
    agent_reads = (
        research_read_contract()
        if skill_id == "ai-sdlc-research"
        else source_inputs or required_inputs
    )

    helper_rows = [record for record in scripts if record.owner == skill_id]
    helper_lines = [
        "| Helper | Purpose | Direct starting point | Repository effect |",
        "| --- | --- | --- | --- |",
    ]
    for record in helper_rows:
        helper_lines.append(
            "| "
            + " | ".join(
                (
                    source_link(record.path, f"`{record.path.name}`"),
                    markdown_cell(record.purpose),
                    f"`{record.invocation}`",
                    markdown_cell(record.repository_effect),
                )
            )
            + " |"
        )
    if not helper_rows:
        helper_lines.append(
            "| None | This capability is instruction-only. | Use the agent prompt below. | Follow artifact routing. |"
        )

    success = output_spec or (
        f"A successful result produces {card['Output']} and satisfies every output rule and blocker check below."
    )
    example = examples or usage
    if skill_id == "ai-sdlc-research":
        example = research_input_example() + "\n" + example
    source_relative = path.relative_to(ROOT).as_posix()
    title = skill_id.removeprefix("ai-sdlc-").replace("-", " ").title()
    if "no independent quick/full" in modes.lower():
        prompt_mode = (
            "Do not select a flow flag independently; preserve the mode of the "
            "owning downstream skill as described below."
        )
    else:
        prompt_mode = (
            "Choose --quick-flow for bounded assumption-driven progress or --full-flow\n"
            "for strict verification only as described below."
        )
    before_start = required_inputs
    prompt_lines = [
        f"Use {skill_id} for <target>.",
        prompt_mode,
        "Read the required evidence,",
        f"produce or report {card['Output']}, preserve human approval boundaries,",
        "and return blockers plus a complete ai-sdlc-handoff/v1.",
    ]
    checkpoint_guidance = clarification
    mode_guidance = modes
    usage_guidance = usage
    blocker_guidance = edge_cases or clarification
    if skill_id == "ai-sdlc-package-trust":
        before_start = (
            "Choose exactly one branch above. Complete only that branch's "
            "inputs and reads; the other branch is not a prerequisite."
        )
        prompt_lines = [
            "Choose Branch A or Branch B above and copy its branch-specific prompt.",
            "Do not send a combined package-verification and metrics request.",
            "Apply --quick-flow or --full-flow only to the selected branch,",
            "preserve human approval boundaries, and return ai-sdlc-handoff/v1.",
        ]
        agent_reads = (
            "Read only the inputs named by the selected branch above. Branch A "
            "does not read runtime metrics; Branch B does not read package files, "
            "manifests, origin policy, or provenance evidence."
        )
        checkpoint_guidance = (
            "Use only the selected branch's human checkpoint above. The trust "
            "reviewer and metrics/privacy reviewer are not interchangeable approvals."
        )
        mode_guidance = (
            "Apply quick/full behavior only within the selected branch as defined "
            "above. Do not use a flow flag to combine the branches."
        )
        usage_guidance = (
            "There is no combined command. Select one branch and use only its "
            "Terminal starting point above; add `--write` only after its output "
            "boundary is understood and authorized."
        )
        success = (
            "Use the selected branch's success example and schema above. A trust "
            "decision and a local-metrics record are separate results."
        )
        blocker_guidance = (
            "Use only the selected branch's blocker and output rule above. If branch "
            "selection is ambiguous, stop and ask instead of reading both input sets."
        )
        example = (
            "Choose one of the two success examples above. Do not run both helpers "
            "merely because both capabilities share this skill package."
        )
    lines = [
        "---",
        f"title: {title}",
        f"description: Human-facing operating guide for {skill_id}, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.",
        "---",
        "",
        f"# `{skill_id}`",
        "",
        metadata["description"],
        "",
        "| Lifecycle position | Primary owner | Supporting roles | Module | Output |",
        "| --- | --- | --- | --- | --- |",
        f"| {markdown_cell(card['SDLC stage'])} | {markdown_cell(card['Primary audience'])} | {markdown_cell(card['Supporting audience'])} | `{modules}` | {markdown_cell(card['Output'])} |",
        "",
        "## Why it exists",
        "",
        card["Purpose"],
        "",
        "## Use it when",
        "",
        metadata["description"],
        "",
        "If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.",
        "",
        "## Do not use it when",
        "",
        *negative_lines,
        "",
        *specialized_sections,
        "",
        "## Who is involved",
        "",
        f"- **Accountable/primary:** {card['Primary audience']}.",
        f"- **Supporting:** {card['Supporting audience']}.",
        "- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.",
        "",
        "## Before you start",
        "",
        before_start,
        "",
        "## Tell your agent",
        "",
        "```text",
        *prompt_lines,
        "```",
        "",
        "This is an agent instruction, not a shell command. Terminal commands belong in the helper section.",
        "",
        "## What the agent reads",
        "",
        agent_reads,
        "",
        "## What it may write",
        "",
        routing,
        "",
        "## Human checkpoints",
        "",
        checkpoint_guidance,
        "",
        "Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.",
        "",
        "## Flow modes",
        "",
        mode_guidance,
        "",
        "## Deterministic helpers",
        "",
        "Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.",
        "",
        *helper_lines,
        "",
        "The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.",
        "",
        "### Contract-provided usage",
        "",
        usage_guidance,
        "",
        "## Success criteria",
        "",
        success,
        "",
        "## Blockers and recovery",
        "",
        blocker_guidance,
        "",
        "On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.",
        "",
        "## Handoff",
        "",
        output_rules,
        "",
        "The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.",
        "",
        "## State, metadata, and indexes",
        "",
        "??? info \"Feature state\"",
        "",
        *(f"    {line}" if line else "" for line in state.splitlines()),
        "",
        "??? info \"Artifact metadata\"",
        "",
        *(f"    {line}" if line else "" for line in metadata_rules.splitlines()),
        "",
        "??? info \"Specs index\"",
        "",
        *(f"    {line}" if line else "" for line in indexes.splitlines()),
        "",
        "## Example",
        "",
        example,
        "",
        "## Source contract",
        "",
        f"This page is generated from {source_link(path, f'`{source_relative}`')}. Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.",
        "",
        "[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def validate_research_example(content: str) -> list[str]:
    """Run the published JSON through the authoritative research helper."""
    example = section_body(content, "## Example")
    blocks = re.findall(r"```json\n(.*?)\n```", example, flags=re.DOTALL)
    if len(blocks) != 1:
        return ["ai-sdlc-research: expected exactly one JSON input example"]
    script = ROOT / "skills/ai-sdlc-research/scripts/research.py"
    spec = importlib.util.spec_from_file_location("ai_sdlc_research_contract", script)
    if spec is None or spec.loader is None:
        return ["ai-sdlc-research: cannot load authoritative research validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = Path(temp_dir) / "research.json"
        input_path.write_text(blocks[0] + "\n", encoding="utf-8")
        value, errors = module.load(input_path)
    if not errors:
        errors.extend(module.validate(value, full_flow=False))
    return [f"ai-sdlc-research: published JSON fails helper: {error}" for error in errors]


def validate_package_trust_branches(content: str) -> list[str]:
    """Validate each package-trust operation independently."""
    common = (
        "**Inputs and reads.**",
        "**Tell your agent.**",
        "**Terminal starting point.**",
        "**Human checkpoint.**",
        "**Modes.**",
        "**Success example.**",
        "**Blockers and output.**",
    )
    branches = {
        "### Branch A — Verify a package": common
        + (
            "package_trust.py",
            "ai-sdlc-package-trust-decision/v1",
            "_ai_sdlc/trust/<package-id>/decision.{toon,json,md}",
        ),
        "### Branch B — Generate local metrics": common
        + (
            "metrics.py",
            "ai-sdlc-local-metrics/v1",
            "status: insufficient-data",
            "_ai_sdlc/metrics/local.{toon,json,md}",
            "helper has no network operation",
        ),
    }
    errors: list[str] = []
    for heading, tokens in branches.items():
        body = section_body(content, heading)
        if not body:
            errors.append(f"ai-sdlc-package-trust: missing branch {heading}")
            continue
        for token in tokens:
            if token not in body:
                errors.append(
                    f"ai-sdlc-package-trust: {heading} missing independent field {token}"
                )
    return errors


def validate_skill_guide(content: str, skill_id: str) -> list[str]:
    """Validate one generated page's complete human-facing operating shape."""
    errors = [
        f"{skill_id}: missing guide section {heading}"
        for heading in SKILL_GUIDE_HEADINGS
        if heading not in content
    ]
    errors.extend(
        f"{skill_id}: empty guide section {heading}"
        for heading in SKILL_GUIDE_HEADINGS
        if heading in content and not section_body(content, heading)
    )
    if "### 0." in content.split("## Why it exists", 1)[0]:
        errors.append(f"{skill_id}: Skill Card summary absorbed nested contract sections")
    for token in (
        skill_id,
        "ai-sdlc-handoff/v1",
        "SKILL.md",
        "--quick-flow",
        "--full-flow",
        "source-checkout",
        ".agents/skills/<skill>/...",
    ):
        if token not in content:
            errors.append(f"{skill_id}: missing guide contract token {token}")
    selection = section_body(content, "## Do not use it when")
    if not selection or " instead" not in selection.lower():
        errors.append(f"{skill_id}: non-use guidance must name a concrete alternative")
    if skill_id == "ai-sdlc-research":
        for token in (
            "### Required reads",
            "### Optional reads",
            "### Freshness rule",
            "<feature-root>/_ai_sdlc/state.toon",
            "specs/_ai_sdlc/specs-index.toon",
            "ai-sdlc-research-input/v1",
            '"scope": "external"',
            '"accessed_at"',
            "Direct web pages",
            "never replace it with model memory",
        ):
            if token not in content:
                errors.append(f"{skill_id}: missing research evidence contract {token}")
        errors.extend(validate_research_example(content))
    if skill_id == "ai-sdlc-package-trust":
        if "## Choose one package-trust branch" not in content:
            errors.append(f"{skill_id}: missing branch selection contract")
        errors.extend(validate_package_trust_branches(content))
    return errors


def validate_selection_contract(paths: list[Path]) -> list[str]:
    """Require one explicit alternative-bearing selection boundary per skill."""
    skill_ids = {skill_frontmatter(path)["name"] for path in paths}
    contract_ids = set(SKILL_SELECTION_BOUNDARIES)
    errors = [
        f"selection contract missing skill {skill_id}"
        for skill_id in sorted(skill_ids - contract_ids)
    ]
    errors.extend(
        f"selection contract has unknown skill {skill_id}"
        for skill_id in sorted(contract_ids - skill_ids)
    )
    for skill_id, boundaries in sorted(SKILL_SELECTION_BOUNDARIES.items()):
        if not boundaries:
            errors.append(f"selection contract has no boundaries for {skill_id}")
        for boundary in boundaries:
            if not boundary.startswith("Do not ") or " instead" not in boundary.lower():
                errors.append(
                    f"selection contract boundary lacks a non-use case and alternative for {skill_id}"
                )
    return errors


def validate_script_catalog(content: str, records: list[ScriptRecord]) -> list[str]:
    """Validate exact path coverage and required operator guidance."""
    errors: list[str] = []
    for record in records:
        relative = record.path.relative_to(ROOT).as_posix()
        if content.count(relative) < 2:
            errors.append(f"script catalog missing documented path {relative}")
    for token in (
        "Who runs it",
        "Safe starting point",
        "Repository effect",
        "Direct-use safety rule",
        "Installed runtime mirrors",
        "harness source checkout",
        ".agents/skills/<skill>/...",
    ):
        if token not in content:
            errors.append(f"script catalog missing field {token}")
    return errors


def validate_coverage_manifest(
    content: str,
    skill_count: int,
    records: list[ScriptRecord],
) -> list[str]:
    """Validate TOON-first source-to-page closure."""
    errors: list[str] = []
    for token in (
        "schema: ai-sdlc-documentation-coverage/v1",
        f"skills[{skill_count}]{{skill,source,page,module,package_scripts}}:",
        f"scripts[{len(records)}]{{path,owner,classification,documentation}}:",
    ):
        if token not in content:
            errors.append(f"coverage manifest missing contract {token}")
    for path in skill_sources():
        skill_id = skill_frontmatter(path)["name"]
        source = path.relative_to(ROOT).as_posix()
        if source not in content:
            errors.append(f"coverage manifest missing skill source {source}")
        if f"reference/skills/{skill_id}.md" not in content:
            errors.append(f"coverage manifest missing skill {skill_id}")
    for record in records:
        relative = record.path.relative_to(ROOT).as_posix()
        if relative not in content:
            errors.append(f"coverage manifest missing script {relative}")
    return errors


def render_skills(
    modules: list[dict[str, object]],
    scripts: list[ScriptRecord],
) -> str:
    """Render the local discovery surface for every detailed skill page."""
    owners = module_owners(modules)
    lines = [
        "---",
        "title: Skill catalog",
        "description: Every installed AI SDLC capability with a local human-facing guide, lifecycle position, module, outputs, and helper count.",
        "---",
        "",
        "# Skill catalog",
        "",
        "This generated catalog is the public discovery surface for every installed capability. Each guide follows the same operating shape, while the linked `SKILL.md` remains execution authority.",
        "",
        '<div class="grid cards" markdown>',
        "",
    ]
    for path in skill_sources():
        text = path.read_text(encoding="utf-8")
        values = skill_frontmatter(path)
        card = skill_card(text, path)
        skill_id = values["name"]
        module_names = " + ".join(sorted(owners.get(skill_id, []))) or "unregistered"
        helper_count = len([record for record in scripts if record.owner == skill_id])
        lines.extend(
            [
                f"-   **`{skill_id}`**",
                "",
                f"    `{module_names}` · {card['SDLC stage']} · {helper_count} package helper(s)",
                "",
                f"    {card['Purpose']}",
                "",
                f"    **Output:** {card['Output']}",
                "",
                f"    [Open the complete guide →](skills/{skill_id}.md)",
                "",
            ]
        )
    lines.extend(
        [
            "</div>",
            "",
            "Need an executable helper rather than a lifecycle guide? Use the [complete script reference](scripts.md).",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_scripts(records: list[ScriptRecord]) -> str:
    """Render all source, package, validation, packaging, and mirror script paths."""
    groups = (
        ("Skill package helpers", "skill package helper"),
        ("Canonical shared helpers", "canonical shared helper"),
        ("Repository validation runners", "repository validation runner"),
        ("Runtime packaging helpers", "runtime packaging helper"),
        ("Installed runtime mirrors", "installed runtime mirror"),
    )
    lines = [
        "---",
        "title: Script reference",
        "description: Complete generated inventory of every Python helper, runner, packaging utility, and installed runtime mirror in documentation scope.",
        "---",
        "",
        "# Script reference",
        "",
        f"This page documents all {len(records)} Python paths in scope. Scripts are agent internals unless a guide explicitly tells a human to run one. Start with the owning skill and `--help`; a helper never grants filesystem, network, approval, policy, or release authority.",
        "",
        "Every inventory path is relative to a **harness source checkout**. Consumer repositories normally invoke an installed skill through the agent; direct diagnosis uses the corresponding project-scoped `.agents/skills/<skill>/...` path. Source-only `skills/_shared` validation and packaging runners are not consumer commands.",
        "",
        "## How to read the inventory",
        "",
        "- **Skill package helper:** behavior owned by one installable capability.",
        "- **Canonical shared helper:** source-checkout runtime imported by many capabilities.",
        "- **Validation/packaging helper:** maintainer and CI surface, not a delivery-stage entry point.",
        "- **Installed runtime mirror:** generated portable copy; edit its canonical `_shared` source and resync instead.",
        "- **Repository effect:** conservative classification; explicit write/apply/execute modes still require the owning workflow and human authority.",
        "",
    ]
    for title, classification in groups:
        selected = [record for record in records if record.classification == classification]
        lines.extend(
            [
                f"## {title} ({len(selected)})",
                "",
                "| Script | Owner | Purpose | Who runs it | Safe starting point | Repository effect |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for record in selected:
            relative = record.path.relative_to(ROOT).as_posix()
            lines.append(
                "| "
                + " | ".join(
                    (
                        source_link(record.path, f"`{relative}`"),
                        f"`{record.owner}`",
                        markdown_cell(record.purpose),
                        markdown_cell(record.actor),
                        f"`{record.invocation}`",
                        markdown_cell(record.repository_effect),
                    )
                )
                + " |"
            )
        lines.append("")
    lines.extend(
        [
            "## Direct-use safety rule",
            "",
            "Run a helper directly only when the owning guide or maintainer workflow names it. Inspect `--help`, begin with read-only check/preview/emit behavior, keep the target repository explicit, and stop on unexpected writes or permission requests. Installed mirrors are never the edit target.",
            "",
            "[Back to the skill catalog](skills.md)",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_modules(modules: list[dict[str, object]]) -> str:
    """Render module compatibility and registration details."""
    lines = [
        "---",
        "title: Module catalog",
        "description: Installed capability modules, compatibility ranges, dependencies, and registered skills.",
        "---",
        "",
        "# Module catalog",
        "",
        '<div class="grid cards" markdown>',
        "",
    ]
    for module in modules:
        harness = module.get("harness_api", {})
        requires = ", ".join(module.get("requires", [])) or "none"
        skills = ", ".join(item["name"] for item in module.get("skills", [])) or "none"
        lines.extend(
            [
                f"-   **{str(module['id']).replace('-', ' ').title()}** · `{module['kind']}` · `v{module['version']}`",
                "",
                f"    {module['description']}",
                "",
                f"    **Harness API:** ≥ {harness.get('min', '')} and < {harness.get('max_exclusive', '')}",
                "",
                f"    **Requires:** {requires}",
                "",
                f"    **Skills:** {skills}",
                "",
                f"    {source_link(ROOT / str(module['manifest_path']), 'Open manifest →')}",
                "",
            ]
        )
    lines.extend(
        [
            "</div>",
            "",
            "Module discovery validates schema, ID uniqueness, dependency presence, API compatibility, skill paths, and protected capability rules before navigation exposes a module.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def toon_value(value: object) -> str:
    """Encode one scalar for the repository's compact TOON subset."""
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def render_coverage(
    modules: list[dict[str, object]],
    records: list[ScriptRecord],
) -> str:
    """Render exact source-to-documentation closure in TOON."""
    owners = module_owners(modules)
    skills = []
    for path in skill_sources():
        skill_id = skill_frontmatter(path)["name"]
        skills.append(
            (
                skill_id,
                path.relative_to(ROOT).as_posix(),
                f"reference/skills/{skill_id}.md",
                "+".join(sorted(owners.get(skill_id, []))) or "unregistered",
                len([record for record in records if record.owner == skill_id]),
            )
        )
    lines = [
        "schema: ai-sdlc-documentation-coverage/v1",
        f"skill_count: {len(skills)}",
        f"script_count: {len(records)}",
        "documentation_root: docs",
        "",
        f"skills[{len(skills)}]{{skill,source,page,module,package_scripts}}:",
    ]
    lines.extend("  " + ",".join(toon_value(value) for value in row) for row in skills)
    lines.extend(
        [
            "",
            f"scripts[{len(records)}]{{path,owner,classification,documentation}}:",
        ]
    )
    for record in records:
        row = (
            record.path.relative_to(ROOT).as_posix(),
            record.owner,
            record.classification,
            "reference/scripts.md",
        )
        lines.append("  " + ",".join(toon_value(value) for value in row))
    return "\n".join(lines).rstrip() + "\n"


def generated_outputs() -> dict[Path, str]:
    """Build the complete deterministic output set in memory."""
    modules = load_modules()
    records = [script_record(path) for path in script_sources()]
    owners = module_owners(modules)
    outputs = {
        DOCS / "reference" / "skills.md": render_skills(modules, records),
        DOCS / "reference" / "scripts.md": render_scripts(records),
        DOCS / "reference" / "modules.md": render_modules(modules),
        DOCS / "reference" / "catalog-coverage.toon": render_coverage(modules, records),
    }
    for path in skill_sources():
        skill_id = skill_frontmatter(path)["name"]
        outputs[SKILL_GUIDES / f"{skill_id}.md"] = render_skill_guide(
            path, owners, records
        )
    paths = skill_sources()
    errors = validate_selection_contract(paths)
    for path in paths:
        skill_id = skill_frontmatter(path)["name"]
        errors.extend(
            validate_skill_guide(outputs[SKILL_GUIDES / f"{skill_id}.md"], skill_id)
        )
    errors.extend(validate_script_catalog(outputs[DOCS / "reference" / "scripts.md"], records))
    errors.extend(
        validate_coverage_manifest(
            outputs[DOCS / "reference" / "catalog-coverage.toon"],
            len(skill_sources()),
            records,
        )
    )
    if errors:
        raise ValueError("generated documentation contract failed:\n" + "\n".join(errors))
    return outputs


def generate(check: bool = False) -> int:
    """Write generated docs or fail when any generated output drifts."""
    outputs = generated_outputs()
    expected_skill_pages = {
        path for path in outputs if path.parent == SKILL_GUIDES and path.suffix == ".md"
    }
    stale_skill_pages = (
        set(SKILL_GUIDES.glob("*.md")) - expected_skill_pages
        if SKILL_GUIDES.is_dir()
        else set()
    )
    drift: list[str] = []
    for path, content in outputs.items():
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                drift.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if check:
        drift.extend(path.relative_to(ROOT).as_posix() for path in stale_skill_pages)
    else:
        for path in stale_skill_pages:
            path.unlink()
    if drift:
        print("Catalog drift: " + ", ".join(sorted(drift)))
        return 1
    skill_count = len(skill_sources())
    script_count = len(script_sources())
    print(
        f"Catalog ready: {skill_count} skills, {len(load_modules())} modules, "
        f"{script_count} scripts"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when generated data is stale")
    args = parser.parse_args()
    return generate(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
