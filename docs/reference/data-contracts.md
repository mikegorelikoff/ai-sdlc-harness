---
title: Data contracts
description: Core versioned records used for artifacts, handoffs, modules, compatibility, context, and findings.
---

| Schema | Purpose |
| --- | --- |
| `ai-sdlc-artifact-metadata/v1` | Route, own, index, and trace Markdown artifacts. |
| `ai-sdlc-handoff/v1` | Communicate result, blockers, and next actions. |
| `ai-sdlc-module/v1` | Register compatible core or optional capabilities. |
| `ai-sdlc-compatibility-result/v1` | Report release contract validation. |
| `ai-sdlc-change-set/v1` | Identify an isolated draft change, its canonical targets, authority boundary, artifacts, and deterministic fingerprint. |
| `ai-sdlc-spec-delta/v1` | Project validated requirement operations, stable IDs, source hashes, scenarios, and non-mutation authority. |
| `ai-sdlc-change-preview/v1` | Record virtual target diffs, conflicts, stale evidence, reopen actions, gates, and drift-sensitive preview identity. |
| `ai-sdlc-change-approval/v1` | Bind an accountable accepted decision and complete gate set to one current preview fingerprint. |
| `ai-sdlc-change-recovery/v1` | Preserve target hashes, backups, applied paths, transaction state, and rollback evidence. |
| `ai-sdlc-delivery-node/v1` | Identify one feature-scoped lifecycle object with exact repository or Git anchors. |
| `ai-sdlc-delivery-edge/v1` | Record one evidence-backed semantic or declaration relationship. |
| `ai-sdlc-delivery-graph/v1` | Aggregate deterministic nodes, edges, coverage gaps, orphans, source identity, and graph identity. |
| `ai-sdlc-evidence-source/v1` | Capture producer, subjects, artifact and dependency hashes, expiry, and upstream evidence identity. |
| `ai-sdlc-evidence-ledger/v1` | Recalculate evidence state, propagate staleness, and report fresh-only lifecycle coverage. |
| `ai-sdlc-policy-layer/v1` | Declare versioned action rules, predicates, effects, gates, protection, and waiver eligibility. |
| `ai-sdlc-policy-waiver/v1` | Bind one accountable, constrained, expiring exception to an exact rule and decision. |
| `ai-sdlc-policy-decision/v1` | Explain the resolved allow, require, or deny result with provenance, gates, reasons, and waiver outcomes. |
| Project context contracts | Preserve evidence-backed repository memory and drift identity. |
| Quality finding contracts | Record evidence, severity, owner, resolution, and trace targets. |

## Artifact metadata fields

Required metadata includes feature, artifact, path, workspace, skill, flow mode, state file, decision log, status, owner, timestamps, trace IDs, related artifacts, validation, and metatags.

Versioned schemas evolve additively within a major harness API. Breaking field or authority changes require migration documentation and compatibility review.
