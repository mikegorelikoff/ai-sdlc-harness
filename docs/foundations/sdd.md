---
title: What is SDD?
description: Learn how specification-driven development turns intent into a testable implementation contract without creating paperwork for its own sake.
---

# What is SDD?

For the full prerequisite lesson, comparison boundary, and traceability lab,
see [AI SDLC and specification-driven development](../learn/ai-sdlc-and-sdd.md).
This page remains the compact repository definition of SDD.

**Specification-driven development (SDD)** means establishing a testable delivery
contract before implementation becomes the source of truth by accident.

This is the repository's canonical meaning of **SDD**. Some organizations and
sources use the same abbreviation for a Software Design Document, software
design and development, or another local practice. Those meanings are not the
lifecycle method defined here. In informal prose this guide may say
“spec-driven,” but it always means this specification-driven workflow.

In this harness, an implementation SDD package connects:

- `requirements.md`: observable behavior, actors, constraints, and acceptance
  criteria;
- `design.md`: boundaries, components, interfaces, data, failures, security,
  and trade-offs;
- `test-cases.md`: explicit scenarios derived before implementation;
- `qa.md`: acceptance, regression, risk, environment, and signoff scope;
- `tasks.md`: bounded pieces of work with acceptance/test references;
- `decision-log.md`: material choices, evidence, owners, and status;
- `_ai_sdlc/plan.toon` and `plan.md`: one machine/human task and trace map.

## What SDD is not

SDD is not a demand for a large document before every edit. It is not a frozen
upfront specification, a replacement for discovery, or a license for the agent
to invent missing product decisions. A typo may need no SDD. A narrow bug may
need one falsifiable scenario and focused validation. A cross-service,
security-sensitive change needs stronger evidence and explicit ownership.

The size of the contract follows the uncertainty and risk—not the desire to
produce paperwork.

## Why write the spec before code?

Code is a costly place to discover that people meant different things. When the
observable contract exists first:

- an ambiguity becomes a question instead of an accidental implementation;
- tests can be derived from intent rather than copied from code behavior;
- tasks can stay small enough to review and commit atomically;
- reviewers can compare implementation with a declared design;
- changed requirements can reopen affected evidence instead of restarting all work.

## From request to evidence

For “add account lockout,” SDD might connect:

```text
AC-003: lock after 5 failed attempts within 15 minutes
  -> design: atomic per-account counter with expiry
  -> TC-007: concurrent fifth and sixth attempts
  -> T004: implement counter and lock transition
  -> validation: focused service and concurrency tests
  -> commit: feat(auth): enforce account lockout
```

The identifiers are not decoration. They let a reviewer ask: Which acceptance
criterion does this task satisfy? Which test proves it? Which commit delivered
it? What must reopen if the rule changes?

## When to use it

Use SDD when a change affects observable behavior, public or internal APIs,
architecture, data, security, multiple components, meaningful rollout risk, or
several team roles. Use a smaller path for a well-understood, low-risk change
with no contract impact. If unsure, let the read-only navigator inspect current
evidence and recommend the earliest missing stage.

`--full-flow` makes the **selected SDD workflow** stricter. It does not silently
run every product, BA, QA, and delivery stage. A full lifecycle is an explicit
multi-skill sequence with handoffs.

## Completion is evidence-based

An SDD task is complete only when the implementation, linked tests, validation,
and required commit evidence exist. Changing a checkbox does not make the work
true. Deterministic gates compare the artifacts, plan, task status, branch, and
validation before handoff.

Next: [Why use a harness?](why-harness.md).
