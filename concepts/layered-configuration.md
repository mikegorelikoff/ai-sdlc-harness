<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# Layered Configuration

The harness resolves configuration in one deterministic order: base, then
team, then user. Every resolved leaf records its source layer. Identical inputs
therefore produce identical values and provenance.

All layers use `ai-sdlc-config/v1`. The source compatibility copy of the base
template remains at `config/ai-sdlc.defaults.json`;
installed consumers use the packaged default automatically. Teams and users may provide partial `values`
objects. Current workflows consume only typed interaction preferences from the
resolved projection. Delivery rigor and gates are enforced through
`ai-sdlc-policy` and repository/platform controls, not this configuration.

Run:

```bash
python3 .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_config.py \
  --team .ai-sdlc/team.json \
  --user ~/.config/ai-sdlc/config.json \
  --format toon
```

With `--write-root`, the resolver writes `config.resolved.json` and
`_ai_sdlc/config-provenance.toon`. Context helpers use only its presentation
profile; they do not treat it as policy.
