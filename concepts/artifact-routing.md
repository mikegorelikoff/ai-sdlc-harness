# Artifact Routing

Artifact routing keeps refinement work separate from implementation work. The
AI assistant uses routing before writing any durable Markdown artifact so PM,
BA, QA, Delivery, and Dev outputs do not collapse into one folder.

## Workspaces

The AI writes PM, BA, QA, Delivery, discovery, planning,
refinement, readiness, and handoff artifacts.

```text
specs-refiniment/
  <feature-name>/
    decision-log.md
    state.toon
    discovery-notes.md
    prfaq.md
    business-context.md
    backlog.md
    user-stories.md
    delivery-spec.md
    qa-strategy.md
    test-cases.md
    qa-readiness.md
```

The AI writes `specs/` only for developer implementation SDD packages and repo-governance
artifacts.

```text
specs/
  <feature-name>/
    decision-log.md
    state.toon
    requirements.md
    design.md
    test-cases.md
    qa.md
    tasks.md
    plan.toon
    plan.md
    validation.md
    code-review.md
```

## Rules

- PM, BA, QA, Delivery, discovery, planning, and readiness artifacts go to
  `specs-refiniment/<feature-name>/<file.md>`.
- Developer implementation SDD artifacts go to
  `specs/<feature-name>/<file.md>`.
- Decision logs live beside the feature artifacts in the same workspace.
- `specs-refiniment/` is upstream context for `specs/`.
- Do not move refinement artifacts into `specs/` only because developers need
  to read them.
- Convert refinement context into implementation SDD only when implementation
  work is explicitly in scope.

## AI Reading Behavior

Before opening many files, the AI first reads the workspace index:

- `specs-refiniment/specs-index.toon` for refinement context;
- `specs/specs-index.toon` for implementation context.

The AI then opens only the feature artifacts that match the active task,
metadata tags, current stage, or trace IDs. Broad recursive reads are a fallback,
not the default path.

## AI Production Behavior

When the AI creates a refinement artifact, it produces:

- the routed Markdown artifact under `specs-refiniment/<feature-name>/`;
- `artifact_metadata` frontmatter at the top of the artifact;
- a decision-log entry when a decision or assumption is involved;
- a refreshed `specs-refiniment/specs-index.toon` and `specs-index.md`.

When the AI creates an implementation artifact, it produces the same supporting
records under `specs/<feature-name>/`. For implementation SDD packages, the AI
also maintains `plan.toon` as the compact task/status/link graph and `plan.md`
as the readable execution plan generated from those links.

## AI Failure Modes

The AI must not:

- write QA/BA/PM refinement material into `specs/`;
- write implementation SDD material into `specs-refiniment/`;
- create a new feature folder with a different slug for the same feature;
- skip metadata, decision-log, state, or index updates when durable artifacts
  change.

## Naming

The AI produces lowercase kebab-case feature folders and files.

```text
specs-refiniment/payment-retry-policy/business-context.md
specs/payment-retry-policy/requirements.md
```

When the feature name is unknown, use a temporary slug such as
`tbd-payment-retry`.
