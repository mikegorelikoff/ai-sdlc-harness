---
title: "Learn the AI SDLC Harness from the foundations"
description: "Choose a starting point and progress from basic generative AI concepts to accountable use of the harness in a real repository."
learning_level: 0
audience:
  - beginner
  - product
  - analysis
  - quality
  - engineering
  - leadership
  - governance
estimated_time: "45–75 minutes for orientation; 12–20 hours for the full path"
prerequisites:
  - "None"
content_type: "learning_hub"
last_reviewed: "2026-07-21"
source_usage:
  - source_id: HARNESS-DOCS
    mode: synthesized
  - source_id: MS-GENAI-BEGINNERS
    mode: reference
  - source_id: MS-AI-BEGINNERS
    mode: reference
  - source_id: GOOGLE-TECH-WRITING
    mode: reference
  - source_id: DIATAXIS
    mode: reference
---

# Learn the AI SDLC Harness from the foundations

This learning path takes you from “I have used a chat interface” to “I can use
the harness safely in a real repository and prove what happened.” You do not
need prior knowledge of artificial intelligence (AI), software development, or
agents. Experienced readers can enter later, but everyone uses the same
evidence and human-authority rules.

The curriculum teaches ideas before commands. It starts with models and
generated output, then builds prompting, context, verification, tool use,
delegation, software delivery, specification-driven development (SDD), harness
operation, guided practice, and role-specific application. The endpoint is not
autonomous approval. It is accountable independent use: you can choose a
bounded workflow, inspect its artifacts, verify claims, and hand a decision to
the correct human owner.

## At a glance

**Level:** Learning hub and starting-level diagnostic<br>
**Audience:** Anyone learning, evaluating, teaching, or maintaining the harness<br>
**Estimated time:** 45–75 minutes for this hub; 12–20 hours for the full path<br>
**Prerequisites:** None

## Expected outcome

After this orientation, you can choose a justified starting level, describe
what evidence will show progress, and name the human decision that remains
outside the curriculum. You will also know where to find exact operational
commands without confusing a lesson with a reference contract.

## What experienced readers may skip

If you can already explain tokens, probabilistic output, prompt injection,
least privilege, and the difference between an agent and a workflow, take the
diagnostic before skipping Level 0. If you already use coding agents with
repository instructions and test evidence, begin at Level 2A. If the harness is
already installed and you can verify its inventory, begin at Level 4, then use
Level 5 to test your mental model. Do not skip a level because its title sounds
familiar; skip only when you can produce the stated evidence.

## Why this matters

An AI tool can produce fluent text before a learner knows what should be
checked. That creates a dangerous illusion of progress. A generated plan may
look orderly while omitting a security constraint. A code diff may compile
while implementing the wrong outcome. Seven reviewers may agree while none of
them owns the product decision. Installation may appear successful while the
skills were placed in a different host scope.

The curriculum therefore separates three competencies:

- **Can explain** means you can distinguish concepts in your own words.
- **Can do** means you can perform a bounded action under stated permissions.
- **Can prove** means you can present observable evidence and identify who has
  authority to accept it.

These competencies prevent two common mistakes. The first is memorizing terms
without being able to operate. The second is operating without being able to
show what changed, what was checked, or which decision remains human-owned.

## Observable learning objectives

By the end of this hub:

- **Can explain:** describe the twelve-step learning journey and the difference
  between Learn, Reference, Use, and Adopt.
- **Can do:** select a starting level from evidence rather than confidence.
- **Can prove:** save a short learning plan with completed diagnostic items,
  chosen next page, and an explicit authority boundary.

## On this page

- [The curriculum map](#the-curriculum-map)
- [Choose your starting level](#choose-your-starting-level)
- [Fast lanes](#fast-lanes)
- [How to study long chapters](#how-to-study-long-chapters)
- [Worked examples](#worked-examples)
- [Practice exercise](#practice-exercise)
- [Check your understanding](#check-your-understanding)
- [Recovery guidance](#recovery-guidance)
- [Evidence of completion](#evidence-of-completion)

## Core concepts

### Learning is an evidence-producing workflow

Reading is an input, not completion. Each chapter asks you to create something:
a task contract, context inventory, evidence table, delegation brief,
multi-role review report, trace map, navigator request, lab artifact, or role
handoff. Your artifact is then checked against visible criteria. This mirrors
the harness: a claim is stronger when it has a durable artifact and current
validation evidence.

A learner may say, “I finished the agents chapter.” A better completion claim
is, “I wrote a read-only delegation with a file boundary, output schema, stop
condition, and recovery action; another person can inspect it in my learning
notes.” The second claim is observable. It can still be wrong, but it can be
reviewed.

### Lessons do not grant authority

Completing a chapter, passing a knowledge check, or receiving agreement from
reviewer agents does **not** grant approval authority. Product owners still own
product acceptance where the organization assigns it. Security owners still
decide whether a risk is accepted. Repository maintainers still decide whether
a documentation change is published. Release owners still authorize release.

The harness helps prepare evidence and make ownership visible. It does not
transfer accountability to the model, the learner, or a review council.

### Documentation types answer different needs

This site uses four operational documentation types alongside Learn:

- **Learn** develops competence in prerequisite order. It explains, demonstrates,
  provides practice, and checks evidence.
- **Reference** is the canonical place to look up exact skill contracts,
  schemas, roles, versions, and terminology while working.
- **Use** contains tutorials, workflow journeys, and how-to instructions for a
  concrete task.
- **Adopt** supports organizational pilots, operating models, governance,
  measurement, rollout, and support.

About contains deeper explanations, foundations, audits, roadmap material, and
maintainer policy. If a lesson and a skill reference ever appear to disagree
about current skill behavior, the skill and its generated reference are the
operational authority. Report the lesson as stale.

## The curriculum map

The following table is a learning map, not a process mandate. The “proof”
column names the minimum artifact that allows you to move forward.

| Level | Focus | You can do after the level | Minimum proof |
| --- | --- | --- | --- |
| 0 | AI foundations | Classify model output, tool use, risk, and human checkpoints | Risk-and-evidence classification sheet |
| 1A | Prompt engineering | Turn a vague request into a bounded task contract | Outcome–Constraints–Context–Acceptance and evidence–Output contract |
| 1B | Context and verification | Select authoritative context and design checks | Source and omission inventory with evidence table |
| 2A | Agents, tools, and subagents | Delegate one safe read-only task | Delegation brief with permissions and stop condition |
| 2B | Multi-role review | Run independent role reviews without voting approval | Structured findings and accountable-owner synthesis |
| 3 | AI SDLC and SDD | Trace intent through artifacts and evidence | Request-to-handoff trace map |
| 4 | Harness essentials | Choose a flow and formulate a navigator request | Flow decision and expected-artifact record |
| 5 | Guided practice | Recover from realistic failures in a safe workspace | Completed lab portfolio with verification outcomes |
| 6 | Role learning paths | Apply the harness from your role without taking another owner’s authority | Role-specific first-task handoff |

The direct chapter sequence is:

1. [AI foundations](learn/ai-foundations.md)
2. [Prompt engineering](learn/prompt-engineering.md)
3. [Context and verification](learn/context-and-verification.md)
4. [Agents, tools, and subagents](learn/agents-tools-and-subagents.md)
5. [Independent multi-role review](learn/multi-role-review.md)
6. [AI SDLC and specification-driven development](learn/ai-sdlc-and-sdd.md)
7. [Harness essentials](learn/harness-essentials.md)
8. [Guided practice](learn/guided-practice.md)
9. [Role learning paths](learn/role-learning-paths.md)

### Level 0 outcome: judge generated output before acting

You begin by separating a computational model from a chat interface, tool,
agent, and workflow. You learn why a probable next token is not a verified
fact, why deterministic commands and probabilistic generation behave
differently, and why confidential data and untrusted content need explicit
boundaries. The outcome is not a mathematical account of model training. It is
the ability to stop fluent output from bypassing judgment.

Move on when you can classify a sample as generated output or evidence,
identify a missing check, mark a required human decision, and explain when an
autonomous action is inappropriate.

### Level 1A outcome: define bounded work

Prompt engineering here means task definition, not secret wording. You use the
harness task contract: Outcome, Constraints, Context, Acceptance and evidence,
and Output. You practice with product, analysis, QA, development, security, and
delivery examples. You learn to expose assumptions and exclusions rather than
hiding them inside a role-playing persona.

Move on when another person can read your task contract and identify what must
be true, what must not change, which information matters, how success will be
tested, and what artifact should be returned.

### Level 1B outcome: curate context and design verification

Context engineering asks which information the system should receive, why it
is authoritative, whether it is current, what is missing, and which content is
untrusted. You compare too little, too much, irrelevant, stale, contradictory,
and malicious context. Verification becomes a designed part of the task rather
than an afterthought.

Move on when you can accept and reject sources with reasons, record omissions,
define negative and regression checks, and produce an evidence table that does
not treat generated prose as proof.

### Level 2A outcome: delegate within permissions

An agent can observe, plan, act through tools, inspect results, update its plan,
stop, and hand off. A subagent receives a bounded task and separate working
context, but it is not independent merely because its prompt names another
role. You learn the difference between read and write actions, reversible and
destructive actions, repository state and chat state, and safe parallel work
versus conflicting concurrent edits.

Move on when you can delegate one read-only question with an input boundary,
output schema, timeout, stop condition, and recovery path, then assess an
incomplete result without silently inventing the missing evidence.

### Level 2B outcome: synthesize disagreement without voting

Different roles notice different defects. Independent execution can reveal
more than one agent simulating several roles, but more reviewers do not create
approval. You learn identical artifact scope, bounded questions, evidence,
severity, confidence, facts versus proposals, accountable owners, and
follow-up after correction.

Move on when you can preserve conflicts and unresolved questions in a
structured report, assign the next decision to the correct human owner, and
explain why six matching opinions can still be wrong.

### Level 3 outcome: trace delivery intent

The software development lifecycle (SDLC) connects discovery, requirements,
design, implementation, testing, release, and maintenance. AI changes who can
produce drafts and how quickly, not the need for accountable outcomes and
evidence. Specification-driven development turns an accepted request into
linked requirements, design boundaries, tests, QA scope, tasks, implementation,
and validation evidence.

Move on when you can trace one outcome through this chain and find a gap such
as code without an accepted requirement, a test without an acceptance link, or
an old artifact that no longer matches implementation.

### Level 4 outcome: operate the harness mental model

You learn the three environments: source checkout, installed agent environment,
and consumer repository. You distinguish skills, helpers, Markdown artifacts,
Token-Oriented Object Notation (TOON), state, policies, agents, and humans. You
classify requests, select quick, full, or lifecycle flow, use the navigator,
read targeted context, identify blockers, and name the next artifact and human
gate.

Move on when your flow choice is tied to risk and evidence rather than task
size alone, and when your navigator request asks for a recommendation rather
than pretending to know the workflow.

### Level 5 outcome: recover, not just succeed

Guided practice includes a first prompt, context selection, evidence design,
read-only delegation, multi-role review, first harness session, first feature,
existing-project adoption, full lifecycle, stale evidence, conflicting
artifacts, and human escalation. Some labs deliberately contain misleading
context or apparent reviewer consensus.

Move on when you can show both successful evidence and a recovery record. A
perfect first attempt is not required. A hidden failure is unacceptable.

### Level 6 outcome: work from a role without role overreach

Product, analysis, QA, engineering, architecture, security, delivery,
AI-practice, and maintainer roles enter at different tasks. Role labels help
discover skills; they do not grant permissions. Each path identifies upstream
inputs, owned decisions, contributions, reviews, prohibited approval claims,
skill sequence, first exercise, evidence, and downstream handoff.

Move from guided learning to independent use when you can take one real,
bounded repository request through the appropriate artifacts and return a
traceable handoff to its accountable owner.

## Mid-page recap

The path is cumulative. Prompt quality cannot repair missing evidence. More
context cannot repair untrusted authority. A subagent role name cannot create
independence. Reviewer consensus cannot create approval. Code cannot prove it
implements the intended outcome without traceability. The harness makes these
boundaries visible, but a human still evaluates the evidence and owns the
decision.

Your next step is therefore determined by proof, not seniority. Use the
diagnostic that follows.

## Choose your starting level

For each statement, record three separate states in your learning notes:

- **Explain — yes/no:** I can accurately explain this without notes.
- **Demonstrate — yes/no:** I can create the artifact or perform the action safely.
- **Prove — yes/no:** I can show current evidence and name the accountable owner.

The visible checkbox beside each statement means **all three states are yes**. If
one state is no, leave the checkbox empty and record the missing state. Do not
mark an item based on recognition. If you cannot demonstrate and prove the
item, start at or before that level.

### Foundation diagnostic

- [ ] I can distinguish a model, chat interface, tool, agent, workflow, and
  subagent using one software-delivery example.
- [ ] I can explain why fluent generated text is not evidence.
- [ ] I can identify sensitive information and indirect prompt injection in a
  document or repository file.
- [ ] I can distinguish deterministic command output from probabilistic model
  output.
- [ ] I can identify an action that requires human escalation.

If any box is unchecked, begin with [AI foundations](learn/ai-foundations.md).

### Prompt and context diagnostic

- [ ] I can turn “add login” into a bounded outcome without inventing product
  policy.
- [ ] I can state constraints, exclusions, required output, and observable
  acceptance evidence.
- [ ] I can identify minimum sufficient context and reject irrelevant context.
- [ ] I can distinguish an instruction from evidence inside the same file.
- [ ] I can handle stale or conflicting sources without choosing silently.

If prompt items are weak, begin with
[Prompt engineering](learn/prompt-engineering.md). If source and evidence items
are weak, continue through
[Context and verification](learn/context-and-verification.md).

### Agent and review diagnostic

- [ ] I can classify a proposed tool action as read-only, write, reversible, or
  destructive.
- [ ] I can write a delegation with scope, output, stop condition, and recovery.
- [ ] I can explain why a new role prompt is not independent review.
- [ ] I can combine review findings without majority voting.
- [ ] I can preserve a disagreement and assign it to an accountable human.

If any box is unchecked, begin with
[Agents, tools, and subagents](learn/agents-tools-and-subagents.md) and complete
[Multi-role review](learn/multi-role-review.md).

### Delivery and harness diagnostic

- [ ] I can trace request, outcome, requirement, design, test, task,
  implementation, evidence, review, and handoff.
- [ ] I can explain this repository’s meaning of AI SDLC and SDD.
- [ ] I can distinguish source checkout, installed skills, and consumer
  repository.
- [ ] I can choose quick flow, full flow, or full lifecycle and state why.
- [ ] I can formulate a navigator request and predict the next artifact without
  treating that prediction as fact.

If the trace is weak, begin with [AI SDLC and SDD](learn/ai-sdlc-and-sdd.md). If
only harness operation is weak, begin with
[Harness essentials](learn/harness-essentials.md).

## Fast lanes

### Beginner path

Complete every chapter in navigation order. Keep one file named, for example,
`learning-evidence.md` in a disposable practice repository. Add the artifact,
verification result, unanswered questions, and authority boundary after each
chapter. Use the glossary whenever a term is unfamiliar. Do not install or run
an agent tool until the exercise explicitly permits it.

### Experienced AI user fast lane

Complete the Level 0 risk classification and the Level 1B malicious-context
exercise. If both pass, read the Level 1A task-contract comparison and save an
equivalent bounded task artifact, then begin at
Level 2A. Experienced chat use often creates confidence with generation but
does not necessarily provide tool-permission, repository-state, or evidence
discipline.

### Installed-harness-user fast lane

Verify the installed skill inventory and current repository instructions using
the canonical [installation guide](how-to/install.md). Then complete the Level
0 authority check, the Level 1 evidence exercise, the Level 4 flow-selection
exercise, and all Level 5 recovery labs. Installation proves
files were placed; it does not prove the learner can choose or validate a
workflow.

### Role-based fast lane

Pass the Level 0 evidence and authority diagnostic, produce a Level 1A bounded
task contract, complete Level 1B’s context/evidence exercise, and demonstrate
Level 2A read-only delegation before using Level 2B’s review model. Equivalent
work evidence may replace a lab only when it satisfies the same completion
criteria and is recorded in the learning plan. Then open
[Role learning paths](learn/role-learning-paths.md) and follow the shared
prerequisites for your role. Use the canonical
[skills-by-role reference](reference/skills-by-role.md) for current skill
discovery. A role path is a learning recommendation, not a permission grant.

## Important distinctions

### Curriculum order versus delivery workflow

The Learn order is how concepts are taught. It is not the order in which every
real feature runs. A small defect may use a compact implementation flow. A new
regulated workflow may require extended discovery, requirements readiness,
security work, QA strategy, and delivery handoff. Level 4 teaches how to choose.

### Completion evidence versus acceptance

Completion evidence shows that an exercise or automated check met stated
criteria. Acceptance is a decision by an accountable owner who may consider
evidence, risk, policy, and business context. Evidence can be complete while
acceptance is denied. Reviewer agreement can be strong while authority is
absent.

### Repository truth versus chat history

Chat history can help continuity but is not a durable source of repository
state. A file, Git diff, test result, generated artifact, or signed decision may
be inspectable later. Even durable artifacts can become stale. The curriculum
therefore asks for paths, commands, dates, and freshness, not “the agent said it
was done.”

### Skill reference versus lesson summary

A skill reference states the current input, output, constraints, and failure
behavior. A lesson explains why and when a learner might use it. If the skill
changes, the reference and tests should change first; the lesson must then be
reviewed for stale teaching.

## Worked examples

### Worked example 1: a complete beginner chooses Level 0

Mara has used a chat assistant to draft meeting summaries. She can describe a
prompt as “the question I type,” but she cannot explain a tool call, context
window, prompt injection, or why a cited file might still be stale. She is a
senior product manager, yet her AI-delivery evidence is beginner-level.

Mara marks the foundation diagnostic honestly. She starts at Level 0, not the
product role path. Her first completion artifact classifies a generated release
note as output, a test log as partial evidence, and release approval as a human
decision. After Levels 0, 1A, 1B, and 2B, she enters the PM or PO role path. Her
job title influenced examples, not prerequisites.

### Worked example 2: an experienced developer chooses Level 2A

Ilya routinely uses a coding assistant. He can produce bounded prompts and
checks diffs and tests. During the diagnostic, however, he describes a subagent
as “another persona” and suggests parallel agents can edit different parts of
the same module without an explicit ownership plan.

Ilya does not repeat all prompt material. He reads the Level 1B injection and
source-conflict sections, then starts Level 2A. His evidence is a read-only
delegation for examining API error handling. It names three files, prohibits
writes and network access, requires line evidence, and stops if the API contract
is missing. He then completes multi-role review before entering Level 3.

### Weak example: starting from confidence

> I use AI every day, so I will skip to the full lifecycle tutorial.

This is weak because frequency is not proof of the required competencies. It
does not show tool permissions, verification, artifact traceability, or human
authority. The learner may copy commands without recognizing a stale state or
unsafe scope.

### Corrected example: starting from observable evidence

> I passed the foundation and prompt diagnostics with written examples. I could
> not produce a safe delegation or explain isolated review, so I will begin at
> Level 2A. I will move on when my delegation artifact includes scope,
> permissions, output schema, stop condition, and recovery, and a human reviewer
> confirms those fields are present.

The corrected version does not claim mastery. It names the gap, next page,
artifact, check, and human checkpoint.

## Harness connection

The curriculum’s evidence model matches the harness operating model:

1. observe the request and repository;
2. choose the smallest relevant workflow;
3. create or update durable artifacts;
4. validate with focused checks;
5. review findings and uncertainty;
6. stop at blockers or human gates;
7. hand off a traceable result.

The [workflow map](reference/workflow-map.md) is the canonical cross-reference.
The [navigator how-to](how-to/navigate-request.md) owns exact operational
guidance. The [glossary](foundations/glossary.md) owns terminology. Learn uses
those owners; it does not replace them.

## Role perspectives

- A **PM or PO** uses the path to distinguish outcome definition from generated
  implementation detail and retain product acceptance.
- A **business analyst** learns to expose ambiguity, rules, exceptions, and
  trace links before code is treated as progress.
- **QA** turns acceptance language into observable positive, negative,
  integration, and regression evidence.
- A **developer or architect** learns bounded agent use, repository state,
  feasibility evidence, and recovery from incorrect generation.
- A **security reviewer** identifies untrusted context, permissions, secrets,
  supply-chain boundaries, and human gates.
- A **delivery leader** uses artifacts and freshness to assess readiness without
  counting generated documents as outcomes.
- A **Head of AI Practice** governs tools, learning evidence, evaluation, and
  exception handling.
- A **harness maintainer** protects canonical ownership, compatibility,
  validation, provenance, and curriculum quality.

## How to study long chapters

Each chapter is intentionally substantial. Use it as a workbook, not a wall of
text.

1. Read **At a glance**, objectives, and the table of contents.
2. Mark unfamiliar terms and use the glossary before proceeding.
3. Read one concept and its adjacent example together.
4. Write the practice artifact in a disposable or approved repository.
5. Attempt the knowledge check before opening answers.
6. Compare evidence with criteria; do not grade by confidence.
7. Use Recovery guidance when a check fails.
8. Record the completion checklist and next step.

Stop if required context is missing. Do not fill a missing repository rule with
a generic best practice. Record the omission, inspect canonical files, and ask
the responsible person only when inspection cannot resolve it.

## Practice exercise

Create a learning-start record. A Markdown table or plain text file is enough.
Do not run harness skills yet.

### Scenario

You have been asked to “use the AI SDLC harness for the next feature.” You know
your job role and have access to this site, but you have not demonstrated the
curriculum competencies.

### Supplied starting state

- The repository and documentation are readable.
- No installation or write permission is assumed.
- The feature request and organization approval policy are not supplied.
- Your confidence level is not evidence.

### Exact learner task

1. Complete all four diagnostic groups.
2. For each unchecked item, write one sentence describing missing evidence.
3. Choose the earliest level with a material gap.
4. Link the exact next page.
5. State what artifact will prove that level complete.
6. State one decision the curriculum cannot make for you.
7. Record where you will keep learning artifacts.

### Permitted actions

- Read documentation and repository files.
- Write personal or disposable learning notes.
- Ask a human to clarify organizational authority.
- Mark an item incomplete without penalty.

### Prohibited actions

- Install skills, modify production code, or execute project commands.
- Paste secrets, personal data, customer data, or private source into an
  unapproved AI service.
- claim that role, seniority, lesson completion, or reviewer agreement grants
  approval.
- mark a diagnostic item complete based only on term recognition.

### Expected artifact

Your record should contain: date, intended role, checked evidence, gaps, chosen
level, next-page link, expected completion artifact, missing context, and human
authority boundary.

### Verification procedure

Ask another person to locate your next page and explain why you chose it using
only the record. If they must infer your evidence or authority boundary, revise
the record. Verification checks clarity, not whether the other person prefers
a different level.

## Check your understanding

1. A learner can define “agent” but has never reviewed a tool permission. Which
   competency is demonstrated, and where should the learner start?
2. Why is the Learn sequence not a mandatory feature-delivery sequence?
3. If all review agents agree that a release is safe, who approves release?
4. A skill lesson and its generated reference disagree. Which is operationally
   canonical, and what should happen next?
5. What evidence shows that a learner can move from Level 1B to Level 2A?

<details>
<summary>Answers for the Learn-hub knowledge check</summary>

1. The learner may satisfy part of **Can explain**, but cannot demonstrate or
   prove safe tool use. Start no later than Level 2A and revisit Level 0’s risk
   boundary if probabilistic output and evidence are also unclear.
2. Curriculum order builds prerequisite knowledge. Delivery order is selected
   from request risk, repository evidence, state, and policy. A defect and a new
   regulated capability need different operational rigor.
3. The organization’s accountable release owner. Review agents supply evidence
   or findings; agreement does not create authority.
4. The skill contract and generated reference own current behavior. Record the
   lesson as stale, verify repository tests, and correct the teaching page.
5. A source-selection and evidence artifact that identifies authority,
   freshness, omissions, rejected context, verification, uncertainty, and a
   human escalation condition.

</details>

## Common failure modes

| Failure | Why it happens | Observable symptom |
| --- | --- | --- |
| Starting from job title | Senior domain expertise is confused with agent-operation evidence | Early exercises contain unexplained tool or evidence assumptions |
| Reading without producing artifacts | Recognition feels like competence | No one can inspect what the learner did |
| Treating checks as approval | Passing criteria are confused with decision authority | “The AI approved it” appears in a handoff |
| Copying commands from lessons | Learn is mistaken for reference or how-to | Command differs from the current canonical page |
| Hiding failed checks | Progress is valued over evidence | Missing context and uncertainty disappear from notes |
| Collecting every source | More context is assumed to be better | Relevant instructions are buried and contradictions go unrecorded |
| Skipping recovery | A first failure feels like disqualification | Learner retries randomly or expands permissions |

## Recovery guidance

If a knowledge check fails, return to the heading linked by the answer, create a
new example from your role, and retake only the failed question. If the problem
is terminology, use the glossary and write a one-sentence distinction; do not
paste the glossary into your notes.

If repository context is missing, record exactly what you searched, what was
not found, what decision depends on it, and the safest provisional assumption.
Continue only with read-only, reversible work that does not depend on the
answer. Escalate when the missing fact changes product scope, permissions,
security posture, legal obligations, or destructive action.

If an exercise command fails, stop at the failure boundary. Record command,
working directory, environment, exit status, and output. Use the exercise reset
path or canonical troubleshooting guide. Do not “fix” the problem by adding
global permissions or deleting files whose ownership is unclear.

If the page feels too dense, use the table of contents to complete one objective
per session. The chapter remains incomplete until the practice artifact and
evidence exist, but learning may be paused safely.

## Evidence of completion

You have completed the hub when you can show:

- a dated diagnostic with honest checked and unchecked items;
- one evidence statement for each checked competency;
- the earliest material learning gap;
- an exact next-page link;
- the expected artifact for that level;
- a named storage location for learning evidence;
- at least one missing-context or uncertainty statement;
- a human decision that lessons and agents cannot approve.

## Completion checklist

- [ ] I can explain Learn, Reference, Use, Adopt, and About.
- [ ] I completed the diagnostic using evidence rather than confidence.
- [ ] I selected the earliest material gap.
- [ ] I recorded an expected next artifact and verification method.
- [ ] I know where the glossary and canonical skill reference live.
- [ ] I can explain why lesson completion and reviewer consensus are not
      approval.
- [ ] I recorded how to recover from a failed check or missing context.
- [ ] I linked my next learning step.

## Previous learning step

There is no prerequisite chapter. If basic Git or terminal vocabulary prevents
you from reading repository examples, use the
[Git and terminal primer](foundations/git-and-terminal-primer.md), then return
to this diagnostic.

## Next learning step

Continue to [Level 0: AI foundations](learn/ai-foundations.md), unless your
diagnostic provides evidence for a later starting point. Even fast-lane
learners should retain this hub as the progress and recovery map.

## Sources and adaptation notes

- **HARNESS-DOCS** — [AI SDLC Harness documentation and repository contracts](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/faccb4354464a1a3cc309b7b2dfa65e8efaf3529/docs). Owner: AI SDLC Harness maintainers; revision: `faccb4354464a1a3cc309b7b2dfa65e8efaf3529`; reuse: `internal-authority`; mode: `synthesized`. Informed: learning order, ownership, and authority. Transformed: repository concepts became an original diagnostic hub. Limitation: exact contracts remain canonical elsewhere.
- **MS-GENAI-BEGINNERS** — [Generative AI for Beginners](https://github.com/microsoft/generative-ai-for-beginners). Owner: Microsoft; revision: `645f932514e9f22f688c8feb3e49a7a7f2eb6f1b`; reuse: `adaptable-with-verification`; mode: `reference`. Informed: progressive beginner sequencing. Transformed: original harness competencies and risk exercises replace source activities. Limitation: no source lesson, heading, media, quiz, or example was imported.
- **MS-AI-BEGINNERS** — [AI for Beginners](https://github.com/microsoft/AI-For-Beginners). Owner: Microsoft; revision: `33e781bf7bfb9b39fd27c4e4a3e592669b52cb4b`; reuse: `adaptable-with-verification`; mode: `reference`. Informed: diagnostic entry and practice rhythm. Transformed: evidence-based fast lanes replace the source course order. Limitation: notebooks, quizzes, datasets, illustrations, and prose were excluded.
- **GOOGLE-TECH-WRITING** — [Google Technical Writing courses](https://developers.google.com/tech-writing). Owner: Google; revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. Informed: audience and observable-objective checks. Transformed: principles were applied to original harness material. Limitation: no Google prose, exercise, example, or structure was adapted.
- **DIATAXIS** — [Diátaxis documentation framework](https://diataxis.fr/). Owner: Daniele Procida; revision: `reviewed-2026-07-21`; reuse: `reference-only`; mode: `reference`. Informed: documentation-purpose boundaries. Transformed: used only to audit the repository-owned six-section architecture. Limitation: wording, diagrams, metaphors, examples, and structure were excluded.
