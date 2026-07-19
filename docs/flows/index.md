---
title: Workflow journeys
description: Choose the right AI SDLC entry point and follow explicit evidence, gate, handoff, and recovery paths.
---

# Workflow journeys

A flow connects bounded skills. Enter at the earliest stage whose required
evidence is missing, and reuse valid upstream work. Do not run every skill just
because it exists.

## Choose from the signal you have

| Starting signal | Begin with | Typical path |
| --- | --- | --- |
| New idea or unclear customer problem | Working-backwards discovery | [Complete refinement](refinement.md) or a bounded discovery package |
| Clear small behavior change | Navigator, task branch, then proportionate SDD | [Implementation](implementation.md) |
| Existing repository with implicit conventions | Project context, then navigator | [Adopt an existing project](../tutorials/existing-project.md) |
| Bug with reproducible expected behavior | Navigator, task branch, then tests or SDD depending contract impact | [Implementation](implementation.md) |
| Review-only request | Code review or security testing | Validation/review branch in [Implementation](implementation.md) |
| Security-sensitive feature | Navigator with risk stated; full SDD/security | Refinement + implementation with Security checkpoints |
| Requirement changed after work began | Change set and impact analysis | [Control plane](control-plane.md) and [Recovery](recovery.md) |
| Interrupted multi-task run | Runtime resume | Runtime branch in [Control plane](control-plane.md) |
| Release/update problem | Doctor and upgrade preview | Operations branch in [Control plane](control-plane.md) |
| Learning or process improvement | Retrospective | [Recovery and learning](recovery.md) |

## Four concepts that are easy to confuse

- **Quick flow:** low-risk behavior inside one selected skill.
- **Full flow:** strict behavior inside one selected skill.
- **Adaptive rigor:** policy-selected strength of controls from explicit risk.
- **Complete lifecycle:** explicit sequence of many skills and handoffs.

`--full-flow` does not mean “run the entire lifecycle.” The user or a declared
workflow must request the full cascade.

## Flow contracts

Every flow page names:

- entry signal and required evidence;
- accountable humans and participating agent skills;
- ordered stages and output paths;
- mutation and approval boundaries;
- completion gate and next consumer;
- reasons to reopen or recover.

Use [Complete refinement](refinement.md), [Implementation](implementation.md),
[Control plane](control-plane.md), and [Recovery and learning](recovery.md) for
the exact branches.
