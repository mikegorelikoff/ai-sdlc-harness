---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "010-learn-knowledge-base"
  artifact: "plan.md"
  path: "specs/010-learn-knowledge-base/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/010-learn-knowledge-base/_ai_sdlc/state.toon"
  decision_log: "specs/010-learn-knowledge-base/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
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
- AC-001: requirements.md -> test-cases.md (TC-016, TC-017, TC-018, TC-020, TC-022) -> tasks.md (T001, T005, T013) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-016, TC-018, TC-019, TC-020, TC-021, TC-022, TC-023) -> tasks.md (T002, T003, T004, T011, T013) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-019, TC-022, TC-028) -> tasks.md (T003, T004, T011, T013) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-022) -> tasks.md (T001, T004, T005, T011, T012, T013) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-011, TC-012, TC-013, TC-014, TC-015, TC-024, TC-025, TC-026, TC-027) -> tasks.md (T001, T002, T008, T012, T013) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021, TC-023, TC-024, TC-025, TC-026, TC-027, TC-028) -> tasks.md (T002, T008, T013) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-020, TC-022) -> tasks.md (T005, T013) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-029) -> tasks.md (T006, T007, T010, T013) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-030) -> tasks.md (T009, T010, T013) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-031) -> tasks.md (T005, T010, T013) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Finalize architecture, ownership map, and source research register.; refs: AC-001, AC-004, AC-005; output: mkdocs.yml; docs/_data/content_sources.yml; docs/about/maintainers/source-reuse-and-adaptation.md
- [x] T002: Implement token, structure, and source validators with pinned dependencies.; refs: AC-002, AC-005, AC-006; output: docs/scripts/learning_tokens.py; docs/scripts/learning_structure.py; requirements-docs.lock
- [x] T003: Draft the hub and Levels 0 through 2B in order.; refs: AC-002, AC-003; output: docs/start.md; docs/learn/ai-foundations.md; docs/learn/prompt-engineering.md; docs/learn/context-and-verification.md; docs/learn/agents-tools-and-subagents.md; docs/learn/multi-role-review.md
- [x] T004: Draft Levels 3 through 6 and guided labs and role paths.; refs: AC-002, AC-003, AC-004; output: docs/learn/ai-sdlc-and-sdd.md; docs/learn/harness-essentials.md; docs/learn/guided-practice.md; docs/learn/role-learning-paths.md; docs/assets/learning-fixtures
- [x] T005: Integrate navigation, home, README, reciprocal links, and governance.; refs: AC-001, AC-004, AC-007, AC-010; output: mkdocs.yml; docs/index.md; README.md; docs/foundations; docs/about/maintainers
- [x] T006: Run nine same-diff reviews and apply accepted corrections.; refs: AC-008; output: docs/about/maintainers/learn-review-2026-07-21.md; corrected Learn snapshot
- [ ] T007: Rerun the four required reviewers.; refs: AC-008; output: post-correction review section in docs/about/maintainers/learn-review-2026-07-21.md
- [x] T008: Add boundary, normalization, structure, source, navigation, link, role, heading, provenance, and fixture tests.; refs: AC-005, AC-006; output: docs/tests/test_learning_tokens.py; docs/tests/test_learning_structure.py; docs/tests/test_content_sources.py
- [ ] T009: Run focused and full regression validation.; refs: AC-009; output: final validation receipts in docs/about/maintainers/learn-review-2026-07-21.md
- [ ] T010: Inspect final diff and record counts, reviews, blockers, and command outcomes.; refs: AC-008, AC-009, AC-010; output: final report and SDD validation evidence
- [x] T011: Create all ten Learn pages with the learner contract and original content.; refs: AC-002, AC-003, AC-004; output: docs/start.md; docs/learn/*.md
- [x] T012: Create source-reuse and curriculum-governance guidance.; refs: AC-004, AC-005; output: docs/about/maintainers/source-reuse-and-adaptation.md; docs/about/maintainers/curriculum-governance.md
- [ ] T013: Report navigation, files, tokens, sources, validations, reviews, corrections, and unresolved items.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010; output: final user-facing implementation report

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on T001
- T003: depends on T001
- T004: depends on T003
- T005: depends on T003, T004
- T006: depends on T005, T008
- T007: depends on T006
- T008: depends on T002
- T009: depends on T007, T008
- T010: depends on T009
- T011: depends on T003, T004
- T012: depends on T001
- T013: depends on T009, T010

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-21

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
