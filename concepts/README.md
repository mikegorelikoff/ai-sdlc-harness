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

Start with [System Model](system-model.md) for architecture and authority. Read
[Refinement Lifecycle](refinement-lifecycle.md) for the end-to-end cascade, then
use the focused concept files when changing a contract or diagnosing a package.

## Concept Map

- [System Model](system-model.md) explains the architecture layers, authority
  hierarchy, invariants, end-to-end data flow, and recovery model.
- [Refinement Lifecycle](refinement-lifecycle.md) defines the canonical
  18-stage cascade, predecessor graph, completion semantics, and SDD handoff.
- [Context And Quality Gates](context-and-quality.md) explains source union,
  context snapshots, 24k budgets, self-contained artifacts, and tiered gates.
- [Migration And Concurrency](migration-and-concurrency.md) explains canonical
  paths, legacy conflict handling, atomic writes, locks, and recovery.
- [Artifact Routing](artifact-routing.md) explains `specs-refiniment/` versus
  `specs/` and where generated files belong.
- [Layered Configuration](layered-configuration.md) defines deterministic
  base/team/user precedence, per-value provenance, and protected gates.
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

## Suggested Reading Paths

- **New maintainer:** System Model → Skill Anatomy → Artifact Routing → State
  Machine → Context And Quality → Migration And Concurrency.
- **PM/BA/QA workflow owner:** Refinement Lifecycle → Flow Modes → Decision Log
  → Traceability.
- **Runtime contributor:** Token-Saving Scripts → Context And Quality → Specs
  Index → Migration And Concurrency.
- **Incident/recovery:** System Model authority hierarchy → Migration And
  Concurrency recovery → State/Artifact consistency → package status gates.
