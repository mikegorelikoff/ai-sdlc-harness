---
title: Layered configuration
description: How defaults, team policy, and personal preferences combine with provenance and protected boundaries.
---

Customization is necessary for real teams, but unstructured overrides make behavior impossible to reproduce. Layered configuration provides flexibility while keeping the effective result explainable.

## Ownership layers

Base values are shipped and versioned by the harness. Team values are committed and reviewed as organization policy. User values remain local and cover personal presentation or convenience preferences.

## Typed interaction preferences

The optional `interaction` object controls communication presentation without
creating a persona or granting authority. It is disabled by default and may
contain a preferred name, response language, response density, technical
depth, and progress-update cadence.

For example, a local user layer can contain:

```json
{
  "schema": "ai-sdlc-config/v1",
  "values": {
    "interaction": {
      "enabled": true,
      "preferred_name": "Sam",
      "language": "en",
      "response_style": "concise",
      "technical_depth": "practitioner",
      "status_updates": "milestones"
    }
  }
}
```

Resolve the layers normally and inspect provenance:

```bash
python3 skills/_shared/ai_sdlc_config.py \
  --base config/ai-sdlc.defaults.json \
  --user ~/.config/ai-sdlc/config.json \
  --write-root . \
  --format toon
```

The resolved profile is attached to context packs as `presentation_only`
metadata. It cannot alter evidence selection, recognized instruction
authority, protected gates, approval rules, validation rigor, or safety. Set
`enabled` to `false`, remove individual values, or delete the local user layer
and resolve again to stop applying it. No chat history or connected data is
mined to infer preferences.

See [Context, prompts, and personalization](../foundations/context-prompt-personalization.md)
for usage guidance and anti-patterns.

## Deterministic resolution

The resolver applies documented precedence and emits provenance for every effective key. Identical layers produce identical output. Sparse overrides inherit future defaults; full copied configurations tend to drift.

## Protected controls

Some settings define minimum rigor, security validation, approval authority, or evidence requirements. Lower layers cannot weaken them. A rejected override is reported with the source and protected rule instead of being silently ignored.

Provenance makes configuration debuggable: a reviewer can see not only the final value, but who owns it and why it won.

## Executable policy

Configuration supplies general harness values; policy evaluates whether a
specific delivery action is allowed, denied, or gated. Versioned policy layers
resolve in base, organization, project, and user order. Every effective rule
retains its source layer and fingerprint.

Protected policy rules are monotonic. A lower layer may strengthen an effect or
add required gates, but it cannot change the protected action scope, narrow its
predicates, remove gates, clear protection, or turn a non-waivable rule into a
waivable one. Invalid weakening fails closed and names the exact source and
rule.

An action decision combines matching rules with deny-first precedence and
returns every required gate and reason. Unknown actions deny by default.
Reusable high-assurance and regulated organization profiles add stronger
evidence, security, privacy, audit, and provenance controls without copying the
base policy.

Waivers are separate, owner-approved, decision-linked, and expiring records.
They suppress only one explicitly waivable rule for one matching action,
subject, and constraint set. An expired or mismatched waiver remains visible in
explain output but does not weaken the decision.
