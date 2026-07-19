---
title: Customize team policy
description: Layer organization and personal preferences without editing installed defaults or weakening protected gates.
---

## Choose the correct layer

Base configuration ships with the harness. Team configuration belongs in the repository and is reviewed. User configuration holds personal preferences and remains local. Put a value in the narrowest layer that legitimately owns it.

## Keep overrides sparse

Specify only values that differ from the inherited configuration. Copying the entire base file freezes old defaults and makes later updates appear successful while behavior silently drifts.

## Resolve with provenance

Run the configuration resolver and inspect the effective value plus its source layer. Test both the happy path and an attempted weakening of security, approval, or evidence minimums.

## Govern material changes

Changes to organization minimum rigor, approval ownership, or protected quality gates require an accepted decision. Personal customization may change presentation preferences; it cannot lower team safety policy.
