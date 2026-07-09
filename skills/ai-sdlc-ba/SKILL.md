---
name: ai-sdlc-ba
description: AI SDLC business analysis workflow. Use when Codex needs to frame a feature or change before implementation, derive actors, workflows, business rules, assumptions, acceptance criteria, and richer spec context for requirements and design.
---

# AI SDLC BA

## Purpose

Convert a vague AI SDLC feature, refactor, or workflow request into requirements-ready business context with actors, rules, assumptions, exclusions, and measurable acceptance criteria.

## Inputs

- Collect the user request and any explicit business goal, pain point, asset, provider, endpoint, role, or workflow name.
- Read the matching `requirements.md` when a spec exists.
- Read `references/business-context-template.md` when the request needs a reusable intake structure.
- Collect related Asana context from `$ai-sdlc-asana-traceability` for medium or large work.
- Collect current behavior from code or docs only when the desired business behavior depends on existing workflow semantics.

## Steps

1. State the business goal in one sentence.
2. State the problem in one sentence that names the current failure, missing capability, or decision gap.
3. List actors and systems that initiate, approve, observe, or are affected by the change.
4. Describe current behavior and desired behavior as separate bullets.
5. Extract business rules using deterministic language: `When X, the system must Y`.
6. List assumptions separately from confirmed facts.
7. List out-of-scope items so implementation does not expand silently.
8. Write acceptance criteria as observable pass/fail statements.
9. Write open questions only for decisions that materially affect scope, design, validation, or rollout.
10. Feed confirmed content into `requirements.md` before design or implementation expands.

## Output Spec

Use this format for visible BA output or requirements-ready notes:

```text
Business context:
- Goal: one sentence.
- Problem: one sentence.
- Actors: actor list.
- Current behavior: concrete observed behavior.
- Desired behavior: concrete target behavior.

Rules and constraints:
- Rule: When condition, the system must outcome.
- Constraint: limit, dependency, policy, or compatibility requirement.
- Assumption: unverified statement that must be validated or accepted.
- Out of scope: explicit exclusion.

Acceptance criteria:
- AC-001: Given setup, when action, then observable result.

Open questions:
- Question: decision needed, why it matters, owner if known.
```

Quality gate:

- Pass when a developer can write `requirements.md` without guessing actors, expected outcomes, exclusions, or acceptance criteria.
- Fail when the output contains vague goals such as "make it better", acceptance criteria without observable results, or assumptions mixed into facts.

## Examples

Before:

```text
Add better BitGo wallet support.
```

After:

```text
Business context:
- Goal: Let operations view BitGo enterprise wallet details before initiating transfers.
- Problem: Operators cannot verify wallet scope and enterprise linkage from the current setup screen.
- Actors: operations user, BitGo integration, AI SDLC API.
- Current behavior: The UI shows configured provider status without wallet-level enterprise details.
- Desired behavior: The UI shows enterprise-linked wallet details required for transfer readiness review.

Acceptance criteria:
- AC-001: Given an organization with BitGo configured, when an operations user opens custodian setup, then the response includes enterprise ID, wallet IDs, and display labels.
```

Invalid counter-example:

```text
Acceptance criteria:
- Works correctly.
```

Reject this because it has no actor, trigger, or observable result.

## Edge Cases

- Stop before implementation when acceptance criteria would require inventing product policy.
- Mark unknowns as assumptions or open questions; do not hide them inside requirements.
- Use `TODO(dm): exact question` in specs when a delivery-manager decision is required.
- Keep BA output out of solution architecture unless a business rule constrains design.
- Use `$ai-sdlc-sdd` after BA to update requirements, design, test cases, QA, and tasks.

## Scope Boundary

- Do not design APIs, schemas, data models, or package boundaries; use `$ai-sdlc-sdd` and architecture guidance for design.
- Do not write implementation tasks except when translating accepted BA output into requirements context.
- Do not create or move Asana tasks; use `$ai-sdlc-asana-traceability`.
- Do not claim assumptions are confirmed without evidence from the user, spec, Asana, code, or docs.
