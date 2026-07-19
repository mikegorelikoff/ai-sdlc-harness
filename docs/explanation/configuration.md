---
title: Layered configuration
description: How defaults, team policy, and personal preferences combine with provenance and protected boundaries.
---

Customization is necessary for real teams, but unstructured overrides make behavior impossible to reproduce. Layered configuration provides flexibility while keeping the effective result explainable.

## Ownership layers

Base values are shipped and versioned by the harness. Team values are committed and reviewed as organization policy. User values remain local and cover personal presentation or convenience preferences.

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
