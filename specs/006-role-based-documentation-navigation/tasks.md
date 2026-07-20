---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "006-role-based-documentation-navigation"
  artifact: "tasks.md"
  path: "specs/006-role-based-documentation-navigation/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/006-role-based-documentation-navigation/_ai_sdlc/state.toon"
  decision_log: "specs/006-role-based-documentation-navigation/decision-log.md"
  status: "validated"
  owner: "docs-maintainers"
  created_at: "2026-07-20"
  updated_at: "2026-07-20"
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
    - "specs/006-role-based-documentation-navigation/decision-log.md"
    - "specs/006-role-based-documentation-navigation/design.md"
    - "specs/006-role-based-documentation-navigation/plan.md"
    - "specs/006-role-based-documentation-navigation/qa.md"
    - "specs/006-role-based-documentation-navigation/requirements.md"
    - "specs/006-role-based-documentation-navigation/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "validated"
---

# Tasks

## Implementation
- [x] T001. Consolidate MkDocs top-level navigation and promote Reference.
  Output: Six top-level groups with Reference third and all stable public pages retained.
  Refs: AC-001, AC-002, AC-008
- [x] T002. Build generated many-to-many Skills by role discovery.
  Output: Role page, validated mapping, direct skill links, task tables, and overlap explanation.
  Refs: AC-003, AC-006, AC-007
  Depends on: T001
- [x] T003. Validate role discovery from the requested internal persona perspectives.
  Output: QA, BA, PM, PO, Dev, VP, and Head of AI Practice review evidence without publishing a role or seniority review page.
  Refs: AC-003, AC-004, AC-005, AC-008
  Depends on: T002
- [x] T004. Reduce duplicated routing copy and strengthen direct Reference entry points.
  Output: Reconciled Home, Start, onboarding, Reference, catalog, and generated skill-guide surfaces.
  Refs: AC-008
  Depends on: T003

## Testing
- [x] T005. Add navigation and role-discovery validation.
  Output: Deterministic tests for compact nav, Reference prominence, role coverage, mapping integrity, overlap, and inventory closure.
  Refs: AC-001, AC-003, AC-004, AC-005, AC-006, AC-007
  Depends on: T004
- [x] T006. Run source, render, SDD, and diff validation.
  Output: Passing unit tests, documentation validator, strict MkDocs build, rendered-site validation, and diff checks.
  Refs: AC-002, AC-010
  Depends on: T005

## Documentation
- [x] T007. Close all requested persona reviews.
  Output: QA/BA, PM/PO, and Dev/VP/Head of AI Practice re-reviews all returned PASS with no unresolved P0/P1 finding.
  Refs: AC-009
  Depends on: T006
