---
title: "Role learning paths: contribute without crossing authority boundaries"
description: "Choose a role-specific entry path, skill sequence, evidence target, and accountable handoff for harness work."
learning_level: 6
audience:
  - product
  - analysis
  - quality
  - engineering
  - architecture
  - security
  - delivery
  - governance
  - maintainer
estimated_time: "90–150 minutes for one path"
prerequisites:
  - "Guided practice"
content_type: "role_paths"
last_reviewed: "2026-07-21"
source_usage:
  - source_id: HARNESS-DOCS
    mode: synthesized
  - source_id: HARNESS-SKILLS
    mode: synthesized
  - source_id: NIST-AI-RMF
    mode: reference
  - source_id: NIST-SSDF
    mode: reference
  - source_id: GOOGLE-STYLE
    mode: reference
  - source_id: W3C-WAI
    mode: reference
---

# Role learning paths: contribute without crossing authority boundaries

Role paths are discovery aids for entry tasks, inputs, outputs, and handoffs. They do not grant permission or approval. Organizational and repository policy assigns each decision.

Use the [canonical skills-by-role map](../reference/skills-by-role.md) to select skills. When a skill reference and this lesson differ, follow Reference and report the drift.

## On this page

- [At a glance](#at-a-glance)
- [Shared operating foundation](#shared-operating-foundation)
- [PM or PO](#pm-or-po)
- [Business Analyst](#business-analyst)
- [QA](#qa)
- [Developer](#developer)
- [Architecture and Security](#architecture-and-security)
- [Delivery and VP](#delivery-and-vp)
- [Head of AI Practice](#head-of-ai-practice)
- [Harness Maintainer](#harness-maintainer)
- [Cross-role worked example](#cross-role-worked-example)
- [Practice exercise](#practice-exercise)
- [Check your understanding](#check-your-understanding)

## At a glance

**Level:** 6 — role-specific paths and independent use

**Audience:** Product Manager (PM) or Product Owner (PO), Business Analyst (BA), Quality Assurance (QA) practitioner, Developer, Architecture and Security reviewer, Delivery leader or Vice President (VP), Head of AI Practice, and Harness Maintainer.

**Estimated time:** 90–150 minutes for the foundation and one path.

**Prerequisites:** [Guided practice](guided-practice.md), especially the evidence, delegation, and human-escalation labs. An experienced learner may substitute equivalent evidence only after passing the [starting-level diagnostic](../start.md#choose-your-starting-level) and recording which lab criteria that evidence satisfies.

## Expected outcome

You can choose three realistic entry tasks for your role, prepare their upstream inputs, use the current role-to-skill map, produce evidence, and hand off without approving another owner's decision. You can explain how adjacent roles challenge and improve the same change.

## What experienced readers may skip

Experienced practitioners may skim the foundation. Read one upstream and one downstream path; handoffs fail when the next role's needs are unknown.

## Why this matters

AI assistance can blur responsibility through role simulation or reviewer-count approval. Role prompts focus questions; they do not create evidence, assignment, or authority. The harness separates contribution from decision.

## Observable learning objectives

### Can explain

- Explain your role outcome, owned decisions, contributions, reviews, and authority limits.
- Explain the upstream evidence your role needs and downstream handoff it owes.
- Explain why skill discovery labels do not grant access or approval.

### Can do

- Select a current skill sequence from the canonical role map for three common tasks.
- Formulate a bounded role-specific request with observable evidence.
- Review one adjacent role's artifact and preserve unresolved disagreements.

### Can prove

- Produce a first-exercise artifact tied to current repository evidence.
- Show the skill reference used, actual validation, and named handoff owner.
- Identify one decision that remains outside your authority.

## Core concepts

### Shared operating foundation

Every role starts with these behaviors:

1. Identify the consumer repository and read its instructions.
2. State the accepted or proposed outcome and whether it has an accountable owner.
3. Separate authoritative inputs from examples, generated summaries, and untrusted content.
4. Choose a flow proportionate to impact, uncertainty, and reversibility.
5. Use the navigator for read-only routing when the owning skill is unclear.
6. Preserve artifact identifiers, decisions, and evidence across handoffs.
7. Stop when permission, authority, evidence, or context is absent; never call a role prompt, reviewer count, test pass, or score an approval.

The role map is task-based. One person may perform several roles but must label each decision and authority; large teams may divide a path. Contract and evidence matter more than title.

### Owned, contributed, reviewed, and accepted

**Owns** means accountable for a decision under the organization's operating model. **Contributes** means supplies evidence, analysis, or implementation. **Reviews** means challenges an artifact from a defined perspective. **Accepts** means records a decision within assigned authority. These verbs should not be interchangeable.

A QA engineer may own test strategy and recommend readiness while product acceptance remains with a Product Owner. A security reviewer may reject a policy violation under delegation but cannot redefine the outcome. Handoffs preserve these boundaries.

## Important distinctions

- **Role path versus skill contract:** this chapter teaches a journey; Reference owns exact skill behavior.
- **Role perspective versus isolated reviewer:** asking one agent for several roles is a simulated perspective exercise, not independent review.
- **Recommendation versus approval:** a recommendation informs the accountable owner; it does not substitute for that decision.
- **Readiness versus completion:** an artifact may be ready for the next stage while the feature remains incomplete.
- **Evidence versus expertise:** expertise helps interpret evidence but should not turn unsupported memory into a repository fact.

### Worked example 1: one person, two decisions

In a small company, Sam is both Product Owner and engineering lead. Sam first records the product decision: guest users may save a draft for seven days. Later Sam reviews the encryption design as engineering lead. The same person acts, but the artifacts name two decision types, evidence sets, and gates. This prevents a future reader from assuming that product acceptance also approved the threat model.

### Worked example 2: contributor without approval

A Business Analyst finds that “business day” is undefined and proposes the organization's holiday calendar. The proposal includes source evidence and affected scenarios. The analyst does not mark the requirement accepted. The product/policy owner chooses the calendar, after which QA updates boundary cases and the developer reassesses scheduling logic.

### Weak example

> You are the Head of AI Practice. Review the feature, run every relevant skill, approve security and product scope, then tell engineering to merge.

The role prompt invents authority, mixes unrelated owners, and prescribes an unbounded chain. It provides no repository context or evidence standard.

### Corrected example

> As the assigned AI-practice reviewer, inspect the proposed agent workflow and repository policy read-only. Report tool permissions, data classes, model/provider assumptions, required human gates, evaluation evidence, and unresolved owners. Do not review product value, accept residual security risk, modify files, or authorize merge. Link each finding to evidence and hand policy questions to the named governance owner.

This version uses role framing to focus questions while keeping authority, scope, evidence, and output explicit.

## PM or PO

**Role outcome:** Turn a customer or stakeholder problem into a valuable, bounded outcome that delivery roles can clarify, implement, and validate. Product Manager (PM) usually emphasizes discovery, value, and strategy; Product Owner (PO) usually emphasizes backlog readiness, sequencing, and acceptance. Local definitions may differ.

**Shared prerequisites:** Accepted problem evidence or a discovery question; known stakeholders; repository product context; authority map; basic evidence and prompting skills.

**What the role owns:** Within assignment, intended customer outcome, priority, scope and non-scope, value hypothesis, acceptance boundaries, and product decisions. A PO may own backlog sequence and product acceptance under delegated policy.

**What the role contributes:** Customer scenarios, measures, assumptions, constraints, trade-offs, release intent, and change decisions.

**What the role reviews:** Outcome alignment, story value and slice, acceptance evidence, and scope changes.

**What the role cannot approve for another owner:** Architecture, test strategy, security/legal risk, operations, or merge/release unless assigned. Reviewer agreement cannot replace an owner.

**Three common entry tasks:** Clarify an uncertain customer problem; synthesize an initiative package; define MVP and release slices from a ready backlog.

**Recommended skill sequence:** Choose a branch by task, not title. A PM exploring an unclear problem can use [`ai-sdlc-working-backwards-discovery`](../reference/skills/ai-sdlc-working-backwards-discovery.md), [`ai-sdlc-prfaq-package-synthesis`](../reference/skills/ai-sdlc-prfaq-package-synthesis.md), then [`ai-sdlc-requirements-readiness-review`](../reference/skills/ai-sdlc-requirements-readiness-review.md). A PO with a validated initiative can use [`ai-sdlc-backlog-decomposition-and-task-planning`](../reference/skills/ai-sdlc-backlog-decomposition-and-task-planning.md), then [`ai-sdlc-release-slicing-and-backlog-readiness-review`](../reference/skills/ai-sdlc-release-slicing-and-backlog-readiness-review.md). Do not run the backlog branch until its package prerequisites are present; [skills by role](../reference/skills-by-role.md) owns current routing.

**Upstream inputs:** Research, strategy, constraints, stakeholder decisions, current behavior, policy, and problem evidence.

**Downstream handoffs:** Outcome package to BA/planning; accepted scope to QA/engineering; product decisions to affected artifacts.

**First exercise:** Given “add team sharing,” create a product framing note with target actor, problem evidence, outcome, non-goals, success observation, five discovery questions, and decision owners. Do not specify database or permission implementation. Ask a BA to identify rule gaps and QA to identify untestable acceptance language.

**Evidence of completion:** Requirements trace to outcome; assumptions differ from decisions; slice is observable; receiver confirms usability.

**Common role-specific failure modes:** Equating urgency with value; UI before outcome; hidden scope changes; agent-owned priority; generated PRFAQ treated as customer evidence.

## Business Analyst

**Role outcome:** Convert accepted intent and domain evidence into explicit actors, workflows, business rules, exceptions, terms, and traceable requirements without inventing policy.

**Shared prerequisites:** Product outcome, stakeholder/source inventory, authority map, current process evidence, glossary, and known constraints.

**What the role owns:** Analysis quality, ambiguity register, requirement structure, domain-term consistency, traceability, and elicitation record within assignment.

**What the role contributes:** Actors, workflows, decision tables, rules, exceptions, assumptions, requirements, and impact.

**What the role reviews:** Discovery gaps, backlog rule coverage, domain fidelity, and changed processes.

**What the role cannot approve for another owner:** Value, priority, disputed policy, design, test signoff, security risk, or release. The analyst exposes; the owner decides.

**Three common entry tasks:** Frame actors and business rules for a feature; review a product package for planning gaps; analyze change impact after a rule changes.

**Recommended skill sequence:** Choose one conditional route. For an individual feature that still needs actors, workflows, and rules, use [`ai-sdlc-ba`](../reference/skills/ai-sdlc-ba.md). For an existing PRFAQ, business requirements document, product brief, or equivalent initiative package, use [`ai-sdlc-backlog-requirements-gap-review`](../reference/skills/ai-sdlc-backlog-requirements-gap-review.md) before backlog decomposition. Use [`ai-sdlc-change-impact`](../reference/skills/ai-sdlc-change-impact.md) only when accepted inputs change. These are alternatives with different prerequisites, not a mandatory chain; the [role map](../reference/skills-by-role.md) owns current routing.

**Upstream inputs:** Outcome, scenarios, policies, domain evidence, workflows, data definitions, and stakeholder questions.

**Downstream handoffs:** Rules to product, testable context to QA, domain boundaries to engineering, impact paths to delivery.

**First exercise:** Analyze “pause a subscription” using the [tracked source pack](../assets/learning-fixtures/subscription-pause-source-pack.txt). Define actors, supported rules, unknown eligible states, timing, billing, notification, resume conditions, failure paths, and at least eight unresolved questions. Build a decision table whose facts cite a source-pack line or policy ID; label all other entries proposals or questions and do not choose answers lacking authority.

**Evidence of completion:** Terms are consistent; rules cite evidence or say proposed; exceptions are observable; IDs trace; questions name owner and impact.

**Common role-specific failure modes:** Interviews as accepted facts; missing negative paths; vague behavior; hidden contradictions; implementation overreach; generated rules as authority.

## QA

**Role outcome:** Make quality risks, expected behavior, coverage, environments, and actual evidence visible so accountable owners can judge readiness.

**Shared prerequisites:** Accepted or reviewable requirements, risk context, architecture or interface boundaries, available environments, test data rules, and evidence freshness.

**What the role owns:** Testability analysis, quality strategy, scenario coverage, test-case quality, execution evidence, defect reporting, and QA readiness recommendation within assignment.

**What the role contributes:** Risk-based positive, negative, boundary, integration, accessibility, security, performance, and regression coverage; environment, data, and traceability.

**What the role reviews:** Observability, testability, implementation evidence, failures, regression, and release evidence.

**What the role cannot approve for another owner:** Product scope, architecture/security risk, deployment, or residual business risk. Passing tests are not product acceptance.

**Three common entry tasks:** Review requirements for testability; design risk-based test scope; synthesize cases and verify requirements-to-test readiness.

**Recommended skill sequence:** Use [`ai-sdlc-qa-requirements-gap-review`](../reference/skills/ai-sdlc-qa-requirements-gap-review.md), [`ai-sdlc-test-scope-and-strategy-design`](../reference/skills/ai-sdlc-test-scope-and-strategy-design.md), [`ai-sdlc-test-case-and-suite-synthesis`](../reference/skills/ai-sdlc-test-case-and-suite-synthesis.md), then [`ai-sdlc-qa-traceability-and-readiness-review`](../reference/skills/ai-sdlc-qa-traceability-and-readiness-review.md). For implementation-level cases rather than a delivery suite, use [`ai-sdlc-test-cases`](../reference/skills/ai-sdlc-test-cases.md) where its trigger and prerequisites fit. Check the [role map](../reference/skills-by-role.md).

**Upstream inputs:** Requirement IDs, rules, design/API boundaries, risk, environments, test data, and change set.

**Downstream handoffs:** Testability gaps to BA/product; test strategy and cases to engineering; actual results and residual gaps to delivery and acceptance owners.

**First exercise:** Review an acceptance criterion, “Users can upload a valid profile image quickly.” Replace it with observable types, sizes, dimensions, outcomes, errors, and a measured performance condition owned by product/operations. Add malformed, oversized, animated, interrupted, and unauthorized cases.

**Evidence of completion:** Requirements map to cases or exclusions; planned differs from executed; environment/revision are recorded; gaps have owners.

**Common role-specific failure modes:** Low-value case volume; line coverage as risk coverage; irreproducible screenshots; missing environment; blocked marked passed; tests silently redefining requirements.

## Developer

**Role outcome:** Design and implement the smallest maintainable change that satisfies accepted requirements, preserves repository conventions, and produces reproducible technical evidence.

**Shared prerequisites:** Consumer repository instructions, accepted task/spec, current project context, dependency-ready task, branch policy, tests, and permitted tool scope.

**What the role owns:** Technical implementation choices within design authority, code quality, local test evidence, scope discipline, defect correction, and transparent technical risk recommendations.

**What the role contributes:** Feasibility, alternatives, uncertainty, implementation, tests, documentation, observability, and review resolution.

**What the role reviews:** Feasibility, maintainability, correctness, dependencies, and validation evidence.

**What the role cannot approve for another owner:** Outcome, security risk, policy exception, QA signoff, release, or merge outside policy. Local success does not override gates.

**Three common entry tasks:** Ground a task in repository evidence; specify and implement a medium change; review and validate a completed diff.

**Recommended skill sequence:** Ground with [`ai-sdlc-project-context`](../reference/skills/ai-sdlc-project-context.md), specify material work through [`ai-sdlc-sdd`](../reference/skills/ai-sdlc-sdd.md), then use [`ai-sdlc-validation`](../reference/skills/ai-sdlc-validation.md) and [`ai-sdlc-code-review`](../reference/skills/ai-sdlc-code-review.md). Confirm with [skills by role](../reference/skills-by-role.md).

**Upstream inputs:** Requirements, design constraints, cases, dependencies, commands, policy, and current evidence.

**Downstream handoffs:** Diff/evidence to review and QA; ambiguity to BA/product; risks to owners; completion evidence to commit/release workflow.

**First exercise:** In a disposable repository, add normalization for a user-entered reference code. Before code, document whitespace, case, Unicode, empty, and invalid-symbol behavior. Write tests from accepted cases, implement narrowly, run focused and regression checks, and hand off without committing unless requested.

**Evidence of completion:** Scoped diff; aligned requirement/test/code; recorded commands/failures; findings resolved or open; user changes preserved.

**Common role-specific failure modes:** Coding through ambiguity; hidden refactor; weakened tests; unauthorized install; compilation as behavior proof; unrelated staging; invented APIs.

## Architecture and Security

**Role outcome:** Preserve system qualities and trust boundaries by making architectural decisions, threat assumptions, dependencies, data flows, permissions, and residual risks explicit.

**Shared prerequisites:** Accepted outcome and constraints, current architecture evidence, data classification, threat context, deployment model, policies, and named decision authorities.

**What the role owns:** Assigned architecture decisions or security assessment quality, decision records, threat/risk analysis, guardrails, and escalation of unacceptable or unowned risk.

**What the role contributes:** Options, boundaries, data/trust flows, abuse cases, controls, dependencies, and operational effects.

**What the role reviews:** Non-functional needs, coupling, resilience, identity, secrets, I/O boundaries, dependencies, and validation.

**What the role cannot approve for another owner:** Value, legal interpretation, unassigned risk, QA, budget, or release. Architecture preference cannot silently override outcome.

**Three common entry tasks:** Compare architecture options for a material change; conduct abuse-case and permission review; assess change impact across interfaces and operations.

**Recommended skill sequence:** Use [`ai-sdlc-architecture`](../reference/skills/ai-sdlc-architecture.md), [`ai-sdlc-security-testing`](../reference/skills/ai-sdlc-security-testing.md), and [`ai-sdlc-change-impact`](../reference/skills/ai-sdlc-change-impact.md). Use policy workflows only under actual authority; verify [skills by role](../reference/skills-by-role.md).

**Upstream inputs:** Outcome, non-functional requirements, current architecture, data, identities, contracts, threats, dependencies, and operations.

**Downstream handoffs:** Decision record and constraints to developers; abuse cases and verification needs to QA; residual risk and policy questions to accountable owners; migration/operations effects to delivery.

**First exercise:** Review a proposed AI-generated support-summary feature. Map data entering and leaving the model boundary, identify untrusted ticket text, secrets and personal data, tool permissions, retention questions, failure containment, human review, and provider assumptions. Do not claim compliance.

**Evidence of completion:** Current evidence supports decisions; alternatives remain visible; threats map to controls/tests; no unsupported compliance; risks have owners.

**Common role-specific failure modes:** Generated-summary design; prompt filters as full defense; broad tools; encryption confused with authorization; checklist compliance claims; evidence-free rejection.

## Delivery and VP

**Role outcome:** Establish a viable operating model, sequence work across dependencies, evaluate readiness and investment evidence, and decide hold, pilot, scale, or stop within delegated authority.

**Shared prerequisites:** Business outcome and sponsorship, delivery graph, backlog/release evidence, ownership map, risks, capacity constraints, governance controls, and measurable baseline.

**What the role owns:** Depending on assignment, delivery sequence, escalation, resource trade-offs, pilot boundaries, operating metrics, and organizational adoption decisions.

**What the role contributes:** Dependency resolution, rollout, thresholds, support, exceptions, benefit/cost framing, and ownership.

**What the role reviews:** Outcome alignment, readiness, blockers, freshness, operations, overhead, support, and metrics.

**What the role cannot approve for another owner:** Product acceptance, architecture/security risk, legal policy, test facts, or merge unless assigned. Scores cannot erase blockers.

**Three common entry tasks:** Inspect lifecycle dependencies and handoff readiness; define a low-risk organizational pilot; decide whether evidence supports hold, adjust, or scale.

**Recommended skill sequence:** Use [`ai-sdlc-delivery-graph`](../reference/skills/ai-sdlc-delivery-graph.md), [`ai-sdlc-delivery-handoff-review`](../reference/skills/ai-sdlc-delivery-handoff-review.md), and for a named high-impact question [`ai-sdlc-evidence-council`](../reference/skills/ai-sdlc-evidence-council.md). Consult [skills by role](../reference/skills-by-role.md).

**Upstream inputs:** Strategy, outcome metrics, delivery package, team dependencies, risk and quality reports, policy, training/support capacity, and current adoption baseline.

**Downstream handoffs:** Prioritized blockers to owners; pilot scope and controls to teams; funding/sequence decisions to product and engineering; scale/stop decision with rationale to governance.

**First exercise:** Design a two-team, four-week pilot for documentation-only and low-risk test-generation tasks. Define eligibility, prohibited work, project-scoped installation, training, human gates, defect/rework metrics, data boundary, support owner, rollback, and weekly decision points.

**Evidence of completion:** Metrics cover outcomes/overhead; gates and blockers have owners; exclusions and rollback are explicit; scale requires quality/risk evidence.

**Common role-specific failure modes:** Mandates without capacity; output-volume metrics; speed without rework; exception sprawl; council as approval; premature scale.

## Head of AI Practice

**Role outcome:** Establish safe, measurable, teachable AI-assisted delivery practices across teams while preserving domain-owner accountability and repository autonomy.

**Shared prerequisites:** Organizational objectives, approved-tool and data policy, threat/risk model, provider contracts, representative repositories, evaluation baseline, training needs, and support ownership.

**What the role owns:** Within mandate, AI practice standards, approved patterns, evaluation methodology, training, platform/tool guidance, exception workflow, incident learning, and continuous improvement.

**What the role contributes:** Tool criteria, context/prompt practice, permissions, human gates, evaluations, metrics, and training community.

**What the role reviews:** AI workflows, provider/data assumptions, evaluations, injection controls, permissions, provenance, training, and drift.

**What the role cannot approve for another owner:** Consumer outcome, architecture, domain rules, legal interpretation, release, or team risk unless delegated. Standards do not centralize all decisions.

**Three common entry tasks:** Define an approved agent-use pattern; create an evaluation and incident-learning baseline; review a team pilot for security, evidence, and maintainability.

**Recommended skill sequence:** Use [`ai-sdlc-policy`](../reference/skills/ai-sdlc-policy.md), [`ai-sdlc-approvals-sandbox`](../reference/skills/ai-sdlc-approvals-sandbox.md), and [`ai-sdlc-evidence-council`](../reference/skills/ai-sdlc-evidence-council.md). Use the current [role map](../reference/skills-by-role.md) for provenance and retrospective tasks.

**Upstream inputs:** Organizational risk appetite, data classification, tool/provider terms, team workflows, security incidents, quality/rework data, and learner feedback.

**Downstream handoffs:** Approved controls and training to teams; provider/tool risks to procurement/security/legal owners; evaluation findings to platform and delivery leaders; compatibility needs to harness maintainers.

**First exercise:** Review a proposal for autonomous issue-to-pull-request execution. Classify read/write/network actions, data sent externally, approval points, evaluation scenarios, failure containment, audit evidence, and prohibited repositories. Recommend a bounded pilot, not organization-wide approval.

**Evidence of completion:** Pattern names assumptions, least privilege, gates, representative evaluations, rollback, ownership, and outcome metrics; no unsupported compliance.

**Common role-specific failure modes:** Vendor behavior as harness contract; prompts as control; cost before validation; hidden incidents; centralized domain decisions; untested model claims.

## Harness Maintainer

**Role outcome:** Keep repository contracts coherent, portable, documented, validated, source-traceable, secure to install, and learnable across supported hosts.

**Shared prerequisites:** Repository contribution rules, architecture and compatibility contracts, skill metadata conventions, documentation type boundaries, test/build commands, release process, and current audit findings.

**What the role owns:** Harness source quality, canonical ownership, compatibility, generated/catalog boundaries, validation, documentation navigation, skill lifecycle, contributor guidance, and release evidence within maintainer authority.

**What the role contributes:** Skills, helpers, adapters, docs, tests, migration, provenance, troubleshooting, security, and review synthesis.

**What the role reviews:** Skill contracts/conflicts, installation, generated artifacts, links, accessibility, provenance, tests, and release readiness.

**What the role cannot approve for another owner:** Consumer outcome, architecture, secrets policy, deployment, adoption, or legal questions.

**Three common entry tasks:** Add or change a reusable skill; correct documentation while preserving canonical ownership; prepare a compatibility-validated release candidate.

**Recommended skill sequence:** Use [`ai-sdlc-sdd`](../reference/skills/ai-sdlc-sdd.md), [`ai-sdlc-code-review`](../reference/skills/ai-sdlc-code-review.md), [`ai-sdlc-validation`](../reference/skills/ai-sdlc-validation.md), then [`ai-sdlc-commit-prep`](../reference/skills/ai-sdlc-commit-prep.md) only after completion. Confirm [skills by role](../reference/skills-by-role.md).

**Upstream inputs:** Accepted maintainer outcome, issue evidence, current contracts, audit reports, supported-host behavior, source and license verification, and clean change scope.

**Downstream handoffs:** Reviewed diff and validation to release owner; migration and update guidance to consumers; corrected catalogs/reference to users; unresolved licensing or compatibility risk to accountable owner.

**First exercise:** Propose a small documentation-validator rule. Identify canonical owner, false-positive risk, fixtures at both boundaries, dependency impact, navigation effect, source provenance, contributor command, and rollback. Implement only in a task branch if authorized.

**Evidence of completion:** Existing and new boundary tests pass; strict/rendered docs checks pass; generated files are regenerated; scope is clean; release stays separate.

**Common role-specific failure modes:** Editing generated reference; copied Learn contracts; weakened checks; broken URLs; unpinned sources; global-install assumptions; unresolved license/CI risk.

## Mid-page recap

- Role labels guide discovery; organizational assignment and repository policy define authority.
- Each path names owned decisions, contributions, reviews, limits, inputs, outputs, evidence, and handoffs.
- Product clarifies value; BA clarifies rules; QA clarifies testability; engineering clarifies feasibility; security clarifies trust; delivery clarifies readiness; AI practice clarifies agent governance; maintainers clarify harness contracts.
- A person may hold several roles, but each decision and evidence boundary should remain explicit.
- Use the canonical role map for current skill selection, and canonical skill pages for behavior.

## Cross-role worked example

### Scenario: add scheduled report delivery

A customer administrator wants a weekly usage report emailed to finance. This touches outcome, rules, data, availability, permissions, and operations.

**PM outcome definition:** Authorized administrators schedule one weekly summary for approved recipients. External lists are excluded; product avoids prescribing queue technology.

**BA ambiguity analysis:** Define “weekly,” time zones, recipients, disabled users, sensitive fields, zero usage, and changes; separate evidence from proposals.

**QA testability review:** Map scheduling, authorization, content, retry, duplicate, accessibility, audit, and cancellation. Missing guarantees remain blockers.

**Developer feasibility review:** Identify systems, migration, idempotency, components, and commands without choosing recipient policy.

**Security threat review:** Map data, email trust, injection, authorization, secrets, retention, and malicious recipients; route disclosure risk.

**Delivery readiness review:** Check dependencies, migration, operations, tests, support, and rollback; report blockers, not averages.

**AI-practice governance review:** Check model data, tool writes, generated-test evaluation, and human gates; runtime AI is not implied.

**Maintainer compatibility review:** A reusable skill needs generic scope, explicit contracts, no hidden global context, and host validation. Consumer scheduling stays local.

The handoff is evidence, not one agent's approvals. Recipient-policy disagreement returns to its owner.

## Harness connection

The [skills-by-role reference](../reference/skills-by-role.md) is generated or maintained as the canonical task-to-skill discovery surface. Each linked skill page owns exact triggers, inputs, permitted writes, checkpoints, validation, and handoff. [Human and agent responsibilities](../foundations/responsibilities.md) owns the shared authority model. [Evidence Council](../how-to/evidence-council.md) supports high-impact synthesis, while [Quality Lenses](../reference/skills/ai-sdlc-quality-lenses.md) supports reusable perspectives. This lesson connects them into learning paths without copying their contracts.

## Role perspectives

The eight paths above are the role perspectives. For independent review, give isolated reviewers the same artifact snapshot, common goals, role-specific questions, read-only scope, and finding schema. Label simulated execution honestly. The parent or assigned editor synthesizes and owns corrections. Accountable humans decide; reviewer roles do not vote policy into existence.

## Practice exercise

Choose your primary path and one adjacent path. Use the scheduled-report scenario or an authorized low-risk request in a consumer repository. Produce a role handoff card.

The card must contain: role outcome; task; authoritative inputs; uncertainty; selected skill and why; allowed actions; expected artifact; validation evidence; findings for the adjacent role; decision you own; decision you do not own; handoff receiver; stop condition.

### Permitted actions

- Read the role map, linked skill references, consumer instructions, and selected task evidence.
- Ask bounded questions and produce a read-only or documentation-only role artifact.
- Label proposals, facts, risks, and questions separately.
- Request review from one adjacent role without asking that reviewer to edit.

### Prohibited actions

- Claim authority based on this chapter or a role prompt.
- Run write-capable skills without repository authorization.
- Approve another owner's decision, suppress disagreement, or use reviewer count as a gate.
- Copy a full skill contract into the handoff card.

### Verification procedure

Compare your selected skill with the current role map and its canonical reference. Trace every upstream input to evidence. Ask the adjacent-role reviewer to identify one missing input and one boundary you respected. Confirm that actual validation and planned validation are labeled differently. Confirm the stop condition triggers when authority or evidence is missing.

### Evidence of completion

- One complete role handoff card with current links.
- One adjacent-role finding with evidence and confidence.
- One explicit owned decision and one decision outside your authority.
- One reproducible validation result or exact environmental blocker.
- A downstream receiver who can state the next action and unresolved risk.

## Check your understanding

1. Does a role label in a prompt grant that role's organizational permissions?
2. What should a BA do when two stakeholders give conflicting business rules?
3. Can QA mark product acceptance complete because all automated tests pass?
4. When should a developer use the navigator rather than invoke a known skill?
5. What must an architecture or security review avoid claiming?
6. Why should delivery metrics include rework and defects rather than only speed?
7. What distinguishes AI-practice governance from consumer product ownership?
8. When should a harness maintainer keep content in a consumer repository?

<details>
<summary>Answers for the role-path knowledge check</summary>

1. No. Role prompts focus analysis; permissions and authority come from organizational assignment, repository policy, and explicit approvals.
2. Preserve both claims and evidence, describe the affected decisions, name the accountable owner, and stop dependent assumptions until resolved.
3. No. QA can report executed evidence and readiness within its remit. Product acceptance belongs to its assigned owner and may require evidence beyond automation.
4. When desired intent is clear but the smallest owning workflow is uncertain. Invoke a known skill directly when trigger and current input clearly match.
5. Unsupported compliance, legal interpretation, total security, or residual-risk acceptance beyond delegation. It should provide evidence, trade-offs, and owners.
6. Speed can rise while quality and total delivery cost worsen. Rework, escaped defects, review load, and blocked time reveal whether adoption helps.
7. AI practice governs model/tool patterns, permissions, evaluation, training, and incidents. Consumer product owners decide the product outcome and value within their scope.
8. When content describes consumer-specific behavior, architecture, policy, or commands rather than a reusable harness contract. Generic appearance is not sufficient reason to centralize it.

</details>

## Common failure modes

Common failures are premature convergence, duplicate artifacts, stale skill selection, evidence-free handoffs, unowned questions, simulated councils labeled independent, and skipping adjacent paths.

## Recovery guidance

When authority is confused, stop, classify statements, reconstruct owners, and restore disagreements. If a skill conflicts with Reference, follow Reference and report drift. For a wrong-owner edit, preserve history, reopen the earliest decision, update dependents, and review.

For a failed handoff, identify missing input, evidence, or decision and route gaps to an accountable human.

## Completion checklist

- [ ] I completed the shared foundation and my primary role path.
- [ ] I read one upstream and one downstream role path.
- [ ] I can name what I own, contribute, review, and cannot approve.
- [ ] I selected current skills using the canonical role map.
- [ ] I linked rather than copied skill contracts.
- [ ] I produced a role handoff card with evidence and a stop condition.
- [ ] I preserved facts, proposals, questions, risks, and decisions separately.
- [ ] I obtained one adjacent-role review without transferring edit ownership.
- [ ] I identified an accountable human gate.
- [ ] I can begin harness use in an authorized consumer repository.

## Previous learning step

Return to [Guided practice](guided-practice.md) if your role exercise lacks a reproducible artifact, recovery path, or authority boundary.

## Next learning step

If Guided Practice evidence is complete, apply your role handoff to one authorized, bounded request in a consumer repository and record what the transfer context changed. Use [First 30 minutes](../onboarding/first-30-minutes.md) or the [first feature tutorial](../tutorials/first-feature.md) only as a refresher when their evidence is missing. Keep the canonical [skills-by-role map](../reference/skills-by-role.md) available while working independently.

## Sources and adaptation notes

- **HARNESS-DOCS** — [AI SDLC Harness documentation and repository contracts](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/faccb4354464a1a3cc309b7b2dfa65e8efaf3529/docs). Owner: AI SDLC Harness maintainers; revision: `faccb4354464a1a3cc309b7b2dfa65e8efaf3529`; reuse: `internal-authority`; mode: `synthesized`. Informed: roles/authority. Transformed: paths teach handoffs. Limitation: Reference owns mapping.
- **HARNESS-SKILLS** — [AI SDLC Harness skill contracts and deterministic helpers](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/faccb4354464a1a3cc309b7b2dfa65e8efaf3529/skills). Owner: AI SDLC Harness maintainers; revision: `faccb4354464a1a3cc309b7b2dfa65e8efaf3529`; reuse: `internal-authority`; mode: `synthesized`. Informed: prerequisites and routing. Transformed: contracts became conditional role decisions. Limitation: syntax and generated tables were excluded.
- **NIST-AI-RMF** — [Artificial Intelligence Risk Management Framework 1.0](https://doi.org/10.6028/NIST.AI.100-1). Owner: National Institute of Standards and Technology; revision: `NIST-AI-100-1-2023`; reuse: `reference-only`; mode: `reference`. Informed: risk ownership and oversight. Transformed: concepts were checked against handoffs. Limitation: no framework structure or compliance claim was imported.
- **NIST-SSDF** — [Secure Software Development Framework version 1.1](https://doi.org/10.6028/NIST.SP.800-218). Owner: National Institute of Standards and Technology; revision: `NIST-SP-800-218-2022`; reuse: `reference-only`; mode: `reference`. Informed: lifecycle responsibility and evidence. Transformed: ideas became original role boundaries. Limitation: no practice statement, mapping, or conformance claim was used.
- **GOOGLE-STYLE** — [Google developer documentation style guide](https://developers.google.com/style). Owner: Google; revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. Informed: global English and role terms. Transformed: checks shaped original paths. Limitation: no prose, example, table, or complete rule was adapted.
- **W3C-WAI** — [W3C Web Accessibility Initiative tutorials and guidance](https://www.w3.org/WAI/tutorials/). Owner: World Wide Web Consortium; revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. Informed: anchors and non-color meaning. Transformed: duplicate anchors were removed. Limitation: no tutorial, media, checklist, or standards wording was reproduced.
