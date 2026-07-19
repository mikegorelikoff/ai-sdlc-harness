---
title: Build a task context pack
description: Map repository topology and select explained, secret-safe task context within an explicit budget.
---

# Build a task context pack

Inspect ownership and source-to-test topology first:

```bash
python3 skills/ai-sdlc-project-context/scripts/context_engine.py \
  --topology --write --format toon
```

Then identify one task, its outcome, known relevant paths or tags, and a token
budget:

```bash
python3 skills/ai-sdlc-project-context/scripts/context_engine.py \
  --build-pack \
  --task T009 \
  --goal "Implement bounded context selection" \
  --path specs/004-executable-delivery-control-plane/tasks.md \
  --tag implementation \
  --budget 2000 \
  --write --format markdown
```

Review selected ranges, reasons, hashes, truncation, total budget, exclusions,
and freshness warnings. A missing evidence ledger or stale project context is a
warning that needs resolution or an explicit task decision; it is never
reported as current evidence.

## Add conditional selectors

An `ai-sdlc-context-selectors/v2` file can match a task glob, any relevant path
glob, and any tag. Each selector declares safe include globs, priority,
per-source cap, and a human reason. Top-level exclusion globs always win.

Use selectors for repository-specific high-signal sources, not as permission to
scan everything. Credential-like content, secret paths, binaries, symlinks,
generated output, and files beyond size limits remain excluded regardless of
selector priority.
