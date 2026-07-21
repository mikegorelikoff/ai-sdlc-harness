---
title: Verify a package and local metrics
description: Check independent package trust controls and generate reproducible content-free delivery aggregates.
---

# Verify a package and local metrics

Run from an installed consumer repository. `packages/example` and its manifest
are placeholders: create or obtain a reviewed package and an
`ai-sdlc-package/v1` manifest using the schemas in
`.agents/skills/ai-sdlc-package-trust/references/` before running the command.

Verify a package against explicit local policy:

```bash
python3 .agents/skills/ai-sdlc-package-trust/scripts/package_trust.py . \
  --package-root packages/example --manifest packages/example.package.json \
  --allowed-origin repository \
  --allowed-capability filesystem.read \
  --require-provenance --write
```

Review origin, compatibility, capabilities, integrity, and provenance as
independent controls. A digest proves byte identity, not author identity or
approval. A deny decision must block installation or execution.

Generate local aggregates:

```bash
python3 .agents/skills/ai-sdlc-package-trust/scripts/metrics.py . --generate --write
```

Metrics include only status and numeric run, task, retry, budget, evidence, and
freshness aggregates plus input fingerprints. They never contain source, file
paths, prompts, commands, diffs, messages, or reason text and are never uploaded.
An empty repository returns `insufficient-data` instead of invented zeros framed
as performance evidence.

Expected output is a structured allow/deny trust decision and a content-free
metrics artifact below `_ai_sdlc/`. A missing manifest, hash mismatch, origin
mismatch, or absent required provenance is a failure to resolve at the package
source—not a reason to weaken the command-line policy.
