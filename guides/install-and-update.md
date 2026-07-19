# Install, Update, And Rollback

## Compatibility Baseline

Release `1.1.0` uses harness API `1.0.0`, configuration schema
`ai-sdlc-config/v1`, module schema `ai-sdlc-module/v1`, canonical feature roots
`specs-refiniment/<feature>` and `specs/<feature>`, and machine records under
`_ai_sdlc`. Python 3.10 is the minimum runtime; CI also validates Python 3.13.
Release `1.1.0` is additive over `1.0.0`: existing skill names, Markdown
authority, flow flags, state paths, configuration, and module contracts remain
valid. New control-plane commands are TOON-first; JSON remains available only
where a schema, external integration, recovery record, or JSONL journal needs it.

Before install or update, run the repository compatibility validator:

```bash
python3 skills/_shared/ai_sdlc_compatibility.py --skip-git-audit --format toon
```

## Install

Install every core and optional skill:

```bash
npx skills add mikegorelikoff/ai-sdlc-harness -g --all
```

Install a specific core or optional capability:

```bash
npx skills add mikegorelikoff/ai-sdlc-harness/skills/ai-sdlc-navigator -g
npx skills add mikegorelikoff/ai-sdlc-harness/skills/ai-sdlc-architecture -g
```

`--all` includes optional capabilities. A minimal installation selects only
skills owned by `modules/core/module.json`; optional module manifests never
become core dependencies.

## Update

1. Preserve repository-local team config, feature artifacts, decision logs,
   and `_ai_sdlc/state.toon` files; never overwrite them with package defaults.
2. Review changes to `compatibility/baseline-v1.json`, config schema, module API,
   canonical routes, and migration notes.
3. Update or reinstall the selected skills with the same Skills CLI source used
   for installation.
4. Resolve base/team/user configuration with `ai_sdlc_config.py`; weakening a
   protected gate must fail.
5. Run module discovery and the compatibility validator.
6. Run project-context drift checks and feature status gates before resuming work.

Existing skill names, quick/full flags, state paths, artifact routes, config
schema, and module contracts remain stable within harness API `1.x`. A future
breaking release must publish a new baseline and migration path.

For the exact additive steps, see the public
[1.1 migration guide](../docs/how-to/migrate-1.1.md).

## Rollback

1. Reinstall the previously pinned repository revision or release source.
2. Restore only package-owned skill files; do not roll back feature artifacts,
   decisions, state, team config, or user config automatically.
3. Run the previous release compatibility validator and module discovery.
4. If new artifacts use an unsupported schema, preserve them and run a documented
   migration; do not delete or silently rewrite them.
5. Record any material recovery choice in the feature decision log.

Rollback is blocked when canonical and legacy records diverge or when the older
release cannot read current feature state safely.
