---
name: ai-sdlc-retrospective
description: AI SDLC evidence-backed retrospective workflow. Use when delivery work is complete or paused and an AI assistant needs to capture observations, connect them to validation or artifact evidence, formulate reviewable process or policy improvement proposals, assign ownership, and preserve the rule that policy changes require an accepted decision. Supports `--quick-flow` for focused learning and `--full-flow` for strict evidence and decision gates.
---

# ai-sdlc-retrospective: Reviewable Delivery Learning

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Retrospectives propose improvements; they never silently change policy.

## 0. Skill Card

- Skill name: `ai-sdlc-retrospective`
- Primary audience: Delivery, Dev, QA, BA
- Supporting audience: PM, platform maintainers
- Audience tags: Delivery, Dev, QA, BA, PM
- SDLC stage: Post-delivery learning
- Purpose: Separate evidence-backed observations from governed improvements.
- Output: `retrospective.md` and `_ai_sdlc/retrospective.toon`

### 0.1 Required Inputs

- Completed or paused feature root.
- Retrospective JSON containing observations and proposals.
- Exact artifact or validation evidence for every observation.

### 0.2 Clarification Rules

- Ask only when evidence, proposal owner, or intended policy target is unclear.
- Keep observed facts separate from interpretation and proposed change.
- Do not mark a proposal accepted without a durable decision reference.
- Do not infer approval from implementation, silence, or prior chat.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits draft proposals but still requires observation evidence.
- Full flow additionally requires every proposal to have an owner and every
  accepted proposal to have a decision reference.
- Neither mode applies proposals or edits target files.

### 0.3 Output Rules

- Return observation and proposal counts, accepted-decision coverage,
  blockers, and output paths directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or policy patches.
- Preserve rejected and deferred proposals for learning history.

### 0.4 Artifact Routing

- Write human output to `<feature-root>/retrospective.md`.
- Write machine output to `<feature-root>/_ai_sdlc/retrospective.toon`.
- Keep proposal target paths as references only.
- Apply accepted improvements later through the target-owning workflow.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Retrospective is a utility workflow and does not advance feature lifecycle.
- Read `_ai_sdlc/state.toon` to confirm feature identity and delivery status.
- `--state-check` is read-only; `--begin-state` and `--complete-state` are
  rejected by the finalizer.
- A proposal decision changes proposal governance status, not lifecycle state.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema
  `ai-sdlc-retrospective-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `retrospective`, `learning`, and proposal
  statuses.
- Record feature, workspace, flow mode, evidence paths, and decision refs.

## 0.7 Specs Index

- Read `specs/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/_ai_sdlc/specs-index.toon` before targeted evidence reads.
- Do not refresh `specs/specs-index.md` or
  `specs-refiniment/specs-index.md` for a read-only draft.
- Refresh indexes only through the owning workflow after durable report writes.

## References

- Read `references/retrospective-contract.md` before preparing input.
- Use `scripts/retrospective.py` to validate separation, decision safety, and
  emit or atomically write the canonical report pair.

## Script Usage

```bash
python3 skills/ai-sdlc-retrospective/scripts/retrospective.py specs/payments --input /tmp/retro.json --emit --quick-flow
python3 skills/ai-sdlc-retrospective/scripts/retrospective.py specs/payments --input /tmp/retro.json --write --full-flow --format toon
```

The finalizer never writes any path named by a proposal `target`.

## Purpose

Create a durable learning loop where teams can improve the harness from real
delivery evidence without allowing an AI session to self-modify governance.

## Inputs

- Anchor observations to repository-relative files and positive line numbers.
- Reference proposals back to one or more observation IDs.
- Give every proposal a target, owner, review status, and next action.
- Add `decision_ref` only when a proposal has actually been accepted.

## Steps

1. Review delivery evidence, outcomes, friction, escapes, and effective controls.
2. Record observations without embedding recommended changes.
3. Draft proposals that cite observation IDs and identify target plus owner.
4. Validate evidence lines and governance statuses with the finalizer.
5. Review proposals with accountable owners and record durable decisions.
6. Regenerate the report when proposal status changes.
7. Route accepted work to SDD or the owning policy/configuration workflow.

## Output Spec

The TOON schema `ai-sdlc-retrospective/v1` contains observations with exact
evidence and proposals with `based_on`, `target`, `change`, `owner`, `status`,
`decision_ref`, and `next_action`.

Quality gate:

- Pass when observations and proposals are separate, evidence is exact, every
  proposal traces to an observation, and accepted proposals cite a decision.
- Fail when a proposal is presented as an observation, approval is implied, or
  target policy content would be mutated by finalization.

## Examples

Valid accepted proposal:

```json
{"id":"PROP-001","based_on":["OBS-002"],"target":"skills/_shared/validation-policy.json","change":"Add the deterministic retry fixture to standard validation.","owner":"Dev","status":"accepted","decision_ref":"DEC-014","next_action":"Implement through a traced SDD task."}
```

Invalid counter-example: `We learned that the policy should now skip tests.` It
mixes observation and policy mutation and has no evidence or decision.

## Edge Cases

- A retrospective with observations and no proposals is valid.
- Rejected proposals retain their evidence links and rationale in `next_action`.
- An accepted proposal without `decision_ref` always fails, including quick flow.
- A target may not exist yet; the report records it without creating it.

## Scope Boundary

- Do not edit policy, configuration, skill, or source targets.
- Do not accept proposals on behalf of owners.
- Do not turn anecdotes into observations without durable evidence.
- Do not advance feature lifecycle or hide failed proposals.
- Use `$ai-sdlc-navigator` to route accepted implementation work.
