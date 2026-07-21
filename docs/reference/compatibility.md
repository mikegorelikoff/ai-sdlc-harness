---
title: Compatibility contract
description: Public surfaces protected across additive harness releases and the checks that enforce them.
---

## Protected surfaces

Release candidate `2.0.0-rc.1` implements Harness API `2.0.0` and protects the
public surface established after `v1.2.0`. Context pack v3 is the intentional
major change; skill names, flow flags, routes, and operating gates remain
mechanically protected.

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
command -v git
python3 skills/_shared/ai_sdlc_compatibility.py \
  --git-executable /absolute/reviewed/path/to/git --format toon
```

A compatible result reports the release, harness API version, complete protected
skill, flag, and route inventories, skill/module counts, and
`result: compatible`. The gate also audits the exact contiguous T001–T007
sequence from `v1.2.0`; an extra or missing release commit fails. Release notes must still explain meaningful additive
behavior; passing structure alone does not replace human review.

The Git history audit has no implicit executable lookup. Review the path printed
by `command -v git` and pass that absolute system path. Use
`--skip-git-audit` for structure-only checks that intentionally do not inspect
release history.
