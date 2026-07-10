# Skill Anatomy

Each skill is a self-contained instruction folder that an AI assistant reads to
decide when to act, what evidence to collect, which script to run, where to
write outputs, and how to preserve traceability.

A skill combines judgment and deterministic machinery. `SKILL.md` tells the
agent how to reason and when to use resources; scripts own contracts that should
not vary between agent sessions.

## Folder Shape

```text
skills/<skill-name>/
  SKILL.md
  references/
  scripts/
  tests/
```

The repository also contains `skills/_shared/`. It is not an installable
lifecycle skill. It holds cross-skill contracts such as artifact profiles,
context building, paths, migration, state, indexes, and repository-wide tests.

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

### Frontmatter And Triggering

The frontmatter contains `name` and `description`. The description is the
trigger contract: it states what the skill does and the user situations in
which it should activate. Workflow detail belongs in the body because the body
is loaded only after triggering.

Names use lowercase kebab-case and match the folder. Changing a skill name is a
lifecycle migration because state, metadata, profiles, tests, and documentation
may reference it.

### Operational Body

The body should be imperative and decision-complete for fragile actions. It
must state canonical routing, flow behavior, source requirements, script usage,
finalization, and completion criteria. Repeating generic background across
skills increases context cost; shared concepts and references hold explanations
that do not need to be loaded for every task.

## `references/`

References hold deeper domain guidance:

- templates;
- checklists;
- review frameworks;
- examples;
- anti-patterns;
- quality bars.

The AI loads only the reference files needed for the current task.

A reference is authoritative guidance for content depth, not a generated
artifact template owned by runtime. When a skill says to read its reference
before writing, the agent must use its table columns, review dimensions, and
examples in addition to the compact scaffold.

## `scripts/`

Scripts handle deterministic work that would otherwise waste prompt tokens:

- compact artifact analysis;
- scaffold generation;
- validation gates;
- readiness checks;
- format checks;
- state and index maintenance.

Scripts must be useful for the specific skill, not generic filler.

Refinement profile wrappers intentionally stay thin. Their domain keywords and
prompts are local, while canonical output names, sections, predecessors, tables,
and budgets come from the shared profile registry. This prevents 18 wrappers
from evolving incompatible lifecycle contracts.

## AI Execution Behavior

When a task triggers a skill, the AI:

1. Reads the skill card and trigger conditions.
2. Resolves the active flow mode.
3. Checks `specs-index.toon` and `state.toon` when feature context exists.
4. Runs the skill script when deterministic scaffolding, compression, validation,
   or indexing is useful.
5. Reads only the references needed for the requested output.
6. Sends each content-only section body to the script on stdin with `--section`.
7. Runs `--finalize`; the script writes the routed artifact, metadata, decision
   log, state changes requested by flags, and specs index.

The AI does not create a temporary content Markdown file and does not directly
edit an artifact owned by a scaffold script.

## AI Production Behavior

A skill output is complete only when the AI has produced the visible answer and,
when file output is requested or implied, the durable supporting records:

- routed Markdown artifact;
- artifact metadata;
- decision-log updates;
- state updates when lifecycle progress changed;
- specs-index refresh;
- validation or residual-risk note.

The visible response and durable output are different channels. Progress,
validation, blockers, and final summaries belong in the agent response.
Canonical Markdown, decisions, state, plans, and indexes belong in their routed
files. A standalone `summary.txt` is not part of the contract unless the user
explicitly requests one.

## `tests/`

Every skill directory should include `tests/test_scripts.py`.

Tests verify that skill scripts:

- compile;
- expose `--help`;
- accept the expected flow flags;
- preserve the shared script contract;
- perform the skill-specific behavior they own.

Repository-wide tests live under `skills/_shared/`.

### Validation Layers

| Layer | What it catches |
| --- | --- |
| Skill quick validation | Invalid frontmatter, name, or required skill shape |
| Per-skill tests | Local script behavior and flags |
| Shared contract tests | Cross-skill CLI, routing, context, budget, and docs drift |
| Migration/E2E tests | Legacy conflicts and strict 18-stage package behavior |
| CI matrix | Runtime differences across supported Python versions |

A change to a shared helper requires repository-wide tests even if one local
skill test passes. A change to a skill reference may need forward validation of
artifact quality even when no Python code changed.

## Contract Evolution

When changing an established skill:

1. Identify whether the change is local guidance or a shared lifecycle contract.
2. Update the shared source of truth before wrappers or prose.
3. Preserve read compatibility when existing feature packages would otherwise
   break.
4. Add migration behavior for renamed durable files.
5. Update concept/skill documentation and contract tests together.
6. Validate every affected skill folder and run the full shared suite.

Do not fix contract drift by copying a new rule into every skill while leaving
the runtime unchanged.

## AI Failure Modes

The AI must not:

- treat `SKILL.md` as a generic essay and ignore script/reference instructions;
- load all references by default;
- create artifacts outside the routing rules;
- skip tests for new or changed scripts;
- update a skill script without keeping the per-skill and shared tests aligned.
