# Token-Saving Scripts

Scripts exist to reduce repeated LLM work. The AI assistant delegates local,
deterministic analysis, scaffolding, validation, and indexing to scripts so it
spends tokens on judgment rather than file scanning and reformatting.

Token saving is a consequence of determinism, not the only quality goal. A
smaller output that omits a blocker, source, or trace ID is worse than a larger
pack with targeted follow-up reads.

## What Scripts Should Do

A useful skill script takes over work that is:

- repetitive;
- deterministic;
- easy to validate locally;
- expensive for an LLM to repeat;
- sensitive to consistency across skills.

Examples:

- project long input artifacts into compact evidence signals;
- extract trace IDs and open markers;
- check required Markdown sections;
- generate canonical artifact templates;
- write `decision-log.md`;
- update `state.toon`;
- update `specs-index.toon` and `specs-index.md`;
- validate SDD packages;
- validate commit message metadata.

## Flow Awareness

Scripts honor the same flow mode used by the skill:

- `--quick-flow` should compress aggressively, avoid clarification loops, and
  prefer documented assumptions for non-blocking gaps;
- `--full-flow` should preserve more evidence, report blockers, and require
  stronger traceability or validation signals.

If both flags are present, full flow wins.

Default flow uses the full 24,000-token context budget and self-contained
artifact shape, while treating depth heuristics as warnings. See
[Context And Quality Gates](context-and-quality.md) for the exact gate matrix.

## AI Reading Behavior

Before the AI reads large artifacts directly, it checks whether the relevant
skill has a script that can compress or validate the inputs. If a script exists,
the AI runs it with the active flow flag and reads the compact output first.

Profile scripts keep Markdown as the human-readable default. For agent work,
the skill invokes `--format toon` to emit an `ai-sdlc-context/v2` evidence
index rather than a generated summary: every anchor carries an
exact source path, Markdown section, and line number. The AI reads `anchors`
first and opens only the `next_reads` ranges needed for details that did not fit
the active budget.

Default approximate budgets are 4,000 tokens for quick flow and 24,000 for
default or full flow. Finalized artifacts are also capped at 24,000. Override them with
`--budget-tokens`; omit `--format toon` when a person needs the Markdown report.

The AI uses script output to identify:

- required sections that are present or missing;
- trace IDs;
- open markers;
- keyword signals;
- next actions;
- artifact templates;
- decision-log rows;
- validation blockers.

### Reading A Context Pack

Use this order:

1. Confirm `feature`, `skill`, `workspace`, `flow_mode`, and budget.
2. Review `budget_status` and source status.
3. Read blocker, decision, security, validation, and trace anchors.
4. Review gaps.
5. Open every required `next_reads` range.
6. Use the complete trace-ID set while drafting and checking coverage.

Do not treat `estimated_tokens` or a cache hit as evidence that sources are
complete or current; source hashes and statuses provide that signal.

## Context Cache And Measurement

Context packs are generated on demand. `--cache-context` stores a derived pack
at `specs[-refiniment]/<feature>/_ai_sdlc/context/<skill>.toon` and reuses it
only while its source/profile fingerprint matches. `--refresh-context` forces a
rebuild. Cache files are reproducible, excluded from the specs index, and
ignored by Git.

Each non-quick skill keeps its own snapshot. `feature-context.toon` is a
skill-neutral source inventory, so one stage cannot replace another stage's
evidence contract.

Use `skills/_shared/ai_sdlc_context_benchmark.py` to compare raw source tokens,
the bounded pack, and the exact line ranges requested through `next_reads`.
Savings are informational: source-detail preservation and evidence correctness
take precedence over a fixed percentage target.

### Cache Identity

The per-skill fingerprint covers context schema, skill, flow, budget, required
sections, keywords, source paths, and source hashes. A change to any of them
invalidates the cache. The feature manifest uses a skill-neutral fingerprint of
the sorted source inventory so it remains deterministic across stages.

## AI Production Behavior

The AI does not create a temporary content file or write the routed Markdown
artifact itself. It sends only one section body to the scaffold script on stdin:

```bash
python3 <skill-script> --feature <feature> --section "<canonical-section>" --quick-flow
```

The script owns:

- routed artifact initialization and section placement;
- `artifact_metadata`;
- `decision-log.md` when absent;
- atomic durable writes.

After all required sections are supplied, the AI runs the same script with
`--finalize`. Finalization checks completeness, refreshes metadata and workspace
indexes, and leaves the artifact ready for the skill's validation gates. On
success, stdout ends with a short human-readable `Summary:` line covering the
artifact, feature, flow, completed section count, trace-ID count, and index
refresh.

Finalization reads the current skill snapshot when available, checks source
freshness, validates Source Coverage, updates metadata, applies requested state
changes, and rebuilds the index. The script summary reports what completed; it
does not replace the artifact body.

## Shared Contract

CLI scripts support:

- `--help`;
- `--quick-flow`;
- `--full-flow`;
- `--section` with content on stdin;
- `--finalize`;
- `--decision-row` with one decision table row on stdin;
- state flags when they operate on a lifecycle skill;
- metadata flags when they create or update generated artifacts.

Skill-specific scripts are tested by both per-skill tests and the shared
repository test suite.

Shared state, index, and migration CLIs are infrastructure commands and do not
pretend to expose lifecycle flags that have no meaning for them. Repository
contract tests explicitly distinguish those commands from skill wrappers.

## Script Exit Semantics

Scripts use non-zero exits for actionable failure:

- invalid CLI input or section content;
- transition/predecessor failure;
- migration conflict;
- missing or stale evidence;
- artifact quality failure;
- incomplete package/readiness gate.

Warnings remain visible on stdout/stderr but do not fail default flow when the
tiered quality policy classifies them as heuristic. Agents must report the
warning as residual risk rather than hiding it.

## What Scripts Should Not Do

Scripts do not hide judgment from the human or agent. They do not invent
requirements, approve decisions, or silently skip blockers. They produce compact
evidence and deterministic outputs that the skill can review.

## AI Failure Modes

The AI must not:

- manually retype large scaffold structures when the script can emit them;
- create temporary section files or directly edit a script-owned artifact;
- ignore script warnings in full flow;
- pass `--quick-flow` to the script while behaving as full flow in the response;
- treat script output as human approval;
- modify script behavior without adding or updating tests.
