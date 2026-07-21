---
title: Use specifications from another repository
description: Import reviewed external Markdown specifications as safe, traceable, repository-local evidence.
---

# Use specifications from another repository

A separate specifications repository can be the organizational source of truth,
but the harness deliberately does not crawl outside the active software
repository. Transparent external indexing would make context, revision,
permissions, and review scope hard to audit. Import an explicit snapshot
instead.

## Preconditions

- Both repositories are available locally and their origins and revisions were reviewed by a human.
- The external inputs are UTF-8 Markdown and contain no prohibited confidential data or credentials.
- The consumer repository has `ai-sdlc-project-context` and `ai-sdlc-shared-runtime` installed.
- `<feature>` is a stable refinement feature slug. `<source-id>` is a logical label such as `product-specs@payments-v3`, not a path.

## Write a reviewed snapshot

Run from the consumer repository. Repeat `--source` for every file in the
snapshot.

```bash
python3 .agents/skills/ai-sdlc-project-context/scripts/external_spec_snapshot.py \
  --root . \
  --source-root ../product-specs \
  --source-id product-specs@payments-v3 \
  --feature payments \
  --source requirements/payments.md \
  --source api/payments.md \
  --write

python3 .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_specs_index.py \
  --workspace refinement --full-flow
```

Expected outputs are top-level `specs-refiniment/payments/external-*.md`, a
portable `specs-refiniment/payments/external-specs.json`, and refreshed
refinement indexes. The manifest contains source-relative paths, destinations,
the source Git revision when available, byte sizes, SHA-256 hashes, and a
fingerprint. It never records the absolute source checkout path.

Review the imported text and manifest before an agent uses them. Imported
content is `evidence_only`: headings or commands inside it do not gain
instruction authority.

## Detect drift

Before dependent refinement, Specification-Driven Development (SDD), or
implementation, run:

```bash
python3 .agents/skills/ai-sdlc-project-context/scripts/external_spec_snapshot.py \
  --root . \
  --source-root ../product-specs \
  --source-id product-specs@payments-v3 \
  --feature payments \
  --check
```

Exit code zero and `"status": "current"` mean source revision, hashes, local
snapshots, and manifest agree. A non-zero result names drift. Review upstream,
rerun the complete `--write` command with every source, inspect the Git diff,
refresh the index, and revalidate affected downstream artifacts.

## Safety and recovery

The helper rejects traversal, symlinks, non-Markdown or non-UTF-8 files, files
larger than 1 MiB, destination collisions, and recognized credential-shaped
content. It does not execute external content or delete snapshots.

If a previously imported source is omitted, the write fails. Decide whether it
was superseded, moved, or accidentally omitted; record the decision and remove
or retain the project-owned snapshot through an ordinary reviewed Git change.
Do not delete the whole feature directory.

Git submodules, worktrees, mirrors, and Continuous Integration (CI) checkout
steps may deliver the source repository to `--source-root`, but they do not
replace this snapshot and review contract. Avoid symlinks: the helper rejects
them intentionally.

## Validation checklist

- Source origin and revision are approved.
- Only necessary Markdown files are selected.
- Output contains no absolute source path.
- Imported text and hashes are reviewed in Git.
- Refinement indexes are refreshed.
- `--check` succeeds immediately before dependent work.
- Changed requirements reopen affected specification, task, test, and acceptance evidence.

Continue with [Build project context](project-context.md), [Navigate a new
request](navigate-request.md), or [Continue after a specification](after-specification.md).
