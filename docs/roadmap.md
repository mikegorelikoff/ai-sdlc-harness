---
title: Roadmap
description: The direction of the AI SDLC Harness and the principles that govern future expansion.
---

The harness evolves around one goal: make AI-assisted delivery faster without making it less inspectable, portable, or safe.

## Now

- Ship and support guided onboarding release `1.2.0`, making the AI SDLC lifecycle, every skill, and every operating path understandable from first install through release.
- Preserve the completed `1.1.0` executable delivery control plane as the compatibility foundation, with deterministic TOON as the agent representation and explicit JSON boundaries.
- Measure adoption, compatibility failures, recovery outcomes, and documentation gaps without collecting source content.

## Next

- Connect host adapters to real execution surfaces while preserving capability negotiation, policy checks, and deterministic fallbacks.
- Add signed package attestations and configurable organization trust roots on top of existing digest and provenance validation.
- Add local longitudinal trend reports and regression thresholds without exporting repository content.

## Later

- Add reusable regulated and high-assurance policy profiles with maintained evidence mappings.
- Add more evidence-council execution adapters and reproducible research evidence ingestion.
- Evaluate a future harness API major only when additive contracts can no longer preserve existing consumers.

## Active program

The guided onboarding program is tracked in the
[implementation specification](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/specs/005-guided-onboarding-documentation/requirements.md).
Its ordered T001–T007 tasks close the onboarding, adoption, governance, and
release evidence loop. The [release 1.2 audit](reference/release-1.2.md) maps
each task to exactly one focused commit; the 1.1 control-plane audit remains
available as completed history.

## Roadmap rules

New capability must preserve artifact authority, explain its decisions, provide deterministic validation where possible, and remain optional when it serves a specialized domain. Proposals become roadmap work only when their user value, compatibility impact, evidence model, and maintenance owner are clear.
