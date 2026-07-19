---
layout: default
title: Add a capability module
description: Register optional skills through a versioned manifest without expanding the core installation contract.
kicker: How-to · Extension
permalink: /how-to/add-module/
nav_order: 17
---

## Define the boundary

Use a module when several skills or artifacts form a coherent optional capability. A single universally required helper probably belongs in core; a domain-specific workflow should not.

## Create the manifest

Add `modules/<id>/module.json` with schema, stable ID, version, kind, harness API range, dependencies, description, and skill entries. Skill paths must remain inside the repository and point to valid packages.

## Validate discovery

Run the module validator and catalog generator. Confirm missing dependencies, incompatible API ranges, duplicate IDs, unknown skills, and path traversal all fail with actionable diagnostics.

## Preserve portability

Document the module’s inputs, artifact routes, decision authority, and fallback when the host lacks specialized execution primitives. Optional capability must not become a hidden requirement for core navigation.
