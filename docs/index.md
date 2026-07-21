---
title: AI SDLC Harness
description: Understand, evaluate, and use a repository-native operating system for software delivery with AI agents.
hide:
  - navigation
---

!!! warning "Main is a maintainer preview"

    This site is built from unreleased `main`. Stable consumer instructions
    install the immutable commit for `v1.2.0`. Use this site's exact-fetch
    installation erratum. The stable release installs, but its installed SDD
    helpers fail the complete consumer-relative workflow by resolving specs
    beneath `.agents/specs`. Use it only for historical comparison; evaluate
    the current candidate from a reviewed source checkout until a corrected
    release and versioned site exist.

## The problem in one minute

AI can generate code faster than teams can reconstruct why that code should
exist, which decisions shaped it, what proves it works, and who approved the
risk. Important context stays in chats, tickets, reviews, and individual memory.
When the session ends, the next person or agent rediscovers the work—or guesses.

The harness applies the software development lifecycle (SDLC) in a form AI
agents can follow. It gives them bounded skills, deterministic helpers, visible
artifacts, explicit state, and protected gates. Humans retain authority over
intent, trade-offs, exceptions, and approval.

```text
intent -> requirement -> design -> task -> code -> test -> evidence -> handoff
```

New to these ideas? Follow the [Foundations learning path](foundations/index.md),
which begins with software delivery, artificial intelligence, agents, and
skills before introducing AI-assisted SDLC and specification-driven
development (SDD).

## Choose your path

<div class="grid cards" markdown>

-   **I need to understand it**

    ---

    Learn SDLC, AI SDLC, SDD, artifacts, evidence, gates, and handoffs from
    first principles.

    [Start Foundations →](foundations/index.md)

-   **I want to use it**

    ---

    Install project-scoped skills, ask the navigator for a safe entry point,
    and complete a guided first session.

    [Start onboarding →](onboarding/index.md)

-   **I am evaluating adoption**

    ---

    Check fit, prerequisites, non-goals, authority boundaries, maturity, and
    the evidence you should require before a pilot.

    [Evaluate the harness →](adoption/index.md)

-   **I need an exact contract**

    ---

    Look up lifecycle stages, skills, scripts, schemas, routes, flags,
    compatibility, and validation commands.

    [Open Reference →](reference/index.md)

</div>

## What it is—and is not

| It is | It is not |
| --- | --- |
| Portable instructions for AI delivery workflows. | A new IDE or autonomous developer. |
| Deterministic helpers for repeatable repository mechanics. | A replacement for product, engineering, QA, security, or legal judgment. |
| Human-readable artifacts plus schema-complete state for the managed workflow. | A complete record of every project fact, decision, or external event. |
| Evidence-backed gates, handoffs, and recovery. | A guarantee of correctness, compliance, or business impact. |
| A layer that can complement Git, issue tracking, CI, and agent hosts. | A project-management system, CI platform, or deployment authority. |

## Go directly to what you need

The [Start page](start.md) owns the canonical first-use sequence. Returning
readers can find [skills by role](reference/skills-by-role.md) or open [Reference](reference/index.md)
for an exact contract without replaying onboarding.

The canonical project- and host-scoped installation sequence is:

```bash
HARNESS_REV=7f36bdbad73e1d73dd8ea2185f8b88c88c8f2dc2
HARNESS_TMP="$(mktemp -d)"
HARNESS_SRC="$HARNESS_TMP/ai-sdlc-harness"
PYTHON_BIN="${PYTHON_BIN:-python3}"
git init "$HARNESS_SRC"
git -C "$HARNESS_SRC" remote add origin https://github.com/mikegorelikoff/ai-sdlc-harness.git
git -C "$HARNESS_SRC" fetch --depth 1 origin "$HARNESS_REV"
git -C "$HARNESS_SRC" checkout --detach FETCH_HEAD
test "$(git -C "$HARNESS_SRC" rev-parse HEAD)" = "$HARNESS_REV"
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" --skill '*' --agent codex -y
mkdir -p .ai-sdlc
cp "$HARNESS_SRC/config/ai-sdlc-managed-skills.txt" .ai-sdlc/harness-managed-skills.txt
printf '{"schema":"ai-sdlc-install-record/v1","revision":"%s","skills_cli":"1.5.19","agent":"codex","selection":"all-skills","inventory":".ai-sdlc/harness-managed-skills.txt"}\n' "$HARNESS_REV" > .ai-sdlc/harness-install.json
"$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
rm skills-lock.json
rm -rf "$HARNESS_TMP"
```

Run it from the consumer repository only after reviewing the
[installation prerequisites, third-party installer telemetry, and trust
boundary](how-to/install.md). The opt-out applies to the Skills CLI; it does not
describe the independent data behavior of an agent host or model provider.
The pinned CLI requires Node.js `>=22.20.0`; verify `node --version` before
starting. Review and commit only `.agents/skills/` plus the portable install
records; the transient CLI lock contains the deleted temporary source path.

## What the evidence proves

Repository tests verify skill contracts, schemas, state transitions, generated
artifacts, compatibility, recovery, and documentation mechanics. This proves
the harness mechanisms behave as specified. It does **not** prove a causal
improvement in your cycle time, quality, or cost. Treat those outcomes as pilot
hypotheses and evaluate them with your own baseline and review.

[Begin with Foundations →](foundations/index.md){ .md-button .md-button--primary }
[Evaluate a bounded pilot →](adoption/index.md){ .md-button }
