---
name: ai-sdlc-working-backwards-discovery
description: Use when a user needs a staged working-backwards interview to clarify the customer problem, audience, value proposition, business case, MVP, requirements, risks, and success metrics before any PRFAQ is written.
---

# ai-sdlc-working-backwards-discovery: Working Backwards Discovery

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-working-backwards-discovery`
- Primary audience: PM
- Supporting audience: BA, Delivery
- Audience tags: PM, BA
- SDLC stage: Discovery / initiative framing
- Purpose: Run the discovery interview that turns an initiative idea into a structured, business-grounded definition.
- Output: Structured discovery notes, clarified assumptions, open questions, and PRFAQ-ready facts

### 0.1 Required Inputs

- Initiative idea or product problem.
- Known customer, user, or stakeholder context.
- Business goal, constraint, or launch driver if available.

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

- Read `references/interview-framework.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Run the discovery interview that turns an initiative idea into a structured, business-grounded definition.

## Use When

- The user wants a PRFAQ but the initiative is still fuzzy.
- The user needs help clarifying customer pain, target audience, business goals, requirements, and risks.
- The user wants a critical product partner who will challenge vague statements.

## Do Not Use When

- The initiative already has a validated, clear requirements package and only needs final document drafting.
- The task is technical implementation planning without business discovery.

## Workflow

1. Start at Stage 1 initiative context.
2. Ask a maximum of 5 to 7 questions at a time.
3. After every answer, summarize facts, assumptions, contradictions, and open questions.
4. Challenge vague wording until it becomes measurable, observable, or testable.
5. Stay in the current stage until the clarity bar is met.
6. Do not hand off to synthesis until the discovery minimums are present.

## Interview Rules

- Ask for real examples and current workarounds.
- Separate facts from assumptions and hypotheses.
- Keep decisions made distinct from decisions still needed.
- Push back if the MVP becomes a disguised full roadmap.
- Capture risks, dependencies, and out-of-scope items as they appear.

## Framework

Use `references/interview-framework.md` for the staged question structure.

## Completion Criteria

- Target customer is specific.
- Customer problem and current workaround are clear.
- Value proposition is explicit.
- Business objective and MVP are defined.
- Success metrics, risks, and dependencies are materially captured.
