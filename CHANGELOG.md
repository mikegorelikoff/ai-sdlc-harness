# Changelog

## v0.2.0 - 2026-07-09

### Added

- Added a tool-agnostic `README.md` that explains the AI SDLC skill library purpose, artifact routing, guides, installation, and usage across AI tools.
- Added operating guides under `guides/`:
  - `guides/workflow.md`
  - `guides/ba.md`
  - `guides/qa.md`
- Added missing local references for planning and PRFAQ workflows:
  - `skills/ai-sdlc-backlog-requirements-gap-review/references/planning-gap-review-framework.md`
  - `skills/ai-sdlc-prfaq-package-synthesis/references/prfaq-package-structures.md`

### Changed

- Standardized skill documentation around `ai-sdlc-<slug>` naming.
- Expanded every skill card with audience metadata for PM, BA, QA, Dev, and Delivery usage.
- Documented artifact routing rules:
  - PM, BA, QA, Delivery, discovery, refinement, and readiness outputs go to `specs-refiniment/<feature-name>/<file.md>`.
  - Developer SDD implementation packages go to `specs/<feature-name>/<file.md>`.
- Updated developer-facing skills to treat `specs-refiniment/` as upstream context and `specs/` as implementation-only output.
- Updated validation and commit helper scripts/tests after removing Asana traceability requirements.

### Removed

- Removed the duplicate Asana traceability skill.
- Removed Asana traceability requirements from SDD validation, commit validation, test fixtures, and skill documentation.
