---
title: Retrospective
description: Human-facing operating guide for ai-sdlc-retrospective, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-retrospective`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Post-delivery learning | Delivery, Dev, QA, BA | PM, platform maintainers | `core` | `retrospective.md` and `_ai_sdlc/retrospective.toon` |

## Why it exists

Separate evidence-backed observations from governed improvements.

## Use it when

AI SDLC evidence-backed retrospective workflow. Use when delivery work is complete or paused and an AI assistant needs to capture observations, connect them to validation or artifact evidence, formulate reviewable process or policy improvement proposals, assign ownership, and preserve the rule that policy changes require an accepted decision. Supports `--quick-flow` for focused learning and `--full-flow` for strict evidence and decision gates.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it while the run or its evidence is still incomplete. Use `ai-sdlc-runtime` or `ai-sdlc-validation` instead.
- Do not use it to adopt a proposal automatically. Use `ai-sdlc-policy` and `ai-sdlc-change-set` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Completed or paused feature root.
- Retrospective JSON containing observations and proposals.
- Exact artifact or validation evidence for every observation.

## Tell your agent

```text
Use ai-sdlc-retrospective for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `retrospective.md` and `_ai_sdlc/retrospective.toon`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Anchor observations to repository-relative files and positive line numbers.
- Reference proposals back to one or more observation IDs.
- Give every proposal a target, owner, review status, and next action.
- Add `decision_ref` only when a proposal has actually been accepted.

## What it may write

- Write human output to `<feature-root>/retrospective.md`.
- Write machine output to `<feature-root>/_ai_sdlc/retrospective.toon`.
- Keep proposal target paths as references only.
- Apply accepted improvements later through the target-owning workflow.

## Human checkpoints

- Ask only when evidence, proposal owner, or intended policy target is unclear.
- Keep observed facts separate from interpretation and proposed change.
- Do not mark a proposal accepted without a durable decision reference.
- Do not infer approval from implementation, silence, or prior chat.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits draft proposals but still requires observation evidence.
- Full flow additionally requires every proposal to have an owner and every
  accepted proposal to have a decision reference.
- Neither mode applies proposals or edits target files.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`retrospective.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-retrospective/scripts/retrospective.py) | Validate and render evidence-backed retrospective learning reports. | `python3 skills/ai-sdlc-retrospective/scripts/retrospective.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-retrospective/scripts/retrospective.py specs/payments --input /tmp/retro.json --emit --quick-flow
python3 skills/ai-sdlc-retrospective/scripts/retrospective.py specs/payments --input /tmp/retro.json --write --full-flow --format toon
```

The finalizer never writes any path named by a proposal `target`.

## Success criteria

The TOON schema `ai-sdlc-retrospective/v1` contains observations with exact
evidence and proposals with `based_on`, `target`, `change`, `owner`, `status`,
`decision_ref`, and `next_action`.

Quality gate:

- Pass when observations and proposals are separate, evidence is exact, every
  proposal traces to an observation, and accepted proposals cite a decision.
- Fail when a proposal is presented as an observation, approval is implied, or
  target policy content would be mutated by finalization.

## Blockers and recovery

- A retrospective with observations and no proposals is valid.
- Rejected proposals retain their evidence links and rationale in `next_action`.
- An accepted proposal without `decision_ref` always fails, including quick flow.
- A target may not exist yet; the report records it without creating it.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return observation and proposal counts, accepted-decision coverage,
  blockers, and output paths directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or policy patches.
- Preserve rejected and deferred proposals for learning history.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Retrospective is a utility workflow and does not advance feature lifecycle.
    - Read `_ai_sdlc/state.toon` to confirm feature identity and delivery status.
    - `--state-check` is read-only; `--begin-state` and `--complete-state` are
      rejected by the finalizer.
    - A proposal decision changes proposal governance status, not lifecycle state.

??? info "Artifact metadata"

    - Markdown starts with `artifact_metadata` using schema
      `ai-sdlc-retrospective-metadata/v1`.
    - Include `metatags` for `ai-sdlc`, `retrospective`, `learning`, and proposal
      statuses.
    - Record feature, workspace, flow mode, evidence paths, and decision refs.

??? info "Specs index"

    - Read `specs/_ai_sdlc/specs-index.toon` or
      `specs-refiniment/_ai_sdlc/specs-index.toon` before targeted evidence reads.
    - Do not refresh `specs/specs-index.md` or
      `specs-refiniment/specs-index.md` for a read-only draft.
    - Refresh indexes only through the owning workflow after durable report writes.

## Example

Valid accepted proposal:

```json
{"id":"PROP-001","based_on":["OBS-002"],"target":"skills/_shared/validation-policy.json","change":"Add the deterministic retry fixture to standard validation.","owner":"Dev","status":"accepted","decision_ref":"DEC-014","next_action":"Implement through a traced SDD task."}
```

Invalid counter-example: `We learned that the policy should now skip tests.` It
mixes observation and policy mutation and has no evidence or decision.

## Source contract

This page is generated from [`skills/ai-sdlc-retrospective/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-retrospective/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
