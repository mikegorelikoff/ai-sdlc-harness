---
layout: default
title: Ship a first feature
description: Walk a small but meaningful feature through navigation, specification, implementation, validation, and commit preparation.
kicker: Tutorial · 20 minutes
permalink: /tutorials/first-feature/
nav_order: 3
---

This tutorial teaches the shortest complete delivery loop. Use a real low-risk feature in a disposable branch; the goal is to understand the evidence chain, not to manufacture paperwork.

## 1. Ask the navigator

```text
Use ai-sdlc-navigator --quick-flow.
I want to add a health endpoint to this service.
Inspect the repository and recommend the next required action.
```

Read the reasons, detected context, blockers, and expected artifact—not only the skill name. A recommendation without evidence is a guess.

## 2. Create the delivery contract

For a behavior change, use `ai-sdlc-sdd --quick-flow`. Define the observable requirement, design boundary, acceptance cases, QA scope, and implementation tasks before editing production code. Small work can have a small spec; it still needs a falsifiable outcome.

## 3. Implement one bounded task

Create a task branch whose name matches the spec. Change only the files named by the task. Mark the task complete only when the implementation and its focused tests actually satisfy the linked acceptance criteria.

## 4. Validate from risk

Use `ai-sdlc-validation --quick-flow` to select focused checks. A health endpoint usually needs transport tests, response-contract checks, and existing service regression—not an unrelated full infrastructure suite.

## 5. Prepare the commit

Run `ai-sdlc-commit-prep` with the task ID. It checks branch/spec alignment, staged scope, structural gates, and current validation. Then validate a conventional message that names the spec and exact checks.

You now have a small feature whose intent, implementation, test evidence, and commit can be reconstructed without the original chat.
