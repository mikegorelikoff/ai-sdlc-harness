---
title: Skills.sh security audit reconciliation — 2026-07-21
description: Provider-by-provider review and source remediation for all 44 published AI SDLC skills.
---

# Skills.sh security audit reconciliation — 2026-07-21

## Scope and method

The review queried the live Skills.sh audit API for every skill published from
`mikegorelikoff/ai-sdlc-harness`, then inspected each reported path in local
candidate `989d88dfe292f97f6675abe0ecf3d789b9c8d807`. Provider results are
revision-specific scanner evidence: they identify review targets but do not by
themselves prove exploitability or prove that a later source correction has
been rescanned.

The API contract and provider/status meanings come from the
[Skills.sh API documentation](https://skills.sh/docs/api). The marketplace also
states that audits reduce risk but cannot guarantee safety; consumers must keep
human review and least-privilege controls
([Skills.sh security guidance](https://skills.sh/docs)).

## Result

- Skills reviewed: **44 of 44**.
- Provider results reviewed: **132** across Gen Agent Trust Hub, Socket, and Snyk.
- Skills with no warning or failure: **33**.
- Skills with at least one warning or failure: **11**.
- Confirmed remediation themes: credential redaction; indirect prompt-injection
  boundaries; bounded local shared-runtime loading; removal of target-root
  Python execution from compatibility validation.
- External status: a new marketplace scan is still required after this candidate
  is committed and published. This repository cannot rewrite old provider results.

Legend: `PASS`; `WARN-M` (Medium); `WARN-L` (Low); `FAIL-H` (High).
Each skill name links to its live marketplace entry.

## All-skills provider matrix

| Skill | Agent Trust Hub | Socket | Snyk | Local disposition |
| --- | --- | --- | --- | --- |
| [ai-sdlc-approvals-sandbox](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-approvals-sandbox) | PASS | PASS | FAIL-H | Confirmed W007; fixed mandatory pre-record redaction and no-echo behavior. |
| [ai-sdlc-architecture](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-architecture) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-ba](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-ba) | WARN-M | PASS | PASS | Bounded packaged imports, removed dynamic test import, added untrusted-input boundary. |
| [ai-sdlc-backlog-decomposition-and-task-planning](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-backlog-decomposition-and-task-planning) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-backlog-requirements-gap-review](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-backlog-requirements-gap-review) | PASS | PASS | WARN-M | Confirmed W011 exposure; added explicit data-only boundary and source handling rules. |
| [ai-sdlc-branching](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-branching) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-change-impact](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-change-impact) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-change-set](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-change-set) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-code-review](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-code-review) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-commit-prep](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-commit-prep) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-conventional-commit](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-conventional-commit) | WARN-M | PASS | PASS | Bounded packaged imports, removed dynamic test import, added untrusted-input boundary. |
| [ai-sdlc-delivery-graph](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-delivery-graph) | PASS | PASS | WARN-M | Confirmed W011 exposure; graph output now declares repository/Git text untrusted. |
| [ai-sdlc-delivery-handoff-review](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-delivery-handoff-review) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-delivery-package-gap-review](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-delivery-package-gap-review) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-delivery-spec-synthesis](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-delivery-spec-synthesis) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-doctor](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-doctor) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-evidence-council](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-evidence-council) | PASS | PASS | WARN-M | Confirmed W011 exposure; raw reviewer collection replaced by normalized, delimited evidence. |
| [ai-sdlc-goal-capability-and-epic-mapping](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-goal-capability-and-epic-mapping) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-host-adapter](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-host-adapter) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-navigator](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-navigator) | PASS | PASS | WARN-M | Confirmed W011 exposure; schema fields route work, free text cannot grant authority. |
| [ai-sdlc-package-trust](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-package-trust) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-policy](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-policy) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-prfaq-package-synthesis](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-prfaq-package-synthesis) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-project-context](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-project-context) | PASS | PASS | WARN-M | Confirmed W011 exposure; excerpts/commands are explicitly untrusted evidence. |
| [ai-sdlc-qa](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-qa) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-qa-requirements-gap-review](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-qa-requirements-gap-review) | PASS | PASS | WARN-M | Confirmed W011 exposure; requirements are data-only and unsafe portions block review. |
| [ai-sdlc-qa-traceability-and-readiness-review](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-qa-traceability-and-readiness-review) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-quality-lenses](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-quality-lenses) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-release-slicing-and-backlog-readiness-review](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-release-slicing-and-backlog-readiness-review) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-requirements-readiness-review](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-requirements-readiness-review) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-research](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-research) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-retrospective](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-retrospective) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-runtime](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-runtime) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-sdd](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-sdd) | PASS | PASS | WARN-M | Confirmed W011 exposure; refinement context is delimited untrusted evidence. |
| [ai-sdlc-security-testing](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-security-testing) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-shared-runtime](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-shared-runtime) | PASS | WARN-L | PASS | Confirmed architectural risk; compatibility no longer executes target-root Python and bounds Git. |
| [ai-sdlc-test-case-and-suite-synthesis](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-test-case-and-suite-synthesis) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-test-cases](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-test-cases) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-test-scope-and-strategy-design](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-test-scope-and-strategy-design) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-user-story-decomposition](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-user-story-decomposition) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-ux](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-ux) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-validation](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-validation) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-workflow](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-workflow) | PASS | PASS | PASS | No provider challenge. |
| [ai-sdlc-working-backwards-discovery](https://www.skills.sh/mikegorelikoff/ai-sdlc-harness/ai-sdlc-working-backwards-discovery) | PASS | PASS | PASS | No provider challenge. |

## Finding reconciliation

| Finding | Classification | Evidence | Correction | Acceptance evidence |
| --- | --- | --- | --- | --- |
| Snyk W007, approvals credential handling | Confirmed issue, High | The skill required the “exact command” in its output while only failing later when secrets were present. | Require redaction before capture, prompting, tool use, logging, or output; prohibit echoing the unsafe original. | `test_marketplace_security.py` checks the independent skill contract. |
| Snyk W011 across seven content-consuming skills | Confirmed issue, Medium | Skills consume requirements, repository text, Git bodies, state, or reviewer content but lacked a local explicit indirect-injection rule. | Add data-only trust boundaries, source anchors, no embedded command execution, secret exclusion, and human escalation. | Security-contract test covers every provider-flagged content skill; generated context/council/graph outputs carry trust markers. |
| Agent Trust Hub BA and commit dynamic loading | Probable issue, Medium | Packaged scripts add an exact shared-runtime directory to `sys.path`; tests dynamically imported the shared contract. No network retrieval was present. | Bound runtime resolution beneath the installed skills root and require exact helper files; replace dynamic test imports with a fixed subprocess contract. | BA and conventional-commit skill suites pass from the packaged paths. |
| Socket shared-runtime `gptAnomaly` | Confirmed issue, High locally despite provider Low | Compatibility ran every discovered Python CLI with `--help`, ran target tests/helpers, and invoked Git through an unresolved name. An attacker-controlled target root could execute top-level code. | Replace Python execution with static flag inspection, static module validation, and byte comparison; resolve Git to an absolute executable outside the target root. | A malicious target fixture writes a marker at import time; compatibility passes without creating the marker. |

## Residual limitations and rescan procedure

The source corrections do not retroactively alter a Skills.sh audit snapshot.
After committing and publishing the candidate, trigger or wait for provider
rescans, verify that each record references the new revision, and reconcile any
remaining warning by its exact path and rule. A provider may continue to warn on
intentional local command execution or defensive `sys.path` setup; such a warning
must remain documented unless the provider confirms the bounded behavior.

Regardless of scanner status, install skills only from a reviewed revision,
inspect requested commands, keep secrets out of prompts and command arguments,
and grant the least filesystem/network authority required for one task.
