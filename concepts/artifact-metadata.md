# Artifact Metadata And Metatags

Generated AI SDLC artifacts carry their own routing and traceability index. The
AI assistant produces this index as YAML frontmatter at the top of each Markdown
artifact so future agents can filter, validate, and connect artifacts without
rereading every body section.

## Required Frontmatter

The AI places this block before the first visible heading:

```yaml
---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "<feature-name>"
  artifact: "<file.md>"
  path: "specs-refiniment/<feature-name>/<file.md>"
  workspace: "refinement"
  skill: "<skill-name>"
  flow_mode: "quick"
  state_file: "specs-refiniment/<feature-name>/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/<feature-name>/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "YYYY-MM-DD"
  updated_at: "YYYY-MM-DD"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "<skill-name>"
    - "<artifact-type>"
    - "draft"
---
```

## Field Rules

- `schema` must remain `ai-sdlc-artifact-metadata/v1` until the repository
  intentionally introduces a new schema.
- `feature`, `artifact`, and `path` must match the physical artifact location.
- `workspace` must be `refinement` for `specs-refiniment/` artifacts and
  `implementation` for `specs/` artifacts.
- `skill` must identify the skill that generated or last materially updated the
  artifact.
- `flow_mode` must match the active skill mode: `quick`, `full`, or `default`.
- `state_file` and `decision_log` must point to the feature-local lifecycle and
  decision files.
- `status` should use a lifecycle value such as `draft`, `review`, `approved`,
  `validated`, `blocked`, or `superseded`.
- `trace_ids` should contain requirement, acceptance, test, task, risk, or
  decision IDs that the artifact materially depends on.
- `related_artifacts` should contain local artifact paths that must be read with
  this artifact to understand the change.
- `validation` should contain short validation commands, evidence IDs, or links
  that prove the artifact has been checked.
- `metatags` should stay compact and retrieval-oriented.

## AI Reading Behavior

When the AI opens an artifact, it reads the metadata first and uses it to decide:

- whether the artifact belongs to the current feature;
- whether the artifact belongs to refinement or implementation;
- which skill created or last materially updated it;
- whether the artifact was produced in quick flow or full flow;
- whether the status is draft, review, approved, validated, blocked, or
  superseded;
- which trace IDs and related artifacts must be considered;
- which validation evidence already exists.

The AI should not spend tokens reading the full body until the metadata proves
the artifact is relevant to the task.

## AI Production Behavior

When the AI creates an artifact, it produces metadata with:

- current feature slug;
- exact artifact filename and path;
- workspace;
- producing skill;
- active flow mode;
- state and decision-log paths;
- lifecycle status;
- owner when known;
- creation and update dates;
- trace IDs when known;
- related artifacts when they are needed to understand the output;
- validation evidence when available;
- compact metatags for retrieval.

When the AI materially updates an artifact, it updates `updated_at`, status,
trace IDs, related artifacts, validation, and metatags as needed.

## Flow Behavior

In `--quick-flow`, metadata is filled from available context without a
clarification loop. The AI keeps `status: "draft"` unless the source evidence
already supports a stronger status. It adds risk or assumption tags only when
they will help future retrieval.

In `--full-flow`, metadata is verified before handoff. Missing owner,
trace IDs, related artifacts, validation evidence, or unresolved decisions should
be reflected in `status`, `trace_ids`, `validation`, and the artifact body.

## Update Triggers

Update the frontmatter whenever any of these change:

- artifact path, filename, workspace, or feature slug;
- generating or owning skill;
- flow mode used for the current material update;
- owner, lifecycle status, or approval state;
- decision-log references or state-machine references;
- trace IDs, related artifacts, or validation evidence;
- metatags needed for retrieval.

Metadata is an index. It does not replace the artifact content, the decision
log, or the feature `state.toon`.

## AI Failure Modes

The AI must not:

- generate Markdown artifacts without metadata frontmatter;
- leave metadata pointing to the wrong feature, workspace, state file, or
  decision log;
- claim an artifact is approved or validated without evidence;
- hide blockers only in metadata without also explaining them in the body;
- treat metatags as a replacement for trace IDs or decision records.
