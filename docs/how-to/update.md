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

Commit or preserve project work, read `.ai-sdlc/harness-install.json`, record
the installed inventory, and verify selected
helper imports before updating. A failing baseline makes post-update diagnosis
ambiguous.

```bash
PYTHON_BIN="${PYTHON_BIN:-python3}"
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
git status --short
"$PYTHON_BIN" .agents/skills/ai-sdlc-navigator/scripts/navigate.py --help
"$PYTHON_BIN" .agents/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help
```

## Consumer repository: repair or upgrade by exact reinstall

The canonical install removes the generated `skills-lock.json` because it
contains a machine-specific temporary path. Skills CLI `1.5.19` also reports
`No project skills to update` for this local-source mode, so `skills update` is
not a repair or upgrade mechanism here.

For a same-release repair, set `<TARGET-COMMIT>` to the revision already
recorded in `.ai-sdlc/harness-install.json`. For an upgrade, use the reviewed
immutable commit published for the target release and read its migration notes.
Then repeat the exact-fetch install with the same selected host and the same
selection mode. The following derives exact `--skill` arguments from the
previous managed inventory for an explicit subset; an all-skills install uses
the target release's full inventory:

```bash
TARGET_REV=<TARGET-COMMIT>
TARGET_TMP="$(mktemp -d)"
TARGET_SRC="$TARGET_TMP/ai-sdlc-harness"
test -f .ai-sdlc/harness-managed-skills.txt
cp .ai-sdlc/harness-managed-skills.txt "$TARGET_TMP/previous-managed-skills.txt"
git init "$TARGET_SRC"
git -C "$TARGET_SRC" remote add origin https://github.com/mikegorelikoff/ai-sdlc-harness.git
git -C "$TARGET_SRC" fetch --depth 1 origin "$TARGET_REV"
git -C "$TARGET_SRC" checkout --detach FETCH_HEAD
test "$(git -C "$TARGET_SRC" rev-parse HEAD)" = "$TARGET_REV"
SELECTION=$("$PYTHON_BIN" -c 'import json; print(json.load(open(".ai-sdlc/harness-install.json"))["selection"])')
if test "$SELECTION" = all-skills; then
  cp "$TARGET_SRC/config/ai-sdlc-managed-skills.txt" "$TARGET_TMP/target-managed-skills.txt"
else
  comm -12 "$TARGET_TMP/previous-managed-skills.txt" "$TARGET_SRC/config/ai-sdlc-managed-skills.txt" > "$TARGET_TMP/target-managed-skills.txt"
fi
grep -qx ai-sdlc-shared-runtime "$TARGET_TMP/target-managed-skills.txt"
printf '%s\n' "$TARGET_REV" > .ai-sdlc/harness-update-in-progress
set --
while IFS= read -r skill; do set -- "$@" --skill "$skill"; done < "$TARGET_TMP/target-managed-skills.txt"
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$TARGET_SRC" "$@" --agent codex -y
git status --short
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
comm -23 "$TARGET_TMP/previous-managed-skills.txt" "$TARGET_TMP/target-managed-skills.txt" > "$TARGET_TMP/retired-managed-skills.txt"
cat "$TARGET_TMP/retired-managed-skills.txt"
cp "$TARGET_TMP/retired-managed-skills.txt" .ai-sdlc/retired-managed-skills.txt
```

Stop here and review the printed retired-skill list. For every listed name,
compare `.agents/skills/<name>` with the prior installation revision. Remove a
directory only when it is confirmed to be an unmodified, harness-owned skill;
record every retained or removed item in the update review. Then finish the
upgrade:

```bash
cp "$TARGET_TMP/target-managed-skills.txt" .ai-sdlc/harness-managed-skills.txt
printf '{"schema":"ai-sdlc-install-record/v1","revision":"%s","skills_cli":"1.5.19","agent":"codex","selection":"%s","inventory":".ai-sdlc/harness-managed-skills.txt"}\n' "$TARGET_REV" "$SELECTION" > .ai-sdlc/harness-install.json
"$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
rm skills-lock.json
rm -rf "$TARGET_TMP"
rm .ai-sdlc/harness-update-in-progress
git status --short
```

If execution stops while `.ai-sdlc/harness-update-in-progress` exists, do not
continue normal work. Read its target revision, preserve `git status --short`,
and rerun this entire exact-fetch procedure for that same revision and prior
selection. The final install-record validator must pass and the marker must be
removed in the same reviewed change. If rerun is impossible, restore only the
installed and `.ai-sdlc` paths from the last accepted installation commit, run
the installed smoke, and confirm product specs/code are untouched.

Do not copy the placeholder literally. If the pilot uses another agent, replace
`codex` consistently. The explicit-subset path never silently expands scope:
newly published skills require a separate review and an intentional inventory
edit. A retired selected skill appears in `retired-managed-skills.txt`.

Review every added, changed, or removed installed file before acceptance. Team
and project artifacts are not installer-owned and must not be overwritten.
The saved `retired-managed-skills.txt` output is the sorted set of previously harness-managed skill
names absent from the target release. If it is non-empty, inspect each matching
`.agents/skills/<name>` against the prior installation commit and remove only
confirmed old harness-owned directories; the reinstall does not remove them.
Never remove a same-named directory whose ownership or local modification is
unclear. Record the disposition in the update commit before deleting the
temporary comparison directory in the final command block.
Re-run the inventory and portable helper checks. Commit the accepted update
alone so it can be audited, reverted, or bisected independently from product
behavior.

## Promote the same revision across environments

Use the project-scoped installation commit,
`.ai-sdlc/harness-install.json`, and
`.ai-sdlc/harness-managed-skills.txt` as the team baseline. In each
environment, fetch the recorded harness revision, use the same pinned Skills
CLI and explicit host, reinstall the recorded selection, validate the install
record, and compare the Git diff with the accepted baseline. Promote a new
revision through a dedicated update commit; do not let each workstation choose
“latest” independently.

Global installations are separate workstation state. Update them per host,
start a new host session, and verify with the global list command. They cannot
replace repository provenance or Continuous Integration (CI). When both scopes
exist, the committed project inventory is the repository's reviewed authority,
even if a host defines its own resolution precedence.

## Source checkout: release validation

Maintainers validate the full repository only from a clone of this source:

```bash
"$PYTHON_BIN" skills/_shared/ai_sdlc_compatibility.py --skip-git-audit --format toon
"$PYTHON_BIN" skills/_shared/test_all_skill_scripts.py
"$PYTHON_BIN" skills/_shared/test_each_skill_tests.py
"$PYTHON_BIN" skills/_shared/sync_installed_runtime.py --check
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

## Remove and verify cleanup

The portable baseline intentionally has no CLI lock, so uninstall through the
dedicated reviewed installation commit: revert that commit, or remove only the
tracked harness paths it added after comparing them with the commit. Never
delete the entire `.agents` tree when it also contains project-owned or other
provider content.

Preserve specifications, decisions, evidence, configuration, and product code.
The acceptance evidence is a reviewed Git diff showing removal of exactly the
skill directories named by the pre-removal
`.ai-sdlc/harness-managed-skills.txt` (44 only for an all-skills install) and
both portable record files, no unrelated path, and no empty installer-created
directory that the project does not own. Retain a reviewed copy of the managed
inventory with the removal commit or ticket so the ownership decision remains
auditable after the live record is removed.

Manual review is intentional. An installer cannot safely infer whether a
same-named directory is harness-owned, locally modified, linked for another
host, or project-owned. Automation may produce retired names and hashes; it
must not recursively delete paths without that ownership decision.
