---
title: Supported environments
description: Distinguish tested harness environments, installer-recognized agent targets, and unverified combinations.
---

# Supported environments

Support is an evidence claim, not a synonym for “the installer recognized a
directory.” Use this page before installation or rollout.

## Runtime requirements

| Component | Required | Why |
| --- | --- | --- |
| Git | Current supported release | Clone, branch, diff, and evidence history |
| Node.js | `>=22.20.0` | Required by the pinned Skills CLI `1.5.19` |
| npm / `npx` | Supplied with Node.js | Runs the pinned third-party installer |
| Python | `>=3.10` | Runs deterministic harness helpers |
| Network | npm and GitHub during first install | Retrieves the CLI and pinned harness release |

Verify the versions rather than relying on an existing shell setup:

```bash
git --version
node --version
npm --version
python3 --version
```

Stop if Node.js or Python is below the stated floor. The installer can copy
files without proving that their Python helpers will run.

## Tested combinations

| Environment | Evidence | Status |
| --- | --- | --- |
| Ubuntu 24.04, Python 3.10 and 3.13 | Repository continuous-integration configuration; no current candidate run exported in this audit | Configured candidate; support pending a passing remote run |
| macOS, POSIX shell | Local corrected-candidate installation and complete consumer workflow | Candidate tested locally; no released combination is approved |
| Codex CLI 0.144.1 on macOS, Skills CLI target `codex` | Corrected-candidate host-scoped clean install and complete installed SDD/commit workflow on 2026-07-21 | Candidate manually validated; immutable `v1.2.0` remains blocked |
| Windows Subsystem for Linux (WSL) | POSIX-compatible documented route; no recorded candidate run | Recommended candidate route for Windows; not yet verified |
| Native PowerShell | Installation command only | Limited; end-to-end tutorials use WSL |
| Offline clean machine | No cached npm or Python packages | Not supported for first bootstrap; use approved mirrors |

“Candidate tested” means that the unreleased corrected tree completed the
recorded local workflow. It is not a released support promise. The matrix does
not promise support for every operating-system release,
shell, model provider, or agent host.

## Agent hosts versus installer targets

The third-party Skills CLI can recognize many agent target names and may print
a large target count when `--all` is used. That is installer behavior, not a
harness compatibility certification. This project currently publishes one
portable skill format and tests its deterministic files independently of a
model host. The maintainers' behavioral examples use Codex-style agents.

The exact manually validated host-scoped install used:

```bash
HARNESS_REV=7f36bdbad73e1d73dd8ea2185f8b88c88c8f2dc2
HARNESS_TMP="$(mktemp -d)"
HARNESS_SRC="$HARNESS_TMP/ai-sdlc-harness"
git init "$HARNESS_SRC"
git -C "$HARNESS_SRC" remote add origin https://github.com/mikegorelikoff/ai-sdlc-harness.git
git -C "$HARNESS_SRC" fetch --depth 1 origin "$HARNESS_REV"
git -C "$HARNESS_SRC" checkout --detach FETCH_HEAD
test "$(git -C "$HARNESS_SRC" rev-parse HEAD)" = "$HARNESS_REV"
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" --skill '*' --agent codex -y
rm -rf "$HARNESS_TMP"
```

It produced the canonical `.agents/skills/` inventory and 44 installed skills;
navigator routing and a single requirements scaffold passed. The stronger
complete installed workflow then failed when stable SDD helpers looked for the
consumer spec beneath `.agents/specs`. For organizational rollout, select
an explicit target with `--agent`, run the
[first feature tutorial](../tutorials/first-feature.md), and record the exact
host/version in pilot evidence. Treat all other hosts as **candidate** until
that workflow passes. Do not infer support merely because files appeared in a
host-specific directory.

## Installation locations

The canonical `--skill '*' --agent codex` installation creates
`.agents/skills/` plus a transient `skills-lock.json`. Remove that lock after
writing the portable install record because the lock contains the absolute
temporary source path. A project-scoped `--all` invocation instead targets all
installer-recognized hosts and can create unrelated host directories; it is
not the documented pilot path. Review `git status --short` before committing.

## Maintainer preview versus stable release

The `main` branch and its documentation can describe unreleased behavior.
Consumer installation instructions pin Skills CLI `1.5.19` and the immutable
commit `7f36bdbad73e1d73dd8ea2185f8b88c88c8f2dc2` to which `v1.2.0` currently
points; use the documentation at the `v1.2.0` tag only to reproduce matching
historical behavior. A future
release must re-run the installation, workflow, compatibility, and
documentation gates before it can make a newer support claim. Until then,
`v1.2.0` is a reproducible historical baseline, not an approved production
workflow.

Installation is the exception: use the current exact-fetch sequence above.
The older tagged page's GitHub `/tree/<SHA>` form does not work with Skills CLI
`1.5.19` and is retained only as historical release evidence.

## Evidence checklist

- [ ] Runtime versions meet the floors above.
- [ ] Installation uses the documented immutable commit and pinned CLI version.
- [ ] The target agent is named in pilot evidence.
- [ ] Navigator and SDD helper `--help` commands succeed.
- [ ] One complete workflow passes in a disposable repository.
- [ ] Unsupported combinations and skipped tests are recorded.

See [Install the harness](../how-to/install.md), [Troubleshooting and
recovery](../operations/troubleshooting.md), and [Governance and
trust](../operations/governance.md).
