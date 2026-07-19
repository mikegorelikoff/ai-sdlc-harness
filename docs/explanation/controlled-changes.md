---
title: Controlled changes
description: How isolated change workspaces keep proposed intent separate from canonical system truth.
---

# Controlled changes

A change request should not become system truth merely because an AI assistant
generated convincing Markdown. The harness therefore separates proposed intent
from canonical artifacts before any delta, impact analysis, approval, or apply
operation occurs.

## Workspace boundary

`ai-sdlc-change-set` creates a complete workspace under
`changes/<change-id>/`. It contains the proposal, design, tasks, delta index,
evidence index, and a compact versioned record. Creation is atomic and refuses
an existing destination.

Canonical targets are recorded as safe repository-relative paths, but their
contents are neither read nor changed during workspace creation. Targets inside
`changes/`, absolute paths, traversal, and duplicates are rejected.

## Authority

The workspace has `draft` status and explicitly denies canonical and policy
mutation. It becomes input to later lifecycle gates:

1. semantic delta validation;
2. non-mutating apply preview and impact analysis;
3. policy evaluation and required approval;
4. atomic apply and evidence-preserving archive.

Until those gates exist and pass, the canonical specifications, accepted
decisions, organization policy, and Git history remain authoritative.

## Deterministic use

```bash
python3 skills/ai-sdlc-change-set/scripts/change_set.py . \
  --change-id add-session-timeout \
  --title "Add session timeout" \
  --summary "Expire inactive sessions." \
  --owner Security \
  --target specs/auth/requirements.md \
  --create --full-flow

python3 skills/ai-sdlc-change-set/scripts/change_set.py . \
  --change-id add-session-timeout \
  --validate --format toon
```

Use `--emit` first when a reviewer needs to inspect the planned identity and
fingerprint without creating files.

## Semantic deltas

After intake, add Markdown delta documents below the workspace `deltas/`
directory. Each file declares one canonical target and groups stable
requirement IDs under `ADDED`, `MODIFIED`, `REMOVED`, or `RENAMED Requirements`.

Added and modified requirements carry their complete normative statement plus
WHEN/THEN scenarios. Removed requirements require a reason and migration path;
renames retain the existing stable ID and declare distinct old and new names.

```bash
python3 skills/ai-sdlc-change-set/scripts/spec_delta.py . \
  --change-id add-session-timeout \
  --validate --write --format toon
```

Validation proves target declaration, stable-ID presence or absence, scenario
completeness, source hashes, and absence of overlapping operations. The
generated `delta-set.json` is still non-authoritative and cannot apply itself.

## Apply preview

Preview recompiles the authoritative delta Markdown against current target
bytes. It produces virtual after-state hashes and unified diffs, detects
ambiguous blocks and overlaps with other active changes, finds exact downstream
references that need revalidation, and explains every required gate.

```bash
python3 skills/ai-sdlc-change-set/scripts/change_preview.py . \
  --change-id add-session-timeout \
  --preview --write --format toon
```

A ready preview still has no write authority. A conflicting preview returns
`blocked`, preserves the evidence for review, and never guesses which target
block or proposal should win.
