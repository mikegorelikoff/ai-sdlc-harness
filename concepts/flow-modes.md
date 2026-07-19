<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# Flow Modes

Every skill supports two explicit execution modes. The AI assistant reads the
requested mode, applies the matching behavior, and passes the same mode to
helper scripts so generated artifacts, state transitions, and validation
strictness stay consistent.

Flow mode is an evidence and interaction policy, not a measure of feature size.
A small security-sensitive change may need full flow, while a large exploratory
draft may intentionally start in quick flow.

## Mode Comparison

| Dimension | Quick | Default | Full |
| --- | --- | --- | --- |
| Questions | Only material-risk blockers | Skill judgment | Clarify material uncertainty |
| Source scope | Explicit/focused when provided | Whole feature package | Whole feature package plus strict follow-up reads |
| Context budget | 4,000 | 24,000 | 24,000 |
| Artifact structure | Canonical stage sections | Shared context plus stage sections | Shared context plus stage sections |
| Depth heuristics | Not applied | Warning | Blocking |
| Predecessors | May proceed with traced assumption/decision | Normal state rules | Incomplete predecessors block |
| Handoff claim | Draft/progress | Context-dependent | Verified or explicitly blocked |

## Quick Flow

`--quick-flow` means the AI prioritizes fast, high-quality progress with the
available evidence.

Behavior:

- use available context and repository evidence;
- avoid questions unless continuing creates material product, security,
  compliance, data-loss, or irreversible implementation risk;
- record assumptions and important defaults in `decision-log.md`;
- rely on `specs-index.toon` before opening broad artifact sets;
- run only focused checks that are relevant and cheap.

Quick flow is not permission to invent requirements. It is permission for the AI
to make documented, low-risk assumptions and keep moving when the missing
information does not create material risk.

## Quick Flow Outputs

In quick flow, the AI produces:

- concise artifact drafts;
- explicit assumptions in the artifact body;
- `artifact_metadata.flow_mode: "quick"`;
- decision-log rows for material assumptions;
- updated specs indexes after file writes;
- a short residual-risk note when broader checks are skipped.

## Full Flow

`--full-flow` means the AI prioritizes verification, traceability, and
confidence before final handoff.

Behavior:

- ask concise clarification questions when material inputs are missing;
- verify upstream and downstream artifacts;
- verify `decision-log.md`, `state.toon`, metadata, and specs indexes;
- treat incomplete predecessor stages as blockers;
- run or recommend the skill-appropriate validation and review gates.

## Full Flow Outputs

In full flow, the AI produces:

- artifact drafts or updates with verified sources;
- explicit blockers and open questions when material inputs are missing;
- `artifact_metadata.flow_mode: "full"`;
- updated `decision-log.md` entries for accepted assumptions or scope choices;
- updated `state.toon` when lifecycle progress changes;
- refreshed TOON and Markdown specs indexes;
- validation evidence or a clear explanation of blocked validation.

## Default Flow

When neither explicit flag is supplied, scripts record `flow_mode: "default"`.
Default uses the same 24,000-token and self-contained artifact contract as full
flow, but heuristic depth/open-marker findings remain warnings. Deterministic
structure, table, source-coverage, freshness, and size failures still block.

Default is appropriate when the user wants a durable artifact with whole-feature
context but has not asked for strict readiness or signoff.

## Precedence

If both flags are supplied, `--full-flow` wins because it is stricter.

When neither flag is supplied, the skill follows its default behavior and chooses
the least risky path for the request size and domain.

## Escalating A Flow

A quick artifact can be upgraded to default or full, but changing the metadata
flag alone is insufficient. Rerun analysis with the broader source set, complete
the shared context sections, resolve or own material gaps, and finalize through
the target gate. The refreshed metadata records the evidence level of the new
material update.

A full artifact should not be downgraded merely to bypass a blocker. If the user
changes the requested scope to a quick draft, preserve the strict artifact and
make the new limitation explicit rather than erasing validated context.

## AI Failure Modes

The AI must not:

- ask long clarification loops in quick flow for non-blocking gaps;
- silently assume material scope, security, compliance, or data-loss behavior;
- claim full-flow readiness without checking artifacts, decisions, state, and
  validation evidence;
- pass a different flow flag to helper scripts than the one used by the skill.
