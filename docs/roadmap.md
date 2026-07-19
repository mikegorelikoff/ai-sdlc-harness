---
title: Roadmap
description: The direction of the AI SDLC Harness and the principles that govern future expansion.
---

The harness evolves around one goal: make AI-assisted delivery faster without making it less inspectable, portable, or safe.

## Now

- Deliver controlled specification evolution through isolated change sets, semantic deltas, non-mutating preview, policy-gated apply, and evidence-preserving archive.
- Build a repository-wide delivery graph with trace queries, gap detection, evidence coverage, and freshness propagation.
- Add versioned policy evaluation and bounded task-specific context packs without weakening existing artifact authority.

## Next

- Add a resumable task runtime with durable journals, budgets, retries, stop reasons, and one-task-one-commit boundaries.
- Add declarative workflows with gates, hooks, dependency waves, cycle detection, and safe sequential fallbacks.
- Publish a portable host adapter SDK with capability negotiation and deterministic fallback behavior.
- Add installation diagnostics, upgrade previews, migration backups, and rollback planning.

## Later

- Validate module and workflow trust through origin, integrity, compatibility, declared capability, and update provenance.
- Publish privacy-preserving local delivery metrics and reusable regulated or high-assurance policy profiles.
- Complete versioned documentation, release migration guidance, and additional evidence-council execution adapters.

## Active program

The executable delivery control-plane program is tracked in the
[implementation specification](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/specs/004-executable-delivery-control-plane/requirements.md).
Its ordered tasks move from controlled spec evolution through delivery graph,
policy, context, runtime, interoperability, operations, and release. Each task
must pass focused validation and land as exactly one commit before the next task
starts.

## Roadmap rules

New capability must preserve artifact authority, explain its decisions, provide deterministic validation where possible, and remain optional when it serves a specialized domain. Proposals become roadmap work only when their user value, compatibility impact, evidence model, and maintenance owner are clear.
