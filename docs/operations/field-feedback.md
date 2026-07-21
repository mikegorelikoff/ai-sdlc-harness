---
title: Field feedback disposition
description: Map operational feedback to harness controls, fixes, and explicit boundaries.
---

# Field feedback disposition

This register turns the 2026-07-21 team notes into actionable harness scope.
The notes are field evidence, not proof that every interpretation is correct.

| Feedback or difficulty | Disposition | Resolution or owner |
| --- | --- | --- |
| Global installation reported 88 failures for Eve and PromptScript. | Resolved | Broad `--all --global` selected unsupported targets. Use `--skill '*' --agent codex --global`; see [Install](../how-to/install.md#optional-install-globally-for-codex). The skills themselves did not fail 88 times. |
| Navigator did not see globally installed skills. | Resolved | Navigator discovers siblings from its executing packaged root and reports searched roots. A fresh host session may still be needed for the host registry. |
| Navigator recommended skills outside the current package. | Resolved for deterministic navigator | Required unavailable skills are blockers; optional actions are limited to discovered skills. Challenge host/model suggestions against `skill_roots`. |
| Local installation created an additional agent directory. | Clarified | `.agents/skills/` is the canonical project store. A host may create aliases or links. Inspect the CLI inventory, Git status, and symlinks; do not delete `.agents` as a duplicate. |
| Old skills are not automatically removed. | Accepted safety property | Reinstall cannot prove ownership or local modification. The update procedure produces retired inventory for review and never deletes by name alone. |
| Installation and updates differ between environments. | Resolved pattern | Commit project inventory and portable provenance; pin CLI and harness revision; promote one reviewed revision. Treat global installs as separate workstation state. |
| Navigator should always be used / wastes context. | Clarified | It is optional when the exact skill and lifecycle state are known. Use it for ambiguous entry, resume, or blockers; rely on durable state, not chat memory. |
| Skills can run in any order. | Corrected | Independent read-only lenses may run directly. Stateful lifecycle skills must respect predecessors, state, artifact authority, and gates. |
| Automation after a specification is unclear. | Resolved | Follow readiness → one ready task → validation → review/security → commit. Workflow plans do not execute; runtime requires reviewed plans and budgets. |
| Specifications in a separate repository were invisible. | Resolved | Keep discovery repository-bounded and use [external specification snapshots](../how-to/external-specifications.md) with hashes and drift checks. |
| Agent and script results require manual rechecking. | Confirmed control | Scripts validate narrow contracts; humans validate requirements, semantics, risk, code, and acceptance. Split work and rerun evidence after changes. |
| An unsafe command deleted files on a shared machine. | Confirmed risk | Verify `pwd`, branch, status, targets, and preview mode; reject untrusted cleanup commands; isolate parallel writes. |
| Token optimization and validation are needed. | Already supported | Context packs and runtime expose token/step/failure budgets and sufficiency. Budget success never substitutes for correctness. |
| Secrets need a proxy box. | Organizational decision | Keep secrets outside prompts and files. Integrate an approved vault/broker/proxy at the host boundary; the harness neither stores nor retrieves secrets. |
| Parallel language servers and fast Elixir indexing are needed; Dexter or grep was proposed. | Host/editor boundary | Select and benchmark tools through host/platform governance. The harness makes no Dexter or Elixir conformance claim, and index speed is not completeness evidence. |
| Subscription and client-cost limits need control. | Organizational decision with harness evidence | Define provider/seat thresholds in the pilot ledger. Token budgets and local metrics do not observe all subscription, support, or labor costs. |
| Teams need training and feedback. | Already supported | Use a bounded pilot, role onboarding, office hours, weekly evidence review, and retrospectives. Compare outputs with stable rubrics and human acceptance. |
| Unclear requests need refinement before PRFAQ/specification work. | Confirmed routing | Use discovery and business analysis, then package synthesis/readiness before SDD. Quick assumptions may not hide product decisions. |
| A skill installed for Claude but not Cursor. | External conformance blocker | Validate every host, operating system, and version independently; record exact target, scope, paths, restart, and list evidence. |

## Operational checklist

1. Prefer reviewed project scope for teams.
2. Start a fresh host session after changing capability inventory.
3. Inspect navigator `skill_roots` when discovery is disputed.
4. Keep specifications, decisions, plans, and evidence in Git.
5. Import external specifications through a reviewed snapshot.
6. Execute one bounded task at a time unless isolation is enforced.
7. Validate manually and deterministically before state completion.
8. Keep secrets in the approved external secret system.
9. Record token, subscription, training, correction, and support cost separately.
10. Route incidents and friction through a retrospective with an owner and acceptance test.

This register covers the supplied notes. New editor defects, provider changes,
security incidents, and workflow gaps require new evidence.
