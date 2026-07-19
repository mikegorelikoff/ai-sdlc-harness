---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "002-github-pages-docs"
  artifact: "requirements.md"
  path: "specs/002-github-pages-docs/requirements.md"
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
    - "AC-009"
    - "AC-010"
    - "AC-011"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
  related_artifacts:
    - "specs/002-github-pages-docs/decision-log.md"
    - "specs/002-github-pages-docs/design.md"
    - "specs/002-github-pages-docs/plan.md"
    - "specs/002-github-pages-docs/qa.md"
    - "specs/002-github-pages-docs/tasks.md"
    - "specs/002-github-pages-docs/test-cases.md"
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
Publish a polished, maintainable GitHub Pages documentation site that explains the AI SDLC harness, helps users start quickly, and exposes the existing guides, concepts, skills, and optional modules.

## Problem Statement
The repository contains strong Markdown documentation but it is optimized for source browsing. New users lack a coherent web entry point, searchable navigation, clear role-based journeys, and an automated publishing path.

## Scope
- Add a Jekyll site under `docs/` with a responsive custom theme.
- Organize approximately forty pages by reader intent: tutorials, how-to guides, explanation, and reference.
- Add grouped sidebar navigation, local page outlines, and previous/next learning paths.
- Cover onboarding, established-project adoption, lifecycle execution, customization, recovery, governance, core concepts, and technical contracts.
- Generate navigable skill and module catalog data from repository sources.
- Add local deterministic validation for links, metadata, navigation coverage, catalog coverage, and critical HTML/CSS assets.
- Add a GitHub Actions workflow that builds and deploys the Pages artifact from `main`.

## Actors
- First-time adopters evaluating the harness.
- PM, BA, QA, Delivery, and Dev practitioners seeking role-specific workflows.
- AI assistant and skill authors looking up contracts and extension points.
- Repository maintainers publishing documentation releases.

## Inputs
- Existing `README.md`, `FAQ.md`, `guides/`, `concepts/`, `skills/`, and `modules/` sources.
- Repository identity and GitHub Pages base URL metadata.
- Official GitHub Pages custom-workflow contract.

## Outputs
- Responsive static documentation site in `docs/`.
- Machine-generated skill and module catalog data consumed by Jekyll.
- Deterministic documentation validation script and tests.
- Pages build/deploy workflow.

## Functional Requirements
- FR-001: The site shall present a clear value proposition and a start-here path from the landing page.
- FR-002: Every documentation page shall expose persistent desktop/mobile navigation grouped by reader intent.
- FR-003: Tutorials shall provide end-to-end learning paths; how-to guides shall solve bounded tasks; explanations shall teach system reasoning; references shall state exact contracts.
- FR-004: The published source shall contain roughly forty substantive pages across the four documentation modes, including section indexes.
- FR-005: Grouped navigation shall expose every public page exactly once and local page outlines shall expose meaningful headings.
- FR-006: A generated catalog shall list every installed skill with purpose and package link.
- FR-007: A generated catalog shall list every module with compatibility and capability metadata.
- FR-008: Internal links, referenced local files, navigation membership, and page metadata shall be validated deterministically.
- FR-009: GitHub Actions shall build a Pages artifact and deploy it only from `main` or manual dispatch.
- FR-010: The site shall work under the repository Pages base path, not only at domain root.

## Non-Functional Requirements
- NFR-001: The site shall be usable at mobile, tablet, and desktop widths.
- NFR-002: Core navigation and content shall remain usable without JavaScript.
- NFR-003: CSS and client JavaScript shall have no runtime third-party dependency.
- NFR-004: The generated site shall use semantic landmarks, visible focus states, sufficient contrast, and reduced-motion support.
- NFR-005: Catalog generation and validation shall use Python standard library only.
- NFR-006: Each implementation task shall be represented by one focused commit.

## Constraints
- GitHub Pages and GitHub Actions are the hosting and delivery targets.
- Repository Markdown remains the authoritative detailed source; web pages reorganize, explain, and link rather than silently replacing delivery contracts.
- Public pages must contain project-specific substance rather than placeholder summaries.
- The current feature branch is based on the completed adaptive harness roadmap because no `dev` branch exists.
- Pages must support the project path `/ai-sdlc-harness/`.

## Acceptance Criteria
- AC-001: Given a new visitor, when the landing page loads, then the product promise, primary workflow, start action, and repository action are visible without opening source files.
- AC-002: Given any primary page, when viewed at 360px and 1280px widths, then grouped navigation and content remain readable and operable.
- AC-003: Given the documentation source, when navigation validation runs, then at least 38 substantive public pages are present and every non-error page is represented exactly once in grouped navigation.
- AC-004: Given a reader goal, when the matching section is opened, then tutorials teach complete journeys, how-to pages provide bounded procedures, explanations provide rationale, and references provide exact contracts.
- AC-005: Given a content page with multiple headings, when it loads with JavaScript, then a local page outline is generated; without JavaScript the content and primary navigation remain usable.
- AC-006: Given the repository skills, when catalog generation runs, then every `skills/*/SKILL.md` package is represented exactly once.
- AC-007: Given module manifests, when catalog generation runs, then every module is represented with declared skills and compatibility.
- AC-008: Given site source changes, when documentation validation runs, then broken local links, missing frontmatter, missing critical assets, unlisted pages, and catalog drift fail with actionable diagnostics.
- AC-009: Given a Pages build, when deployed under the repository base path, then styles, scripts, navigation, and canonical links resolve correctly.
- AC-010: Given a push to `main`, when the Pages workflow runs, then it builds, uploads, and deploys through the `github-pages` environment with least-required permissions.
- AC-011: Given JavaScript is unavailable or reduced motion is requested, then primary content/navigation remain accessible and animations do not block use.

## Out of Scope
- Full-text search service or hosted analytics.
- A custom domain or DNS configuration.
- Automatic publication of every internal SDD artifact.
- Replacing authoritative repository Markdown with a CMS.
- Interactive account, authentication, or server-side features.

## Assumptions
- The user intended GitHub Pages (`github.io`) documentation.
- English is the initial site language because repository documentation is English.
- GitHub Actions will be selected as the Pages publishing source in repository settings.
- A custom Jekyll layout provides enough polish without adding a Node toolchain.

## Open Questions
- Non-blocking: custom domain and analytics can be added later if requested.
- Non-blocking: multilingual navigation can be introduced after the English information architecture stabilizes.

## Decision Status
- All blocking decisions are resolved for implementation.
- DEC-001 selects native Jekyll with a custom dependency-free presentation layer.
- DEC-002 selects generated catalogs plus curated web pages, keeping repository Markdown authoritative.
- DEC-003 selects the official two-job GitHub Pages Actions deployment contract.
