# AI SDLC Harness

AI SDLC Harness is a small, repository-native operating system for building
software with AI agents. It gives teams repeatable skills, specifications,
plans, tests, validation evidence, and human approval points.

It is designed to make AI-assisted delivery easier to understand, review, and
resume—not to replace engineering judgment or product ownership.

[Documentation](https://mikegorelikov.github.io/ai-sdlc-harness/) ·
[Start learning](https://mikegorelikov.github.io/ai-sdlc-harness/start/) ·
[Install guide](docs/how-to/install.md) ·
[Skills catalog](docs/reference/skills.md)

## What you get

- A clear path from request → specification → plan → implementation → tests →
  review → commit.
- Reusable skills for product discovery, business analysis, SDD, coding,
  QA, security, release, and recovery.
- Deterministic scripts that scaffold and validate artifacts.
- Markdown records for people plus compact TOON state for agents.
- Explicit boundaries for secrets, permissions, generated output, and human
  decisions.

## Is it for you?

Use it when your team already works in Git and wants AI work to remain
traceable across chats, agents, and handoffs. It works for developers, QA,
product, business analysis, delivery, platform, and security roles.

It is not an IDE, project-management system, deployment platform, compliance
certification, or guarantee that AI output is correct. Every generated change
still needs a human-owned review and validation decision.

## Quick start

### 1. Install into a project

Run the following from the project that will use the skills. Keep the install
project-scoped while evaluating the harness.

Prerequisites: Git, Node.js `>=22.20.0`, npm, Python `3.10+`, and an AI agent
host. The harness is tool-agnostic; choose an agent host supported by your
installer (for example Claude Code, Codex, Cursor, or another Skills CLI
target). The short command below shows the host flag; replace `codex` with
your target:

```bash
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add \
  mikegorelikoff/ai-sdlc-harness --skill '*' --agent codex -y
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
```

Replace `codex` with your supported host. Review the installed files before
using an agent. Keep the install
project-scoped while evaluating the harness.

<details>
<summary>Reproducible pinned install (optional)</summary>

Use this when you need to pin one release tag and record its exact commit:

```bash
HARNESS_TAG=v2.1.0
HARNESS_TMP="$(mktemp -d)"
HARNESS_SRC="$HARNESS_TMP/ai-sdlc-harness"
git init "$HARNESS_SRC"
git -C "$HARNESS_SRC" remote add origin https://github.com/mikegorelikoff/ai-sdlc-harness.git
git -C "$HARNESS_SRC" fetch --depth 1 origin "refs/tags/$HARNESS_TAG:refs/tags/$HARNESS_TAG"
git -C "$HARNESS_SRC" checkout --detach "$HARNESS_TAG^{commit}"
HARNESS_REV="$(git -C "$HARNESS_SRC" rev-parse HEAD)"
test "$(git -C "$HARNESS_SRC" rev-list -n 1 "$HARNESS_TAG")" = "$HARNESS_REV"
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" \
  --skill '*' --agent codex -y
# Canonical project-scoped form:
# DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" --skill '*' --agent codex -y
# Historical validation baseline: HARNESS_TAG=v2.0.0-rc.1
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
rm -rf "$HARNESS_TMP"
```

</details>

For a complete install record, update, rollback, and host-specific setup, see
[Install the harness](docs/how-to/install.md).

### 2. Global installs are host-specific

Global skill directories and permissions differ by host. Select exactly one
host and follow its documented global directory. For example, Codex uses:

```bash
mkdir -p "$HOME/.codex/skills"
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" \
  --skill '*' --agent codex --global --copy -y
```

Do not combine `--all` with `--global`: `--all` asks the CLI to install into
every recognized agent, including hosts that do not support global skill
installation. Install locally when a host has no global directory. See the
[global installation notes](docs/how-to/install.md#optional-install-globally-for-codex)
and the host-specific sections for other agents.

### 3. Run your first request

Start with the read-only navigator:

```text
Use ai-sdlc-navigator --quick-flow.
Inspect this repository and my request. Report the evidence you found,
the smallest safe next action, expected artifact, blockers, and validation.

Request: add a health endpoint to this service.
```

Then follow [Your first 30 minutes](docs/onboarding/first-30-minutes.md) and
the [first feature tutorial](docs/tutorials/first-feature.md).

## The basic workflow

```text
request
  ↓
discovery and requirements
  ↓
specification and acceptance criteria
  ↓
design, plan, and tasks
  ↓
bounded implementation
  ↓
tests, security checks, and review
  ↓
validated commit and handoff
```

Use `--quick-flow` for low-risk, bounded work. Use `--full-flow` when you need
questions, predecessor checks, traceability, and a complete handoff. For a
medium or large change, use [specification-driven development (SDD)](docs/foundations/sdd.md).

## Where to go next

- **New to AI or SDLC:** [Learning hub](docs/start.md)
- **First installation:** [Install](docs/how-to/install.md)
- **Evaluate a team rollout:** [Onboarding](docs/onboarding/index.md)
- **First feature:** [Tutorials](docs/tutorials/index.md)
- **Choose a workflow:** [Workflow map](docs/reference/workflow-map.md)
- **Find a skill:** [Skills by role](docs/reference/skills-by-role.md)
- **Understand the model:** [System model](docs/explanation/system-model.md)
- **Adopt with a team:** [Pilot and adoption](docs/adoption/index.md)
- **Operate and recover:** [Operations](docs/operations/index.md)
- **Extend or release:** [Maintainer guide](docs/maintainers/index.md)

## Contributing

Before changing the harness, read [Contributing](CONTRIBUTING.md), the [Code
of Conduct](.github/CODE_OF_CONDUCT.md), and [Support](SUPPORT.md). Check the
[community guides](.github/) and run documentation validation locally:

```bash
python3 -m pip install -r requirements-docs.txt
python3 docs/scripts/validate_docs.py
python3 -m pytest -q docs/tests
git diff --check
```

Keep changes focused, do not commit secrets or generated caches, and include
validation evidence in the pull request. See [how maintainers release](docs/maintainers/release.md)
for versioning and rollback rules.

## Security and privacy

Treat agent instructions, scripts, generated commands, and external content as
untrusted until reviewed. Do not provide secrets or confidential data to an AI
provider unless your organization explicitly allows it. The Skills CLI may
send anonymous telemetry; the install examples opt out with
`DISABLE_TELEMETRY=1`.

Report vulnerabilities privately using [SECURITY.md](SECURITY.md). For threat
boundaries and safe automation, read [Security testing](docs/how-to/verify-package-and-metrics.md)
and the [security review guidance](docs/reference/validation.md).

## License and release status

The repository is licensed under [Apache License 2.0](LICENSE). Preserve the
license and attribution notices when redistributing it, and review third-party
source terms listed in the [source registry](docs/_data/content_sources.yml).
The current release is `v2.1.0`; release history and compatibility notes are
in [docs/reference](docs/reference/index.md).

The previous `v2.0.0-rc.1` tag remains the documented compatibility baseline
for older validation scripts; new installs should use `v2.1.0`.
