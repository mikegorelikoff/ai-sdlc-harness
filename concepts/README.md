# Concepts

This folder explains the reusable concepts behind the AI SDLC skill library.
The concepts describe how an AI assistant reads project context, chooses the
right skill, produces artifacts, updates traceability records, and avoids wasting
tokens on broad file search.

These files are not role playbooks. Role playbooks live in `guides/`. Concept
files define the operating contracts that every role workflow depends on.

## Concept Map

- [Artifact Routing](artifact-routing.md) explains `specs-refiniment/` versus
  `specs/` and where generated files belong.
- [Artifact Metadata](artifact-metadata.md) defines the required
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

When an AI assistant works with this repository, it should treat these concept
files as system behavior contracts and the role guides as workflow playbooks.
