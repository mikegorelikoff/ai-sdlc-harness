---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "006-role-based-documentation-navigation"
  artifact: "test-cases.md"
  path: "specs/006-role-based-documentation-navigation/test-cases.md"
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
  related_artifacts:
    - "specs/006-role-based-documentation-navigation/decision-log.md"
    - "specs/006-role-based-documentation-navigation/design.md"
    - "specs/006-role-based-documentation-navigation/plan.md"
    - "specs/006-role-based-documentation-navigation/qa.md"
    - "specs/006-role-based-documentation-navigation/requirements.md"
    - "specs/006-role-based-documentation-navigation/tasks.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "validated"
---

# Test Cases

## Scope
Verify compact navigation, Reference prominence, stable public coverage, generated role mappings, overlap behavior, direct routes, absence of a public seniority matrix, rendering, and SDD traceability.

## Scenario Matrix
- TC-001 / AC-001: Parse top-level nav and require at most six entries with Reference in positions one through three.
- TC-002 / AC-002: Validate every public page appears exactly once and every nav target exists.
- TC-003 / AC-003: Require QA, BA, PM, PO, Dev, VP, and Head of AI Practice role sections.
- TC-004 / AC-004: Review QA, BA, PM, PO, and Dev discovery from junior, middle, senior, and lead perspectives while verifying the published pages contain no seniority matrix.
- TC-005 / AC-005: Require VP and Head of AI Practice responsibility routes and authority boundaries.
- TC-006 / AC-006: Generate successfully for complete mappings and fail for unknown or unmapped installed skills.
- TC-007 / AC-007: Verify shared skills appear in several roles with grouped relationship labels and one canonical guide.
- TC-008 / AC-008: Verify direct role/reference links and one canonical first-use sequence.
- TC-009 / AC-009: Reconcile all persona re-reviews with no P0/P1 finding.
- TC-010 / AC-010: Run catalog drift, unit, source, strict build, rendered, SDD, and diff gates.

## Layer Mapping
Unit: role mapping integrity and renderer output. Source integration: nav, links, page metadata, role contracts. Render integration: strict MkDocs and rendered targets. Manual UX: desktop/mobile nav hierarchy and persona task finding. SDD: artifact and trace validation.

## Automation Plan
Extend docs/scripts/build_catalog.py tests through generated drift checks and docs/scripts/validate_docs.py with compact-navigation and role-discovery assertions. Reuse existing MkDocs and rendered validators.

## Open Gaps
No formal external usability test is available. Simulated persona findings validate completeness and obvious friction, not measured task time.
