---
title: "Agents, tools, delegation, and safe action"
description: "Learn how agents use tools, how to bound subagent work, and how permissions, evidence, stop conditions, and human authority keep repository changes safe."
learning_level: 2
audience:
  - beginner
  - product
  - analysis
  - quality
  - engineering
  - security
estimated_time: "100–130 minutes"
prerequisites:
  - "AI foundations"
  - "Prompt engineering"
  - "Context, verification, and evidence"
content_type: "lesson"
last_reviewed: "2026-07-21"
source_usage:
  - source_id: HARNESS-DOCS
    mode: synthesized
  - source_id: HARNESS-SKILLS
    mode: synthesized
  - source_id: MS-AGENTS-BEGINNERS
    mode: adapted
  - source_id: NIST-GENAI-PROFILE
    mode: reference
  - source_id: OWASP-LLM-SECURITY
    mode: reference
  - source_id: OPENAI-CODEX-DOCS
    mode: reference
  - source_id: W3C-WAI
    mode: reference
---

# Agents, tools, delegation, and safe action

An agent is useful because it can do more than generate text: it can inspect state, choose a bounded next action, call an allowed tool, and evaluate the result. That capability also creates risk. A plausible plan is not proof that a command was safe, a successful tool call is not proof that the requested outcome was achieved, and a subagent report is not a human decision.

This chapter gives you a practical operating model. You will learn to separate a model from its tools, control the action loop, distinguish read, write, reversible, and destructive actions, and delegate one small read-only task with an explicit output contract. The emphasis is not on a particular vendor interface. It is on durable repository state, least privilege, observable evidence, and accountable handoffs.

## At a glance

**Level:** 2A — tools, agents, delegation, and subagents

**Audience:** Anyone who asks an AI system to inspect a repository, run a command, create an artifact, or coordinate another reviewer

**Estimated time:** 100–130 minutes, including the practice exercise

**Prerequisites:** Complete [AI foundations](ai-foundations.md), [prompt engineering](prompt-engineering.md), and [context, verification, and evidence](context-and-verification.md), or demonstrate the equivalent skills.

## Expected outcome

You can design and supervise a bounded agent run. You can name what an agent may observe and change, select the least powerful useful tool, define a stop condition, recognize when a subagent result is incomplete, and preserve human decision authority. You can prove this by producing a delegation brief, a permission decision, and an evidence-based recovery note.

## What experienced readers may skip

If you already operate repository agents, skim the definitions of tools and state. Do not skip **Action classes and permission boundaries**, **Subagents are scoped workers, not automatic independent authorities**, **Parallel work**, or the practice exercise. Those sections establish harness-specific expectations that may differ from a host product.

## On this page

- [Why this matters](#why-this-matters)
- [Observable learning objectives](#observable-learning-objectives)
- [Core concepts](#core-concepts)
- [The safe action loop](#the-safe-action-loop)
- [Action classes and permission boundaries](#action-classes-and-permission-boundaries)
- [State, memory, and durable artifacts](#state-memory-and-durable-artifacts)
- [Delegation and subagents](#delegation-and-subagents)
- [Parallel work and synthesis](#parallel-work-and-synthesis)
- [Important distinctions](#important-distinctions)
- [Worked examples](#worked-examples)
- [Harness connection](#harness-connection)
- [Role perspectives](#role-perspectives)
- [Practice exercise](#practice-exercise)
- [Check your understanding](#check-your-understanding)
- [Recovery guidance](#recovery-guidance)
- [Evidence of completion](#evidence-of-completion)

## Why this matters

A chat response is transient text. An agent may cross the boundary from text into action: reading private files, running tests, changing documentation, installing a dependency, sending a request, or deleting data. The same model can therefore have very different risk depending on its tools, permissions, working directory, input data, and approval policy.

The common failure is to treat “the agent” as one indivisible capability. In practice, risk is distributed across a system: the model proposes; the host exposes tools; the sandbox limits reach; repository instructions define local rules; a human grants or refuses approval; scripts perform deterministic operations; and validation supplies evidence. A safe workflow makes each part visible.

This visibility matters to beginners because fluent narration can hide an unverified action. It matters to experienced engineers because concurrency and broad permissions can turn a small reasoning error into a large state change. It matters to product, analysis, and quality roles because delegation must not silently transfer decisions they own. It matters to security reviewers because retrieved files can contain malicious instructions and because secrets may leave the local boundary through a model or tool.

## Observable learning objectives

By the end of this chapter, you:

- **Can explain** the difference between a model, tool, agent, workflow, and subagent without using the terms as synonyms.
- **Can explain** why a different role prompt does not by itself create an independent reviewer.
- **Can do** an action classification for read, write, reversible, destructive, and externally consequential operations.
- **Can do** a bounded delegation with explicit input scope, output schema, evidence expectations, timeout behavior, and stop conditions.
- **Can do** a least-privilege permission decision and state which human must authorize any expansion.
- **Can prove** what a worker inspected, what it did not inspect, what evidence supports its findings, and how an incomplete result was recovered.
- **Can prove** that a human-owned decision remained with the accountable human rather than being inferred from agent agreement.

## Core concepts

### Model

A model maps input into output according to learned statistical patterns and its current instructions. It can propose a command or summarize a file. By itself, it does not establish that the file exists, execute the command, or verify the result. Even when the output is confident and specific, treat it as generated content until supported by evidence.

### Tool

A tool is a callable capability exposed to an agent. Examples include searching files, reading a document, editing text, running a test command, browsing approved sources, or querying a connected service. Tools differ in scope and consequence. A file search is usually read-only. A patch changes local state. A release command changes shared external state. Tool output is evidence about that invocation, not automatic proof of the wider goal.

### Agent

An agent combines a model with instructions, context, tools, state, and an action loop. It can choose a next step based on observations and results. Its autonomy is bounded by the host, permissions, repository rules, task contract, and human gates. “Agent” does not mean unconstrained authority, reliable judgment, or legal accountability.

### Workflow

A workflow is an ordered or conditional process with inputs, steps, artifacts, gates, and completion rules. Some steps may be performed by agents and some by people or deterministic automation. A workflow can exist without an agent; for example, a fixed continuous-integration pipeline is a workflow. An agent can also act outside a formal workflow, although that makes boundaries harder to audit.

### Subagent

A subagent is a delegated worker operating under a parent task. It may have isolated context, a specialized question, and a narrower tool set. Its result returns to a parent for synthesis. “Sub” describes orchestration position, not lower intelligence and not independent authority. A subagent should know its scope, evidence standard, prohibited actions, stop condition, and output contract.

### Human checkpoint

A human checkpoint is a decision boundary owned by an accountable person. Examples include approving product scope, accepting residual security risk, authorizing a destructive command, or deciding whether evidence is sufficient for release. An agent can organize evidence and identify the owner. It cannot acquire the owner’s authority by producing a recommendation.

## The safe action loop

Use a visible loop: **observe, plan, act, inspect, update, stop, and hand off**. These are reasoning checkpoints, not a requirement to print hidden model reasoning.

### Observe

Establish current state before proposing a change. Read applicable repository instructions, inspect the working tree, locate the canonical artifact, and identify pre-existing failures. Observation should be targeted. Reading every available file can consume context, expose unnecessary sensitive information, and make relevant evidence harder to find.

A useful observation record states both coverage and omission: “Read `mkdocs.yml`, the Learn validator, and the three pages in the requested diff. Did not inspect deployment workflows because the task is read-only curriculum review.” That statement is more reliable than “reviewed the repository.”

### Plan

Select the smallest sequence that can produce the outcome and evidence. Mark human gates, risky operations, and dependencies. A plan is provisional: tool results may invalidate it. Planning is not permission. Listing “delete obsolete files” does not authorize deletion.

### Act

Call an allowed tool with the narrowest useful scope. Prefer a targeted file search over a full disk scan, a focused test over an unrelated test suite, and a patch limited to the authorized files over broad reformatting. Keep the working directory explicit when a command could otherwise affect the wrong repository.

### Inspect

Read the actual result. Check exit status, changed files, diagnostic output, and unexpected side effects. A zero exit status may still represent the wrong command, an empty test selection, or stale output. A nonzero status may be an environmental limitation rather than a product defect. Classify rather than guess.

### Update

Revise the plan, issue record, or task state based on observed evidence. If a test reveals an adjacent defect, record it and decide whether it is in scope. Do not silently expand into unrelated remediation. If context becomes stale after another actor changes the repository, observe again.

### Stop

Stop when completion evidence is satisfied, a declared stop condition occurs, or further action needs new authority. Examples include encountering credentials, detecting conflicting user changes, reaching a destructive migration, or finding that the required decision owner is absent. “I can probably infer the intent” is not a reason to cross the boundary.

### Hand off

Return an outcome-oriented record: changes or findings, evidence, untested areas, remaining risks, and the next accountable owner. A handoff should let another person reproduce the important checks without reconstructing the chat.

### Loop failure patterns

An agent may act before observing and overwrite a user change. It may plan once and ignore later evidence. It may inspect only stdout and miss changed files. It may continue after a stop condition because it is optimizing for apparent completion. The correction is to make the loop’s checkpoints part of the task contract and require durable evidence at the handoff.

## Action classes and permission boundaries

Action categories overlap. Classify both technical reversibility and organizational consequence.

| Action class | Example | Main question | Typical control |
| --- | --- | --- | --- |
| Read | Search tracked Markdown | Is the data in scope and safe to expose? | Limit paths and data classes |
| Local write | Edit one authorized lesson | Is the file owned by the task and are user changes preserved? | Patch and diff review |
| Reversible state change | Create a task branch | Is rollback reliable and free of shared impact? | Record before/after state |
| Destructive action | Remove unbacked local files | Could information be irrecoverable? | Explicit human approval and backup |
| External state change | Publish a release or send a message | Who is affected and who owns the decision? | Named owner approval and confirmation |
| Privileged action | Access secrets or bypass a sandbox | Is elevated access necessary and narrowly scoped? | Least privilege, reason, audit record |

“Reversible” does not mean “safe without approval.” Reverting a public message may not undo who saw it. Reverting a database migration may lose data written after the migration. Conversely, a read can be high risk if it retrieves credentials or sends confidential code to an external service.

### Least privilege

Least privilege means granting only the capability, path, duration, and data access necessary for the bounded task. If a reviewer needs to compare three Markdown files, it does not need a write tool. If a test needs network access only to download pinned dependencies, the approval should not imply permission to publish artifacts. If a command can run in a sandbox, do not request broader access merely for convenience.

### Sandboxing

A sandbox limits file-system, network, process, or service access. It reduces impact; it does not prove an action is correct. When a command fails because of a sandbox boundary, distinguish four possibilities: the task genuinely requires expanded access; an offline or local alternative exists; the requested action is outside scope; or the failure is unrelated to the sandbox. Escalation should include the exact command, reason, expected effect, and narrow reusable permission if appropriate.

### Approvals

An approval is contextual. Permission to run tests is not permission to install arbitrary software. Permission to edit documentation is not permission to commit or push. Permission previously granted for a prefix may be technically reusable while still inappropriate for the current task. The human instruction and task scope remain controlling.

For a high-impact action, the approval record should bind the decision to the exact **actor**, **tool**, **target**, and normalized parameters; its purpose and data class; an expiry or one-use boundary; and the accountable approver. Treat any material parameter, target, input, or revision change as a new request. Do not replay a stale approval merely because the interface still permits it. At execution time, compare the proposed action with the approved record and fail closed when the match, owner, or expiry is uncertain. Record the result separately: approval authorizes a bounded attempt, while observed output and side effects provide evidence about what happened. The [approval and sandbox reference](../reference/skills/ai-sdlc-approvals-sandbox.md) remains the canonical operational contract.

## State, memory, and durable artifacts

Agent systems can appear to “remember,” but several kinds of state are involved:

- **Conversation context** contains recent instructions and observations. It may be truncated, summarized, or unavailable in a new session.
- **Repository state** includes tracked and untracked files, branches, configuration, and generated artifacts. It persists beyond a chat but can be changed by other actors.
- **Workflow state** records lifecycle stage, blocked conditions, decisions, freshness, and handoffs in defined artifacts.
- **External state** includes issues, release records, cloud resources, mail, calendars, or deployment environments.
- **Model parameters** are not a project notebook and should not be treated as a place where a task’s decisions are durably stored.

Important decisions belong in repository-owned artifacts or another approved system of record. A chat statement such as “the product owner accepted the scope” is not durable acceptance unless the process names chat as the system of record and identifies the accountable person. State also has freshness. A test result collected before a code change may remain historically accurate but no longer support current completion.

## Mid-page recap

An agent is a model operating with tools, instructions, context, and state. Safe action uses an observable loop, least privilege, explicit action classes, and human checkpoints. Tool success is narrow evidence, not universal proof. Durable decisions belong in governed artifacts. You are now ready to delegate without assuming that delegation transfers responsibility.

## Delegation and subagents

Delegate when a bounded unit of work can be described more clearly and verified more cheaply than keeping it in the parent’s context. Good candidates are read-heavy inventory, a focused security review, an independent terminology scan, or comparison of a known artifact against explicit criteria. Poor candidates are ambiguous product decisions, a tiny lookup with high coordination overhead, or overlapping edits to the same files.

### The delegation contract

A useful delegation brief includes:

1. **Outcome:** the exact question the worker must answer.
2. **Input scope:** paths, diff, version, and repository state it may inspect.
3. **Excluded scope:** areas it must not infer or explore.
4. **Permissions:** read-only or named writes; network rules; prohibited external actions.
5. **Evidence:** path, heading, line, command, or output required for each finding.
6. **Output contract:** fields, classifications, severity scale, and concise completion format.
7. **Stop conditions:** missing file, unsafe data, contradiction, timeout, or required owner decision.
8. **Failure behavior:** return partial coverage and omissions rather than inventing completion.
9. **Deadline or timeout:** when orchestration should continue without the result.
10. **Handoff:** who synthesizes and who owns any resulting decision.

An output contract is especially important when several workers will be compared. Free-form reviews may use different meanings for “critical,” omit evidence, or bury questions inside recommendations.

### Isolated context

Context isolation can reduce anchoring: a reviewer who has not seen another reviewer’s conclusion is less likely to repeat it automatically. It can also omit necessary information. Independence therefore requires more than a different role label. Reviewers need separate execution contexts, the same artifact version, bounded questions, and no access to one another’s initial findings. If a host cannot provide isolated workers, label the result **simulated perspectives**, not independent subagent review.

A fresh subagent also lacks unwritten parent knowledge. Put required constraints in the delegation brief. Do not expect it to infer that “review this” means “do not edit,” “use the current diff,” or “report every source consulted.”

### When not to delegate

Do not delegate merely to create an impressive agent count. Avoid delegation when coordination cost exceeds the task, when the outcome depends on a conversation with the accountable owner, when isolation would hide essential context, or when writes cannot be partitioned safely. A parent should also avoid splitting one coupled judgment into fragments that no worker can evaluate end to end.

### Incomplete results

A useful incomplete result says what was inspected, what failed, and what remains unknown. The parent can retry with corrected context, reduce the task, choose another tool, inspect locally, or escalate. It should never silently convert “could not inspect the generated schema” into “no schema issues found.”

## Parallel work and synthesis

Parallel read-heavy work can reduce elapsed time and preserve independent perspectives. Examples include separate accessibility, security, and beginner-usability reviews of a frozen diff. All reviewers should receive the same artifact snapshot during one round. The parent should not edit midway and give later reviewers a newer target.

Parallel write-heavy work is riskier. Two agents can edit the same paragraph, regenerate the same catalog, or make individually reasonable but mutually conflicting architectural decisions. Partition writes by file only when semantic boundaries are also clear. Even then, the parent must integrate, validate cross-links, and inspect the combined diff. Shared file access means “different agents” does not necessarily mean isolated worktrees.

Synthesis is not concatenation and not majority voting. The parent deduplicates findings, preserves disagreements, distinguishes facts from proposals, checks evidence, selects corrections according to canonical repository authority, and routes decisions to humans. Three unsupported opinions do not outweigh one evidenced blocker.

## Important distinctions

### One agent simulating roles versus isolated reviewers

One agent can ask, “How might QA, product, and security view this?” That is a useful brainstorming technique, but all perspectives share one context and generation path. Isolated reviewers receive the same frozen artifact independently and do not see each other’s initial conclusions. Label the execution honestly so readers can judge the evidence.

### Several reviewers versus several editors

Reviewers can operate read-only and return findings to one editor. Editors mutate state. Concurrency that is safe for review may be unsafe for editing. The harness’s parent-owned edit pattern makes integration responsibility explicit.

### Agent output versus tool evidence

“The test passed” is an agent claim. The exact command, environment, exit status, and relevant output are evidence. Evidence can still be incomplete: the command may have selected zero tests. Verification connects the evidence to the acceptance criterion.

### Confidence versus authority

Confidence describes a reviewer’s certainty. Authority describes who may decide. A security reviewer can have high confidence that a secret is exposed, but the accountable owner still controls remediation priority and risk acceptance. An agent cannot increase its authority by reporting high confidence.

### Stop condition versus failure

Stopping at an approval boundary is correct behavior, not failure. A failed tool call may be recoverable without stopping. The task contract should distinguish both.

## Worked examples

### Worked example 1 — read-only terminology review

A documentation maintainer wants to know whether three pages use “approval,” “acceptance,” and “sign-off” consistently.

**Bounded delegation:**

> Compare `docs/foundations/responsibilities.md`, `docs/how-to/record-product-acceptance.md`, and the changed Learn page. Read only. Report one row per inconsistent term with file, heading, quoted label of no more than five words, competing interpretation, learner impact, confidence, and proposed owner. Do not edit. Stop if any file is missing. State inspected and omitted scope.

The subagent reports two evidence-backed inconsistencies and one question. It does not declare which policy is correct. The parent checks the glossary and canonical responsibility page, applies one correction, and records that product acceptance remains a product-owner decision.

**Why it works:** the artifact scope is small, read-only access is sufficient, the output is comparable, missing input has a stop rule, and the parent owns integration.

### Worked example 2 — recovering an incomplete test review

A developer delegates: “Review tests for the new parser.” The worker finds unit tests and says coverage looks good, but its report does not mention malformed input or integration tests.

The parent does not accept the conclusion. It compares the report with the contract and marks the result incomplete. The retry brief names the parser files, acceptance criteria, negative cases, and required evidence fields. It asks for read-only inspection of unit and integration tests and requires `covered`, `not_covered`, or `blocked` for each criterion. The second result identifies missing malformed UTF-8 coverage. A test owner decides whether it blocks the change.

**Why it works:** recovery corrects the contract rather than blaming the worker, preserves the first report as partial evidence, and routes the completion decision to the owner.

### Weak example — unbounded parallel editing

> Ask five agents to improve all documentation. Let each fix anything it notices. Merge whichever version looks best.

This request has no shared snapshot, ownership partition, canonical authority, evidence schema, stop conditions, or integration plan. Agents may overwrite user work, duplicate concepts, and make incompatible navigation changes. “Looks best” is not an acceptance test.

### Corrected example — independent review and parent-owned correction

> Freeze the current documentation diff. Give five isolated reviewers the same paths and acceptance criteria. Keep them read-only. Assign beginner usability, product boundaries, testability, security, and maintainability questions. Require evidence, confidence, classification, and omissions. After every report returns, the parent groups agreements, conflicts, and unique findings, checks canonical pages, applies accepted edits, and reruns validation. Human owners decide product scope, risk acceptance, and publication.

The corrected request uses parallelism for independent observation while preserving one edit owner and explicit human gates.

## Harness connection

The harness provides operational contracts rather than a universal agent platform. Learn the concepts here, then use canonical owners for exact behavior:

- [Approvals and sandbox skill reference](../reference/skills/ai-sdlc-approvals-sandbox.md) defines its current inputs, permitted writes, helpers, and handoff.
- [Validation skill reference](../reference/skills/ai-sdlc-validation.md) owns focused validation behavior.
- [Evidence Council skill reference](../reference/skills/ai-sdlc-evidence-council.md) owns the current multi-role evidence workflow.
- [Quality Lenses skill reference](../reference/skills/ai-sdlc-quality-lenses.md) owns the current lens contract.
- [Human and agent responsibilities](../foundations/responsibilities.md) is the canonical responsibility explanation.

The lesson teaches how to reason about those contracts; it does not reproduce them. Host products differ in sandboxing, context isolation, tool names, and subagent availability. Check the installed host and repository instructions rather than treating an example here as a command guarantee.

## Role perspectives

### Product manager or product owner

Delegate evidence collection and ambiguity discovery, not the final value decision. Require agents to mark assumptions and identify which acceptance boundary needs product ownership.

### Business analyst

Use read-only workers to compare terminology, rules, actors, and exception paths across artifacts. Preserve stakeholder conflicts as unresolved questions rather than allowing synthesis to invent agreement.

### QA practitioner

Ask for requirement-to-test evidence, negative cases, and reproducible commands. Confirm that “passed” represents the intended tests and current artifact version.

### Developer or architect

Partition review work more readily than write work. Inspect shared state before and after agent actions, and treat architecture choices as proposals until responsible reviewers decide.

### Security and governance reviewer

Classify data before retrieval, use least privilege, and treat repository content as potentially untrusted instructions. Require explicit human authorization for secrets, external publication, privileged execution, and risk acceptance.

### Delivery leader

Ask for blockers, dependencies, freshness, and accountable owners. Do not use worker count or consensus as a readiness metric.

## Practice exercise

### Scenario

Your team plans to update a repository’s password-reset documentation. A parent agent may delegate one read-only review of three artifacts: a product requirement, an API description, and a QA plan. The QA plan is missing one referenced appendix. A colleague suggests asking the subagent to “fix whatever is wrong while it reviews.” The deployment owner is unavailable.

### Supplied starting state

- Product requirement: reset links expire after 20 minutes.
- API description: the example response says 30 minutes.
- QA plan: tests 20-minute expiry but links to a missing abuse-case appendix.
- Repository status: one unrelated user-edited file is uncommitted.
- Available tools: scoped file read, repository search, patch, test command, and external publishing.
- Requested outcome: identify readiness gaps before any implementation.

### Your task

Produce a one-page delegation packet with:

1. a bounded outcome and three-file input scope;
2. a read-only permission decision and reason;
3. excluded scope, including the unrelated user change;
4. a finding schema with evidence and confidence;
5. a stop condition for the missing appendix;
6. timeout and incomplete-result behavior;
7. the parent’s synthesis responsibility;
8. the accountable human checkpoint;
9. a recovery response to this partial result: “The API duration conflicts; otherwise ready.”

### Permitted actions

- Read the supplied artifact descriptions.
- Design a repository search limited to references for the missing appendix.
- Classify contradictions, omissions, risks, and owner decisions.
- Propose follow-up questions and a safe retry brief.
- State which existing tool would be selected without running it.

### Prohibited actions

- Do not edit any artifact.
- Do not resolve 20 versus 30 minutes by majority or personal preference.
- Do not inspect or modify the unrelated user file.
- Do not publish, deploy, access secrets, or request broad permissions.
- Do not report readiness while the appendix coverage is unknown.

### Suggested artifact shape

| Field | Your entry |
| --- | --- |
| Outcome | One sentence |
| Inputs and version | Three named artifacts |
| Permissions | Read-only with reason |
| Required finding fields | Evidence, impact, classification, confidence, owner |
| Stop conditions | Missing input and human decision |
| Incomplete-result response | Coverage and omissions |
| Human checkpoint | Named role and decision |
| Completion evidence | What proves the review happened |

### Verification procedure

Check that the packet cannot be interpreted as permission to edit. Confirm that every conclusion requires a path or artifact heading. Confirm that the duration conflict remains open for its product owner. Confirm that the missing appendix produces a blocker or explicit omission rather than an invented clean result. Confirm that the unrelated change is excluded.

### Failure and recovery

If your packet says “review everything,” reduce the scope to the three artifacts. If it grants patch access, remove it because the outcome is review. If the subagent returns a partial result without omissions, mark it incomplete, retain the evidenced conflict, and retry only the missing coverage. If the appendix cannot be found, hand off a blocker to the QA owner; do not create its expected content from assumptions.

## Check your understanding

### 1. A subagent uses a security-review role prompt in the same conversation context as the parent. Is the review independent?

<details>
<summary>Answer: role prompt versus independent review</summary>

No. The role framing may produce another perspective, but the work shares context and a generation path. Label it simulated. Independent review needs isolated execution, the same frozen artifact, bounded questions, and no exposure to other initial findings.

</details>

### 2. A sandboxed command can only modify the requested repository. Does that prove it is safe to run?

<details>
<summary>Answer: sandbox reach versus action safety</summary>

No. The sandbox limits reach, but the command might still delete requested files, overwrite user work, or implement the wrong outcome. Scope, reversibility, approval, and inspection remain necessary.

</details>

### 3. Three read-only reviewers recommend release, while the accountable release owner has not reviewed the evidence. Is release approved?

<details>
<summary>Answer: recommendation versus release approval</summary>

No. Reviewer agreement is evidence and advice, not transferred authority. The release owner must make and record the decision under the applicable process.

</details>

### 4. What should a worker return when a required file is missing?

<details>
<summary>Answer: missing-file partial result</summary>

It should stop or return a defined partial result: inspected scope, missing file, effect on conclusions, safe attempts made, and the owner or input needed. It must not reinterpret missing evidence as absence of issues.

</details>

### 5. Why is parallel review usually safer than parallel editing?

<details>
<summary>Answer: parallel review versus editing</summary>

Read-only reviewers do not compete to mutate shared state, and a parent can synthesize their reports. Concurrent editors may overwrite one another or create semantic contradictions even when they touch different files. Parallel editing needs stronger partitioning and integration controls.

</details>

## Common failure modes

- **Tool anthropomorphism:** describing the agent as if it personally holds authority. Correct by naming tools, boundaries, and decision owners.
- **Read-only means harmless:** ignoring data exposure or prompt injection in files. Correct by classifying inputs and limiting retrieval.
- **Approval drift:** reusing a prior permission outside its purpose. Correct by checking current task scope and consequence.
- **Missing working directory:** running a valid command in the wrong repository. Correct by making location part of observation and command evidence.
- **Narrated validation:** accepting “tests pass” without command output and selection. Correct by recording reproducible evidence.
- **Role-label independence:** presenting simulated perspectives as isolated reviews. Correct the execution label.
- **Parallel write collision:** allowing several agents to edit shared concepts. Freeze writes, assign one parent editor, and revalidate.
- **Silent partial result:** treating omitted files as clean. Record coverage and blockers.
- **Authority by consensus:** converting repeated recommendations into approval. Route the decision to its owner.
- **No stop rule:** continuing through secrets, conflicting user changes, or destructive actions. Define boundaries before action.

## Recovery guidance

When an agent run goes wrong, preserve evidence before attempting a fix. Record the initial state if known, command or tool invocation, changed paths, output, and current status. Stop additional writers. Determine whether the action was read-only, reversible, destructive, or externally consequential.

For a local reversible change, inspect the diff and use the repository’s approved recovery process; do not discard unrelated user work. For an incomplete review, preserve valid findings and rerun only missing scope with a clearer contract. For a permission error, test whether an in-scope sandboxed alternative exists before escalating. For possible secret exposure, stop, notify the accountable security owner, rotate or revoke according to policy, and avoid repeating the secret in reports. For an external action, contact the system owner because local rollback may not reverse impact.

After recovery, improve the system: add a stop condition, narrow a tool permission, update repository instructions, create a deterministic check, or revise the delegation schema. The goal is not to hide the failure; it is to make recurrence less likely and evidence more useful.

## Evidence of completion

You have completed this chapter when you can provide:

- your password-reset delegation packet;
- an action classification for every available tool;
- a written reason for read-only access and least privilege;
- a stop condition for the missing appendix;
- a corrected response to the incomplete worker report;
- a named human owner for the duration decision;
- a short statement distinguishing simulated and independent review;
- a reproducible verification checklist showing that no write was authorized.

Completion evidence shows learning; it does not grant repository write access, product approval, security risk acceptance, or release authority.

## Completion checklist

- [ ] I can distinguish a model, tool, agent, workflow, and subagent.
- [ ] I can describe the observe–plan–act–inspect–update–stop–handoff loop.
- [ ] I classify reads for data risk and writes for state risk.
- [ ] I treat reversibility and external consequence separately.
- [ ] I request only the least privilege needed for the outcome.
- [ ] My delegation names scope, exclusions, evidence, output, timeout, and stop conditions.
- [ ] I label simulated perspectives honestly.
- [ ] I know why several reviewers should not edit concurrently by default.
- [ ] I preserve partial results and omissions during recovery.
- [ ] I keep accountable human decisions with their owners.

## Previous learning step

Return to [Context, verification, and evidence](context-and-verification.md) if you cannot yet distinguish instructions from evidence or assess source quality.

## Next learning step

Continue to [Independent multi-role review](multi-role-review.md) to apply bounded, read-only subagents to a shared artifact without turning consensus into approval.

## Sources and adaptation notes

- **HARNESS-DOCS** — [AI SDLC Harness documentation and repository contracts](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/faccb4354464a1a3cc309b7b2dfa65e8efaf3529/docs). Owner: AI SDLC Harness maintainers; revision: `faccb4354464a1a3cc309b7b2dfa65e8efaf3529`; reuse: `internal-authority`; mode: `synthesized`. Informed: responsibility and recovery. Transformed: original action-loop cases teach the model. Limitation: linked pages own operations.
- **HARNESS-SKILLS** — [AI SDLC Harness skill contracts and deterministic helpers](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/faccb4354464a1a3cc309b7b2dfa65e8efaf3529/skills). Owner: AI SDLC Harness maintainers; revision: `faccb4354464a1a3cc309b7b2dfa65e8efaf3529`; reuse: `internal-authority`; mode: `synthesized`. Informed: approvals and delegation. Transformed: contracts became decisions. Limitation: exact skill instructions were excluded.
- **MS-AGENTS-BEGINNERS** — [AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners). Owner: Microsoft; revision: `b7f34fd824767162f484e03cc500e23c0966372f`; reuse: `adaptable-with-verification`; mode: `adapted`. Informed: components before orchestration. Transformed: an original harness loop and delegation lab replace source lessons. Limitation: structure, code, examples, and media were excluded.
- **NIST-GENAI-PROFILE** — [Artificial Intelligence Risk Management Framework Generative Artificial Intelligence Profile](https://doi.org/10.6028/NIST.AI.600-1). Owner: National Institute of Standards and Technology; revision: `NIST-AI-600-1-2024`; reuse: `reference-only`; mode: `reference`. Informed: provenance and oversight. Transformed: topics became original stop-condition cases. Limitation: no profile text or conformance claim was used.
- **OWASP-LLM-SECURITY** — [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html). Owner: OWASP Foundation Cheat Sheet Series; revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. Informed: injection and least privilege. Transformed: original permission decisions teach the risks. Limitation: no checklist, attack text, or code was adapted.
- **OPENAI-CODEX-DOCS** — [Official Codex behavior documentation set](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Owner: OpenAI; revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. Informed: [subagent](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [security](https://learn.chatgpt.com/docs/security) behavior. Transformed: host variability became explicit. Limitation: no vendor prose or promise was reused.
- **W3C-WAI** — [W3C Web Accessibility Initiative tutorials and guidance](https://www.w3.org/WAI/tutorials/). Owner: World Wide Web Consortium; revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. Informed: headings, links, and tables. Transformed: presentation was checked. Limitation: no tutorial or media was reproduced.
