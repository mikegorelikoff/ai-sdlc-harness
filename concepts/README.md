# Concepts

This folder explains the reusable concepts behind the AI SDLC skill library.
The concepts describe the system design behind artifact routing, flow modes,
decision logs, lifecycle state, indexes, helper scripts, metadata, and
traceability.

These files are not role playbooks. Role playbooks live in `guides/`. Concept
files are for understanding, onboarding, maintenance, and system design review.
They are not required runtime input for every AI task; operational behavior lives
in the selected skill instructions, helper scripts, state files, and workspace
indexes.

## Concept Map

- [Artifact Routing](artifact-routing.md) explains `specs-refiniment/` versus
  `specs/` and where generated files belong.
- [Artifact Metadata And Metatags](artifact-metadata.md) defines the required
  `artifact_metadata` frontmatter and `metatags` contract.
- [Decision Log](decision-log.md) explains feature-level decision traceability.
- [Feature State Machine](feature-state-machine.md) explains `state.toon`, skill
  sequencing, and quick/full transition behavior.
- [Flow Modes](flow-modes.md) defines `--quick-flow` and `--full-flow`.
- [Specs Index](specs-index.md) explains the workspace-level TOON and Markdown
  indexes for feature discovery.
- [Skill Anatomy](skill-anatomy.md) explains `SKILL.md`, `references/`,
  `scripts/`, and `tests/`.
- [Token-Saving Scripts](token-saving-scripts.md) explains how deterministic
  scripts take over repetitive work from the AI assistant.
- [Traceability](traceability.md) explains how artifacts, state, decisions,
  validation, and generated metadata connect.

When working with the harness, use these concept files to understand why the
system behaves the way it does. Use role guides and individual `SKILL.md` files
as the workflow and execution entrypoints.
