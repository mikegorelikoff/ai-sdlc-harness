---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-mkdocs-material-site"
  artifact: "requirements.md"
  path: "specs/003-mkdocs-material-site/requirements.md"
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
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
  related_artifacts:
    - "specs/003-mkdocs-material-site/decision-log.md"
    - "specs/003-mkdocs-material-site/design.md"
    - "specs/003-mkdocs-material-site/plan.md"
    - "specs/003-mkdocs-material-site/qa.md"
    - "specs/003-mkdocs-material-site/tasks.md"
    - "specs/003-mkdocs-material-site/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "approved"
---

# Requirements

## Goal
Replace the custom Jekyll presentation with a polished MkDocs Material site while preserving the complete documentation corpus, intent-based information architecture, stable public URLs, generated catalogs, and GitHub Pages delivery.

## Problem Statement
The current hand-built shell technically publishes the content but looks unfinished and lacks mature documentation affordances. Readers need professional typography, responsive navigation, built-in search, light and dark modes, strong code presentation, and accessible interaction without maintaining a custom frontend framework.

## Scope
- Replace Jekyll configuration, layouts, includes, styles, scripts, and build action with MkDocs Material 9.7.7.
- Preserve all existing documentation topics and the Tutorials, How-to, Explanation, Reference, Start, and Roadmap navigation model.
- Convert Jekyll-specific Liquid and catalog templates to MkDocs-compatible Markdown.
- Add search, responsive navigation, section indexes, light/dark palette controls, code copy, anchor tracking, and a restrained project brand layer.
- Keep deterministic catalog generation, source validation, tests, and GitHub Pages artifact deployment.

## Actors
- New adopters evaluating and installing the harness.
- PM, BA, QA, Delivery, and Dev practitioners following lifecycle guidance.
- Skill and module authors consulting contracts.
- Maintainers previewing and publishing documentation.

## Inputs
- The completed documentation corpus and information architecture from specs/002-github-pages-docs/.
- Repository skills, modules, README entry point, and Pages workflow.
- Official Material for MkDocs installation, navigation, search, color, and publishing guidance.

## Outputs
- Root mkdocs.yml using the Material theme.
- Reproducible documentation dependencies.
- Material-native landing page, navigation, generated catalogs, and small brand stylesheet.
- Updated validator, tests, and GitHub Pages workflow.

## Functional Requirements
- FR-001: The site shall build with MkDocs Material 9.7.7 in strict mode.
- FR-002: Navigation shall expose every public Markdown page exactly once in the established reader-intent hierarchy.
- FR-003: Client-side search, suggestions, highlighting, and shareable searches shall be enabled.
- FR-004: Readers shall be able to switch between accessible light and dark palettes.
- FR-005: The landing page shall present the value proposition, primary actions, lifecycle, capability proof, and installation entry point using Material-native components.
- FR-006: Skill and module catalogs shall be generated as portable Markdown from authoritative repository sources.
- FR-007: The Pages workflow shall install pinned dependencies, build strictly, upload the artifact, and deploy from main.
- FR-008: Validation shall reject stale catalogs, missing navigation pages, broken internal source links, Jekyll remnants, and incomplete workflow/config contracts.

## Non-Functional Requirements
- NFR-001: The generated site shall remain usable on mobile, tablet, and desktop viewports.
- NFR-002: Custom presentation code shall be limited to a small brand stylesheet; navigation, search, accessibility, and layout shall use maintained Material components.
- NFR-003: The build shall be reproducible from a pinned Python dependency file.
- NFR-004: The build and source checks shall be deterministic and CI-friendly.
- NFR-005: Existing public route shapes shall remain stable.
- NFR-006: The migration shall be delivered as one user-visible task and one focused commit.

## Constraints
- GitHub Pages remains the hosting target and the site remains under /ai-sdlc-harness/.
- The documentation corpus remains English and repository-local.
- No paid Material Insiders features or external hosted search service are required.
- The branch is based on main because the repository has no dev branch.

## Acceptance Criteria
- AC-001: Given pinned documentation dependencies, when mkdocs build --strict runs, then Material 9.7.7 produces the complete site with no warning or error.
- AC-002: Given the documentation source, when navigation validation runs, then every public Markdown page appears exactly once in mkdocs.yml and path-derived routes match the established URL shapes.
- AC-003: Given the rendered site, when a reader navigates on mobile or desktop, then responsive navigation, local table of contents, built-in search, search suggestions/highlighting, and back-to-top controls are available.
- AC-004: Given either supported palette, when a reader switches between light and dark mode, then the preference control works and content remains readable.
- AC-005: Given a new visitor, when the home page loads, then a coherent hero, primary actions, capability cards, lifecycle explanation, and quick install example are visible.
- AC-006: Given 35 skill packages and 5 module manifests, when catalog generation and drift checking run, then every item appears once in portable Markdown with no Jekyll template marker.
- AC-007: Given representative navigation gaps, broken links, catalog drift, Jekyll remnants, or missing workflow contracts, when validation or unit tests run, then the change fails with a file-scoped diagnostic.
- AC-008: Given a push to main, when the Pages workflow runs, then it installs the pinned dependency, builds strictly, uploads site/, and deploys through the github-pages environment with least-required permissions.

## Out of Scope
- Rewriting the substantive documentation corpus.
- Paid plugins, analytics, a custom domain, multilingual content, or a version selector.
- A custom JavaScript application or custom theme fork.

## Assumptions
- The user values a mature maintained documentation experience over the existing bespoke visual shell.
- The established information architecture and page count remain correct.
- Material 9.x is compatible with GitHub Pages artifact deployment and Python 3.x.

## Open Questions
- Non-blocking: a custom logo and domain can be introduced after the Material migration is live.

## Decision Status
- All blocking decisions are resolved.
- DEC-001 selects MkDocs Material 9.7.7, its built-in search and navigation features, generated Markdown catalogs, and the existing GitHub Pages artifact deployment model.
