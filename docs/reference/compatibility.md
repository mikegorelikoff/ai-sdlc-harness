---
title: Compatibility contract
description: Public surfaces protected across additive harness releases and the checks that enforce them.
---

## Protected surfaces

- Installed skill names and package identity.
- Stable `--quick-flow` and `--full-flow` support.
- Canonical refinement and implementation artifact routes.
- Feature state and machine plan locations.
- Configuration schema and protected gate semantics.
- Module manifest schema and harness API range behavior.
- Required compatibility baseline inventory.

## Additive evolution

New skills, optional modules, fields, and documentation may be added when old consumers continue to work. Renames, removals, authority changes, or required new fields are breaking unless a migration and version contract explicitly handles them.

## Mechanical gate

```bash
python3 skills/_shared/ai_sdlc_compatibility.py --format toon
```

A compatible result reports the release, harness API version, skill/module counts, and `result: compatible`. Release notes must still explain meaningful additive behavior; passing structure alone does not replace human review.
