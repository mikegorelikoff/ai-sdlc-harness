---
title: Customize presentation and policy
description: Configure presentation preferences separately from enforceable delivery policy.
---

## Keep the two control planes separate

The installed configuration resolver controls typed **presentation preferences**
consumed by context packs. It does not enforce workflow rigor, approval, or
quality gates. The policy skill is the executable control for organization and
project delivery rules. Do not treat `config.resolved.json` as policy evidence.

## Resolve presentation preferences in a consumer

The base file ships inside `ai-sdlc-shared-runtime`; the installed helper finds
it automatically. A user layer remains local unless team policy deliberately
requires it:

```bash
python3 .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_config.py \
  --user ~/.config/ai-sdlc/config.json \
  --write-root . \
  --format toon
```

Expected outputs are `config.resolved.json` and
`_ai_sdlc/config-provenance.toon`. Only the validated `interaction` object is
consumed, as presentation-only metadata, by repository context. It cannot
change evidence selection, tool authority, flow mode, or gates. Delete the two
generated files to stop applying the local projection.

## Keep preference overrides sparse

Specify only values that differ from the inherited configuration. Copying the entire base file freezes old defaults and makes later updates appear successful while behavior silently drifts.

## Enforce organization policy

Built-in policy profiles and their schemas ship inside `ai-sdlc-policy`. Resolve
and evaluate them through the installed consumer path:

```bash
python3 .agents/skills/ai-sdlc-policy/scripts/policy.py . \
  --resolve --profile high-assurance --format markdown
```

Add reviewed organization or project layers with the policy helper's
`--organization` and `--project` arguments. Unknown actions deny by default;
protected rules cannot be weakened by a later layer. A policy decision returns
required gates, but the repository or platform must still make that decision a
required check. Follow [Evaluate delivery policy](evaluate-policy.md).

## Govern material changes

Changes to organization rigor, approval ownership, or protected quality gates
require an accepted decision and enforceable policy/platform control. Personal
presentation preferences cannot lower team policy.
