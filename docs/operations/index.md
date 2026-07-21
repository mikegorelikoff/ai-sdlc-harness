---
title: Operate the harness
description: Establish ownership, governance, recovery, support, and evidence review for routine AI SDLC Harness use.
---

# Operate the harness

Operation begins after installation. A healthy installation can still be used
unsafely if roles, data boundaries, permissions, exceptions, incidents, or
recovery are ambiguous.

Use these three operating contracts:

- [Operating model and RACI](operating-model.md): who owns each gate, what the agent may do, and how small teams collapse roles.
- [Governance and trust](governance.md): data, secrets, permissions, packages, policy, retention, exceptions, and incidents.
- [Troubleshooting and recovery](troubleshooting.md): diagnose failures without deleting authoritative evidence.
- [Field feedback disposition](field-feedback.md): map reported installation, navigation, specification, quality, security, automation, and tooling problems to controls or boundaries.

## Minimum service ownership

Name people or rotations for:

- harness/product ownership and adoption decisions;
- source package and compatibility maintenance;
- consumer repository ownership;
- security/privacy review and incident response;
- delivery/release and rollback;
- documentation and onboarding;
- user support and escalation.

An AI agent can route an issue and collect evidence. It cannot be the service
owner, risk acceptor, incident commander, or release approver.

## Routine cadence

| Cadence | Review |
| --- | --- |
| Per change | Scope, selected flow, human gates, validation, handoff, commit trace. |
| Weekly during pilot | Blockers, retries, evidence freshness, incidents, burden, participant feedback. |
| Per release | Compatibility, package trust, docs, migrations, rollback, deprecation, known limitations. |
| Monthly or quarterly | Policy, permissions, hosts/models, retained data, exceptions, support load, adoption decision. |
| After incident | Containment, evidence preservation, root cause, control changes, notification, safe resume. |

## Operational rule

Derived indexes, summaries, metrics, and state projections can be rebuilt.
Requirements, decisions, test evidence, accepted policy, Git history, and
incident records must not be deleted merely to clear an error.
