---
layout: default
title: Validate a release
description: Combine focused change checks with compatibility, documentation, and release-contract evidence.
kicker: How-to · Release
permalink: /how-to/validate-release/
nav_order: 22
---

## Start from changed risk

Use `ai-sdlc-validation` to select deterministic checks for the changed packages, contracts, schemas, workflows, and documentation. Run focused tests before broad suites so failures remain attributable.

## Protect public contracts

Run compatibility validation for stable skill names, flow flags, artifact routes, configuration schemas, module API ranges, and required commit audit rules. An additive release should not require undocumented migration.

## Verify delivery evidence

Confirm acceptance criteria map to passing tests, known gaps have owners, security review matches the risk profile, and deployment or installation instructions match the actual release mechanics.

## Record the result

Keep exact commands, outcomes, revision, environment assumptions, skipped checks, and residual risk. “CI green” is a useful signal, but it is not a substitute for knowing which release contracts CI covered.
