# Feature State Machine

The feature state machine prevents agents from violating the skill chain for a
single feature. The AI assistant reads `state.toon` before durable work,
checks whether the requested skill can run, marks the skill in progress, and
marks it complete only after the required artifact or review exists.

## State Files

- Refinement: `specs-refiniment/<feature-name>/state.toon`
- Implementation: `specs/<feature-name>/state.toon`

Implementation state may reference upstream refinement state through
`upstream_state`.

## AI Reading Behavior

Before the AI selects or starts a lifecycle skill, it reads:

- the relevant workspace `specs-index.toon`;
- the feature `state.toon`;
- the candidate skill's predecessor status;
- any active skill already marked `in_progress`;
- decision references attached to completed or skipped stages.

The state file lets the AI understand the feature chain without reopening every
artifact.

## TOON Contract

The state file uses the repository TOON subset:

```toon
feature: <feature-name>
workspace: refinement
current_stage: discovery
active_skill:
flow_mode: default
updated_at: YYYY-MM-DD
decision_log: specs-refiniment/<feature-name>/decision-log.md

stages[1]{id,skill,status,workspace,artifacts,decision_ref}:
  discovery,ai-sdlc-working-backwards-discovery,not_started,refinement,discovery.md,

skips[0]{stage,reason,decision_ref,flow_mode}:
```

Allowed statuses:

- `not_started`
- `in_progress`
- `blocked`
- `done`
- `skipped`
- `not_applicable`

## Enforcement Rules

- Only one lifecycle skill may be `in_progress` for a feature.
- A skill may start only when its predecessor stages are `done`, `skipped`, or
  `not_applicable`.
- In `--full-flow`, incomplete predecessors block.
- In `--quick-flow`, incomplete predecessors may be skipped only with
  `--assumption` or `--decision-ref`.
- Skips must be represented in both `state.toon` and `decision-log.md`.

## AI Production Behavior

When the AI starts durable work, it produces or updates:

- `state.toon` with `active_skill`, `current_stage`, `flow_mode`, and
  `updated_at`;
- a warning or blocker message when predecessors are incomplete;
- a skip record when quick flow proceeds with an accepted assumption or
  decision reference.

When the AI finishes a lifecycle step, it updates:

- the stage status to `done`;
- the stage artifact path;
- `decision_ref` when a decision shaped the work;
- `active_skill` back to empty;
- `updated_at`;
- the workspace specs index.

## CLI Commands

```bash
python3 skills/_shared/state_machine.py init --feature <feature> --workspace refinement --entrypoint discovery
python3 skills/_shared/state_machine.py check --feature <feature> --workspace refinement --skill ai-sdlc-working-backwards-discovery --full-flow
python3 skills/_shared/state_machine.py begin --feature <feature> --workspace refinement --skill ai-sdlc-working-backwards-discovery
python3 skills/_shared/state_machine.py complete --feature <feature> --workspace refinement --skill ai-sdlc-working-backwards-discovery --artifacts specs-refiniment/<feature>/discovery.md --decision-ref DEC-001
python3 skills/_shared/state_machine.py status --feature <feature> --workspace refinement --format toon
```

## Agent Execution Pattern

Before choosing a next skill, the AI follows this pattern:

1. Print or inspect `state.toon`.
2. Run `check` for the candidate skill.
3. If valid, run or recommend `begin`.
4. Produce the skill artifact.
5. Run or recommend `complete` with artifact and decision trace.

Utility skills such as approvals do not advance the lifecycle unless a caller
explicitly asks for state side effects.

## AI Failure Modes

The AI must not:

- run a downstream lifecycle skill in full flow when predecessors are incomplete;
- ignore another active lifecycle skill;
- mark a stage done before its artifact or review exists;
- skip a predecessor in quick flow without `--assumption` or `--decision-ref`;
- update the state file for unrelated feature folders.
