---
title: Governance and trust
description: Govern human authority, data, secrets, permissions, packages, policy exceptions, retention, incidents, and regulatory boundaries for repository-native AI agents.
---

# Governance and trust

The harness preserves evidence for governance; it does not supply an
organization's risk appetite or legal authority. Adopt it only inside an
approved policy for AI services, source code, data, credentials, third-party
packages, repositories, and release systems.

The [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
calls for defined human/AI roles, executive risk responsibility, third-party
risk controls, monitoring, incident response, recovery, and change management.
The model below translates those themes to this repository; it is not a claim
of NIST conformance or legal compliance.

## Authority hierarchy

1. Applicable law, contract, and organizational policy.
2. Accountable human decisions and accepted repository policy.
3. Authoritative requirements, decisions, tests, and Git history.
4. Skill execution contracts and deterministic helper validation.
5. Derived state, indexes, metrics, summaries, and chat explanations.

A lower layer cannot override a higher one. A passing helper does not grant
permission, and a chat message does not replace a required approval system.

## Data and secrets

The installer is a separate data boundary. The third-party Skills CLI documents
anonymous telemetry of skill name, skill files, and timestamp by default. The
canonical install commands set `DISABLE_TELEMETRY=1`; a pilot must record the
human privacy/data owner's choice, provider policy, retention, and any approved
exception. Content-free local metrics do not imply that npm, GitHub, the agent
host, or model provider is network-free.

Classify data before an agent can read it.

| Class | Default treatment |
| --- | --- |
| Public | May be used within approved host terms and repository policy. |
| Internal | Limit to approved repositories, models, tools, retention, and users. |
| Confidential | Deny by default; require named purpose, minimum fields, approved service, and owner. |
| Secret/credential | Never place in prompts, artifacts, logs, examples, or agent-readable files. Use the authorized secret system. |
| Regulated/special category | Deny unless qualified privacy/legal/compliance owners approve the use case and controls. |

Minimize inputs, redact examples, use placeholders, and inspect diffs and agent
output for disclosure. OWASP identifies
[Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
as a material generative-AI risk; repository locality does not guarantee that a
hosted model or connector keeps data local.

If a secret is exposed, stop work, preserve non-secret incident evidence,
contact the incident owner, rotate/revoke through the authorized system, assess
downstream exposure, and resume only with approval. The agent must not rotate a
credential autonomously.

### Data-egress worksheet

Complete this matrix for the actual deployment before a pilot. “Unknown” is a
blocker for confidential or regulated data, not permission to proceed.

| Boundary | Data that may leave | Questions the accountable owner must answer |
| --- | --- | --- |
| Agent/model host | Prompts, selected source, diffs, tool results, metadata | Provider, model, region, retention, training use, access, deletion, contract |
| Browser/search | Search text, opened URLs, page content, IP/identity metadata | Approved domains, logging, safe-search policy, confidential terms prohibited |
| Connectors | Query parameters and returned mail/calendar/document data | OAuth scopes, tenant boundary, recipients, retention, revocation, audit log |
| npm/GitHub installer | Package/source requests and upstream CLI telemetry unless disabled | Mirror, proxy logs, account identity, integrity, telemetry opt-out |
| Continuous integration | Source, commands, logs, caches, artifacts, job metadata | Fork exposure, secret masking, retention, artifact access, runner location |
| Error/reporting systems | Stack traces, filenames, snippets, environment metadata | Redaction, access, retention, downstream processors, deletion |

Record the decision owner, date, evidence link, accepted data classes, denied
fields, compensating controls, and review/expiry date. Reassess after provider,
model, connector, region, retention, or repository classification changes.

Pattern screening in project-context helpers is defense in depth, not a
complete secret scanner. Keep credentials out of agent-readable files and use
approved repository/CI secret scanning as a separate preventive control.

## Permissions and sandbox

Grant the least filesystem, command, network, identity, and external-system
capability required for the bounded task. Prefer read-only discovery, then
preview/check/emit modes, then explicit writes. Separate repository write from
release, cloud, production, messaging, and financial authority.

OWASP describes
[Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
as risk rooted in excessive functionality, permissions, or autonomy. Skill
selection and sandbox approval reduce exposure only when host enforcement and
human review are real.

Never approve a broad command prefix merely to avoid repeated prompts. Review
the command category, target, effects, credentials, rollback, and whether the
same authority would apply to future arguments.

## Package and supply-chain trust

Before accepting an installed or updated capability:

- verify repository/package origin and version;
- inspect the manifest, declared files, hashes, capabilities, API range, and provenance policy;
- reject unsafe paths, symlinks, hash drift, undeclared capabilities, or incompatibility;
- review code and release history appropriate to risk;
- install project-scoped before considering broader scope;
- record the accepted inventory and rollback baseline.

An `allow` trust decision is evidence, not install or execution approval. A hash
matches bytes to a manifest; it does not prove author identity or safety.

## Policy, waivers, and exceptions

Policy evaluation must fail closed when a protected field, owner, condition, or
evidence is missing. A waiver records:

- policy/rule and exact scope;
- business reason and alternatives considered;
- risk and compensating controls;
- accountable approver and consulted owners;
- start, expiry, and review date;
- affected repositories, tasks, data, hosts, and capabilities;
- rollback/revocation action and required evidence.

Agents may draft and validate the record. They may not grant, extend, or hide a
waiver. Expired or broadened exceptions require a new decision.

## Retention and deletion

Define retention by artifact class, not convenience.

| Record | Minimum governance question |
| --- | --- |
| Requirements and decisions | How long must delivery intent and approvals remain auditable? |
| Validation and review evidence | What release, audit, or incident window applies? |
| Agent/runtime journals | What diagnostic value justifies retention, and what content is prohibited? |
| Local metrics | Are aggregates sufficient, and who may access or export them? |
| Research/source inventory | Do licenses, privacy, or source terms limit storage and quotation? |
| Incident and exception records | Which legal, security, contractual, or insurance requirements apply? |

Derived data may be rebuilt, but deletion still follows authorized records
policy. Never remove authoritative evidence to bypass a validator or conceal an
incident. Legal hold or investigation requirements override routine cleanup.

## Enforcement map

| Governance concern | Repository mechanism | Accountable decision remains with |
| --- | --- | --- |
| Command permission and sandbox escalation | [Approvals and sandbox](../reference/skills/ai-sdlc-approvals-sandbox.md) | Repository/security owner. |
| Delivery rule and eligible waiver evaluation | [Policy](../reference/skills/ai-sdlc-policy.md) | Named policy authority. |
| Package origin, integrity, capability, compatibility, provenance | [Package trust Branch A](../reference/skills/ai-sdlc-package-trust.md) | Security/release owner. |
| Content-free local aggregate generation | [Package trust Branch B](../reference/skills/ai-sdlc-package-trust.md) | Delivery/privacy owner. |
| Security abuse cases and validation | [Security testing](../reference/skills/ai-sdlc-security-testing.md) | Security owner. |
| Independent evidence synthesis | [Evidence council](../reference/skills/ai-sdlc-evidence-council.md) | Human review/signoff owner. |
| Failed state, change, or interrupted run | [Recovery journey](../flows/recovery.md) and [troubleshooting](troubleshooting.md) | Artifact owner or incident commander. |

## Incident response

1. **Stop and contain:** pause agent/runtime mutations and narrow or revoke temporary access.
2. **Preserve:** record time, revision, state, commands, outputs, permissions, affected systems, and known data exposure without copying secrets.
3. **Escalate:** notify the named incident commander, security/privacy owner, repository owner, and external provider owner as policy requires.
4. **Assess:** classify confidentiality, integrity, availability, safety, legal, contractual, and delivery impact.
5. **Recover:** repair through reviewed changes, rotate credentials in authorized systems, validate from the last accepted baseline, and keep failed evidence.
6. **Communicate:** the accountable organization decides notifications, disclosure, and user/customer communication.
7. **Learn:** record root causes, control changes, owners, deadlines, and safe-resume approval.

The agent may help collect and correlate evidence. It is not the incident
commander and cannot decide notification obligations.

## Regulatory and contractual boundary

AI, privacy, employment, accessibility, records, intellectual-property,
cybersecurity, export, and sector rules vary by jurisdiction and use case. The
harness does not interpret which rules apply and does not certify compliance.
Engage qualified owners before regulated or high-impact use. Record the
applicable policy and review decision as inputs, not model-generated facts.
