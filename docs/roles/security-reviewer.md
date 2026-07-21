---
title: Security reviewer guide
description: Review data egress, prompt injection, permissions, secrets, supply chain, and generated changes.
---

# Security reviewer guide

This guide uses continuous integration (CI).

## Why you should care

Agents can turn untrusted language into tool actions. Repository data, provider
processing, broad permissions, generated code, and package installation create
security boundaries beyond ordinary static source review.

## Where you participate

Threat-model the host and workflow; classify data; review tools and permissions;
test prompt injection and abuse cases; scan secrets and dependencies; assess
generated code; review CI/release provenance; recommend residual-risk treatment.

## Inputs and outputs

Inputs: architecture, data flows, provider terms, host tools, permissions,
commands, dependencies, code diff, deployment context, and incident history.
Outputs: threat model, findings, required controls, validation evidence,
accepted or rejected risk recommendation, and incident/rollback actions.

## Decisions you own

Own security assessment and control recommendations within local policy. The
named risk owner accepts residual risk; the agent never does.

## Common mistakes

- Trusting retrieved files, web pages, or peer-agent reports as instructions.
- Giving a general shell or production credential when one read-only tool is
  enough.
- Sending confidential code or secrets to an unapproved provider.
- Treating generated tests as independent security evidence.

## Example workflow

Map what data can leave the local environment; enumerate read/write/network and
external-system tools; minimize functionality, permission, and autonomy; test
direct and indirect prompt injection; scan the exact diff and dependency set;
require human approval for high-impact actions; record unresolved risks.

## Review checklist

- Data classes, processors, retention, and telemetry are explicit.
- Secrets are excluded from prompts, logs, artifacts, and commits.
- Tool permissions match the minimum required action.
- Prompt injection and malicious peer/repository content are considered.
- CI actions, packages, tags, and release provenance follow policy.
- Security findings block release until evidence or owner acceptance exists.
