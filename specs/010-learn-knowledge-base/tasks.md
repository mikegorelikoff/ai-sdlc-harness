---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "010-learn-knowledge-base"
  artifact: "tasks.md"
  path: "specs/010-learn-knowledge-base/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/010-learn-knowledge-base/_ai_sdlc/state.toon"
  decision_log: "specs/010-learn-knowledge-base/decision-log.md"
  status: "review"
  owner: "Repository-maintainers"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
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
  related_artifacts:
    - "specs/010-learn-knowledge-base/decision-log.md"
    - "specs/010-learn-knowledge-base/design.md"
    - "specs/010-learn-knowledge-base/qa.md"
    - "specs/010-learn-knowledge-base/requirements.md"
    - "specs/010-learn-knowledge-base/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "review"
    - "learn-curriculum"
---

# Tasks

## Implementation
- [x] T001. Finalize architecture, ownership map, and source research register.
  Refs: AC-001, AC-004, AC-005
  Output: mkdocs.yml; docs/_data/content_sources.yml; docs/about/maintainers/source-reuse-and-adaptation.md
- [x] T002. Implement token, structure, and source validators with pinned dependencies.
  Refs: AC-002, AC-005, AC-006
  Depends on: T001
  Output: docs/scripts/learning_tokens.py; docs/scripts/learning_structure.py; requirements-docs.lock
- [x] T003. Draft the hub and Levels 0 through 2B in order.
  Refs: AC-002, AC-003
  Depends on: T001
  Output: docs/start.md; docs/learn/ai-foundations.md; docs/learn/prompt-engineering.md; docs/learn/context-and-verification.md; docs/learn/agents-tools-and-subagents.md; docs/learn/multi-role-review.md
- [x] T004. Draft Levels 3 through 6 and guided labs and role paths.
  Refs: AC-002, AC-003, AC-004
  Depends on: T003
  Output: docs/learn/ai-sdlc-and-sdd.md; docs/learn/harness-essentials.md; docs/learn/guided-practice.md; docs/learn/role-learning-paths.md; docs/assets/learning-fixtures
- [x] T005. Integrate navigation, home, README, reciprocal links, and governance.
  Refs: AC-001, AC-004, AC-007, AC-010
  Depends on: T003, T004
  Output: mkdocs.yml; docs/index.md; README.md; docs/foundations; docs/about/maintainers
- [x] T006. Run nine same-diff reviews and apply accepted corrections.
  Refs: AC-008
  Depends on: T005, T008
  Output: docs/about/maintainers/learn-review-2026-07-21.md; corrected Learn snapshot
- [ ] T007. Rerun the four required reviewers.
  Refs: AC-008
  Depends on: T006
  Output: post-correction review section in docs/about/maintainers/learn-review-2026-07-21.md

## Testing
- [x] T008. Add boundary, normalization, structure, source, navigation, link, role, heading, provenance, and fixture tests.
  Refs: AC-005, AC-006
  Depends on: T002
  Output: docs/tests/test_learning_tokens.py; docs/tests/test_learning_structure.py; docs/tests/test_content_sources.py
- [ ] T009. Run focused and full regression validation.
  Refs: AC-009
  Depends on: T007, T008
  Output: final validation receipts in docs/about/maintainers/learn-review-2026-07-21.md
- [ ] T010. Inspect final diff and record counts, reviews, blockers, and command outcomes.
  Refs: AC-008, AC-009, AC-010
  Depends on: T009
  Output: final report and SDD validation evidence

## Documentation
- [x] T011. Create all ten Learn pages with the learner contract and original content.
  Refs: AC-002, AC-003, AC-004
  Depends on: T003, T004
  Output: docs/start.md; docs/learn/*.md
- [x] T012. Create source-reuse and curriculum-governance guidance.
  Refs: AC-004, AC-005
  Depends on: T001
  Output: docs/about/maintainers/source-reuse-and-adaptation.md; docs/about/maintainers/curriculum-governance.md
- [ ] T013. Report navigation, files, tokens, sources, validations, reviews, corrections, and unresolved items.
  Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010
  Depends on: T009, T010
  Output: final user-facing implementation report
