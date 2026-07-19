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
| Project context contracts | Preserve evidence-backed repository memory and drift identity. |
| Quality finding contracts | Record evidence, severity, owner, resolution, and trace targets. |

## Artifact metadata fields

Required metadata includes feature, artifact, path, workspace, skill, flow mode, state file, decision log, status, owner, timestamps, trace IDs, related artifacts, validation, and metatags.

Versioned schemas evolve additively within a major harness API. Breaking field or authority changes require migration documentation and compatibility review.
