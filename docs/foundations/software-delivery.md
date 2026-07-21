---
title: Software delivery foundations
description: Learn what software development and the SDLC are, who participates, and why delivery work needs explicit evidence.
---

# Software delivery foundations

This chapter is for readers who have not worked with a formal software
development lifecycle. It introduces the delivery concepts that later harness
pages rely on.

## Software development is more than writing code

Software development turns a need into a maintained software capability. Code
is one output. Teams also discover the problem, decide scope, design behavior,
manage risk, test results, release safely, observe operation, and change the
system over time.

A **software development lifecycle (SDLC)** is the repeatable set of activities
used to organize that work. Names vary, and real teams iterate rather than move
once through a straight line, but most lifecycles include:

1. **Discovery and requirements:** understand the users, desired outcome,
   business rules, constraints, assumptions, and acceptance conditions.
2. **Design:** decide boundaries, data, interfaces, user experience, operational
   behavior, risks, and alternatives.
3. **Implementation:** change source code, configuration, infrastructure, or
   documentation within the accepted scope.
4. **Verification and validation:** check that the result was built correctly
   and that it solves the intended problem.
5. **Release:** review, approve, deploy, communicate, and preserve rollback
   evidence.
6. **Operation and maintenance:** monitor behavior, respond to incidents, fix
   defects, manage dependencies, and evolve the system.

Lifecycle structure matters because decisions made early affect every later
stage. If a requirement changes after tests and code exist, those downstream
artifacts may be stale. The harness makes that relationship visible; it does
not require every change to use the same amount of ceremony.

## Roles and accountability

One person may perform several roles on a small team, but the decisions remain
different:

| Role area | Typical responsibility |
| --- | --- |
| Product | Customer problem, value, priority, scope, and outcome acceptance |
| Business analysis | Actors, workflows, business rules, exceptions, assumptions, and requirements quality |
| Design and architecture | Technical and experience boundaries, trade-offs, and constraints |
| Engineering | Implementation, technical tests, maintainability, and engineering risk |
| Quality assurance | Test strategy, negative paths, regression, and independent acceptance evidence |
| Security and privacy | Threats, data handling, permissions, abuse cases, and residual risk |
| Platform and operations | Reproducible environments, continuous integration, release, observability, rollback, and support |
| Delivery leadership | Ownership, sequencing, capacity, governance, and escalation |

The harness assigns work to roles, but a local responsibility assignment matrix
(RACI) must name the actual people or groups. **Responsible** means doing the
work; **Accountable** means owning the final decision; **Consulted** and
**Informed** describe participation. A slash-separated role label is a template
candidate, not two simultaneous accountable owners.

## Requests, requirements, specifications, plans, and tasks

These terms are related but not interchangeable:

- A **request** is the initial statement of desired change. It may be vague.
- A **requirement** states a needed outcome, rule, quality, or constraint.
- A **specification** organizes accepted requirements and observable behavior
  precisely enough to guide design, implementation, and testing.
- A **plan** orders work and dependencies.
- A **task** is a bounded unit of work with an output and traceable references.
- An **implementation** is the actual change.
- **Validation evidence** is the recorded result of checks against the accepted
  requirement; saying that a check ran is not evidence that it passed.

## Functional and non-functional requirements

A **functional requirement** describes behavior: for example, an authenticated
user can revoke one active session. A **non-functional requirement (NFR)**
describes a measurable quality or constraint: for example, revocation becomes
effective within 30 seconds under a named load and is verified by a specified
test. Words such as “fast,” “secure,” or “accessible” are goals, not testable
NFRs, until a target, condition, measurement method, and owner are defined.

## Ready and done

**Definition of Ready** is a local checklist for starting work. It may require a
clear outcome, owner, dependencies, acceptance criteria, risks, and test data.

**Definition of Done** is a local checklist for accepting an increment. It may
require implementation, review, relevant tests, security checks, documentation,
operational readiness, acceptance evidence, and a clean handoff. Neither
definition replaces judgment; both make expectations reviewable.

## Common delivery failures

- **Ambiguity:** several reasonable interpretations exist, but nobody records
  which one was accepted.
- **Scope creep:** work expands without a corresponding product decision,
  impact analysis, or updated acceptance boundary.
- **Rework:** downstream work must be repeated because upstream intent or
  constraints were incomplete or changed silently.
- **Defect:** software behaves differently from an accepted requirement or
  expected quality.
- **Technical debt:** a deliberate or accidental design compromise increases
  the cost or risk of future change.
- **Stale evidence:** a test, approval, or review describes an older revision.
- **Handoff loss:** the next person knows what changed but not why, what remains,
  or which evidence can be trusted.

## A compact delivery model

```text
problem and evidence
        ↓
accepted requirements and decisions
        ↓
design, risks, acceptance criteria, and tests
        ↓
bounded implementation tasks
        ↓
implementation plus independent validation
        ↓
human acceptance, release, operation, and learning
```

At every arrow, ask: what is authoritative, who owns the decision, what can be
checked mechanically, and what becomes stale if this changes?

## Check your understanding

- Can you distinguish a request from a testable requirement?
- Can you name the accountable owner for value, technical correctness, quality,
  security, and release in your project?
- Can you explain why passing unit tests may still be insufficient acceptance
  evidence?
- Can you identify which downstream artifacts must be reconsidered after a
  requirement changes?

## References

- [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf)
- [ISO/IEC/IEEE 29148 requirements engineering overview](https://www.iso.org/standard/72089.html)
- [Official Scrum Guide](https://scrumguides.org/scrum-guide.html) for one
  established Product Owner and increment model; this harness is not limited to
  Scrum.

Next: [Artificial intelligence foundations](ai-foundations.md).
