<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# Migration And Concurrency

The harness uses canonical names and `_ai_sdlc` paths, but existing feature
packages may contain files produced by older skill versions. Migration must
preserve data, and concurrent agents must not publish partially written state
or indexes.

## Canonical Write Policy

All new writes use canonical paths. Legacy paths are compatibility inputs only.

Examples:

| Legacy | Canonical |
| --- | --- |
| `<feature>/state.toon` | `<feature>/_ai_sdlc/state.toon` |
| `<feature>/plan.toon` | `<feature>/_ai_sdlc/plan.toon` |
| `<workspace>/specs-index.toon` | `<workspace>/_ai_sdlc/specs-index.toon` |
| `<feature>/.ai-sdlc/context/<skill>.toon` | `<feature>/_ai_sdlc/context/<skill>.toon` |
| `discovery-notes.md` | `discovery.md` |
| `qa-plan.md` | `qa.md` |
| `qa-traceability.md` | `qa-readiness.md` |

The artifact profile registry contains every supported legacy Markdown alias.
Do not add ad hoc aliases in individual skills.

## Safe Migration Matrix

| Canonical file | Legacy file | Result |
| --- | --- | --- |
| Missing | Missing | No action |
| Missing | Present | Atomically move legacy to canonical |
| Present | Present, byte-identical | Keep canonical and remove duplicate legacy |
| Present | Present, different | Block with `MIGRATION CONFLICT`; modify neither |
| Present | Missing | No action |

The divergent case intentionally requires judgment. Filename precedence is not
evidence that one body is correct, and modification time is not a safe merge
policy.

## Migration CLI

Check without changing files:

```bash
python3 skills/_shared/ai_sdlc_migrate.py \
  --workspace all --check
```

Apply safe moves and identical deduplication:

```bash
python3 skills/_shared/ai_sdlc_migrate.py \
  --workspace all --apply
```

`--check` exits non-zero when an action is required and exits with the conflict
code when divergent content exists. Normal artifact and index writers apply the
same safe migration before their first write, so new activity naturally moves
old packages forward.

## Resolving A Divergent Conflict

When both files differ:

1. Stop the current write or cascade stage.
2. Open both files and identify unique facts, decisions, IDs, and status.
3. Determine the correct canonical content using artifact authority and the
   decision log; do not rely only on timestamps.
4. Merge deliberately into the canonical path.
5. Preserve a material resolution in `decision-log.md` when behavior, scope, or
   accepted evidence changed.
6. Remove the legacy file only after verifying the canonical result.
7. Rerun migration `--check`, rebuild indexes, and rerun the relevant status or
   validation gate.

## Atomic Writes

State, indexes, context snapshots, and scaffold-owned artifacts use temporary
files in the destination directory followed by atomic replacement. Readers see
either the previous complete file or the new complete file, never a partially
written body.

Atomic replacement protects one file. It does not make an entire feature
package a database transaction, so write ordering remains important.

## Write Serialization

State and workspace-index mutations use OS advisory locks at
`_ai_sdlc/.write.lock`. Locks are released automatically when the process exits,
including abnormal termination.

Serialization prevents these races:

- two agents both loading the same state and overwriting each other's stage;
- two index builders publishing scans from overlapping writes;
- a reader observing truncated state or index output.

Lock files are operational and ignored by Git. A timeout means another writer
is active or unhealthy; the agent should report the lock path rather than
bypassing synchronization.

## Durable Write Ordering

Artifact finalization follows this order:

1. Run migration and transition preflight.
2. Validate section, table, context, and size gates.
3. Atomically write the finalized artifact and required decision record.
4. Apply the state transition under the feature lock.
5. Scan the post-transition workspace and atomically rebuild indexes under the
   workspace lock.
6. Return the completion summary.

State must precede index rebuild. Otherwise the new artifact can appear in an
index row whose current stage still reflects the previous lifecycle step.

## Derived Versus Durable Machine Files

| File | Durable | Git behavior |
| --- | --- | --- |
| `_ai_sdlc/state.toon` | Yes | Keep with the feature package |
| `_ai_sdlc/plan.toon` | Yes | Keep with implementation planning |
| `_ai_sdlc/specs-index.toon` | Rebuildable projection, operationally important | Keep when repository workflow tracks indexes |
| `_ai_sdlc/context/<skill>.toon` | No | Ignore; regenerate from sources |
| `_ai_sdlc/feature-context.toon` | No | Ignore; regenerate from sources |
| `_ai_sdlc/.write.lock` | No | Ignore |

Deleting a derived context file loses cache efficiency, not delivery truth.
Deleting state or a decision log loses lifecycle or decision history and is not
a cache cleanup operation.

## Interrupted Write Recovery

After an interrupted process:

1. Run migration `--check` for path conflicts.
2. Inspect the visible artifact and decision log for completed durable work.
3. Inspect state for an active or incomplete stage.
4. Complete or roll forward state only when the artifact supports it.
5. Rebuild the workspace index.
6. Rerun full package status or implementation validators.

Do not reset the whole feature package merely because one projection is stale.
Repair the smallest inconsistent layer from its authoritative sources.

## Failure Modes

The agent must not:

- overwrite a divergent canonical file with legacy content;
- keep writing after a migration conflict;
- manually edit derived context as if it were source evidence;
- bypass a write lock to make progress faster;
- rebuild an index before committing the matching state transition;
- commit context snapshots or lock files as durable feature artifacts.
