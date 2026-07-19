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

The full compatibility helper requires a **harness source checkout**, including
`compatibility/`, `modules/`, `concepts/`, and `skills/_shared`. Maintainers run:

```bash
python3 skills/_shared/ai_sdlc_compatibility.py --skip-git-audit --format toon
```

Consumer repositories instead verify the installed inventory and portable
helper entry points described in [Update safely](../how-to/update.md). Pin a
release tag when reproducibility matters.
