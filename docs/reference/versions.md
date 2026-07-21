---
title: Supported versions
description: Release, harness API, compatibility, and migration support matrix.
---

# Supported versions

| Release | Harness API | Status | Migration |
| --- | --- | --- | --- |
| [`v1.2.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0) | `1.0.0` | Published Git tag; known installed consumer-root defect blocks complete SDD/commit use | Historical comparison only; wait for a corrected reviewed release |
| [`v1.1.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.1.0) | `1.0.0` | Compatible prior tag | Remain on an accepted pin or wait for a corrected reviewed release; do not upgrade to blocked `v1.2.0` |
| [`v1.0.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.0.0) | `1.0.0` | Historical compatible tag | Evaluate `v1.1.0` under local policy, or wait for the corrected release |

These versions exist as Git tags; the GitHub Releases API returned no matching
release objects during this audit. The repository version describes the tagged capability set. The
harness API version protects public skill names, flags, routes, configuration,
module ranges, handoffs, and artifact authority. Release `1.2.0` therefore adds
guided onboarding and the portable runtime without forcing an API-major
migration.

The full compatibility helper requires a **harness source checkout**, including
`compatibility/`, `modules/`, `concepts/`, and `skills/_shared`. Maintainers run:

```bash
python3 skills/_shared/ai_sdlc_compatibility.py --skip-git-audit --format toon
```

Consumer repositories instead verify the installed inventory and portable
helper entry points described in [Update safely](../how-to/update.md). Pin and
verify the immutable commit behind a reviewed release; a movable tag alone is
not reproducible identity.
