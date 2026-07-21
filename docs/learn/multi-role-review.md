---
title: "Independent multi-role review with subagents"
description: "Learn how to run evidence-based, read-only reviews across several roles without confusing repeated opinions, consensus, or agent output with approval."
learning_level: 2
audience:
  - beginner
  - product
  - analysis
  - quality
  - engineering
  - security
  - governance
  - documentation
estimated_time: "120–150 minutes"
prerequisites:
  - "Agents, tools, delegation, and safe action"
content_type: "lab"
last_reviewed: "2026-07-21"
source_usage:
  - source_id: HARNESS-DOCS
    mode: synthesized
  - source_id: HARNESS-SKILLS
    mode: synthesized
  - source_id: MS-AGENTS-BEGINNERS
    mode: adapted
  - source_id: NIST-AI-RMF
    mode: reference
  - source_id: OWASP-LLM-SECURITY
    mode: reference
  - source_id: OPENAI-CODEX-DOCS
    mode: reference
  - source_id: W3C-WAI
    mode: reference
---

# Independent multi-role review with subagents

A single reviewer can miss an issue because every review has a point of view. A product reviewer may notice an undefined outcome but miss an unsafe command. A security reviewer may identify excessive permission but not see that a beginner cannot complete the exercise. A documentation maintainer may catch duplicated concepts but not an untestable business rule. Multi-role review deliberately applies different questions to the same frozen artifact.

More reviewers do not automatically create better evidence. If they share conclusions before reviewing, edit the target concurrently, inspect different versions, or report unsupported preferences, the result may only amplify one assumption. Even a sound council does not approve product scope, security risk, release readiness, or publication. It supplies structured evidence to accountable human owners.

This chapter teaches a complete read-only review cycle: prepare one bounded snapshot, run role-specific reviews independently when the environment supports isolation, record evidence and uncertainty in a common schema, synthesize without voting, correct through one parent editor, and recheck affected areas.

## At a glance

**Level:** 2B — independent multi-role re-check

**Audience:** Learners and practitioners who coordinate reviews of specifications, documentation, code changes, test plans, or delivery evidence

**Estimated time:** 120–150 minutes, including the seven-role lab

**Prerequisites:** Complete [Agents, tools, delegation, and safe action](agents-tools-and-subagents.md). You should be able to define read-only scope, evidence requirements, stop conditions, and a human checkpoint.

## Expected outcome

You can run and document a multi-role review without overstating independence or approval. You can freeze one artifact scope, issue comparable reviewer briefs, preserve disagreement, separate facts from proposals, identify accountable owners, and prove that corrected work was re-reviewed.

## What experienced readers may skip

If you already facilitate review councils, skim the introductory case for role diversity. Do not skip **Execution modes and honest labels**, **The common finding contract**, **Synthesis without majority voting**, or the lab. Those sections define evidence and authority boundaries used by this curriculum.

## On this page

- [Why this matters](#why-this-matters)
- [Observable learning objectives](#observable-learning-objectives)
- [Core concepts](#core-concepts)
- [Designing a trustworthy review round](#designing-a-trustworthy-review-round)
- [Execution modes and honest labels](#execution-modes-and-honest-labels)
- [The common finding contract](#the-common-finding-contract)
- [Seven role lenses](#seven-role-lenses)
- [Synthesis without majority voting](#synthesis-without-majority-voting)
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

Software delivery artifacts serve several audiences simultaneously. A requirement must describe value, express rules, support testing, remain feasible, address material risks, and be usable by the people who maintain it. One reviewer rarely has equal depth across all of those concerns. Specialization is therefore useful, but only if review questions are bounded and results can be traced to the same artifact.

AI-assisted review introduces additional risks. A role prompt can create the appearance of expertise without supplying domain facts. Several generated reports may repeat the same pattern because the underlying model, context, or examples are similar. A parent may summarize away disagreement to produce a tidy answer. A reviewer may modify the artifact it is supposed to assess, invalidating other reviews. A team may treat unanimous recommendations as an approval event even though no accountable person made a decision.

The safe alternative is not to reject agent review. It is to treat it as an evidence-collection workflow. Reviewers answer defined questions, cite observable material, state confidence and omissions, and remain read-only. The parent verifies findings against canonical sources and routes decisions. Humans retain product, technical, security, accessibility, delivery, and publication authority assigned by the organization.

## Observable learning objectives

By the end of this chapter, you:

- **Can explain** why role diversity improves issue discovery but does not create approval authority.
- **Can explain** the difference between independent isolated subagents and one agent simulating several perspectives.
- **Can do** a frozen-snapshot review round in which every reviewer receives identical artifact scope and common constraints.
- **Can do** a role-specific review using bounded questions, read-only permission, evidence, severity, classification, confidence, and omissions.
- **Can do** synthesis that preserves conflicts and unique findings without counting votes.
- **Can prove** which execution mode was used, which reviewers completed, what each inspected, what changed after review, and which roles rechecked the corrections.
- **Can prove** that accountable owners—not reviewer count—made or retained required decisions.

## Core concepts

### Review lens

A review lens is a set of questions focused on a quality dimension or stakeholder need. It is not a persona with automatic authority. “New learner” directs attention to prerequisites and clarity. “QA” directs attention to observable behavior and reproducibility. The lens helps discover issues; evidence determines whether a finding is supported.

### Artifact scope

Artifact scope is the exact material under review: named files, a commit, a diff, a rendered page set, or a versioned package. “Review the docs” is not a stable scope. “Review the changes from base commit A to working-tree snapshot B in these ten Learn files, plus linked canonical pages read-only” is closer. All reviewers in one round need the same target.

### Independent execution

Independent execution means reviewers work in isolated contexts, receive the same initial target and constraints, and do not see one another’s initial findings. Different role prompts inside one context are not independent. Separate agents that share a discussion thread or are fed earlier conclusions are also anchored. Independence reduces some correlated bias; it does not guarantee correctness.

### Evidence

Evidence connects a finding to observable material. For documentation, it may be a file and heading, broken link result, measured token count, or conflicting canonical statement. For code, it may be a diff hunk, test result, trace, or API contract. Evidence should be sufficient for the parent to reproduce the concern. Long copied passages are rarely needed; precise location and concise description are safer.

### Severity

Severity communicates likely impact and urgency under a declared scale. This lab uses only `blocker`, `high`, `medium`, and `low`. A blocker prevents the stated acceptance boundary, such as an unsafe instruction or a required exercise that cannot run. High is a material learning, security, or workflow defect. Medium affects a bounded area or causes avoidable ambiguity. Low improves polish without changing the core outcome. Severity is not reviewer seniority.

### Classification

Classification keeps different kinds of statements visible:

- `fact`: an evidenced condition in the reviewed artifact;
- `proposal`: a suggested change or design choice;
- `question`: information needed from an owner or source;
- `risk`: a plausible adverse outcome with uncertainty.

A reviewer can report a fact and then attach a proposal, but the synthesis must not transform the proposal into fact.

### Accountable owner

The accountable owner is the person or role authorized to decide or accept the outcome. It may be a product owner for scope, a security owner for residual risk, a maintainer for navigation architecture, or a release owner for publication. Naming an owner prevents the parent from silently claiming authority.

## Designing a trustworthy review round

### 1. Define the review question

Start with a decision-support question rather than “find anything wrong.” Example: “Does the changed curriculum meet the Learn contract, preserve canonical operational ownership, and provide safe, usable progression from beginner concepts to independent harness use?” This provides a shared boundary while role-specific questions remain distinct.

### 2. Freeze the artifact

Record the base revision, changed paths, and any generated or rendered view reviewers may inspect. Do not edit until all initial reports return. If an urgent correction is necessary, close the round and start a new one; do not quietly give later reviewers a newer version.

### 3. Give every reviewer common input

Common input should contain the outcome, same artifact scope, shared acceptance criteria, source-adaptation rule, read-only instruction, finding schema, severity and classification enums, and a requirement to state omissions. Add role questions without changing the common target.

### 4. Keep reviewers read-only

Read-only workers protect independence and avoid competing edits. A reviewer can recommend a correction but must not implement it. The parent owns the combined edit because only the parent sees all findings, canonical ownership, and conflicts.

### 5. Require bounded evidence

Every material finding names a file, heading or anchor, observable condition, learner or operator impact, and confidence. If a reviewer cannot obtain evidence, it reports a question or risk. It does not state an inference as a confirmed defect.

### 6. Wait for all reviewers

Do not publish an interim conclusion that can anchor remaining workers. Timeouts are possible, but label the reviewer incomplete and state the coverage gap. Never convert a missing report into agreement.

### 7. Synthesize and decide corrections

The parent groups agreements, conflicts, unique findings, unresolved questions, and proposed corrections. It checks repository-owned canonical pages before editing. Decisions are evidence-based and scoped; majority voting is prohibited.

### 8. Recheck after corrections

Run deterministic checks, then ask affected roles to review the corrected artifact and adjacent workflows. A correction can introduce a broken link, shift authority language, duplicate a canonical contract, or make a long page harder to navigate. Rechecking is a new observation, not a ceremonial sign-off.

## Execution modes and honest labels

Use one of these labels in the review record.

### Independent isolated subagents

Use this label only when the host actually provides isolated workers and they do not receive one another’s initial conclusions. Record the host mechanism, shared snapshot identifier, and read-only constraint. Reviewers may use the same model; independence refers to execution context, not statistical independence or organizational independence.

### Simulated multi-role perspectives

Use this label when one agent applies several lenses sequentially or when the environment cannot isolate worker contexts. Simulation can still expose gaps, especially with a strict schema, but it has higher anchoring and correlated-error risk. Do not describe it as a council of independent reviewers.

### Human multi-role review

Humans from several roles may review the same artifact. They can hold organizational authority that agents do not, but the record must still distinguish reviewer input from formal approval. Human reviewers can also anchor one another, inspect different versions, or omit evidence, so a common contract remains useful.

### Mixed review

Some roles may be agents and others humans. Label each participant and execution mode. Do not combine them into an anonymous consensus score.

## The common finding contract

Every lab finding must contain exactly enough context to be audited and routed. Use these fields:

| Field | Required content |
| --- | --- |
| `finding_id` | Stable identifier unique in the review round |
| `reviewer_role` | One of the assigned role labels |
| `severity` | `blocker`, `high`, `medium`, or `low` |
| `file` | Reviewed repository-relative path |
| `heading_or_anchor` | Most precise visible location |
| `evidence` | Observable condition or reproducible check |
| `learner_or_operator_impact` | Consequence for the intended user |
| `classification` | `fact`, `proposal`, `question`, or `risk` |
| `recommended_correction` | Bounded correction or next decision |
| `confidence` | Stated confidence with a reason or limit |
| `accountable_owner` | Human role that owns correction or decision |
| `resolution_status` | Current workflow state, initially `open` |

Allowed severities are only:

- `blocker`
- `high`
- `medium`
- `low`

Allowed classifications are only:

- `fact`
- `proposal`
- `question`
- `risk`

For this lab, use resolution values `open`, `accepted`, `corrected`, `rejected_with_reason`, `deferred_with_owner`, or `not_applicable`. Do not let a reviewer mark its own proposal `corrected`; the parent updates resolution after verification.

### Example finding

```yaml title="One evidence-backed finding"
finding_id: LEARNER-003
reviewer_role: New learner
severity: high
file: docs/learn/harness-essentials.md
heading_or_anchor: "Choose a flow"
evidence: "The exercise requires selecting full flow before quick flow and full flow are defined."
learner_or_operator_impact: "A beginner must guess the central decision and cannot verify the exercise."
classification: fact
recommended_correction: "Define the three flow choices before the exercise and add one comparison case."
confidence: "High; heading order and missing definitions were checked in the same snapshot."
accountable_owner: Documentation maintainer
resolution_status: open
```

The evidence is concise and reproducible. The correction remains a proposal even though the finding is a fact. The maintainer owns the editorial decision.

## Mid-page recap

A trustworthy review round freezes one target, gives every reviewer common constraints, uses role-specific questions, keeps workers read-only, and requires evidence and omissions. Execution mode must be honest. Findings distinguish fact, proposal, question, and risk. Severity helps route attention; it does not grant authority. The parent synthesizes and edits only after all initial reports return.

## Seven role lenses

These roles are lenses for the lab, not organizational approval grants.

### 1. New learner

Ask: Are prerequisites explicit? Are terms defined before use? Can a learner predict the outcome of each step? Are examples understandable without hidden Git, AI, or delivery experience? Can the exercise be completed and recovered? Does page length remain navigable?

Evidence includes first-use terminology, links, task instructions, answer explanations, and dead ends. The learner reviewer must not redesign technical contracts from preference.

### 2. PM or PO

Ask: Is the intended user outcome explicit? Are scope, non-scope, assumptions, and acceptance boundaries visible? Does the lesson preserve product decision authority? Are product examples realistic and not disguised technical implementation decisions?

This lens reports where product ownership is missing or improperly delegated. It does not approve security or architecture choices for their owners.

### 3. Business Analyst

Ask: Are actors, conditions, rules, exceptions, and terminology consistent? Can requirements be traced to examples, tests, and handoffs? Does the content distinguish facts from assumptions and route stakeholder conflicts?

The BA lens should locate competing interpretations and identify missing elicitation, not invent an agreement.

### 4. QA

Ask: Are learning objectives observable? Do exercises state starting state, permitted actions, output, evidence, verification, negative cases, and recovery? Are knowledge-check answers correct? Can token and source checks be reproduced? Are completion criteria stronger than self-reported confidence?

QA may identify a blocker when an exercise cannot be executed as written. Formal publication remains with its owner.

### 5. Developer or Architect

Ask: Are model, tool, agent, subagent, state, and repository concepts technically coherent? Do examples reflect feasible workflows? Do relative links and canonical ownership work? Is the implementation maintainable? Does a lesson accidentally redefine a skill contract?

This reviewer separates repository behavior from vendor behavior and proposal from current architecture.

### 6. Security, Governance, and Accessibility

Ask: Does the content address secrets, sensitive data, prompt injection, untrusted inputs, least privilege, destructive actions, and human gates? Are compliance claims avoided? Are headings logical, links descriptive, tables usable, and images supplied with meaningful alternatives? Is any action unsafe for a learner to copy?

Security, governance, and accessibility contain distinct ownership domains; this combined lens discovers issues and routes them rather than accepting risk on behalf of all three.

### 7. Head of AI Practice or Documentation Maintainer

Ask: Does the sequence build prerequisites? Does Learn teach while Reference owns contracts and Use owns procedures? Are sources current and adaptations original? Are navigation, validation, page length, maintenance ownership, and contribution rules sustainable? Does the curriculum create a duplicate terminology authority?

This lens owns or advises curriculum maintenance according to repository governance. It does not inherit product or risk authority.

## Synthesis without majority voting

### Agreements

An agreement is the same material issue supported by more than one reviewer. Merge duplicate records while preserving contributing roles and their distinct impact statements. Agreement can increase confidence that an issue affects several audiences, but it does not determine the correction automatically.

### Conflicts

A conflict exists when reviewers recommend incompatible outcomes, assign materially different severity, or interpret the canonical contract differently. Preserve both findings. Check repository authority and ask the accountable owner when evidence cannot resolve the difference. Do not average severity or choose the more senior-sounding role.

### Unique findings

Role specialization is intended to create unique findings. A single security reviewer may be the only person to detect an unsafe copy-paste command. A single learner may be the only person to notice a missing prerequisite. Evaluate evidence and impact rather than reviewer count.

### Unresolved questions

Questions identify missing authority, source material, or decision context. Keep them open with owners. A tidy report that removes questions can be less trustworthy than an incomplete report that names them precisely.

### Proposed corrections

The parent maps accepted findings to bounded edits and acceptance checks. It may reject a proposal with a reason—for example, because it would duplicate a canonical skill contract. Rejection of a correction does not erase the original fact; another resolution may be needed.

### No council-by-score

Do not compute approval from seven “pass” labels, a median confidence, or the number of low findings. Those calculations can summarize activity but cannot establish product acceptance or release authority. Readiness depends on defined criteria, evidence freshness, unresolved severity, and accountable decisions.

## Important distinctions

### Perspective diversity versus independence

Different role questions create perspective diversity. Separate isolated execution creates a degree of independence. You can have one without the other. Both are useful, and both must be labeled accurately.

### Review finding versus decision

A finding says what a reviewer observed or inferred. A decision selects an action under authority and records rationale. A parent can correct an obvious broken link within its editorial authority but must route a change in product acceptance semantics to product ownership.

### Consensus versus approval

Consensus describes alignment among participants. Approval is a governed act by a named owner. Seven reviewers can agree that a change is ready and still lack publication authority.

### Recheck versus repeated opinion

A recheck examines a corrected artifact and validates the affected condition. Asking the reviewer “Do you agree now?” without a new snapshot and evidence is repeated opinion, not revalidation.

### Evidence Council versus Quality Lenses

The repository’s Evidence Council and Quality Lenses are canonical operational skills with exact contracts. This lesson explains why evidence gathering and diverse lenses matter. It does not merge or restate their complete behavior. Follow their reference pages for current invocation, state, outputs, and human checkpoints.

## Worked examples

### Worked example 1 — conflict resolved by canonical ownership

A beginner reviewer reports that every skill command should be copied into the lesson so learners do not need links. A maintainer reviewer reports that copying commands would create stale duplicates. Both cite the same page.

The parent records a conflict instead of counting votes. It checks the site architecture: Learn teaches concepts; skill references own exact contracts. The beginner’s fact—that task switching is difficult—is accepted. The proposed correction is changed: the lesson adds a short decision example and a descriptive link to the canonical skill page, but does not duplicate the command block. The maintainer rechecks canonical ownership; the learner rechecks discoverability.

This synthesis addresses the evidenced impact without violating repository authority.

### Worked example 2 — unique high-severity finding outweighs six passes

Six reviewers report no material issue in a lab. The security reviewer finds that the “recovery” step tells learners to paste a full environment file into an external agent. It cites the exact heading and classifies likely secret disclosure as `high` risk.

The parent stops publication of the affected lesson even though six reviews passed. It replaces the instruction with local key-name inspection and approved secret-handling escalation. Security and learner reviewers recheck the correction. The organization’s security owner retains any residual-risk decision.

Reviewer count was irrelevant; evidence and impact controlled the response.

### Weak example — council by applause

> Give the document to seven role agents. Ask whether it looks good. If five approve, publish it. Let agents fix small issues while reviewing.

This mixes versions, permits concurrent edits, supplies no bounded questions or evidence schema, and turns a vote into publication authority. It also cannot distinguish simulated perspectives from isolated review.

### Corrected example — frozen, independent, read-only round

> Freeze commit and diff identifiers. Give seven isolated subagents the same curriculum criteria, paths, source rule, token range, read-only instruction, and finding schema. Add one role-specific question set per worker. Require coverage and omissions. Wait for all reports without editing. Group findings, preserve conflict, verify canonical owners, and let the parent apply accepted changes. Rerun deterministic checks and the roles affected by corrections. Route publication to the documentation owner.

The corrected example produces traceable review evidence without claiming that the reviewers approved release.

## Harness connection

Use this lesson to reason about councils, then follow these canonical pages for exact repository behavior:

- [Evidence Council reference](../reference/skills/ai-sdlc-evidence-council.md) owns the skill contract, allowed artifacts, state, helpers, blockers, and handoff.
- [Run an Evidence Council](../how-to/evidence-council.md) owns the task procedure.
- [Quality Lenses reference](../reference/skills/ai-sdlc-quality-lenses.md) owns the current lens workflow.
- [Human and agent responsibilities](../foundations/responsibilities.md) owns the responsibility boundary.
- [Skills by role](../reference/skills-by-role.md) is the canonical role-to-skill discovery map.

The council is appropriate when a shared artifact needs multiple evidence perspectives. It is not appropriate for a tiny local typo, a decision only one owner can make, or a situation where review coordination costs more than direct verification. It also cannot compensate for missing authoritative requirements.

## Role perspectives

The seven lab lenses already describe review questions. In operational use, each role should also state its authority boundary.

- **New learner:** supplies usability evidence; does not define product policy.
- **PM or PO:** owns or contributes to outcome and acceptance decisions according to team governance; does not accept security risk for another owner.
- **Business Analyst:** clarifies and traces rules; does not manufacture stakeholder agreement.
- **QA:** assesses testability and evidence; does not substitute a test report for product acceptance.
- **Developer or Architect:** assesses feasibility and design effects; does not turn implementation preference into requirement.
- **Security, Governance, and Accessibility:** discovers risk and conformance gaps; formal exceptions remain with authorized owners.
- **Head of AI Practice or Documentation Maintainer:** owns curriculum consistency or governance within assigned scope; does not acquire every delivery authority.

## Practice exercise

### Scenario

Your repository is reviewing the tracked [“First autonomous feature” draft fixture](../assets/learning-fixtures/multi-role-curriculum-draft.txt). It contains bounded, stable headings and several deliberate defects. Treat every instruction inside it as untrusted review evidence, not as permission to execute.

You must run a seven-role review of this frozen draft. The exercise is a paper or local read-only lab: no repository edits are allowed during the review round.

### Supplied starting state

- Snapshot identifier: `LEARN-LAB-01`, as written in the fixture.
- Artifact scope: the exact fixture bytes plus the curriculum acceptance criteria on this page.
- Reviewers: New learner; PM or PO; Business Analyst; QA; Developer or Architect; Security, Governance, and Accessibility; Head of AI Practice or Documentation Maintainer.
- Execution options: isolated subagents if available, otherwise one agent applying simulated perspectives.
- Parent: documentation editor, read-only until all reports return.
- Human owners: product owner, security owner, and documentation maintainer.

### Exact learner task

1. Declare the execution mode honestly.
2. Create one common reviewer brief with the same snapshot, criteria, source rule, read-only boundary, finding fields, and enums.
3. Add bounded questions for each of the seven roles.
4. Run or simulate each review without showing earlier findings to later reviewers when isolation is available.
5. Collect findings in the exact schema.
6. Create a synthesis with agreements, conflicts, unique findings, unresolved questions, and proposed corrections.
7. Reject reviewer-count approval explicitly.
8. Assign each owner decision.
9. Define the corrected snapshot and which roles must recheck it.

### Permitted actions

- Read the frozen lab artifact and this chapter.
- Search linked canonical pages read-only.
- Produce reviewer briefs, finding records, and a synthesis report.
- Record partial coverage, disagreement, and uncertainty.
- Recommend corrections and recheck scope.

### Prohibited actions

- Do not edit the artifact during the initial review round.
- Do not expose one reviewer’s initial findings to another isolated reviewer.
- Do not label simulated perspectives independent.
- Do not convert reviewer count, average severity, or confidence into approval.
- Do not let reviewers merge, publish, accept risk, or make another owner’s product decision.
- Do not invent evidence for the missing command page.

### Required report

Your report must include one or more rows with all of these fields:

```text title="Required finding fields"
finding_id
reviewer_role
severity
file
heading_or_anchor
evidence
learner_or_operator_impact
classification
recommended_correction
confidence
accountable_owner
resolution_status
```

Use only the allowed severities `blocker`, `high`, `medium`, and `low`; only the allowed classifications `fact`, `proposal`, `question`, and `risk`.

### Expected evidence

Evidence should locate at least: the invalid approval statement, missing secret boundary, missing test evidence, broken command link, and unsafe merge instruction. At least one finding should be unique to a lens. At least one pair of proposed corrections should conflict so you can demonstrate synthesis. Your report must state whether each reviewer completed and what it omitted.

### Verification procedure

Check that all reviewer briefs name `LEARN-LAB-01`. Confirm every reviewer was read-only and had the same common criteria. Confirm the report contains all required fields and enum values. Trace every fact to the fixture file and a bracketed heading. Verify that proposals remain distinct from facts. Confirm human owners are named and that no review result says “approved.”

### Common mistakes

Learners often allow a reviewer to edit a typo, which changes the shared snapshot. They use “critical” even though it is not an allowed severity. They collapse the security and learner effects into one vague record. They drop a dissenting proposal because six reports prefer another. They state “independent” when one conversation simulated all roles.

### Failure path and reset

If any edit occurs, discard no user work; instead close the round, record the event, create a new snapshot identifier, and restart every initial review. If a reviewer times out, mark it incomplete and do not count silence as a pass. If isolation is unavailable, switch the record to `simulated multi-role perspectives`, clear earlier role conclusions from the brief where possible, and state the limitation. If a source is missing, create a question or blocker rather than fabricating its content.

### Completion criteria

The lab is complete when all seven roles have a report or explicit incomplete status, the common snapshot is proven, required findings are evidenced, disagreement is visible, owner decisions are routed, the parent correction plan is bounded, and a recheck plan exists. Completion does not authorize publication.

## Check your understanding

### 1. Seven reviewers independently say “no issues.” What can you conclude?

<details>
<summary>Answer: limits of seven no-issue reports</summary>

You can conclude that seven bounded reviews reported no issue within their declared coverage. You cannot conclude that the artifact is correct, approved, or safe outside that coverage. Inspect omissions, evidence quality, correlated model risk, deterministic validation, and owner gates.

</details>

### 2. Can a reviewer correct a broken link during the initial round?

<details>
<summary>Answer: edit ownership during review</summary>

No. Even a harmless edit changes the artifact for later reviewers. The reviewer records the fact and correction proposal. The parent edits after all initial reports return.

</details>

### 3. Two reviewers disagree on severity. Should the parent average the values?

<details>
<summary>Answer: severity disagreement</summary>

No. Preserve both rationales, examine impact and acceptance criteria, and assign severity under the declared scale. Ask the accountable owner when the difference reflects risk tolerance or policy.

</details>

### 4. One agent produces seven role sections. What execution label applies?

<details>
<summary>Answer: simulated multi-role execution label</summary>

Simulated multi-role perspectives. Role headings do not provide isolated context. The result may still be useful if its limitation is explicit.

</details>

### 5. Why re-run selected roles after corrections?

<details>
<summary>Answer: purpose of post-correction recheck</summary>

Corrections can fail to resolve the original impact or introduce adjacent defects. The affected reviewer tests the new artifact, while deterministic checks catch structural regressions. Recheck evidence is stronger than an editor’s assertion.

</details>

## Common failure modes

- **Different targets:** later reviewers inspect a changed artifact. Freeze or restart the round.
- **Hidden anchoring:** reviewers see earlier conclusions. Isolate initial execution or label it simulated.
- **Free-form findings:** reports omit evidence or ownership. Enforce the common schema.
- **Concurrent corrections:** reviewers edit while assessing. Keep them read-only.
- **Severity inflation:** every preference becomes a blocker. Tie severity to acceptance impact.
- **Fact–proposal collapse:** a suggested rewrite is presented as the only truth. Preserve classification.
- **Consensus approval:** a pass count triggers publication. Route the decision to its owner.
- **Silent timeout:** a missing reviewer is treated as agreement. Record incomplete coverage.
- **Canonical duplication:** the lesson copies an operational contract to satisfy a reviewer. Link the canonical owner instead.
- **Review fatigue:** repeated reviewers report the same low-value wording issue. Deduplicate and narrow subsequent questions.
- **No recheck:** corrections are assumed effective. Inspect the corrected snapshot and adjacent links.

## Recovery guidance

If independence is compromised, stop the round and record how: shared findings, changed snapshot, or a reviewer edit. Decide whether the affected reports remain useful as simulated perspectives. Start a new isolated round only if the benefit justifies the cost.

If the finding schema is incomplete, ask reviewers to amend metadata without changing their substantive conclusion. If evidence cannot be reproduced, downgrade the item to a question or risk and state why. If two canonical sources conflict, preserve the conflict and route it to the owning maintainer; do not let synthesis invent precedence.

If reviewers produce excessive duplicates, retain one primary finding, list contributing roles, and preserve distinct impacts. If a material unique finding arrives after edits began, pause corrections, record the changed scope, and decide whether to restart. If a security or destructive-action blocker appears, stop affected action immediately and involve its human owner.

For a failed recheck, reopen the finding rather than creating a new identifier unless the correction introduced a distinct issue. Record the new evidence, revise the correction, rerun relevant validation, and ask the same affected role to inspect the next snapshot.

## Evidence of completion

Provide these artifacts:

- execution-mode statement and limitation;
- frozen snapshot identifier and exact scope;
- common reviewer brief plus seven question sets;
- completion and omission record for every reviewer;
- structured findings using every required field;
- synthesis separated into agreements, conflicts, unique findings, unresolved questions, and proposed corrections;
- resolution and accountable owner for each item;
- parent-owned correction plan;
- deterministic validation and affected-role recheck plan;
- explicit statement that reviewer agreement did not create approval.

## Completion checklist

- [ ] I froze one target before review.
- [ ] Every reviewer received the same common input.
- [ ] Reviewers remained read-only.
- [ ] I labeled isolated and simulated execution honestly.
- [ ] Every material finding has reproducible evidence and confidence.
- [ ] I used only the allowed severity and classification values.
- [ ] I preserved facts, proposals, questions, and risks separately.
- [ ] I did not vote on truth or approval.
- [ ] Unique findings received evidence-based consideration.
- [ ] Accountable owners retained their decisions.
- [ ] The parent owns all corrections.
- [ ] Corrected areas and adjacent workflows have a recheck plan.

## Previous learning step

Return to [Agents, tools, delegation, and safe action](agents-tools-and-subagents.md) if you cannot yet bound read-only work, define stop conditions, or recover an incomplete result.

## Next learning step

Continue to [AI SDLC and spec-driven development](ai-sdlc-and-sdd.md) to connect multi-role evidence with requirements, design, tests, tasks, implementation, and traceable handoff.

## Sources and adaptation notes

- **HARNESS-DOCS** — [AI SDLC Harness documentation and repository contracts](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/faccb4354464a1a3cc309b7b2dfa65e8efaf3529/docs). Owner: AI SDLC Harness maintainers; revision: `faccb4354464a1a3cc309b7b2dfa65e8efaf3529`; reuse: `internal-authority`; mode: `synthesized`. Informed: authority and evidence. Transformed: an original review lab teaches the model. Limitation: linked references own review contracts.
- **HARNESS-SKILLS** — [AI SDLC Harness skill contracts and deterministic helpers](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/faccb4354464a1a3cc309b7b2dfa65e8efaf3529/skills). Owner: AI SDLC Harness maintainers; revision: `faccb4354464a1a3cc309b7b2dfa65e8efaf3529`; reuse: `internal-authority`; mode: `synthesized`. Informed: Evidence Council and Quality Lenses. Transformed: contracts became fixture practice. Limitation: exact behavior was not copied.
- **MS-AGENTS-BEGINNERS** — [AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners). Owner: Microsoft; revision: `b7f34fd824767162f484e03cc500e23c0966372f`; reuse: `adaptable-with-verification`; mode: `adapted`. Informed: orchestration prerequisites. Transformed: an original immutable review council replaces source activities. Limitation: structure, code, examples, and media were excluded.
- **NIST-AI-RMF** — [Artificial Intelligence Risk Management Framework 1.0](https://doi.org/10.6028/NIST.AI.100-1). Owner: National Institute of Standards and Technology; revision: `NIST-AI-100-1-2023`; reuse: `reference-only`; mode: `reference`. Informed: risk ownership and response. Transformed: concerns became owner-bearing findings. Limitation: no framework text or compliance claim was used.
- **OWASP-LLM-SECURITY** — [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html). Owner: OWASP Foundation Cheat Sheet Series; revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. Informed: untrusted content and permissions. Transformed: an original unsafe-draft fixture makes them reviewable. Limitation: no checklist, attack text, or code was copied.
- **OPENAI-CODEX-DOCS** — [Official Codex behavior documentation set](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Owner: OpenAI; revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. Informed: [subagent](https://learn.chatgpt.com/docs/agent-configuration/subagents) behavior. Transformed: isolation limits became host-neutral rules. Limitation: no vendor prose or promise was reused.
- **W3C-WAI** — [W3C Web Accessibility Initiative tutorials and guidance](https://www.w3.org/WAI/tutorials/). Owner: World Wide Web Consortium; revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. Informed: headings, links, and tables. Transformed: presentation was checked. Limitation: no tutorial or media was reproduced.
