---
title: Skill catalog
description: Every installed AI SDLC capability with a local human-facing guide, lifecycle position, module, outputs, and helper count.
---

# Skill catalog

This generated catalog is the public discovery surface for every installed capability. Each guide follows the same operating shape, while the linked `SKILL.md` remains execution authority.

<div class="grid cards" markdown>

-   **`ai-sdlc-approvals-sandbox`**

    `core` · Sandbox escalation decision · 1 package helper(s)

    Decide, request, and report sandbox escalation for AI SDLC commands only when the sandbox blocks a required action or the task explicitly requires approved external access.

    **Output:** Sandbox escalation decision record with prefix_rule guidance and residual risk

    [Open the complete guide →](skills/ai-sdlc-approvals-sandbox.md)

-   **`ai-sdlc-architecture`**

    `architecture` · Design and implementation planning · 1 package helper(s)

    Preserve traceable architecture boundaries, decisions, and risks.

    **Output:** `architecture.md` and `_ai_sdlc/architecture.toon`

    [Open the complete guide →](skills/ai-sdlc-architecture.md)

-   **`ai-sdlc-ba`**

    `core` · Business analysis and refinement · 1 package helper(s)

    Convert a vague AI SDLC feature, refactor, or workflow request into requirements-ready business context with actors, rules, assumptions, exclusions, and measurable acceptance criteria.

    **Output:** Business context, rules, assumptions, out-of-scope items, acceptance criteria, and open questions

    [Open the complete guide →](skills/ai-sdlc-ba.md)

-   **`ai-sdlc-backlog-decomposition-and-task-planning`**

    `core` · Backlog decomposition · 1 package helper(s)

    Convert planning structure into a delivery-oriented backlog with cross-functional work represented explicitly.

    **Output:** Features, user stories, acceptance summaries, and cross-functional delivery tasks

    [Open the complete guide →](skills/ai-sdlc-backlog-decomposition-and-task-planning.md)

-   **`ai-sdlc-backlog-requirements-gap-review`**

    `core` · Pre-backlog planning review · 1 package helper(s)

    Review the incoming initiative package and determine whether it is specific enough to support backlog decomposition and release planning.

    **Output:** Backlog-blocking gaps, assumptions, open questions, and readiness decision

    [Open the complete guide →](skills/ai-sdlc-backlog-requirements-gap-review.md)

-   **`ai-sdlc-branching`**

    `core` · Git workflow setup · 1 package helper(s)

    Create or verify the correct Git-flow task branch before repo-tracked file mutation, keep branch names aligned with active specs, and hand completed work to validation and commit prep without mixing unrelated changes.

    **Output:** Branching decision, branch name, base branch, dirty-tree assessment, and next handoff

    [Open the complete guide →](skills/ai-sdlc-branching.md)

-   **`ai-sdlc-change-impact`**

    `core` · Cross-lifecycle change recovery · 1 package helper(s)

    Trace changed sources to stale artifacts and safe reopen actions.

    **Output:** `change-impact.md` and `_ai_sdlc/change-impact.toon`

    [Open the complete guide →](skills/ai-sdlc-change-impact.md)

-   **`ai-sdlc-change-set`**

    `core` · Controlled change intake · 4 package helper(s)

    Create and validate an isolated, reviewable workspace before any authoritative specification mutation.

    **Output:** `changes/<change-id>/` with proposal, design, tasks, delta and evidence indexes, lifecycle records, preview, approval, and recovery evidence

    [Open the complete guide →](skills/ai-sdlc-change-set.md)

-   **`ai-sdlc-code-review`**

    `core` · Code review quality gate · 1 package helper(s)

    Review AI SDLC code, diffs, branches, commits, or completed implementations for correctness, regressions, contract drift, missing tests, SDD drift, and material maintainability risks.

    **Output:** Findings-first review with severity, path, impact, fix, validation gaps, and residual risk

    [Open the complete guide →](skills/ai-sdlc-code-review.md)

-   **`ai-sdlc-commit-prep`**

    `core` · Commit readiness / traceability · 1 package helper(s)

    Prepare and create a safe AI SDLC commit by reviewing the branch and working tree, staging only related files, validating SDD evidence, using a valid Conventional Commit message, and reporting post-commit traceability.

    **Output:** Safe staged set, validated commit readiness, conventional commit message, and post-commit traceability

    [Open the complete guide →](skills/ai-sdlc-commit-prep.md)

-   **`ai-sdlc-conventional-commit`**

    `core` · Commit message drafting · 1 package helper(s)

    Draft, validate, or repair an AI SDLC commit message that uses Conventional Commit syntax and includes SDD, business, implementation, testing, and validation traceability when the change is medium or large.

    **Output:** Conventional Commit subject/body with traceability and validation summary

    [Open the complete guide →](skills/ai-sdlc-conventional-commit.md)

-   **`ai-sdlc-delivery-graph`**

    `core` · Traceability and readiness · 2 package helper(s)

    Build a deterministic repository-wide lifecycle graph and answer trace, gap, coverage, and orphan questions from stable evidence anchors.

    **Output:** complete `_ai_sdlc/delivery-graph.toon` for agents, plus `_ai_sdlc/delivery-graph.json` for schema/interoperability and `_ai_sdlc/delivery-graph.md` for human review when `--write` is requested

    [Open the complete guide →](skills/ai-sdlc-delivery-graph.md)

-   **`ai-sdlc-delivery-handoff-review`**

    `core` · Engineering handoff quality gate · 1 package helper(s)

    Run the final quality gate on the delivery package before it is treated as ready for implementation planning or handoff.

    **Output:** Handoff readiness score, remaining blockers, contradictions, and execution risks

    [Open the complete guide →](skills/ai-sdlc-delivery-handoff-review.md)

-   **`ai-sdlc-delivery-package-gap-review`**

    `core` · Pre-delivery gap review · 1 package helper(s)

    Review an upstream discovery package and decide whether it is specific enough to decompose into delivery artifacts.

    **Output:** Delivery gaps, contradictions, missing business rules, and handoff blockers

    [Open the complete guide →](skills/ai-sdlc-delivery-package-gap-review.md)

-   **`ai-sdlc-delivery-spec-synthesis`**

    `core` · Delivery specification · 1 package helper(s)

    Convert the clarified package and story set into a structured delivery specification.

    **Output:** Structured delivery specification for engineering and cross-functional planning

    [Open the complete guide →](skills/ai-sdlc-delivery-spec-synthesis.md)

-   **`ai-sdlc-doctor`**

    `core` · Installation and upgrade operations · 1 package helper(s)

    Explain installation health and upgrade impact before mutation.

    **Output:** `_ai_sdlc/doctor/report.{toon,json,md}` or `_ai_sdlc/upgrades/<id>/plan.{toon,json,md}`

    [Open the complete guide →](skills/ai-sdlc-doctor.md)

-   **`ai-sdlc-evidence-council`**

    `evidence-council` · Cross-lifecycle high-impact review · 1 package helper(s)

    Combine multiple evidence perspectives while preserving authority.

    **Output:** `evidence-council.md` and `_ai_sdlc/evidence-council.toon`

    [Open the complete guide →](skills/ai-sdlc-evidence-council.md)

-   **`ai-sdlc-goal-capability-and-epic-mapping`**

    `core` · Planning architecture · 1 package helper(s)

    Turn a clarified initiative package into a structured planning model of goals, roles, capabilities, and epics.

    **Output:** Goal-to-capability map and outcome-oriented epics

    [Open the complete guide →](skills/ai-sdlc-goal-capability-and-epic-mapping.md)

-   **`ai-sdlc-host-adapter`**

    `core` · Portable execution handoff · 1 package helper(s)

    Preserve workflow semantics across hosts with explicit mappings and safe fallbacks.

    **Output:** `_ai_sdlc/adapters/<adapter-id>/negotiation.{toon,json,md}`

    [Open the complete guide →](skills/ai-sdlc-host-adapter.md)

-   **`ai-sdlc-navigator`**

    `core` · Cross-lifecycle navigation · 1 package helper(s)

    Inspect compact repository control records and recommend one ranked required action plus relevant optional actions with reasons, exact invocations, expected artifacts, and blockers.

    **Output:** Read-only Markdown or TOON navigation report

    [Open the complete guide →](skills/ai-sdlc-navigator.md)

-   **`ai-sdlc-package-trust`**

    `core` · Package trust and local observability · 2 package helper(s)

    Fail closed on untrusted packages and measure delivery without content collection.

    **Output:** `_ai_sdlc/trust/<package-id>/decision.{toon,json,md}` or `_ai_sdlc/metrics/local.{toon,json,md}`

    [Open the complete guide →](skills/ai-sdlc-package-trust.md)

-   **`ai-sdlc-policy`**

    `core` · Governance and control evaluation · 1 package helper(s)

    Resolve policy layers with provenance and evaluate actions against protected, versioned, waiver-aware rules.

    **Output:** `_ai_sdlc/policy-resolution.{toon,json}` or fingerprint-addressed TOON/JSON records below `_ai_sdlc/policy-decisions/` when `--write` is requested

    [Open the complete guide →](skills/ai-sdlc-policy.md)

-   **`ai-sdlc-prfaq-package-synthesis`**

    `core` · PRFAQ / business requirements synthesis · 1 package helper(s)

    Convert validated discovery notes into a decision-ready PRFAQ package and business requirements document.

    **Output:** PRFAQ, FAQ package, and BRD-style requirements summary

    [Open the complete guide →](skills/ai-sdlc-prfaq-package-synthesis.md)

-   **`ai-sdlc-project-context`**

    `core` · Cross-feature repository context · 2 package helper(s)

    Generate durable repository memory and task-specific, bounded, freshness-aware context from explained safe sources.

    **Output:** `project-context.md`, `_ai_sdlc/project-context.toon`, and optional topology and task-pack records below `_ai_sdlc/context/`

    [Open the complete guide →](skills/ai-sdlc-project-context.md)

-   **`ai-sdlc-qa`**

    `core` · QA planning and refinement · 1 package helper(s)

    Produce QA acceptance, regression, manual-check, and signoff evidence for AI SDLC changes and place QA refinement artifacts under `specs-refiniment/<feature-name>/<file.md>` when writing files.

    **Output:** QA acceptance plan, regression targets, manual checks, validation evidence, and residual risks

    [Open the complete guide →](skills/ai-sdlc-qa.md)

-   **`ai-sdlc-qa-requirements-gap-review`**

    `core` · Pre-QA requirements review · 1 package helper(s)

    Review the incoming delivery package and determine whether it is specific enough to support rigorous test design.

    **Output:** QA-blocking gaps, missing business rules, ambiguity, and testability risks

    [Open the complete guide →](skills/ai-sdlc-qa-requirements-gap-review.md)

-   **`ai-sdlc-qa-traceability-and-readiness-review`**

    `core` · QA execution readiness gate · 1 package helper(s)

    Run the final QA gate on the generated test pack before execution starts.

    **Output:** Requirements-to-test traceability matrix, coverage gaps, blockers, and readiness score

    [Open the complete guide →](skills/ai-sdlc-qa-traceability-and-readiness-review.md)

-   **`ai-sdlc-quality-lenses`**

    `core` · Cross-lifecycle quality review · 1 package helper(s)

    Apply reusable challenge lenses and finalize evidence-backed findings.

    **Output:** `quality-lens-report.md` and `_ai_sdlc/quality-lens-report.toon`

    [Open the complete guide →](skills/ai-sdlc-quality-lenses.md)

-   **`ai-sdlc-release-slicing-and-backlog-readiness-review`**

    `core` · Release planning / backlog readiness · 1 package helper(s)

    Run the final planning gate on the backlog package before estimation, roadmap slicing, or execution planning.

    **Output:** MVP/release slices, sequencing, readiness score, and planning risks

    [Open the complete guide →](skills/ai-sdlc-release-slicing-and-backlog-readiness-review.md)

-   **`ai-sdlc-requirements-readiness-review`**

    `core` · Requirements quality gate · 1 package helper(s)

    Run the final gate on a PRFAQ package and business requirements document before they are treated as ready for alignment or handoff.

    **Output:** Readiness score, blockers, contradictions, and required clarifications before design or development

    [Open the complete guide →](skills/ai-sdlc-requirements-readiness-review.md)

-   **`ai-sdlc-research`**

    `research` · Discovery, refinement, and design evidence · 1 package helper(s)

    Preserve questions, sources, findings, confidence, and limitations.

    **Output:** `research.md` and `_ai_sdlc/research.toon`

    [Open the complete guide →](skills/ai-sdlc-research.md)

-   **`ai-sdlc-retrospective`**

    `core` · Post-delivery learning · 1 package helper(s)

    Separate evidence-backed observations from governed improvements.

    **Output:** `retrospective.md` and `_ai_sdlc/retrospective.toon`

    [Open the complete guide →](skills/ai-sdlc-retrospective.md)

-   **`ai-sdlc-runtime`**

    `core` · Controlled execution · 1 package helper(s)

    Persist task selection and outcomes so interrupted delivery can resume without duplicate work or unsupported completion claims.

    **Output:** `_ai_sdlc/runs/<run-id>/journal.jsonl`, exact `state.json`, and complete token-efficient `state.toon`

    [Open the complete guide →](skills/ai-sdlc-runtime.md)

-   **`ai-sdlc-sdd`**

    `core` · Repository SDD workflow · 11 package helper(s)

    Create, update, validate, and enforce the AI SDLC SDD package for medium and large changes before implementation expands.

    **Output:** SDD package, Markdown execution plan, TOON machine plan, validation status, task alignment, and implementation handoff

    [Open the complete guide →](skills/ai-sdlc-sdd.md)

-   **`ai-sdlc-security-testing`**

    `core` · Security review / abuse-case validation · 1 package helper(s)

    Review AI SDLC diffs, endpoints, workflows, provider integrations, and configs for concrete security findings, abuse paths, trust-boundary failures, and missing security validation. When the output makes OWASP- or standards-based claims, verify them against current primary sources before presenting them as authoritative guidance.

    **Output:** Security findings, trust-boundary analysis, standards-backed notes, validation gaps, and fixes

    [Open the complete guide →](skills/ai-sdlc-security-testing.md)

-   **`ai-sdlc-shared-runtime`**

    `core` · Installation and cross-lifecycle runtime support · 17 package helper(s)

    Make the deterministic shared Python runtime portable when Skills CLI installs individual skill directories without the source-only `skills/_shared/` directory.

    **Output:** Read-only runtime verification or an explicit installation blocker

    [Open the complete guide →](skills/ai-sdlc-shared-runtime.md)

-   **`ai-sdlc-test-case-and-suite-synthesis`**

    `core` · Detailed test design · 1 package helper(s)

    Generate the detailed QA artifacts used for structured execution.

    **Output:** Executable test cases plus smoke, regression, and UAT suites

    [Open the complete guide →](skills/ai-sdlc-test-case-and-suite-synthesis.md)

-   **`ai-sdlc-test-cases`**

    `core` · Implementation test design · 1 package helper(s)

    Derive executable AI SDLC test scenarios from requirements or delivery context and place QA refinement artifacts under `specs-refiniment/<feature-name>/<file.md>` when writing files.

    **Output:** Scenario matrix with requirement refs, verifiable outcomes, automation paths, and execution order

    [Open the complete guide →](skills/ai-sdlc-test-cases.md)

-   **`ai-sdlc-test-scope-and-strategy-design`**

    `core` · QA strategy · 1 package helper(s)

    Turn a clarified delivery package into a structured QA scope and strategy.

    **Output:** QA scope, coverage priorities, suite strategy, data needs, and risk-based execution plan

    [Open the complete guide →](skills/ai-sdlc-test-scope-and-strategy-design.md)

-   **`ai-sdlc-user-story-decomposition`**

    `core` · Story decomposition · 1 package helper(s)

    Turn a clarified delivery package into implementable, actor-based user stories with acceptance logic and scenario coverage.

    **Output:** Epics, user stories, acceptance criteria, scenario coverage, and priority signals

    [Open the complete guide →](skills/ai-sdlc-user-story-decomposition.md)

-   **`ai-sdlc-ux`**

    `ux` · Discovery, refinement, and design · 1 package helper(s)

    Preserve testable journeys, states, recovery, and accessibility.

    **Output:** `ux-spec.md` and `_ai_sdlc/ux-spec.toon`

    [Open the complete guide →](skills/ai-sdlc-ux.md)

-   **`ai-sdlc-validation`**

    `core` · Implementation validation · 1 package helper(s)

    Select, run, and report focused deterministic validation checks for AI SDLC code, SQL, API, provider, SDD, documentation, and tool-governance changes.

    **Output:** Focused validation commands, outcomes, coverage notes, and residual risk

    [Open the complete guide →](skills/ai-sdlc-validation.md)

-   **`ai-sdlc-workflow`**

    `core` · Controlled execution planning · 1 package helper(s)

    Compile portable workflow intent into deterministic, gated, host-safe waves.

    **Output:** `_ai_sdlc/workflows/<workflow-id>/plan.{toon,json,md}`

    [Open the complete guide →](skills/ai-sdlc-workflow.md)

-   **`ai-sdlc-working-backwards-discovery`**

    `core` · Discovery / initiative framing · 1 package helper(s)

    Run the discovery interview that turns an initiative idea into a structured, business-grounded definition.

    **Output:** Structured discovery notes, clarified assumptions, open questions, and PRFAQ-ready facts

    [Open the complete guide →](skills/ai-sdlc-working-backwards-discovery.md)

</div>

Need an executable helper rather than a lifecycle guide? Use the [complete script reference](scripts.md).
