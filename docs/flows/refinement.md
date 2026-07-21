---
title: Complete refinement flow
description: Follow the canonical 18-stage route from customer problem to an implementation-ready delivery and QA handoff.
---

# Complete refinement flow

Refinement turns an initial product signal into an implementation-ready package
under `specs-refiniment/<feature>/`. It is appropriate when the customer
problem, business behavior, planning, QA, or cross-functional ownership still
needs deliberate work.

Use `--full-flow` when one selected stage needs its strict question, evidence,
and quality gates. The flag strengthens only that skill and never starts the
next one. A complete 18-stage lifecycle exists only when the user or a declared
workflow explicitly sequences all 18 skills and accepts each handoff.

## Exact stage contract

| # | Stage ID | Exact skill | Exact predecessor stage IDs | Accountable | Artifact | Exit / reopen signal |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `discovery` | `ai-sdlc-working-backwards-discovery` | none | Product manager | `discovery.md` | Problem, value, audience, scope, and evidence clear; reopen on new problem evidence. |
| 2 | `prfaq` | `ai-sdlc-prfaq-package-synthesis` | `discovery` | Product manager | `prfaq.md` | Promise, FAQ, business requirements, and risks coherent; reopen on contradiction. |
| 3 | `delivery_package_gap_review` | `ai-sdlc-delivery-package-gap-review` | `prfaq` | Product manager | `delivery-gap-review.md` | Blocking gaps owned/resolved; reopen on a missing workflow or rule. |
| 4 | `requirements_readiness` | `ai-sdlc-requirements-readiness-review` | `delivery_package_gap_review` | Product manager | `requirements-readiness.md` | Ready for planning/QA; reopen on ambiguous scope or actor. |
| 5 | `goal_epic_mapping` | `ai-sdlc-goal-capability-and-epic-mapping` | `requirements_readiness` | Product manager | `goal-capability-map.md` | Outcomes trace to capabilities/epics; reopen on missing value or owner. |
| 6 | `backlog_gap_review` | `ai-sdlc-backlog-requirements-gap-review` | `goal_epic_mapping` | Product manager | `backlog-gap-review.md` | Planning gaps/dependencies resolved; reopen on priority or sequence conflict. |
| 7 | `backlog_decomposition` | `ai-sdlc-backlog-decomposition-and-task-planning` | `backlog_gap_review` | Product manager | `backlog.md` | Epics/stories/tasks bounded and ready; reopen on oversized or unowned work. |
| 8 | `story_decomposition` | `ai-sdlc-user-story-decomposition` | `backlog_decomposition` | Product manager | `user-stories.md` | Stories, acceptance, scenarios, and dependencies ready; reopen on a rule gap. |
| 9 | `release_slicing` | `ai-sdlc-release-slicing-and-backlog-readiness-review` | `backlog_decomposition` | Product manager | `release-slicing.md` | MVP/releases have value and exit criteria; reopen on dependency/rollout change. |
| 10 | `ba_context` | `ai-sdlc-ba` | `story_decomposition` | Product manager | `business-context.md` | Actors, permissions, workflows, rules, and acceptance explicit; reopen on behavior gap. |
| 11 | `delivery_spec` | `ai-sdlc-delivery-spec-synthesis` | `ba_context` | Engineering lead | `delivery-spec.md` | Implementation-facing behavior complete; reopen on a handoff gap. |
| 12 | `qa_plan` | `ai-sdlc-qa` | `requirements_readiness` | QA owner | `qa.md` | Acceptance, risks, environments, evidence, and signoff scoped; reopen on an untestable rule. |
| 13 | `qa_gap_review` | `ai-sdlc-qa-requirements-gap-review` | `qa_plan` | QA owner | `qa-gap-review.md` | Testability gaps resolved/owned; reopen on missing negative/data/environment paths. |
| 14 | `test_strategy` | `ai-sdlc-test-scope-and-strategy-design` | `qa_gap_review` | QA owner | `qa-strategy.md` | Layers, suites, data, automation, and priorities accepted; reopen on risk change. |
| 15 | `test_cases` | `ai-sdlc-test-cases` | `test_strategy` | QA owner | `test-cases.md` | Positive/negative/permission cases trace to requirements; reopen on ambiguity. |
| 16 | `test_suite` | `ai-sdlc-test-case-and-suite-synthesis` | `test_cases` | QA owner | `test-suite.md` | Smoke/regression/UAT sets and entry/exit criteria defined; reopen on coverage change. |
| 17 | `qa_traceability` | `ai-sdlc-qa-traceability-and-readiness-review` | `test_suite` | QA owner | `qa-readiness.md` | Coverage and execution dependencies ready; reopen on stale or missing evidence. |
| 18 | `delivery_handoff` | `ai-sdlc-delivery-handoff-review` | `delivery_spec`, `qa_traceability` | Engineering lead | `delivery-handoff-review.md` | Owners, decisions, dependencies, and implementation inputs accepted; reopen on any blocker. |

Stage 9 is optional for a focused flow but required—or explicitly represented
as evidence-backed N/A—for a declared complete 18-stage cascade.

## Parallel branches

After `requirements_readiness`, product/backlog work and `qa_plan` can progress
in parallel. `delivery_handoff` joins the branches: its exact predecessors are
`delivery_spec` and `qa_traceability`. Parallel work never means two agents may
edit the same artifact concurrently or bypass a predecessor.

## How an agent executes the cascade

For each stage the agent reads state, decision log, specs index, predecessor,
and targeted context; begins durable state only when writing starts; uses the
stage scaffold; finalizes quality; records decisions; completes state; refreshes
indexes; and returns the common handoff. It resumes from the earliest blocking
stage rather than trusting chat history.

## Completion and recovery

The strict completion gate requires 18/18 state, canonical artifacts, full-flow
metadata, and blocking quality checks. State without artifact evidence does not
pass. An artifact without completed state is validated before repair. Divergent
legacy/canonical files block until migration analysis resolves them.

Next consumer: [Implementation SDD](implementation.md).
