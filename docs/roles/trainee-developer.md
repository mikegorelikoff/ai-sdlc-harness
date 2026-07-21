---
title: Trainee developer guide
description: Complete a first artificial-intelligence-assisted change without relying on unexplained expert knowledge.
---

# Trainee developer guide

This guide uses artificial intelligence (AI).

## Why you should care

The harness teaches you to turn a request into reviewed evidence instead of
accepting plausible AI output. It also gives you a recovery path when a command,
test, or generated change is wrong.

## Where you participate

Start with [Foundations](../foundations/index.md), install in a disposable
consumer repository, ask the read-only navigator for one next action, and follow
the [first feature tutorial](../tutorials/first-feature.md) with a mentor review
at every human checkpoint.

## Inputs and outputs

Inputs: one small request, a clean Git repository, supported prerequisites, and
a named reviewer. Outputs: a task branch, small specification, tests, code,
validation evidence, reviewed commit, and a record of anything not understood.

## Decisions you own

You own whether you understand a step and whether to stop. You do not silently
approve product scope, security risk, production access, or a command you cannot
explain. Escalate those decisions to the named owner.

## Common mistakes

- Pasting an agent instruction into a terminal.
- Continuing after a prerequisite version check fails.
- Treating generated text or a green structural check as proof of correctness.
- Using broad staging without reviewing generated files.
- Hiding confusion instead of recording a question or blocker.

## Example workflow

1. Verify Git, Node.js, npm, Python, network, and agent host.
2. Install project-scoped skills and inspect every created path.
3. Ask `ai-sdlc-navigator --quick-flow` to route one low-risk request.
4. Create a task branch, specification, tests, and implementation in that order.
5. Run the exact validation, introduce the tutorial failure, and recover it.
6. Ask a lead or mentor to review the diff and evidence before merge.

## Review checklist

- I can explain the request, acceptance criteria, and exclusions.
- I know which text is a prompt and which text is a shell command.
- My prerequisite versions meet the documented minimums.
- Tests failed when the deliberate defect existed and passed after repair.
- I reviewed the diff and no cache, secret, or unrelated file is staged.
- A named reviewer approved the exact revision.
