---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-executable-delivery-control-plane"
  artifact: "tasks.md"
  path: "specs/004-executable-delivery-control-plane/tasks.md"
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
    - "AC-015"
    - "DEC-001"
    - "DEC-002"
  related_artifacts:
    - "specs/004-executable-delivery-control-plane/decision-log.md"
    - "specs/004-executable-delivery-control-plane/design.md"
    - "specs/004-executable-delivery-control-plane/plan.md"
    - "specs/004-executable-delivery-control-plane/qa.md"
    - "specs/004-executable-delivery-control-plane/requirements.md"
    - "specs/004-executable-delivery-control-plane/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "approved"
---

# Tasks

## Implementation
- [x] T001. Define and validate the executable delivery control-plane program.
  Output: Complete SDD package, accepted decisions, registered roadmap, generated plans and indexes, validation evidence, and one focused planning commit.
  Refs: AC-013, AC-014, DEC-001, DEC-002
- [x] T002. Implement the isolated ChangeSet workspace contract.
  Output: ChangeSet skill, versioned schemas, deterministic workspace creator and validator, fixtures, tests, and documentation.
  Refs: AC-001, AC-013, DEC-001
- [x] T003. Implement requirement delta parsing and semantic validation.
  Output: Added, modified, removed, and renamed operation parser; scenario and target validation; overlap detection; tests; and documentation.
  Refs: AC-001, AC-002, AC-013
- [x] T004. Implement non-mutating apply preview and conflict analysis.
  Output: Deterministic preview plan, target diffs, downstream staleness and reopen analysis, policy gate discovery, conflict reasons, tests, and documentation.
  Refs: AC-002, AC-013
- [x] T005. Implement policy-gated atomic apply and archive.
  Output: Staged multi-file apply, approval checks, archive record, recovery manifest, repeat protection, fault-injection tests, and documentation.
  Refs: AC-003, AC-015, AC-013
- [x] T006. Implement the repository delivery graph and trace queries.
  Output: Versioned node and edge schemas, deterministic indexer, trace and gap queries, orphan detection, tests, and documentation.
  Refs: AC-004, AC-013
- [x] T007. Implement the evidence ledger and freshness propagation.
  Output: Evidence identity and fingerprint contract, dependency-aware staleness propagation, coverage queries, tests, and documentation.
  Refs: AC-004, AC-008, AC-013
- [x] T008. Implement versioned policy-as-code and waiver lifecycle.
  Output: Layered policy schema and resolver, protected rules, action evaluator, explain output, expiring waiver contract, organization profiles, tests, and documentation.
  Refs: AC-007, AC-015, AC-013, DEC-002
- [ ] T009. Implement Context Engine v2 and bounded task packs.
  Output: Repository ownership and test topology, conditional selectors, token budget allocator, freshness-aware context packs, secret exclusions, tests, and documentation.
  Refs: AC-008, AC-013
- [ ] T010. Implement the resumable task runtime core.
  Output: Versioned run state and journal, ready-task selection, budgets, retries, stop reasons, resume and idempotency behavior, commit-boundary contract, tests, and documentation.
  Refs: AC-005, AC-015, AC-014
- [ ] T011. Implement declarative workflows, gates, hooks, and dependency waves.
  Output: Workflow schema and validator, typed step planner, conditions, approval gates, deterministic hooks, cycle detection, safe wave planning and fallbacks, tests, and documentation.
  Refs: AC-005, AC-006, AC-007, AC-013
- [ ] T012. Implement the host adapter SDK and capability negotiation.
  Output: Adapter manifest and operation contract, negotiation and fallback engine, conformance fixtures for representative hosts, tests, and documentation.
  Refs: AC-006, AC-009, AC-013
- [ ] T013. Implement installation doctor and safe upgrade planning.
  Output: Environment diagnostic registry, compatibility checks, file and schema change preview, backup and rollback plan, migration fixtures, tests, and documentation.
  Refs: AC-010, AC-013
- [ ] T014. Implement package trust and privacy-preserving local metrics.
  Output: Package origin, integrity, compatibility, capability and provenance validation; local run and quality aggregates; privacy tests; and documentation.
  Refs: AC-011, AC-012, AC-013
- [ ] T015. Complete versioned documentation, compatibility, release, and commit audit.
  Output: Final integration docs, release-version navigation, migration guide, generated catalogs, full validation evidence, task-to-commit audit, branch publication, main integration, and release tag.
  Refs: AC-013, AC-014

## Testing
Each T-ID includes its focused unit, integration, negative, recovery, compatibility, and documentation checks. T001 validates the SDD package. T002 through T014 validate one bounded capability per commit. T015 runs the complete regression, strict documentation build, migration fixtures, commit audit, and release verification.

## Documentation
Every capability task updates its package documentation and public concept, how-to, or reference surface in the same focused commit. T015 reconciles navigation, versioning, migration, generated catalogs, roadmap status, and release notes without hiding residual risks.
