# PRFAQ Package Structures

Use these sections when synthesizing a PRFAQ package from validated discovery notes.

## Press Release

- Headline: customer-visible outcome, not an internal project label.
- Customer problem: who is affected and what is hard today.
- New experience: what changes for the customer or operator.
- Value proposition: why the change matters commercially or operationally.
- MVP boundary: what is included now and what is deliberately excluded.

## FAQ Package

- Customer FAQ: expected customer questions, objections, and value proof.
- Internal FAQ: delivery, support, operations, rollout, analytics, and dependency questions.
- Risk FAQ: assumptions, open decisions, compliance, privacy, scalability, and adoption risks.
- Measurement FAQ: success metrics, leading indicators, and launch-readiness checks.

## BRD Summary

- Business goals and non-goals.
- Actors, workflows, and scenarios.
- Functional and non-functional requirements.
- Acceptance logic with observable outcomes.
- Dependencies, assumptions, risks, and open questions.

## When To Load This Reference

Load this when discovery notes are long, stakeholder intent is scattered, or the
output needs to become a PRFAQ/FAQ/BRD package rather than a short summary.

## Input Quality Checklist

Confirm the source material has enough signal for:

- target customer or internal user;
- painful current alternative;
- new customer/operator experience;
- measurable business reason;
- MVP and non-goals;
- launch risks and dependencies;
- open decisions that affect delivery.

If these are absent, use the working-backwards discovery skill before finalizing
the package.

## Press Release Detail

| Part | Purpose | Quality Test |
|---|---|---|
| Headline | Names the customer-visible outcome | understandable without internal jargon |
| Date/Location | Optional launch context | does not invent fake dates unless requested |
| Opening Paragraph | Who benefits and what changed | includes customer, problem, and outcome |
| Problem Evidence | Why now | cites current pain, cost, risk, or opportunity |
| Solution | What is newly possible | avoids implementation details |
| Quote | Stakeholder/customer voice | reinforces value, not marketing filler |
| Availability | MVP boundary and rollout | clear enough for delivery planning |

## FAQ Depth

Customer FAQ should cover:

- What problem does this solve?
- Who is it for?
- Why is it better than today?
- What changes on day one?
- What limitations remain?

Internal FAQ should cover:

- What is in MVP?
- What is explicitly out of scope?
- Who owns launch, support, analytics, operations, and risk?
- What dependencies can block delivery?
- What decisions remain unresolved?

Risk FAQ should cover:

- adoption risk;
- legal/compliance risk;
- operational support risk;
- data/privacy risk;
- technical feasibility risk;
- rollback or mitigation options.

## Quick Flow Guidance

In `--quick-flow`, synthesize the PRFAQ with explicit assumptions and avoid a
long clarification loop. Keep weak areas visible in FAQ form instead of burying
them in prose.

## Full Flow Guidance

In `--full-flow`, verify that the package can support downstream backlog,
delivery, and QA work. Ask questions when MVP, actor, business value, or launch
boundary is unclear.

## Decision Log And Traceability

Record decisions for:

- headline/value proposition choice;
- MVP scope;
- out-of-scope items;
- launch approach;
- accepted assumptions;
- unresolved risks deferred to later phases.

Each material FAQ answer should trace to discovery evidence, an accepted
assumption, or a decision-log row.

## Quality Bar

A strong PRFAQ package should make it possible to derive goals, capabilities,
epics, requirements, QA risks, and release slices without losing the customer
problem or inventing delivery scope.
