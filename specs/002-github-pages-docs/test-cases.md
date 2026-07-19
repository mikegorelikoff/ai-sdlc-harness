---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "002-github-pages-docs"
  artifact: "test-cases.md"
  path: "specs/002-github-pages-docs/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/002-github-pages-docs/_ai_sdlc/state.toon"
  decision_log: "specs/002-github-pages-docs/decision-log.md"
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
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
  related_artifacts:
    - "specs/002-github-pages-docs/decision-log.md"
    - "specs/002-github-pages-docs/design.md"
    - "specs/002-github-pages-docs/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "approved"
---

# Test Cases

## Scope
Validate the generated catalogs, site structure, internal navigation, accessibility-critical shell behavior, base-path-safe links, and GitHub Pages workflow contract.

## Scenario Matrix
| ID | Scenario | Expected Result | Refs |
| --- | --- | --- | --- |
| TC-001 | Load landing page content | Promise, workflow, start, and repository actions are present | AC-001 |
| TC-002 | Validate responsive shell contracts | Mobile toggle, semantic navigation, viewport metadata, and desktop sidebar hooks exist | AC-002, AC-008 |
| TC-003 | Generate skill catalog | Every skill package appears exactly once with valid repository path | AC-003 |
| TC-004 | Generate module catalog | Every manifest appears and references existing skills | AC-004 |
| TC-005 | Validate clean documentation tree | Frontmatter, local links, anchors, and required assets pass | AC-005 |
| TC-006 | Introduce broken local target in fixture | Validator exits non-zero with source and missing target | AC-005 |
| TC-007 | Inspect project-base URL usage | Internal template links use Jekyll URL filters and no root-only asset paths exist | AC-006 |
| TC-008 | Inspect Pages workflow | Official action versions, permissions, environment, build dependency, and main trigger exist | AC-007 |
| TC-009 | Disable JavaScript/reduced motion | Core links remain in markup and reduced-motion CSS disables nonessential transitions | AC-008 |

## Layer Mapping
- Unit: catalog parser, frontmatter parsing, local path and anchor resolution.
- Contract: Jekyll page metadata, generated data schema, workflow action and permission checks.
- Integration: full docs source validation and generated-catalog parity.
- Manual/browser: responsive navigation, visual hierarchy, keyboard focus, no-JavaScript fallback.

## Automation Plan
- Add `docs/scripts/build_catalog.py` with `--check`.
- Add `docs/scripts/validate_docs.py` with repository-root discovery.
- Add standard-library tests under `docs/tests/`.
- Run those checks in the Pages build job before Jekyll.
- Use browser smoke checks locally for representative widths.

## Open Gaps
- The final hosted URL cannot be verified until GitHub Pages is enabled with GitHub Actions as its source.
- Visual regression snapshots are deferred; responsive smoke testing covers the initial release.
