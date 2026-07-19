---
title: Maturity and limitations
description: Distinguish validated harness mechanisms from expected organizational outcomes, known limitations, support boundaries, and claims the project does not make.
---

# Maturity and limitations

AI SDLC Harness is an open repository of versioned skills, deterministic
helpers, contracts, examples, and documentation. It is suitable for controlled
evaluation and repository-scoped use by teams that retain human review. Its
mechanism tests are stronger evidence than its organizational outcome evidence.

## What is verified today

Repository validation covers:

- skill identity, required sections, flow flags, artifact routes, and handoffs;
- state transitions, TOON encoding, metadata, indexes, configuration, and migration;
- helper behavior, failure cases, installed-runtime synchronization, and compatibility;
- generated documentation inventory, local links, navigation, strict build, and rendered targets;
- copyable onboarding fixtures, deliberate failure/recovery, and release smoke checks.

These checks demonstrate behavior under their declared inputs. They do not
exhaust every host, repository, concurrency pattern, model behavior, policy, or
failure mode.

## Expected but not yet proven generally

The design is intended to improve continuity, reviewability, traceability,
recovery, role clarity, and selection of appropriate rigor. Those are pilot
hypotheses for each adopting team. This project does not currently publish a
controlled multi-organization study proving changes to cycle time, defect rate,
cost, developer experience, or business outcomes.

## Known limitations

- Skills depend on the host agent correctly loading and following instructions.
- Natural-language reasoning remains fallible; deterministic helpers cover only declared mechanics.
- A passing artifact can contain a poor human decision or weak underlying evidence.
- The harness cannot observe production deployment, incidents, or customer outcomes unless external systems provide that evidence.
- Public guides translate execution contracts but do not replace `SKILL.md` authority.
- Script mutability classification is conservative and cannot grant runtime permission.
- Package hashes establish integrity against a manifest, not author identity or organizational approval.
- Local metrics intentionally omit content and therefore cannot explain every cause.
- Small pilots cannot establish universal causality or rare-event safety.
- Host support, sandbox semantics, model behavior, and external CLIs can change independently.
- Regulatory, privacy, labor, accessibility, records, and sector requirements vary by jurisdiction and use case.
- English is the only maintained public documentation language for this release.

## Support boundary

The project supplies repository contracts and validation, not a hosted service,
SLA, managed incident response, compliance certification, legal advice, or
production deployment authority. GitHub issues and repository history can
support open-source maintenance, but an adopting organization must name its own
support, security, privacy, release, and incident owners.

## Non-goals

The harness is not:

- an IDE, project-management platform, CI system, deployment platform, or telemetry backend;
- an autonomous approver, product owner, security authority, QA signoff, or legal reviewer;
- a guarantee of correct software, safe models, compliance, or business value;
- a reason to expose secrets, grant broad permissions, or skip normal engineering controls;
- a requirement to run the full lifecycle for every small change.

## External governance context

The [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) is a
voluntary, use-case-agnostic risk framework and is currently being revised.
Its Core emphasizes defined human/AI roles, executive risk responsibility,
third-party risk, monitoring, incident response, recovery, and change
management. The harness can preserve evidence for local controls, but it does
not claim conformance to that framework.

The [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
describes risks such as tool misuse, privilege abuse, data leakage, cascading
failure, and rogue behavior. The harness reduces some exposure through bounded
skills, approvals, sandboxing, package trust, and fail-closed evidence. It is
not a substitute for threat modeling, secure architecture, monitoring, or
security testing.

## How to make a defensible claim

Name the exact version, scope, input, command, result, sample, limitation, and
owner. Prefer “this validator rejected these five malformed states” over “the
system is safe.” Use the [pilot metrics guide](../adoption/metrics.md) to keep
mechanism evidence separate from organizational outcomes.
