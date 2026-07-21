---
title: Glossary
description: Canonical definitions for AI SDLC, SDD, lifecycle roles, artifacts, controls, state, and representation terms.
---

# Glossary

| Term | Meaning in this harness |
| --- | --- |
| Acceptance criterion (AC) | Observable condition that must be true for a requirement to be accepted. |
| Adoption owner | Human accountable for pilot scope, evidence, stop/scale decision, and rollout proposal. |
| Agent | AI assistant acting through available tools and selected skill instructions. |
| Artificial intelligence (AI) | Software techniques that perform tasks associated with perception, prediction, language, reasoning, or generation; capability and limits depend on the system and evidence. |
| AI SDLC | A software development lifecycle expressed as durable evidence, bounded agent capabilities, deterministic helpers, explicit state, and human authority. |
| Artifact | Repository file that preserves delivery context or evidence, such as requirements, design, QA, decisions, or plans. |
| BA | Business analyst role responsible for rules, workflows, actors, and testable business behavior. |
| Blocker | Missing decision, evidence, permission, capability, or valid predecessor that prevents safe continuation. |
| BRD | Business requirements document describing business context, rules, scope, actors, constraints, and acceptance logic. |
| Capability | A bounded operation an installed skill, module, adapter, or host can support. |
| Command-line interface (CLI) | Text interface used to invoke a program from a terminal. |
| Change set | Isolated proposal workspace used to preview and approve specification changes before canonical apply. |
| Command | An instruction executed by a shell or tool; unlike an agent prompt, it can directly affect the local or external environment according to granted permissions. |
| Continuous integration (CI) | Automated checks run when changes are proposed or pushed so integration problems are detected before release. |
| Confabulation / hallucination | Plausible but false, unsupported, or internally inconsistent generated output. This documentation prefers *confabulation* for the risk and retains *hallucination* as the widely used synonym. |
| Context | Information available to a model for the current interaction, including prompts, selected repository evidence, tool results, and host instructions. |
| Context window | Bounded amount of tokenized input and output a model can process in one interaction. |
| Control plane | Policy, state, runtime, graph, context, adapter, trust, and recovery mechanisms that coordinate delivery without replacing authoritative artifacts. |
| Consumer repository | Software project receiving installed skills and preserving its own delivery artifacts; not the harness source checkout. |
| Decision log | Markdown record of material choices, context, options, owner, status, affected artifacts, and validation links. |
| Delivery | Role accountable for coordination, readiness, handoff, ownership, and release confidence. |
| Drift | Difference between a stored identity/projection and current authoritative source content. |
| Evidence | Inspectable proof supporting a delivery claim, including source anchors, tests, reviews, approvals, commands, outcomes, and commits. |
| Generative artificial intelligence | AI that produces new text, code, images, or other content from learned statistical patterns and supplied context. |
| Fingerprint | Deterministic hash identifying normalized content or a derived record. |
| Flow | Ordered connection of skills, evidence, gates, and handoffs toward an outcome. |
| Freshness | Whether evidence still matches its artifacts, dependencies, time bounds, and upstream evidence. |
| Full flow | Strict execution mode for one selected skill; it verifies prerequisites and decisions but does not automatically run the entire lifecycle. |
| Gate | Condition that must be satisfied before a transition, mutation, approval, or completion claim. |
| Handoff | Versioned result containing outcome, blockers, required next action, and optional next actions. |
| Harness | Repository-native system of skills, helpers, artifacts, state, and controls that makes AI-assisted delivery repeatable and inspectable. |
| Human checkpoint | Point where accountable human review, decision, approval, or risk acceptance is required. |
| Integrated development environment (IDE) | Application that combines code editing with capabilities such as navigation, debugging, tests, and version-control integration. |
| Large language model (LLM) | Model trained on large text or code corpora to predict token sequences and perform language-oriented tasks. |
| Machine learning (ML) | AI approach in which behavior is learned from data or experience rather than expressed only as hand-written rules. |
| Module | Versioned compatible group of core or optional skills. |
| `npx` | npm package runner used here to execute the pinned third-party Skills CLI package. |
| PM | Product manager role responsible for customer problem, value, priority, scope, and success measures. |
| Product owner (PO) | Delegated role accountable for day-to-day backlog ordering, story clarity, and acceptance decisions within the product direction; the product manager retains broader product strategy and outcome accountability unless local governance says otherwise. |
| Policy | Versioned rules that allow, require gates for, or deny a delivery action. |
| PRFAQ | Working-backwards press release and frequently asked questions package used to clarify customer value and difficult questions. |
| Prompt | Instructions and context supplied to an AI model for a task; a prompt is not proof, permission, or an executed command. |
| Projection | Derived human- or machine-readable view that can be rebuilt from authoritative evidence. |
| Provenance | Evidence of origin, history, integrity, and production path for a package or record. |
| QA | Quality assurance role responsible for testability, risk-based coverage, environments, evidence, and acceptance signoff. |
| Quick flow | Fast execution mode for low-risk bounded work using explicit assumptions and focused checks. |
| Rigor | Strength of clarification, traceability, review, evidence, and approval controls applied to work. |
| RACI | Responsibility model: Responsible performs work, Accountable accepts the decision, Consulted provides input, and Informed receives the result. |
| SDLC | Software development lifecycle: the path from problem and intent through planning, building, testing, release, operation, and learning. |
| SDD | Specification-driven development: this repository's practice of establishing a testable requirement/design/QA/task contract before implementation grows. Other sources may use SDD for a Software Design Document or a different local meaning. |
| Skill | Portable `SKILL.md` workflow contract telling an agent when and how to perform one bounded capability. |
| Sub-agent | Separately tasked agent working under an orchestrator with its own context and evidence responsibilities; its conclusions require verification. |
| Orchestration | Delegating bounded work, coordinating dependencies, resolving disagreement, and verifying results across agents or tools. |
| Template | Reusable artifact structure with placeholders and rules; it is not an executing agent or complete workflow. |
| Token | Unit into which a model encodes text or code; it can be shorter or longer than a word and is used to measure context limits and usage. |
| Source checkout | Clone of this harness repository used by maintainers for canonical skill, shared runtime, compatibility, documentation, and release work. |
| Shell | Program that interprets terminal commands; POSIX shells and PowerShell differ in variable and quoting syntax. |
| Working tree | Current checked-out repository files, including staged, unstaged, and untracked content. |
| Commit hash / SHA | Content-derived Git identifier for one commit; the full value is used here as immutable source identity. |
| State | Versioned machine record of lifecycle or runtime progress; it must agree with authoritative evidence. |
| Test case (TC) | Explicit setup, action, and expected result used to verify acceptance or risk behavior. |
| TOON | Token-Oriented Object Notation used for complete token-efficient agent state, indexes, plans, and results. |
| Traceability | Links connecting intent, requirements, decisions, tests, tasks, evidence, and commits. |
| Workflow | Ordered sequence of activities, gates, skills, tools, and handoffs that produces an outcome. |
| Waiver | Scoped, owned, reasoned, time-bounded exception to an eligible policy rule. |
