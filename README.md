# AI SDLC Harness

The Artificial Intelligence (AI) Software Development Lifecycle (SDLC) Harness
is a repository-native operating system for software teams working with AI
agents. It turns requests, decisions, requirements, tests,
implementation tasks, validation, and handoffs into visible evidence that can
survive a chat, agent, or team change.

**[Read the guided documentation](https://mikegorelikoff.github.io/ai-sdlc-harness/)**

> **Release status:** `v2.0.0-rc.1` is the current release candidate. It fixes
> the installed consumer-root defect in `v1.2.0`, hardens skill/runtime trust
> boundaries, and introduces context contract v3 plus Harness API `2.0.0`.
> It remains a prerelease because this repository has no owner-selected license
> and protected remote CI must still be verified. The tag does not grant rights
> absent a license; evaluate it in a bounded pilot and review the
> [release notes](docs/reference/release-2.0.md) before adoption.

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
human-readable Markdown artifacts, complete Token-Oriented Object Notation
(TOON) state for agents, and explicit
gates. It does not replace engineering judgment; it makes the evidence behind
that judgment easier to create, inspect, hand off, and recover.

## Learn before you install

If these terms are new, begin here:

1. [Git and terminal primer](docs/foundations/git-and-terminal-primer.md)
2. [Software delivery foundations](docs/foundations/software-delivery.md)
3. [Artificial intelligence foundations](docs/foundations/ai-foundations.md)
4. [Agents, sub-agents, and skills](docs/foundations/agents-and-skills.md)
5. [What is AI SDLC?](docs/foundations/ai-sdlc.md)
6. [What is SDD?](docs/foundations/sdd.md)
7. [Why use a harness?](docs/foundations/why-harness.md)
8. [How the pieces fit together](docs/foundations/mental-model.md)
9. [Human and agent responsibilities](docs/foundations/responsibilities.md)

The short version:

```text
request -> evidence-backed requirement -> design -> bounded task
        -> implementation -> test evidence -> review -> traceable commit
```

Specification-driven development (SDD) means agreeing on observable behavior, design
boundaries, test cases, quality assurance (QA) scope, and delivery tasks before implementation grows
beyond a safe guess. Small changes can use small specs; risky changes need more
evidence and stronger gates.

## Who it is for

Good fit:

- software teams already using Git and AI coding assistants;
- teams that want portable workflows instead of one vendor-specific chat;
- work where decisions, tests, reviews, or handoffs must remain inspectable;
- mixed product manager (PM), business analyst (BA), QA, delivery, security,
  architecture, and developer (Dev) collaboration;
- teams that want low-risk quick flows and stricter controls for high-risk work.

Poor fit or prerequisite gap:

- work that is not managed in a software repository;
- teams unwilling to review agent changes or preserve basic Git discipline;
- environments where an AI agent must autonomously approve or deploy changes;
- teams seeking a project-management system, continuous integration (CI)
  platform, integrated development environment (IDE), or correctness
  guarantee rather than a delivery workflow layer.

The harness supports accountable delivery. It is not a release authority,
compliance certification, hosted telemetry service, or substitute for product,
engineering, QA, security, or legal ownership.

## Install in a consumer repository

Prerequisites: Git, Node.js `>=22.20.0`/npm with `npx`, Python 3.10 or newer, a
candidate agent host selected for a bounded pilot, and a clean Git working tree
in the project that will use the skills.

Run this from the **consumer project**, not from a clone of this source
repository. The pinned CLI version below is the version verified by these docs:

The third-party Skills CLI sends anonymous telemetry by default. These
privacy-safe commands opt out with `DISABLE_TELEMETRY=1`; review the
[upstream telemetry contract](https://www.skills.sh/docs/cli#telemetry) before
choosing a different policy. This installer boundary is separate from the
harness's content-free local metrics.

```bash
HARNESS_TAG=v2.0.0-rc.1
HARNESS_TMP="$(mktemp -d)"
HARNESS_SRC="$HARNESS_TMP/ai-sdlc-harness"
git init "$HARNESS_SRC"
git -C "$HARNESS_SRC" remote add origin https://github.com/mikegorelikoff/ai-sdlc-harness.git
git -C "$HARNESS_SRC" fetch --depth 1 origin "refs/tags/$HARNESS_TAG:refs/tags/$HARNESS_TAG"
git -C "$HARNESS_SRC" checkout --detach "$HARNESS_TAG^{commit}"
HARNESS_REV="$(git -C "$HARNESS_SRC" rev-parse HEAD)"
test "$(git -C "$HARNESS_SRC" rev-list -n 1 "$HARNESS_TAG")" = "$HARNESS_REV"
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" --list
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" --skill '*' --agent codex -y
```

The fetch resolves the annotated release tag to one exact commit before the
local checkout is passed to Skills CLI `1.5.19`; the resolved commit is stored
in the portable install record. The install is project-scoped because `-g` is
absent and host-scoped to the manually validated `codex` target. Review the
files reported by the CLI, then verify the installed inventory:

```bash
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
git status --short
PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" --version
"$PYTHON_BIN" .agents/skills/ai-sdlc-navigator/scripts/navigate.py --help
"$PYTHON_BIN" .agents/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help
mkdir -p .ai-sdlc
cp "$HARNESS_SRC/config/ai-sdlc-managed-skills.txt" .ai-sdlc/harness-managed-skills.txt
printf '{"schema":"ai-sdlc-install-record/v1","revision":"%s","skills_cli":"1.5.19","agent":"codex","selection":"all-skills","inventory":".ai-sdlc/harness-managed-skills.txt"}\n' "$HARNESS_REV" > .ai-sdlc/harness-install.json
"$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
rm skills-lock.json
rm -rf "$HARNESS_TMP"
```

The complete installation includes `ai-sdlc-shared-runtime`, which makes
deterministic helpers executable outside this source checkout. Both `--help`
commands must complete without an import traceback. The generated CLI lock
contains the absolute temporary source path, so record portable identity and
remove the lock as shown. Review and commit only `.agents/skills/` and the two
portable `.ai-sdlc/harness-*` records before feature work.

For a workstation-wide Codex installation, keep the agent target explicit:

```bash
mkdir -p "$HOME/.codex/skills"
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" --skill '*' --agent codex --global --copy -y
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --global --agent codex
```

Do not replace `--skill '*'` with `--all`. In the third-party CLI, `--all`
means all skills **and all recognized agents**. Some recognized targets,
including Eve and PromptScript in CLI `1.5.19`, have no global installation
location, so `--all --global` reports two failures for every harness skill.
Pre-creating Codex's directory also avoids the pinned CLI's clean-home linking
bug; verification must list `Codex` for each skill, not an empty agent list.
See the [full installation scope guidance](docs/how-to/install.md#optional-install-globally-for-codex).

Network access to npm and GitHub is required for installation. An offline
source checkout can run repository tests and compatibility validation, but it
does not install skills into another project by itself.

See [Install the harness](docs/how-to/install.md) for scope, trust, update,
remove, and rollback details. If Codex is your host, complete
[Set up Codex CLI](docs/how-to/setup-codex.md) before first use.

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
| TOON | Gives agents schema-complete, token-efficient managed-workflow state, indexes, plans, and results. | Machine projection; does not contain every project fact or replace Markdown truth. |
| State and policy | Sequence work, explain gates, and preserve protected controls. | Fail closed where unsafe ambiguity could weaken a gate. |
| Humans | Own intent, risk acceptance, approvals, and accountable signoff. | Final decision authority. |

JavaScript Object Notation (JSON) remains at JSON Schema, external
interoperability, exact recovery, and JSON Lines (JSONL) journal boundaries.
New agent-facing control-plane output is TOON-first.

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
UV_CACHE_DIR=/tmp/ai-sdlc-uv-cache uv run \
  --with-requirements requirements-docs.lock mkdocs serve
```

The first run requires package-index access. After that command has populated
the named cache, add `--offline` for repeatable offline previews. Starting with
`--offline` in a clean cache fails because the pinned documentation dependency
has not been downloaded yet.

Validate a source checkout against the current `2.0.0-rc.1` compatibility
baseline (this command skips the Git commit audit; the full `v1.2.0..HEAD`
audit is documented in `docs/how-to/validate-release.md`):

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
