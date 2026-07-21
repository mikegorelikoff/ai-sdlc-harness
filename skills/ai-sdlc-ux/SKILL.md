---
name: ai-sdlc-ux
description: Optional AI SDLC user-experience workflow. Use when an AI assistant needs to define actors, goals, user journeys, interaction steps, loading/empty/error/success states, recovery behavior, content intent, accessibility requirements, or UX acceptance evidence and route them into traceable human and machine artifacts. Supports `--quick-flow` for a focused journey slice and `--full-flow` for strict state, accessibility, and acceptance coverage.
---

# ai-sdlc-ux: Traceable Experience Specification

> Optional domain skill, not required by the core module.
> Every rule below is important to follow. None of it can be skipped.
> UX artifacts specify behavior; they do not imply stakeholder approval or visual fidelity.

## 0. Skill Card

- Skill name: `ai-sdlc-ux`
- Primary audience: UX, BA, PM
- Supporting audience: Dev, QA, Accessibility, Delivery
- Audience tags: UX, BA, PM, Dev, QA
- SDLC stage: Discovery, refinement, and design
- Purpose: Preserve testable journeys, states, recovery, and accessibility.
- Output: `ux-spec.md` and `_ai_sdlc/ux-spec.toon`

### 0.1 Required Inputs

- Owning feature root.
- UX input using `ai-sdlc-ux-input/v1`.
- Actors and requirement or acceptance trace targets.

### 0.2 Clarification Rules

- Ask when actor, goal, permission, channel, or success outcome is ambiguous.
- Separate user need from interface solution and visual preference.
- Include non-happy states and recovery behavior, not only a golden path.
- Do not infer accessibility conformance or user research evidence.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits one traced actor journey with explicit gaps.
- Full flow requires at least one journey, interaction state, and accessibility check.
- Both modes require exact trace targets and actor consistency.

### 0.3 Output Rules

- Return actors, journey/state coverage, accessibility status, blockers, and
  output paths directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or untraced mockup prose.
- Keep behavior testable and avoid presenting assumptions as research.

### 0.4 Artifact Routing

- Write `<feature-root>/ux-spec.md`.
- Write `<feature-root>/_ai_sdlc/ux-spec.toon`.
- Use the owning workspace selected by the feature; implementation UX supports SDD.
- Keep generated image/design files separate and link them as evidence when present.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read `<feature-root>/_ai_sdlc/state.toon` before durable work.
- UX is an optional capability and does not add a core lifecycle stage.
- `--state-check` is read-only; `--begin-state` and `--complete-state` are rejected.
- Route accepted behavior changes through owning requirements and change-impact workflows.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema `ai-sdlc-ux-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `ux`, `experience`, and `traceable`.
- Record feature, workspace, flow mode, state file, trace IDs, and review status.

## 0.7 Specs Index

- Read the relevant `specs/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/_ai_sdlc/specs-index.toon` before broad reads.
- Refresh the matching `specs/specs-index.md` or
  `specs-refiniment/specs-index.md` only after durable writes.
- Keep one UX artifact in the owning feature boundary.

## References

- Read `references/ux-contract.md` for actor, journey, state, and accessibility fields.
- Use `scripts/ux.py` to validate and route the canonical artifact pair.

## Script Usage

```bash
python3 skills/ai-sdlc-ux/scripts/ux.py specs-refiniment/onboarding --input /tmp/ux.json --emit --quick-flow
python3 skills/ai-sdlc-ux/scripts/ux.py specs/onboarding --input /tmp/ux.json --write --full-flow --format toon
```

## Purpose

Add explicit experience behavior where it creates value without forcing visual
design work into every delivery path or reducing UX to generic acceptance prose.

## Inputs

- Define stable actor IDs, goals, and needs.
- Trace every journey, state, and accessibility check.
- Make steps ordered and acceptance outcomes observable.
- Cover recovery from failure and blocked user states.

## Steps

1. Read customer/problem evidence, requirements, actors, and constraints.
2. Define actors and their goals without inventing research claims.
3. Map end-to-end journeys with ordered steps and acceptance outcomes.
4. Specify loading, empty, error, permission, success, and recovery states.
5. Define accessibility requirements and evidence status.
6. Finalize routed Markdown and TOON outputs.
7. Route behavior changes to BA/SDD and test cases.

## Output Spec

`ai-sdlc-ux/v1` contains context, actors, journeys, interaction states,
accessibility checks, content notes, and exact trace targets.

Quality gate:

- Pass when journey actors exist, steps and acceptance are observable, states
  include behavior plus recovery, and accessibility status has evidence.
- Full flow fails without journey, state, or accessibility coverage.

## Examples

A valid journey identifies actor `ACT-001`, ordered steps, `AC-012` traces, and
observable completion. “Make onboarding delightful” is invalid because it has
no actor, behavior, evidence, or testable outcome.

## Edge Cases

- One actor may have several journeys with different permissions or channels.
- A state may intentionally have no recovery; document the reason explicitly.
- Accessibility checks may be planned, passed, failed, or blocked.
- Visual references remain optional evidence and never replace behavior contracts.

## Scope Boundary

- Do not claim user validation without research evidence.
- Do not generate production UI code unless separately requested through SDD.
- Do not replace business rules, requirements, or test cases.
- Do not mark accessibility conformance from intent alone.
- Use `$ai-sdlc-change-impact` when accepted UX behavior invalidates downstream work.
