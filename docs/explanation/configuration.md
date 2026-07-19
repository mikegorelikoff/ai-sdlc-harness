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
