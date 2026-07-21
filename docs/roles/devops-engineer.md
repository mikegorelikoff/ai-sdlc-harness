---
title: Development and operations engineer guide
description: Make installation, continuous integration and continuous delivery, configuration, release, upgrade, and rollback reproducible.
---

# Development and operations (DevOps) engineer guide

This guide uses continuous integration and continuous delivery (CI/CD) and operating system (OS).

## Why you should care

The harness installs executable instructions and scripts into many repositories.
Platform controls keep versions, permissions, generated files, and validation
consistent across developer machines and continuous integration.

## Where you participate

Validate prerequisites and supported environments; create approved mirrors;
integrate consumer CI; manage configuration and secrets; test upgrades,
rollback, uninstall, cache, and cleanup; monitor fleet drift.

## Inputs and outputs

Inputs: pinned release, package origin, supported host/OS matrix, network policy,
configuration schema, CI platform, and rollback requirements. Outputs: install
runbook, consumer CI, artifact manifest, version inventory, upgrade waves,
rollback evidence, and support diagnostics.

## Decisions you own

Own platform implementation and operational recommendations. Security approves
trust controls; application teams own repository changes; release owners approve
production promotion.

## Common mistakes

- Using `--offline` before a clean cache is populated.
- Treating installer target creation as host support.
- Allowing generated caches or broad agent directories into feature commits.
- Running network-dependent smoke tests without timeouts and captured output.

## Example workflow

Provision exact Git, Node.js, npm, Python, and agent versions; install in an
empty Git repository; record created paths and counts; run installed-only helper
checks; add consumer CI; test update, rollback, remove, and artifact preservation;
repeat on every claimed OS and host.

## Review checklist

- Runtime and package-manager floors are machine-checked.
- Network, proxy, certificate, authentication, and permissions are documented.
- Dependencies and CI actions follow an approved pin/update policy.
- Scripts are idempotent or clearly state mutation and recovery.
- Generated files are ignored or intentionally tracked.
- Fleet version, policy, rollback, and uninstall are observable.
