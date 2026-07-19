---
layout: default
title: Install the harness
description: Add AI SDLC skills and shared helpers to a project while keeping repository-owned files visible and reviewable.
kicker: How-to · Setup
permalink: /how-to/install/
nav_order: 11
---

## Before you begin

Use a clean working tree and know which project should receive the skills. Installation writes repository files; treat the result like source code, not an opaque tool cache.

## Install

```bash
git clone https://github.com/mikegorelikoff/ai-sdlc-harness.git
cd ai-sdlc-harness
./scripts/install.sh /absolute/path/to/project
```

If your checkout exposes a different installer command, follow the [authoritative install guide](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/guides/install-and-update.md) for the current release.

## Verify the result

Confirm that skill packages, shared helpers, modules, and configuration arrived at their documented paths. Run the compatibility validator in the installed project and inspect `git status --short`; unexpected replacement of project-owned files is a blocker.

## First use

Ask the assistant to run `ai-sdlc-navigator --quick-flow` with a real task. The navigator should detect installed capabilities and repository context rather than presenting a fixed generic menu.
