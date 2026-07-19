---
title: Supported versions
description: Release, harness API, compatibility, and migration support matrix.
---

# Supported versions

| Release | Harness API | Status | Migration |
| --- | --- | --- | --- |
| [`v1.1.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/releases/tag/v1.1.0) | `1.0.0` | Current | [Migrate to 1.1](../how-to/migrate-1.1.md) |
| [`v1.0.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/releases/tag/v1.0.0) | `1.0.0` | Compatible prior release | Update additively to `v1.1.0` |

The repository release version describes the delivered capability set. The
harness API version protects public skill names, flags, routes, configuration,
module ranges, handoffs, and artifact authority. Release `1.1.0` therefore adds
the executable control plane without forcing an API-major migration.

Run `skills/_shared/ai_sdlc_compatibility.py` from the installed release before
and after an update. Pin a release tag when reproducibility matters.
