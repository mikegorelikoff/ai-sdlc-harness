# FAQ

## What is this harness?

AI Software Development Lifecycle (AI SDLC) Harness is a lifecycle harness for
traceable artificial-intelligence-assisted delivery across product management
(PM), business analysis (BA), quality assurance (QA), delivery, and software
development (Dev). It preserves state, decisions, evidence,
and workflow handoffs as repository artifacts that different AI assistants and
team members can continue safely.


## Is this domain-specific?

No. The harness is domain-agnostic. It focuses on software delivery workflow
structure: discovery, refinement, QA, implementation, validation, review, and
commit preparation. Domain-specific rules can be added through project artifacts
and skill inputs.

## Can this work with a private repository?

Yes. Configure GitHub access for the machine or agent environment before using
`npx skills`. Use SSH, `gh auth login`, or an HTTPS credential helper/token with
read access to the repository.

## Do small changes need the full workflow?

No. Use `--quick-flow` or a single focused skill for low-risk work. Use
`--full-flow` when the change needs stronger traceability, upstream context,
questions, validation evidence, or handoff confidence.

## What does TOON do?

Token-Oriented Object Notation (TOON) files provide compact machine-readable
continuity for artificial intelligence (AI). They let the
assistant inspect state, feature indexes, and execution plans before opening
larger Markdown artifacts.

Common examples:

- `state.toon` tracks feature lifecycle state.
- `specs-index.toon` summarizes feature artifacts.
- `plan.toon` links implementation tasks, status, dependencies, tests, and
  validation order.
- Profile-script context packs carry exact facts, trace IDs, blockers, and
  source line references within a configurable context budget. They are
  derived views and never replace the full Markdown specification.

When a pack cannot include all useful evidence, `next_reads` identifies the
smallest source sections and line ranges the assistant should inspect next.

## Where do generated artifacts go?

Use `specs-refiniment/` for upstream PM, BA, QA, Delivery, discovery,
refinement, readiness, and handoff artifacts.

Use `specs/` for developer implementation Specification-driven development
(SDD) artifacts.

This separation keeps product/refinement context useful as upstream evidence
without mixing it into implementation-owned specs.

## What is the difference between quick flow and full flow?

`--quick-flow` is fast and assumption-driven. It is useful when the task is
low-risk or already clear enough to move.

`--full-flow` is strict and evidence-driven. It is useful when work needs
questions answered, upstream context checked, traceability preserved, and
validation evidence recorded.

## Do concepts need to be read by the AI every time?

No. `concepts/` explains the system for teams and maintainers. Operational
behavior lives in the selected skill, helper scripts, state files, and workspace
indexes.

## What should a new user read first?

Start with:

- [README.md](README.md) for installation and overview.
- [Start here](docs/start.md) for the progressive learning path.
- [Foundations](docs/foundations/index.md) when AI-assisted delivery or SDD is
  new.
- [Skills by role](docs/reference/skills-by-role.md) for current role and task
  routing.
- [Tutorials](docs/tutorials/index.md) for runnable delivery journeys.

The tracked `guides/` and `concepts/` trees are historical context, not the
canonical public learning path. Current behavior is documented under `docs/`.
