---
layout: default
title: Flow flags
description: Stable execution-mode flags and their precedence rules across AI SDLC skills and helper scripts.
kicker: Reference · CLI
permalink: /reference/flow-flags/
nav_order: 55
---

| Flag | Contract |
| --- | --- |
| `--quick-flow` | Make evidence-backed assumptions for low-risk gaps, run focused checks, and keep assumptions visible. |
| `--full-flow` | Stop on missing material decisions or predecessors and run stricter end-to-end gates. |
| Both flags | Full flow takes precedence. |
| Neither flag | Use the skill’s least-risky default or an explainable adaptive policy when supported. |

## Common output modes

Human-facing commands normally return Markdown. Deterministic helpers may support `--format toon` for compact agent consumption. Machine output must preserve the same result, blocker, and trace meaning as the human view.

## Precedence

Explicit full flow and organization minimum policy cannot be downgraded by automatic classification or a user override. Unknown risk inputs cannot reduce rigor.
