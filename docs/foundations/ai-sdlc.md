---
title: What is AI SDLC?
description: Understand the software delivery lifecycle, what AI changes, and why evidence must survive the agent conversation.
---

# What is AI SDLC?

The **software development lifecycle (SDLC)** is the repeatable path from a
problem or opportunity to software that is understood, built, tested,
released, operated, and improved. Organizations name the stages differently,
but the underlying questions are stable:

- Why should this change exist?
- What behavior and constraints define success?
- How will it be designed and divided into safe work?
- What evidence will show it works?
- Who decides, reviews, approves, releases, and responds when assumptions change?

## What AI changes

An AI agent makes exploration and implementation much faster. It can read a
repository, propose requirements, generate code, write tests, and explain a
diff. It can also lose context between sessions, infer an unstated rule,
optimize for the current prompt instead of the product outcome, or claim
completion without the evidence another person needs.

The common failure is **delivery amnesia**:

```text
chat request -> fast code -> passing local test -> context disappears
```

The diff may be valid, but the team cannot reliably answer why a choice was
made, which requirement a test proves, whether a reviewer accepted the risk,
or what the next agent may safely do.

## AI SDLC adds an evidence loop

**AI SDLC** is the SDLC expressed so humans and AI agents can share a durable,
inspectable operating model. The agent still performs judgment-heavy work, but
it works through bounded capabilities and leaves repository evidence:

```text
request
  -> grounded context
  -> requirement and acceptance criteria
  -> design and decisions
  -> bounded tasks and tests
  -> implementation
  -> validation and review evidence
  -> handoff and traceable commit
  -> learning or controlled recovery
```

The important change is not “more documents.” It is **continuity**. Each stage
produces enough evidence for the next person or agent to verify its inputs,
understand its authority, and continue without reconstructing the original chat.

## A concrete example

Suppose the request is “add account lockout after repeated failed logins.”

Without an evidence loop, an agent might select five attempts, a 15-minute
window, and an administrator reset because those defaults sound reasonable.
Those are product and security decisions, not implementation details.

With AI SDLC:

1. The agent identifies the missing rules and asks the accountable owner.
2. Requirements record attempts, time window, reset behavior, audit needs, and
   user-visible states.
3. Design records where counters live, concurrency boundaries, and failure modes.
4. Test cases cover expiry, concurrent attempts, reset, bypass, and audit events.
5. Tasks bound the implementation; validation links results to the cases.
6. The commit names the spec and current checks.

If the lockout window later changes, traceability shows which design, tests,
evidence, and tasks may be stale.

## What remains human

AI SDLC does not turn an agent into an accountable product owner, security
approver, or release authority. The agent can discover evidence, expose options,
execute permitted mechanics, and report gaps. People own intent, trade-offs,
risk acceptance, protected approvals, and signoff.

Next: [What is SDD?](sdd.md).
