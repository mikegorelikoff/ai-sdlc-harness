---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-adaptive-harness-roadmap"
  artifact: "tasks.md"
  path: "specs/001-adaptive-harness-roadmap/tasks.md"
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
  related_artifacts:
    - "specs/001-adaptive-harness-roadmap/decision-log.md"
    - "specs/001-adaptive-harness-roadmap/design.md"
    - "specs/001-adaptive-harness-roadmap/qa.md"
    - "specs/001-adaptive-harness-roadmap/requirements.md"
    - "specs/001-adaptive-harness-roadmap/test-cases.md"
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
- [x] T001. Establish the roadmap SDD package and traceable execution plan.
  Output: Complete SDD artifacts, decision log, plan.toon, plan.md, registry entry, and passing gates.
  Refs: AC-014, DEC-001, DEC-002, DEC-003
- [ ] T002. Implement the context-aware AI SDLC navigator.
  Output: Navigator skill, deterministic router CLI, Markdown and TOON outputs, tests, and docs.
  Refs: AC-001
  Depends on: T001
- [ ] T003. Implement the common post-workflow handoff contract.
  Output: Shared handoff schema, emitter, adoption guidance, compatibility tests, and docs.
  Refs: AC-002
  Depends on: T002
- [ ] T004. Implement explainable risk-adaptive rigor profiles.
  Output: Policy engine, patch/standard/assured/regulated profiles, safe overrides, tests, and docs.
  Refs: AC-003, AC-004
  Depends on: T002, T003
- [ ] T005. Implement evidence-backed project context and drift detection.
  Output: Project-context skill, Markdown and TOON generator, evidence anchors, drift checks, tests, and docs.
  Refs: AC-005
  Depends on: T002, T004
- [ ] T006. Implement the reusable quality-lens registry and reports.
  Output: Quality-lens skill, registry, traceable finding schema, report generator, tests, and docs.
  Refs: AC-006
  Depends on: T003, T004
- [ ] T007. Implement change-impact analysis and safe lifecycle reopening.
  Output: Change-impact skill, affected-artifact analysis, reopen plan, evidence gates, tests, and docs.
  Refs: AC-007
  Depends on: T003, T005, T006
- [ ] T008. Implement retrospective learning with reviewable proposals.
  Output: Retrospective skill, observation and proposal schemas, policy safety checks, tests, and docs.
  Refs: AC-008
  Depends on: T007
- [ ] T009. Implement layered team and user customization.
  Output: Versioned config schema, deterministic resolver, provenance, protected-gate checks, tests, and docs.
  Refs: AC-009
  Depends on: T004, T005
- [ ] T010. Implement optional module manifests and discovery.
  Output: Versioned module schema, registry and discovery CLI, compatibility checks, tests, and docs.
  Refs: AC-010
  Depends on: T002, T009
- [ ] T011. Add the optional Architecture capability.
  Output: Architecture skill, routed design artifact workflow, tests, and module registration.
  Refs: AC-011
  Depends on: T010
- [ ] T012. Add the optional UX capability.
  Output: UX skill, routed experience artifact workflow, tests, and module registration.
  Refs: AC-011
  Depends on: T010
- [ ] T013. Add the optional Research capability.
  Output: Research skill, evidence and source artifact workflow, tests, and module registration.
  Refs: AC-011
  Depends on: T010
- [ ] T014. Implement the evidence council and portable review orchestration.
  Output: Council skill, simulated and independent plans, authority-safe report, tests, and docs.
  Refs: AC-012
  Depends on: T006, T010, T011, T012, T013
- [ ] T015. Add install, update, and compatibility contracts and run final integration validation.
  Output: Compatibility baseline, validator, install and update docs, full regression evidence, and closed roadmap.
  Refs: AC-013, AC-014
  Depends on: T001, T002, T003, T004, T005, T006, T007, T008, T009, T010, T011, T012, T013, T014

## Testing
Testing is embedded in T002 through T015. Each task commit must add or update focused tests, run the validation planner, execute selected checks, and record exact outcomes before its checkbox is closed.

## Documentation
Documentation is embedded in T002 through T015. Each public capability task must update its skill package and the smallest relevant README, guide, or concept page before its task commit.
