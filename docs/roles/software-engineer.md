---
title: Software engineer guide
description: Use specifications, tests, validation, and review to deliver one bounded change.
---

# Software engineer guide

This guide uses artificial intelligence (AI) and Specification-driven development (SDD).

## Why you should care

The harness bounds AI generation with accepted behavior, explicit tasks, and
fresh evidence, making code review and interrupted-work recovery easier.

## Where you participate

Engineers inspect repository context, create the task branch, write or consume
the SDD package, derive tests, implement listed tasks, validate, resolve review
findings, and prepare an auditable change.

## Inputs and outputs

Inputs: accepted requirement, repository policy, affected surface, risks, and
available validation commands. Outputs: design decisions, tasks, implementation,
tests, current validation, review resolution, and commit or pull-request evidence.

## Decisions you own

Own technical design recommendations, implementation choices within accepted
scope, test coverage, and engineering-risk escalation. Product scope, security
risk acceptance, and release authority remain with their named owners.

## Common mistakes

- Starting code before observable behavior and exclusions are agreed.
- Expanding beyond `tasks.md` without updating the specification.
- Running only happy-path tests or trusting the agent's report of a command.
- Repairing a generated projection instead of its authoritative source.

## Example workflow

`navigator → branching → SDD → test cases → implementation → validation → code
review → security review when applicable → commit preparation → pull request`.
If output is wrong, preserve the diff, reopen the earliest stale contract,
repair the smallest surface, and rerun downstream checks.

## Review checklist

- Requirement, design, test, task, and decision IDs agree.
- Every changed path maps to an accepted task.
- Negative, regression, and relevant non-functional cases are covered.
- Validation ran on the exact revision under review.
- Residual risks and skipped checks are explicit.
- The pull request contains no secret, cache, or unrelated generated content.
