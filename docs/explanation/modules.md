---
layout: default
title: Optional modules
description: Why specialized capabilities use versioned manifests while the core lifecycle remains small and portable.
kicker: Explanation · Extensibility
permalink: /explanation/modules/
nav_order: 40
---

Core should contain the controls most delivery work needs. Architecture, UX, research, and independent review can be valuable without becoming mandatory weight in every installation.

## The manifest boundary

A module declares stable identity, version, kind, harness API compatibility, dependencies, skills, and artifact capability. Discovery validates the manifest before exposing its skills to navigation.

## Additive capability

Optional modules register new workflows without changing existing skill names, flow flags, state files, or artifact authority. Core navigation can recommend an installed capability but must not assume it exists.

## Compatibility before convenience

Version ranges, dependency checks, valid paths, and duplicate detection prevent a module from looking available when it cannot safely run. A host-specific execution optimization needs a portable fallback or an explicit blocker.

This design supports a larger ecosystem while keeping the base harness understandable and independently useful.
