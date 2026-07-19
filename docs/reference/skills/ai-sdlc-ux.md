---
title: Ux
description: Human-facing operating guide for ai-sdlc-ux, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-ux`

Optional AI SDLC user-experience workflow. Use when an AI assistant needs to define actors, goals, user journeys, interaction steps, loading/empty/error/success states, recovery behavior, content intent, accessibility requirements, or UX acceptance evidence and route them into traceable human and machine artifacts. Supports `--quick-flow` for a focused journey slice and `--full-flow` for strict state, accessibility, and acceptance coverage.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Discovery, refinement, and design | UX, BA, PM | Dev, QA, Accessibility, Delivery | `ux` | `ux-spec.md` and `_ai_sdlc/ux-spec.toon` |

## Why it exists

Preserve testable journeys, states, recovery, and accessibility.

## Use it when

Optional AI SDLC user-experience workflow. Use when an AI assistant needs to define actors, goals, user journeys, interaction steps, loading/empty/error/success states, recovery behavior, content intent, accessibility requirements, or UX acceptance evidence and route them into traceable human and machine artifacts. Supports `--quick-flow` for a focused journey slice and `--full-flow` for strict state, accessibility, and acceptance coverage.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it while actors, workflows, or business rules are unclear. Use `ai-sdlc-ba` instead.
- Do not use it to implement interface code. Use `ai-sdlc-sdd` instead.


## Who is involved

- **Accountable/primary:** UX, BA, PM.
- **Supporting:** Dev, QA, Accessibility, Delivery.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Owning feature root.
- UX input using `ai-sdlc-ux-input/v1`.
- Actors and requirement or acceptance trace targets.

## Tell your agent

```text
Use ai-sdlc-ux for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `ux-spec.md` and `_ai_sdlc/ux-spec.toon`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Define stable actor IDs, goals, and needs.
- Trace every journey, state, and accessibility check.
- Make steps ordered and acceptance outcomes observable.
- Cover recovery from failure and blocked user states.

## What it may write

- Write `<feature-root>/ux-spec.md`.
- Write `<feature-root>/_ai_sdlc/ux-spec.toon`.
- Use the owning workspace selected by the feature; implementation UX supports SDD.
- Keep generated image/design files separate and link them as evidence when present.

## Human checkpoints

- Ask when actor, goal, permission, channel, or success outcome is ambiguous.
- Separate user need from interface solution and visual preference.
- Include non-happy states and recovery behavior, not only a golden path.
- Do not infer accessibility conformance or user research evidence.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits one traced actor journey with explicit gaps.
- Full flow requires at least one journey, interaction state, and accessibility check.
- Both modes require exact trace targets and actor consistency.

## Deterministic helpers

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`ux.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-ux/scripts/ux.py) | Validate and route traceable UX specifications. | `python3 skills/ai-sdlc-ux/scripts/ux.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-ux/scripts/ux.py specs-refiniment/onboarding --input /tmp/ux.json --emit --quick-flow
python3 skills/ai-sdlc-ux/scripts/ux.py specs/onboarding --input /tmp/ux.json --write --full-flow --format toon
```

## Success criteria

`ai-sdlc-ux/v1` contains context, actors, journeys, interaction states,
accessibility checks, content notes, and exact trace targets.

Quality gate:

- Pass when journey actors exist, steps and acceptance are observable, states
  include behavior plus recovery, and accessibility status has evidence.
- Full flow fails without journey, state, or accessibility coverage.

## Blockers and recovery

- One actor may have several journeys with different permissions or channels.
- A state may intentionally have no recovery; document the reason explicitly.
- Accessibility checks may be planned, passed, failed, or blocked.
- Visual references remain optional evidence and never replace behavior contracts.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return actors, journey/state coverage, accessibility status, blockers, and
  output paths directly in the Codex response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or untraced mockup prose.
- Keep behavior testable and avoid presenting assumptions as research.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read `<feature-root>/_ai_sdlc/state.toon` before durable work.
    - UX is an optional capability and does not add a core lifecycle stage.
    - `--state-check` is read-only; `--begin-state` and `--complete-state` are rejected.
    - Route accepted behavior changes through owning requirements and change-impact workflows.

??? info "Artifact metadata"

    - Markdown starts with `artifact_metadata` using schema `ai-sdlc-ux-metadata/v1`.
    - Include `metatags` for `ai-sdlc`, `ux`, `experience`, and `traceable`.
    - Record feature, workspace, flow mode, state file, trace IDs, and review status.

??? info "Specs index"

    - Read the relevant `specs/_ai_sdlc/specs-index.toon` or
      `specs-refiniment/_ai_sdlc/specs-index.toon` before broad reads.
    - Refresh the matching `specs/specs-index.md` or
      `specs-refiniment/specs-index.md` only after durable writes.
    - Keep one UX artifact in the owning feature boundary.

## Example

A valid journey identifies actor `ACT-001`, ordered steps, `AC-012` traces, and
observable completion. “Make onboarding delightful” is invalid because it has
no actor, behavior, evidence, or testable outcome.

## Source contract

This page is generated from [`skills/ai-sdlc-ux/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-ux/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
