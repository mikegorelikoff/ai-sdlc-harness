---
title: Migrate to 1.1
description: Adopt the additive executable control plane while preserving existing artifacts and integrations.
---

# Migrate to 1.1

Release `1.1.0` remains on harness API `1.0.0`. Existing skills, Markdown
artifacts, state files, configuration layers, module manifests, and quick/full
flow behavior remain valid; no bulk rewrite is required.

## Before updating

1. Commit or back up repository-local configuration and delivery artifacts.
2. Record the installed revision and selected skills or modules.
3. Run the `1.0.0` validation commands available in the current checkout.

## Update and verify

1. Install or check out release `v1.1.0` using the same installation method only
   when reproducing that historical baseline. Release `v1.2.0` is also
   reproducible but has a confirmed complete-workflow defect; new consumers
   should retain an already accepted prior pin or wait for a corrected immutable
   release, as explained in [Install](install.md).
2. Run the installation doctor and preview any proposed upgrade before applying it.
3. Run the compatibility gate:

   ```bash
   python3 skills/_shared/ai_sdlc_compatibility.py --skip-git-audit --format toon
   ```

4. Re-run the project-context drift check and the status gate for active features.
5. Opt into change sets, graph indexes, policies, context packs, runtime state,
   workflows, adapters, package trust, or metrics only where they add value.

New generated control-plane data belongs under feature or repository
`_ai_sdlc` directories. Complete deterministic TOON is the primary
agent-facing representation. Keep JSON consumers only at JSON Schema, external
interoperability, recovery comparison, or append-only JSONL journal boundaries.
Where an older automation explicitly consumes prose, keep `--format markdown`;
where a supported boundary needs JSON, keep its explicit JSON mode rather than
changing the global representation strategy.

## Roll back

Reinstall `v1.0.0`, restore only package-owned files, and preserve all feature
artifacts and new machine records. If an older reader cannot understand a new
schema, leave the record intact and use the documented migration or export
path. Never silently delete or rewrite authoritative Markdown.
