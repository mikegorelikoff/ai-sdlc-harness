---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-guided-onboarding-documentation"
  artifact: "design.md"
  path: "specs/005-guided-onboarding-documentation/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/005-guided-onboarding-documentation/_ai_sdlc/state.toon"
  decision_log: "specs/005-guided-onboarding-documentation/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-19"
  updated_at: "2026-07-19"
  trace_ids: []
  related_artifacts:
    - "specs/005-guided-onboarding-documentation/decision-log.md"
    - "specs/005-guided-onboarding-documentation/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "review"
---

# Design

## Overview
The public site becomes a layered learning system rather than a flat collection of short pages. Progressive disclosure starts with product purpose and foundations, then offers persona-specific onboarding, reproducible tutorials, complete lifecycle flows, task-oriented how-to guides, generated capability guides, and exact reference. Authoritative execution details remain in skill packages, while public pages translate them into human decisions and expected outcomes.

## Architecture
The documentation architecture has seven public layers:
1. Home and README: one canonical product name, value, fit/non-fit, and two primary paths—Evaluate/adopt and Learn/use.
2. Foundations: SDLC, AI SDLC, SDD, why the harness, mental model, responsibility model, and glossary.
3. Onboarding: prerequisites, canonical installation, first 30 minutes, persona paths, operating model, and adoption.
4. Tutorials and flows: runnable examples plus exact lifecycle journeys with entry/exit/recovery semantics.
5. How-to: bounded operational procedures.
6. Capability guides: generated per-skill detail pages and complete script reference sourced from repository contracts.
7. Reference and governance: schemas, paths, lifecycle matrix, authority, trust, limitations, compatibility, validation, and release evidence.

`docs/` is the canonical public source. Root `concepts/` and `guides/` remain internal historical/authoring material until separately removed; public pages do not depend on readers discovering them.

## Components
- Hand-authored foundation/onboarding pages for concepts, adoption, authority, and governance.
- Expanded tutorials with fixed example scenarios, action labels, expected artifacts, and recovery checkpoints.
- Lifecycle flow pages grouped by discovery/refinement, planning, QA, SDD/build, release, controlled change, runtime/operations, and learning/recovery.
- Enhanced `docs/scripts/build_catalog.py` that parses standardized `SKILL.md` sections and Python helpers into a skill index, one detail page per skill, and a script catalog.
- A machine-readable documentation coverage manifest generated from skill/script inventories.
- Enhanced `docs/scripts/validate_docs.py` and tests enforcing inventory closure, required detail headings, persona entry paths, lifecycle coverage, command existence, canonical naming, and navigation.
- Material navigation grouped for beginners, adopters, practitioners, maintainers, and reference users.

## Interfaces and Contracts
Every public capability page uses a stable human-facing shape: Why it exists; Use it when; Do not use it when; Who is involved; Before you start; Tell your agent; What the agent reads; What it may write; Human checkpoints; Flow modes; Deterministic helpers; Success; Blockers and recovery; Handoff; Example. Generated content points to the authoritative package contract and never changes runtime semantics.

Every lifecycle flow page defines entry signal, accountable owner, participating skills, required evidence, ordered stages, output artifacts, approval gates, completion signal, downstream consumer, and reopen path.

Action blocks use explicit labels: Tell your agent, Run in terminal, Agent does automatically, and Human checkpoint. Beginner pages do not present a skill name as a shell command.

Documentation validation treats the filesystem inventories as authority: installed skills are `skills/*/SKILL.md`; executable helpers are Python files under skill `scripts/` plus declared shared control-plane scripts. Generated pages and manifest must close over those sets.

## Data Model
The generated documentation manifest records schema, generated timestamp-independent inventory identity, skill entries, script entries, lifecycle stages, persona paths, and coverage counts. A skill entry includes ID, module, description, audience, stage, purpose, output, source path, scripts, and generated guide path. A script entry includes relative path, owning capability, docstring purpose, mutation classification, public invocation, and guide anchors. The manifest is derived and deterministic; `SKILL.md`, script source, module manifests, and the lifecycle profile registry remain authoritative.

## Error Handling
Generation fails on missing skill frontmatter, malformed standardized sections, duplicate IDs, unresolved module ownership, or unreadable scripts. Validation accumulates page-scoped errors for missing navigation, broken links, missing required guide sections, uncovered skills/scripts/stages, nonexistent local command paths, conflicting canonical install commands, stale generated output, or missing persona routes. Public troubleshooting uses fail-closed recovery: preserve authoritative artifacts, inspect exact diagnostics, repair derived state, rerun the narrow validator, and escalate when ownership or approval is unclear.

## Security Considerations
Documentation must not normalize autonomous approval, unrestricted shell/network use, secret collection, package trust bypass, policy weakening, or deletion of evidence. Governance explicitly separates human authority from agent execution and links protected actions to policy, approvals, sandbox, package trust, and recovery controls. Examples use placeholder identities and no live credentials. Installation guidance explains source trust, version pinning, global versus scoped effects, and rollback. Claims avoid implying compliance certification or guaranteed correctness.

## Observability
Documentation quality is visible through deterministic counts and gates: public page count, inventory-complete skill coverage, full in-scope script coverage, lifecycle-stage coverage, broken local links, stale catalog status, strict MkDocs result, rendered target count, command smoke checks, and persona PASS/FAIL findings. The final handoff records exact validation commands and remaining limitations. Pilot documentation defines product outcome signals but does not transmit repository data.

## Risks and Tradeoffs
A very complete site can overwhelm beginners; progressive disclosure, persona paths, copyable tutorials, and collapsed detail sections mitigate this. Generated pages can feel repetitive; a stable shared shape makes any skill predictable and prevents silent coverage gaps. Parsing prose-based SKILL.md sections is less strong than a dedicated metadata schema; validation fails clearly and the source link remains authoritative. Root concepts/guides may drift while retained; public docs explicitly become canonical and tests prevent public links from depending on hidden duplicates. Script mutability classification may require conservative heuristics; uncertain helpers are labeled review source before direct use.

## Validation Strategy
Validate in layers:
- Unit tests for parsing skill cards, section extraction, script inventory, guide rendering, and completeness failures.
- Generated-catalog drift checks and coverage manifest closure.
- Command/path smoke checks for canonical install examples and every local Python invocation.
- Documentation source validation, navigation closure, internal links, required headings, persona routes, canonical naming, and lifecycle stage coverage.
- Strict Material build and rendered target validation.
- Focused skill/script contract regression tests and compatibility validation.
- SDD clarify/checklist/plan/analyze/validate gates.
- Independent junior, lead, and VP rereads; any P0/P1 FAIL reopens the relevant documentation task.

## Migration Notes
Existing URLs should remain where practical; rewritten pages preserve paths or add clear replacements through navigation. README, Home, Start, install, and tutorials switch atomically to the canonical Skills CLI path so no mixed installation model remains. Generated skill index remains at `reference/skills.md` and gains linked detail pages; module and release references remain stable. The new site is additive to harness API 1.0.0 and does not migrate user artifacts. Root `concepts/` and `guides/` are labeled internal/non-canonical rather than deleted in this program.
