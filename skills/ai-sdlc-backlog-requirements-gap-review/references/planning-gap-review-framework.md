# Planning Gap Review Framework

Use this checklist to decide whether an initiative package is ready for backlog decomposition.

## Minimum Planning Bar

- Business goal is explicit and measurable enough to prioritize work.
- Target actors, user groups, or operational roles are named.
- MVP, launch, and out-of-scope boundaries are visible.
- Major dependencies, integrations, data sources, and constraints are identified.
- Priority drivers are clear enough to sequence features and stories.

## Gap Categories

- Scope gaps: unclear MVP, overloaded launch slice, hidden roadmap work.
- Actor gaps: missing user roles, admin roles, operational owners, or external systems.
- Rule gaps: missing business rules, permissions, data constraints, or exception handling.
- Priority gaps: no basis for ordering epics, features, stories, or release slices.
- Dependency gaps: unresolved technical, legal, operational, data, vendor, or design inputs.

## Review Output

- Ready: the package can move to capability and epic mapping.
- Ready with notes: decomposition can start, but specific assumptions must stay visible.
- Not ready: blocking gaps must be clarified before backlog work starts.

## When To Load This Reference

Load before backlog decomposition when requirements look incomplete, overloaded,
or ambiguous. This review protects downstream planning from turning unclear
intent into false precision.

## Evidence To Inspect

- PRFAQ, BRD, discovery notes, product brief, workflow docs.
- Existing backlog or roadmap items.
- Decision log entries from discovery/refinement.
- Known constraints, risks, dependencies, and launch expectations.

## Gap Severity

| Severity | Meaning | Action |
|---|---|---|
| Blocker | Decomposition would invent scope or rules | ask/stop |
| Major | Decomposition can start but high-risk assumptions remain | record and isolate |
| Minor | Can proceed with documented assumption | record |
| None | Sufficient evidence | proceed |

## Detailed Review Matrix

| Category | Question | Evidence | Severity | Recommended Action |
|---|---|---|---|---|
| Goal | Is the business outcome measurable enough? | KPI, statement |  |  |
| Actor | Are user/operator/system roles explicit? | roles, workflows |  |  |
| Scope | Is MVP distinct from later work? | scope notes |  |  |
| Rules | Are permissions and domain rules explicit? | BRD, policy |  |  |
| Dependencies | Are external blockers visible? | vendor/legal/data |  |  |
| Priority | Can items be sequenced? | value/risk |  |  |

## Quick Flow Guidance

In `--quick-flow`, return a concise go/no-go with assumptions. Ask only when a
gap blocks all meaningful backlog movement.

## Full Flow Guidance

In `--full-flow`, require enough evidence to support goals, actors, MVP,
dependencies, rules, and priority. Do not let a package proceed as ready when a
major category is unsupported.

## Decision Log Guidance

Add decision-log rows for accepted assumptions, MVP boundary decisions, priority
drivers, and known gaps allowed to move forward.
