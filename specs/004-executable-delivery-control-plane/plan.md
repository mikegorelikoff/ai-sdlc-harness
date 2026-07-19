---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-executable-delivery-control-plane"
  artifact: "plan.md"
  path: "/Users/mikegorelikov/Documents/GitHub/ai-sdlc-harness/specs/004-executable-delivery-control-plane/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "/Users/mikegorelikov/Documents/GitHub/ai-sdlc-harness/specs/004-executable-delivery-control-plane/_ai_sdlc/state.toon"
  decision_log: "/Users/mikegorelikov/Documents/GitHub/ai-sdlc-harness/specs/004-executable-delivery-control-plane/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-07-19"
  updated_at: "2026-07-19"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "plan"
    - "draft"
---

# plan.md

## Upstream Refinement Sources
- Refinement index: `specs-refiniment/_ai_sdlc/specs-index.toon`
- Refinement state: `specs-refiniment/<feature-name>/_ai_sdlc/state.toon`
- Delivery spec: `specs-refiniment/<feature-name>/delivery-spec.md`
- QA readiness: `specs-refiniment/<feature-name>/qa-readiness.md`
- Decision trace: `decision-log.md`

## SDD Artifact Links
- Requirements: `requirements.md`
- Design: `design.md`
- Test cases: `test-cases.md`
- QA: `qa.md`
- Tasks: `tasks.md`
- Machine plan: `_ai_sdlc/plan.toon`
- Decision log: `decision-log.md`

## Cross-Artifact Trace Map
- AC-001: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T002, T003) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T003, T004) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T005) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T006, T007) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T010, T011) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T011, T012) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T008, T011) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T007, T009) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T012) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T013) -> qa.md -> decision-log.md
- AC-011: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T014) -> qa.md -> decision-log.md
- AC-012: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T014) -> qa.md -> decision-log.md
- AC-013: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T001, T002, T003, T004, T005, T006, T007, T008, T009, T011, T012, T013, T014, T015) -> qa.md -> decision-log.md
- AC-014: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015) -> tasks.md (T001, T010, T015) -> qa.md -> decision-log.md

## Task Execution Plan
- [ ] T001: - [x] T001. Define and validate the executable delivery control-plane program.; refs: AC-013, AC-014, DEC-001, DEC-002; output: Complete SDD package, accepted decisions, registered roadmap, generated plans and indexes, validation evidence, and one focused planning commit.
- [ ] T002: - [x] T002. Implement the isolated ChangeSet workspace contract.; refs: AC-001, AC-013, DEC-001; output: ChangeSet skill, versioned schemas, deterministic workspace creator and validator, fixtures, tests, and documentation.
- [ ] T003: - [ ] T003. Implement requirement delta parsing and semantic validation.; refs: AC-001, AC-002, AC-013; output: Added, modified, removed, and renamed operation parser; scenario and target validation; overlap detection; tests; and documentation.
- [ ] T004: - [ ] T004. Implement non-mutating apply preview and conflict analysis.; refs: AC-002, AC-013; output: Deterministic preview plan, target diffs, downstream staleness and reopen analysis, policy gate discovery, conflict reasons, tests, and documentation.
- [ ] T005: - [ ] T005. Implement policy-gated atomic apply and archive.; refs: AC-003, AC-015, AC-013; output: Staged multi-file apply, approval checks, archive record, recovery manifest, repeat protection, fault-injection tests, and documentation.
- [ ] T006: - [ ] T006. Implement the repository delivery graph and trace queries.; refs: AC-004, AC-013; output: Versioned node and edge schemas, deterministic indexer, trace and gap queries, orphan detection, tests, and documentation.
- [ ] T007: - [ ] T007. Implement the evidence ledger and freshness propagation.; refs: AC-004, AC-008, AC-013; output: Evidence identity and fingerprint contract, dependency-aware staleness propagation, coverage queries, tests, and documentation.
- [ ] T008: - [ ] T008. Implement versioned policy-as-code and waiver lifecycle.; refs: AC-007, AC-015, AC-013, DEC-002; output: Layered policy schema and resolver, protected rules, action evaluator, explain output, expiring waiver contract, organization profiles, tests, and documentation.
- [ ] T009: - [ ] T009. Implement Context Engine v2 and bounded task packs.; refs: AC-008, AC-013; output: Repository ownership and test topology, conditional selectors, token budget allocator, freshness-aware context packs, secret exclusions, tests, and documentation.
- [ ] T010: - [ ] T010. Implement the resumable task runtime core.; refs: AC-005, AC-015, AC-014; output: Versioned run state and journal, ready-task selection, budgets, retries, stop reasons, resume and idempotency behavior, commit-boundary contract, tests, and documentation.
- [ ] T011: - [ ] T011. Implement declarative workflows, gates, hooks, and dependency waves.; refs: AC-005, AC-006, AC-007, AC-013; output: Workflow schema and validator, typed step planner, conditions, approval gates, deterministic hooks, cycle detection, safe wave planning and fallbacks, tests, and documentation.
- [ ] T012: - [ ] T012. Implement the host adapter SDK and capability negotiation.; refs: AC-006, AC-009, AC-013; output: Adapter manifest and operation contract, negotiation and fallback engine, conformance fixtures for representative hosts, tests, and documentation.
- [ ] T013: - [ ] T013. Implement installation doctor and safe upgrade planning.; refs: AC-010, AC-013; output: Environment diagnostic registry, compatibility checks, file and schema change preview, backup and rollback plan, migration fixtures, tests, and documentation.
- [ ] T014: - [ ] T014. Implement package trust and privacy-preserving local metrics.; refs: AC-011, AC-012, AC-013; output: Package origin, integrity, compatibility, capability and provenance validation; local run and quality aggregates; privacy tests; and documentation.
- [ ] T015: - [ ] T015. Complete versioned documentation, compatibility, release, and commit audit.; refs: AC-013, AC-014; output: Final integration docs, release-version navigation, migration guide, generated catalogs, full validation evidence, task-to-commit audit, branch publication, main integration, and release tag.

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on previous applicable task / none
- T003: depends on previous applicable task / none
- T004: depends on previous applicable task / none
- T005: depends on previous applicable task / none
- T006: depends on previous applicable task / none
- T007: depends on previous applicable task / none
- T008: depends on previous applicable task / none
- T009: depends on previous applicable task / none
- T010: depends on previous applicable task / none
- T011: depends on previous applicable task / none
- T012: depends on previous applicable task / none
- T013: depends on previous applicable task / none
- T014: depends on previous applicable task / none
- T015: depends on previous applicable task / none

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-19

## Open Links And Blockers
- TBD until every AC/TC/TASK/DEC link is confirmed.
