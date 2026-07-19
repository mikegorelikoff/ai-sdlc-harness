---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "002-github-pages-docs"
  artifact: "design.md"
  path: "specs/002-github-pages-docs/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/002-github-pages-docs/_ai_sdlc/state.toon"
  decision_log: "specs/002-github-pages-docs/decision-log.md"
  status: "approved"
  owner: "Dev"
  created_at: "2026-07-19"
  updated_at: "2026-07-19"
  trace_ids: []
  related_artifacts:
    - "specs/002-github-pages-docs/decision-log.md"
    - "specs/002-github-pages-docs/plan.md"
    - "specs/002-github-pages-docs/qa.md"
    - "specs/002-github-pages-docs/requirements.md"
    - "specs/002-github-pages-docs/tasks.md"
    - "specs/002-github-pages-docs/test-cases.md"
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
Create a Jekyll site rooted at `docs/` with an intent-based information architecture. Liquid layouts and includes provide the shared shell, grouped sidebar, local outline, and learning-path navigation; SCSS/CSS and a small progressive-enhancement script provide the visual system and mobile behavior. Python generation converts skill frontmatter and module JSON into Jekyll data files.

## Architecture
Source content lives in `docs/` across four modes: `tutorials/` for learning journeys, `how-to/` for bounded tasks, `explanation/` for rationale and mental models, and `reference/` for exact contracts. `_layouts/default.html` owns the document shell, `_includes/` owns navigation and reusable sections, `_data/navigation.yml` owns the complete public information architecture, `_data/` owns generated catalogs, and `assets/` owns local presentation resources. A standard-library Python tool refreshes catalogs and validates source contracts. GitHub Actions builds with the official Pages Jekyll action and deploys the resulting artifact.

## Components
- Site shell: default layout, header, grouped sidebar, local outline, footer, skip link, SEO/social metadata.
- Information architecture: welcome, roadmap, four section indexes, and approximately 36 detailed content pages.
- Learning paths: section-purpose framing plus previous/next actions on detailed pages.
- Design system: color, typography, spacing, cards, callouts, code, tables, responsive navigation.
- Catalog generator: parses skill YAML-lite frontmatter and module JSON into deterministic YAML.
- Documentation validator: checks frontmatter, local links, anchors, required assets, page count, navigation membership, and catalog parity.
- Pages workflow: build artifact and environment-bound deploy job.

## Interfaces and Contracts
- Every public page has Jekyll frontmatter with `layout`, `title`, `description`, `nav_order`, and `permalink`.
- Every public page except the error page appears exactly once in `_data/navigation.yml`.
- Navigation groups use `title`, `url`, and `children`; child entries use `title` and `url`.
- Navigation entries and assets use `relative_url` so project base paths work.
- Local outlines are progressive enhancement generated from visible `h2` and `h3` elements.
- Generated `_data/skills.yml` records `id`, `name`, `description`, `path`, and optional module ownership.
- Generated `_data/modules.yml` records manifest identity, version, compatibility, description, and skills.
- Validation exits non-zero with path-scoped diagnostics.
- Workflow uses GitHub's current official Pages actions and minimal permissions.

## Data Model
- Page metadata: layout, title, description, navigation order, permalink.
- Skill entry: id, display name, description, repository path, module list.
- Module entry: id, name, version, description, harness API range, skill IDs.
- Navigation entry: title, URL, optional section and external flag.
- Build metadata: repository URL, base URL, social image, release label.

## Error Handling
- Missing or malformed skill frontmatter fails catalog generation with its path.
- Invalid module JSON or undeclared skill references fail generation.
- Broken relative links or fragments fail validation with source and target.
- Missing required frontmatter or critical assets fail validation.
- Mobile navigation script failure leaves semantic links visible through CSS/no-JS behavior.

## Security Considerations
- No secrets or environment contents are embedded into generated pages.
- Liquid output uses repository-controlled data only.
- Workflow permissions default to `contents: read`; only deploy receives `pages: write` and `id-token: write`.
- No third-party browser scripts, analytics, remote fonts, or arbitrary HTML injection pipeline is introduced.

## Observability
- CI logs separate catalog generation, docs validation, Jekyll build, artifact upload, and deployment.
- Validator reports counts for pages, skills, modules, and checked links.
- Deployment job exposes the resulting `page_url` through the GitHub environment.

## Risks and Tradeoffs
- Curated pages can drift from source docs; catalog generation and repository links reduce duplication.
- Jekyll build behavior exists mainly in CI; local source validation remains dependency-free and a Docker/Bundler path can be added later.
- A custom visual layer requires CSS maintenance but avoids theme lock-in and remote dependencies.
- Publishing requires the repository Pages source to be set to GitHub Actions once.

## Validation Strategy
- Unit-test catalog parsing and documentation link checks with temporary fixtures.
- Run generator in check mode to detect catalog drift.
- Run validator against `docs/`, requiring at least 38 navigated public pages.
- Validate that every public page is listed exactly once and every navigation target exists.
- Validate YAML workflow shape and required action/permission contracts.
- Build with Jekyll locally when available and rely on the official Pages build action in CI.
- Perform responsive browser smoke checks at mobile and desktop widths.

## Migration Notes
- Existing README, FAQ, guides, concepts, skills, and modules remain in place.
- GitHub Pages is additive and does not change skill/runtime compatibility.
- A future custom domain only requires repository Pages settings and optional CNAME work.
