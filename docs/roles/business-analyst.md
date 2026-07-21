---
title: Business analyst guide
description: Discover and validate actors, workflows, rules, exceptions, assumptions, and measurable requirements.
---

# Business analyst guide

This guide uses business analyst (BA) and quality assurance (QA).

## Why you should care

The harness preserves business meaning across product, engineering, and QA so a
plausible implementation does not silently encode the wrong rule.

## Where you participate

Support discovery, confirm stakeholder evidence, model current and future
workflows, document actors and permissions, define rules and exceptions, expose
conflicts, make non-functional needs measurable, and review downstream stories
and tests for semantic drift.

The executable refinement graph has two BA participation modes. BA contributes
rules and workflow evidence during discovery and requirements preparation. The
formal `ai-sdlc-ba` stage runs after initial story decomposition to consolidate
that evidence into `business-context.md` and challenge story semantics before
delivery-spec synthesis. Initial stories are proposals at that point, not
approved implementation input.

## Inputs and outputs

Inputs: stakeholder evidence, domain terms, policies, current process, desired
outcome, constraints, and known exceptions. Outputs: business context, actor and
permission matrix, workflow, rule and exception catalog, assumption/conflict
registers, measurable requirements, acceptance criteria, and source links.

## Decisions you own

Own analysis quality and requirements recommendations. The named business or
product authority resolves stakeholder conflict and accepts requirements; the
BA records that decision and its affected trace IDs.

## Common mistakes

- Treating stakeholder statements as consistent facts without sources.
- Writing “fast,” “secure,” or “user friendly” without a measurable target.
- Finalizing stories before rules, exceptions, and permissions are understood;
  early story drafts must remain revisable through the later BA gate.
- Interpreting a structurally valid artifact or zero source-access gaps as
  semantic readiness.

## Example workflow

Capture competing stakeholder positions and sources; model the current and
future workflow; record each rule with applicability, exception, failure
behavior, owner, and decision reference; turn material assumptions into a
validation plan; trace accepted behavior into stories, tests, and delivery spec;
reopen downstream QA evidence when rules change.

## Review checklist

- Terms, actors, permissions, states, rules, exceptions, and sources are clear.
- Conflicts identify positions, authority, resolution, dissent, and DEC IDs.
- Material assumptions have impact, confidence, owner, validation, and status.
- Functional and non-functional requirements are measurable and traceable.
- Negative, recovery, and out-of-scope behavior is explicit.
- Accountable stakeholders confirmed the accepted interpretation.
