---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-executable-delivery-control-plane"
  artifact: "requirements.md"
  path: "specs/004-executable-delivery-control-plane/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/004-executable-delivery-control-plane/_ai_sdlc/state.toon"
  decision_log: "specs/004-executable-delivery-control-plane/decision-log.md"
  status: "approved"
  owner: "Dev"
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
    - "DEC-001"
    - "DEC-002"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
    - "NFR-008"
  related_artifacts:
    - "specs/004-executable-delivery-control-plane/decision-log.md"
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
Turn the repository-local AI SDLC Harness into an executable delivery control plane that manages living specification changes, policy enforcement, traceability, resumable task execution, bounded context, host interoperability, and operational upgrades while preserving human-readable artifact authority and deterministic evidence.

## Problem Statement
The harness has strong lifecycle skills, state, decisions, adaptive rigor, evidence, and compatibility controls, but change evolution and execution remain distributed across human-invoked workflows. Teams cannot yet represent proposed specification deltas separately from canonical truth, preview and apply them under policy, query end-to-end delivery traceability, resume a bounded task loop, or diagnose upgrades through one portable runtime.

## Scope
- Add a controlled change workspace with proposal, design, tasks, requirement deltas, evidence, state, preview, apply, and archive semantics.
- Add a repository-wide delivery graph joining goals, requirements, decisions, components, tasks, tests, evidence, commits, and releases.
- Add a resumable workflow and task runtime with dependency waves, budgets, gates, hooks, journals, and one-task-one-commit enforcement.
- Add versioned policy-as-code with explainable evaluation, protected minimums, waivers, and reusable high-assurance profiles.
- Extend project context with conditional source selection, ownership and test topology, freshness propagation, and task-specific context packs.
- Add host adapter contracts, installation diagnostics, upgrade preview and rollback planning, module provenance, metrics, and versioned documentation.

## Actors
- Maintainers evolving the harness and its schemas.
- Delivery teams proposing and implementing changes in brownfield repositories.
- PM, BA, QA, Security, Architecture, Delivery, and Dev owners approving controlled transitions.
- AI assistants and workflow runners consuming portable contracts.
- Organization administrators defining protected policy and trusted modules.

## Inputs
- Existing specs, refinement artifacts, state.toon, plan.toon, decision logs, validation evidence, project context, configuration, and module manifests.
- Git revision, branch, commit, file-change, dependency, ownership, and test evidence.
- User change intent, runtime budgets, organization policy, host capabilities, and approval decisions.
- Official researched patterns from living-spec, workflow-runner, steering, hook, and modular lifecycle systems.

## Outputs
- Versioned change-set, delta, policy, graph, runtime, context-pack, adapter, diagnostic, provenance, and metrics schemas.
- Deterministic CLIs and reusable skills for creating, validating, previewing, applying, archiving, querying, executing, diagnosing, and explaining those records.
- Human-readable Markdown remains authoritative while compact JSON or TOON projections support machines.
- Focused tests, documentation, migration guidance, and one validated commit per implementation task.

## Functional Requirements
- FR-001: The harness shall create and validate isolated change workspaces without mutating canonical specifications.
- FR-002: The delta engine shall support added, modified, removed, and renamed requirements with scenario completeness and conflict checks.
- FR-003: Apply preview shall report canonical changes, stale downstream artifacts, policy gates, conflicts, and required reopen actions.
- FR-004: Controlled apply and archive shall update canonical truth only after validation and required approvals while preserving immutable change evidence.
- FR-005: A delivery graph shall index and query trace links across lifecycle artifacts, tests, evidence, commits, and releases and detect orphan or stale nodes.
- FR-006: A resumable runtime shall select ready tasks, assemble context, enforce policy, execute lifecycle stages, persist journals, and continue after interruption.
- FR-007: Workflow definitions shall support typed steps, dependencies, conditions, approval gates, hooks, sequential waves, and safe parallel task planning.
- FR-008: The runtime shall enforce configurable time, token, tool, retry, concurrency, and commit-boundary budgets with explainable stop reasons.
- FR-009: Policy evaluation shall resolve versioned layered rules, protected minimums, approvals, and expiring waivers with per-value provenance.
- FR-010: Context Engine v2 shall produce task-specific context packs from conditional sources, repository topology, evidence freshness, and explicit budgets.
- FR-011: Host adapters shall negotiate capabilities and map portable operations to supported assistant hosts or deterministic fallbacks.
- FR-012: Installation and upgrade tooling shall diagnose environment compatibility, preview writes and migrations, report risk, and produce rollback plans.
- FR-013: Module and workflow packages shall carry compatibility, origin, integrity, trust, and update provenance without requiring a remote marketplace.
- FR-014: Local metrics shall report cycle time, retries, rework, blocked reasons, coverage, freshness, and budget use without collecting source content.
- FR-015: Documentation shall describe the control-plane model, contracts, workflows, operations, and supported release versions.

## Non-Functional Requirements
- NFR-001: All core validators and planners shall be deterministic, offline-capable, dependency-light, and safe to run in CI.
- NFR-002: Human-readable Markdown remains authoritative; machine projections cannot silently replace or mutate it.
- NFR-003: Proposed changes, reviews, retrospective findings, and automated runtime outputs cannot alter canonical artifacts or protected policy without an accepted authority transition.
- NFR-004: Existing skills, quick and full flow flags, manifests, schemas, repository paths, and generated documentation remain backward compatible unless an explicit migration handles the break.
- NFR-005: Every mutation command shall support dry-run or preview semantics and produce actionable file-scoped diagnostics.
- NFR-006: Runtime state shall survive process interruption and context compaction without relying on chat history.
- NFR-007: External workflows and modules shall be untrusted by default and cannot gain undeclared filesystem, shell, network, approval, or policy authority.
- NFR-008: Each roadmap task shall be implemented, validated, and recorded in exactly one focused commit.

## Constraints
- The repository uses a main-based feature branch model because no dev branch exists.
- Core implementation uses the Python standard library unless a separately approved module justifies another dependency.
- Git history remains the authoritative commit record; the harness may index but not rewrite it.
- Safe parallel execution requires isolation capability; unsupported hosts fall back to sequential execution.
- No mandatory hosted service, telemetry endpoint, API key, or proprietary assistant feature is introduced.

## Acceptance Criteria
- AC-001: Given a proposed change, when its workspace is validated, then its proposal, delta operations, scenarios, tasks, evidence links, state, and authority boundaries are complete and canonical specs remain byte-identical.
- AC-002: Given valid and conflicting deltas, when preview runs, then deterministic output shows exact target changes, conflicts, stale artifacts, required gates, and reopen actions without writing targets.
- AC-003: Given an approved conflict-free change, when apply and archive run, then canonical specs are updated atomically, evidence and decisions are retained, and repeated application is safely rejected or idempotent.
- AC-004: Given repository lifecycle artifacts, when graph indexing runs twice, then identical nodes, edges, gaps, stale paths, and evidence coverage are produced and trace queries resolve end to end.
- AC-005: Given interrupted runtime state, when execution resumes, then completed steps are not repeated, the next ready task is selected, budgets and approvals remain enforced, and the journal explains every transition.
- AC-006: Given a dependency task graph, when waves are planned, then only dependency-independent tasks share a wave and unsupported isolation or host concurrency produces a safe sequential fallback.
- AC-007: Given layered policy and a requested action, when evaluation runs, then the decision, effective values, provenance, required gates, waiver state, and denial reasons are deterministic and protected rules cannot be weakened silently.
- AC-008: Given a bounded task, when Context Engine v2 builds a pack, then selected sources fit the budget, each inclusion is explained, sensitive paths are excluded, and upstream drift propagates freshness warnings.
- AC-009: Given different host capabilities, when adapter negotiation runs, then portable operations are mapped to supported features or explicit deterministic fallbacks without changing workflow semantics.
- AC-010: Given a current installation and target release, when doctor and upgrade preview run, then environment failures, file changes, schema migrations, compatibility risks, backups, and rollback commands are reported before mutation.
- AC-011: Given installed or candidate packages, when trust validation runs, then version compatibility, origin, integrity, declared capabilities, and update provenance are visible and unsafe packages fail closed.
- AC-012: Given completed and blocked runs, when metrics are generated, then local aggregate lifecycle, quality, freshness, and budget measures are reproducible without leaking source content.
- AC-013: Given existing consumers and documentation checks, when the program completes, then compatibility suites, skill tests, docs validation, strict site build, and migration tests pass.
- AC-014: Given the Git history for this program, when commits are audited, then every completed task maps to one focused commit and no commit combines multiple roadmap tasks.

## Out of Scope
- Building an IDE, hosted project-management service, remote marketplace, or general-purpose CI platform.
- Replacing Git, repository Markdown, existing issue trackers, or human approval ownership.
- Mandatory persona roleplay or hidden autonomous decision authority.
- Automatic merge, deployment, or destructive repository repair without explicit workflow and policy authorization.

## Assumptions
- The user authorizes quick-flow execution across the complete roadmap and prefers informed repository-aligned defaults over repeated non-material clarification.
- Existing artifact authority, adaptive rigor, configuration, state, module, navigator, evidence-council, validation, and commit contracts remain the foundation.
- One task means one independently testable capability slice represented by one T-ID and one commit; a task may contain its own tests and documentation.
- Main remains the integration branch and feature/004-executable-delivery-control-plane is the program branch.

## Open Questions
- Non-blocking: external host-specific SDKs and hosted registries may be added later through optional adapters.
- Non-blocking: parallel execution will initially plan isolated waves and expose adapter hooks; actual multi-process spawning remains host-owned.

## Decision Status
- All blocking product and architecture decisions for starting implementation are resolved.
- DEC-001 adopts the executable delivery control-plane direction and the ordered task program.
- DEC-002 preserves Markdown authority, deterministic previews, explicit approvals, safe fallbacks, and one-task-one-commit delivery.
