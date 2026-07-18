---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-adaptive-harness-roadmap"
  artifact: "plan.md"
  path: "/Users/mikegorelikov/Documents/GitHub/ai-sdlc-harness/specs/001-adaptive-harness-roadmap/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "/Users/mikegorelikov/Documents/GitHub/ai-sdlc-harness/specs/001-adaptive-harness-roadmap/_ai_sdlc/state.toon"
  decision_log: "/Users/mikegorelikov/Documents/GitHub/ai-sdlc-harness/specs/001-adaptive-harness-roadmap/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-07-18"
  updated_at: "2026-07-18"
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
- AC-001: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T002) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T003) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T004) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T004) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T005) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T006) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T007) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T008) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T009) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T010) -> qa.md -> decision-log.md
- AC-011: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T011, T012, T013) -> qa.md -> decision-log.md
- AC-012: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T014) -> qa.md -> decision-log.md
- AC-013: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T015) -> qa.md -> decision-log.md
- AC-014: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014) -> tasks.md (T001, T015) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: - [x] T001. Establish the roadmap SDD package and traceable execution plan.; refs: AC-014, DEC-001, DEC-002, DEC-003; output: Complete SDD artifacts, decision log, plan.toon, plan.md, registry entry, and passing gates.
- [x] T002: - [x] T002. Implement the context-aware AI SDLC navigator.; refs: AC-001; output: Navigator skill, deterministic router CLI, Markdown and TOON outputs, tests, and docs.
- [ ] T003: - [ ] T003. Implement the common post-workflow handoff contract.; refs: AC-002; output: Shared handoff schema, emitter, adoption guidance, compatibility tests, and docs.
- [ ] T004: - [ ] T004. Implement explainable risk-adaptive rigor profiles.; refs: AC-003, AC-004; output: Policy engine, patch/standard/assured/regulated profiles, safe overrides, tests, and docs.
- [ ] T005: - [ ] T005. Implement evidence-backed project context and drift detection.; refs: AC-005; output: Project-context skill, Markdown and TOON generator, evidence anchors, drift checks, tests, and docs.
- [ ] T006: - [ ] T006. Implement the reusable quality-lens registry and reports.; refs: AC-006; output: Quality-lens skill, registry, traceable finding schema, report generator, tests, and docs.
- [ ] T007: - [ ] T007. Implement change-impact analysis and safe lifecycle reopening.; refs: AC-007; output: Change-impact skill, affected-artifact analysis, reopen plan, evidence gates, tests, and docs.
- [ ] T008: - [ ] T008. Implement retrospective learning with reviewable proposals.; refs: AC-008; output: Retrospective skill, observation and proposal schemas, policy safety checks, tests, and docs.
- [ ] T009: - [ ] T009. Implement layered team and user customization.; refs: AC-009; output: Versioned config schema, deterministic resolver, provenance, protected-gate checks, tests, and docs.
- [ ] T010: - [ ] T010. Implement optional module manifests and discovery.; refs: AC-010; output: Versioned module schema, registry and discovery CLI, compatibility checks, tests, and docs.
- [ ] T011: - [ ] T011. Add the optional Architecture capability.; refs: AC-011; output: Architecture skill, routed design artifact workflow, tests, and module registration.
- [ ] T012: - [ ] T012. Add the optional UX capability.; refs: AC-011; output: UX skill, routed experience artifact workflow, tests, and module registration.
- [ ] T013: - [ ] T013. Add the optional Research capability.; refs: AC-011; output: Research skill, evidence and source artifact workflow, tests, and module registration.
- [ ] T014: - [ ] T014. Implement the evidence council and portable review orchestration.; refs: AC-012; output: Council skill, simulated and independent plans, authority-safe report, tests, and docs.
- [ ] T015: - [ ] T015. Add install, update, and compatibility contracts and run final integration validation.; refs: AC-013, AC-014; output: Compatibility baseline, validator, install and update docs, full regression evidence, and closed roadmap.

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on T001
- T003: depends on T002
- T004: depends on T002, T003
- T005: depends on T002, T004
- T006: depends on T003, T004
- T007: depends on T003, T005, T006
- T008: depends on T007
- T009: depends on T004, T005
- T010: depends on T002, T009
- T011: depends on T010
- T012: depends on T010
- T013: depends on T010
- T014: depends on T006, T010, T011, T012, T013
- T015: depends on T001, T002, T003, T004, T005, T006, T007, T008, T009, T010, T011, T012, T013, T014

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-18

## Open Links And Blockers
- TBD until every AC/TC/TASK/DEC link is confirmed.
