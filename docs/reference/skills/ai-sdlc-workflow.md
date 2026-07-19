---
title: Workflow
description: Human-facing operating guide for ai-sdlc-workflow, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-workflow`

AI SDLC declarative workflow planning. Use when an AI assistant needs to validate a versioned workflow, plan typed dependency steps, evaluate bounded conditions, enforce approval gates, attach deterministic hooks, detect cycles, or create safe dependency waves with sequential fallback when host concurrency or isolation is unavailable. Supports `--quick-flow` and `--full-flow`.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Controlled execution planning | Delivery, Dev | QA, Security, Architecture | `core` | `_ai_sdlc/workflows/<workflow-id>/plan.{toon,json,md}` |

## Why it exists

Compile portable workflow intent into deterministic, gated, host-safe waves.

## Use it when

AI SDLC declarative workflow planning. Use when an AI assistant needs to validate a versioned workflow, plan typed dependency steps, evaluate bounded conditions, enforce approval gates, attach deterministic hooks, detect cycles, or create safe dependency waves with sequential fallback when host concurrency or isolation is unavailable. Supports `--quick-flow` and `--full-flow`.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it for a one-off task with no reusable or declared DAG. Use the normal owning skill instead.
- Do not use it to execute an accepted plan. Use `ai-sdlc-runtime` instead.


## Who is involved

- **Accountable/primary:** Delivery, Dev.
- **Supporting:** QA, Security, Architecture.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Versioned workflow JSON, declared capabilities, typed steps, dependencies,
  bounded conditions, approval gates, and deterministic hook declarations.
- Optional JSON context and explicit host concurrency/isolation capabilities.

## Tell your agent

```text
Use ai-sdlc-workflow for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `_ai_sdlc/workflows/<workflow-id>/plan.{toon,json,md}`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Exact workflow identity and version.
- Declared capability set and typed steps.
- Optional bounded condition context.
- Explicit host concurrency and isolation support.

## What it may write

- Write generated plans only below `_ai_sdlc/workflows/<workflow-id>/`.
- Keep authored workflow definitions in visible repository-owned paths.
- Never execute or rewrite the authored workflow during planning.

## Human checkpoints

- Ask when an action, approval owner, or required capability is missing.
- Reject unknown fields, undeclared capabilities, cycles, unsafe identifiers,
  invalid conditions, and hooks without exact targets.
- Never infer approval, shell authority, network authority, or safe isolation.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use identical validation, cycle, capability, and fallback rules.
- Full flow requires review of every skipped/deferred condition, gate, hook, and fallback.

## Deterministic helpers

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`workflow.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-workflow/scripts/workflow.py) | Validate and plan declarative, gated, host-safe delivery workflows. | `python3 skills/ai-sdlc-workflow/scripts/workflow.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.json --validate --format toon
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.json --plan --context context.json --concurrency 4 --isolation-supported --write
```

## Success criteria

The plan records every step as eligible, skipped, or deferred; selected waves;
approval gates; hooks; fallback reason codes; source and plan fingerprints; and
explicit host capabilities.

Quality gate:

- Pass when the workflow is acyclic, capabilities are declared, conditions are
  bounded, hook targets resolve, and every planned parallel step is isolated.
- Fail closed on invalid workflow structure or ambiguous authority.

## Blockers and recovery

- Ask when an action, approval owner, or required capability is missing.
- Reject unknown fields, undeclared capabilities, cycles, unsafe identifiers,
  invalid conditions, and hooks without exact targets.
- Never infer approval, shell authority, network authority, or safe isolation.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Default to complete TOON with workflow fingerprint, step decisions, waves,
  gates, hooks, fallbacks, host capabilities, and plan fingerprint.
- Return validation and handoff summaries directly in the Codex response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read the owning feature `_ai_sdlc/state.toon` before planning feature work.
    - Workflow plans do not advance feature state or runtime task state.

??? info "Artifact metadata"

    - Machine records use `ai-sdlc-workflow/v1` and `ai-sdlc-workflow-plan/v1`.
    - Workflow-related Markdown uses canonical `artifact_metadata` and `metatags`
      when authored.

??? info "Specs index"

    - Read `_ai_sdlc/specs-index.toon` before resolving feature-local actions and
      use `specs-index.md` for human review.
    - Planning does not refresh either specs index.

## Example

```bash
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.json --validate --format toon
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.json --plan --context context.json --concurrency 4 --isolation-supported --write
```

## Source contract

This page is generated from [`skills/ai-sdlc-workflow/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-workflow/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
