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
