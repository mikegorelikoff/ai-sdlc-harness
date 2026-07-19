---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-executable-delivery-control-plane"
  artifact: "test-cases.md"
  path: "specs/004-executable-delivery-control-plane/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/004-executable-delivery-control-plane/_ai_sdlc/state.toon"
  decision_log: "specs/004-executable-delivery-control-plane/decision-log.md"
  status: "approved"
  owner: "QA"
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
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-010"
    - "TC-011"
    - "TC-012"
    - "TC-013"
    - "TC-014"
    - "TC-015"
  related_artifacts:
    - "specs/004-executable-delivery-control-plane/decision-log.md"
    - "specs/004-executable-delivery-control-plane/design.md"
    - "specs/004-executable-delivery-control-plane/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "approved"
---

# Test Cases

## Scope
Validate change isolation and delta semantics; conflict-free apply and archive; graph traceability and evidence freshness; policy and waiver safety; bounded context; resumable execution, workflow dependencies, hooks, and fallbacks; host negotiation; installation and migration planning; package trust; metrics privacy; documentation, compatibility, and commit traceability.

## Scenario Matrix
- TC-001 / AC-001: create valid and incomplete change-set fixtures; expect complete isolated workspace output and structural rejection without canonical writes.
- TC-002 / AC-002: preview added, modified, removed, renamed, stale-target, and overlapping deltas twice; expect identical plans, conflicts, gates, and no mutations.
- TC-003 / AC-003: apply an approved delta, archive it, retry it, and inject a staged-write failure; expect atomic canonical state, retained evidence, safe repeat behavior, and recovery data.
- TC-004 / AC-004: index representative lifecycle artifacts and query requirement-to-commit and requirement-to-evidence paths; expect stable nodes, edges, gaps, coverage, and stale propagation.
- TC-005 / AC-005: interrupt runs at ready, executing, validation, approval, and commit boundaries; expect exact safe resume without duplicate completed work.
- TC-006 / AC-006: plan acyclic, cyclic, isolated, and isolation-unsupported task graphs; expect correct waves, cycle diagnostics, and sequential fallback.
- TC-007 / AC-007: evaluate layered allow, deny, protected minimum, missing input, valid waiver, expired waiver, and weakening fixtures; expect deterministic decisions and provenance.
- TC-008 / AC-008: build task packs across small, large, stale, secret-bearing, and over-budget repositories; expect bounded explained selections, exclusions, fingerprints, and freshness warnings.
- TC-009 / AC-009: negotiate full, partial, unknown, and incompatible host manifests; expect stable mappings or explicit fallbacks and failures.
- TC-010 / AC-010: run doctor and upgrade preview against compatible, missing-tool, incompatible-schema, and rollback fixtures; expect no mutation and complete diagnostic and recovery plans.
- TC-011 / AC-011: validate trusted, tampered, incompatible, undeclared-capability, unknown-origin, and upgrade package fixtures; expect fail-closed trust decisions with provenance.
- TC-012 / AC-012: aggregate completed, retried, blocked, stale, and empty runs; expect reproducible content-free metrics and explicit insufficient-data states.
- TC-013 / AC-013: run full compatibility, skill, documentation, build, schema, and migration suites; expect all current and new contracts to pass.
- TC-014 / AC-014: audit commits from program base to head against completed T-IDs; expect exactly one focused commit per task and no missing or duplicate mappings.
- TC-015 / AC-005, AC-007: attempt runtime mutation without satisfied policy or approval; expect a persisted blocked state, no authoritative writes, and actionable reason codes.

## Layer Mapping
Pure schema, parser, policy, budget, dependency, graph, trust, and metrics behavior uses unit tests. Change apply, archive, context, runtime resume, adapters, doctor, migrations, documentation generation, and commit audit use integration tests. Filesystem failure, stale evidence, compatibility, and unsafe capability cases use negative and recovery fixtures. Host processes and network services are represented through deterministic adapters rather than required external calls.

## Automation Plan
Every task adds tests under its capability package or skills/_shared and registers them in existing discovery. Reusable fixtures cover authoritative Markdown, machine projections, Git metadata, policies, manifests, and run journals. Focused task validation runs before its commit. Program completion runs python3 -m unittest discover for shared and skill tests, compatibility validation, documentation catalog and source checks, mkdocs build --strict, git diff --check, and the task-to-commit audit.

## Open Gaps
Real multi-process host execution, remote registries, and cross-repository network coordination remain adapter concerns and are not required for deterministic core acceptance. Initial confidence comes from conformance fixtures and safe fallback behavior; optional live adapter smoke may be added when a supported host runtime is available.
