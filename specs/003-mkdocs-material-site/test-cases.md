---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-mkdocs-material-site"
  artifact: "test-cases.md"
  path: "specs/003-mkdocs-material-site/test-cases.md"
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
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
  related_artifacts:
    - "specs/003-mkdocs-material-site/decision-log.md"
    - "specs/003-mkdocs-material-site/design.md"
    - "specs/003-mkdocs-material-site/requirements.md"
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
Validate configuration, dependency pinning, navigation completeness, stable path mapping, generated catalogs, absence of Jekyll syntax, strict output, internal links, search assets, palettes, and Pages workflow behavior.

## Scenario Matrix
- TC-001 / AC-001: install requirements-docs.txt and run mkdocs build --strict; expect success.
- TC-002 / AC-002: compare nav source paths with all public Markdown pages; expect one-to-one coverage.
- TC-003 / AC-003: inspect built output for navigation, table-of-contents, search index, and back-to-top components.
- TC-004 / AC-004: inspect configuration and rendered controls for default/slate palette toggles.
- TC-005 / AC-005: render the home page at mobile and desktop widths; expect clear hero, actions, cards, lifecycle, and install example.
- TC-006 / AC-006: run catalog check; expect 35 skills and 5 modules with no template markers.
- TC-007 / AC-007: inject representative broken nav, link, and legacy token fixtures; expect actionable failures.
- TC-008 / AC-008: inspect workflow for pinned install, strict build, artifact upload, least-required deploy permissions, and main trigger.

## Layer Mapping
TC-002, TC-006, TC-007, and TC-008 are Python source/unit checks. TC-001 is the canonical build check. TC-003 and TC-004 are rendered-output checks. TC-005 is browser-level responsive QA.

## Automation Plan
Extend docs/tests/test_docs.py for MkDocs navigation and link semantics. Run docs/scripts/validate_docs.py before mkdocs build --strict. Audit site HTML links with a local script or HTTP smoke. Use the in-app browser when available for visual QA.

## Open Gaps
Visual preference remains subjective; acceptance is anchored to maintained Material components, legible custom branding, and explicit mobile/desktop smoke rather than pixel matching.
