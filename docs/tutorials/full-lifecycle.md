---
title: Run the full lifecycle
description: Execute a fixture-backed organization SSO journey through all 18 refinement stages, a blocked-and-resumed QA handoff, the 18/18 gate, and implementation SDD.
---

# Run the full lifecycle

This runnable delivery exercise turns a prepared organization single sign-on
(SSO) scenario into an implementation-ready package. It deliberately stops
before production code: the reproducible outcome is accepted 18/18 refinement
evidence plus an implementation SDD, not a fictional shipped identity system.

`--full-flow` makes one selected skill strict. It never triggers the next skill.
The complete lifecycle below exists because you explicitly invoke all 18 skills
and accept each handoff.

## 1. Create the disposable lifecycle repository

!!! terminal "Run in terminal — harness source checkout"

    ```bash
    cp -R examples/onboarding-sso /tmp/ai-sdlc-sso-demo
    cp /tmp/ai-sdlc-sso-demo/test-environment-resolution.md /tmp/ai-sdlc-sso-test-environment-resolution.md
    rm /tmp/ai-sdlc-sso-demo/test-environment-resolution.md
    cd /tmp/ai-sdlc-sso-demo
    git init
    git checkout -b dev
    git add scenario.md decisions.md
    git commit -m "chore: initialize organization SSO scenario"
    npx -y skills@1.5.19 add mikegorelikoff/ai-sdlc-harness --all
    git add .agents .claude agent skills-lock.json
    git commit -m "chore: install AI SDLC harness"
    git init --bare /tmp/ai-sdlc-sso-demo-origin.git
    git remote add origin /tmp/ai-sdlc-sso-demo-origin.git
    git push -u origin dev
    git checkout -b feature/organization-sso
    git status --short
    ```

!!! warning "Human checkpoint"

    Review the scenario, accepted decisions, installed package diff, and branch.
    Do not continue with a secret, real identity data, an unreviewed package, or
    a dirty shared base. The prepared environment-resolution file is withheld
    until the deliberate blocker exercise.

Expected starting tree:

```text
scenario.md
decisions.md
.agents/skills/
skills-lock.json
```

The QA Platform evidence is outside the consumer at
`/tmp/ai-sdlc-sso-test-environment-resolution.md`. The agent cannot discover it
until the accountable human supplies it during the recovery exercise.

## 2. Use the same execution contract at every stage

For every prompt below, the agent must read the feature state, decision log,
specs index, exact predecessor artifacts, and only the targeted scenario
context. It writes the named canonical artifact under
`specs-refiniment/organization-sso/`, runs the owning scaffold and quality
gate, records material decisions, refreshes indexes, and returns a valid
`ai-sdlc-handoff/v1`. The accountable human accepts or rejects the exit gate.

Do not ask the agent to “continue everything” without the explicit next stage:
that would hide approval boundaries and make blocked/resume behavior impossible
to verify.

## 3. Execute stages 1–4: problem to ready requirements

### Stage 1 — `discovery`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-working-backwards-discovery --full-flow for organization-sso.
    Read scenario.md and decisions.md. Interview me about customer evidence,
    current process, alternatives, value, MVP, risks, operations, success and
    disconfirming evidence. Produce discovery.md. Do not write a PRFAQ yet.
    ```

**Owner:** Product. **Exit:** customer, problem, value, audience, boundaries,
evidence, assumptions, and unresolved decisions are explicit.

### Stage 2 — `prfaq`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-prfaq-package-synthesis --full-flow for organization-sso.
    Consume discovery.md and accepted decisions. Produce prfaq.md with press
    release, customer FAQ, internal FAQ, business requirements and launch risks.
    Stop if the promise exceeds the accepted OIDC-only MVP.
    ```

**Owner:** Product. **Exit:** customer promise and internal operating reality do
not contradict discovery or the decision log.

### Stage 3 — `delivery_package_gap_review`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-delivery-package-gap-review --full-flow for organization-sso.
    Consume prfaq.md. Produce delivery-gap-review.md with evidence reviewed,
    gap matrix, contradictions, blocking questions and readiness verdict.
    Assign every blocker to a human owner; do not repair the PRFAQ silently.
    ```

**Owner:** Delivery/BA. **Exit:** blocking workflow, rule, support, rollout, and
ownership gaps are resolved or explicitly block progression.

### Stage 4 — `requirements_readiness`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-requirements-readiness-review --full-flow for organization-sso.
    Consume prfaq.md and delivery-gap-review.md. Produce
    requirements-readiness.md with score, dimension evidence, blocking gaps,
    follow-up and final verdict. Stop on ambiguous actor, scope or policy.
    ```

**Owner:** Product/BA. **Exit:** requirements are ready to feed planning and QA.

Check the resumable state. A non-zero result is expected because 14 stages
remain; it must name the next stage rather than claiming completion.

!!! terminal "Run in terminal"

    ```bash
    python3 .agents/skills/ai-sdlc-shared-runtime/scripts/refinement_status.py --feature organization-sso --gate full --format toon
    ```

## 4. Execute stages 5–9: outcomes, backlog, and release slices

### Stage 5 — `goal_epic_mapping`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-goal-capability-and-epic-mapping --full-flow for organization-sso.
    Consume requirements-readiness.md. Produce goal-capability-map.md with
    business goals, role matrix, capabilities, outcome epics and traceability.
    Separate mechanism signals from customer outcomes.
    ```

### Stage 6 — `backlog_gap_review`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-backlog-requirements-gap-review --full-flow for organization-sso.
    Consume goal-capability-map.md. Produce backlog-gap-review.md. Challenge
    unclear scope, priority, dependency, owner, sequencing and readiness.
    ```

### Stage 7 — `backlog_decomposition`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-backlog-decomposition-and-task-planning --full-flow for organization-sso.
    Consume backlog-gap-review.md and goal-capability-map.md. Produce backlog.md
    with bounded epics, stories, acceptance summary, priorities, dependencies,
    cross-functional tasks and Definition of Ready.
    ```

### Stage 8 — `story_decomposition`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-user-story-decomposition --full-flow for organization-sso.
    Consume backlog.md. Produce user-stories.md with actor/value stories,
    acceptance criteria, positive/negative scenarios, dependencies, risks and
    readiness. Cover administrator, member, support and break-glass actors.
    ```

### Stage 9 — `release_slicing`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-release-slicing-and-backlog-readiness-review --full-flow for organization-sso.
    Consume backlog.md. Produce release-slicing.md with opt-in MVP, later slices,
    sequencing, dependencies, milestones, exit criteria, rollout and rollback.
    This declared complete cascade requires the stage; do not silently skip it.
    ```

**Owners:** Product and Delivery. **Checkpoint:** accept outcome trace, story
boundaries, OIDC-only MVP, opt-in rollout, dependencies, and rollback criteria.

## 5. Execute stages 10–12: business behavior and QA entry

### Stage 10 — `ba_context`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-ba --full-flow for organization-sso.
    Consume user-stories.md. Produce business-context.md with current/desired
    behavior, actor-permission matrix, end-to-end workflows, business rules,
    acceptance and gaps. Make organization isolation and recovery explicit.
    ```

### Stage 11 — `delivery_spec`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-delivery-spec-synthesis --full-flow for organization-sso.
    Consume business-context.md. Produce delivery-spec.md with requirement,
    workflow and rule detail, story/acceptance trace, QA and operational notes,
    and handoff risks. Do not choose architecture that owners have not accepted.
    ```

### Stage 12 — `qa_plan`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-qa --full-flow for organization-sso.
    Consume requirements-readiness.md, scenario.md and accepted decisions.
    Produce qa.md with acceptance, regression, risk, data/environment,
    validation, manual checks and signoff. Include wrong organization, expired
    assertion, provider outage, clock skew, removed user and break-glass paths.
    ```

Stages 10–11 and 12 may progress as two controlled branches after
`requirements_readiness`; they never share one writable artifact. Product/BA
accept behavior, and QA accepts initial scope before the QA branch continues.

## 6. Execute stage 13 with a deliberate blocker and resume

### Stage 13 — `qa_gap_review`, first attempt

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-qa-requirements-gap-review --full-flow for organization-sso.
    Consume qa.md and accepted requirements. For this first attempt, do not read
    test-environment-resolution.md. Treat the OIDC simulator owner, synthetic
    data boundary and environment availability as unknown. Produce only valid
    blocked evidence and the exact information needed to resume; do not invent it.
    ```

Expected: `qa-gap-review.md` or state records an owned blocker; stage 14 does
not start; the handoff result is `blocked` with a non-empty blocker list.

!!! warning "Human checkpoint"

    QA Platform is accountable for environment facts. Review the withheld file;
    if acceptable, provide it as new repository evidence:

    ```bash
    cp /tmp/ai-sdlc-sso-test-environment-resolution.md test-environment-resolution.md
    git status --short
    ```

    Expected: exactly `test-environment-resolution.md` plus the current
    lifecycle artifacts are new or modified; no production identity data or
    secret is present.

### Stage 13 — resume

!!! example "Tell your agent"

    ```text
    Resume ai-sdlc-qa-requirements-gap-review --full-flow for organization-sso.
    Read test-environment-resolution.md as owner-provided evidence. Update
    qa-gap-review.md, resolve only covered blockers, rerun its quality gate,
    complete stage 13, refresh indexes, and hand off to test strategy.
    ```

This is a true resume: it preserves the blocked attempt and adds evidence. It
does not restart discovery or erase why progress stopped.

## 7. Execute stages 14–17: executable QA coverage

### Stage 14 — `test_strategy`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-test-scope-and-strategy-design --full-flow for organization-sso.
    Consume qa-gap-review.md. Produce qa-strategy.md with scope, risk priorities,
    layers/suites, synthetic data, environment, automation and residual risks.
    ```

### Stage 15 — `test_cases`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-test-cases --full-flow for organization-sso.
    Consume qa-strategy.md and requirements. Produce test-cases.md with detailed
    expected results and trace for positive, negative, permission, isolation,
    outage, clock, provisioning, removal, audit and recovery cases.
    ```

### Stage 16 — `test_suite`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-test-case-and-suite-synthesis --full-flow for organization-sso.
    Consume test-cases.md. Produce test-suite.md with smoke, regression and UAT
    suites, entry/exit criteria and execution dependencies. Do not label an
    unautomated case automated.
    ```

### Stage 17 — `qa_traceability`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-qa-traceability-and-readiness-review --full-flow for organization-sso.
    Consume test-suite.md and requirements. Produce qa-readiness.md with
    requirement-to-test traceability, risk coverage, gaps, environment evidence,
    blocked coverage and QA readiness verdict.
    ```

Expected status: 17 stages complete and `delivery_handoff` is the exact next
stage. Missing or stale test environment evidence must reopen stage 13–17 work.

## 8. Execute stage 18 and prove 18/18

### Stage 18 — `delivery_handoff`

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-delivery-handoff-review --full-flow for organization-sso.
    Consume delivery-spec.md and qa-readiness.md. Produce
    delivery-handoff-review.md with requirement/story coverage, QA readiness,
    ownership, dependencies, decisions, implementation inputs and final verdict.
    Stop if either predecessor is missing, stale, blocked or unaccepted.
    ```

!!! terminal "Run in terminal"

    ```bash
    python3 .agents/skills/ai-sdlc-shared-runtime/scripts/refinement_status.py --feature organization-sso --gate full --format toon
    git status --short
    ```

Expected: exit zero, `18/18`, no blocking stage, and this artifact tree:

```text
specs-refiniment/organization-sso/
  _ai_sdlc/state.toon
  decision-log.md
  discovery.md
  prfaq.md
  delivery-gap-review.md
  requirements-readiness.md
  goal-capability-map.md
  backlog-gap-review.md
  backlog.md
  user-stories.md
  release-slicing.md
  business-context.md
  delivery-spec.md
  qa.md
  qa-gap-review.md
  qa-strategy.md
  test-cases.md
  test-suite.md
  qa-readiness.md
  delivery-handoff-review.md
```

If status is non-zero, resume the earliest reported stage. Never edit
`state.toon` to manufacture 18/18.

## 9. Create the implementation SDD on the verified feature branch

!!! example "Tell your agent"

    ```text
    We are already on the verified feature/organization-sso branch.
    Use ai-sdlc-sdd --full-flow for organization-sso. Consume delivery-spec.md,
    qa-readiness.md, delivery-handoff-review.md and decisions. Produce
    implementation requirements, design, test cases, QA plan, bounded tasks,
    decision trace, plan.toon and plan.md. Stop on conflicting authority.
    ```

**Owners:** Dev/Architecture, with QA and Security signoff. **Exit:** every task
traces to accepted behavior and tests; architecture, threat boundaries,
observability, rollout, migration, monitoring and rollback are explicit.

Implementation then follows one bounded task at a time: code and tests,
validation, risk-based review/security, task evidence, and a traceable commit.
The runtime may preserve retries and resume state, but it cannot approve
product, security, QA, rollout, or release decisions.

## 10. Clean up

!!! terminal "Run in terminal"

    ```bash
    cd /tmp
    rm -rf ai-sdlc-sso-demo ai-sdlc-sso-demo-origin.git
    rm ai-sdlc-sso-test-environment-resolution.md
    ```

Only remove these disposable tutorial paths. For exact profiles and recovery
edges, keep the [complete refinement map](../flows/refinement.md) open while
running the exercise.
