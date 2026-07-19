---
title: Update safely
description: Upgrade the installed harness while protecting team configuration, user overrides, and public compatibility contracts.
---

# Update safely

This page separates two execution contexts. **Consumer repository** commands
update installed skills in a software project. **Source checkout** commands test
and publish the harness itself. Do not run source-only paths in a consumer
repository.

## Consumer repository: establish the baseline

Commit or preserve project work, record installed inventory, and verify selected
helper imports before updating. A failing baseline makes post-update diagnosis
ambiguous.

```bash
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
git status --short
python3 .agents/skills/ai-sdlc-navigator/scripts/navigate.py --help
python3 .agents/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help
```

## Consumer repository: preview and apply

Review the target release, migration, package origin, and expected changed skill
inventory. Then use the pinned Skills CLI from the consumer repository:

```bash
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 update
git status --short
```

Review every added, changed, or removed installed file before acceptance. Team
and project artifacts are not installer-owned and must not be overwritten.
Re-run the inventory and portable helper checks. Commit the accepted update
alone so it can be audited, reverted, or bisected independently from product
behavior.

## Source checkout: release validation

Maintainers validate the full repository only from a clone of this source:

```bash
python3 skills/_shared/ai_sdlc_compatibility.py --skip-git-audit --format toon
python3 skills/_shared/test_all_skill_scripts.py
python3 skills/_shared/test_each_skill_tests.py
python3 skills/_shared/sync_installed_runtime.py --check
```

Review renamed skills, flag changes, module API ranges, artifact routes,
migrations, deprecations, installed-runtime drift, and documentation. Protected
gates must not be weakened by an override that merely survived syntactically.

## Roll back

Stop new agent writes, capture the inventory and Git status, and restore the
last accepted project-scoped installation through reviewed Git changes or the
pinned prior release. Preserve product specs, decisions, state, evidence, and
the update failure record. Removing a skill is not permission to delete
artifacts it produced.
