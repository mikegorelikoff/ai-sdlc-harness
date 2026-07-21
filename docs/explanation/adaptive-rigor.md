---
title: Adaptive rigor
description: Why delivery controls should follow risk, uncertainty, and reversibility rather than a universal ceremony level.
---

Uniform process creates two failure modes: low-risk changes drown in ceremony, while deceptively small high-risk changes receive too little scrutiny. Adaptive rigor separates work size from delivery risk.

## The profiles

Patch favors narrow evidence for reversible changes. Standard supports normal feature delivery. Assured adds stronger cross-artifact and review gates. Regulated preserves formal evidence, ownership, and approval expectations for sensitive domains.

## Explainable selection

Classification is deterministic for the same inputs and exposes factor scores, escalation reasons, and the effective override. Relevant factors include data sensitivity, authorization, external contracts, migration behavior, blast radius, rollback difficulty, operational coupling, and uncertainty.

## Safe precedence

An explicit full-flow request raises rigor. An organization minimum raises it
only when the caller supplies that minimum to the rigor decision or an
enforced `ai-sdlc-policy` rule requires the corresponding gates. Presentation
configuration is not a rigor input. Unknown values remain conservative.

Adaptive rigor is therefore a routing aid, not permission to skip reasoning. The decision stays inspectable and can be challenged with better evidence.
