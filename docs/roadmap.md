---
title: Roadmap
description: The direction of the AI SDLC Harness and the principles that govern future expansion.
---

The harness evolves around one goal: make AI-assisted delivery faster without making it less inspectable, portable, or safe.

## Now

- Validate `v2.0.0-rc.1`, close its license and protected-CI blockers, and promote the same reviewed capability set to stable `v2.0.0`.
- Preserve the completed `1.1.0` executable delivery control plane as the compatibility foundation, with deterministic TOON as the agent representation and explicit JSON boundaries.
- Measure adoption, compatibility failures, recovery outcomes, and documentation gaps without collecting source content.

## Next

- Connect host adapters to real execution surfaces while preserving capability negotiation, policy checks, and deterministic fallbacks.
- Add signed package attestations and configurable organization trust roots on top of existing digest and provenance validation.
- Add local longitudinal trend reports and regression thresholds without exporting repository content.

## Later

- Add reusable regulated and high-assurance policy profiles with maintained evidence mappings.
- Add more evidence-council execution adapters and reproducible research evidence ingestion.
- Evolve Harness API `2.x` additively and require an explicit migration before any future API major.

## Active program

The guided onboarding program is tracked in the
[implementation specification](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/specs/005-guided-onboarding-documentation/requirements.md).
Its ordered T001–T007 tasks close the onboarding, adoption, governance, and
release evidence loop. The [release 2.0 candidate](reference/release-2.0.md)
combines that foundation with context v3, production hardening, security audit,
and field-operation fixes. The 1.2 and 1.1 audits remain completed history.

## Roadmap rules

New capability must preserve artifact authority, explain its decisions, provide deterministic validation where possible, and remain optional when it serves a specialized domain. Proposals become roadmap work only when their user value, compatibility impact, evidence model, and maintenance owner are clear.
