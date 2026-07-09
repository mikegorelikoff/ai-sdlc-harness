# OWASP Backend Checklist

Use this checklist when the request is broad enough that a deeper security pass
is warranted.

## Identity And Access

- Who controls the caller identity?
- Which organization, account, role, or service boundary gates the action?
- Can the action be replayed or performed on behalf of another tenant?
- Are side effects guarded before persistence, queueing, or provider calls?

## Input And State

- Which fields are externally controlled?
- Are identifiers, enums, decimals, and state transitions normalized and
  validated before use?
- Can malformed or unexpected values cross trust boundaries?
- Do failure paths leave partial state, duplicate work, or inconsistent status?

## Data Exposure

- Do responses, logs, chat messages, emails, or metrics leak sensitive values?
- Are secrets, bearer tokens, webhook secrets, or provider credentials handled
  safely?
- Are internal-only identifiers exposed where public identifiers are required?

## Workflow Abuse

- Is the operation idempotent under retries?
- Can concurrent callers bypass a business invariant or authorization check?
- Are queue, saga, or outbox retries safe?
- Can one organization influence another organization's workflow state?

## Dependency And Config Risk

- Are security-sensitive defaults explicit in config?
- Does the code assume trusted transport, trusted proxies, or trusted headers?
- Are provider/webhook signatures, timestamps, or nonces checked where needed?

## Validation Expectations

- Is the risky path covered by unit, service, transport, or integration tests?
- Are negative-path and abuse-path checks present?
- If checks are missing, can the reviewer explain the highest-value test to add?

## When To Load This Reference

Load when reviewing auth, permissions, inputs, state transitions, integrations,
secrets, webhooks, provider calls, data exposure, or security-sensitive diffs.

## Security Review Matrix

| Area | Threat | Evidence | Finding? | Test/Validation |
|---|---|---|---|---|
| Identity | spoofed or missing caller | auth context |  |  |
| Authorization | cross-tenant or role bypass | permission checks |  |  |
| Input | malformed or hostile input | validation code |  |  |
| State | invalid transition or replay | state machine |  |  |
| Secret | leaked credential | logs/config/output |  |  |
| Integration | untrusted provider/webhook | signature/nonce |  |  |
| Data | overexposure or retention issue | response/log/storage |  |  |

## Abuse Case Prompts

- What can a low-privilege user try that should fail?
- What can a different tenant or account try that should fail?
- What happens if the same request/event arrives twice?
- What happens if provider response is delayed, malformed, or replayed?
- What sensitive value could appear in logs, errors, emails, or metrics?

## Quick Flow Guidance

In `--quick-flow`, focus on the highest-risk boundary touched by the change and
recommend the smallest meaningful validation.

## Full Flow Guidance

In `--full-flow`, inspect identity, authorization, input validation, state,
secrets, integration trust, logging, data exposure, and negative-path tests.

## Decision Log Guidance

Record accepted security risk, deferred security tests, scope decisions, and
security-sensitive assumptions.

## Output Discipline

Security findings should include:

- impact;
- exploit or failure scenario;
- affected boundary;
- concrete fix direction;
- validation that would prove the fix.
