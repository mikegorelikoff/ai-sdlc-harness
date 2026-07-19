---
title: Control-plane flows
description: Understand controlled specification changes, delivery graph, policy, context, runtime, workflows, adapters, diagnostics, trust, and metrics.
---

# Control-plane flows

The control plane coordinates delivery evidence. It does not replace
authoritative Markdown or grant an agent more host, filesystem, network, policy,
approval, or release authority.

## Exact control-plane branch contract

| Branch ID | Predecessor / entry | Accountable owner | Required input | Exact capability | Artifact / result | Exit gate | Next consumer / handoff | Reopen condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `controlled_change` | Accepted intent/decision changed after dependent evidence exists. | Product/BA/Delivery plus canonical target owners | Change ID, owner, canonical targets, proposal/design/tasks, semantic deltas, approval and recovery plan. | `ai-sdlc-change-set` | Governed `changes/<change-id>/` workspace with preview, approval, recovery, apply, and archive evidence. | Delta validates; preview matches intent; owners approve; policy allows; targets have no drift/conflict; recovery is ready. | `change_impact` and every affected artifact owner. | Target drift, conflict, rejected approval, policy denial, incomplete recovery, or later intent change. |
| `change_impact` | Approved/applied change set or exact changed source references. | Delivery with BA/Dev/QA owners | Feature root, stable changed-reference JSON, source evidence, current lifecycle state. | `ai-sdlc-change-impact` | Feature `change-impact.md` and `_ai_sdlc/change-impact.toon`. | Every stale dependent, reason, owner, and earliest safe reopen action is explicit. | Named refinement, SDD, QA, validation, or release producer. | Another source changes, dependency trace changes, or reopened evidence is still stale. |
| `delivery_graph` | Canonical lifecycle artifacts and Git evidence exist. | Delivery/Architecture | Repository root, canonical metadata/trace IDs, state/index evidence, optional explicit trace edges. | `ai-sdlc-delivery-graph` | `_ai_sdlc/delivery-graph.{toon,json,md}`. | Graph rebuild is deterministic; ambiguities, gaps, orphans, and coverage are explicit. | QA/readiness/release gates or a named artifact owner. | Any indexed source changes, ambiguous edge remains, or required coverage is missing. |
| `evidence_freshness` | Validation/test/review evidence claims coverage of mutable sources. | QA/Delivery | Evidence-source records, dependency identities, timestamps/expiry, current files and as-of time. | `ai-sdlc-delivery-graph` evidence ledger | `_ai_sdlc/evidence-ledger.{toon,json,md}`. | Fingerprints and dependencies recompute; stale/expired/blocked coverage is reported without rewriting sources. | Producing validation/test/review stage, then `delivery_graph`. | Covered source/dependency changes, evidence expires, or ledger integrity fails. |
| `policy_waiver` | A workflow action needs a governed allow/deny/gate decision or exception. | Security/Architecture/Release | Action/context JSON, versioned policy layers, protected rules, explicit owner-approved waiver when requested. | `ai-sdlc-policy` | `_ai_sdlc/policy-resolution.{toon,json}` or `_ai_sdlc/policy-decisions/` record. | Provenance is complete; protected rules are not weakened; required gates and waiver eligibility are satisfied. | The owning workflow action; denial returns to its accountable owner. | Policy/context/fingerprint changes, waiver expires/revokes, or a required gate becomes unsatisfied. |
| `context_pack` | A bounded task needs repository evidence beyond its accepted spec. | Dev/Repository owner | Repository manifests/guidance, task ID/goal, selectors, exclusions, ownership/test topology, token budget. | `ai-sdlc-project-context` | `project-context.md`, `_ai_sdlc/project-context.toon`, and optional `_ai_sdlc/context/task-packs/<task>.{toon,json,md}`. | Every selected range/exclusion is explained; fingerprint is current; budget and secret boundaries pass. | Implementation, validation, review, workflow, or runtime task. | Repository drift, changed task/selectors, stale topology, missing owner/test evidence, or secret risk. |
| `runtime` | Immutable task plan and its dependencies/gates are accepted. | Dev/Delivery | Versioned run plan, run ID, task fingerprints, retry/budget/commit rules, exact outcomes and token use. | `ai-sdlc-runtime` | `_ai_sdlc/runs/<run-id>/journal.jsonl`, exact `state.json`, and complete `state.toon`. | Journal chain/replay is valid; transitions and dependencies are legal; completion has required result/commit evidence. | Validation/commit owner for completed tasks or exact blocker owner for stopped runs. | Interrupted run, journal/projection mismatch, changed task input, exhausted budget, terminal retry, or missing approval. |
| `workflow_plan` | Repeated multi-step delivery intent is explicit and governable. | Delivery/Dev | Versioned workflow JSON, typed steps/dependencies, conditions, gates, hooks, capabilities, host constraints. | `ai-sdlc-workflow` | `_ai_sdlc/workflows/<workflow-id>/plan.{toon,json,md}`. | Schema/cycle/capability checks pass; waves, skips, gates, hooks, and fallbacks are explicit; nothing executed. | `host_adapter`, then runtime/host executor after approvals. | Workflow/context/policy/host capability changes or an unsafe declaration appears. |
| `host_adapter` | A valid workflow requires execution on a specific agent host. | Dev/Delivery/Architecture | Adapter manifest, capability request, portable operations, isolation/concurrency requirements. | `ai-sdlc-host-adapter` | `_ai_sdlc/adapters/<adapter-id>/negotiation.{toon,json,md}`. | API/capabilities match; every mapping is native or equivalent registered fallback; missing requirement blocks. | Workflow/runtime executor with the negotiated limits. | Host/manifest/request changes, compatibility range fails, or fallback equivalence is lost. |
| `doctor` | Installation behavior is missing, broken, or uncertain. | Dev/Delivery | Repository root, installed inventory, diagnostics registry, environment evidence. | `ai-sdlc-doctor` | `_ai_sdlc/doctor/report.{toon,json,md}`. | Every check has evidence and exact remediation; the skill itself performs no repair. | Human/operator remediation, then repeat `doctor`. | Environment/inventory changes or any required check remains failed/unknown. |
| `upgrade` | A reviewed target harness/package version is proposed. | Repository owner/Release | Current and target inventories, active harness API, hashes, migration, backup, rollback and compatibility evidence. | `ai-sdlc-doctor` upgrade preview | `_ai_sdlc/upgrades/<id>/plan.{toon,json,md}`. | File diff, migrations, backups, rollback, compatibility and blockers are reviewed before apply. | Authorized installer/operator; post-change `doctor` and validation. | Target/current inventory drift, backup/rollback gap, incompatible API, hash/path conflict, or failed post-check. |
| `package_trust` | Install/update wants to expose a package capability. | Security/Delivery/Release | Package root/manifest, allowed origins/capabilities, harness API, digests and provenance policy. | `ai-sdlc-package-trust` | `_ai_sdlc/trust/<package-id>/decision.{toon,json,md}`. | Origin, API, declarations, every file digest, capabilities and required provenance pass independently. | Installer/update owner or policy denial owner. | Package/manifest/policy/API changes, provenance expires, digest drifts, or undeclared capability appears. |
| `local_metrics` | Repository-local runtime/evidence records can support process learning. | Delivery/Team lead | Local run/task/budget/coverage records and privacy boundary; no source content. | `ai-sdlc-package-trust` metrics mode | `_ai_sdlc/metrics/local.{toon,json,md}`. | Aggregation is content-free, reproducible, scoped, and does not claim causality. | `ai-sdlc-retrospective` and accountable adoption owners. | Source schema/privacy scope changes, invalid record appears, or interpretation exceeds the evidence. |

## Controlled specification change

```text
create isolated change set
  -> validate semantic delta
  -> preview canonical diffs and downstream staleness
  -> evaluate policy and approvals
  -> stage and apply atomically
  -> archive recovery evidence
  -> rebuild graph and reopen affected work
```

Use this path when accepted requirements or decisions change after downstream
work exists. Preview is non-mutating. Apply is blocked by drift, conflicts,
missing approval, policy denial, or incomplete recovery preparation.

## Delivery graph and evidence freshness

The graph derives nodes and evidence-backed edges from canonical artifacts and
Git. Query it for trace paths, gaps, orphans, and fresh coverage. The evidence
ledger fingerprints artifacts and dependencies, propagates stale state, and
never edits authoritative sources to improve a metric.

## Policy and waivers

Layered policy resolves base, organization profile, project, and user inputs.
Protected rules can be strengthened but not weakened by later layers. A waiver
is eligible only when scoped to a rule/action/subject/context, owned, approved,
reasoned, accepted, and unexpired. Unknown safety-sensitive actions fail closed.

## Context Engine v2

Repository topology, ownership, source-to-test relationships, task selectors,
freshness, exclusions, and token budgets produce a bounded context pack. The
pack explains why each range was selected and which secrets or generated paths
were excluded. It is context for a task, not authority to alter a file.

## Resumable runtime

The runtime starts from an immutable task plan and appends hash-chained JSONL
events. Exact `state.json` supports recovery and complete `state.toon` exposes
the same task state, attempts, ready work, budgets, stop reason, sequence, and
fingerprint. `--next` is idempotent; resume replays the journal;
commit-boundary tasks cannot succeed without commit evidence.

Stop conditions include exhausted step/failure/token budgets, terminal retry,
blocked approval, invalid transition, journal damage, or missing dependency.

## Declarative workflows and host adapters

A workflow declares typed steps, dependencies, conditions, approval gates,
hooks, capabilities, isolation, and concurrency. Validation rejects cycles or
unsafe declarations. Planning creates safe dependency waves and falls back to
sequential execution when a host lacks isolation or concurrency.

The host adapter negotiates exact capabilities and mappings. A fallback must be
registered and behaviorally equivalent; a missing required capability blocks.
The adapter never converts a workflow declaration into undeclared shell/network
authority.

## Doctor, upgrade, package trust, and metrics

- Doctor runs deterministic environment checks and gives exact remediation.
- Upgrade preview compares inventories, schemas, backups, migrations, rollback,
  compatibility, and blockers before any apply.
- Package trust evaluates origin, API range, declared capability, file digest,
  and required provenance independently.
- Local metrics aggregate content-free run/task/budget/coverage signals. They
  do not export source or prove organizational causality.

Every operation returns a complete TOON result by default. JSON is retained for
schema, external interoperability, exact recovery, and JSONL journal boundaries.
