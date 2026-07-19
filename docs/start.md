---
title: Start here
description: Choose the shortest guided path from first principles to a safe first AI SDLC workflow.
---

# Start here

You do not need to understand all 44 currently installed capabilities before
using the harness. You do
need a clear mental model, a working installation, and one bounded request.

## If AI SDLC or SDD is new

Read these pages in order. They take you from ordinary software delivery to the
repository evidence loop used by the harness:

1. [What is AI SDLC?](foundations/ai-sdlc.md)
2. [What is SDD?](foundations/sdd.md)
3. [Why use a harness?](foundations/why-harness.md)
4. [Mental model](foundations/mental-model.md)
5. [Human and agent responsibilities](foundations/responsibilities.md)

You are ready to install when you can explain why an AI-generated code diff is
not, by itself, evidence that the right thing was built safely.

## If you understand the model and want to use it

1. Check the [prerequisites and installation scope](how-to/install.md).
2. Install into a disposable or low-risk consumer repository.
3. Complete [your first 30 minutes](onboarding/first-30-minutes.md).
4. Follow [Ship a first feature](tutorials/first-feature.md).

## If you are evaluating it for a team

Begin with [fit, non-goals, and adoption questions](foundations/why-harness.md).
Do not start with a global rollout. A decision-grade evaluation needs one team,
one repository, one bounded change, an accountable owner, a baseline, explicit
stop conditions, and review of the resulting evidence.

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
