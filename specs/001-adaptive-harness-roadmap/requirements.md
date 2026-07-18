---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-adaptive-harness-roadmap"
  artifact: "requirements.md"
  path: "specs/001-adaptive-harness-roadmap/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/001-adaptive-harness-roadmap/_ai_sdlc/state.toon"
  decision_log: "specs/001-adaptive-harness-roadmap/decision-log.md"
  status: "approved"
  owner: "Dev"
  created_at: "2026-07-18"
  updated_at: "2026-07-18"
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
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
  related_artifacts:
    - "specs/001-adaptive-harness-roadmap/decision-log.md"
    - "specs/001-adaptive-harness-roadmap/design.md"
    - "specs/001-adaptive-harness-roadmap/plan.md"
    - "specs/001-adaptive-harness-roadmap/qa.md"
    - "specs/001-adaptive-harness-roadmap/tasks.md"
    - "specs/001-adaptive-harness-roadmap/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "approved"
---

# Requirements

## Goal
Deliver a guided, adaptive, extensible AI SDLC operating layer while preserving the existing deterministic evidence and continuity model.

## Problem Statement
The harness has strong lifecycle state, traceability, artifact routing, and deterministic validation, but users must already know which of 26 skills to invoke and must choose between only quick and full rigor. Cross-cutting project memory, quality lenses, change recovery, customization, optional domain modules, and independent review orchestration are not first-class capabilities.

## Scope
- Add a context-aware navigator and post-workflow recommendations.
- Add explainable risk-adaptive rigor profiles while retaining explicit quick and full overrides.
- Add evidence-backed project context, reusable quality lenses, change-impact recovery, retrospective learning, layered customization, optional module foundations, Architecture, UX, Research capabilities, and an evidence council.
- Document and validate compatibility, install, and update contracts.

## Actors
- Software delivery practitioners invoking skills.
- AI assistants and agent runners consuming repository-local control records.
- Team maintainers configuring organization policy.
- Skill and module authors extending the harness.

## Inputs
- Natural-language task intent.
- Repository state, Git diff, specs indexes, state.toon, plan.toon, decision logs, and artifact metadata.
- Team and user configuration.
- Optional domain module manifests and project-context evidence.

## Outputs
- Ranked next-action recommendations with reasons and exact commands.
- Adaptive rigor decisions with inspectable factors and safe overrides.
- Durable Markdown and TOON context, evidence, configuration, module, change, retrospective, and council artifacts.
- Backward-compatible skill behavior with deterministic validation.

## Functional Requirements
- FR-001: The navigator shall inspect installed capabilities and repository control records and return prioritized required and optional next actions.
- FR-002: Every durable workflow shall expose a common post-workflow handoff contract.
- FR-003: The rigor engine shall classify work as patch, standard, assured, or regulated from explicit risk factors and explain the result.
- FR-004: Explicit quick and full flow flags shall remain supported and shall override automatic selection.
- FR-005: Project context shall be generated as human-readable Markdown and bounded TOON with source evidence and drift identity.
- FR-006: Reusable quality lenses shall produce traceable findings linked to requirements, tests, decisions, owners, and resolution status.
- FR-007: Change-impact analysis shall identify stale artifacts and safe lifecycle reopen actions.
- FR-008: Retrospectives shall create reviewable improvement proposals and shall not silently change policy.
- FR-009: Layered team and user customization shall resolve deterministically with provenance and validation.
- FR-010: Optional modules shall be discoverable through a validated manifest contract without bloating core installation.
- FR-011: Architecture, UX, and Research capabilities shall be available as optional domain skills.
- FR-012: Evidence council shall support simulated and independent review modes while protecting authoritative artifacts from direct panel writes.
- FR-013: Install and update compatibility contracts shall be documented and mechanically testable.

## Non-Functional Requirements
- NFR-001: Core routing and configuration results shall be deterministic for identical repository state and inputs.
- NFR-002: Machine outputs shall support bounded TOON and human outputs shall remain readable Markdown.
- NFR-003: Existing installed skill names, quick/full flags, canonical artifact paths, and state files shall remain backward compatible unless a migration is explicitly documented.
- NFR-004: New Python helpers shall use the standard library unless a dependency is explicitly justified.
- NFR-005: Every task shall be validated and committed separately.
- NFR-006: Safety or governance requirements shall never be silently downgraded by adaptive routing or customization.

## Constraints
- Work is repository-local and agent-agnostic.
- The repository currently uses main as its only shared branch, so the program branch is based on main.
- Existing Markdown artifacts remain authoritative for detailed delivery truth.
- Existing TOON state, indexes, context packs, plans, migrations, and deterministic helper scripts remain the control-plane foundation.

## Acceptance Criteria
- AC-001: Given an empty or existing project, when the navigator runs, then it reports detected context, one ranked required action, optional actions, reasons, exact invocation names, expected outputs, and blockers in Markdown and TOON.
- AC-002: Given any completed durable workflow, when its handoff is emitted, then result, blockers, next_required, next_optional, reason, command, and expected_artifact fields are present.
- AC-003: Given explicit risk inputs, when rigor classification runs twice, then both runs select the same profile and expose factor scores, escalation reasons, and effective override.
- AC-004: Given an explicit full flow or mandatory organization minimum, when automatic classification suggests lower rigor, then the effective profile is not downgraded.
- AC-005: Given an established repository, when project context is generated, then Markdown and TOON outputs contain evidence paths, validation commands, architecture constraints, generation revision, and drift status.
- AC-006: Given an artifact and selected quality lens, when the lens report is finalized, then every finding has evidence, severity, trace targets, owner, resolution status, and next action.
- AC-007: Given a changed requirement or decision, when change impact runs, then affected artifacts and lifecycle stages are identified and reopen actions require evidence.
- AC-008: Given completed delivery work, when retrospective runs, then observations and improvement proposals are separated and policy remains unchanged until an accepted decision exists.
- AC-009: Given base, team, and user configuration, when resolution runs, then precedence and provenance are deterministic and weakening a protected gate fails validation.
- AC-010: Given core and optional module manifests, when discovery runs, then compatible skills are listed without requiring optional modules in core.
- AC-011: Given requests for architecture, UX, or research work, when the matching optional skill is invoked, then it produces routed, traceable artifacts with deterministic tests.
- AC-012: Given a review topic, when evidence council runs in simulated or independent mode, then the report distinguishes agreements, conflicts, evidence, proposals, owners, and unresolved questions and does not directly rewrite authoritative artifacts.
- AC-013: Given a release candidate, when compatibility validation runs, then existing skill names, flow flags, artifact routing, config schema, and module contracts are checked.
- AC-014: Given the program backlog, when work is committed, then each task is represented by exactly one focused commit and its validation evidence is recorded.

## Out of Scope
- Replacing issue trackers, source control, CI, or deployment systems.
- Mandatory fictional personas or conversational menus.
- A remote hosted marketplace service.
- Automatic stakeholder approval.
- Direct production integration execution.
- Breaking current artifact authority or lifecycle recovery rules.

## Assumptions
- The agreed roadmap is authoritative for initial scope.
- Standard-library Python and existing repository patterns are sufficient for the first implementation.
- Optional independent-agent execution can be described through a portable orchestration contract even when a host does not expose multi-agent primitives.
- The program can use quick-flow SDD because the user explicitly authorized the complete roadmap and each task retains its own validation and commit gate.

## Open Questions
- None blocking. Product naming and exact optional module packaging may be refined within the compatibility constraints and recorded in the decision log.

## Decision Status
- All blocking decisions are resolved for implementation.
- DEC-001 accepts a navigator-first architecture over adding more disconnected skills.
- DEC-002 accepts risk dimensions rather than story count as the adaptive rigor basis.
- DEC-003 accepts one program branch with one focused commit per task because the repository has no dev branch.
