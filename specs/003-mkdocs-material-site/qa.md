---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-mkdocs-material-site"
  artifact: "qa.md"
  path: "specs/003-mkdocs-material-site/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/003-mkdocs-material-site/_ai_sdlc/state.toon"
  decision_log: "specs/003-mkdocs-material-site/decision-log.md"
  status: "approved"
  owner: "Dev"
  created_at: "2026-07-19"
  updated_at: "2026-07-19"
  trace_ids: []
  related_artifacts:
    - "specs/003-mkdocs-material-site/decision-log.md"
    - "specs/003-mkdocs-material-site/design.md"
    - "specs/003-mkdocs-material-site/requirements.md"
    - "specs/003-mkdocs-material-site/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "approved"
---

# QA

## Change Summary
Presentation and build migrate from custom Jekyll to MkDocs Material while preserving content, page hierarchy, public path shapes, generated catalogs, and Pages deployment.

## Acceptance Scenarios
Validate a first-time visitor path from Home to Start, search for a workflow term, switch palettes, open mobile navigation, traverse section indexes, copy a code example, and open skill/module source links.

## Regression Targets
All 43 public content pages; Tutorials, How-to, Explanation, Reference, Start, and Roadmap navigation; skill/module counts; README docs link; repository compatibility; GitHub Pages base path.

## Risk Notes
Highest risks are broken path conversion, hidden Jekyll syntax, catalog generation drift, a non-strict CI build, and visually over-customizing Material. Mitigate with one-to-one nav validation, token scans, strict build, rendered link audit, and minimal CSS.

## Validation Commands
- python3 docs/scripts/build_catalog.py --check
- python3 docs/scripts/validate_docs.py
- python3 -m unittest discover -s docs/tests -v
- python3 -m pip install -r requirements-docs.txt
- mkdocs build --strict
- git diff --check

## Manual Checks
At 360px and 1280px verify header, search, navigation, table of contents, cards, code blocks, palette toggle, focus visibility, and absence of horizontal overflow. Verify Home, Start, Skill catalog, Module catalog, and one deep guide.

## Signoff
Dev owns implementation and deterministic checks. QA acceptance requires all automated gates plus representative responsive visual smoke with no critical or high-severity findings.
