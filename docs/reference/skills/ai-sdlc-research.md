---
title: Research
description: Human-facing operating guide for ai-sdlc-research, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-research`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Discovery, refinement, and design evidence | Research, PM, BA, Architecture | Dev, QA, Security, Delivery | `research` | `research.md` and `_ai_sdlc/research.toon` |

## Why it exists

Preserve questions, sources, findings, confidence, and limitations.

## Use it when

Optional AI SDLC research workflow. Use when an AI assistant needs to investigate a customer, market, domain, technology, regulation, competitor, operational question, or implementation uncertainty and produce a routed source inventory plus synthesized findings with confidence, limitations, open questions, and delivery trace targets. Supports `--quick-flow` for focused evidence and `--full-flow` for multi-source and source-diversity gates.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use external research for facts already authoritative in the repository. Use `ai-sdlc-project-context` instead.
- Do not use research to accept a product, legal, security, or delivery decision. Route evidence to the accountable owner or `ai-sdlc-change-impact` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Owning feature root.
- Research input using `ai-sdlc-research-input/v1`.
- Verifiable source locators and delivery trace targets.
- Internet access through the host web or browser tool for external or current questions.

## Tell your agent

```text
Use ai-sdlc-research for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `research.md` and `_ai_sdlc/research.toon`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

### Required reads

- `<feature-root>/_ai_sdlc/state.toon` before any durable write.
- The matching `specs/_ai_sdlc/specs-index.toon` or `specs-refiniment/_ai_sdlc/specs-index.toon` before broad repository reads.
- `/tmp/research.json`, or another explicitly supplied input file, conforming to `ai-sdlc-research-input/v1`.
- Every repository evidence path and direct source locator registered by that input.

### Optional reads

- Existing requirements, decisions, or earlier research only when their IDs are named as trace targets.
- Direct web pages opened through the host web/browser tool for `external` or `mixed` scope. Search-result pages and cached model knowledge are not evidence.

### Freshness rule

For current claims, compare the source publication date with the date the event or data applies to, record ISO `accessed_at`, search for superseding primary or official material, and preserve material contradictions and freshness limitations.

The [research input contract](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-research/references/research-contract.md) defines required fields; the [web research protocol](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-research/references/web-research-protocol.md) defines direct-source and freshness behavior. JSON is used only at this validated interoperability boundary; durable repository output remains Markdown plus TOON.

## What it may write

- Write `<feature-root>/research.md`.
- Write `<feature-root>/_ai_sdlc/research.toon`.
- Keep downloaded or licensed source files outside generated output unless allowed.
- Link research to requirements and decisions; do not overwrite them.

## Human checkpoints

- Ask when topic, decision to inform, source boundary, or freshness requirement is unclear.
- Separate sourced findings from inference and unresolved questions.
- Record contradictory sources and limitations; do not average them away.
- Do not claim current facts, legal conclusions, or user evidence without verification.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits one strong source when scope is explicitly narrow.
- Full flow requires at least two sources and two source types for each report.
- External and mixed scopes require an internet search and at least one direct
  `http://` or `https://` source locator; do not cite search-result pages.
- Both modes require every finding to cite registered sources and trace targets.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`research.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-research/scripts/research.py) | Validate and route sourced research artifacts. | `python3 skills/ai-sdlc-research/scripts/research.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-research/scripts/research.py specs-refiniment/payments --input /tmp/research.json --emit --quick-flow
python3 skills/ai-sdlc-research/scripts/research.py specs/payments --input /tmp/research.json --write --full-flow --format toon
```

## Success criteria

`ai-sdlc-research/v1` contains topic, questions, sources, findings, source IDs,
confidence, limitations, trace targets, and owned open questions.

Quality gate:

- Pass when source IDs resolve, findings have confidence plus limitations, and
  delivery traces explain why the evidence matters.
- Full flow fails without two sources, two source types, or any open question owner.

## Blockers and recovery

- A source may support and contradict different findings; keep both links.
- A blocked source remains registered only if its unavailability matters.
- Time-sensitive sources include an explicit access date and freshness limitation.
- Full flow source diversity counts distinct `type` values, not duplicate URLs.
- If internet access is unavailable for external scope, report a blocker and do
  not present cached model knowledge as completed research.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return question, source, finding, confidence, blocker, and output path counts
  directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or uncited research prose.
- Keep quotes within source rights and use concise paraphrase by default.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read `<feature-root>/_ai_sdlc/state.toon` before durable research writes.
    - Research is optional and does not add a core lifecycle stage.
    - `--state-check` is read-only; `--begin-state` and `--complete-state` are rejected.
    - Accepted implications move through decisions, requirements, SDD, or change impact.

??? info "Artifact metadata"

    - Markdown starts with `artifact_metadata` using schema `ai-sdlc-research-metadata/v1`.
    - Include `metatags` for `ai-sdlc`, `research`, `evidence`, and `traceable`.
    - Record feature, workspace, flow mode, state file, trace IDs, and review status.

??? info "Specs index"

    - Read the relevant `specs/_ai_sdlc/specs-index.toon` or
      `specs-refiniment/_ai_sdlc/specs-index.toon` before broad reads.
    - Refresh the matching `specs/specs-index.md` or
      `specs-refiniment/specs-index.md` only after durable writes.
    - Keep research inside the feature whose decisions it informs.

## Example

Create `/tmp/research.json` with the validated input shape before running the helper:

```json
{
  "schema": "ai-sdlc-research-input/v1",
  "topic": "Current payment retry requirements",
  "scope": "external",
  "questions": [
    {"id": "Q-001", "question": "What is currently required?", "trace_targets": ["REQ-014"]}
  ],
  "sources": [
    {"id": "SRC-001", "title": "Primary guidance", "locator": "https://example.org/guidance", "type": "official-guidance", "accessed_at": "2026-07-19", "credibility": "primary", "notes": "Check for superseding guidance"}
  ],
  "findings": [
    {"id": "F-001", "statement": "The current guidance requires a bounded retry policy.", "source_ids": ["SRC-001"], "confidence": "medium", "limitations": "Jurisdiction review is still required", "trace_targets": ["REQ-014"]}
  ],
  "open_questions": [
    {"id": "OQ-001", "question": "Which jurisdictions apply?", "owner": "Legal", "next_action": "Confirm scope"}
  ]
}
```

Then run the source-contract command. External or current work must use internet research to open and verify direct pages; never replace it with model memory.

A valid finding cites `SRC-001/SRC-003`, states medium confidence, names data
freshness limitations, and traces to `DEC-022`. “Competitors all do this” is
invalid without registered sources, boundary, or confidence.

## Source contract

This page is generated from [`skills/ai-sdlc-research/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-research/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
