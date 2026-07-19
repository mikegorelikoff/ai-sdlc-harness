---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-guided-onboarding-documentation"
  artifact: "plan.md"
  path: "/Users/mikegorelikov/Documents/GitHub/ai-sdlc-harness/specs/005-guided-onboarding-documentation/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "/Users/mikegorelikov/Documents/GitHub/ai-sdlc-harness/specs/005-guided-onboarding-documentation/_ai_sdlc/state.toon"
  decision_log: "/Users/mikegorelikov/Documents/GitHub/ai-sdlc-harness/specs/005-guided-onboarding-documentation/decision-log.md"
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
- AC-001: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T001, T002) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T001, T002, T005) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T002) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T003) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T003) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T003) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T004) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T004) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T002, T003, T005) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T005) -> qa.md -> decision-log.md
- AC-011: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T005) -> qa.md -> decision-log.md
- AC-012: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T003, T005) -> qa.md -> decision-log.md
- AC-013: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T002, T005) -> qa.md -> decision-log.md
- AC-014: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T001, T004, T005, T006) -> qa.md -> decision-log.md
- AC-015: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T004, T006) -> qa.md -> decision-log.md
- AC-016: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T001, T006) -> qa.md -> decision-log.md
- AC-017: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T002, T005) -> qa.md -> decision-log.md
- AC-018: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018) -> tasks.md (T001, T002, T003, T004, T005, T006) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: - [x] T001. Define the guided onboarding documentation program and persona acceptance gates.; refs: AC-001, AC-002, AC-014, AC-016, AC-018; output: Complete SDD package, accepted information architecture, persona findings, generated plan/indexes, focused validation, and one planning commit.
- [ ] T002: - [x] T002. Build the beginner-first foundations and first-use path.; refs: AC-001, AC-002, AC-003, AC-009, AC-013, AC-017, AC-018; output: Canonical product story and naming, AI SDLC/SDD foundations, fit/non-fit, mental model, responsibilities, glossary, canonical install/verification, first 30 minutes, action labels, Home/README/Start integration, navigation, tests, and one focused commit.
- [ ] T003: - [ ] T003. Publish runnable tutorials and the complete lifecycle flow library.; refs: AC-004, AC-005, AC-006, AC-009, AC-012, AC-018; output: Copyable small-change and full-feature walkthroughs, explicit prompts/terminal actions/expected artifacts/checkpoints/recovery, all 18 refinement stages, implementation/control-plane journeys, entry/exit/reopen matrices, decision tree, navigation, tests, and one focused commit.
- [ ] T004: - [ ] T004. Generate complete human-facing skill and script documentation.; refs: AC-007, AC-008, AC-014, AC-015, AC-018; output: Enhanced deterministic catalog generator, 43/43 per-skill guides, complete in-scope script inventory, coverage manifest, required detail fields, navigation/discovery surfaces, parser/render/coverage tests, and one focused commit.
- [ ] T005: - [ ] T005. Publish adoption, governance, operations, and maintainer guidance.; refs: AC-002, AC-009, AC-010, AC-011, AC-012, AC-013, AC-014, AC-017, AC-018; output: Persona/role paths, pilot playbook, metrics interpretation, operating model, human/agent RACI, trust/governance, maturity/limitations, troubleshooting runbook, contributor/extension path, canonical-source reconciliation, full navigation/index consistency, tests, and one focused commit.
- [ ] T006: - [ ] T006. Close independent persona review and release-quality validation.; refs: AC-014, AC-015, AC-016, AC-018; output: Junior, lead, and VP reread findings, revisions until all return PASS with no P0/P1, complete regression/build/render/compatibility/SDD evidence, exact task-to-commit audit, clean tree, and one focused completion commit.

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on previous applicable task / none
- T003: depends on previous applicable task / none
- T004: depends on previous applicable task / none
- T005: depends on previous applicable task / none
- T006: depends on previous applicable task / none

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-19

## Open Links And Blockers
- TBD until every AC/TC/TASK/DEC link is confirmed.
