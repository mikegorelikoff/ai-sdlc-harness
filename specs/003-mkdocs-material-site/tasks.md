---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-mkdocs-material-site"
  artifact: "tasks.md"
  path: "specs/003-mkdocs-material-site/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/003-mkdocs-material-site/_ai_sdlc/state.toon"
  decision_log: "specs/003-mkdocs-material-site/decision-log.md"
  status: "approved"
  owner: "Dev"
  created_at: "2026-07-19"
  updated_at: "2026-07-19"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "DEC-001"
  related_artifacts:
    - "specs/003-mkdocs-material-site/decision-log.md"
    - "specs/003-mkdocs-material-site/design.md"
    - "specs/003-mkdocs-material-site/plan.md"
    - "specs/003-mkdocs-material-site/qa.md"
    - "specs/003-mkdocs-material-site/requirements.md"
    - "specs/003-mkdocs-material-site/test-cases.md"
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
- [x] T001. Migrate the complete documentation site and delivery pipeline to MkDocs Material.
  Output: SDD package, MkDocs Material configuration, pinned dependency, Material-native home and catalogs, migrated links, minimal brand CSS, strict Pages workflow, validators, tests, rendered QA evidence, and one focused commit.
  Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, DEC-001

## Testing
T001 includes catalog drift, source validation, unit tests, strict MkDocs build, a 44-page rendered audit covering 2,725 local targets, and HTTP smoke. Interactive browser smoke was unavailable because the required browser runtime was not exposed; responsive confidence comes from maintained Material components, strict output inspection, viewport metadata, palette/navigation/search contracts, and limited custom CSS.

## Documentation
The task updates the public documentation implementation and records migration decisions, exact validation evidence, and the browser-runtime residual risk in specs/003-mkdocs-material-site/.
