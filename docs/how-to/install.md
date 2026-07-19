---
title: Install the harness
description: Install AI SDLC skills into a consumer repository, verify the result, and understand scope, trust, and rollback.
---

# Install the harness

This procedure installs agent skills into a project using the Skills CLI. It
does not copy this source repository into your application and it does not
create delivery artifacts until you ask an agent to use a workflow.

## Before you begin

You need:

- Git and a repository with a clean or understood working tree;
- Node.js/npm with `npx`;
- Python 3.10 or newer for deterministic helpers;
- network access to npm and GitHub during installation;
- a supported AI agent environment;
- permission to add project-scoped agent files.

Choose a low-risk consumer repository for your first use. The **consumer
repository** is the software project receiving skills. The **harness source
repository** is this GitHub project, used by maintainers and contributors.

## Inspect before installing

!!! terminal "Run in terminal — from the consumer repository"

    ```bash
    npx -y skills@1.5.19 add mikegorelikoff/ai-sdlc-harness --list
    ```

This lists available skills without installing them. Review the repository
origin and selected package names. Release `v1.1.0` is the current documented
harness release; the CLI version is pinned here so this procedure is
reproducible.

## Install project-scoped skills

!!! terminal "Run in terminal — from the consumer repository"

    ```bash
    npx -y skills@1.5.19 add mikegorelikoff/ai-sdlc-harness --all
    ```

`--all` selects every skill and every detected supported agent. Because `-g`
is absent, the intended scope is the current project. Review the CLI summary
before accepting any unexpected target.

For a smaller installation, omit `--all` and select exact skills/agents in the
interactive prompt, or use the CLI's `--skill` and `--agent` options. A useful
starter set is navigator, project context, SDD, validation, and commit prep;
installing all skills is easier when you want the navigator to expose every
role and control-plane path.

## Verify the result

!!! terminal "Run in terminal"

    ```bash
    npx -y skills@1.5.19 list --json
    git status --short
    python3 --version
    ```

Expected result:

- the list contains AI SDLC skill names;
- Git shows only the agent/skill files you intended to add;
- Python reports 3.10 or newer;
- no application source, secrets, or existing project artifacts were replaced.

!!! warning "Human checkpoint"

    Review the installed diff before committing it. Installation is not
    approval for an agent to modify product code, policy, or delivery evidence.

## Verify first use

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-navigator --quick-flow.
    Inspect this repository without modifying it. Report the detected context,
    one required next action, optional actions, reasons, expected artifacts,
    and blockers for this request: add a health endpoint.
    ```

Expected result: a read-only `ai-sdlc-handoff/v1` recommendation grounded in
repository evidence. If the agent cannot find the skill, verify the target
agent and installation scope with `skills list` before reinstalling.

## Update, remove, or roll back

!!! terminal "Run in terminal"

    ```bash
    npx -y skills@1.5.19 update
    npx -y skills@1.5.19 remove
    ```

Review updates like source changes. Preserve project-owned specs, decisions,
state, configuration, and evidence. Removing an installed skill must not delete
artifacts it previously helped create. For version compatibility and schema
recovery, follow [Update safely](update.md) and [Migrate to 1.1](migrate-1.1.md).

## Offline and private environments

The Skills CLI installation path requires registry and Git access. In an
offline environment, prepare and review a pinned package mirror through your
organization's approved supply-chain process. A local harness checkout can run
tests and compatibility validation, but this documentation does not claim that
cloning alone installs skills into another agent environment.

For a private repository, configure an SSH key, GitHub CLI login, or approved
HTTPS credential with read access. Never paste tokens into an agent prompt.
