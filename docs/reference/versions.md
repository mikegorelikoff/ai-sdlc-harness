---
title: Supported versions
description: Release, harness API, compatibility, and migration support matrix.
---

# Supported versions

| Release | Harness API | Status | Migration |
| --- | --- | --- | --- |
| [`v2.0.0-rc.1`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v2.0.0-rc.1) | `2.0.0` | Current prerelease; locally validated Codex installation/workflow; license and protected remote CI remain blockers | [Migrate to 2.0](../how-to/migrate-2.0.md); evaluate in a bounded pilot |
| [`v1.2.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0) | `1.0.0` | Published Git tag; known installed consumer-root defect blocks complete SDD/commit use | Historical comparison only; wait for a corrected reviewed release |
| [`v1.1.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.1.0) | `1.0.0` | Compatible prior tag | Remain on an accepted pin or wait for a corrected reviewed release; do not upgrade to blocked `v1.2.0` |
| [`v1.0.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.0.0) | `1.0.0` | Historical compatible tag | Evaluate `v1.1.0` under local policy, or wait for the corrected release |

Historical versions exist as Git tags without matching GitHub Release objects.
`v2.0.0-rc.1` is published as a GitHub prerelease. The repository version
describes the tagged capability set. The Harness API version protects public
skill names, flags, routes, configuration, module ranges, handoffs, artifact
authority, and major data contracts. Context pack v3 therefore requires the
Harness API `2.0.0` migration even though many operational surfaces remain
source compatible.

The full compatibility helper requires a **harness source checkout**, including
`compatibility/`, `modules/`, `concepts/`, and `skills/_shared`. Maintainers run:

```bash
python3 skills/_shared/ai_sdlc_compatibility.py --skip-git-audit --format toon
```

Consumer repositories instead verify the installed inventory and portable
helper entry points described in [Update safely](../how-to/update.md). Pin and
verify the immutable commit behind a reviewed release; a movable tag alone is
not reproducible identity.
