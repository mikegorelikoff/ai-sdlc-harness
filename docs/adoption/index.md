---
title: Evaluate and adopt
description: Decide whether AI SDLC Harness fits your team, what evidence to require, and how to enter a bounded pilot without assuming value.
---

# Evaluate and adopt

Adoption is a management decision, not an installation command. AI SDLC Harness
can make delivery intent, evidence, gates, and handoffs more inspectable. It
cannot guarantee that a team chooses the right product, writes correct code, or
improves an organizational metric.

Use this path to answer four questions in order:

1. Is the problem real for this team?
2. Can the team operate the human approval and repository controls?
3. Does a bounded pilot produce better evidence without unacceptable burden?
4. Should the team stop, adjust, continue, or scale?

## Fit decision

| Signal | Good fit | Poor fit or prerequisite gap |
| --- | --- | --- |
| Work system | Git-based software delivery with reviewable changes. | Work is not represented in a repository. |
| AI use | Agents already help analyze, plan, code, test, or review. | The team wants an autonomous replacement for accountable roles. |
| Problem | Decisions disappear in chat; handoffs, tests, or scope are hard to reconstruct. | Existing evidence is already complete and the extra workflow has no named benefit. |
| Control | People can approve intent, risk, exceptions, release, and destructive actions. | No one will own gates or review agent output. |
| Tooling | Git, Python 3.10+, Node/npm, and a supported skill host are available. | Agent execution, repository writes, or required dependencies are prohibited. |
| Pilot | One owner, one team, one repository, a baseline, and stop conditions can be named. | The first step must be an organization-wide mandate. |

If the problem is primarily CI, deployment, project tracking, observability, or
IDE functionality, address that system directly. The harness integrates with
those systems; it does not replace them.

## Evidence ladder

Do not jump from “the demo worked” to “the organization should standardize it.”

| Evidence level | What it supports | What it does not support |
| --- | --- | --- |
| Contract tests | Helpers, schemas, state, catalogs, and recovery behave as specified. | Team productivity or business impact. |
| Guided walkthrough | A newcomer can complete a known scenario. | Behavior on the team's real constraints. |
| Bounded pilot | The selected team can operate the workflow and compare local evidence with a baseline. | Causal claims or enterprise-wide suitability. |
| Repeated use | Results persist across several representative changes and people. | Automatic compliance or guaranteed ROI. |
| Independent audit | Controls and evidence meet a named internal or external review standard. | Legal approval outside that audit's scope. |

Read [maturity and limitations](../explanation/maturity-limitations.md) before
presenting any benefit claim.

## Decision package

An adoption owner should be able to show:

- the problem statement and current baseline;
- the selected repository, team, workload, and exclusions;
- accountable product, engineering, QA, security, delivery, and pilot owners;
- allowed agent hosts, data classes, permissions, package policy, and retention;
- the [pilot plan](pilot.md), metrics dictionary, thresholds, and review dates;
- examples of requirements, decisions, tests, validation, and handoffs produced;
- incidents, exceptions, manual corrections, and abandoned paths;
- a written stop, adjust, continue, or scale decision with residual risk.

An agent can assemble this package. A person accountable for the pilot accepts
the decision.

## Recommended route

1. Review [why the harness exists](../foundations/why-harness.md).
2. Read [human and agent responsibilities](../foundations/responsibilities.md).
3. Define the [operating model and RACI](../operations/operating-model.md).
4. Approve the [governance and trust boundary](../operations/governance.md).
5. Run the [one-team pilot](pilot.md).
6. Interpret [pilot metrics](metrics.md) without claiming causality.
7. If the pilot passes, write the [staged rollout contract](rollout.md).
8. Record a scale or stop decision.

Broad rollout is a new decision. It is not an automatic final step of the pilot.
Use the rollout contract to move pilot → limited cohort → broader cohort or
standard/hold, with a separate rollback boundary for every cohort.
