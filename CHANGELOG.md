# Changelog

## Unreleased

### Added

- Expanded `concepts/` with detailed system architecture, the canonical
  18-stage refinement lifecycle, context/quality semantics, and safe
  migration/concurrency behavior.
- Added authority hierarchies, invariants, status matrices, worked traceability
  examples, consistency checks, and recovery playbooks across concept docs.
- Added safe `--check`/`--apply` migration for legacy TOON and Markdown paths,
  with hard failure for divergent canonical and legacy content.
- Added tiered artifact quality signals and full-cascade gating.
- Added per-skill context snapshots and a skill-neutral feature source manifest.
- Added bounded `ai-sdlc-context/v2` TOON packs with exact source evidence,
  trace anchors, structural gaps, and targeted `next_reads` ranges.
- Added optional fingerprinted feature-local context caching and an
  informational raw/pack/targeted-reread benchmark CLI.
- Added SDD-specific compact context and TOON workflow status output.
- Added a short human-readable stdout summary after successful artifact
  finalization.
- Added stdin-driven `--section` and `--finalize` artifact assembly across the
  20 shared profile skills.
- Added deterministic decision-log row insertion with `--decision-row`.
- Added `sdd_artifact_scaffold.py` for content-only generation of the five SDD
  source Markdown artifacts.

### Changed

- Centralized the 18-stage refinement order, predecessors, artifact names,
  sections, tables, and token budgets in one canonical profile registry.
- Moved delivery handoff after QA traceability and made index writes atomic and
  state-aware.
- Routed every maintained TOON file through `_ai_sdlc`; derived context files
  are reproducible and ignored by Git.
- Profile analysis keeps Markdown as the human-readable default and exposes
  bounded TOON through `--format toon` for token-efficient agent context.
- Scaffold scripts now own Markdown initialization, section placement, metadata,
  atomic writes, and index refresh; the AI supplies only section bodies.
- Centralized SDD artifact section definitions for scaffold and validator reuse.

## v0.3.0 - 2026-07-10

### Added

- Added `concepts/` documentation for the core system model:
  - artifact routing;
  - artifact metadata and metatags;
  - decision logs;
  - flow modes;
  - feature state machine;
  - scripts;
  - specs index;
  - traceability.
- Added PM and Dev role guides to match the existing BA and QA guide model.
- Added role/workflow diagrams showing skill relationships, handoffs, and feedback loops.
- Added shared script infrastructure under `skills/_shared/` for:
  - artifact metadata generation;
  - specs index generation;
  - state machine enforcement;
  - script contract tests.
- Added deterministic helper scripts and tests across skills so agents can offload repetitive artifact scaffolding, validation, and token-heavy checks.
- Added `decision-log.md` requirements and a shared decision-log structure across skills.
- Added `--quick-flow` and `--full-flow` behavior across skill descriptions and helper scripts.
- Added TOON-based feature state machine guidance so LLMs can enforce lifecycle sequencing before moving to the next skill.
- Added specs index outputs for both AI and humans:
  - `specs-index.toon`
  - `specs-index.md`
- Added artifact metadata and metatag requirements for generated Markdown artifacts.
- Added SDD `plan.toon` as the machine-readable implementation execution plan.
- Added SDD `plan.md` as the human-readable execution plan generated from plan links and TOON task status.
- Added `skills/ai-sdlc-sdd/scripts/plan_links.py` to emit, write, and validate `plan.toon` plus `plan.md`.
- Added `skills/ai-sdlc-sdd/scripts/check_refinement_context.py` to enforce upstream refinement context in SDD full flow.
- Added SDD tests for:
  - `plan.toon` presence;
  - `plan.md` link coverage;
  - TOON task status syncing into Markdown task checkboxes;
  - full-flow refinement blockers;
  - completed upstream refinement context.

### Changed

- Reworked the top-level `README.md` to keep setup, repository purpose, skill workflow, and starting points concise.
- Updated `guides/workflow.md` to describe the full PM -> BA -> QA -> Delivery -> Dev lifecycle and how AI produces/consumes artifacts.
- Updated `guides/dev.md` to include `plan.toon` and `plan.md` in Dev-owned SDD context and diagrams.
- Updated `concepts/artifact-routing.md` to document `plan.toon` and `plan.md` as implementation SDD artifacts.
- Updated every skill to describe:
  - consistent flow flags;
  - decision-log usage;
  - artifact metadata;
  - state machine participation;
  - specs index refresh behavior;
  - helper script usage where available.
- Updated references across skills with more detailed templates, structures, checklists, and examples.
- Updated SDD validation so the implementation package now requires:
  - `requirements.md`
  - `design.md`
  - `test-cases.md`
  - `qa.md`
  - `tasks.md`
  - `plan.toon`
  - `plan.md`
- Updated SDD full flow so it consumes upstream refinement artifacts from `specs-refiniment/<feature-name>/`, including delivery spec and QA readiness evidence.
- Updated SDD analysis to require `plan.md` links for acceptance criteria, test cases, tasks, and core SDD artifacts.
- Updated SDD status evaluation to include `plan.toon`, `plan.md`, and full-flow upstream refinement gates.
- Updated code review readiness to require `plan.toon` and `plan.md` for medium/large SDD-backed work.
- Updated commit readiness to run SDD gates and `plan_links.py --check` when a spec is provided.
- Moved script tests out of `scripts/` folders into per-skill `tests/` folders for consistency.
- Standardized test coverage expectations so every skill script has colocated tests.

### Removed

- Removed old test-file placement from `scripts/` directories in favor of dedicated `tests/` directories.
- Removed old SDD assumptions that treated the implementation package as a five-file spec.

### Validation

- Verified Python syntax for the updated SDD, code-review, and commit-prep scripts.
- Ran SDD validator tests.
- Ran SDD workflow tests.
- Ran the shared repository-wide skill script contract test suite.

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
