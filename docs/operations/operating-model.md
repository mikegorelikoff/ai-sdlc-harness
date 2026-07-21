---
title: Operating model and RACI
description: Define accountable human owners, agent permissions, evidence, escalation, and small-team role collapse for every material AI SDLC gate.
---

# Operating model and RACI

RACI means Responsible, Accountable, Consulted, and Informed. The agent can be
a tool used by a Responsible person; it is never Accountable. Each material
gate needs exactly one named accountable human or group under local policy.

## Lifecycle gate matrix

| Gate | Accountable (A) | Responsible (R) | Consulted (C) | Informed (I) | Agent may | Agent must not | Required evidence | Escalation owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Problem/value accepted | Product manager | Product discovery lead | Research, BA, Product Owner, representative users | Delivery and engineering leads | Gather and synthesize evidence. | Invent customers or accept value. | Discovery, sources, assumptions, decision. | Product leadership. |
| Requirements ready | Product manager | BA | Product Owner, QA, architecture, dev | Delivery and affected implementers | Derive actors, rules, scenarios, gaps. | Resolve material ambiguity silently. | Requirements, decisions, gap/readiness result. | Product leadership. |
| UX/architecture accepted | Architecture owner | Architect or UX owner | Security, dev, QA, product | Delivery and affected teams | Propose options and trace constraints. | Select material trade-offs without review. | Design, alternatives, risks, decision. | Engineering lead. |
| QA strategy ready | QA owner | QA lead | BA, dev, product, security | Delivery and implementers | Generate coverage and traceability. | Accept uncovered risk. | QA strategy, cases, suite, readiness. | QA lead. |
| Release slice approved | Product manager | Product Owner | Delivery, engineering, QA, security | Affected teams and stakeholders | Analyze dependency and readiness. | Change priority or scope approval. | Backlog, dependencies, release decision. | Product leadership. |
| Branch/task start | Engineering lead | Developer | Repository owner, reviewer | QA and delivery owner | Check branch/spec alignment. | Rewrite unrelated work or bypass policy. | Clean status, branch, task/spec reference. | Repository owner. |
| SDD ready | Engineering lead | Change owner | BA, QA, architecture, security | Implementers and delivery owner | Scaffold, analyze, validate, report gaps. | Start material implementation with blocking gaps. | Requirements, design, tests, QA, tasks, plan. | Engineering owner. |
| Implementation accepted | Code owner | Developer | Reviewers, QA, security as required | Product and delivery owner | Modify in-scope code and tests under instruction. | Expand scope, approve own risk, or hide failures. | Diff, tests, decisions, task state. | Engineering lead. |
| Product outcome accepted | Product Owner | Change owner | Product manager, QA, representative user | Delivery and engineering leads | Assemble revision-bound acceptance evidence. | Accept outside delegated authority or invent product approval. | Accepted revision, AC results, demonstration evidence, DEC disposition. | Product manager. |
| Security/privacy accepted | Security owner | Security reviewer | Engineering, legal/compliance, data owner | Product, delivery, and incident owner | Test, enumerate abuse cases, report evidence. | Declare legal compliance or accept residual risk. | Threats, findings, remediation, exceptions. | Security leadership. |
| Validation complete | QA owner | Developer or QA executor | Engineering, CI owners, security as required | Change and delivery owners | Run focused deterministic checks and report exact results. | Claim skipped or stale evidence passed. | Commands, outputs, revision, environment, gaps. | Change owner. |
| Review findings resolved | Code owner | Developer | Independent reviewer, QA/security | Change and delivery owners | Rank findings and verify revisions. | Suppress P0/P1 or self-approve protected changes. | Findings, dispositions, revalidation. | Engineering lead. |
| Policy/waiver accepted | Policy owner | Policy administrator | Security, delivery, product, legal as needed | Affected repository and release owners | Evaluate declared rules and produce resolution. | Weaken policy or grant an exception. | Policy input, resolution, owner, expiry. | Policy authority. |
| Commit ready | Change owner | Developer | Reviewer, QA as required | Repository and delivery owners | Check staged scope, traceability, message, tests. | Stage unrelated files or commit incomplete work. | Staged diff, task, validation, commit message. | Repository owner. |
| Release/deployment approved | Release owner | Delivery/release lead | Product, engineering, QA, security, operations | Support teams and stakeholders | Assemble readiness and rollback evidence. | Deploy or approve release without explicit authority. | Release package, compatibility, rollback, signoffs. | Delivery leadership. |
| Incident contained/resumed | Incident commander | Incident response team | Security, operations, engineering, vendor owners | Affected owners and notification stakeholders | Collect diagnostics, stop bounded automation, propose recovery. | Destroy evidence, rotate secrets, notify parties, or resume autonomously. | Timeline, state, logs, containment, approvals. | Incident commander. |
| Pilot scale/stop decision | Executive/adoption owner | Pilot owner | Team leads, users, security, finance as relevant | Participants and affected leadership | Aggregate metrics and limitations. | Claim causality or authorize rollout. | Baseline, samples, incidents, feedback, cost/resource ledger, recommendation. | Executive sponsor. |

## Decision and action separation

The accountable person accepts the decision. The agent may perform a bounded
action after that decision only when repository policy, sandbox, permissions,
and the selected skill allow it. Approval in a chat is not automatically a
release-system, cloud, credential, or production authorization.

## Small-team role collapse

Small teams can combine responsibilities without hiding which hat is active.

| Team shape | Allowed collapse | Required separation |
| --- | --- | --- |
| Solo/learning repository | One person may own product, engineering, QA, and release. | Agent remains non-accountable; destructive/external actions still need explicit human confirmation. |
| Small product squad | PM can own product/BA; lead can own architecture/dev; QA can own test readiness. | Material security, policy exception, and release risk need named review, internal or external. |
| Platform team | Platform owner can own harness and repository operations. | Consumer product intent and risk stay with consumer owners. |
| Regulated/high-risk work | Roles may share staff only if policy permits. | Independent review, qualified legal/compliance authority, and formal records cannot be collapsed away. |

When one person fills several cells, record the role and decision separately in
the artifact or decision log. For high-impact changes, use two-person review or
another control required by policy.

## Handoff contract

A handoff contains result, blockers, required next action, optional actions,
reasons, exact invocations, and expected artifacts. The receiver verifies the
artifact and freshness rather than trusting the previous conversation.

Escalate when:

- no accountable owner exists;
- evidence conflicts or a protected decision is unresolved;
- requested permissions exceed the declared task;
- a policy exception, destructive action, external write, release, or incident action is needed;
- the agent or helper cannot reproduce its own claimed result.
