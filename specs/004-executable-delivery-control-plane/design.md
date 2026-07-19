---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-executable-delivery-control-plane"
  artifact: "design.md"
  path: "specs/004-executable-delivery-control-plane/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/004-executable-delivery-control-plane/_ai_sdlc/state.toon"
  decision_log: "specs/004-executable-delivery-control-plane/decision-log.md"
  status: "approved"
  owner: "Dev"
  created_at: "2026-07-19"
  updated_at: "2026-07-19"
  trace_ids: []
  related_artifacts:
    - "specs/004-executable-delivery-control-plane/decision-log.md"
    - "specs/004-executable-delivery-control-plane/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
---

# Design

## Overview
The control plane extends the existing repository-local harness through additive versioned contracts and deterministic Python CLIs. It separates proposed intent from canonical truth, materializes lifecycle traceability as a generated graph, evaluates policy before mutation, builds bounded context packs, and persists workflow execution so any supported host can resume safely.

## Architecture
Five layers remain separable. Artifact layer owns authoritative Markdown and compact machine projections. Analysis layer parses deltas, trace links, repository topology, freshness, policies, and packages without mutation. Control layer evaluates gates, budgets, dependencies, and state transitions. Execution layer applies approved mutations atomically and delegates host-specific actions through adapters. Experience layer exposes skills, CLI output, generated documentation, diagnostics, and metrics. Shared schemas and helpers live under skills/_shared while user-facing capability packages own their instructions, scripts, references, and tests.

## Components
- Change lifecycle: change-set skill plus schema, workspace planner, delta validator, preview, atomic apply, and archive helpers.
- Delivery graph: deterministic indexer, trace query, gap analysis, freshness propagation, and evidence ledger.
- Policy engine: layered rules, protected controls, action evaluation, waiver lifecycle, profiles, and explain output.
- Context Engine v2: repository topology, conditional selectors, budget allocator, freshness-aware task packs, and secret exclusions.
- Runtime: run state, journal, ready-task selection, budgets, retries, workflow DAG, gates, hooks, wave planner, and commit boundary enforcement.
- Adapter SDK: capability manifest, negotiation, operation mapping, fallbacks, and host conformance fixtures.
- Operations: installation doctor, upgrade planner, migration registry, backup and rollback plan, package trust, metrics, and versioned docs.

## Interfaces and Contracts
All new records use versioned schemas and stable IDs. Commands support human Markdown or JSON output and compact TOON where useful. Read-only analyze, validate, preview, plan, query, doctor, and metrics operations never alter authoritative inputs. Mutating create, apply, archive, migrate, and runtime transition operations require explicit destinations, policy permission, and atomic writes. Host adapters implement capability discovery and a bounded operation contract rather than embedding host prompts in core logic.

## Data Model
ChangeSet records identity, status, canonical targets, delta operations, scenarios, decisions, approvals, evidence, conflicts, and archive identity. Graph records typed nodes and directed trace, dependency, evidence, ownership, and freshness edges. Policy records scopes, rules, protected flags, gates, waivers, versions, and provenance. ContextPack records task, budget, selected anchors, exclusions, reasons, freshness, and fingerprint. Run records workflow version, inputs, step and task states, budgets, approvals, journal events, artifacts, commits, and resume cursor. Package records origin, version, compatibility, digest, capabilities, trust decision, and installation history.

## Error Handling
Validators accumulate file-scoped structural and semantic diagnostics. Preview reports conflicts instead of guessing. Mutations stage content in the destination filesystem and replace targets only after all validations pass. Runtime failures persist a failed or paused state with retry eligibility and never mark incomplete tasks done. Unknown policy, host capability, package trust, or freshness inputs fail closed when they could weaken protection; otherwise they produce an explicit conservative fallback.

## Security Considerations
Canonical and policy mutations require explicit authority. Waivers are scoped, owned, reasoned, time-bounded, and auditable. External workflow and package inputs are untrusted, confined to declared capabilities, and never imply shell or network authority. Context scanning excludes secret-named, environment, key, token, credential, binary, generated, and configured sensitive paths. Metrics contain identifiers, durations, counts, statuses, and fingerprints rather than source content.

## Observability
Every control decision emits a stable reason code and evidence anchor. Run journals are append-only JSONL with deterministic sequence numbers and a summarized TOON state. Change archive retains preview fingerprint, approvals, applied target hashes, validation evidence, and commit references. Metrics aggregate run and graph records locally. Doctor and upgrade operations report exact checks, affected paths, planned migrations, backups, and rollback actions.

## Risks and Tradeoffs
A broad control plane can become rigid or token-heavy. Mitigation is adaptive rigor, optional modules, compact indexes, conditional context, and progressive validation. Generated graph data can drift; fingerprints and rebuild checks make staleness explicit. Workflow execution can overreach; capability declarations, policy gates, preview, and host-owned execution retain boundaries. Atomic multi-file updates are limited by filesystem semantics; staged writes, backups, and recovery manifests reduce partial-failure risk.

## Validation Strategy
Each task adds unit fixtures for pure contracts, integration fixtures across existing state and artifacts, negative tests for unsafe or stale inputs, compatibility checks, docs validation, and git diff checks. Core deterministic suites remain dependency-free. Program-level completion runs all skill tests, source compatibility validation, documentation generation and tests, strict MkDocs build, schema migration fixtures, and a Git audit mapping T-IDs to exactly one commit each.

## Migration Notes
All capability is additive during this program. Existing specs remain valid without change workspaces or graph indexes. Existing project context and configuration schemas remain readable and migrate only through explicit new-version writers. New runtime and package records live in dedicated machine directories and can be removed without altering authoritative Markdown. Deprecations require a separate accepted decision and documented compatibility window.
