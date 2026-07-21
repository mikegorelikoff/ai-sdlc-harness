---
title: Adopt an existing project
description: Introduce the harness without overwriting established conventions, inventing history, or forcing an organization-wide rollout.
---

# Adopt an existing project

This tutorial uses continuous integration (CI) and an artificial
intelligence-assisted software development lifecycle (AI SDLC), including
Specification-driven development (SDD).

An established repository already has a delivery system: Git conventions, CI,
owners, release habits, architecture rules, and undocumented assumptions.
Adoption begins by observing that system, not replacing it with generic defaults.

## 1. Define the pilot boundary

Choose one team, one repository, one low-to-medium-risk change, and an informed
reviewer. Name the accountable owner, what is being evaluated, which existing
process remains authoritative, and conditions that will stop or roll back the
pilot.

Do not backfill fictional AI SDLC history for completed work.

## 2. Install project-scoped skills

Follow [Install the harness](../how-to/install.md). Review the installed diff
and preserve existing agent instructions, CI, templates, ownership, policy, and
project artifacts unless the team explicitly accepts a change.

## 3. Build evidence-backed repository context

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-project-context --quick-flow.
    Profile this repository from evidence. Cite exact paths for stack,
    architecture, test commands, ownership, security boundaries, generated
    code, and delivery conventions. Mark unknown facts unknown. Do not infer
    policy or product behavior from filenames alone.
    ```

Expected: a bounded project-context artifact and drift identity. Secrets,
credentials, environment files, binaries, and configured sensitive paths must
be excluded.

## 4. Compare the profile with human knowledge

!!! warning "Human checkpoint"

    Repository owners review the profile. Correct missing evidence at its
    authoritative source; do not teach the agent a private fact only in chat and
    call the project documented.

Classify mismatches:

- evidence is present but the profile missed it;
- the convention is real but undocumented;
- the convention is only historical and should not govern new work;
- a material decision is required.

## 5. Navigate the pilot request

Ask the read-only navigator for the earliest missing stage. Reuse existing valid
requirements, designs, tests, or tickets; do not recreate artifacts merely to
match a template. If observable behavior changes and no implementation contract
exists, create a proportionate SDD.

## 6. Preserve existing gates

Quick flow can reduce ceremony but cannot weaken protected repository policy.
Keep required reviewers, CI checks, security controls, release approvals, and
branch rules. Add harness evidence alongside them and compare whether it reduces
rediscovery or exposes gaps earlier.

## 7. Review and decide

After the pilot, inspect artifacts, agent retries, validation gaps, review
rework, handoff delay, escaped issues, and qualitative team feedback. Separate
mechanism signals from business outcomes and avoid claiming causality from one
change.

Scale only with an explicit decision, owner, support plan, and rollback. If the
pilot adds overhead without useful continuity or control, remove installed
skills while preserving the delivery evidence already created.
