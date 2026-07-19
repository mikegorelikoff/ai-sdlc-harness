---
title: Role-based paths
description: Enter the AI SDLC lifecycle from the responsibilities, artifacts, gates, and handoffs owned by your role.
---

# Role-based paths

You do not need to read every capability guide. Start with the shared
[foundations](../foundations/index.md), then follow the path closest to your
accountability. Roles may collapse in a small team; decision authority must not.

## New or junior engineer

**Outcome:** complete one bounded change without guessing which instructions
are agent prompts, shell commands, or human decisions.

1. Read the [mental model](../foundations/mental-model.md).
2. Complete [your first 30 minutes](first-30-minutes.md).
3. Run the [first-feature tutorial](../tutorials/first-feature.md).
4. Learn [implementation](../flows/implementation.md) and [recovery](../flows/recovery.md).
5. Look up only the selected [skill guide](../reference/skills.md).

Stop when expected behavior, authority, evidence, or the correct repository is
unclear. Escalate to the owning lead instead of asking the agent to choose risk.

## PM or product owner

**Own:** customer problem, value, scope, priority, product decisions, and
acceptance of material trade-offs.

Follow [complete refinement](../flows/refinement.md) from discovery through
PRFAQ, requirements readiness, goals, epics, backlog, and release slicing.
Review the actual refinement artifacts: `discovery.md`, `prfaq.md`,
`requirements-readiness.md`, `goal-capability-map.md`, `backlog.md`, and
`release-slicing.md`, plus the feature decision log. The business requirements
document (BRD) is a section inside `prfaq.md`, not a separate refinement file.
The later implementation SDD owns `specs/<feature>/requirements.md`; it is not
a refinement output. The agent may synthesize evidence; it cannot accept
customer value, priority, or rollout risk for you.

## Business analyst

**Own:** actors, workflows, business rules, acceptance logic, assumptions, and
delivery clarification.

Use the BA, delivery-package gap, story decomposition, and delivery-spec guides
from the [skill catalog](../reference/skills.md). Hand implementation a
self-contained observable behavior contract, not a pointer to a chat. Reopen
the earliest producer when a downstream question reveals missing business
logic.

## QA or test owner

**Own:** testability, coverage strategy, acceptance validation, test evidence,
and QA readiness/signoff within organizational policy.

Enter the refinement journey at QA requirements gap review, test scope and
strategy, test cases, suite synthesis, or traceability/readiness. During build,
use [implementation validation](../flows/implementation.md). An agent may derive
and run tests; it cannot decide that uncovered risk is acceptable.

## Developer or engineering lead

**Own:** technical design, task boundaries, implementation correctness,
review resolution, and engineering risk recommendations.

Use [spec-driven development](../foundations/sdd.md), then the complete
[implementation journey](../flows/implementation.md): branch, SDD, task context,
implementation, validation, review, commit prep, and release handoff. The lead
checks that upstream behavior is usable before allowing design or code to hide
a requirement gap.

## Architecture or platform

**Own:** system boundaries, integration constraints, compatibility, operability,
and platform policy.

Read the [system model](../explanation/system-model.md),
[artifact authority](../explanation/artifact-authority.md), and
[optional modules](../explanation/modules.md). Use architecture, project
context, workflow, host adapter, doctor, and module guides. Approve host
capabilities and compatibility changes; do not treat an agent-generated diagram
as architecture acceptance.

## Security, privacy, or compliance

**Own:** threat/risk interpretation, data classification, permissions,
exceptions, incidents, and required review.

Start with [governance and trust](../operations/governance.md), then use
security testing, approvals/sandbox, policy, package trust, and evidence council
guides. Preserve the distinction between deterministic evidence and human risk
acceptance. Legal or regulatory conclusions require qualified review outside
the harness.

## Delivery, release, or operations

**Own:** sequencing, readiness, release/rollback coordination, runtime controls,
and incident handoff.

Read [the operating model](../operations/operating-model.md),
[control-plane flows](../flows/control-plane.md), and the
[troubleshooting runbook](../operations/troubleshooting.md). Use validation,
runtime, workflow, policy, doctor, package trust, and retrospective guides.
Release and deployment authority remain in the organization's delivery system.

## Harness maintainer

**Own:** package contracts, shared runtime, schemas, compatibility, catalogs,
tests, documentation, release evidence, and deprecation.

Use the [maintainer path](../maintainers/index.md), then
[extend safely](../maintainers/extend.md) and
[prepare a release](../maintainers/release.md). Work in a source checkout, not
an installed mirror in a consumer repository.

## Engineering manager or VP

**Own:** fit, accountable operating model, risk tolerance, pilot scope,
resources, stop/scale decision, and organizational claims.

Use [Evaluate and adopt](../adoption/index.md), approve the
[bounded pilot](../adoption/pilot.md), interpret
[metrics](../adoption/metrics.md), and review
[maturity and limitations](../explanation/maturity-limitations.md). Do not infer
ROI from helper counts or a successful tutorial.

## When one person has several roles

Write the role currently being exercised next to each decision. The same person
may be Responsible and Accountable, but the agent is never Accountable. For
high-risk work, require a second human reviewer even when the team is small.
Use the [RACI and collapse rules](../operations/operating-model.md) as the
minimum operating contract.
