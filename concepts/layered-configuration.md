<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# Layered Configuration

The harness resolves configuration in one deterministic order: base, then
team, then user. Every resolved leaf records its source layer. Identical inputs
therefore produce identical values and provenance.

All layers use `ai-sdlc-config/v1`. The canonical base template is
`config/ai-sdlc.defaults.json`; teams and users may provide partial `values`
objects. Only the base declares protected dotted paths. Later layers may
strengthen protected rigor or gates but cannot weaken them or redefine which
paths are protected.

Run:

```bash
python3 skills/_shared/ai_sdlc_config.py \
  --base config/ai-sdlc.defaults.json \
  --team .ai-sdlc/team.json \
  --user ~/.config/ai-sdlc/config.json \
  --format toon
```

With `--write-root`, the resolver writes `config.resolved.json` and
`_ai_sdlc/config-provenance.toon`. Consumers should use the resolved projection,
not independently merge layer files.
