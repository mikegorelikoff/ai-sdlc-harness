---
title: Lead developer guide
description: Govern technical scope, review quality, incorrect artificial intelligence output, and safe integration.
---

# Lead developer guide

This guide uses continuous integration (CI).

## Why you should care

You decide whether the harness reduces rework or adds ceremony. Your review
protects architecture, maintainability, test quality, and safe integration when
artificial intelligence (AI) output is plausible but incomplete.

## Where you participate

Select rigor with product and security peers, review Specification-driven
development (SDD) design and task
boundaries, challenge generated code and tests, resolve technical findings, and
confirm pull-request and merge evidence.

## Inputs and outputs

Inputs: accepted scope, architecture constraints, risk profile, diff, tests,
validation, and open decisions. Outputs: technical decisions, review findings,
required corrections, merge recommendation, and recorded residual risk.

## Decisions you own

Own technical direction within delegated architecture authority, coding and
test standards, engineering review disposition, and recommendation to merge.
Do not accept product, legal, security, or production risk on behalf of others.

## Common mistakes

- Reviewing only the diff rather than the accepted requirement and exclusions.
- Allowing tests written by the same agent to be the only evidence.
- Treating task completion in a machine projection as more authoritative than
  the reviewed Markdown and implementation.
- Merging with stale CI or unresolved blocking findings.

## Example workflow

Review the SDD before implementation expands. After implementation, compare the
requirement-to-test-to-task trace, inspect the full diff, rerun focused tests,
request independent security or quality assurance (QA) review, require resolved findings, then use
[Open, review, and merge](../how-to/review-and-merge.md).

## Review checklist

- Architecture decisions and alternatives are explicit.
- Scope is no larger than the accepted tasks.
- Incorrect-output and failure recovery were exercised where risk warrants.
- CI and local evidence refer to the reviewed commit.
- Blocking findings are closed with evidence, not merely answered.
- Rollback and post-merge validation are proportionate to impact.
