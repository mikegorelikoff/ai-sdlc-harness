# Skill Anatomy

Each skill is a self-contained instruction folder that an AI assistant reads to
decide when to act, what evidence to collect, which script to run, where to
write outputs, and how to preserve traceability.

## Folder Shape

```text
skills/<skill-name>/
  SKILL.md
  references/
  scripts/
  tests/
```

## `SKILL.md`

`SKILL.md` is the AI entry point. It describes:

- when to use the skill;
- required inputs;
- clarification behavior;
- `--quick-flow` and `--full-flow` behavior;
- artifact routing;
- decision-log requirements;
- feature state-machine usage;
- artifact metadata requirements;
- specs-index usage;
- script usage and references.

`SKILL.md` stays operational. Long examples, checklists, and templates belong in
`references/`.

## `references/`

References hold deeper domain guidance:

- templates;
- checklists;
- review frameworks;
- examples;
- anti-patterns;
- quality bars.

The AI loads only the reference files needed for the current task.

## `scripts/`

Scripts handle deterministic work that would otherwise waste prompt tokens:

- compact artifact analysis;
- scaffold generation;
- validation gates;
- readiness checks;
- format checks;
- state and index maintenance.

Scripts must be useful for the specific skill, not generic filler.

## AI Execution Behavior

When a task triggers a skill, the AI:

1. Reads the skill card and trigger conditions.
2. Resolves the active flow mode.
3. Checks `specs-index.toon` and `state.toon` when feature context exists.
4. Runs the skill script when deterministic scaffolding, compression, validation,
   or indexing is useful.
5. Reads only the references needed for the requested output.
6. Produces or updates the routed artifact.
7. Updates metadata, decision log, state, and specs index when durable files
   change.

## AI Production Behavior

A skill output is complete only when the AI has produced the visible answer and,
when file output is requested or implied, the durable supporting records:

- routed Markdown artifact;
- artifact metadata;
- decision-log updates;
- state updates when lifecycle progress changed;
- specs-index refresh;
- validation or residual-risk note.

## `tests/`

Every skill directory should include `tests/test_scripts.py`.

Tests verify that skill scripts:

- compile;
- expose `--help`;
- accept the expected flow flags;
- preserve the shared script contract;
- perform the skill-specific behavior they own.

Repository-wide tests live under `skills/_shared/`.

## AI Failure Modes

The AI must not:

- treat `SKILL.md` as a generic essay and ignore script/reference instructions;
- load all references by default;
- create artifacts outside the routing rules;
- skip tests for new or changed scripts;
- update a skill script without keeping the per-skill and shared tests aligned.
