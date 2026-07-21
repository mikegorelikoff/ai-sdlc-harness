---
title: Install the harness
description: Install AI SDLC skills into a consumer repository, verify the result, and understand scope, trust, and rollback.
---

# Install the harness

This procedure installs agent skills into a project using the Skills CLI. It
does not copy this source repository into your application and it does not
create delivery artifacts until you ask an agent to use a workflow.

## Before you begin

!!! note "Current release"

    These consumer commands install `v2.1.0`. Resolve the annotated tag to an
    exact commit, review the release notes, and apply your organization's trust
    policy. The harness supports multiple agent hosts; use the host-specific
    install scope documented below.

You need:

- Git and a repository with a clean or understood working tree;
- Node.js `>=22.20.0`/npm with `npx`;
- Python 3.10 or newer for deterministic helpers;
- network access to npm and GitHub during installation;
- an AI agent environment selected for a pilot; see [supported environments](../reference/supported-environments.md);
- permission to add project-scoped agent files.

Choose a low-risk consumer repository for your first use. The **consumer
repository** is the software project receiving skills. The **harness source
repository** is this GitHub project, used by maintainers and contributors.
For the documented Codex pilot, [install and authenticate Codex CLI](setup-codex.md)
before the first agent prompt.

Install missing prerequisites from the official [Git](https://git-scm.com/downloads),
[Node.js](https://nodejs.org/en/download), and
[Python](https://www.python.org/downloads/) distribution pages or an approved
organizational package mirror. Do not use an agent-generated download URL.

The shell blocks below use POSIX syntax (Linux, macOS, Windows Subsystem for
Linux (WSL), or Git Bash). In PowerShell, set the opt-out once in the session
and run the same pinned CLI:

```powershell
$env:DISABLE_TELEMETRY = "1"
$HarnessTag = "v2.0.0-rc.1"
$HarnessSource = Join-Path ([System.IO.Path]::GetTempPath()) ("ai-sdlc-harness-" + [guid]::NewGuid())
node --version  # expected: v22.20.0 or newer
git init $HarnessSource
git -C $HarnessSource remote add origin https://github.com/mikegorelikoff/ai-sdlc-harness.git
git -C $HarnessSource fetch --depth 1 origin ("refs/tags/{0}:refs/tags/{0}" -f $HarnessTag)
git -C $HarnessSource checkout --detach ($HarnessTag + "^{commit}")
$HarnessRevision = git -C $HarnessSource rev-parse HEAD
if ((git -C $HarnessSource rev-list -n 1 $HarnessTag) -ne $HarnessRevision) { throw "Harness revision mismatch" }
npx -y skills@1.5.19 add $HarnessSource --skill '*' --agent codex -y
npx -y skills@1.5.19 list --json
New-Item -ItemType Directory -Force .ai-sdlc | Out-Null
Copy-Item (Join-Path $HarnessSource "config/ai-sdlc-managed-skills.txt") .ai-sdlc/harness-managed-skills.txt
@{schema="ai-sdlc-install-record/v1"; revision=$HarnessRevision; skills_cli="1.5.19"; agent="codex"; selection="all-skills"; inventory=".ai-sdlc/harness-managed-skills.txt"} | ConvertTo-Json -Compress | Set-Content -Encoding utf8 .ai-sdlc/harness-install.json
python .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
Remove-Item -LiteralPath skills-lock.json
Remove-Item -LiteralPath $HarnessSource -Recurse -Force
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

Inspecting repository files in a browser or a separately cloned checkout is the
only inspection that occurs before third-party installer code runs. The
following `--list` command still downloads and executes the pinned Skills CLI;
review `npm view skills@1.5.19 dist.integrity repository engines --json` and
your approved npm provenance before invoking it.

!!! terminal "Run in terminal — from the consumer repository"

    ```bash
    HARNESS_TAG=v2.0.0-rc.1
    HARNESS_TMP="$(mktemp -d)"
    HARNESS_SRC="$HARNESS_TMP/ai-sdlc-harness"
    git --version
    node --version
    npm --version
    PYTHON_BIN="${PYTHON_BIN:-python3}"
    "$PYTHON_BIN" --version
    npm view skills@1.5.19 dist.integrity repository engines --json
    git init "$HARNESS_SRC"
    git -C "$HARNESS_SRC" remote add origin https://github.com/mikegorelikoff/ai-sdlc-harness.git
    git -C "$HARNESS_SRC" fetch --depth 1 origin "refs/tags/$HARNESS_TAG:refs/tags/$HARNESS_TAG"
    git -C "$HARNESS_SRC" checkout --detach "$HARNESS_TAG^{commit}"
    HARNESS_REV="$(git -C "$HARNESS_SRC" rev-parse HEAD)"
    test "$(git -C "$HARNESS_SRC" rev-list -n 1 "$HARNESS_TAG")" = "$HARNESS_REV"
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" --list
    ```

Stop unless Node reports `v22.20.0` or newer and Python reports 3.10 or newer.
The installer does not enforce the Python floor. `npm view
skills@1.5.19 engines --json` is the recovery check when a pinned CLI invocation
reports an engine mismatch.

This lists available skills without installing them. Review the repository
origin and selected package names. The annotated `v2.0.0-rc.1` tag is resolved
to the exact revision checked above. Skills CLI `1.5.19` treats the final
segment of a GitHub `/tree/...` URL as a branch, so installation uses the
verified detached local checkout instead.

## Install project-scoped skills

!!! terminal "Run in terminal — from the consumer repository"

    ```bash
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" --skill '*' --agent codex -y
    ```

Run this in the same terminal session as the inspection block so
`HARNESS_SRC` still names the verified checkout. `--skill '*'` selects all 44
harness skills—including the shared runtime—while `--agent codex` selects the
one manually validated host target. `--all` would override that scope: a clean
baseline test of CLI
`1.5.19` reported 73 possible targets; that broad mode is not the canonical
pilot path. Because `-g` is absent, installation remains project-scoped. Stop
if the CLI summary names unexpected locations.

### Understand the created directories

For this project-scoped path, `.agents/skills/` is the canonical universal
skill store, not an accidental duplicate. A host or installer may also create
a host-specific directory or symlink. Inspect before deciding:

```bash
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
git status --short
find . -maxdepth 3 -type l -print
```

Do not delete `.agents/` merely because another folder shows the same skill
names; host links can depend on it. An unexpected regular copy, unclear owner,
or unrelated pre-existing directory is a blocker for manual comparison, not
permission for recursive cleanup.

For a smaller installation, create the reviewed inventory first and use it as
the exact installer input; do not copy the 44-name full inventory afterward:

```bash
mkdir -p .ai-sdlc
printf '%s\n' \
  ai-sdlc-commit-prep \
  ai-sdlc-conventional-commit \
  ai-sdlc-navigator \
  ai-sdlc-project-context \
  ai-sdlc-sdd \
  ai-sdlc-shared-runtime \
  ai-sdlc-validation | sort -u > .ai-sdlc/harness-managed-skills.txt
set --
while IFS= read -r skill; do set -- "$@" --skill "$skill"; done < .ai-sdlc/harness-managed-skills.txt
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" "$@" --agent codex -y
```

This starter subset includes shared runtime plus the commit-message dependency
used by commit prep. Keep `selection` as `explicit-skills` in the record below.
For all skills, retain the canonical wildcard command and full packaged
inventory. The validator treats the managed inventory as ownership, requires
every managed name to be installed, and permits unrelated project or
third-party skill directories to coexist.

## Optional: install globally for Codex

Project-scoped installation is the auditable team default. Use global scope
only when one person intentionally wants the skills available to Codex across
multiple repositories. Run this in the same terminal session as the inspection
block, before deleting `HARNESS_SRC`:

```bash
mkdir -p "$HOME/.codex/skills"
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" --skill '*' --agent codex --global --copy -y
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --global --agent codex
```

Expected: 44 skills install for the single `codex` target and the list command
shows `"agents": ["Codex"]` for every global inventory item. `--copy` makes
the selected installation method explicit before the temporary checkout is
removed. Pre-creating `$HOME/.codex/skills` is required for a clean-home test
because the pinned CLI can otherwise populate `$HOME/.agents/skills` without
linking the inventory to Codex. Treat an empty `agents` array or “not linked”
result as a failed verification even when the install summary says success.

The upstream CLI defines these flags differently:

- `--skill '*'` selects every skill from this repository;
- `--agent codex` selects one agent;
- `--global` (or `-g`) selects user scope;
- `--all` selects every skill **and every recognized agent**.

Never combine global scope with `--all` or `--agent '*'` for this harness.
Skills CLI `1.5.19` recognizes agents that do not define global installation,
including Eve and PromptScript. With 44 skills, those two unsupported targets
produce exactly 88 failures even when supported targets installed correctly.
Rerun the explicit command above; do not interpret the failure count as 88
broken harness skills. The flag meanings are defined by the
[official Skills CLI documentation](https://github.com/vercel-labs/skills#options),
and the clean-home behavior is tracked in the upstream
[global directory issue](https://github.com/vercel-labs/skills/issues/537).

Global installation is workstation state: it is not committed with a consumer
repository and the project-scoped `.ai-sdlc/harness-install.json` procedure
below does not describe it. Record the CLI version, harness revision, selected
agent, installation method, and verification output in your workstation or
organizational inventory. Use project scope when repository-level provenance
and peer review are required.

After changing a global inventory, start a fresh agent-host session. A host may
cache its skill registry for one conversation. This refreshes host discovery;
it does not replace filesystem verification. For a direct POSIX diagnostic,
run the packaged navigator and inspect `skill_roots`:

```bash
python3 "$HOME/.agents/skills/ai-sdlc-navigator/scripts/navigate.py" \
  --root /path/to/consumer --intent "<request>" --quick-flow --format toon
```

The navigator discovers siblings from the package it is executing. If that
report is correct but the host cannot invoke a skill after a new session,
record host, version, target, scope, and `skills list` evidence as a host
conformance issue. Do not install every recognized agent as a workaround.

## Verify the result

!!! terminal "Run in terminal"

    ```bash
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
    git status --short
    "$PYTHON_BIN" --version
    "$PYTHON_BIN" .agents/skills/ai-sdlc-navigator/scripts/navigate.py --help
    "$PYTHON_BIN" .agents/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help
    ```

Expected result:

- for `all-skills`, the list contains all 44 managed names; for
  `explicit-skills`, every name in the reviewed managed inventory is present;
  either list may also contain unrelated project or third-party skills;
- Git shows only the agent/skill files you intended to add;
- Python reports 3.10 or newer;
- navigator and SDD helper usage render without an import traceback;
- no application source, secrets, or existing project artifacts were replaced.

The Codex-scoped command creates `.agents/skills/` and a transient
`skills-lock.json`. CLI `1.5.19` records the absolute temporary source path in
that lock and cannot update this local-source installation, so the lock is not
portable team provenance and must not be committed. Record portable identity,
then remove only the transient lock:

```bash
mkdir -p .ai-sdlc
test -f .ai-sdlc/harness-managed-skills.txt || cp "$HARNESS_SRC/config/ai-sdlc-managed-skills.txt" .ai-sdlc/harness-managed-skills.txt
HARNESS_SELECTION=all-skills # use explicit-skills when you ran the subset block
printf '{"schema":"ai-sdlc-install-record/v1","revision":"%s","skills_cli":"1.5.19","agent":"codex","selection":"%s","inventory":".ai-sdlc/harness-managed-skills.txt"}\n' "$(git -C "$HARNESS_SRC" rev-parse HEAD)" "$HARNESS_SELECTION" > .ai-sdlc/harness-install.json
"$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
rm skills-lock.json
rm -rf "$HARNESS_TMP"
git status --short
```

The installed validator checks record fields, revision syntax, sorted managed
inventory, full-versus-explicit selection integrity, and presence of every
managed skill before temporary source cleanup. Unrelated installed skills are
allowed and are never claimed as harness-owned. The published JSON Schema remains available for organization
tooling. Commit `.agents/skills/` and both portable harness records. Skill documentation uses logical paths such as
`skills/<name>`; in a consumer installation, resolve those paths beneath
`.agents/skills/`.

!!! warning "Human checkpoint"

    Review and commit the accepted `.agents/skills/` inventory and portable
    install record before starting a feature branch. Installation is not
    approval for an agent to modify product code, policy, or delivery evidence.

From a clean consumer baseline, create that auditable installation commit with
exact paths rather than broad staging:

```bash
git status --short
git add .agents/skills .ai-sdlc/harness-install.json .ai-sdlc/harness-managed-skills.txt
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "chore: install AI SDLC harness"
git status --short
```

Expected: the staged diff contains only the reviewed managed skills and two
portable records; the commit succeeds; final status prints nothing. If Git asks
for identity, unrelated paths appear, or status remains dirty, stop and use the
[Git and terminal primer](../foundations/git-and-terminal-primer.md) plus
[troubleshooting](../operations/troubleshooting.md). Do not use `git add -A` as
a shortcut.

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

Skills CLI `1.5.19` does not update this exact local-source installation and its
generic remove operation can leave the transient lock and empty host
directories. Do not use those commands as the canonical lifecycle. Follow
[Update safely](update.md) for exact reinstall, reviewed rollback, and cleanup.
Preserve project-owned specs, decisions, state, configuration, and evidence;
they are never installer-owned. For schema recovery, see
[Migrate to 1.1](migrate-1.1.md).

## Offline and private environments

The Skills CLI installation path requires registry and Git access. In an
offline environment, prepare and review a pinned package mirror through your
organization's approved supply-chain process. A local harness checkout can run
tests and compatibility validation, but this documentation does not claim that
cloning alone installs skills into another agent environment.

An offline invocation succeeds only when every required npm package and source
object already exists in an approved local cache or mirror. A clean offline
machine is therefore expected to fail. Prepare the mirror while connected,
record integrity metadata, disconnect, and test the complete install in a
disposable repository before organizational rollout.

For a private repository, configure an SSH key, GitHub CLI login, or approved
HTTPS credential with read access. Never paste tokens into an agent prompt.

## Troubleshooting first install

| Symptom | Safe response |
| --- | --- |
| Command appears hung | Wait for the npm/Git timeout; use `Ctrl-C` once, then check approved proxy/DNS/TLS access. Do not repeatedly launch installers. |
| Engine mismatch | Compare `node --version` with `npm view skills@1.5.19 engines --json`; upgrade Node through an approved source. |
| `python3` missing or below 3.10 | Install a supported Python, set `PYTHON_BIN` to its exact executable (for example `PYTHON_BIN=/opt/homebrew/bin/python3.11`), rerun `"$PYTHON_BIN" --version`, and substitute `"$PYTHON_BIN"` for displayed `python3` helper commands. Do not assume `python` and `python3` are the same. |
| `list --json` requires network | This CLI behavior is expected; use an approved registry/cache or record the offline limitation. |
| Skill helper path missing | Confirm `.agents/skills/ai-sdlc-shared-runtime` and the selected skill both exist; reinstall the pair if either is absent. |
| Unexpected agent directories | Do not commit or use the generic CLI remover. If the repository is disposable, delete that whole verified fixture from its parent. Otherwise follow the ownership-safe [uninstall procedure](update.md#remove-and-verify-cleanup), review every managed path, inspect status, and reinstall with an explicit `--agent`. |
| Navigator says a global sibling skill is missing | Start a fresh host session, run the packaged navigator diagnostic above, and inspect `skill_roots`. Repair the explicit Codex-scoped install only when the root or sibling `SKILL.md` is absent; otherwise record a host-conformance issue. |
| Project and global installations both exist | Treat the committed project inventory as repository authority. Compare revisions and update workstation state separately; do not assume host precedence or mix evidence from two revisions. |
| Authentication or certificate failure | Stop and ask the repository/network owner. Never disable TLS verification or paste a token into chat. |

After any failed attempt, inspect `git status --short`. Remove only files that
the installer created and that a human has verified are not project-owned. The
successful POSIX sequence removes only the unique directory named by
`HARNESS_TMP`; after a failure, inspect that variable and remove that exact
temporary directory only after preserving useful diagnostics.
