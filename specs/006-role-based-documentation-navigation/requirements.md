---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "006-role-based-documentation-navigation"
  artifact: "requirements.md"
  path: "specs/006-role-based-documentation-navigation/requirements.md"
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
    - "DEC-001"
    - "DEC-002"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
  related_artifacts:
    - "specs/006-role-based-documentation-navigation/decision-log.md"
    - "specs/006-role-based-documentation-navigation/design.md"
    - "specs/006-role-based-documentation-navigation/plan.md"
    - "specs/006-role-based-documentation-navigation/qa.md"
    - "specs/006-role-based-documentation-navigation/tasks.md"
    - "specs/006-role-based-documentation-navigation/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "validated"
---

# Requirements

## Goal
Make the documentation easier to navigate and the skill catalog easier to use by role, while preserving complete reference coverage and stable URLs.

## Problem Statement
The current MkDocs navigation exposes 13 top-level tabs, Reference appears near the end, and the 44-skill catalog requires scanning one undifferentiated list. This creates visual load, duplicated route descriptions, and unnecessary cross-page travel.

## Scope
Reorganize top-level navigation; promote Reference; consolidate entry surfaces without deleting stable pages; generate one skill-by-role discovery page for QA, BA, PM, PO, Dev, VP, and Head of AI Practice; use junior, middle, senior, and lead personas only to review documentation usability; validate role discovery and reference access.

## Actors
Primary readers: QA, BA, PM, PO, Dev, VP, and Head of AI Practice. Junior, middle, senior, and lead perspectives are internal review lenses for applicable delivery roles, not published navigation categories. Supporting actors: documentation maintainers and AI agents selecting skills.

## Inputs
Viachaslau Matsveyeu feedback on tab overload, duplication, cross-links, Reference depth, and role separation; current MkDocs navigation; generated 44-skill inventory; independent persona reviews.

## Outputs
A compact top navigation, prominent Reference entry, generated Skills by role page, reduced duplicate overview prose, validation rules, updated catalogs, and persona-review evidence.

## Functional Requirements
FR-001: Reduce top-level navigation from 13 tabs to no more than 6 coherent groups. FR-002: Place Reference among the first three top-level entries. FR-003: Preserve stable public page URLs except the internal-only onboarding role review page. FR-004: Provide one generated role-first skill finder covering QA, BA, PM, PO, Dev, VP, and Head of AI Practice. FR-005: Show shared skills under every relevant role and explain overlap. FR-006: Use junior, middle, senior, and lead personas to review role discovery without publishing seniority-specific paths. FR-007: Link Reference and the skill catalog directly without multi-hop discovery. FR-008: Update deterministic documentation validation.

## Non-Functional Requirements
NFR-001: Generated role mappings must fail on unknown or missing skill IDs. NFR-002: Strict MkDocs and internal-link validation must pass. NFR-003: Navigation labels must be understandable without internal architecture knowledge. NFR-004: Existing deep links remain valid. NFR-005: Content must keep human authority boundaries explicit.

## Constraints
Keep MkDocs Material, the generated detailed skill guides, repository skill contracts, and current public Markdown paths. Do not change runtime skill semantics. Use English for public documentation.

## Acceptance Criteria
AC-001: Navigation must expose at most six top-level entries and must place Reference first, second, or third.
AC-002: Navigation validation must report every public page exactly once and no missing target.
AC-003: The generated role finder must include QA, BA, PM, PO, Dev, VP, and Head of AI Practice.
AC-004: QA, BA, PM, PO, and Dev reviews must cover junior, middle, senior, and lead perspectives, while published documentation must remain role-based rather than seniority-based.
AC-005: VP and Head of AI Practice must each have responsibility-appropriate discovery guidance.
AC-006: Generation must fail for an unknown mapped skill or an installed skill absent from every role.
AC-007: Shared skills must appear under multiple relevant roles and the page must explain the overlap model.
AC-008: Home, Start, Reference, and the catalog must link directly to role and exact-reference routes without duplicating the canonical first-use sequence.
AC-009: Final persona reviews must report no unresolved P0 or P1 navigation or discovery issue.
AC-010: Catalog drift, documentation, strict build, rendered output, SDD, and diff checks must pass.

## Out of Scope
Deleting or renaming public pages; changing skill behavior; redesigning branding; translating the site; changing installer behavior; claiming measured usability improvement from simulated personas.

## Assumptions
The feedback refers primarily to MkDocs top navigation tabs. Role membership is many-to-many. Seniority is used only as an internal validation lens and is not a requested documentation dimension. Quick-flow is appropriate because the change is documentation-only and reversible.

## Open Questions
No blocking questions. Real-user usability measurement remains a future follow-up; this change uses explicit stakeholder feedback plus simulated persona review.

## Decision Status
All blocking decisions are resolved. Accepted assumptions: the feedback concerns persistent top navigation and role-based skill discovery; role membership is many-to-many; seniority is internal review coverage only. DEC-002 supersedes the public role-path portion of DEC-001 and authorizes the generated Skills by role reference as the only public role surface.
