---
title: Skill catalog
description: Every installed AI SDLC skill, its purpose, owning module, and authoritative package path.
---

# Skill catalog

This page is generated from each package's `SKILL.md` frontmatter. The linked source is the authoritative execution contract.

<div class="grid cards" markdown>

-   **`ai-sdlc-approvals-sandbox`**

    `core`

    AI SDLC approvals, sandbox, and command rule workflow. Use when an AI assistant needs to decide whether to request escalated permissions, explain sandbox failures, propose prefix_rule approvals, avoid unsafe command patterns, or document why a command was or was not rerun outside the sandbox. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-approvals-sandbox/SKILL.md)

-   **`ai-sdlc-architecture`**

    `architecture`

    Optional AI SDLC architecture workflow. Use when an AI assistant needs to define system boundaries, components, interfaces, architectural constraints, alternatives, decisions, tradeoffs, risks, or validation for a feature and produce routed human and machine artifacts linked to requirements and durable decisions. Supports `--quick-flow` for focused design and `--full-flow` for strict decision, risk, and validation coverage.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-architecture/SKILL.md)

-   **`ai-sdlc-ba`**

    `core`

    AI SDLC business analysis workflow. Use when an AI assistant needs to frame a feature or change before implementation, derive actors, workflows, business rules, assumptions, acceptance criteria, and richer spec context for requirements and design. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-ba/SKILL.md)

-   **`ai-sdlc-backlog-decomposition-and-task-planning`**

    `core`

    Use when goals, capabilities, and epics are defined and you need to decompose them into features, user stories, acceptance summaries, and cross-functional delivery tasks. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-backlog-decomposition-and-task-planning/SKILL.md)

-   **`ai-sdlc-backlog-requirements-gap-review`**

    `core`

    Use when PRFAQ, BRD, PRD, product brief, workflow, or equivalent initiative artifacts exist and you need to review them for planning gaps, unclear scope, weak priorities, missing actors, and backlog-blocking ambiguity before decomposing work. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-backlog-requirements-gap-review/SKILL.md)

-   **`ai-sdlc-branching`**

    `core`

    AI SDLC Git-flow branching workflow. Use when an AI assistant starts implementation work, needs to create or verify a task branch, checks branch/spec alignment, or prepares to hand off a completed user-visible task to validation and commit prep. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-branching/SKILL.md)

-   **`ai-sdlc-change-impact`**

    `core`

    AI SDLC change-impact and lifecycle recovery workflow. Use when a requirement, acceptance criterion, decision, API contract, risk assumption, or other traced source changed after downstream artifacts were created and an AI assistant must identify stale artifacts, affected lifecycle stages, and evidence-backed reopen or revalidation actions without silently rewriting authoritative state. Supports `--quick-flow` for focused trace scanning and `--full-flow` for strict state and source-evidence gates.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-impact/SKILL.md)

-   **`ai-sdlc-change-set`**

    `core`

    AI SDLC controlled change-workspace and specification-delta workflow. Use when an AI assistant needs to create or validate an isolated proposal workspace, author and validate requirement deltas, preview canonical changes, or apply and archive an explicitly approved change with rollback evidence. Supports `--quick-flow` for assumption-driven drafts and `--full-flow` for strict owner, target, evidence, and authority checks.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-set/SKILL.md)

-   **`ai-sdlc-code-review`**

    `core`

    AI SDLC code review workflow. Use when an AI assistant is asked to review a diff, PR, branch, commit, staged changes, or completed implementation against SDD requirements, tests, API contracts, security, and scope discipline. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-code-review/SKILL.md)

-   **`ai-sdlc-commit-prep`**

    `core`

    AI SDLC commit preparation workflow. Use when an AI assistant is asked to commit repository changes, prepare an auditable commit message, stage files safely, include SDD traceability, verify branch/spec alignment, or verify the working tree before committing. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-commit-prep/SKILL.md)

-   **`ai-sdlc-conventional-commit`**

    `core`

    AI SDLC Conventional Commit workflow. Use when an AI assistant drafts, validates, reviews, or fixes commit messages in this repository, especially when commits must include SDD spec references, validation summaries, or safe conventional commit subjects. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-conventional-commit/SKILL.md)

-   **`ai-sdlc-delivery-graph`**

    `core`

    AI SDLC repository delivery-graph and evidence-freshness workflow. Use when an AI assistant needs to index lifecycle traceability, resolve end-to-end paths, report gaps or orphans, register evidence identity, propagate stale dependencies, or calculate fresh evidence coverage. Supports `--quick-flow` for deterministic local analysis and `--full-flow` for strict trace and evidence review.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-delivery-graph/SKILL.md)

-   **`ai-sdlc-delivery-handoff-review`**

    `core`

    Use after story and spec synthesis to perform a strict delivery handoff review, identify remaining gaps or contradictions, and score readiness for engineering and cross-functional execution. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-delivery-handoff-review/SKILL.md)

-   **`ai-sdlc-delivery-package-gap-review`**

    `core`

    Use when a PRFAQ, BRD, or equivalent discovery package exists and you need to review it for delivery gaps, contradictions, missing business rules, and insufficient implementation handoff detail before writing user stories or specs. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-delivery-package-gap-review/SKILL.md)

-   **`ai-sdlc-delivery-spec-synthesis`**

    `core`

    Use when stories and clarified delivery context are ready and you need to produce a structured delivery specification that engineering and cross-functional teams can use for implementation planning and handoff. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-delivery-spec-synthesis/SKILL.md)

-   **`ai-sdlc-evidence-council`**

    `evidence-council`

    Optional AI SDLC evidence-council workflow. Use when an AI assistant needs to review a high-impact topic through several explicit perspectives, orchestrate simulated lenses or truly independent reviewer executions, and synthesize evidence-backed agreements, conflicts, proposals, owners, and unresolved questions without allowing panel members to rewrite authoritative artifacts. Supports `--quick-flow` for labeled simulated review and `--full-flow` for stricter panel and evidence coverage.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-evidence-council/SKILL.md)

-   **`ai-sdlc-goal-capability-and-epic-mapping`**

    `core`

    Use when planning inputs are clear enough and you need to map business goals, roles, capabilities, and outcome-oriented epics before detailed backlog decomposition. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-goal-capability-and-epic-mapping/SKILL.md)

-   **`ai-sdlc-navigator`**

    `core`

    AI SDLC context-aware navigation workflow. Use when an AI assistant needs to determine what to do next, select the right installed skill, start or resume a feature, explain blockers, inspect available capabilities, or provide evidence-backed required and optional next actions from repository state. Supports `--quick-flow` for compact guidance and `--full-flow` for stricter context verification.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-navigator/SKILL.md)

-   **`ai-sdlc-policy`**

    `core`

    AI SDLC versioned policy-as-code workflow. Use when an AI assistant needs to resolve layered delivery policy, evaluate an action with explainable rules and gates, protect organization minimums from weaker overrides, apply or reject an expiring waiver, or select a reusable assurance profile. Supports `--quick-flow` for deterministic evaluation and `--full-flow` for strict owner and exception review.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-policy/SKILL.md)

-   **`ai-sdlc-prfaq-package-synthesis`**

    `core`

    Use when working-backwards discovery is complete and you need to synthesize a PRFAQ, FAQ package, and business requirements document tied to business value, scenarios, and testable acceptance logic. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-prfaq-package-synthesis/SKILL.md)

-   **`ai-sdlc-project-context`**

    `core`

    AI SDLC evidence-backed project context and bounded task-pack workflow. Use when an AI assistant needs to onboard to a repository, detect stack and commands, map ownership and test topology, check context drift, conditionally select task sources, exclude secrets, or allocate a freshness-aware context pack within an explicit token budget. Supports `--quick-flow` for focused evidence and `--full-flow` for stricter repository coverage.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-project-context/SKILL.md)

-   **`ai-sdlc-qa`**

    `core`

    AI SDLC QA workflow. Use when an AI assistant is asked for QA planning, acceptance validation, regression scope, exploratory checks, smoke tests, release verification, or change-focused manual validation evidence. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-qa/SKILL.md)

-   **`ai-sdlc-qa-requirements-gap-review`**

    `core`

    Use when stories, specs, BRDs, APIs, workflows, or equivalent delivery artifacts exist and you need to review them for testability, missing business rules, unclear behavior, scope ambiguity, and QA blocking gaps before generating tests. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-qa-requirements-gap-review/SKILL.md)

-   **`ai-sdlc-qa-traceability-and-readiness-review`**

    `core`

    Use after QA strategy and test-case synthesis to build the requirements-to-test traceability matrix, identify missing coverage and test blockers, and score readiness for QA execution. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-qa-traceability-and-readiness-review/SKILL.md)

-   **`ai-sdlc-quality-lenses`**

    `core`

    AI SDLC reusable quality-lens workflow. Use when an AI assistant needs to challenge a requirement, design, plan, test strategy, change, or delivery artifact through pre-mortem, adversarial, edge-case, stakeholder-conflict, reversibility, abuse-case, operational-failure, or assumption lenses and finalize evidence-backed findings with ownership and traceability. Supports `--quick-flow` for selected high-value lenses and `--full-flow` for the complete applicable registry.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-quality-lenses/SKILL.md)

-   **`ai-sdlc-release-slicing-and-backlog-readiness-review`**

    `core`

    Use after backlog decomposition to define prioritization, MVP and release slices, sequencing, readiness, traceability, and JIRA-ready outputs, then score backlog quality for planning and estimation. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-release-slicing-and-backlog-readiness-review/SKILL.md)

-   **`ai-sdlc-requirements-readiness-review`**

    `core`

    Use after PRFAQ and BRD creation to run a strict final quality review, identify gaps or contradictions, and assign a readiness score before design or development starts. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-requirements-readiness-review/SKILL.md)

-   **`ai-sdlc-research`**

    `research`

    Optional AI SDLC research workflow. Use when an AI assistant needs to investigate a customer, market, domain, technology, regulation, competitor, operational question, or implementation uncertainty and produce a routed source inventory plus synthesized findings with confidence, limitations, open questions, and delivery trace targets. Supports `--quick-flow` for focused evidence and `--full-flow` for multi-source and source-diversity gates.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-research/SKILL.md)

-   **`ai-sdlc-retrospective`**

    `core`

    AI SDLC evidence-backed retrospective workflow. Use when delivery work is complete or paused and an AI assistant needs to capture observations, connect them to validation or artifact evidence, formulate reviewable process or policy improvement proposals, assign ownership, and preserve the rule that policy changes require an accepted decision. Supports `--quick-flow` for focused learning and `--full-flow` for strict evidence and decision gates.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-retrospective/SKILL.md)

-   **`ai-sdlc-runtime`**

    `core`

    AI SDLC resumable task-runtime workflow. Use when an AI assistant needs to start or resume a versioned delivery run, select dependency-ready work, enforce step, failure, and token budgets, retry safely, persist exact stop reasons, recover state from an append-only journal, or require commit evidence at task boundaries. Supports `--quick-flow` for deterministic local runs and `--full-flow` for strict transition review.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-runtime/SKILL.md)

-   **`ai-sdlc-sdd`**

    `core`

    AI SDLC repository spec-driven development workflow. Use when an AI assistant receives a medium or large feature, refactor, API change, architecture change, provider integration change, or any request that must follow requirements, design, test cases, QA planning, tasks, implementation, and validation. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/SKILL.md)

-   **`ai-sdlc-security-testing`**

    `core`

    AI SDLC security testing workflow. Use when an AI assistant is asked for OWASP review, security testing, abuse-case analysis, authz/authn review, input validation review, secret exposure review, or security-focused validation of a diff, endpoint, workflow, or subsystem. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-security-testing/SKILL.md)

-   **`ai-sdlc-test-case-and-suite-synthesis`**

    `core`

    Use when QA scope and strategy are defined and you need to generate detailed, executable test cases plus smoke, regression, and user acceptance suites tied to requirements, roles, workflows, and risks. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-test-case-and-suite-synthesis/SKILL.md)

-   **`ai-sdlc-test-cases`**

    `core`

    AI SDLC test-case-driven testing workflow. Use when an AI assistant is asked to derive test cases, create a test plan, expand coverage, or write tests from explicit scenarios before implementing unit, service, transport, or integration tests. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-test-cases/SKILL.md)

-   **`ai-sdlc-test-scope-and-strategy-design`**

    `core`

    Use when requirements are testable enough and you need to define QA scope, coverage priorities, test strategy, suite intent, test data needs, environment dependencies, and risk-based execution focus. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-test-scope-and-strategy-design/SKILL.md)

-   **`ai-sdlc-user-story-decomposition`**

    `core`

    Use when the delivery gap review is complete and you need to convert a clarified initiative package into epics, user stories, acceptance criteria, scenario coverage, and priority signals tied to business value. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-user-story-decomposition/SKILL.md)

-   **`ai-sdlc-ux`**

    `ux`

    Optional AI SDLC user-experience workflow. Use when an AI assistant needs to define actors, goals, user journeys, interaction steps, loading/empty/error/success states, recovery behavior, content intent, accessibility requirements, or UX acceptance evidence and route them into traceable human and machine artifacts. Supports `--quick-flow` for a focused journey slice and `--full-flow` for strict state, accessibility, and acceptance coverage.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-ux/SKILL.md)

-   **`ai-sdlc-validation`**

    `core`

    AI SDLC backend validation workflow. Use when an AI assistant needs to validate Go, SQL, API, provider integration, SDD, or documentation changes in this repository and choose focused deterministic checks without running unrelated expensive tests by default. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/SKILL.md)

-   **`ai-sdlc-workflow`**

    `core`

    AI SDLC declarative workflow planning. Use when an AI assistant needs to validate a versioned workflow, plan typed dependency steps, evaluate bounded conditions, enforce approval gates, attach deterministic hooks, detect cycles, or create safe dependency waves with sequential fallback when host concurrency or isolation is unavailable. Supports `--quick-flow` and `--full-flow`.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-workflow/SKILL.md)

-   **`ai-sdlc-working-backwards-discovery`**

    `core`

    Use when a user needs a staged working-backwards interview to clarify the customer problem, audience, value proposition, business case, MVP, requirements, risks, and success metrics before any PRFAQ is written. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-working-backwards-discovery/SKILL.md)

</div>
