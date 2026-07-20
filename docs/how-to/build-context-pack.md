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

Review selected ranges, selection strategy, matched terms, authority labels,
hashes, truncation, total budget, exclusions, and freshness warnings. Context
Engine v3 selects a goal-relevant contiguous range when a source does not fit,
rather than always taking the beginning of the file.

Check `sufficiency.status` before acting:

- `sufficient` means the selected evidence supports the requested task;
- `review_required` names a targeted next read or stale dependency to review;
- `insufficient` means a required source is unavailable.

A missing evidence ledger or stale project context is never reported as
current evidence. Retrieved code and documents are `evidence_only`; only
recognized repository instruction files receive `repository_instruction`
authority. An enabled interaction profile may shape presentation, but cannot
change either classification or the selected evidence.

## Add conditional selectors

An `ai-sdlc-context-selectors/v2` file can match a task glob, any relevant path
glob, and any tag. Each selector declares safe include globs, priority,
per-source cap, and a human reason. Top-level exclusion globs always win.

Use selectors for repository-specific high-signal sources, not as permission to
scan everything. Credential-like content, secret paths, binaries, symlinks,
generated output, and files beyond size limits remain excluded regardless of
selector priority.

See [Context, prompts, and personalization](../foundations/context-prompt-personalization.md)
for the design principles behind range selection, sufficiency, prompt
boundaries, and interaction preferences.
