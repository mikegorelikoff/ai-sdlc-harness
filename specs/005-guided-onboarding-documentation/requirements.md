---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-guided-onboarding-documentation"
  artifact: "requirements.md"
  path: "specs/005-guided-onboarding-documentation/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/005-guided-onboarding-documentation/_ai_sdlc/state.toon"
  decision_log: "specs/005-guided-onboarding-documentation/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-19"
  updated_at: "2026-07-19"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "AC-011"
    - "AC-012"
    - "AC-013"
    - "AC-014"
    - "AC-015"
    - "AC-016"
    - "AC-017"
    - "AC-018"
    - "DEC-001"
  related_artifacts:
    - "specs/005-guided-onboarding-documentation/decision-log.md"
    - "specs/005-guided-onboarding-documentation/design.md"
    - "specs/005-guided-onboarding-documentation/plan.md"
    - "specs/005-guided-onboarding-documentation/qa.md"
    - "specs/005-guided-onboarding-documentation/tasks.md"
    - "specs/005-guided-onboarding-documentation/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
---

# Requirements

## Goal
Turn the public site into a beginner-first, decision-grade onboarding system that explains why AI SDLC Harness exists, teaches AI SDLC and SDD from first principles, guides a newcomer through safe use, and documents every lifecycle flow, skill, script, control, recovery path, and adoption decision in sufficient detail for junior engineers, technical leads, and engineering executives.

## Problem Statement
The repository has deep internal contracts but the public documentation behaves like a compact reference. It assumes unfamiliar terms, exposes contradictory installation paths, summarizes rather than teaches the lifecycle, covers many skills only through generated frontmatter cards, and does not let a reader distinguish human decisions, agent instructions, and terminal commands. As a result, junior readers cannot complete a first workflow, leads cannot verify full skill/script coverage or recovery behavior, and executives cannot make an informed adoption decision.

## Scope
In scope:
- Establish one canonical public documentation layer under `docs/`.
- Reorder the README and site around why, fit, foundations, guided onboarding, lifecycle flows, skill guides, operations, adoption, and exact reference.
- Define SDLC, AI SDLC, SDD, the harness, skills, flows, artifacts, evidence, gates, handoffs, TOON, policy, runtime, and recovery before operational use.
- Publish beginner, practitioner, maintainer, and executive reading paths.
- Provide reproducible small-change and full-feature walkthroughs.
- Cover the complete discovered skill inventory (44 capabilities after the portable runtime addition) and all executable Python helpers through generated, validated references.
- Document the 18-stage refinement lifecycle, implementation SDD, control-plane flows, role authority, governance, adoption metrics, limitations, troubleshooting, extension, and release operations.
- Add deterministic completeness and command-existence validation.
- Use independent junior, lead, and VP persona reviews as release gates.

## Actors
- New or junior engineer: needs definitions, safe copyable steps, expected results, and explicit stop conditions.
- Senior, Staff, or Lead engineer: needs architecture, authority, lifecycle, recovery, script behavior, and complete capability coverage.
- PM, BA, QA, Delivery, Dev, Security, Architecture, and Release practitioners: need role-specific entry points, owned artifacts, gates, and handoffs.
- Platform engineer or harness maintainer: needs installation, extension, compatibility, validation, and troubleshooting contracts.
- Engineering manager, Head of Delivery, or VP Engineering: needs fit, non-goals, governance, pilot design, outcome signals, risks, rollout, and exit criteria.
- AI agent: consumes explicit skill instructions and TOON projections, runs deterministic helpers, preserves evidence, and stops at human authority boundaries.

## Inputs
- Current MkDocs Material site, README, root concepts and guides.
- All `skills/*/SKILL.md` packages, their scripts, references, tests, module manifests, compatibility baseline, and public data contracts.
- Existing 18-stage refinement registry and implementation SDD contracts.
- Persona findings from junior, lead, and VP reviewers.
- Release 1.1 behavior, TOON-first representation rules, and current installation mechanisms.

## Outputs
- A canonical guided public documentation site and reordered README.
- Foundation, onboarding, lifecycle-flow, role/authority, adoption/governance, limitations, troubleshooting, contributor, glossary, and worked-example pages.
- One generated human-facing detail page for every installed skill and a complete script/control-plane reference.
- Updated Material navigation and index pages with separate evaluate/adopt and use/build paths.
- Deterministic documentation coverage manifests/tests and working installation instructions.
- Persona review evidence showing PASS for junior, lead, and VP readers.

## Functional Requirements
FR-001: Explain conventional SDLC, AI-assisted failure modes, AI SDLC, SDD, and the harness using plain language and a concrete request-to-commit example.
FR-002: State target users, prerequisites, supported usage model, non-goals, maturity, limitations, and accountable-human boundaries before installation.
FR-003: Provide one canonical, executable install path and clearly distinguish source checkout, installed agent skills, and the consumer repository.
FR-004: Label instructions as Tell your agent, Run in terminal, Agent does automatically, or Human checkpoint.
FR-005: Provide a runnable small-change tutorial and a medium/full-feature tutorial with setup, exact prompts, expected artifacts, checkpoints, failure/recovery, validation, and cleanup.
FR-006: Publish the exact 18-stage refinement lifecycle plus implementation, validation/release, controlled-change, runtime/automation, recovery/learning, and operations flows. Each flow defines entry, owner, inputs, sequence, artifacts, gates, exit, handoff, and reopen conditions.
FR-007: Generate a detail page for every discovered capability with why/when, do-not-use, roles, prerequisites, prompt, inputs, outputs/paths, mutability/authority, modes, scripts, success, blockers, recovery, handoff, and examples.
FR-008: Inventory all package and shared Python scripts with owner, purpose, caller, mutability, inputs, important flags/defaults, outputs, exit behavior, retry/recovery, and copyable invocation.
FR-009: Publish role paths and a human/agent RACI covering every material lifecycle gate, approvals, escalation, and small-team role collapse.
FR-010: Publish an adoption playbook for a bounded one-team/one-repo pilot with baseline, owner, 2–4 week checkpoints, leading/lagging metrics, qualitative evidence, thresholds, rollback, and scale decision.
FR-011: Publish a unified governance/trust model covering data, secrets, permissions, policy, packages, approvals, failures, exceptions, retention, regulatory limits, and incident response.
FR-012: Publish a glossary and link core terms at first meaningful use on beginner pages.
FR-013: Publish troubleshooting for install failure, invalid/corrupt state, stale indexes, state/artifact contradictions, interrupted writes, divergent paths, predecessor blocks, dirty Git, unsupported hosts, exhausted budgets, and non-zero helper exits.
FR-014: Publish a maintainer path for skill/module creation, scripts, references, schemas, tests, catalogs, compatibility, release, deprecation, and rollback.
FR-015: Make benefits and proof claims honest: distinguish validated mechanism behavior from expected organizational outcomes and state known constraints.
FR-016: Preserve exact technical references and TOON-first/JSON-boundary contracts without forcing implementation detail into the beginner journey.

## Non-Functional Requirements
- Clarity: core beginner pages use plain English, define acronyms, and avoid requiring `SKILL.md` reads.
- Discoverability: any skill is reachable within two navigation actions from the skill index; executive and practitioner paths are separated from Home.
- Completeness: generated coverage is inventory-complete for skills and 100% of in-scope executable Python helpers.
- Determinism: catalogs and coverage checks fail on drift, missing pages, stale navigation, undocumented scripts, or nonexistent local commands.
- Safety: no page instructs an agent to approve protected actions, erase authoritative evidence, expose secrets, or guess missing decisions.
- Consistency: `docs/` is the canonical public source; README, concepts, and guides point to it or are explicitly repository-internal sources without competing user guidance.
- Portability: concepts remain host-agnostic and distinguish agent prompts from shell commands.
- Accessibility: headings, tables, code labels, admonitions, link text, and diagrams remain readable in light/dark themes and without visual-only meaning.
- Build quality: strict MkDocs build, rendered-link validation, documentation tests, compatibility checks, and whitespace checks pass.

## Constraints
- Product behavior and public harness API remain unchanged unless documentation validation exposes a real broken contract such as the nonexistent installer.
- Generated skill pages derive from authoritative `SKILL.md` packages; they must not become a competing execution contract.
- JSON remains limited to schema/interoperability/recovery boundaries and JSONL journals; public agent examples remain TOON-first.
- No outcome or ROI claim may be presented as measured evidence without a reproducible source.
- Existing release and compatibility history must remain valid.
- The work follows one bounded task per commit and retains an auditable SDD task map.
- Public documentation remains English for this delivery; localization is separate work.

## Acceptance Criteria
AC-001: A first-time reader can explain SDLC, AI SDLC, SDD, the harness, artifact, evidence, gate, flow, and handoff after the foundation path, and identify at least three non-goals.
AC-002: README and Home expose separate Evaluate/adopt and Learn/use paths, and each reaches the relevant decision or first action within two clicks.
AC-003: A clean-environment reader can follow one canonical install path, verify installed skills, identify source versus consumer repositories, and safely update or roll back; every referenced local executable exists.
AC-004: The small-change tutorial is copyable end to end and includes terminal commands, agent prompts, expected response shapes, file trees, artifact excerpts, human checkpoints, validation, one deliberate failure/recovery, and final commit evidence.
AC-005: The full-feature tutorial demonstrates discovery/refinement, SDD, QA, implementation, validation, release evidence, and learning with explicit stage ownership and handoffs.
AC-006: The lifecycle reference covers all 18 refinement stages and every implementation/control-plane branch with predecessor, owner, input, artifact, exit gate, next consumer, and reopen condition; it distinguishes single-skill full flow from a full lifecycle cascade.
AC-007: Generated public guides cover exactly every installed skill and require all defined detail fields; adding a skill without a complete guide fails validation.
AC-008: Generated script reference covers every in-scope Python helper and requires purpose, caller, mutability, inputs, flags/defaults, outputs, exit behavior, retry/recovery, and example; adding an undocumented script fails validation.
AC-009: Every material gate identifies accountable human, agent-permitted work, prohibited autonomous action, evidence, and escalation owner.
AC-010: The adoption playbook lets a VP decide fit/non-fit, run a bounded pilot, interpret metrics without overstating causality, stop/roll back, or approve scale.
AC-011: Governance documentation covers human authority, trust boundaries, secrets/privacy, package provenance, policy/waivers, incident response, retention, limitations, and regulatory caveats with links to enforcement details.
AC-012: Troubleshooting contains safe diagnosis and recovery for all enumerated failure classes and never recommends deleting authoritative evidence.
AC-013: One canonical glossary covers all core acronyms and terms; beginner pages expand or link them at first meaningful use.
AC-014: Documentation tests reject broken local commands, missing persona paths, incomplete skill/script coverage, missing lifecycle stages, stale catalogs, broken links, and duplicate canonical concept routes.
AC-015: Strict source and rendered documentation validation, skill regression tests affected by generator changes, SDD gates, compatibility, and prohibited-name search pass.
AC-016: Independent junior, lead, and VP persona rereads each return PASS with no unresolved P0 or P1 finding.
AC-017: Documentation clearly states maturity, current proof, expected-but-unproven outcomes, known limitations, support boundaries, and non-goals.
AC-018: All completed implementation tasks map one-to-one to focused commits.

## Out of Scope
- Changing the core delivery algorithms, schemas, skill semantics, or harness API.
- Adding an IDE, SaaS control plane, hosted telemetry, autonomous approvals, deployment authority, project-management replacement, or CI replacement.
- Claiming guaranteed software correctness, compliance certification, or measured organizational ROI.
- Translating the site into languages other than English.
- Replacing authoritative skill contracts with public prose.
- Creating a new package manager or installer when the existing Skills CLI path works.

## Assumptions
- The public documentation language remains English because the repository and existing site are English.
- `npx skills add/use` is the canonical consumer installation mechanism; source checkout is for contributors and local preview.
- The discovered skill packages and current Python helpers are authoritative inventory sources; fixed counts are evidence, not configuration.
- Material for MkDocs remains the site generator and GitHub Pages remains the publishing target.
- Existing concepts and guides may be migrated, consolidated, or converted into pointers when public `docs/` becomes canonical.
- Persona reviewers represent usability gates, not claims of formal user research.

## Open Questions
No blocking product questions remain. Implementation may choose the exact page split and navigation labels as long as all acceptance criteria remain traceable. Real organizational ROI data is not available and must be labeled as a pilot hypothesis rather than invented.

## Decision Status
All blocking decisions are resolved for implementation. Accepted assumptions are listed above. DEC-001 establishes `docs/` as the single canonical public documentation layer; generated skill/script detail must derive from repository contracts; the canonical install path is the Skills CLI; and junior, lead, and VP PASS are required before completion.
