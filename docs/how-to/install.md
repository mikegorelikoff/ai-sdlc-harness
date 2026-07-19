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
- Node.js `>=22.20.0`/npm with `npx`;
- Python 3.10 or newer for deterministic helpers;
- network access to npm and GitHub during installation;
- a supported AI agent environment;
- permission to add project-scoped agent files.

Choose a low-risk consumer repository for your first use. The **consumer
repository** is the software project receiving skills. The **harness source
repository** is this GitHub project, used by maintainers and contributors.

The shell blocks below use POSIX syntax (Linux, macOS, WSL, or Git Bash). In
PowerShell, set the opt-out once in the session and run the same pinned CLI:

```powershell
$env:DISABLE_TELEMETRY = "1"
node --version  # expected: v22.20.0 or newer
npx -y skills@1.5.19 add https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0 --all
npx -y skills@1.5.19 list --json
```

Do not paste the PowerShell environment assignment into a POSIX shell; use the
`DISABLE_TELEMETRY=1` prefix shown in the POSIX blocks instead.

## Decide the installer telemetry boundary

The third-party Skills CLI is separate from the harness. Its
[official CLI documentation](https://www.skills.sh/docs/cli#telemetry) says
that it sends anonymous telemetry by default, including the skill name, skill
files, and a timestamp. The harness's content-free local metrics do not send
network requests, but that property does not cover npm, GitHub, the Skills CLI,
your agent host, or model provider.

The canonical commands below set `DISABLE_TELEMETRY=1`. Keep that privacy-safe
default unless a human data/privacy owner explicitly accepts the upstream
collection and retention policy. `DO_NOT_TRACK=1` is also supported upstream;
use the form required by your organization consistently.

## Inspect before installing

!!! terminal "Run in terminal — from the consumer repository"

    ```bash
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0 --list
    ```

Before this command, run `node --version` and stop unless it reports
`v22.20.0` or newer. `npm view skills@1.5.19 engines --json` is the recovery
check when a pinned CLI invocation reports an engine mismatch.

This lists available skills without installing them. Review the repository
origin and selected package names. Release `v1.2.0` is the current documented
harness release; the CLI version is pinned here so this procedure is
reproducible.

## Install project-scoped skills

!!! terminal "Run in terminal — from the consumer repository"

    ```bash
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0 --all
    ```

`--all` selects every capability—including the portable shared runtime—and
every detected supported agent. Because `-g` is absent, the intended scope is
the current project. Review the CLI summary before accepting any unexpected
target.

For a smaller installation, omit `--all` and select exact skills/agents in the
interactive prompt, or use the CLI's `--skill` and `--agent` options. A useful
starter set is shared runtime, navigator, project context, SDD, validation, and commit prep;
installing all skills is easier when you want the navigator to expose every
role and control-plane path. Any selected helper-backed skill must be installed
with `ai-sdlc-shared-runtime`; a skill inventory without its runtime is not a
healthy installation.

## Verify the result

!!! terminal "Run in terminal"

    ```bash
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
    git status --short
    python3 --version
    python3 .agents/skills/ai-sdlc-navigator/scripts/navigate.py --help
    python3 .agents/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help
    ```

Expected result:

- the list contains AI SDLC skill names;
- Git shows only the agent/skill files you intended to add;
- Python reports 3.10 or newer;
- navigator and SDD helper usage render without an import traceback;
- no application source, secrets, or existing project artifacts were replaced.

!!! warning "Human checkpoint"

    Review and commit the accepted installation baseline before starting a
    feature branch. Installation is not approval for an agent to modify product
    code, policy, or delivery evidence.

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
agent and installation scope with `DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json`
before reinstalling.

## Update, remove, or roll back

!!! terminal "Run in terminal"

    ```bash
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 update
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 remove
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
