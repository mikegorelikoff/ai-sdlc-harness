---
title: Migrate to 2.0
description: Move from Harness API 1.x to the 2.0 release candidate and context contract v3 safely.
---

# Migrate to 2.0

Release candidate `v2.0.0-rc.1` introduces Harness API `2.0.0`. The intentional
breaking change is the default context snapshot and task-pack contract:
consumers that parse only `ai-sdlc-context/v2` or
`ai-sdlc-context-pack/v2` must add v3 support before upgrading.

## Before updating

1. Commit or back up the consumer repository and record
   `.ai-sdlc/harness-install.json` plus the managed skill inventory.
2. Find integrations that parse context TOON, context-pack fields, module
   manifests, or an exact Harness API range.
3. Preserve active specifications, decision logs, state, and validation
   evidence. Do not delete delivery artifacts during a skill reinstall.
4. Read the [release candidate evidence](../reference/release-2.0.md) and accept
   the prerelease, licensing, and host-support limitations explicitly.

## Update and verify

1. Follow [Update safely](update.md) using the exact commit resolved from
   `v2.0.0-rc.1`.
2. Update context readers for v3 authority labels, sufficiency states,
   goal-relevant source ranges, fingerprints, and targeted `next_reads`.
3. Change module compatibility ranges to accept Harness API `2.0.0` only after
   the module passes its own tests. Bundled modules declare `>=2.0.0,<3.0.0`.
4. Start a new agent session so the host reloads the installed skill inventory.
5. Run the navigator diagnostic, a complete disposable SDD workflow, the
   project tests, and the install-record validator.

Existing context command flags, selector v2, topology v2, canonical artifact
routes, and quick/full flow flags remain available. Compatibility at those
surfaces does not make a v2-only context parser compatible with v3 output.

## Roll back

Reinstall the last locally accepted exact revision, restore only harness-owned
skill and install-record files, and keep product specifications and evidence.
If a v2-only integration cannot read a v3 record, preserve the record and use
the old reader against the prior checkout; never rewrite authoritative evidence
silently.
