---
title: Start here
description: Install the harness and route your first piece of work in a few deliberate steps.
---

The harness is a library of repository-local skills, scripts, and evidence contracts. You bring it into a project, then ask your AI assistant to use the workflow that matches the work in front of you.

!!! tip "Adopt only what you need"

    Start with navigation, validation, or one role-specific workflow. The artifacts remain compatible as your use expands.

## Install

1. **Clone the library.** Keep a local source checkout so updates remain explicit and reviewable.
2. **Install into a project.** Copy the skill packages and shared runtime using the repository installer.
3. **Ask for the next action.** Use the navigator when you know the goal but not the correct lifecycle entry point.

```bash
git clone https://github.com/mikegorelikoff/ai-sdlc-harness.git
cd ai-sdlc-harness
./scripts/install.sh /path/to/your-project
```

For update modes, compatibility behavior, and installation layout, read the [complete install and update guide](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/guides/install-and-update.md).

## Route the first request

Give your assistant a concrete request and name the navigator:

```text
Use ai-sdlc-navigator --quick-flow.
I need to add organization-level SSO to this service.
Inspect the repository context and tell me the smallest safe next action.
```

The response should include detected context, a required next action, optional actions, reasons, exact commands, expected artifacts, and blockers.

## Choose a flow mode

| Mode | Best for | Behavior |
| --- | --- | --- |
| `--quick-flow` | Low-risk, well-bounded work | Makes documented assumptions and runs focused checks. |
| `--full-flow` | Ambiguous, high-risk, or signoff-sensitive work | Stops on missing decisions and verifies the complete handoff chain. |
| Adaptive rigor | Teams using policy profiles | Explains risk factors and selects patch, standard, assured, or regulated controls. |

Explicit quick or full flow always wins over automatic selection. Organization minimums can raise rigor, but customization cannot silently weaken protected gates.

## Pick a direct entry point

You can skip navigation when the need is already clear:

- Product discovery: `ai-sdlc-working-backwards-discovery`
- Requirements and design: `ai-sdlc-sdd`
- Test design: `ai-sdlc-test-cases`
- QA acceptance: `ai-sdlc-qa`
- Change validation: `ai-sdlc-validation`
- Review: `ai-sdlc-code-review`
- Commit preparation: `ai-sdlc-commit-prep`

Next, see how these entry points connect in the [workflow map](reference/workflow-map.md).
