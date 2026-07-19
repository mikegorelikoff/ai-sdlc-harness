---
title: Why use a harness?
description: Decide whether AI SDLC Harness fits your team, what it provides, and which prerequisites and non-goals matter.
---

# Why use a harness?

A single prompt can tell an agent what to do once. A **harness** makes safe,
repeatable behavior available across requests, agents, sessions, repositories,
and roles.

AI SDLC Harness is a repository-native collection of:

- skills that define bounded AI workflows;
- deterministic scripts that own repetitive mechanics;
- human-readable delivery artifacts;
- complete machine state and indexes for agent continuity;
- policy, approval, trust, validation, and recovery controls;
- a common handoff contract that makes the next action explicit.

It is not a long-running server. The operating context stays beside the work and
can be inspected through Git.

## Problems it is designed to reduce

- Re-explaining the repository and delivery context in every chat.
- Requirements, decisions, tests, and commits drifting apart.
- Agents starting implementation before missing rules are visible.
- “Done” claims without current validation or review evidence.
- Inconsistent rigor across low-risk patches and high-risk changes.
- Unsafe continuation after interruption, requirement change, or failed write.
- Vendor lock-in caused by keeping the workflow only in one assistant's UI.

## Good fit

The strongest fit is a software team using Git and one or more AI agents that
wants traceable delivery without adopting a hosted orchestration platform. It is
especially useful when work crosses PM, BA, QA, Delivery, Dev, Security, or
Architecture boundaries; when another agent may continue later; or when audit,
approval, recovery, and evidence freshness matter.

## Prerequisites

- A software repository and basic Git discipline.
- Humans willing to own decisions and review agent changes.
- An agent environment that can read skill packages and run allowed helpers.
- Python 3.10+ for deterministic repository scripts.
- Node.js `>=22.20.0`/npm and network access for the documented Skills CLI installation.
- A willingness to keep authoritative artifacts in the repository.

## Poor fit and non-goals

Do not adopt the harness as a workaround for absent engineering ownership or a
policy that forbids repository-resident agent instructions. It is not:

- an IDE, issue tracker, project-management tool, CI platform, or deployer;
- an autonomous approver or release authority;
- a guarantee that generated code is correct or secure;
- a compliance certification or legal interpretation;
- hosted telemetry or a system that exports your source by design;
- a substitute for customer research, architecture ownership, QA, security, or
  accountable management decisions.

## Maturity and proof

The repository mechanically tests contracts, schemas, helpers, state,
compatibility, documentation, and recovery paths. This is evidence that the
implemented mechanisms behave as specified. Organizational outcomes—cycle time,
rework, escaped defects, handoff delay, or cost—depend on team behavior and must
be evaluated in a bounded pilot. Inventory counts such as 44 capabilities describe
coverage, not business value.

## A sensible first decision

Do not begin with organization-wide installation. Choose one team, one
repository, and one low-to-medium-risk change. Name an accountable pilot owner,
record the current baseline, agree on human checkpoints and stop conditions,
then compare the resulting evidence with the old way of working.

If the fit is plausible, continue to the [mental model](mental-model.md) and
[installation guide](../how-to/install.md).
