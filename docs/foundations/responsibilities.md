---
title: Human and agent responsibilities
description: Understand who owns intent, evidence, execution, approval, validation, and escalation throughout AI-assisted delivery.
---

# Human and agent responsibilities

The harness is designed for accountable collaboration, not autonomous delivery.
An agent can do a large amount of work; that does not transfer ownership of
product intent, risk acceptance, or release authority.

## Responsibility model

| Activity | Accountable human | Agent may | Agent must not |
| --- | --- | --- | --- |
| Define outcome and priority | Product/Delivery owner | Clarify, synthesize, identify contradictions | Invent customer value or approve priority |
| Accept requirements and design trade-offs | Product, BA, Architecture, Dev owner as applicable | Propose options and record evidence | Resolve a material missing decision silently |
| Define QA risk and signoff | QA/Delivery owner | Derive cases, coverage, and gaps | Claim acceptance from test generation alone |
| Modify code and artifacts | Dev/Documentation owner | Execute bounded tasks in allowed scope | Expand scope or weaken protected policy |
| Approve security, compliance, or exception | Named Security/Compliance/Delivery approver | Present evidence and waiver constraints | Self-approve or create an indefinite waiver |
| Validate and review | Dev, QA, Security, reviewer | Run deterministic checks and report findings | Hide failures or convert warnings into success |
| Commit, release, or roll back | Repository/Release owner | Prepare commands and evidence within authority | Deploy or publish without granted authority |

Small teams may have one person wearing several roles. The responsibilities do
not disappear; name which role that person is acting as at each checkpoint.

## What the agent is good at

- Reading current repository evidence and locating gaps.
- Applying a consistent skill contract and flow mode.
- Producing structured options, requirements, designs, cases, and plans.
- Running declared deterministic helpers.
- Keeping trace IDs, artifact routes, indexes, and handoffs consistent.
- Stopping when prerequisites, permissions, evidence, or decisions are missing.

## Human checkpoints

A person must intervene when work changes intended behavior, accepts a material
trade-off, weakens or waives a protected control, authorizes sensitive access,
approves release risk, or resolves a contradiction between authoritative
evidence. The agent should state the decision, why it is needed, available
options, affected artifacts, and the exact evidence that will record it.

## Maintainer responsibilities

Harness maintainers change skill packages, helpers, schemas, modules,
compatibility baselines, and generated documentation. They own repository-wide
tests and safe versioning. A product engineer using an installed skill should
not edit internal helpers merely to bypass a failed gate; fix the project
evidence or escalate a genuine harness defect.

## The handoff boundary

Every durable workflow returns `ai-sdlc-handoff/v1` with:

- `result`: what happened and the evidence identity;
- `blockers`: what prevents a safe claim or transition;
- `next_required`: the smallest action that must happen next;
- `next_optional`: useful but non-blocking actions.

Actions include a reason, command or agent invocation, and expected artifact.
The handoff does not grant authority; it makes the requested next decision or
operation inspectable.

Use the [glossary](glossary.md) when a role or control-plane term is unfamiliar.
