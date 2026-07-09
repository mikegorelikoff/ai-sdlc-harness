# FAQ

## Is this external delivery framework?

No. This is not external delivery framework, not a external delivery framework-compatible preset, and not a external delivery framework clone.
external delivery framework is a broad AI agile agent method. AI SDLC Skill Library is a lifecycle
harness for traceable AI-assisted delivery across PM, BA, QA, Delivery, and Dev.


## Is this domain-specific?

No. The library is domain-agnostic. It focuses on software delivery workflow
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

TOON files provide compact machine-readable continuity for AI. They let the
assistant inspect state, feature indexes, and execution plans before opening
larger Markdown artifacts.

Common examples:

- `state.toon` tracks feature lifecycle state.
- `specs-index.toon` summarizes feature artifacts.
- `plan.toon` links implementation tasks, status, dependencies, tests, and
  validation order.

## Where do generated artifacts go?

Use `specs-refiniment/` for upstream PM, BA, QA, Delivery, discovery,
refinement, readiness, and handoff artifacts.

Use `specs/` for developer implementation SDD artifacts.

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
- [guides/workflow.md](guides/workflow.md) for the end-to-end lifecycle.
- The role guide that matches the current work:
  - [PM](guides/pm.md)
  - [BA](guides/ba.md)
  - [QA](guides/qa.md)
  - [Dev](guides/dev.md)

Use [concepts/README.md](concepts/README.md) when you want to understand the
system design behind the harness.
