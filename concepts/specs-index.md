# Specs Index

The specs index is a workspace-level map of feature folders and artifacts. The
AI assistant reads it before broad file search and produces it after durable
artifact writes.

It exists in two forms:

- `specs-refiniment/_ai_sdlc/specs-index.toon` and `specs/_ai_sdlc/specs-index.toon` for LLMs;
- `specs-refiniment/specs-index.md` and `specs/specs-index.md` for humans.

The TOON file is the first place the AI reads before opening individual feature
artifacts. It keeps feature state, artifact paths, lifecycle status, skills,
flow modes, trace IDs, and metadata tags in a compact form.

The Markdown file is the human-facing view of the same index. It is optimized
for review, handoff, and feature inventory.

## AI Reading Behavior

When the AI needs feature context, it reads the relevant TOON index first:

- `specs-refiniment/_ai_sdlc/specs-index.toon` for PM, BA, QA, Delivery, and refinement
  work;
- `specs/_ai_sdlc/specs-index.toon` for implementation work.

The AI uses index rows to narrow the file set by:

- feature slug;
- current lifecycle stage;
- active skill;
- artifact status;
- producing skill;
- flow mode;
- trace IDs;
- metatags.

Only after narrowing does the AI open the selected artifact bodies.

## AI Production Behavior

When the AI creates or materially updates an artifact, it refreshes the matching
workspace index. The generated TOON index includes:

- feature rows with lifecycle state and artifact counts;
- artifact rows with path, producing skill, status, flow, trace IDs, and tags;
- decision-log and state paths for direct follow-up.

The generated Markdown index includes the same information in tables for humans.

## CLI

The AI refreshes both refinement and implementation indexes with:

```bash
python3 skills/_shared/ai_sdlc_specs_index.py --workspace all --quick-flow
```

The AI refreshes one workspace with:

```bash
python3 skills/_shared/ai_sdlc_specs_index.py --workspace refinement --quick-flow
python3 skills/_shared/ai_sdlc_specs_index.py --workspace implementation --full-flow
```

`--quick-flow` is enough after routine scaffold writes. The AI uses
`--full-flow` when a handoff, readiness review, or signoff depends on proving
that the index reflects the latest artifacts.

## TOON Shape

```toon
workspace: refinement
root: specs-refiniment
updated_at: YYYY-MM-DD

features[1]{feature,workspace,current_stage,active_skill,flow_mode,updated_at,artifact_count,decision_log,state_file,metatags}:
  payment-retry-policy,refinement,qa_traceability,,full,YYYY-MM-DD,8,specs-refiniment/payment-retry-policy/decision-log.md,specs-refiniment/payment-retry-policy/_ai_sdlc/state.toon,ai-sdlc;qa-readiness;validated

artifacts[1]{feature,path,artifact,skill,status,flow_mode,updated_at,trace_ids,metatags}:
  payment-retry-policy,specs-refiniment/payment-retry-policy/qa-readiness.md,qa-readiness.md,ai-sdlc-qa-traceability-and-readiness-review,validated,full,YYYY-MM-DD,AC-001;TC-001,ai-sdlc;refinement;qa-readiness;validated
```

## AI Execution Pattern

Before broad search, the AI:

1. Open the workspace `specs-index.toon`.
2. Find the feature row by feature slug, active skill, current stage, tags, or
   artifact count.
3. Open only the artifact paths listed for that feature that match the task.
4. If the selected artifact is missing metadata or stale status, update the
   artifact and refresh the index.

After writing artifacts, the AI:

1. Update `artifact_metadata` in the written artifact.
2. Update `state.toon` if lifecycle status changed.
3. Update `decision-log.md` when a decision was made or relied on.
4. Run `ai_sdlc_specs_index.py` for the affected workspace.
5. In full flow, confirm the new artifact appears in both TOON and Markdown
   indexes.

The specs index is not a source of truth for detailed requirements. It is a
token-saving routing layer that points agents and humans to the right source
artifacts.

## AI Failure Modes

The AI must not:

- recursively read every feature artifact before checking `specs-index.toon`;
- rely on stale index rows after creating or materially changing artifacts;
- treat `specs-index.md` as the LLM-optimized source when TOON exists;
- treat the index summary as a replacement for reading selected source
  artifacts when details, approvals, or validation evidence matter.
