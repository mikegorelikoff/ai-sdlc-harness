# Gap Review Framework

Run this before any story or spec synthesis.

## Inputs

Possible inputs:

- PRFAQ
- FAQ package
- BRD
- readiness review notes
- discovery notes
- initiative memo or equivalent

## Review Dimensions

Check whether the package clearly defines:

- target actors and their roles;
- problem and business objective;
- launch/MVP boundaries;
- workflows and role transitions;
- business rules and constraints;
- data requirements;
- failure, rollback, and exception scenarios;
- dependencies and ownership;
- success metrics;
- unresolved decisions.

## Mandatory Blocking Questions

If any of these are still too vague, block decomposition and ask follow-ups:

- Who actually performs each core action?
- What is the main happy path from trigger to outcome?
- What are the key failure states?
- What rules decide whether an action is allowed, rejected, retried, escalated, or rolled back?
- What is in MVP versus explicitly deferred?
- Which dependencies are required before delivery starts?

## Output Shape

Return:

- confirmed facts;
- assumptions;
- contradictions;
- blockers;
- clarifying questions;
- a short go/no-go judgment for moving into story decomposition.

## When To Load This Reference

Load this when a discovery/PRFAQ/BRD package exists but may not be ready to
become delivery stories or specs. The goal is to prevent downstream artifacts
from inventing rules, actors, or workflows.

## Gap Severity Model

| Severity | Meaning | Delivery Action |
|---|---|---|
| Blocker | Story/spec synthesis would invent core behavior | stop and ask |
| High | Delivery can draft, but risk must be isolated | record and ask owner |
| Medium | Assumption is acceptable for first pass | record in decision log |
| Low | Cleanup/detail issue | proceed with note |

## Detailed Gap Matrix

| Area | Evidence To Find | Common Failure | Severity | Next Action |
|---|---|---|---|---|
| Actor | named roles/systems | "user" is generic |  |  |
| Trigger | workflow start event | trigger missing |  |  |
| Outcome | final state/value | success not observable |  |  |
| Rules | permissions, timing, exceptions | rules implied |  |  |
| Data | inputs, outputs, ownership | missing source of truth |  |  |
| Failure | errors, rollback, retry | only happy path |  |  |
| MVP | included/deferred | roadmap mixed with launch |  |  |

## Quick Flow Guidance

In `--quick-flow`, produce a compact gap report and proceed with assumptions
unless a blocker prevents story/spec synthesis entirely.

## Full Flow Guidance

In `--full-flow`, block on unknown actors, triggers, permissions, MVP boundary,
data source, failure handling, or launch-critical dependencies.

## Decision Log Guidance

Record:

- assumptions accepted to proceed;
- contradictions resolved;
- MVP boundary choices;
- deferred risks;
- owner decisions required before delivery.

## Quality Bar

A strong gap review makes the next artifact safer: every later story, workflow,
or requirement should be traceable to a confirmed fact, an explicit assumption,
or a blocker.
