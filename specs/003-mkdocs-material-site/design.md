---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-mkdocs-material-site"
  artifact: "design.md"
  path: "specs/003-mkdocs-material-site/design.md"
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
    - "specs/003-mkdocs-material-site/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
---

# Design

## Overview
MkDocs owns routing, navigation, search, responsive layout, accessibility, and rendering. Repository scripts own generated catalog Markdown and deterministic source checks. A small extra stylesheet adds project identity without replacing theme components.

## Architecture
The root mkdocs.yml declares site identity, Material theme features, Markdown extensions, plugins, navigation, and output directory. docs/ contains portable Markdown plus one brand stylesheet. requirements-docs.txt pins the build dependency. GitHub Actions builds into site/ and uploads that directory to Pages.

## Components
- MkDocs Material 9.7.7 theme and built-in search plugin.
- Root mkdocs.yml navigation and feature configuration.
- docs/assets/stylesheets/extra.css for brand tokens and landing-page polish.
- docs/scripts/build_catalog.py for generated skill and module Markdown.
- docs/scripts/validate_docs.py and docs/tests/test_docs.py for source contracts.
- .github/workflows/pages.yml for strict build and Pages deployment.

## Interfaces and Contracts
- Source routes derive from Markdown paths with use_directory_urls enabled.
- Navigation entries map labels to source paths, not rendered URLs.
- Catalog generator writes complete reference/skills.md and reference/modules.md documents.
- CI runs catalog drift, source validation, unit tests, then mkdocs build --strict.

## Data Model
Each page has YAML frontmatter with title and description, followed by Markdown or Material-compatible HTML. Catalog entries are loaded from SKILL.md frontmatter and module.json manifests, sorted deterministically, and emitted as Markdown cards/tables.

## Error Handling
Strict MkDocs warnings fail CI. The validator reports file-scoped navigation, link, catalog, legacy-template, and workflow errors. Catalog check mode reports drift without mutation.

## Security Considerations
The workflow uses read-only repository access during build and grants pages/id-token permissions only to deploy. Dependencies are pinned. No analytics, remote JavaScript, secrets, or server-side execution are introduced.

## Observability
GitHub Actions logs catalog counts, validation errors, unit results, strict build output, artifact upload, and deployment URL. Local validation prints public page, skill, and module counts.

## Risks and Tradeoffs
Material adds a pinned Python dependency and generated theme assets, but removes bespoke frontend maintenance. Existing Jekyll permalinks are replaced by path-derived routes; matching source paths preserve published URLs. Generated catalogs avoid an extra templating plugin.

## Validation Strategy
Run catalog drift validation, documentation source validation, unit tests, strict MkDocs build, rendered link audit, and responsive browser smoke at representative mobile and desktop widths.

## Migration Notes
Delete Jekyll-only configuration, layouts, includes, data navigation, SCSS, JavaScript, and custom 404 source. Convert Liquid links and catalog loops. Preserve all substantive pages and public paths. Update README development commands and Pages workflow.
