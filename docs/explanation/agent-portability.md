---
layout: default
title: Agent portability
description: Why workflows are packaged as inspectable repository skills instead of depending on one assistant host or conversational persona.
kicker: Explanation · Portability
permalink: /explanation/agent-portability/
nav_order: 42
---

AI tools change quickly. Delivery evidence, team policy, and workflow contracts should outlive a specific model, chat surface, or agent runtime.

## Repository-local instructions

Each skill is a plain package with applicability, inputs, steps, outputs, scripts, and references. A capable assistant can inspect the contract before acting. The repository—not a remote hidden prompt—defines the expected workflow.

## Host capabilities are optional accelerators

Some hosts provide subagents, browsers, connectors, or sandboxes. Skills may use them when the task and policy allow, but the durable artifact contract remains host-neutral. Missing optional capability produces a fallback or explicit blocker.

## Continuity beyond conversation

State, plans, decisions, indexes, context, and validation live with the project. Another assistant can resume from those artifacts without reproducing the original dialogue or trusting an unverifiable summary.

Portability does not mean identical user experience everywhere. It means the delivery truth and safety boundaries remain consistent.
