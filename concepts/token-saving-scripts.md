# Token-Saving Scripts

Scripts exist to reduce repeated LLM work. The AI assistant delegates local,
deterministic analysis, scaffolding, validation, and indexing to scripts so it
spends tokens on judgment rather than file scanning and reformatting.

## What Scripts Should Do

A useful skill script takes over work that is:

- repetitive;
- deterministic;
- easy to validate locally;
- expensive for an LLM to repeat;
- sensitive to consistency across skills.

Examples:

- summarize long input artifacts into compact signals;
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

## AI Reading Behavior

Before the AI reads large artifacts directly, it checks whether the relevant
skill has a script that can compress or validate the inputs. If a script exists,
the AI runs it with the active flow flag and reads the compact output first.

The AI uses script output to identify:

- required sections that are present or missing;
- trace IDs;
- open markers;
- keyword signals;
- next actions;
- artifact templates;
- decision-log rows;
- validation blockers.

## AI Production Behavior

When the AI uses a scaffold script with `--write`, the script produces:

- the routed artifact skeleton;
- `artifact_metadata`;
- `decision-log.md` when absent;
- refreshed workspace specs indexes.

The AI then fills or updates the generated artifact body and reports any
residual risk or blocked validation.

## Shared Contract

CLI scripts support:

- `--help`;
- `--quick-flow`;
- `--full-flow`;
- state flags when they operate on a lifecycle skill;
- metadata flags when they create or update generated artifacts.

Skill-specific scripts are tested by both per-skill tests and the shared
repository test suite.

## What Scripts Should Not Do

Scripts do not hide judgment from the human or agent. They do not invent
requirements, approve decisions, or silently skip blockers. They produce compact
evidence and deterministic outputs that the skill can review.

## AI Failure Modes

The AI must not:

- manually retype large scaffold structures when the script can emit them;
- ignore script warnings in full flow;
- pass `--quick-flow` to the script while behaving as full flow in the response;
- treat script output as human approval;
- modify script behavior without adding or updating tests.
