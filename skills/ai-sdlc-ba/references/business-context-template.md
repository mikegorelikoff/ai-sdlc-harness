# Business Context Template

Use this structure when the request needs stronger upstream framing before
writing or updating `requirements.md`.

## Minimal Shape

- Goal: the business outcome or operator outcome
- Problem: what is broken, missing, risky, or inefficient today
- Actors: human users, services, operators, or external systems involved
- Current flow: how the workflow behaves today
- Desired flow: how it should behave after the change
- Rules: business invariants, permissions, timing, or lifecycle constraints
- Assumptions: temporary defaults or unresolved dependencies
- Acceptance criteria: observable outcomes
- Out of scope: explicit non-goals

## Prompts

- Which actor benefits or is constrained by the change?
- Which workflow step changes, and which steps must stay stable?
- Which business rule is easy to violate if it is not written down?
- Which acceptance criterion is observable without reading implementation
  details?
