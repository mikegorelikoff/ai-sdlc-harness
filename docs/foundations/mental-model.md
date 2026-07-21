---
title: Mental model
description: See how the source repository, installed skills, consumer project, artifacts, state, helpers, agent, and humans fit together.
---

# Mental model

The harness separates instructions, deterministic mechanics, evidence, and
authority. Understanding those boundaries prevents the two most common mistakes:
treating a skill name as a shell command and treating agent output as approval.

## Three environments

```text
Harness source repository
  skills/ + shared helpers + modules + schemas + tests + public docs
                     |
                     | Skills CLI install
                     v
Installed agent environment
  selected SKILL.md packages + references + scripts available to the agent
                     |
                     | agent works in
                     v
Consumer repository
  product code + specs-refiniment/ + specs/ + _ai_sdlc/ + Git evidence
```

- The **source repository** is this project. Maintainers change and test the
  harness here.
- The **installed agent environment** is where the agent discovers a selected
  skill and its helpers.
- The **consumer repository** is your software project. Delivery artifacts and
  state belong beside that work.

Cloning the source repository does not automatically install skills into a
consumer project. Installing skills does not authorize product changes.

## The operating loop

```text
Human intent → AI agent → selected skill → deterministic helpers
     ↑                                         ↓
     └── handoff ← gates/review ← durable artifacts
```

The agent supplies contextual judgment. The skill bounds that judgment. Helpers
own repeatable operations such as scaffolding, parsing, indexing, state
transitions, validation, and compatibility checks. Artifacts preserve the
result. Gates decide whether evidence is sufficient to continue. The handoff
makes the next step visible.

## Human and machine representations

Markdown is the detailed human authority for requirements, design, test cases,
QA plans, decisions, and delivery plans. TOON is the complete token-efficient
representation agents read for state, indexes, plans, context packs, and
control-plane results. JSON stays at schema, interoperability, exact recovery,
and JSONL journal boundaries.

A projection can be rebuilt. Authoritative product intent and accepted
decisions cannot be reconstructed safely by guessing.

## State is not truth by itself

`state.toon` records workflow progress and `plan.toon` records task status, but
a status such as `done` must agree with artifacts, tests, validation, and commit
evidence. If state and evidence contradict each other, the workflow blocks and
requires diagnosis; it does not choose the most convenient version.

## Flows, skills, and modes

- A **skill** performs one bounded kind of work.
- A **flow** connects skills and handoffs toward an outcome.
- `--quick-flow` and `--full-flow` change rigor inside the selected skill.
- A full 18-stage refinement is a declared cascade, not a side effect of
  `--full-flow`.
- Adaptive rigor uses risk and protected team policy to select controls.

Next: [Human and agent responsibilities](responsibilities.md).
