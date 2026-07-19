---
title: Navigator
description: Human-facing operating guide for ai-sdlc-navigator, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-navigator`

AI SDLC context-aware navigation workflow. Use when an AI assistant needs to determine what to do next, select the right installed skill, start or resume a feature, explain blockers, inspect available capabilities, or provide evidence-backed required and optional next actions from repository state. Supports `--quick-flow` for compact guidance and `--full-flow` for stricter context verification.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Cross-lifecycle navigation | PM, BA, QA, Delivery, Dev | AI assistants, agent runners, workflow maintainers | `core` | Read-only Markdown or TOON navigation report |

## Why it exists

Inspect compact repository control records and recommend one ranked required action plus relevant optional actions with reasons, exact invocations, expected artifacts, and blockers.

## Use it when

AI SDLC context-aware navigation workflow. Use when an AI assistant needs to determine what to do next, select the right installed skill, start or resume a feature, explain blockers, inspect available capabilities, or provide evidence-backed required and optional next actions from repository state. Supports `--quick-flow` for compact guidance and `--full-flow` for stricter context verification.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it when the correct skill is already known and execution is requested. Use that owning skill instead; the navigator is read-only.


## Who is involved

- **Accountable/primary:** PM, BA, QA, Delivery, Dev.
- **Supporting:** AI assistants, agent runners, workflow maintainers.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Target repository root.
- Optional natural-language intent.
- Optional explicit feature slug.
- Requested human-readable Markdown or compact TOON format.

## Tell your agent

```text
Use ai-sdlc-navigator for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Read-only Markdown or TOON navigation report, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Collect the repository root from the current workspace or `--root`.
- Collect the user request as `--intent` when intent should influence fallback
  routing.
- Collect `--feature` when the user identifies an exact feature.
- Collect current branch, dirty-tree count, installed skill directories, and
  feature-local state through the script.
- In full flow, confirm relevant workspace indexes exist when features are
  expected.

## What it may write

- This skill is read-only and produces no canonical artifact.
- Read refinement control records from `specs-refiniment/` and implementation
  control records from `specs/`.
- Do not create or update decision logs, SDD artifacts, refinement artifacts,
  indexes, or plans.
- Route durable work to the recommended downstream skill.

## Human checkpoints

- Ask a concise question only when the repository or explicitly requested
  feature cannot be identified safely.
- Treat an omitted feature as optional; resolve it from active state, current
  branch, and recent state records.
- Separate detected evidence from routing inference.
- Report corrupt, missing, blocked, or unavailable context instead of silently
  selecting a different feature.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence when both
  are supplied.
- In quick flow, use compact state, branch, installed-skill, and intent signals
  and avoid broad repository reads.
- In full flow, verify the explicit feature state, selected skill availability,
  workspace indexes, and reported blockers before recommending handoff.
- Neither mode may mutate lifecycle state or artifacts.
- When neither flag is supplied, perform deterministic default navigation.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`navigate.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-navigator/scripts/navigate.py) | Recommend the next evidence-backed AI SDLC action for a repository. | `python3 skills/ai-sdlc-navigator/scripts/navigate.py --help` | Read-only router; mutation-shaped flags are rejected and reported as blockers. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- Default Markdown guidance:

  ```bash
  python3 skills/ai-sdlc-navigator/scripts/navigate.py \
    --intent "<user request>" --format markdown
  ```

- Compact agent routing:

  ```bash
  python3 skills/ai-sdlc-navigator/scripts/navigate.py \
    --feature <feature-name> --intent "<user request>" \
    --quick-flow --format toon
  ```

- Strict feature verification:

  ```bash
  python3 skills/ai-sdlc-navigator/scripts/navigate.py \
    --feature <feature-name> --full-flow --format toon
  ```

- A non-zero exit means one or more reported blockers remain; do not discard
  the report.

## Success criteria

Markdown output must contain:

```text
Detected Context:
- repository, branch, installed skills, features, selected feature, workspace,
  current stage, active skill, dirty count, flow mode

Next Required:
- skill, reason, command, expected artifact

Next Optional:
- zero or more actions with the same fields

Blockers:
- none or explicit blocker messages
```

TOON output uses schema `ai-sdlc-navigator/v1` and arrays:
`next_required[1]`, `next_optional[N]`, and `blockers[N]`.

Quality gate:

- Pass when the selected feature follows signal precedence, the required skill
  is installed, every action contains all contract fields, and blockers are
  explicit.
- Fail when the navigator silently changes an explicit feature, recommends a
  missing skill without a blocker, mutates repository state, or mixes optional
  actions with required predecessors.

## Blockers and recovery

- When refinement and implementation state exist for the same explicit feature,
  prefer implementation only when no state has an active skill.
- When multiple features have active skills, select deterministically and make
  the ambiguity visible in blockers during full flow.
- When Git is unavailable, report `not-a-git-repository` and continue with
  repository-local state.
- When state parsing fails, skip the corrupt record in quick flow and report it
  as a blocker in full flow.
- When no recommended skill is installed, retain the recommendation and add an
  installation blocker.
- Treat dirty-tree count as context, not automatic authorization to edit or
  clean files.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Lead with the detected feature and next required action.
- Always include detected context, `next_required`, `next_optional`, and
  blockers.
- For every action include exact skill name, evidence-backed reason, portable
  invocation guidance, and expected artifact.
- Return the navigation report directly in the Codex response.
- Return progress, blockers, and recommendations directly in the Codex response.
- Before the final response, emit the `ai-sdlc-handoff/v1` contract with
  `result`, `blockers`, `next_required`, and `next_optional`; every action
  includes `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or a durable navigation artifact.
- Do not imply that an optional action is a lifecycle predecessor.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - The navigator is a utility and is not a lifecycle transition.
    - Read canonical `specs-refiniment/<feature>/_ai_sdlc/state.toon` or
      `specs/<feature>/_ai_sdlc/state.toon` before broad artifacts.
    - Prefer an explicit feature, then an active skill, then a feature matching the
      current branch, then the most recently updated state.
    - When a feature has an active skill, recommend resuming it before intent-based
      routing.
    - When no skill is active, recommend the first incomplete stage in the selected
      workspace.
    - Never call `begin` or `complete` from this skill.

??? info "Artifact metadata"

    - Navigation output is ephemeral and does not carry `artifact_metadata`.
    - Navigation output does not create or update artifact `metatags`.
    - Use artifact metadata only as read-only routing evidence when a downstream
      decision needs artifact status, flow mode, owner, or trace IDs.
    - Do not treat metadata as a replacement for state or visible artifact content.

??? info "Specs index"

    - Inspect `specs-refiniment/_ai_sdlc/specs-index.toon` and
      `specs/_ai_sdlc/specs-index.toon` before broad feature searches when they
      exist.
    - Use `specs-refiniment/specs-index.md` and `specs/specs-index.md` only when a
      human-readable inventory is needed.
    - Use feature-local `state.toon` as lifecycle authority.
    - Report a stale or missing index as a blocker only when it prevents safe
      feature selection in full flow.
    - Do not rebuild indexes from this skill.

## Example

Valid resume request:

```text
User: What should I do next for 101-payment-retry?
Navigator: ai-sdlc-validation is required because branching is complete and
validation is the first incomplete implementation stage.
```

Valid empty-project request:

```text
User: I have a product idea. Where do I start?
Navigator: ai-sdlc-working-backwards-discovery is required because no active
feature state or established codebase signal exists.
```

Invalid counter-example:

```text
The requested feature was not found, so I selected another recent feature.
```

Reject this because explicit feature identity is authoritative.

## Source contract

This page is generated from [`skills/ai-sdlc-navigator/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-navigator/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
