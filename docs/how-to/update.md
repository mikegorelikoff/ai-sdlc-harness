---
title: Update safely
description: Upgrade the installed harness while protecting team configuration, user overrides, and public compatibility contracts.
---

## Establish the baseline

Commit or stash project work, record the installed harness version, and run compatibility validation before updating. A failing baseline makes post-update diagnosis ambiguous.

## Preview the update

Fetch the desired release in the harness source checkout. Use the installer update or merge mode described by the release, and review which base files will change. Team and user configuration layers must remain separate from installer-owned defaults.

## Apply and validate

Run the update, then execute:

```bash
python3 skills/_shared/ai_sdlc_compatibility.py --format toon
python3 skills/_shared/test_all_skill_scripts.py
```

Review renamed skills, flag changes, module API ranges, artifact routes, and migrations. Protected gates must not be weakened by an override that happened to survive syntactically.

## Commit the upgrade alone

Keep the harness update in its own commit so teams can audit, revert, or bisect it independently from product behavior.
