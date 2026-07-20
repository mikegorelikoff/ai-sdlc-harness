---
title: Skill catalog
description: Compact alphabetical inventory of every installed AI SDLC capability, its role views, lifecycle position, module, output, and canonical guide.
---

# Skill catalog

This compact alphabetical inventory links every installed capability to its canonical guide. If you know your responsibility rather than the skill name, start with [Skills by role](skills-by-role.md).

| Skill | Roles | Lifecycle position | Module | Output |
| --- | --- | --- | --- | --- |
| [`ai-sdlc-approvals-sandbox`](skills/ai-sdlc-approvals-sandbox.md) | Dev, Head of AI Practice | Sandbox escalation decision | `core` | Sandbox escalation decision record with prefix_rule guidance and residual risk |
| [`ai-sdlc-architecture`](skills/ai-sdlc-architecture.md) | Dev, Head of AI Practice | Design and implementation planning | `architecture` | `architecture.md` and `_ai_sdlc/architecture.toon` |
| [`ai-sdlc-ba`](skills/ai-sdlc-ba.md) | BA, PM, PO | Business analysis and refinement | `core` | Business context, rules, assumptions, out-of-scope items, acceptance criteria, and open questions |
| [`ai-sdlc-backlog-decomposition-and-task-planning`](skills/ai-sdlc-backlog-decomposition-and-task-planning.md) | BA, PM, PO | Backlog decomposition | `core` | Features, user stories, acceptance summaries, and cross-functional delivery tasks |
| [`ai-sdlc-backlog-requirements-gap-review`](skills/ai-sdlc-backlog-requirements-gap-review.md) | BA, PM, PO | Pre-backlog planning review | `core` | Backlog-blocking gaps, assumptions, open questions, and readiness decision |
| [`ai-sdlc-branching`](skills/ai-sdlc-branching.md) | Dev | Git workflow setup | `core` | Branching decision, branch name, base branch, dirty-tree assessment, and next handoff |
| [`ai-sdlc-change-impact`](skills/ai-sdlc-change-impact.md) | QA, BA, PM, PO, Dev, VP, Head of AI Practice | Cross-lifecycle change recovery | `core` | `change-impact.md` and `_ai_sdlc/change-impact.toon` |
| [`ai-sdlc-change-set`](skills/ai-sdlc-change-set.md) | Dev, Head of AI Practice | Controlled change intake | `core` | `changes/<change-id>/` with proposal, design, tasks, delta and evidence indexes, lifecycle records, preview, approval, and recovery evidence |
| [`ai-sdlc-code-review`](skills/ai-sdlc-code-review.md) | QA, Dev | Code review quality gate | `core` | Findings-first review with severity, path, impact, fix, validation gaps, and residual risk |
| [`ai-sdlc-commit-prep`](skills/ai-sdlc-commit-prep.md) | Dev | Commit readiness / traceability | `core` | Safe staged set, validated commit readiness, conventional commit message, and post-commit traceability |
| [`ai-sdlc-conventional-commit`](skills/ai-sdlc-conventional-commit.md) | Dev | Commit message drafting | `core` | Conventional Commit subject/body with traceability and validation summary |
| [`ai-sdlc-delivery-graph`](skills/ai-sdlc-delivery-graph.md) | QA, BA, PM, PO, Dev, VP, Head of AI Practice | Traceability and readiness | `core` | complete `_ai_sdlc/delivery-graph.toon` for agents, plus `_ai_sdlc/delivery-graph.json` for schema/interoperability and `_ai_sdlc/delivery-graph.md` for human review when `--write` is requested |
| [`ai-sdlc-delivery-handoff-review`](skills/ai-sdlc-delivery-handoff-review.md) | QA, BA, PM, PO, Dev, VP | Engineering handoff quality gate | `core` | Handoff readiness score, remaining blockers, contradictions, and execution risks |
| [`ai-sdlc-delivery-package-gap-review`](skills/ai-sdlc-delivery-package-gap-review.md) | BA, PM | Pre-delivery gap review | `core` | Delivery gaps, contradictions, missing business rules, and handoff blockers |
| [`ai-sdlc-delivery-spec-synthesis`](skills/ai-sdlc-delivery-spec-synthesis.md) | BA, PO, Dev | Delivery specification | `core` | Structured delivery specification for engineering and cross-functional planning |
| [`ai-sdlc-doctor`](skills/ai-sdlc-doctor.md) | Dev, VP, Head of AI Practice | Installation and upgrade operations | `core` | `_ai_sdlc/doctor/report.{toon,json,md}` or `_ai_sdlc/upgrades/<id>/plan.{toon,json,md}` |
| [`ai-sdlc-evidence-council`](skills/ai-sdlc-evidence-council.md) | QA, PM, Dev, VP, Head of AI Practice | Cross-lifecycle high-impact review | `evidence-council` | `evidence-council.md` and `_ai_sdlc/evidence-council.toon` |
| [`ai-sdlc-goal-capability-and-epic-mapping`](skills/ai-sdlc-goal-capability-and-epic-mapping.md) | BA, PM, VP | Planning architecture | `core` | Goal-to-capability map and outcome-oriented epics |
| [`ai-sdlc-host-adapter`](skills/ai-sdlc-host-adapter.md) | Dev, VP, Head of AI Practice | Portable execution handoff | `core` | `_ai_sdlc/adapters/<adapter-id>/negotiation.{toon,json,md}` |
| [`ai-sdlc-navigator`](skills/ai-sdlc-navigator.md) | QA, BA, PM, PO, Dev, VP, Head of AI Practice | Cross-lifecycle navigation | `core` | Read-only Markdown or TOON navigation report |
| [`ai-sdlc-package-trust`](skills/ai-sdlc-package-trust.md) | Dev, VP, Head of AI Practice | Package trust and local observability | `core` | `_ai_sdlc/trust/<package-id>/decision.{toon,json,md}` or `_ai_sdlc/metrics/local.{toon,json,md}` |
| [`ai-sdlc-policy`](skills/ai-sdlc-policy.md) | QA, PM, Dev, VP, Head of AI Practice | Governance and control evaluation | `core` | `_ai_sdlc/policy-resolution.{toon,json}` or fingerprint-addressed TOON/JSON records below `_ai_sdlc/policy-decisions/` when `--write` is requested |
| [`ai-sdlc-prfaq-package-synthesis`](skills/ai-sdlc-prfaq-package-synthesis.md) | BA, PM, PO, VP | PRFAQ / business requirements synthesis | `core` | PRFAQ, FAQ package, and BRD-style requirements summary |
| [`ai-sdlc-project-context`](skills/ai-sdlc-project-context.md) | Dev, Head of AI Practice | Cross-feature repository context | `core` | `project-context.md`, `_ai_sdlc/project-context.toon`, and optional topology and task-pack records below `_ai_sdlc/context/` |
| [`ai-sdlc-qa`](skills/ai-sdlc-qa.md) | QA, Dev | QA planning and refinement | `core` | QA acceptance plan, regression targets, manual checks, validation evidence, and residual risks |
| [`ai-sdlc-qa-requirements-gap-review`](skills/ai-sdlc-qa-requirements-gap-review.md) | QA, BA, PM, PO | Pre-QA requirements review | `core` | QA-blocking gaps, missing business rules, ambiguity, and testability risks |
| [`ai-sdlc-qa-traceability-and-readiness-review`](skills/ai-sdlc-qa-traceability-and-readiness-review.md) | QA, PO | QA execution readiness gate | `core` | Requirements-to-test traceability matrix, coverage gaps, blockers, and readiness score |
| [`ai-sdlc-quality-lenses`](skills/ai-sdlc-quality-lenses.md) | QA, BA, PM, PO, Dev, VP, Head of AI Practice | Cross-lifecycle quality review | `core` | `quality-lens-report.md` and `_ai_sdlc/quality-lens-report.toon` |
| [`ai-sdlc-release-slicing-and-backlog-readiness-review`](skills/ai-sdlc-release-slicing-and-backlog-readiness-review.md) | BA, PM, PO, VP | Release planning / backlog readiness | `core` | MVP/release slices, sequencing, readiness score, and planning risks |
| [`ai-sdlc-requirements-readiness-review`](skills/ai-sdlc-requirements-readiness-review.md) | QA, BA, PM, PO | Requirements quality gate | `core` | Readiness score, blockers, contradictions, and required clarifications before design or development |
| [`ai-sdlc-research`](skills/ai-sdlc-research.md) | BA, PM, Dev, VP, Head of AI Practice | Discovery, refinement, and design evidence | `research` | `research.md` and `_ai_sdlc/research.toon` |
| [`ai-sdlc-retrospective`](skills/ai-sdlc-retrospective.md) | PM, PO, Dev, VP, Head of AI Practice | Post-delivery learning | `core` | `retrospective.md` and `_ai_sdlc/retrospective.toon` |
| [`ai-sdlc-runtime`](skills/ai-sdlc-runtime.md) | Dev, Head of AI Practice | Controlled execution | `core` | `_ai_sdlc/runs/<run-id>/journal.jsonl`, exact `state.json`, and complete token-efficient `state.toon` |
| [`ai-sdlc-sdd`](skills/ai-sdlc-sdd.md) | QA, Dev | Repository SDD workflow | `core` | SDD package, Markdown execution plan, TOON machine plan, validation status, task alignment, and implementation handoff |
| [`ai-sdlc-security-testing`](skills/ai-sdlc-security-testing.md) | QA, Dev, Head of AI Practice | Security review / abuse-case validation | `core` | Security findings, trust-boundary analysis, standards-backed notes, validation gaps, and fixes |
| [`ai-sdlc-shared-runtime`](skills/ai-sdlc-shared-runtime.md) | Dev, Head of AI Practice | Installation and cross-lifecycle runtime support | `core` | Read-only runtime verification or an explicit installation blocker |
| [`ai-sdlc-test-case-and-suite-synthesis`](skills/ai-sdlc-test-case-and-suite-synthesis.md) | QA | Detailed test design | `core` | Executable test cases plus smoke, regression, and UAT suites |
| [`ai-sdlc-test-cases`](skills/ai-sdlc-test-cases.md) | QA, Dev | Implementation test design | `core` | Scenario matrix with requirement refs, verifiable outcomes, automation paths, and execution order |
| [`ai-sdlc-test-scope-and-strategy-design`](skills/ai-sdlc-test-scope-and-strategy-design.md) | QA, PO | QA strategy | `core` | QA scope, coverage priorities, suite strategy, data needs, and risk-based execution plan |
| [`ai-sdlc-user-story-decomposition`](skills/ai-sdlc-user-story-decomposition.md) | BA, PM, PO | Story decomposition | `core` | Epics, user stories, acceptance criteria, scenario coverage, and priority signals |
| [`ai-sdlc-ux`](skills/ai-sdlc-ux.md) | BA, PM, Dev | Discovery, refinement, and design | `ux` | `ux-spec.md` and `_ai_sdlc/ux-spec.toon` |
| [`ai-sdlc-validation`](skills/ai-sdlc-validation.md) | QA, Dev, Head of AI Practice | Implementation validation | `core` | Focused validation commands, outcomes, coverage notes, and residual risk |
| [`ai-sdlc-workflow`](skills/ai-sdlc-workflow.md) | Dev, VP, Head of AI Practice | Controlled execution planning | `core` | `_ai_sdlc/workflows/<workflow-id>/plan.{toon,json,md}` |
| [`ai-sdlc-working-backwards-discovery`](skills/ai-sdlc-working-backwards-discovery.md) | BA, PM, PO, VP | Discovery / initiative framing | `core` | Structured discovery notes, clarified assumptions, open questions, and PRFAQ-ready facts |

Role labels are discovery aids, not exclusive ownership. A skill can support several roles while retaining one source contract and one guide. Need an executable helper instead? Use the [complete script reference](scripts.md).
