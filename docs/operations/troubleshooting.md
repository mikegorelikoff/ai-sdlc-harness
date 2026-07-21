---
title: Troubleshooting and recovery
description: Diagnose installation, state, index, artifact, branch, host, budget, and helper failures while preserving authoritative evidence.
---

# Troubleshooting and recovery

Start narrow. Preserve the current evidence, identify the authority layer that
failed, run read-only diagnosis, repair the earliest invalid producer, and then
re-run its downstream consumers. Never delete an authoritative artifact just
to make a derived check pass.

## First response

!!! terminal "Run in terminal"

    ```bash
    pwd
    git branch --show-current
    git status --short
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
    ```

Capture the exact command, exit code, stdout/stderr, repository revision,
working directory, selected skill/flow, expected artifact, and recent approved
change. Redact secrets before sharing diagnostics.

## Failure matrix

| Failure | Diagnose safely | Safe repair or blocker | Validate / expected result | Do not do | Escalate when |
| --- | --- | --- | --- | --- | --- |
| Install command fails | Run `node --version`, `npm --version`, `git status --short`, then verify that the exact-fetch checkout in the [install guide](../how-to/install.md) resolves to the documented SHA before running `DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" --list`. | If origin, telemetry policy, revision, and scope are accepted, restore partial installation changes through Git and retry the host-scoped install; otherwise return a blocker. | Run `DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json` and navigator `--help`; expected inventory is present and no import traceback appears. | Do not paste credentials, enable unapproved telemetry, add global scope, put a SHA in a GitHub `/tree/...` URL, or delete unrelated files to force installation. | Origin, package contents, telemetry, scope, network policy, revision, or requested permissions differ. |
| Helper import fails after install | Run `python3 .agents/skills/ai-sdlc-navigator/scripts/navigate.py --help` and inspect the installed shared-runtime inventory. | Reinstall the accepted version with `ai-sdlc-shared-runtime`; if the source version is unknown, stop with a package-owner blocker. | Re-run navigator and SDD `--help`; expected usage renders from both with no traceback. | Do not edit an installed runtime mirror as the canonical fix or copy source-only `_shared` ad hoc. | Source and installed inventory disagree after a clean reinstall. |
| Invalid or corrupt state | Preserve the file, then run `python3 .agents/skills/ai-sdlc-shared-runtime/scripts/state_machine.py status --feature <feature> --workspace <refinement-or-implementation> --format toon`. | Use the [recovery journey](../flows/recovery.md) to reconstruct derived state from accepted artifacts/transitions; if no unique transition exists, return a blocker. | Re-run `python3 .agents/skills/ai-sdlc-shared-runtime/scripts/state_machine.py status --feature <feature> --workspace <refinement-or-implementation> --format toon`; expected schema, feature, workspace, stages, and fingerprints agree with authoritative artifacts. | Do not hand-edit status to “done,” initialize over existing evidence, or discard the corrupt copy. | No unambiguous accepted transition, artifact owner, or recovery evidence exists. |
| Stale specs index | Run `git diff -- specs/_ai_sdlc specs-refiniment/_ai_sdlc` and compare index routes/fingerprints with feature artifacts and state. | After durable artifacts validate, run `python3 .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_specs_index.py --workspace all --quick-flow`. | Re-run `python3 .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_specs_index.py --workspace all --quick-flow` and `git diff --check`; expected TOON/Markdown indexes contain each feature once at its canonical route. | Do not edit index rows by hand, hide a duplicate, or refresh before fixing source artifacts. | Duplicate identity, conflicting roots, unreadable metadata, or an unowned feature remains. |
| State/artifact contradiction | Run the owning skill's `--state-check` plus `git diff -- <feature-root>` and identify the earliest producer whose artifact/state disagree. | Reopen that producer through the [recovery journey](../flows/recovery.md); if the contradiction changes accepted scope, approval, or risk, return a blocker to the accountable owner. | Re-run the producer validator and `--state-check`; expected artifact, state, decision, and downstream index agree on the current revision. | Do not choose the newer timestamp automatically or alter derived state to overrule accepted Markdown. | The authoritative artifact or accepted decision is disputed. |
| Interrupted write | Run `git status --short`, inspect the target directory and journal/lock, and preserve any temporary file before another write. | Follow the owning helper's recovery or the [interrupted-write flow](../flows/recovery.md); when old/new candidates are ambiguous, return a blocker rather than merge bytes. | Run the owning validator and `git diff --check`; expected one atomic canonical artifact exists and failed/interrupted evidence remains recorded. | Do not delete locks/temp files before capture, concatenate partial outputs, or rerun a non-idempotent mutation blindly. | Both candidates appear valid, a journal gap exists, or evidence was lost. |
| Divergent refinement/implementation paths | Run `python3 .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_migrate.py --root . --workspace all --check` and inspect both feature indexes/decisions. | Apply only an approved migration with the same helper's `--apply`; unresolved independently accepted truth is a blocker. | Re-run `ai_sdlc_migrate.py ... --check`; expected no unresolved conflict and all trace links point to canonical routes. | Do not select by timestamp, copy one tree over another, or rename `specs-refiniment` manually. | Both paths contain accepted conflicting truth or migration changes public compatibility. |
| Predecessor blocked | Run `python3 .agents/skills/ai-sdlc-shared-runtime/scripts/state_machine.py check --feature <feature> --skill <blocked-skill> --workspace <workspace> --quick-flow` and read the returned predecessor/owner. | Resume the earliest incomplete producer named by the blocker; if it needs a protected decision or exception, return that exact blocker. | Re-run the same installed `state_machine.py check` command; expected transition is allowed before starting the consumer. | Do not switch to `--quick-flow`, fabricate an assumption, or mark the predecessor complete to skip it. | The predecessor owner, required evidence, or eligible exception authority is unavailable. |
| Dirty Git worktree | Run `git status --short`, `git diff --name-only`, and `git diff --cached --name-only`; classify task, user-owned, generated, and unrelated paths. | Preserve unrelated work; stage exact task paths or use the [branching guide](../reference/skills/ai-sdlc-branching.md) for a separate approved branch/worktree. If safe separation is impossible, return a blocker. | Re-run `git status --short` and `git diff --cached --check`; expected staged scope matches one task and unrelated edits remain preserved. | Do not use destructive reset/checkout, stage everything, or overwrite another contributor's changes. | Ownership is unclear, paths overlap inseparably, or cleanup would be destructive. |
| Unsupported host/capability | Run installed adapter `--help`, then follow [host negotiation](../how-to/negotiate-host-adapter.md) with an explicit request/adapter contract. | Choose a declared deterministic fallback or another approved host; no safe fallback means return a blocker. | Re-run `adapter.py --validate` or `adapter.py --negotiate`; expected result names supported mapping or explicit unsupported capability with no hidden mutation. | Do not silently expand permissions, invent a host capability, or weaken a protected gate. | Required capability has no approved mapping/fallback or changes identity, network, or external-write authority. |
| Global install reports Eve/PromptScript failures | Inspect the original command for `--all --global` or `--agent '*'`; preserve the summary and confirm the pinned CLI version. | Create `$HOME/.codex/skills`, rerun the verified checkout with `--skill '*' --agent codex --global --copy -y`, then list with `--global --agent codex --json`. | Expected: 44 skills, no Eve/PromptScript attempts, and every item names `Codex` in `agents`; an empty list means not linked. | Do not use `--all` when you mean all skills for one agent, and do not trust install-summary success without link verification. | The explicit Codex command still fails, any item is not linked, or another host needs support evidence. |
| Exhausted runtime budget | Run `python3 .agents/skills/ai-sdlc-runtime/scripts/runtime.py . --status --run-id <run-id> --format toon` and inspect task attempts, failures, tokens, blockers, and journal. | Stop with a handoff, narrow/replan the accepted DAG, and obtain owner approval for any new budget; otherwise return a blocker and keep `runtime.py` state intact. | Re-run runtime `--status`; expected plan fingerprint is accepted, remaining budget is explicit, and only eligible work is ready. | Do not reset counters, start a duplicate run, drop failed attempts, or buy scope with an undeclared budget. | More budget changes cost, scope, safety, policy, or the immutable plan. |
| Non-zero helper exit | Run `python3 <documented-helper> --help`, repeat the exact read/check invocation, and capture exit code plus stdout/stderr. | Correct only the named input, route, schema, or permission; unknown/nondeterministic exit meaning is a blocker for the helper owner. | Re-run `python3 <documented-helper> <same-read-or-check-arguments>`; expected exit and artifact/report match the helper's guide before any broader suite runs. | Do not append random flags, grant broad permission, suppress stderr, or claim the failed check passed. | Exit meaning is undocumented, changes between identical inputs, or conflicts with authoritative evidence. |
| Research network/source failure | Preserve the question/source record and use the [web research protocol](../reference/skills/ai-sdlc-research.md) to open the direct locator and check freshness. | Retry only approved internet access or return a sourced blocker; do not substitute cached model knowledge. | Re-run the authoritative research helper on `/tmp/research.json`; expected direct HTTP(S) sources, access dates, citations, and limitations validate. | Do not cite search-result pages, fabricate access dates, or present model memory as current evidence. | Access rights, source authenticity, legal use, or required current evidence remains unresolved. |
| Package trust deny | Run the read-only Branch A command in [package trust](../reference/skills/ai-sdlc-package-trust.md) and inspect each independent control/reason code. | Correct/rebuild at package source or choose an accepted version; policy change or waiver request is a human blocker. | Re-run Branch A; expected `allow` only when every required origin, API, capability, integrity, and provenance control passes. | Do not weaken allowed origins/capabilities, ignore a failed control, or treat a hash as author approval. | A new trust root, capability, provenance rule, or waiver decision is required. |
| Rendered docs/link failure | Run `python3 docs/scripts/build_catalog.py --check`, `python3 docs/scripts/validate_docs.py`, strict MkDocs, then `python3 docs/scripts/validate_rendered.py`. | Fix the authoritative source or `build_catalog.py`, regenerate, and rebuild; generated output alone is not the repair target. | Repeat `build_catalog.py --check`, source validation, strict build, and `validate_rendered.py`; expected catalog is drift-free and every rendered local target resolves. | Do not hand-edit generated guides, ignore strict-build diagnostics, or publish a stale `site/`. | Public prose and runtime source disagree or external build dependencies changed incompatibly. |
| Documentation dependency import fails | If `validate_docs.py` reports a missing package such as `tiktoken`, compare the interpreter with `requirements-docs.lock` and the [validation environment](../reference/validation.md). | Run the check through `UV_CACHE_DIR=/tmp/ai-sdlc-uv-cache uv run --with-requirements requirements-docs.lock ...`; populate the cache only with approved package-index access. | Re-run source and token validation in the pinned environment; expected exact `o200k_base` counts and no import traceback. | Do not skip Learn validation, substitute word counts, install an unpinned global package, or report the blocked check as passing. | Package access is denied, the lock cannot resolve on the supported runtime, or the pinned dependency fails integrity checks. |

## Recovery order

```text
authority/policy -> accepted decision -> source artifact -> state/index
                 -> generated projection -> validation -> handoff
```

Repair left to right. Rebuilding a projection before fixing its source creates
fresh-looking stale evidence.

## Safe resume checklist

- The accountable owner accepts the recovery decision.
- Secrets/permissions are contained and temporary access is reviewed.
- The repository and branch are correct; unrelated work is preserved.
- Authoritative artifacts and decisions are readable and consistent.
- The narrow failed validator passes on the current revision.
- Downstream state, indexes, metrics, and handoff are refreshed.
- The incident/blocker record names cause, action, owner, and residual risk.

If any item is uncertain, return a blocker with the exact missing input and
owner. “Try again with more permissions” is not a recovery plan.
