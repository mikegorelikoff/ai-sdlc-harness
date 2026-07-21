---
title: Installation validation report
description: Clean-environment commands, failures, corrections, and verified consumer sequence.
---

# Installation validation report

## Environments and authority

Baseline host: macOS 26.3.1 arm64, Git 2.50.1, Node 26.4.0, npm/npx
11.17.0, system Python 3.9.6, uv 0.11.28. Python 3.11.15 was used for the
supported local regression. GitHub Actions defines Ubuntu 24.04, Node 22.20.0,
and Python 3.10/3.13. Native Windows, Windows Subsystem for Linux (WSL), and the
remote jobs were not executed locally and are not represented as verified.

Network operations initially failed in the restricted sandbox and were rerun
only after explicit network approval. Temporary consumers and source checkouts
were created under `/tmp`; no existing project was used as an install target.

## Baseline release test

The baseline used Skills CLI 1.5.19 against immutable release commit
`7f36bdbad73e1d73dd8ea2185f8b88c88c8f2dc2`. Its old shallow check could list
and install 44 skills and run helper `--help`. A broad `--all` install also
created several host roots, demonstrating that CLI target recognition is not
harness support and that `--all` is unsuitable as the canonical scope.

The strengthened consumer test performs a complete Specification-driven
development (SDD) scaffold, gates each artifact, refreshes projections, and runs installed
commit readiness. Against that exact released commit it fails at the first
artifact because the installed helper incorrectly resolves the consumer root:

```text
ERROR: installed check_clarify.py ... missing
.agents/specs/001-runtime-smoke/requirements.md
```

CI now requires that exact released regression through `--expected-failure`;
it fails if the diagnostic changes or the release unexpectedly starts passing.
This is characterization evidence, not approval of the release.

## Candidate clean install and workflow

The corrected candidate was installed from a local exact checkout with a
bounded host selection:

```bash
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" \
  --skill '*' --agent codex -y
```

Actual result: 44 skills under `.agents/skills/`; no unexpected host root; all
20 installed shared helpers imported; the complete requirements, design,
test-cases, tasks, and QA scaffold passed its gates; task projection and status
agreed; installed commit readiness passed. The emulated install passed the
same workflow. The smoke runner now rejects real CLI modes without `--agent`.

The portable sequence copies the sorted 44-name managed inventory and writes a
schema-validated record under `.ai-sdlc/`. It removes the transient
machine-specific `skills-lock.json` and deletes the temporary source checkout.

## Documentation dependency bootstrap

An empty uv cache plus the old first command `uv run --offline` failed because
MkDocs Material was unavailable. Online locked resolution succeeded. The
corrected maintainer sequence installs `requirements-docs.lock` with hashes;
offline execution is documented only after preparing a cache or mirror.

## Update, rollback, and removal

Skills CLI 1.5.19 reports `No project skills to update` after the portable
local-source installation, so `skills update` is not a repair or upgrade path.
The documented procedure fetches the exact target commit, reinstalls the same
host scope, preserves the old managed inventory, and writes a retired-skill
list. A human checkpoint precedes removal of any retired directory and precedes
temporary evidence cleanup. The updated managed inventory and install record
are committed together.

Rollback uses the reviewed installation commit. Uninstall removes only paths
proved to be harness-owned by that commit and inventory; product specifications,
decisions, evidence, other providers, and locally modified same-named paths are
preserved.

## Final verified sequence

1. Verify supported Git, Node, npm/npx, Python, network policy, clean Git state,
   and one selected host.
2. Review package content and resolve an immutable 40-character commit.
3. Fetch that commit into a temporary directory and verify `rev-parse HEAD`.
4. Preview the 44 skills; install with `--skill '*' --agent codex`.
5. Verify only `.agents/` changed; copy the managed inventory; write and validate
   the portable install record; remove the transient lock and temporary source.
6. Execute installed helper help, the complete SDD consumer smoke, and Git diff
   review; commit both `.agents/` and `.ai-sdlc/` records.
7. Follow the first-feature tutorial. For upgrades, repeat exact reinstall and
   review the retired-skill set before any removal.

See the [canonical installation guide](../../how-to/install.md). Production
adoption remains blocked until a corrected immutable release exists and the
owner supplies a license.
