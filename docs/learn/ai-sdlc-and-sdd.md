---
title: "AI SDLC and spec-driven development"
description: "Learn how requests become traceable requirements, design boundaries, tests, implementation tasks, validation evidence, human review, and accountable handoffs when AI participates in delivery."
learning_level: 3
audience:
  - beginner
  - product
  - analysis
  - quality
  - engineering
  - security
  - delivery
estimated_time: "110–140 minutes"
prerequisites:
  - "Independent multi-role review with subagents"
content_type: "lesson"
last_reviewed: "2026-07-21"
source_usage:
  - source_id: HARNESS-DOCS
    mode: synthesized
  - source_id: HARNESS-SKILLS
    mode: synthesized
  - source_id: GITHUB-SPEC-KIT
    mode: adapted
  - source_id: NIST-SSDF
    mode: reference
  - source_id: NIST-AI-RMF
    mode: reference
  - source_id: W3C-WAI
    mode: reference
---

# AI SDLC and spec-driven development

Software delivery is not finished when code exists. A useful change begins with an intended outcome, passes through requirements and design, is implemented and tested, and reaches people through controlled release and maintenance. When AI agents participate, the lifecycle needs clearer boundaries, stronger evidence, and deliberate traceability because generated work can be fast, fluent, incomplete, or inconsistent.

In this repository, **AI software development lifecycle (AI SDLC)** means applying lifecycle discipline to work in which AI assistants or agents help discover, plan, implement, review, test, document, or operate software. **Spec-driven development (SDD)** means using reviewed specifications and related evidence as the control surface for implementation. SDD is not a promise that a specification makes code correct, and the abbreviation is used differently elsewhere. This page teaches the harness interpretation and links exact operational contracts to their canonical owners.

## At a glance

**Level:** 3 — AI SDLC and spec-driven development

**Audience:** Product, analysis, quality, engineering, security, delivery, and governance participants who need a shared lifecycle and traceable handoff model

**Estimated time:** 110–140 minutes, including the artifact-mapping exercise

**Prerequisites:** Complete [Independent multi-role review with subagents](multi-role-review.md). You should already be able to distinguish generated output from evidence and route decisions to accountable humans.

## Expected outcome

You can map a software change from request to accountable handoff, explain what AI changes and what remains human, select proportionate specification rigor, detect stale or inconsistent artifacts, and prove completion with current evidence rather than a code diff alone.

## What experienced readers may skip

Experienced delivery practitioners may skim the ordinary lifecycle overview. Do not skip **The harness artifact chain**, **Adaptive rigor is not optional evidence**, **Stale and conflicting artifacts**, or the failure scenario. Those sections establish how this repository interprets SDD and how it differs from other approaches.

## On this page

- [Why this matters](#why-this-matters)
- [Observable learning objectives](#observable-learning-objectives)
- [Core concepts](#core-concepts)
- [The ordinary software development lifecycle](#the-ordinary-software-development-lifecycle)
- [What changes when AI participates](#what-changes-when-ai-participates)
- [The harness artifact chain](#the-harness-artifact-chain)
- [Requirements, design, tests, and tasks](#requirements-design-tests-and-tasks)
- [Traceability, gates, and handoffs](#traceability-gates-and-handoffs)
- [Adaptive rigor is not optional evidence](#adaptive-rigor-is-not-optional-evidence)
- [Stale and conflicting artifacts](#stale-and-conflicting-artifacts)
- [Important distinctions](#important-distinctions)
- [Worked examples](#worked-examples)
- [Harness connection](#harness-connection)
- [Role perspectives](#role-perspectives)
- [Practice exercise](#practice-exercise)
- [Check your understanding](#check-your-understanding)
- [Common failure modes](#common-failure-modes)
- [Recovery guidance](#recovery-guidance)
- [Evidence of completion](#evidence-of-completion)

## Why this matters

Without a lifecycle, teams optimize locally. A product request may skip ambiguity analysis. A developer may implement a plausible interpretation that no stakeholder intended. Tests may confirm the implementation rather than the required outcome. Documentation may describe an older behavior. Release evidence may be a screenshot with no environment or version. Maintenance begins with no record of why the design exists.

AI can increase the speed of each local action. It can also increase the speed of coordinated error. A model may produce requirements that appear complete, invent an API detail, write code for its own assumption, generate tests that repeat that assumption, and then summarize the matching artifacts as proof. Internal consistency is useful, but a consistently wrong artifact chain still fails the user.

AI SDLC therefore adds control around context, artifact authority, evidence, and human decisions. It does not require maximum ceremony for every typo. It requires rigor proportional to change risk, with a minimum evidence boundary that cannot be replaced by confidence. The aim is faster safe learning and delivery, not documentation for its own sake.

## Observable learning objectives

By the end of this chapter, you:

- **Can explain** the ordinary software development lifecycle and the additional risks created by probabilistic generation and agent action.
- **Can explain** this harness’s meaning of AI SDLC and SDD without presenting another framework’s behavior as a harness contract.
- **Can do** a traceability map from request through outcome, requirement, design boundary, test, task, implementation, evidence, review, and handoff.
- **Can do** a proportionate rigor decision based on uncertainty, impact, reversibility, security, data, and cross-team effects.
- **Can do** an artifact freshness and consistency review after requirements or implementation change.
- **Can prove** that acceptance criteria are backed by current evidence, human checkpoints are recorded, and unverified or stale areas remain visible.

## Core concepts

### Software development lifecycle

A software development lifecycle (SDLC) is a managed progression from identifying a need through requirements, design, implementation, verification, release, operation, and maintenance. Teams may arrange stages sequentially, iteratively, or continuously. The essential idea is not a single process diagram; it is that work has changing questions, artifacts, risks, and decision owners across its life.

### AI software development lifecycle

AI SDLC in this repository is the ordinary lifecycle with explicit controls for AI-assisted work: bounded context, source authority, generated-output validation, tool permissions, artifacts, evidence freshness, human gates, recovery, and traceability. AI may assist in any stage. It does not become the accountable product owner, security risk owner, or release authority.

### Specification

A specification is a reviewed description of the behavior and boundaries to be delivered. It records outcomes, actors, inputs, outputs, requirements, constraints, acceptance criteria, assumptions, exclusions, and unresolved questions at a level proportionate to the change. A specification is more precise than an initial request and remains connected to design, tests, tasks, and evidence.

### Spec-driven development

SDD in the harness means that implementation is controlled by explicit, current specification artifacts rather than by an unstructured prompt alone. The specification is not static law: authorized requirement changes update it and dependent artifacts. “Driven” means implementation and validation trace back to accepted intent, not that the document writes or approves code by itself.

The abbreviation **SDD** can also mean secure design, software design documents, or another tool's workflow. In this repository, follow the harness's canonical contracts. External frameworks are comparison inputs, not behavior authorities.

### Artifact

An artifact is a durable work product used by the lifecycle: request record, requirement set, design, decision log, test case, QA plan, task list, code change, test report, risk record, or handoff. A chat response becomes useful lifecycle state only when captured in an approved artifact with ownership and freshness.

### Evidence

Evidence is observable support for a claim. A test result may support functional behavior. A dependency scan may support a supply-chain claim. A product owner’s recorded acceptance may support outcome acceptance. Evidence is scoped: a unit test does not prove accessibility, a code diff does not prove deployment success, and reviewer agreement does not prove authorization.

### Gate

A gate is a condition that must be satisfied or consciously decided before work advances. Gates can be deterministic—such as a clean link check—or human—such as product acceptance or residual-risk approval. A gate should name criteria, evidence, and owner. It is not a vague “looks good.”

### Handoff

A handoff transfers an artifact, current evidence, known limitations, and a requested decision or next action to another accountable role. Good handoffs preserve what changed, why, validation performed, omissions, blockers, and freshness. They do not transfer authority merely by assigning work.

## The ordinary software development lifecycle

Lifecycle names vary, but these questions are common.

### Discover and frame

Identify the problem, affected people, value, known facts, assumptions, exclusions, and disputes without prematurely choosing an implementation.

### Specify requirements

Define observable behavior, quality attributes, rules, constraints, acceptance conditions, and unresolved decisions.

### Design

Describe responsibility boundaries and trade-offs across architecture, data, interfaces, security, operations, and maintenance.

### Plan

Connect design to tasks, dependencies, ownership, sequence, environments, and rollout.

### Implement

Change code and related assets within accepted scope, recording decisions discovered during work.

### Verify and validate

Verify conformance to specifications and technical contracts; validate intended use and outcome. Technical tests alone do not establish product acceptance.

### Release and operate

Control promotion, monitoring, communication, data protection, rollback, and incident response using evidence for the released version and environment.

### Maintain and learn

Repair, update, retire, and learn from production evidence; new evidence can restart discovery.

## What changes when AI participates

### Generated artifacts need source checks

An agent can draft requirements quickly, but it may fill missing information with a plausible assumption. Each artifact must distinguish source facts, human decisions, model proposals, and open questions. A polished requirement is not accepted simply because it uses formal language.

### Speed increases drift risk

If requirements, code, tests, and documentation are generated in one burst, a later correction to the first artifact may not reach the rest. Traceability and freshness checks are essential. The faster the generation, the easier it is to overlook that evidence belongs to an older state.

### Tool permissions become lifecycle concerns

An agent may read files, change state, call services, or publish output. Permission, sandbox, secret handling, and destructive-action controls therefore belong in planning and implementation, not only security review at the end.

### Review can be correlated

An agent reviewing its own output may repeat its assumption. Multi-role or isolated re-review can uncover gaps, but it remains evidence gathering. Human owners still decide acceptance and risk.

### Reproducibility needs durable commands and artifacts

Chat narration can disappear or be summarized. Record exact validation commands, environment, versions, outputs, and limitations in durable artifacts. A future maintainer should not need the original conversation to understand the change.

### Human accountability remains

People define outcomes, resolve stakeholder conflicts, accept product behavior, authorize risk, and control release according to organizational governance. An agent can recommend, organize, and execute within permission. It cannot acquire accountability from speed or fluency.

## The harness artifact chain

Use this learning map:

```text title="Traceable delivery chain"
request
  → accepted outcome
  → requirement
  → design boundary
  → test case
  → implementation task
  → validation evidence
  → human review
  → traceable handoff
```

The arrow does not require one file per concept or a purely sequential process. It means each downstream claim can be traced back, and changes are propagated deliberately.

### Request

A request, such as “Add saved report filters,” is initial input and usually not a complete requirement.

### Accepted outcome

The accepted outcome states the result and boundaries. A named human owner accepts it.

### Requirement

A requirement states observable behavior or quality, including relevant security, performance, accessibility, resilience, and operability.

### Design boundary

A design boundary divides responsibility: for example, normalize names in the service, enforce uniqueness in the database, and map conflicts through the API.

### Test case

A test case links preconditions, action, expected behavior, and evidence to a requirement, with risk-based positive, negative, boundary, and recovery cases.

### Implementation task

A task is a bounded unit connected to requirements and design, not a disconnected technical chore.

### Validation evidence

Evidence records what ran or was inspected, its scope, and its relation to the relevant version.

### Human review

Accountable roles examine evidence and decide only within their assigned authority.

### Traceable handoff

The handoff carries current artifacts, evidence, limitations, decisions, and next owner.

## Mid-page recap

AI SDLC preserves the ordinary lifecycle while adding explicit controls for probabilistic output, tool action, source authority, evidence, and human decisions. Harness SDD uses current specification artifacts to control implementation. The artifact chain links request to handoff; each arrow represents traceability and change propagation, not bureaucracy or guaranteed correctness.

## Requirements, design, tests, and tasks

### Functional and non-functional requirements

Functional requirements describe what behavior occurs. Non-functional requirements describe qualities and constraints: response time, availability, privacy, security, accessibility, compatibility, observability, and recovery. A feature can function correctly and still fail because it exposes data or cannot be used with a keyboard.

Use measurable conditions where evidence is feasible. “Fast” is not testable. “For the agreed data profile, the saved-filter list returns within the team’s accepted percentile and environment boundary” can be tested once owners specify the threshold and profile. Do not invent numbers merely to appear precise.

### Acceptance criteria

Acceptance criteria turn requirements into observable boundaries. They should include important negative and exception behavior, not only a happy path. They must name what evidence will support completion and who decides any subjective outcome.

### Assumptions and constraints

An assumption is treated as true provisionally and needs validation. A constraint limits the solution: platform support, regulation, compatibility, budget, deadline, or approved provider. Mixing them hides risk. “Only PostgreSQL is supported” may be a product constraint; “the existing table has no duplicate names” is an assumption requiring data evidence.

### Design decisions and records

When a decision has meaningful trade-offs, record context, chosen option, alternatives, consequences, and owner. A generated explanation can help draft the record, but the decision owner must verify it. Design records should reference requirements and be revisited when context changes.

### Test layers and QA scope

Map requirements to appropriate layers: unit tests for local rules, integration tests for database and service boundaries, end-to-end tests for critical journeys, and manual or automated checks for accessibility, security, performance, and operations. No fixed list applies to every change; risk and architecture determine the useful set.

### Tasks and sequencing

Tasks should include implementation, testing, documentation, migration, validation, and handoff work. Sequence dependencies explicitly. A schema change may require compatibility order, backfill, dual-read behavior, monitoring, and rollback before application cleanup. “Implement feature” hides these boundaries.

## Traceability, gates, and handoffs

Traceability lets a reviewer move in both directions. Forward: which design, task, and test implement requirement R-004? Backward: which accepted requirement justifies this new endpoint? Orphan implementation may be scope drift. Orphan requirements may be incomplete delivery. A test with no requirement may represent valuable regression coverage or an unexplained contract; classify it.

Traceability can use identifiers, links, tables, or structured metadata. The form matters less than reliable navigation and update behavior. Avoid a matrix that is maintained only for appearance. A compact table with current links and evidence status is better than a large stale spreadsheet.

Gates should be proportional and explicit. A small documentation correction might require link validation and editorial review. An authentication change might require accepted requirements, threat analysis, negative authorization cases, secret handling review, regression, rollout, rollback, and several human decisions. The gate record states what passed, what remains, and who authorized movement.

A handoff should answer:

- What outcome and scope were accepted, and what changed?
- Which artifacts and evidence are current?
- What was not tested or remains uncertain?
- Which decisions, blockers, and risks remain, with owners?
- Who owns the next action?

## Adaptive rigor is not optional evidence

Adaptive rigor means using the smallest lifecycle path that responsibly addresses uncertainty and impact. It does not mean skipping validation for convenience.

Consider these factors:

| Factor | Lower-rigor signal | Higher-rigor signal |
| --- | --- | --- |
| Scope | Isolated wording fix | Cross-service behavior change |
| Reversibility | Simple local rollback | Irreversible data transformation |
| Data | No sensitive data | Personal, regulated, or secret data |
| Security | No trust-boundary change | Authentication, authorization, or tool privilege |
| Uncertainty | Clear canonical requirement | Conflicting stakeholders or missing domain rule |
| Reach | Internal noncritical path | Public API or many teams |
| Operations | No runtime effect | Migration, deployment, monitoring, incident risk |

A quick flow can still require explicit outcome, constraints, acceptance evidence, and human gate. A full lifecycle adds richer requirements, design, tests, QA, tasks, and review where risk warrants it. The [flow-mode guidance](../how-to/choose-flow.md) owns current selection procedure; this lesson supplies the reasoning.

## Stale and conflicting artifacts

### Freshness

An artifact is fresh when it corresponds to the relevant current state. Freshness is relational, not merely a recent date. A test run after a documentation edit may remain valid for code behavior, while a security review from yesterday may be stale if today’s change adds a network call.

Record evidence inputs or version identifiers. If requirement R-003 changes, find design, test, task, implementation, documentation, and evidence links that depend on it. Mark old evidence stale until its applicability is reassessed.

### Contradiction

Artifacts conflict when they imply incompatible behavior: a requirement says 20-minute expiry, an API example says 30, and a test expects 20. Do not select the majority. Identify canonical ownership and decision status. The API may be stale, or the requirement may not have recorded an approved change.

### Omission

An artifact can be consistent yet incomplete. Requirements and tests might agree on the happy path while omitting rate limiting. Traceability should include risk and negative scenarios so agreement does not conceal absence.

### Recovery sequence

1. Stop affected implementation or handoff if the contradiction changes behavior or safety.
2. Capture current artifacts and evidence without overwriting them.
3. Identify the earliest authoritative divergence and accountable owner.
4. Resolve or explicitly defer the decision.
5. Update the canonical upstream artifact first.
6. Propagate the decision to design, tests, tasks, implementation, and documentation.
7. Invalidate or relabel stale evidence.
8. Rerun focused validation and affected role review.
9. Record the traceable handoff and remaining limitations.

## Important distinctions

### Request versus requirement

A request expresses desired work and may be vague. A requirement states an observable need or constraint accepted into scope. Agents can help transform one into the other; humans resolve missing business decisions.

### Requirement versus specification

A requirement is one behavior or quality statement. A specification organizes outcomes, requirements, assumptions, constraints, exclusions, and acceptance into a coherent artifact. The terms may be used differently elsewhere, so follow repository conventions.

### Specification versus plan

A specification defines what and why within boundaries. A plan organizes how and when work will be performed. Mixing tasks into requirements can lock implementation prematurely; omitting feasibility can make a specification impossible. Iteration connects them.

### Test case versus validation evidence

A test case describes what should be checked. Validation evidence records what was actually checked and observed against a version and environment. A complete test document with no run evidence is not proof of passing behavior.

### Implementation versus completion

Implementation is a changed system state. Completion requires current validation, artifact alignment, human decisions, and handoff under the defined acceptance boundary. A code diff is necessary for many changes but insufficient as universal evidence.

### Human review versus automatic gate

An automatic gate executes deterministic checks. A human review evaluates evidence and makes decisions within authority. Neither should be described as the other. Automation can block a merge; it does not own business acceptance.

### Harness SDD versus GitHub Spec Kit

GitHub Spec Kit is an external project with its own commands, templates, and artifact progression. Its public material can help compare approaches. It does not define this harness. The harness integrates specification work with its own skills, lifecycle state, context packs, QA, evidence, council, validation, and human authority rules. Never copy a Spec Kit command into harness guidance unless the repository actually implements it and its canonical owner documents it.

## Worked examples

### Worked example 1 — saved filters from request to handoff

**Request:** “Let users save report filters.”

**Accepted outcome:** Authorized analysts can save, rename, apply, and delete up to ten personal filter sets per workspace. Sharing and organization-wide templates are out of scope. The product owner records the boundary.

**Requirements:** Names are unique per user and workspace without case sensitivity; criteria preserve supported field types; deleted source fields produce a visible invalid-filter state rather than silent broadening; authorization is checked on every operation.

**Design boundaries:** The service owns validation and authorization. The database enforces normalized uniqueness. The API returns a documented conflict. A migration adds storage without changing existing report queries.

**Tests and QA:** Unit cases cover normalization. Integration covers concurrent creation and authorization. End-to-end covers save/apply/delete and invalid fields. Security review checks workspace isolation. Accessibility review checks error announcement and keyboard use.

**Tasks:** migration and rollback; service operations; API contract; interface behavior; tests; documentation; focused validation; product evidence capture.

**Evidence and handoff:** Exact tests run against the change revision, migration rehearsal, API contract validation, manual accessibility record, security finding resolution, and product owner acceptance. The release handoff names one deferred sharing feature and current evidence.

The chain prevents a plausible code implementation from silently choosing sharing behavior or ignoring deleted fields.

### Worked example 2 — requirement changes during implementation

An initial specification allows ten saved filters. During implementation, a pilot customer needs twenty. A developer changes a constant and updates its unit test. The code now passes, but the accepted outcome, API limits, performance data, interface copy, and QA plan still say ten.

The team pauses completion. Product ownership confirms twenty and records why. Analysis checks whether subscription tiers or workspace rules are affected. Design reassesses list performance and quota storage. QA adds boundary cases for 20 and 21. Documentation and API examples update. Prior performance evidence is marked stale and rerun for the larger profile. The handoff records the decision and new evidence.

The implementation was not “wrong” because change occurred; the defect would be allowing artifact drift to masquerade as completion.

### Weak example — code-led specification after the fact

> Ask an agent to implement saved filters. When tests pass, generate a specification that describes what the code does and mark every requirement complete.

This reverses authority. The generated specification can rationalize accidental behavior, tests can repeat agent assumptions, and no product owner accepted the outcome. It also lacks negative cases, evidence freshness, and handoff.

### Corrected example — accepted intent controls implementation

> Clarify the saved-filter outcome, actors, exclusions, rules, risks, and acceptance evidence. Record open questions. Design the responsibility boundaries and derive tests and tasks. Implement in bounded changes. Compare the diff and results against accepted artifacts, update authorized changes upstream, invalidate stale evidence, run focused validation, and route product, security, engineering, and release decisions to their owners.

The corrected approach is iterative but traceable. It does not freeze learning; it controls how learning changes the delivery chain.

## Harness connection

Repository-owned pages define exact behavior:

- [What is AI SDLC?](../foundations/ai-sdlc.md) is the concise canonical foundation.
- [What is SDD?](../foundations/sdd.md) defines the repository interpretation.
- [Human and agent responsibilities](../foundations/responsibilities.md) owns authority boundaries.
- [Specification-driven development skill](../reference/skills/ai-sdlc-sdd.md) owns exact inputs, writes, flows, helpers, gates, and handoff.
- [Workflow map](../reference/workflow-map.md) shows current lifecycle routing.
- [Artifact routing](../reference/artifact-routing.md) owns artifact location and routing rules.
- [Manage evidence freshness](../how-to/manage-evidence-freshness.md) owns the operational recovery procedure.
- [Choose a flow mode](../how-to/choose-flow.md) owns current quick, full, and lifecycle selection guidance.

Use this lesson to understand relationships. Do not use it as a substitute for installed skill contracts or commands. Harness behavior can evolve; reference pages are generated or maintained from current repository sources.

## Role perspectives

### PM or PO

Own outcome, priority, scope, and acceptance according to governance; do not let technical tests impersonate product acceptance.

### Business Analyst

Trace actors, rules, exceptions, assumptions, and conflicts into testable requirements without inventing domain answers.

### QA

Map acceptance to representative coverage and report evidence version, environment, selection, freshness, and limitations.

### Developer or architect

Assess feasibility and design impact; link implementation to requirements and record deviations.

### Security reviewer

Bring threats, data, permissions, supply chain, abuse cases, and evidence into relevant stages; risk acceptance remains human-owned.

### Delivery leader

Track dependencies, gates, blockers, owners, and freshness without rewarding document volume.

## Practice exercise

### Scenario

A customer-support product receives this request: “Add an urgent flag to tickets so important customers get faster help.” The request contains no definition of important customer, who may set urgency, response-time target, audit behavior, accessibility need, or misuse control. A prototype already adds a red icon and a boolean database column. Two unit tests pass. The developer says the feature is 90% complete.

### Supplied starting state

- Initial request as written above.
- Prototype diff summary: red icon, boolean `urgent`, unrestricted update endpoint.
- Existing policy: support priority decisions are owned by Operations; customer tier data is commercially sensitive.
- Test evidence: two unit tests for boolean serialization, run before the latest interface edit.
- Open decision owners: Product for outcome, Operations for priority policy, Security for misuse risk, Accessibility for non-color cues.

### Exact learner task

Create a traceability packet with this chain:

```text
request
→ accepted outcome
→ requirement
→ design boundary
→ test case
→ implementation task
→ validation evidence
→ human review
→ traceable handoff
```

For each node, write at least one original entry and identify its owner or source. Add assumptions, exclusions, risks, and open questions. Mark the prototype and test evidence as current, stale, unsupported, or out of scope with reasons. Select proportionate rigor and identify required gates. Include one negative misuse scenario and one accessibility condition.

### Permitted actions

- Analyze only the supplied state and linked repository concepts.
- Propose requirements, design options, tests, tasks, evidence, and owner questions.
- Mark unknowns and stop conditions.
- Recommend whether prototype work can be retained after review.
- Produce a traceability table and handoff outline.

### Prohibited actions

- Do not decide what “important customer” means.
- Do not accept Operations, Security, Accessibility, or Product decisions on their behalf.
- Do not call two unit tests completion evidence for the feature.
- Do not use color as the only urgency signal.
- Do not infer authorization from the unrestricted prototype endpoint.
- Do not claim the prototype is 90% complete without a defined denominator.

### Suggested traceability table

| ID | Artifact type | Statement or question | Upstream source | Downstream evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| OUT-01 | Proposed customer outcome | Faster handling for an accepted eligible case; acceptance wording is pending | Initial request | Product acceptance criteria needed | Product | open |
| RULE-01 | Priority policy | Eligibility, setter, and queue effect are undefined | Existing policy | Decision table and scenario tests needed | Operations | open |
| RISK-01 | Misuse risk | Unauthorized urgency could reorder queues | Prototype endpoint | Authorization negative test needed | Security | open |

Add enough rows to reach the handoff. Include a current-evidence column or separate evidence register.

### Verification procedure

Trace every requirement backward to an accepted source or explicit open question. Trace every high-impact requirement forward to a test and expected evidence. Confirm the prototype does not define policy merely because it exists. Confirm stale unit evidence is not counted for the interface change. Confirm each human decision is assigned. Confirm security, accessibility, audit, and negative cases are present.

### Common mistakes

Learners often rewrite the initial request as a formal sentence without resolving ambiguity. They turn “red icon” into a requirement because code already exists. They choose a response-time target to make the table complete. They list test cases but no actual evidence. They mark the endpoint complete because serialization passes. They use “stakeholders” as owner instead of a named role.

### Failure path and recovery

If you invent policy, replace it with an open question, safest provisional behavior, and owner. If the traceability table has implementation rows with no requirement, classify possible scope drift. If tests have no version relation, mark them stale or insufficient. If two owners disagree, preserve both positions and stop affected implementation. Update the accepted outcome first after a decision, then propagate and revalidate.

### Completion criteria

The exercise is complete when every chain node is represented, unknowns remain visible, at least one functional and three relevant non-functional concerns are covered, negative and accessibility cases exist, current evidence is distinguished from planned tests, human gates are assigned, and the handoff states limitations. The packet is learning evidence, not product approval.

## Check your understanding

### 1. The code and tests agree, but the accepted requirement says something else. Which is authoritative?

<details>
<summary>Answer: requirement versus aligned code and tests</summary>

The accepted requirement controls intended behavior until its authorized owner changes it. Code and tests may share the same drift. Stop, resolve the discrepancy, update upstream artifacts when authorized, then propagate and rerun evidence.

</details>

### 2. Does spec-driven development prevent requirement changes?

<details>
<summary>Answer: specification-driven change handling</summary>

No. It makes change explicit and traceable. Authorized decisions update the specification and dependent design, tests, tasks, implementation, documentation, and evidence. Unrecorded drift is the problem, not learning.

</details>

### 3. Why is a code diff insufficient completion evidence?

<details>
<summary>Answer: limits of diff evidence</summary>

A diff shows implementation change, not that requirements were accepted, behavior works, negative cases were checked, risks were addressed, documentation aligns, or human gates occurred. Completion uses multiple scoped evidence types.

</details>

### 4. Is a full lifecycle always required?

<details>
<summary>Answer: adaptive lifecycle rigor</summary>

No. Rigor is adaptive. A small reversible change may use a compact path. Every path still needs a bounded outcome, relevant context, acceptance evidence, scope discipline, and required human decisions. Higher uncertainty or impact warrants richer artifacts and gates.

</details>

### 5. Can an AI agent approve a specification it drafted?

<details>
<summary>Answer: specification approval authority</summary>

No. It can self-check, run deterministic validation, or request independent review. Approval belongs to named human owners under governance. Agent agreement is evidence, not authority.

</details>

## Common failure modes

- **Formalized ambiguity:** rewriting a vague request without resolving decisions. Record questions and owners.
- **Code as policy:** treating prototype behavior as the requirement. Trace back to accepted outcome.
- **Generated chain consistency:** requirements, tests, and code repeat one unsupported assumption. Verify upstream sources independently.
- **Happy-path specification:** omitting errors, misuse, boundaries, and recovery. Add risk-based negative cases.
- **Non-functional blindness:** ignoring security, privacy, accessibility, performance, operations, and maintainability.
- **Stale evidence:** reusing results from an earlier relevant state. Relate evidence to inputs and version.
- **Orphan tasks:** implementation work with no requirement or design link. Classify scope drift or add authorized traceability.
- **Document volume as rigor:** creating many artifacts with little decision value. Use proportionate, current artifacts.
- **Gate theater:** marking review complete without evidence or owner. Define observable criteria.
- **Authority transfer:** allowing agents or reviewer consensus to accept product or risk decisions.
- **External framework substitution:** presenting another SDD tool’s commands as harness behavior. Follow repository-owned contracts.

## Recovery guidance

When implementation outruns specification, freeze affected work, inventory behavior, recover the authoritative outcome, and ask owners whether deviations are defects, accepted changes, or out of scope. Update upstream artifacts only after decisions.

When requirements conflict, record both interpretations and their effects, locate owners and decision history, and block affected action when no authorized provisional behavior exists.

Retain stale evidence as history but remove it from current completion claims. Record the invalidating change, focused rerun, unavailable sources, and remaining risk.

When an agent fabricates an artifact or command, stop using it, verify canonical sources, correct dependents, and add a preventive check where useful.

## Evidence of completion

You have completed this chapter when you can provide:

- the urgent-ticket traceability packet covering every chain node;
- a list of source facts, proposals, assumptions, and open decisions;
- functional and relevant non-functional requirements with owners;
- positive, negative, boundary, accessibility, and misuse test intent;
- a current-versus-stale evidence assessment;
- an adaptive-rigor decision with reasons;
- named gates and human decision owners;
- a recovery sequence for one conflicting or changed artifact;
- a handoff that states limitations and next owner.

## Completion checklist

- [ ] I can explain ordinary SDLC and what AI changes.
- [ ] I use the harness definition of spec-driven development.
- [ ] I distinguish requests, outcomes, requirements, specifications, plans, tasks, and evidence.
- [ ] I trace implementation backward to accepted intent and forward to current evidence.
- [ ] I include functional and relevant non-functional requirements.
- [ ] I keep assumptions, constraints, exclusions, and decisions separate.
- [ ] I choose rigor based on uncertainty and impact, not document volume.
- [ ] I identify stale evidence after relevant changes.
- [ ] I recover contradictions through canonical ownership, not majority vote.
- [ ] I preserve human approval and risk authority.
- [ ] My handoff names current artifacts, evidence, omissions, and owner.

## Previous learning step

Return to [Independent multi-role review with subagents](multi-role-review.md) if you cannot yet preserve evidence, disagreement, and human authority across several reviews.

## Next learning step

Continue to [Harness essentials](harness-essentials.md) to learn the installed harness environment, navigator, skills, flow choices, state, artifacts, Evidence Council, Quality Lenses, blockers, and handoffs.

## Sources and adaptation notes

- **HARNESS-DOCS** — [AI SDLC Harness documentation and repository contracts](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/faccb4354464a1a3cc309b7b2dfa65e8efaf3529/docs). Owner: AI SDLC Harness maintainers; revision: `faccb4354464a1a3cc309b7b2dfa65e8efaf3529`; reuse: `internal-authority`; mode: `synthesized`. Informed: AI SDLC, SDD, and evidence. Transformed: original feature traces form the lesson. Limitation: operational pages remain canonical.
- **HARNESS-SKILLS** — [AI SDLC Harness skill contracts and deterministic helpers](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/faccb4354464a1a3cc309b7b2dfa65e8efaf3529/skills). Owner: AI SDLC Harness maintainers; revision: `faccb4354464a1a3cc309b7b2dfa65e8efaf3529`; reuse: `internal-authority`; mode: `synthesized`. Informed: artifacts, validation, and handoff. Transformed: contracts became an alignment model. Limitation: Reference owns exact commands.
- **GITHUB-SPEC-KIT** — [GitHub Spec Kit](https://github.com/github/spec-kit). Owner: GitHub; revision: `7873c447bd5ea8f919d7bdde8b118525c463d9c0`; reuse: `adaptable-with-verification`; mode: `adapted`. Informed: specification-to-task progression. Transformed: an original harness trace adds QA, state, evidence, and gates. Limitation: no command, template, workflow, prose, or example was imported.
- **NIST-SSDF** — [Secure Software Development Framework version 1.1](https://doi.org/10.6028/NIST.SP.800-218). Owner: National Institute of Standards and Technology; revision: `NIST-SP-800-218-2022`; reuse: `reference-only`; mode: `reference`. Informed: lifecycle security and evidence. Transformed: concerns became original gates. Limitation: no practice text or conformance claim was used.
- **NIST-AI-RMF** — [Artificial Intelligence Risk Management Framework 1.0](https://doi.org/10.6028/NIST.AI.100-1). Owner: National Institute of Standards and Technology; revision: `NIST-AI-100-1-2023`; reuse: `reference-only`; mode: `reference`. Informed: ownership and risk response. Transformed: concerns checked harness traceability. Limitation: no framework text or compliance claim was used.
- **W3C-WAI** — [W3C Web Accessibility Initiative tutorials and guidance](https://www.w3.org/WAI/tutorials/). Owner: World Wide Web Consortium; revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. Informed: accessible headings and tables. Transformed: original scenarios include non-color acceptance. Limitation: no tutorial or media was reproduced.
