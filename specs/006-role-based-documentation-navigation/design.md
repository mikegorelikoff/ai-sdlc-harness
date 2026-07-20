---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "006-role-based-documentation-navigation"
  artifact: "design.md"
  path: "specs/006-role-based-documentation-navigation/design.md"
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
  related_artifacts:
    - "specs/006-role-based-documentation-navigation/decision-log.md"
    - "specs/006-role-based-documentation-navigation/plan.md"
    - "specs/006-role-based-documentation-navigation/qa.md"
    - "specs/006-role-based-documentation-navigation/requirements.md"
    - "specs/006-role-based-documentation-navigation/tasks.md"
    - "specs/006-role-based-documentation-navigation/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "validated"
---

# Design

## Overview
Collapse the 13-tab public navigation into Home, Start, Reference, Use, Adopt, and About. Keep stable public pages at their paths. Add a generated role discovery layer that links directly to complete skill guides; do not publish the internal persona-review matrix.

## Architecture
The site keeps four information layers: entry (Home/Start), execution (Use), organizational adoption (Adopt), and exact contracts (Reference), with About for rationale and contribution. Reference is top-level and early. Role discovery is generated from an explicit many-to-many mapping validated against the installed skill inventory.

## Components
mkdocs.yml compact navigation; docs/reference/skills-by-role.md generated role finder; docs/reference/index.md and docs/reference/skills.md direct discovery links; docs/scripts/build_catalog.py role-page generator; docs/scripts/validate_docs.py navigation and role contract tests.

## Interfaces and Contracts
The role finder exposes role, task signal, role relationship, required input, next handoff, and responsibility boundary. A skill may appear in multiple roles. Skill guide URLs and the full catalog remain canonical. Validation requires all requested role headings, complete inventory coverage, grouped overlaps, and a compact Reference-prominent nav. Seniority perspectives are review evidence only.

## Data Model
ROLE_SKILL_GROUPS maps each public role to ordered task entry points and supporting skill IDs plus a concise responsibility statement. TASK_SELECTION_HINTS records choose-when, required-input, and next-handoff guidance. Shared-skill grouping records the role relationship without duplicating the canonical guide.

## Error Handling
Catalog generation fails on unknown mapped skills, an installed skill absent from all role groups, duplicate entries inside a role tier, or missing requested roles. Documentation validation reports nav-count, Reference-position, persona heading, link, and generated-drift failures.

## Security Considerations
Role guidance distinguishes skill use from approval authority. Executive, QA, product, engineering, security, release, and policy decisions remain human-owned. Overlap never grants a role authority it does not have.

## Observability
Validation reports public page, skill, and module counts; generated drift; source/link/nav checks; strict render results; and SDD gate results. The persona review matrix records role and experience coverage.

## Risks and Tradeoffs
Six broad tabs create deeper side navigation, but lower global visual load. Many-to-many mappings intentionally repeat skill links across role groups, but this is purposeful discovery rather than duplicated contract prose. Explicit mappings need maintenance, mitigated by inventory validation.

## Validation Strategy
Run catalog generator and tests, documentation source validator, strict MkDocs build, rendered target validation, SDD clarify/checklist/plan/analyze/validate gates, git diff checks, and independent persona rereads.

## Migration Notes
Stable public URLs remain except the internal-only onboarding role-path page, which is removed. The generated Skills by role reference is the sole public role-discovery surface.
