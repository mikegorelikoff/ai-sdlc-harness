---
title: AI SDLC Harness
description: Understand, evaluate, and use a repository-native operating system for software delivery with AI agents.
hide:
  - navigation
---

<div class="hero" markdown>

<p class="hero__eyebrow">Repository-native AI delivery</p>

# Move at AI speed. <span class="hero__accent">Keep human control.</span>

<p class="hero__copy">AI SDLC Harness turns requests, decisions, requirements, tests, implementation, and validation into durable repository evidence—so a person or another agent can understand what happened and continue safely.</p>

[Learn the foundations](foundations/index.md){ .md-button .md-button--primary }
[Evaluate adoption](adoption/index.md){ .md-button }

<div class="metric-strip">
  <div class="metric"><strong>44</strong><span>Installed capabilities</span></div>
  <div class="metric"><strong>18</strong><span>Traceable refinement stages</span></div>
  <div class="metric"><strong>1</strong><span>Accountable evidence chain</span></div>
</div>

</div>

## The problem in one minute

AI can generate code faster than teams can reconstruct why that code should
exist, which decisions shaped it, what proves it works, and who approved the
risk. Important context stays in chats, tickets, reviews, and individual memory.
When the session ends, the next person or agent rediscovers the work—or guesses.

The harness applies the software development lifecycle (SDLC) in a form AI
agents can follow. It gives them bounded skills, deterministic helpers, visible
artifacts, explicit state, and protected gates. Humans retain authority over
intent, trade-offs, exceptions, and approval.

```text
intent -> requirement -> design -> task -> code -> test -> evidence -> handoff
```

New to these ideas? Read [What is AI SDLC?](foundations/ai-sdlc.md) and
[What is SDD?](foundations/sdd.md) before installing anything.

## Choose your path

<div class="grid cards" markdown>

-   **I need to understand it**

    ---

    Learn SDLC, AI SDLC, SDD, artifacts, evidence, gates, and handoffs from
    first principles.

    [Start Foundations →](foundations/index.md)

-   **I want to use it**

    ---

    Install project-scoped skills, ask the navigator for a safe entry point,
    and complete a guided first session.

    [Start onboarding →](onboarding/index.md)

-   **I am evaluating adoption**

    ---

    Check fit, prerequisites, non-goals, authority boundaries, maturity, and
    the evidence you should require before a pilot.

    [Evaluate the harness →](adoption/index.md)

-   **I need an exact contract**

    ---

    Look up lifecycle stages, skills, scripts, schemas, routes, flags,
    compatibility, and validation commands.

    [Open Reference →](reference/index.md)

</div>

## What it is—and is not

| It is | It is not |
| --- | --- |
| Portable instructions for AI delivery workflows. | A new IDE or autonomous developer. |
| Deterministic helpers for repeatable repository mechanics. | A replacement for product, engineering, QA, security, or legal judgment. |
| Human-readable artifacts plus complete agent state. | A hidden SaaS database or hosted telemetry service. |
| Evidence-backed gates, handoffs, and recovery. | A guarantee of correctness, compliance, or business impact. |
| A layer that can complement Git, issue tracking, CI, and agent hosts. | A project-management system, CI platform, or deployment authority. |

## A safe first experience

1. Read [the mental model](foundations/mental-model.md).
2. Check [fit, prerequisites, and non-goals](foundations/why-harness.md).
3. [Install project-scoped skills](how-to/install.md).
4. Complete [your first 30 minutes](onboarding/first-30-minutes.md).
5. Follow the runnable [first feature tutorial](tutorials/first-feature.md).

At every step, the documentation labels what to tell the agent, what to run in
a terminal, what the agent does automatically, and where a human must decide.

The canonical project-scoped installation command is:

```bash
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0 --all
```

Run it from the consumer repository only after reviewing the
[installation prerequisites, third-party installer telemetry, and trust
boundary](how-to/install.md). The opt-out applies to the Skills CLI; it does not
describe the independent data behavior of an agent host or model provider.
The pinned CLI requires Node.js `>=22.20.0`; verify `node --version` before
starting.

## What the evidence proves

Repository tests verify skill contracts, schemas, state transitions, generated
artifacts, compatibility, recovery, and documentation mechanics. This proves
the harness mechanisms behave as specified. It does **not** prove a causal
improvement in your cycle time, quality, or cost. Treat those outcomes as pilot
hypotheses and evaluate them with your own baseline and review.

[Begin with Foundations →](foundations/index.md){ .md-button .md-button--primary }
[Evaluate a bounded pilot →](adoption/index.md){ .md-button }
