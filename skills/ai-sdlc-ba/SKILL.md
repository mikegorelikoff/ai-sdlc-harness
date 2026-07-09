---
name: ai-sdlc-ba
description: AI SDLC business analysis workflow. Use when Codex needs to frame a feature or change before implementation, derive actors, workflows, business rules, assumptions, acceptance criteria, and richer spec context for requirements and design.
---

# ai-sdlc-ba: Business Analysis

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-ba`
- Primary audience: BA
- Supporting audience: PM, Dev, QA
- Audience tags: BA, PM, Dev, QA
- SDLC stage: Business analysis and refinement
- Purpose: Convert a vague AI SDLC feature, refactor, or workflow request into requirements-ready business context with actors, rules, assumptions, exclusions, and measurable acceptance criteria.
- Output: Business context, rules, assumptions, out-of-scope items, acceptance criteria, and open questions

### 0.1 Required Inputs

- User request or feature/refactor intent.
- Business goal, workflow, role, provider, endpoint, or system context.
- Existing requirements, product notes, delivery artifact, or `specs-refiniment/<feature-name>/<file.md>` context if available.

### 0.2 Clarification Rules

- Ask concise questions before finalizing when role, artifact, requirements, scope, audience, or constraints are unclear.
- If optional information is missing, mark it as `TBD`, `Not provided`, or `Assumption` instead of inventing it.
- Separate confirmed facts from assumptions and open questions.
- Do not proceed to downstream synthesis when a required upstream artifact or decision is missing.

### 0.3 Output Rules

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, `specs-refiniment/<feature-name>/<file.md>` workspace, stakeholder context, or user-provided source material.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.

### 0.4 Artifact Routing

- When writing or updating files, place PM, BA, QA, Delivery, discovery, planning, refinement, and readiness artifacts at `specs-refiniment/<feature-name>/<file.md>`.
- Use the path pattern `specs-refiniment/<feature-name>/<file.md>`; choose a stable feature slug when known, otherwise use `tbd-<short-topic>` for `<feature-name>`.
- Do not write this skill's output into `specs/`; that folder is reserved for developer implementation SDD artifacts.
- If the user explicitly asks to convert a refined artifact into developer implementation work, hand off to `$ai-sdlc-sdd`.

## References

- Read `references/business-context-template.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Convert a vague AI SDLC feature, refactor, or workflow request into requirements-ready business context with actors, rules, assumptions, exclusions, and measurable acceptance criteria.

## Inputs

- Collect the user request and any explicit business goal, pain point, asset, provider, endpoint, role, or workflow name.
- Read the matching requirements document, delivery artifact, or `specs-refiniment/<feature-name>/<file.md>` package when one exists.
- Read `references/business-context-template.md` when the request needs a reusable intake structure.
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
10. Return requirements-ready BA notes and write them under `specs-refiniment/<feature-name>/<file.md>` when file output is requested.

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

- Pass when BA, PM, QA, and Dev stakeholders can use the output without guessing actors, expected outcomes, exclusions, or acceptance criteria.
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
- Do not claim assumptions are confirmed without evidence from the user, artifact, `specs-refiniment/<feature-name>/<file.md>`, code, or docs.
