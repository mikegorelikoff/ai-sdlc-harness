---
title: Set up Codex CLI
description: Install, authenticate, open a consumer repository, and verify the Codex host used by the documented pilot path.
---

# Set up Codex CLI

Use this guide when Codex is the agent host selected for the documented pilot.
Codex is separate from the harness and from the third-party Skills CLI: Codex
runs the agent session, while the Skills CLI copies harness skills into the
consumer repository.

## Prerequisites and data boundary

You need Node.js and npm, a supported ChatGPT account or an approved OpenAI API
credential, and permission to send the selected repository context to the
configured OpenAI service. Before login, confirm your organization's approved
account, data classification, retention, network, and repository rules. Never
paste a secret, API key, customer record, or production credential into a
prompt.

The current official Codex CLI documentation is the authority for product
installation and authentication behavior. This repository manually exercised
Codex CLI `0.144.1`; newer versions are candidates until the first workflow is
revalidated.

## Install and verify the host

Run in a terminal, outside an agent conversation:

```bash
npm install --global @openai/codex@0.144.1
codex --version
```

Expected: the first command completes without an npm error and the second
prints exactly `codex-cli 0.144.1`. Verify it in a POSIX-compatible shell with
`test "$(codex --version)" = "codex-cli 0.144.1"`. A different version is a
candidate: stop and revalidate the first workflow before treating it as
supported. If your organization uses a package mirror, install
through that reviewed mirror. Do not use `sudo` merely to bypass a permissions
error; repair the approved Node/npm installation or ask the workstation owner.

## Authenticate

Start the documented browser sign-in and then verify status:

```bash
codex login
codex login status
```

Expected: `codex login` opens or prints the browser authentication flow and the
status command confirms an authenticated session. If a browser cannot open,
follow the device or alternative login flow printed by the current official
CLI; do not copy a token into chat, shell history, documentation, or Git.

An API-key login is an organizational choice, not the default in this guide.
If policy requires it, use the official non-interactive login method and a
secret manager or protected standard input. Never put a key directly in a
command argument or repository environment file.

## Open the consumer repository

Change to the software project that received `.agents/skills/`, verify the
boundary, and launch Codex:

```bash
cd /path/to/your-consumer-repository
git rev-parse --show-toplevel
git status --short
codex
```

Expected: Git prints the intended repository root, the status is clean or
understood, and Codex opens its terminal interface for that repository. Review
the host's permission/sandbox prompt before granting tool access. Installation
of a skill does not authorize shell commands, file writes, network access,
commits, pushes, deployment, or access to secrets.

Enter this first read-only prompt in the Codex interface:

```text
Use ai-sdlc-navigator --quick-flow.
Inspect this repository without modifying it. Report the repository evidence,
smallest safe next action, expected artifact, blockers, and optional actions.
Request: add a health endpoint.
```

Expected: a grounded `ai-sdlc-handoff/v1` response and no working-tree change.
Confirm with `git status --short` in a terminal. Stop if the skill is not found,
the agent opens the wrong repository, or any file changes during this read-only
step.

## Troubleshooting and recovery

| Symptom | Safe response and expected result |
| --- | --- |
| `codex: command not found` | Run `npm prefix --global`, correct the approved npm executable path, and rerun `codex --version`; expected: one version line. |
| Login does not complete | Cancel, run `codex login` once, and follow only the official flow it prints; escalate proxy, account, or policy failures to the owner. |
| Wrong repository opened | Exit Codex, `cd` to the consumer root, verify `git rev-parse --show-toplevel`, and relaunch. |
| Skill not found | Verify `.agents/skills/ai-sdlc-navigator/SKILL.md` and the project-scoped inventory from [Install](install.md); do not switch to a global install as a shortcut. |
| Unexpected file or command request | Deny the action, inspect `git status --short`, and review the host permission plus [security model](../operations/governance.md). |

The authoritative product references are the official
[Codex CLI guide](https://learn.chatgpt.com/docs/codex/cli) and
[authentication guide](https://learn.chatgpt.com/docs/auth.md). Continue with
[Your first 30 minutes](../onboarding/first-30-minutes.md) only after the
read-only result and clean status are verified.
