---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "006-role-based-documentation-navigation"
  artifact: "plan.md"
  path: "specs/006-role-based-documentation-navigation/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/006-role-based-documentation-navigation/_ai_sdlc/state.toon"
  decision_log: "specs/006-role-based-documentation-navigation/decision-log.md"
  status: "validated"
  owner: "docs-maintainers"
  created_at: "2026-07-20"
  updated_at: "2026-07-20"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "plan"
    - "validated"
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
- AC-001: requirements.md -> test-cases.md (TC-001) -> tasks.md (T001, T005) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-002) -> tasks.md (T001, T006) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-003) -> tasks.md (T002, T003, T005) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-004) -> tasks.md (T003, T005) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-005) -> tasks.md (T003, T005) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-006) -> tasks.md (T002, T005) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-007) -> tasks.md (T002, T005) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-008) -> tasks.md (T001, T003, T004) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-009) -> tasks.md (T007) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-010) -> tasks.md (T006) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: - [x] T001. Consolidate MkDocs top-level navigation and promote Reference.; refs: AC-001, AC-002, AC-008; output: Six top-level groups with Reference third and all stable public pages retained.
- [x] T002: - [x] T002. Build generated many-to-many Skills by role discovery.; refs: AC-003, AC-006, AC-007; output: Role page, validated mapping, direct skill links, task tables, and overlap explanation.
- [x] T003: - [x] T003. Validate role discovery from the requested internal persona perspectives.; refs: AC-003, AC-004, AC-005, AC-008; output: QA, BA, PM, PO, Dev, VP, and Head of AI Practice review evidence without publishing a role or seniority review page.
- [x] T004: - [x] T004. Reduce duplicated routing copy and strengthen direct Reference entry points.; refs: AC-008; output: Reconciled Home, Start, onboarding, Reference, catalog, and generated skill-guide surfaces.
- [x] T005: - [x] T005. Add navigation and role-discovery validation.; refs: AC-001, AC-003, AC-004, AC-005, AC-006, AC-007; output: Deterministic tests for compact nav, Reference prominence, role coverage, mapping integrity, overlap, and inventory closure.
- [x] T006: - [x] T006. Run source, render, SDD, and diff validation.; refs: AC-002, AC-010; output: Passing unit tests, documentation validator, strict MkDocs build, rendered-site validation, and diff checks.
- [x] T007: - [x] T007. Close all requested persona reviews.; refs: AC-009; output: QA/BA, PM/PO, and Dev/VP/Head of AI Practice re-reviews all returned PASS with no unresolved P0/P1 finding.

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on T001
- T003: depends on T002
- T004: depends on T003
- T005: depends on T004
- T006: depends on T005
- T007: depends on T006

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-20

## Open Links And Blockers
- TBD until every AC/TC/TASK/DEC link is confirmed.
