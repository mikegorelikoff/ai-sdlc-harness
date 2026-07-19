---
title: Architecture
description: Human-facing operating guide for ai-sdlc-architecture, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-architecture`

Optional AI SDLC architecture workflow. Use when an AI assistant needs to define system boundaries, components, interfaces, architectural constraints, alternatives, decisions, tradeoffs, risks, or validation for a feature and produce routed human and machine artifacts linked to requirements and durable decisions. Supports `--quick-flow` for focused design and `--full-flow` for strict decision, risk, and validation coverage.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Design and implementation planning | Architecture, Dev | QA, Security, Delivery, BA | `architecture` | `architecture.md` and `_ai_sdlc/architecture.toon` |

## Why it exists

Preserve traceable architecture boundaries, decisions, and risks.

## Use it when

Optional AI SDLC architecture workflow. Use when an AI assistant needs to define system boundaries, components, interfaces, architectural constraints, alternatives, decisions, tradeoffs, risks, or validation for a feature and produce routed human and machine artifacts linked to requirements and durable decisions. Supports `--quick-flow` for focused design and `--full-flow` for strict decision, risk, and validation coverage.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it while business behavior or customer value is still unclear. Use `ai-sdlc-ba` or the appropriate refinement workflow instead.


## Who is involved

- **Accountable/primary:** Architecture, Dev.
- **Supporting:** QA, Security, Delivery, BA.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Implementation feature root.
- Architecture input using `ai-sdlc-architecture-input/v1`.
- Requirement, acceptance, risk, or decision trace targets.

## Tell your agent

```text
Use ai-sdlc-architecture for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `architecture.md` and `_ai_sdlc/architecture.toon`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Capture design context and constraints before components.
- Trace interfaces and decisions to durable requirement or decision IDs.
- Give risks an owner and mitigation.
- Provide executable or inspectable validation evidence.

## What it may write

- Write `<feature-root>/architecture.md`.
- Write `<feature-root>/_ai_sdlc/architecture.toon`.
- Keep ADRs or decision-log entries separate when organizational authority
  requires them; link their IDs from architecture decisions.
- Do not write into refinement unless architecture work is explicitly upstream.

## Human checkpoints

- Ask when system boundary, quality attribute, authority, or irreversible choice is ambiguous.
- Separate constraints from decisions and decisions from implementation tasks.
- Record alternatives and consequences for every material decision.
- Do not invent infrastructure, data classification, or production topology.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits a bounded architecture slice with explicit gaps.
- Full flow requires at least one decision, risk, and validation check.
- Both modes require trace targets for constraints, interfaces, decisions, and risks.

## Deterministic helpers

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`architecture.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-architecture/scripts/architecture.py) | Validate and route traceable architecture artifacts. | `python3 skills/ai-sdlc-architecture/scripts/architecture.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-architecture/scripts/architecture.py specs/payments --input /tmp/architecture.json --emit --quick-flow
python3 skills/ai-sdlc-architecture/scripts/architecture.py specs/payments --input /tmp/architecture.json --write --full-flow --format toon
```

## Success criteria

`ai-sdlc-architecture/v1` contains context, constraints, components, interfaces,
decisions, risks, and validation checks with trace targets and owners.

Quality gate:

- Pass when boundaries are explicit and every material claim has traceability.
- Full flow fails without decisions, risks, validation, alternatives, consequences,
  risk ownership, or mitigation.

## Blockers and recovery

- A local reversible patch may use quick flow and record no new decision.
- External systems remain components with explicit unverified interface assumptions.
- Existing ADRs are referenced, not duplicated.
- Diagram generation is optional; structured contracts remain authoritative.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return design scope, decision/risk counts, blockers, validation status, and
  output paths directly in the Codex response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or untraced diagrams.
- Keep Markdown authoritative for detail and TOON bounded for routing.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read `<feature-root>/_ai_sdlc/state.toon` before architecture work.
    - Architecture is an optional design utility and does not add a core lifecycle stage.
    - `--state-check` is read-only; `--begin-state` and `--complete-state` are rejected.
    - Route accepted design changes back through SDD and change-impact recovery.

??? info "Artifact metadata"

    - Markdown starts with `artifact_metadata` using schema
      `ai-sdlc-architecture-metadata/v1`.
    - Include `metatags` for `ai-sdlc`, `architecture`, `design`, and `traceable`.
    - Record feature, workspace, flow mode, state file, trace IDs, and status.

??? info "Specs index"

    - Read `specs/_ai_sdlc/specs-index.toon` and feature state before broad reads.
    - Refresh `specs/specs-index.md` only after a durable architecture write.
    - Do not alter `specs-refiniment/_ai_sdlc/specs-index.toon` or
      `specs-refiniment/specs-index.md` for implementation-owned architecture.

## Example

A valid decision records `DEC-021`, its requirement traces, selected option,
rationale, alternatives, and operational consequences. “Use microservices
because they scale” is invalid without evidence, boundary, alternatives, or tradeoff.

## Source contract

This page is generated from [`skills/ai-sdlc-architecture/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-architecture/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
