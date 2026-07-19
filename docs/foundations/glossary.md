---
title: Glossary
description: Canonical definitions for AI SDLC, SDD, lifecycle roles, artifacts, controls, state, and representation terms.
---

# Glossary

| Term | Meaning in this harness |
| --- | --- |
| Acceptance criterion (AC) | Observable condition that must be true for a requirement to be accepted. |
| Agent | AI assistant acting through available tools and selected skill instructions. |
| AI SDLC | A software development lifecycle expressed as durable evidence, bounded agent capabilities, deterministic helpers, explicit state, and human authority. |
| Artifact | Repository file that preserves delivery context or evidence, such as requirements, design, QA, decisions, or plans. |
| BA | Business analyst role responsible for rules, workflows, actors, and testable business behavior. |
| Blocker | Missing decision, evidence, permission, capability, or valid predecessor that prevents safe continuation. |
| BRD | Business requirements document describing business context, rules, scope, actors, constraints, and acceptance logic. |
| Capability | A bounded operation an installed skill, module, adapter, or host can support. |
| Change set | Isolated proposal workspace used to preview and approve specification changes before canonical apply. |
| Control plane | Policy, state, runtime, graph, context, adapter, trust, and recovery mechanisms that coordinate delivery without replacing authoritative artifacts. |
| Decision log | Markdown record of material choices, context, options, owner, status, affected artifacts, and validation links. |
| Delivery | Role accountable for coordination, readiness, handoff, ownership, and release confidence. |
| Drift | Difference between a stored identity/projection and current authoritative source content. |
| Evidence | Inspectable proof supporting a delivery claim, including source anchors, tests, reviews, approvals, commands, outcomes, and commits. |
| Fingerprint | Deterministic hash identifying normalized content or a derived record. |
| Flow | Ordered connection of skills, evidence, gates, and handoffs toward an outcome. |
| Freshness | Whether evidence still matches its artifacts, dependencies, time bounds, and upstream evidence. |
| Full flow | Strict execution mode for one selected skill; it verifies prerequisites and decisions but does not automatically run the entire lifecycle. |
| Gate | Condition that must be satisfied before a transition, mutation, approval, or completion claim. |
| Handoff | Versioned result containing outcome, blockers, required next action, and optional next actions. |
| Harness | Repository-native system of skills, helpers, artifacts, state, and controls that makes AI-assisted delivery repeatable and inspectable. |
| Human checkpoint | Point where accountable human review, decision, approval, or risk acceptance is required. |
| Module | Versioned compatible group of core or optional skills. |
| PM | Product manager role responsible for customer problem, value, priority, scope, and success measures. |
| Policy | Versioned rules that allow, require gates for, or deny a delivery action. |
| PRFAQ | Working-backwards press release and frequently asked questions package used to clarify customer value and difficult questions. |
| Projection | Derived human- or machine-readable view that can be rebuilt from authoritative evidence. |
| Provenance | Evidence of origin, history, integrity, and production path for a package or record. |
| QA | Quality assurance role responsible for testability, risk-based coverage, environments, evidence, and acceptance signoff. |
| Quick flow | Fast execution mode for low-risk bounded work using explicit assumptions and focused checks. |
| Rigor | Strength of clarification, traceability, review, evidence, and approval controls applied to work. |
| SDLC | Software development lifecycle: the path from problem and intent through planning, building, testing, release, operation, and learning. |
| SDD | Spec-driven development: establishing a testable requirement/design/QA/task contract before implementation grows. |
| Skill | Portable `SKILL.md` workflow contract telling an agent when and how to perform one bounded capability. |
| State | Versioned machine record of lifecycle or runtime progress; it must agree with authoritative evidence. |
| Test case (TC) | Explicit setup, action, and expected result used to verify acceptance or risk behavior. |
| TOON | Token-Oriented Object Notation used for complete token-efficient agent state, indexes, plans, and results. |
| Traceability | Links connecting intent, requirements, decisions, tests, tasks, evidence, and commits. |
| Waiver | Scoped, owned, reasoned, time-bounded exception to an eligible policy rule. |
