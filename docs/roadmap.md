---
title: Roadmap
description: The direction of the AI SDLC Harness and the principles that govern future expansion.
---

The harness evolves around one goal: make AI-assisted delivery faster without making it less inspectable, portable, or safe.

## Now

- Release and support the completed executable delivery control plane: controlled change sets, delivery graph, evidence freshness, policy, bounded context, resumable runtime, declarative workflows, portable adapters, safe upgrades, package trust, and private local metrics.
- Keep the `1.1.0` release additive over harness API `1.0.0`, with complete deterministic TOON as the agent representation and explicit JSON boundaries.
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

The executable delivery control-plane program is tracked in the
[implementation specification](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/specs/004-executable-delivery-control-plane/requirements.md).
Its ordered T001–T015 tasks are complete. They move from controlled spec
evolution through delivery graph, policy, context, runtime, interoperability,
operations, and release. The [release audit](reference/release-1.1.md) maps each
task to exactly one focused commit.

## Roadmap rules

New capability must preserve artifact authority, explain its decisions, provide deterministic validation where possible, and remain optional when it serves a specialized domain. Proposals become roadmap work only when their user value, compatibility impact, evidence model, and maintenance owner are clear.
