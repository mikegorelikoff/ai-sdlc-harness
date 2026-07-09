# Interview Framework

Use this progressively. Do not ask every question in one turn.

## Global Rules

- Ask a maximum of 5 to 7 questions per turn.
- After every answer:
  - summarize what was learned;
  - separate facts, assumptions, hypotheses, decisions made, decisions needed, open questions, risks, and dependencies;
  - identify contradictions and weak claims;
  - ask follow-ups before advancing if the stage is not clear enough.
- Challenge vague phrases and force measurable or observable definitions.
- Do not finalize discovery until the following are clear enough:
  - target customer;
  - customer problem;
  - current alternative or workaround;
  - value proposition;
  - business objective;
  - MVP;
  - success metrics;
  - main risks;
  - key dependencies.

## When To Load This Reference

Load this reference when the user asks to discover, clarify, shape, pressure-test,
or turn a rough idea into a usable initiative package. Use it progressively; do
not dump the whole interview at once.

## Quick Flow Guidance

In `--quick-flow`:

- ask only the smallest set of questions needed to avoid a bad direction;
- infer non-critical details as assumptions;
- produce a compact discovery summary quickly;
- record assumptions and decisions.

## Full Flow Guidance

In `--full-flow`:

- proceed stage by stage;
- verify contradictions before moving on;
- ask follow-up questions whenever core scope, value, role, metric, or MVP is
  unclear;
- produce a more rigorous discovery package with traceability.

## Decision Capture During Discovery

After each stage, classify notes into:

| Type | Meaning | Example |
|---|---|---|
| Fact | Confirmed by user/source | "Admins approve refunds" |
| Assumption | Used temporarily | "Refund approval uses existing roles" |
| Hypothesis | Needs validation | "Manual review is the bottleneck" |
| Decision | Chosen direction | "MVP excludes automated payouts" |
| Open Question | Needs owner/input | "Who can override a rejection?" |
| Risk | Could affect success | "Third-party API has rate limits" |
| Dependency | External prerequisite | "Legal must approve retention policy" |

Material decisions should be copied into `specs-refiniment/<feature>/decision-log.md`.

## Stage 1. Initiative Context

Start with:

`Describe the initiative in 3–5 sentences: what do you want to create, who is it for, what problem does it solve, and why is it important now?`

Clarify:

- what we want to build;
- who it is for;
- why this matters now;
- what business problem it solves;
- who initiated the idea;
- what stage it is in;
- deadlines or external pressure;
- whether it is a product, feature, internal tool, process change, or strategic initiative.

## Stage 2. Customer and Problem

Clarify:

- primary customer or user;
- multiple segments if relevant;
- buyer, user, approver, and beneficiary;
- pain, unmet need, and current workaround;
- frequency, cost, and consequences of the problem;
- whether customers know they have the problem;
- evidence that the problem matters.

Ask for concrete situations, not abstractions.

## Stage 3. Current Process and Alternatives

Clarify:

- current workflow and systems;
- manual workarounds;
- teams involved;
- customer touchpoints;
- competitors, substitutes, and internal alternatives;
- likes, dislikes, switching barriers, and adoption blockers.

## Stage 4. Value Proposition

Force the value proposition into this shape:

`For [target customer], who struggles with [problem], this product provides [solution/value], so they can achieve [outcome], unlike [current alternative].`

Clarify immediate value, long-term value, and what creates a real wow moment.

## Stage 5. Business Goals

Clarify:

- why the business should invest;
- which metrics should improve;
- revenue, cost, retention, efficiency, quality, or risk impact;
- constraints on budget, team, timeline;
- key stakeholders and decision-makers.

Separate primary from secondary goals.

## Stage 6. Users, Roles, and Permissions

Clarify all user types, permissions, restrictions, and role-specific success criteria.

## Stage 7. User Scenarios and Use Cases

Collect primary, secondary, rare, edge, negative, failure, onboarding, support, cancellation, rollback, and recovery scenarios.

For each scenario, clarify:

- trigger;
- actor;
- goal;
- steps;
- expected result;
- business rule;
- data involved;
- error conditions;
- acceptance criteria.

## Stage 8. MVP Scope

Use MoSCoW:

- Must-have
- Should-have
- Could-have
- Won't-have for now

Challenge every must-have by asking what happens if it is excluded and whether it can be manual first.

## Stage 9. Functional Requirements

Capture requirements in this form:

`As a [user role], I want to [action], so that [outcome].`

Add acceptance criteria when useful:

`Given ... When ... Then ...`

Also capture owner, priority, metrics, assumptions, dependencies, and open questions.

## Stage 10. Non-Functional Requirements

Check for:

- performance;
- reliability;
- availability;
- scalability;
- security;
- privacy;
- compliance;
- accessibility;
- localization;
- auditability;
- monitoring;
- retention;
- SLA and recovery needs.

## Stage 11. Data, Analytics, and Reporting

Clarify what data is collected, displayed, stored, exported, and protected; which events are tracked; which dashboards and reports are needed; and which product, business, operational, customer, and risk metrics matter.

## Stage 12. Operations and Support

Clarify support ownership, manual processes, automation needs, escalation paths, training, documentation, monitoring, incident handling, and fallback processes.

## Stage 13. Go-to-Market and Launch

Clarify launch audience, pilot or rollout shape, messaging, packaging, enablement needs, launch blockers, go/no-go criteria, and post-launch monitoring.

## Stage 14. Risks and Dependencies

Enumerate customer, business, product, technical, operational, legal, compliance, financial, reputational, adoption, delivery, and data risks.

For each risk, capture:

- description;
- likelihood;
- impact;
- warning signal;
- mitigation;
- owner;
- fallback plan.
