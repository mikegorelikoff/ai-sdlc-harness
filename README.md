# AI SDLC Harness

AI SDLC Harness is a repository-native operating system for software teams
working with AI agents. It turns requests, decisions, requirements, tests,
implementation tasks, validation, and handoffs into visible evidence that can
survive a chat, agent, or team change.

**[Read the guided documentation](https://mikegorelikoff.github.io/ai-sdlc-harness/)**

## Why this exists

An AI coding agent can produce code quickly, but speed alone does not answer:

- What customer or business outcome is this change meant to produce?
- Which decisions and assumptions shaped it?
- What may the agent change, and what still requires a person?
- Which requirements, tests, tasks, reviews, and commits belong together?
- How can another person or agent safely continue after an interruption?

Traditional software delivery answers these questions through the software
development lifecycle (SDLC). AI-assisted delivery needs the same disciplines,
but encoded so an agent can follow them repeatedly. That is AI SDLC.

The harness provides portable skill instructions, deterministic helper scripts,
human-readable Markdown artifacts, complete TOON state for agents, and explicit
gates. It does not replace engineering judgment; it makes the evidence behind
that judgment easier to create, inspect, hand off, and recover.

## Learn before you install

If these terms are new, begin here:

1. [What is AI SDLC?](docs/foundations/ai-sdlc.md)
2. [What is SDD?](docs/foundations/sdd.md)
3. [Why use a harness?](docs/foundations/why-harness.md)
4. [How the pieces fit together](docs/foundations/mental-model.md)
5. [Human and agent responsibilities](docs/foundations/responsibilities.md)

The short version:

```text
request -> evidence-backed requirement -> design -> bounded task
        -> implementation -> test evidence -> review -> traceable commit
```

Spec-driven development (SDD) means agreeing on observable behavior, design
boundaries, test cases, QA scope, and delivery tasks before implementation grows
beyond a safe guess. Small changes can use small specs; risky changes need more
evidence and stronger gates.

## Who it is for

Good fit:

- software teams already using Git and AI coding assistants;
- teams that want portable workflows instead of one vendor-specific chat;
- work where decisions, tests, reviews, or handoffs must remain inspectable;
- mixed PM, BA, QA, Delivery, Security, Architecture, and Dev collaboration;
- teams that want low-risk quick flows and stricter controls for high-risk work.

Poor fit or prerequisite gap:

- work that is not managed in a software repository;
- teams unwilling to review agent changes or preserve basic Git discipline;
- environments where an AI agent must autonomously approve or deploy changes;
- teams seeking a project-management system, CI platform, IDE, or correctness
  guarantee rather than a delivery workflow layer.

The harness supports accountable delivery. It is not a release authority,
compliance certification, hosted telemetry service, or substitute for product,
engineering, QA, security, or legal ownership.

## Install in a consumer repository

Prerequisites: Git, Node.js `>=22.20.0`/npm with `npx`, Python 3.10 or newer, a supported
AI agent, and a clean Git working tree in the project that will use the skills.

Run this from the **consumer project**, not from a clone of this source
repository. The pinned CLI version below is the version verified by these docs:

The third-party Skills CLI sends anonymous telemetry by default. These
privacy-safe commands opt out with `DISABLE_TELEMETRY=1`; review the
[upstream telemetry contract](https://www.skills.sh/docs/cli#telemetry) before
choosing a different policy. This installer boundary is separate from the
harness's content-free local metrics.

```bash
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0 --all
```

This is project-scoped because `-g` is intentionally absent. Review the files
reported by the CLI, then verify the installed inventory:

```bash
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
git status --short
python3 .agents/skills/ai-sdlc-navigator/scripts/navigate.py --help
python3 .agents/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help
```

The complete installation includes `ai-sdlc-shared-runtime`, which makes
deterministic helpers executable outside this source checkout. Both `--help`
commands must complete without an import traceback. Review and commit the
accepted installation baseline before starting feature work.

To inspect available skills before installing:

```bash
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0 --list
```

Network access to npm and GitHub is required for installation. An offline
source checkout can run repository tests and compatibility validation, but it
does not install skills into another project by itself.

See [Install the harness](docs/how-to/install.md) for scope, trust, update,
remove, and rollback details.

## First use

Tell your AI agent:

```text
Use ai-sdlc-navigator --quick-flow.
Inspect this repository and my request. Explain the evidence you found,
the smallest safe next action, expected artifact, blockers, and optional steps.

Request: add a health endpoint to this service.
```

The navigator is read-only. It should return a versioned handoff containing a
result, blockers, one required next action, optional actions, reasons, exact
invocations, and expected artifacts. A recommendation without repository
evidence is a blocker, not permission to guess.

Continue with [Your first 30 minutes](docs/onboarding/first-30-minutes.md) and
then the runnable [first feature tutorial](docs/tutorials/first-feature.md).

## How it works

| Layer | Purpose | Authority |
| --- | --- | --- |
| Skills | Tell the agent when and how to perform one bounded workflow. | Instructions; not evidence that work succeeded. |
| Helpers | Scaffold, parse, validate, index, migrate, and report deterministically. | Mechanical enforcement within declared inputs. |
| Markdown | Holds requirements, design, decisions, tests, QA, and plans for people. | Authoritative delivery detail. |
| TOON | Gives agents complete token-efficient state, indexes, plans, and results. | Machine projection; does not replace Markdown truth. |
| State and policy | Sequence work, explain gates, and preserve protected controls. | Fail closed where unsafe ambiguity could weaken a gate. |
| Humans | Own intent, risk acceptance, approvals, and accountable signoff. | Final decision authority. |

JSON remains at JSON Schema, external interoperability, exact recovery, and
JSONL journal boundaries. New agent-facing control-plane output is TOON-first.

## Choose the right amount of process

- `--quick-flow`: low-risk, bounded work with visible assumptions and focused
  validation.
- `--full-flow`: stricter execution of **one selected skill**, with questions,
  predecessor checks, traceability, and complete handoff evidence.
- Adaptive rigor: policy uses explicit risk factors to select patch, standard,
  assured, or regulated controls.
- Full lifecycle: an explicit sequence of many skills and role handoffs. It is
  not automatically triggered by writing `--full-flow` once.

When the entry point is unclear, use the navigator. When observable behavior or
architecture changes, use SDD. When you only need review or validation, enter
at that stage and reuse valid upstream evidence.

## Explore the system

- **Learn and use:** [Foundations](docs/foundations/index.md) →
  [Onboarding](docs/onboarding/index.md) →
  [Skills by role](docs/reference/skills-by-role.md) →
  [Tutorials](docs/tutorials/index.md).
- **Evaluate and adopt:** [fit decision](docs/adoption/index.md) →
  [bounded pilot](docs/adoption/pilot.md) →
  [metrics](docs/adoption/metrics.md) →
  [maturity and limitations](docs/explanation/maturity-limitations.md).
- [Tutorials](docs/tutorials/index.md): learn by completing delivery journeys.
- [Workflow map](docs/reference/workflow-map.md): lifecycle stages and handoffs.
- [Skill catalog](docs/reference/skills.md): complete operating guides for all installed capabilities.
- [Script catalog](docs/reference/scripts.md): every helper path, safe starting point, repository effect, and generated-mirror boundary.
- [How-to guides](docs/how-to/index.md): bounded operational procedures.
- [Operations](docs/operations/index.md): RACI, governance, incidents, troubleshooting, and recovery.
- [Maintainers](docs/maintainers/index.md): extend, validate, deprecate, release, and roll back.
- [Reference](docs/reference/index.md): paths, flags, schemas, and validation.

## Maintainer checkout

Clone this repository only when contributing to the harness, running its tests,
or previewing its documentation:

```bash
git clone https://github.com/mikegorelikoff/ai-sdlc-harness.git
cd ai-sdlc-harness
UV_CACHE_DIR=/tmp/ai-sdlc-uv-cache uv run --offline \
  --with-requirements requirements-docs.txt mkdocs serve
```

Validate a source checkout against the current release `1.2.0` compatibility baseline (this command skips the Git commit audit; the full `v1.1.0..HEAD` audit is documented in `docs/how-to/validate-release.md`):

```bash
python3 skills/_shared/ai_sdlc_compatibility.py \
  --skip-git-audit --format toon
```

Source checkout, installed agent environment, and consumer project are three
different contexts. The [mental model](docs/foundations/mental-model.md)
illustrates what belongs in each.

## Maturity and evidence

The repository has deterministic tests for skill contracts, state, generated
artifacts, compatibility, documentation, and recovery behavior. Those tests
show that the mechanisms behave as specified; they do not prove that every
team will reduce cycle time or defects. Treat organizational benefits as pilot
hypotheses, establish a baseline, and decide to scale or stop from local
evidence. Read [Evaluate and adopt](docs/adoption/index.md) and
[Maturity and limitations](docs/explanation/maturity-limitations.md) before
broad rollout.
