---
layout: default
title: Build project context
description: Capture architecture and delivery conventions with source evidence and drift detection.
kicker: How-to · Context
permalink: /how-to/project-context/
nav_order: 15
---

## Generate from evidence

Run `ai-sdlc-project-context --quick-flow` at the repository root. Ask it to inspect project instructions, build manifests, CI, tests, ownership, architecture docs, active specs, and validation commands.

## Review the evidence anchors

Every important fact should cite a path, command, or accepted decision. Remove inferred claims that cannot be supported. Never include secret values, local credentials, or environment contents.

## Keep both views

The Markdown context is for people and detailed reasoning. The bounded TOON projection is for fast routing and cross-session continuity. They describe the same project but serve different context budgets.

## Detect drift

Regenerate after architecture, build, test, or policy changes. Compare generation identity and evidence hashes. Stale context must be labelled stale rather than silently reused as current truth.
