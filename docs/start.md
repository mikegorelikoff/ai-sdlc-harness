---
title: Start here
description: Choose the shortest guided path from first principles to a safe first artificial-intelligence-assisted software delivery workflow.
---

# Start here

You do not need to understand all 44 packaged capabilities before
using the harness. You do
need a clear mental model, a working installation, and one bounded request.

## If the AI-assisted lifecycle or specifications are new

**Artificial intelligence (AI) software development lifecycle (SDLC)** is the
use of AI within an accountable delivery lifecycle. **Specification-driven
development (SDD)** is this repository's method for making requirements,
design, tests, tasks, and validation explicit before implementation expands.

Read these pages in order. They take you from ordinary software delivery to the
repository evidence loop used by the harness:

1. [Git and terminal primer](foundations/git-and-terminal-primer.md)
2. [Software delivery foundations](foundations/software-delivery.md)
3. [Artificial intelligence foundations](foundations/ai-foundations.md)
4. [Agents, sub-agents, and skills](foundations/agents-and-skills.md)
5. [What is AI SDLC?](foundations/ai-sdlc.md)
6. [What is SDD?](foundations/sdd.md)
7. [Why use a harness?](foundations/why-harness.md)
8. [Mental model](foundations/mental-model.md)
9. [Human and agent responsibilities](foundations/responsibilities.md)

You are ready to install when you can explain why an AI-generated code diff is
not, by itself, evidence that the right thing was built safely.

## If you understand the model and want to use it

1. Check the [prerequisites and installation scope](how-to/install.md).
2. Install into a disposable or low-risk consumer repository.
3. Complete [your first 30 minutes](onboarding/first-30-minutes.md).
4. Follow the maintainer-preview [Ship a first feature](tutorials/first-feature.md).

The command blocks use a POSIX-compatible shell: the standard command
interpreter on Linux/macOS and the form available through Windows Subsystem for
Linux (WSL) or Git Bash. `npm` is the Node.js package manager; `npx` runs a
specific package without installing that package globally. Read the primer and
install prerequisites before copying either form.

## If you are evaluating it for a team

Begin with [Evaluate and adopt](adoption/index.md), then define a
[bounded pilot](adoption/pilot.md). Do not start with a global rollout. A
decision-grade evaluation needs one team, one repository, representative
changes, an accountable owner, a baseline, explicit stop conditions, and review
of the resulting evidence.

## The four action labels

Every guided procedure uses these labels:

!!! example "Tell your agent"

    Natural-language instructions belong in the conversation with your AI
    assistant. A skill name in this block is not a shell command.

!!! terminal "Run in terminal"

    These commands run in a shell. Check the stated working directory first.

!!! info "Agent does automatically"

    The selected skill tells the agent which deterministic helpers and reads it
    should perform. You normally do not need to copy those internal commands.

!!! warning "Human checkpoint"

    Stop and review. The agent may present evidence and options, but a person
    owns the decision, approval, exception, or risk acceptance.

## The safest default

When you know the outcome but not the workflow, tell the agent to use
`ai-sdlc-navigator --quick-flow`. The navigator is read-only: it should inspect
evidence and recommend one required action rather than mutate the project.

When observable behavior or architecture will change, use SDD before code. When
the request is only a review, validation, or recovery task, enter directly at
that stage and reuse valid upstream evidence.

Already know your responsibility? Skip the learning sequence and choose from
[Skills by role](reference/skills-by-role.md). For an exact capability, schema,
path, or command, open [Reference](reference/index.md) directly.
