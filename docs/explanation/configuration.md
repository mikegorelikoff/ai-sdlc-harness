---
title: Presentation configuration and delivery policy
description: How presentation preferences remain separate from enforceable organization controls.
---

Customization is necessary for real teams, but presentation preferences and
delivery controls have different authority. The configuration resolver creates
an inspectable preference projection. The policy skill evaluates enforceable
delivery rules. Neither artifact grants platform permissions by itself.

## Ownership layers

Base presentation values ship inside the installed shared-runtime skill. User
values remain local. If a team chooses to standardize presentation, its sparse
layer may be reviewed and committed, but it is not organization delivery policy.

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
python3 .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_config.py \
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

## Resolver boundary

The generic resolver can preserve declared values and provenance, but current
workflow helpers consume only the typed `interaction` object. Resolved values
for rigor, gates, approval, or modules would be informational and must not be
represented as enforced. Use executable policy and protected repository or CI
settings for those controls.

## Executable policy

Presentation configuration supplies communication preferences; policy evaluates whether a
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
