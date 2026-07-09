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

## When To Load This Reference

Load this file when the request has product or workflow ambiguity and the short
skill instructions are not enough to produce a confident `business-context.md`.
This is especially useful before requirements writing, story decomposition,
delivery spec synthesis, QA planning, or implementation SDD work.

## Input Checklist

Before drafting, look for:

- source request, ticket, transcript, or stakeholder note;
- existing workflows or screenshots;
- current implementation behavior if the feature modifies an existing system;
- role, permission, approval, or operational constraints;
- known deadlines, launch constraints, or rollout expectations;
- prior decisions in `decision-log.md`.

If an input is missing, decide whether it is blocking:

- Blocking: actor is unknown, success outcome is unknown, permission boundary is
  unknown, data-loss or compliance implication is unclear.
- Non-blocking: wording can be improved, examples are missing but workflow is
  clear, exact metric target is not yet known.

## Expanded Output Shape

Use this structure when detail matters:

| Section | Content | Evidence Needed |
|---|---|---|
| Goal | Business/operator outcome and why now | request, KPI, stakeholder note |
| Problem | Current pain, inefficiency, risk, or missed opportunity | current flow, defect, manual process |
| Actors | Humans, services, systems, decision owners | roles, permissions, integrations |
| Current Flow | Present trigger, steps, states, and handoffs | code, docs, workflow notes |
| Desired Flow | Future trigger, steps, states, and handoffs | target scenario |
| Business Rules | Invariants, permissions, time limits, exception rules | policy, domain logic |
| Acceptance Criteria | Observable pass/fail outcomes | AC IDs or scenario evidence |
| Assumptions | Defaults accepted for now | decision-log row |
| Open Questions | Questions with owner and impact | blocker evidence |

## Quick Flow Guidance

In `--quick-flow`, draft the artifact using the best available evidence.
Mark weak areas as assumptions instead of stopping, unless the gap changes core
scope, permission, security, compliance, money movement, data retention, or
irreversible user impact.

Use wording like:

- `Assumption/default: ...`
- `Evidence: ...`
- `Risk if wrong: ...`

## Full Flow Guidance

In `--full-flow`, do not silently invent:

- primary actor;
- business outcome;
- permission or approval rule;
- launch boundary;
- acceptance criterion;
- data ownership or retention rule.

Ask concise questions or mark the section blocked. Full flow should also verify
that material assumptions are represented in `decision-log.md`.

## Decision Log And Traceability

Create or update `specs-refiniment/<feature>/decision-log.md` when:

- choosing a default behavior;
- narrowing MVP scope;
- accepting an assumption;
- resolving conflicting stakeholder inputs;
- deferring a rule, metric, dependency, or edge case.

Trace every major business rule to one of:

- stakeholder input;
- existing behavior;
- product decision;
- acceptance criterion;
- explicit assumption.

## Quality Bar

A strong business context artifact lets another agent write requirements without
re-asking basic discovery questions. It should make the change understandable
without reading implementation code, but it should not pretend uncertain facts
are confirmed.
