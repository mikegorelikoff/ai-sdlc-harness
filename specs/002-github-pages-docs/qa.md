---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "002-github-pages-docs"
  artifact: "qa.md"
  path: "specs/002-github-pages-docs/qa.md"
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
    - "specs/002-github-pages-docs/design.md"
    - "specs/002-github-pages-docs/plan.md"
    - "specs/002-github-pages-docs/requirements.md"
    - "specs/002-github-pages-docs/tasks.md"
    - "specs/002-github-pages-docs/test-cases.md"
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
Add a public GitHub Pages documentation experience and automated deployment while preserving existing repository documentation and runtime contracts.

## Acceptance Scenarios
- New visitor understands the harness and can reach installation in one action.
- Reader can choose learning, task, explanation, or reference material from grouped navigation.
- Every substantive public page is navigated once and exposes a local outline when headings exist.
- Role-based user can find the relevant workflow and authoritative repository guide.
- Maintainer can regenerate catalogs and detect drift before commit.
- GitHub Actions can build and deploy the site under the repository base path.

## Regression Targets
- Existing repository Markdown paths and links.
- Skills and module compatibility validation.
- Existing `skills-ci` workflow.
- Repository root README onboarding.

## Risk Notes
- Highest risk is broken navigation under `/ai-sdlc-harness/`; enforce `relative_url` and scan root-absolute paths.
- Catalog drift is likely as skills evolve; enforce generator check in CI.
- Hosted deployment depends on Pages repository settings outside the commit.

## Validation Commands
- `python3 docs/scripts/build_catalog.py --check`
- `python3 docs/scripts/validate_docs.py`
- `python3 -m unittest discover -s docs/tests -v`
- `python3 skills/_shared/ai_sdlc_compatibility.py --format toon`
- Jekyll build through `actions/jekyll-build-pages@v1`.

## Manual Checks
- Inspect landing, start, skills, and workflow pages at 360px and 1280px.
- Navigate by keyboard through skip link, header, mobile menu, cards, and footer.
- Confirm legibility in light and dark color schemes.
- Confirm primary navigation remains available without JavaScript.

## Signoff
- Dev owns implementation and deterministic checks.
- QA acceptance requires automated checks plus responsive browser smoke evidence.
- Deployment is ready when the workflow passes after Pages source is set to GitHub Actions.
