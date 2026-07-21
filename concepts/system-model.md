<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# System Model

The AI SDLC harness is a repository-resident coordination system for AI-assisted
delivery. It does not replace product judgment, engineering review, or source
control. It makes the state, evidence, decisions, and outputs of those activities
durable enough for another agent or person to continue the feature safely.

## Why The System Exists

Long-running feature work crosses roles and sessions. Chat history alone cannot
reliably answer which requirement is current, why a scope choice was accepted,
whether QA is ready, or which artifact should be read next. The harness solves
that continuity problem with a small set of linked, repository-local records.

The design optimizes for four outcomes:

- a new session can recover the current feature state without rereading the repo;
- human-readable Markdown remains the source of detailed delivery truth;
- machine-readable TOON makes routing and lifecycle checks inexpensive;
- deterministic scripts protect fragile writes and validation rules from drift.

## Four System Layers

| Layer | Purpose | Canonical records |
| --- | --- | --- |
| Delivery artifacts | Preserve detailed product, BA, QA, and implementation meaning | Feature Markdown files |
| Control plane | Preserve lifecycle, decisions, and execution status | `state.toon`, `decision-log.md`, `plan.toon` |
| Discovery projections | Help agents find relevant records without broad reads | `specs-index.toon`, `specs-index.md`, context packs |
| Runtime helpers | Apply routing, scaffolding, migration, locking, and gates consistently | Scripts under `skills/_shared/` and skill `scripts/` |

The layers complement one another. A specs index can point to a requirement but
cannot replace its detailed acceptance criteria. State can say a stage is done
but cannot prove the artifact is strong. Metadata can advertise validation but
cannot replace the validation output.

## Authority Hierarchy

When records disagree, use this order to determine what must be repaired:

1. The visible artifact body is authoritative for detailed requirements,
   scenarios, risks, designs, and evidence.
2. `decision-log.md` is authoritative for why a material choice was accepted,
   rejected, or superseded.
3. `state.toon` is authoritative for lifecycle transition status.
4. `tasks.md` checkboxes are authoritative for implementation completion;
   `plan.toon` and `plan.md` are derived task/link projections and must be rebuilt
   when they drift.
5. Artifact metadata is a routing and traceability index over the artifact.
6. Specs indexes and context packs are derived projections and may be rebuilt.

This hierarchy does not permit silently choosing one side of a contradiction.
If an artifact says a requirement is open while state says its stage is done,
the package is inconsistent and must be repaired before strict handoff.

## Canonical Feature Boundary

Every lifecycle record belongs to exactly one feature slug and one workspace.

```text
specs-refiniment/<feature>/      upstream product, BA, QA, and delivery package
specs/<feature>/                 implementation SDD and execution package
```

The same feature slug connects the two workspaces. Refinement is upstream
evidence for implementation; implementation does not rewrite refinement history.
A separate feature must not share state, decisions, indexes, or context snapshots.

## Canonical Feature Shape

```text
specs-refiniment/
  _ai_sdlc/specs-index.toon
  specs-index.md
  payment-retry-policy/
    discovery.md
    prfaq.md
    business-context.md
    delivery-spec.md
    qa.md
    qa-readiness.md
    delivery-handoff-review.md
    decision-log.md
    _ai_sdlc/
      state.toon
      feature-context.toon
      context/<skill>.toon

specs/
  _ai_sdlc/specs-index.toon
  specs-index.md
  payment-retry-policy/
    requirements.md
    design.md
    test-cases.md
    qa.md
    tasks.md
    plan.md
    decision-log.md
    _ai_sdlc/
      state.toon
      plan.toon
      feature-context.toon
      context/<skill>.toon
```

Not every feature needs every implementation artifact immediately. The shape
shows ownership: visible Markdown is for humans and durable delivery meaning;
machine-oriented files are grouped under `_ai_sdlc`.

## End-To-End Data Flow

For a normal durable stage, the agent and helpers follow this sequence:

1. Resolve the feature and workspace from the request and existing indexes.
2. Read the workspace TOON index, feature state, and relevant decision records.
3. Run the stage analysis script. Explicit inputs receive priority, but default
   and full flow also include the visible feature package.
4. Read context anchors and any targeted `next_reads` ranges.
5. Emit the canonical scaffold and write section bodies through stdin.
6. Finalize the artifact through deterministic structure and quality gates.
7. Apply the requested state transition.
8. Rebuild the workspace index from the post-transition state.
9. Return the completion or blocker summary directly in the agent response.

The ordering is intentional. Rebuilding the index before the state transition
would publish a stale current stage. Writing an artifact without finalization
would make a draft look complete merely because the file exists.

## System Invariants

| Invariant | Why it matters |
| --- | --- |
| One feature slug per logical feature | Prevents fragmented context and duplicate state |
| One canonical output name per lifecycle stage | Prevents duplicate or ambiguous artifacts |
| TOON writes live under `_ai_sdlc` | Separates machine records from visible delivery prose |
| One active lifecycle skill per feature | Prevents concurrent stages from racing state |
| Full-flow predecessors are complete | Prevents downstream certainty from exceeding upstream evidence |
| Durable decisions have `DEC-###` records | Keeps scope and behavior choices out of chat-only history |
| Default/full artifacts contain shared feature context | Lets every stage stand alone across sessions |
| Indexes are rebuilt after artifact and state updates | Keeps routing projections consistent with sources |
| Divergent legacy/canonical files block migration | Prevents silent data loss |
| Derived context is reproducible | Allows caches to be discarded without losing delivery truth |

## Consistency And Recovery

The harness provides strong single-file writes and serialized state/index
updates, but a feature package still spans multiple files. A terminated process
can therefore leave an artifact updated while state or an index is stale.

Recovery is deterministic:

1. Treat visible artifacts and the decision log as durable evidence.
2. Run migration `--check` to detect path conflicts.
3. Inspect `state.toon` and correct only transitions supported by artifacts.
4. Rebuild the matching workspace index.
5. Run `refinement_status.py` or the SDD validators before resuming.

Never repair a package by deleting the side of a contradiction that is less
convenient. Preserve both inputs, determine authority, and record any material
resolution as a decision.

## Non-Goals

The harness does not attempt to:

- replace an issue tracker, source control, CI, or deployment platform;
- infer stakeholder approval from artifact completeness;
- turn every small task into an 18-stage process;
- make TOON a human documentation format;
- guarantee semantic correctness from structural checks alone.

Its job is to make delivery context explicit, navigable, and verifiable enough
for safe continuation.
