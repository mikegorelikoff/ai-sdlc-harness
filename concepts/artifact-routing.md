<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# Artifact Routing

Artifact routing keeps refinement work separate from implementation work. The
AI assistant uses routing before writing any durable Markdown artifact so PM,
BA, QA, Delivery, and Dev outputs do not collapse into one folder.

Routing answers three different questions:

- **ownership:** which lifecycle group is responsible for the artifact;
- **authority:** whether the artifact defines upstream intent or implementation;
- **discovery:** where future agents and indexes will look for it.

See [System Model](system-model.md) for the complete authority hierarchy and
[Migration And Concurrency](migration-and-concurrency.md) for canonical/legacy
path behavior.

## Workspaces

The AI writes PM, BA, QA, Delivery, discovery, planning,
refinement, readiness, and handoff artifacts.

```text
specs-refiniment/
  <feature-name>/
    decision-log.md
    _ai_sdlc/state.toon
    discovery.md
    prfaq.md
    business-context.md
    backlog.md
    user-stories.md
    delivery-spec.md
    qa-strategy.md
    test-cases.md
    qa-readiness.md
    delivery-handoff-review.md
```

The full refinement workspace has 18 canonical lifecycle outputs. The tree
shows representative files; [Refinement Lifecycle](refinement-lifecycle.md)
contains the complete inventory and predecessor graph.

The AI writes `specs/` only for developer implementation SDD packages and repo-governance
artifacts.

```text
specs/
  <feature-name>/
    decision-log.md
    _ai_sdlc/state.toon
    requirements.md
    design.md
    test-cases.md
    qa.md
    tasks.md
    _ai_sdlc/plan.toon
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

## Routing Decision

Use this decision order before creating a file:

1. If the output defines customer value, scope, actors, business rules,
   readiness, QA design, or delivery handoff, route it to refinement.
2. If the output defines repository-specific requirements, architecture,
   implementation tasks, execution planning, validation, or review, route it
   to implementation.
3. If implementation consumes an upstream fact, link the refinement artifact;
   do not copy it into `specs/` as a second source of truth.
4. If the output is a machine projection, place it under the matching
   `_ai_sdlc` boundary.
5. If the feature slug is ambiguous, inspect indexes and existing folders
   before creating a temporary slug.

### Common Boundary Cases

| Output | Workspace | Reason |
| --- | --- | --- |
| Product acceptance behavior | Refinement | Defines intended observable value |
| QA test strategy and readiness | Refinement | Validates delivery intent before implementation |
| Repository-specific test implementation plan | Implementation | Defines how this codebase will prove behavior |
| Architecture tradeoff caused by code constraints | Implementation, with refinement decision link when scope changes | Repository design is implementation-owned; product impact remains upstream |
| Rollout business rule | Refinement | Changes customer/delivery behavior |
| Deployment command and rollback procedure | Implementation | Repository/environment execution detail |

## AI Reading Behavior

Before opening many files, the AI first reads the workspace index:

- `specs-refiniment/_ai_sdlc/specs-index.toon` for refinement context;
- `specs/_ai_sdlc/specs-index.toon` for implementation context.

The AI then opens only the feature artifacts that match the active task,
metadata tags, current stage, or trace IDs. Broad recursive reads are a fallback,
not the default path.

For implementation work, the agent may read both indexes: implementation first
for active SDD state, then refinement for upstream delivery spec, QA readiness,
and decisions. Reading both does not merge their ownership boundaries.

## AI Production Behavior

When the AI creates a refinement artifact, it produces:

- the routed Markdown artifact under `specs-refiniment/<feature-name>/`;
- `artifact_metadata` frontmatter at the top of the artifact;
- a decision-log entry when a decision or assumption is involved;
- a refreshed `specs-refiniment/_ai_sdlc/specs-index.toon` and `specs-index.md`.

When the AI creates an implementation artifact, it produces the same supporting
records under `specs/<feature-name>/`. For implementation SDD packages, the AI
also maintains `_ai_sdlc/plan.toon` as the compact task/status/link graph and `plan.md`
as the readable execution plan generated from those links.

All machine-readable TOON files live under `_ai_sdlc`. Context snapshots and
`feature-context.toon` are derived; state, plans, and indexes are durable.
Writers migrate legacy files only when the canonical path is absent or the
content is identical. Divergent copies are blocking conflicts.

## AI Failure Modes

The AI must not:

- write QA/BA/PM refinement material into `specs/`;
- write implementation SDD material into `specs-refiniment/`;
- create a new feature folder with a different slug for the same feature;
- skip metadata, decision-log, state, or index updates when durable artifacts
  change.

Additional warning signs include two feature slugs with overlapping trace IDs,
the same canonical filename in both workspaces without distinct ownership, and
visible TOON files outside `_ai_sdlc`. Resolve routing before continuing rather
than teaching indexes to tolerate ambiguity.

## Naming

The AI produces lowercase kebab-case feature folders and files.

```text
specs-refiniment/payment-retry-policy/business-context.md
specs/payment-retry-policy/requirements.md
```

When the feature name is unknown, use a temporary slug such as
`tbd-payment-retry`.

Once the stable slug is known, migrate the whole feature boundary together:
artifact paths, metadata, state and decision references, related-artifact links,
and indexes. Renaming only the folder leaves internally valid-looking but stale
references.
