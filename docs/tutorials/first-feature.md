---
title: Ship a first feature
description: Follow a runnable sample from clean project setup through installation, branch-first specification, implementation, real failure recovery, validation, and traceable commit evidence.
---

# Ship a first feature

This tutorial uses artificial intelligence (AI), Specification-driven
development (SDD), Windows Subsystem for Linux (WSL), and command-line
interface (CLI).

This tutorial adds a read-only `/health` route to a tiny dependency-free Python
service. It teaches the shortest complete evidence loop; the point is not the
endpoint but the ability to explain and verify every step without the original
chat.

`/health` is a web route used to report whether the tiny process is alive.
Hypertext Transfer Protocol (HTTP) `GET` means read that route; status `200`
means the request succeeded; `{"status": "ok"}` is the expected JavaScript
Object Notation (JSON) response body.

You need network access, Git, Python 3.10+, Node.js `>=22.20.0`, npm, and a
supported AI agent. The commands are written for Linux/macOS/WSL or Git Bash;
PowerShell users should use WSL for this end-to-end fixture. Every repository
created here is disposable.

## 0. Open the release-candidate source checkout

This tutorial validates `v2.0.0-rc.1`, including the documentation, security,
and workflow fixes that are not present in `v1.2.0`. Acquire the annotated tag
explicitly:

```bash
CANDIDATE_PARENT="$(mktemp -d)"
git clone https://github.com/mikegorelikoff/ai-sdlc-harness.git "$CANDIDATE_PARENT/ai-sdlc-harness"
cd "$CANDIDATE_PARENT/ai-sdlc-harness"
test "$(git remote get-url origin)" = "https://github.com/mikegorelikoff/ai-sdlc-harness.git"
git fetch --depth 1 origin refs/tags/v2.0.0-rc.1:refs/tags/v2.0.0-rc.1
git checkout --detach 'v2.0.0-rc.1^{commit}'
```

The captured commit below is evidence for the bytes exercised, not a signature
or permission grant. A contributor may instead open an already reviewed,
committed source checkout containing this page.
Capture the exact candidate revision only from a clean committed checkout so
the recorded revision identifies every installed byte. The Git checks below
fail on tracked, staged, or untracked candidate content:

!!! terminal "Linux/macOS/WSL/Git Bash"

    ```bash
    HARNESS_SRC="$(git rev-parse --show-toplevel)"
    HARNESS_REV="$(git -C "$HARNESS_SRC" rev-parse HEAD)"
    git -C "$HARNESS_SRC" diff --quiet
    git -C "$HARNESS_SRC" diff --cached --quiet
    test -z "$(git -C "$HARNESS_SRC" ls-files --others --exclude-standard)"
    test -f "$HARNESS_SRC/docs/tutorials/first-feature.md"
    TUTORIAL_ROOT="$(mktemp -d)"
    cd "$HARNESS_SRC"
    node --version  # expected: v22.20.0 or newer
    npm --version
    PYTHON_BIN="${PYTHON_BIN:-python3}"
    "$PYTHON_BIN" --version
    ```

If any clean-check command fails, stop and commit or discard the candidate
content through normal review before recording `HARNESS_REV`. If Node is older than `22.20.0`, stop and upgrade Node before invoking the
pinned Skills CLI. The CLI package declares that engine floor; changing the
Node version is safer than forcing installation with an unsupported runtime.
If Python is older than 3.10, stop as well; installation alone does not verify
the helper runtime. Windows users should perform the complete fixture in WSL.

## 1. Create a clean consumer and explicit base branch

!!! terminal "Run in terminal — harness source checkout (POSIX)"

    ```bash
    DEMO_PARENT="$TUTORIAL_ROOT"
    DEMO_ROOT="$DEMO_PARENT/ai-sdlc-health-demo"
    cp -R examples/onboarding-health-service "$DEMO_ROOT"
    cd "$DEMO_ROOT"
    git init
    git checkout -b dev
    git config --local user.name "AI SDLC Tutorial"
    git config --local user.email "tutorial@example.invalid"
    git config --local commit.gpgsign false
    git config --get user.name
    git config --get user.email
    printf '__pycache__/\n*.py[cod]\n' > .gitignore
    git add .gitignore README.md app.py test_app.py deliberate_unknown_route_regression.py.disabled
    git commit -m "chore: initialize health service fixture"
    "$PYTHON_BIN" -m unittest -v
    git status --short
    ```

Expected tests:

```text
test_unknown_path ... ok
test_version ... ok
Ran 2 tests ... OK
```

Expected tree:

```text
ai-sdlc-health-demo/
  .gitignore
  README.md
  app.py
  deliberate_unknown_route_regression.py.disabled
  test_app.py
```

The repository is on `dev` and clean. The `.disabled` file is not discovered by
`unittest`; it is used later to create deterministic failing evidence.

## 2. Install and commit the accepted baseline

Reuse the scope, telemetry, and trust rules from the
[canonical project-scoped installation](../how-to/install.md), but do **not**
rerun that guide's stable-source selection in this candidate exercise. Preserve
the `HARNESS_SRC` and `HARNESS_REV` captured in step 0, then inspect what the
installer adds.

!!! terminal "Run in terminal"

    ```bash
    test "$(git -C "$HARNESS_SRC" rev-parse HEAD)" = "$HARNESS_REV"
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 add "$HARNESS_SRC" --skill '*' --agent codex -y
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
    "$PYTHON_BIN" .agents/skills/ai-sdlc-navigator/scripts/navigate.py --help
    "$PYTHON_BIN" .agents/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help
    mkdir -p .ai-sdlc
    cp "$HARNESS_SRC/config/ai-sdlc-managed-skills.txt" .ai-sdlc/harness-managed-skills.txt
    printf '{"schema":"ai-sdlc-install-record/v1","revision":"%s","skills_cli":"1.5.19","agent":"codex","selection":"all-skills","inventory":".ai-sdlc/harness-managed-skills.txt"}\n' "$HARNESS_REV" > .ai-sdlc/harness-install.json
    "$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
    rm skills-lock.json
    git status --short
    ```

!!! warning "Human checkpoint"

    Review the installed diff and source identity. Continue only if changes are
    limited to `.agents/skills/` and the two portable harness records under
    `.ai-sdlc/`. The transient
    CLI lock contains an absolute temporary path and must be absent. Installed
    instructions run with the agent's authority; inventory is not a trust
    decision.

Commit the accepted installation before feature work. This keeps the later
branch gate clean and prevents package files from being mistaken for feature
scope.

!!! terminal "Run in terminal"

    ```bash
    git status --short
    git add .agents .ai-sdlc/harness-install.json .ai-sdlc/harness-managed-skills.txt
    git diff --cached --stat
    git commit -m "chore: install AI SDLC harness"
    git init --bare "$TUTORIAL_ROOT/health-origin.git"
    git remote add origin "$TUTORIAL_ROOT/health-origin.git"
    git push -u origin dev
    git status --short
    ```

Expected: the base is clean, `dev` tracks the disposable local origin, and
`git pull --ff-only` can be proven rather than assumed. A real project uses its
existing reviewed remote and never creates this fixture-only exception.

## 3. Ask for read-only routing

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-navigator --quick-flow.
    Do not modify the repository. Find the smallest safe workflow for:
    Implement GET /health behavior while preserving existing route behavior.
    The new route must return status 200 and {"status": "ok"}.
    The existing /version and unknown-path behavior must not change.
    Report evidence anchors, blockers, next_required, next_optional, commands,
    and expected artifacts.
    ```

!!! info "Agent does automatically"

    The navigator inspects project-scoped installed capabilities, Git state,
    feature state, and repository structure. It must not write a file.

The deterministic routing record uses its own schema:

```toon
schema: ai-sdlc-navigator/v1
branch: dev
installed_skill_count: 44
features: none
selected_feature: none
workspace: none
current_stage: none
active_skill: none
dirty_change_count: 0
flow_mode: quick

next_required[1]{skill,reason,command,expected_artifact}:
  ai-sdlc-branching,Repository-tracked specification and implementation work must not start on shared base branch dev.,Use $ai-sdlc-branching to create a task branch before SDD writes.,task branch

next_optional[0]{skill,reason,command,expected_artifact}:

blockers[0]{message}:
```

The agent's final workflow handoff is a separate valid contract:

```toon
schema: ai-sdlc-handoff/v1
result: complete
summary: Navigation selected the smallest implementation path.

blockers[0]{message}:

next_required[1]{skill,reason,command,expected_artifact}:
  ai-sdlc-branching,Repository-tracked work must start on a task branch.,Use ai-sdlc-branching --quick-flow for 001-health-endpoint.,feature/001-health-endpoint

next_optional[0]{skill,reason,command,expected_artifact}:
```

If the navigator reports `recommended skill is not installed`, stop: the
project-scoped inventory is incomplete. If it changes a file, inspect and
restore that unexpected mutation before continuing.

## 4. Create the task branch before SDD mutation

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-branching --quick-flow for feature 001-health-endpoint.
    Treat the fixture's local origin/dev as the documented disposable base.
    Verify the clean tree, checkout dev, pull --ff-only, and create
    feature/001-health-endpoint. Do not create a spec or edit code yet.
    ```

Expected branch evidence:

```text
Base branch: dev
Base refresh: pulled latest dev
Current branch: feature/001-health-endpoint
Dirty tree: clean
Next phase: SDD
```

!!! terminal "Run in terminal"

    ```bash
    git branch --show-current
    git status --short
    ```

Do not continue unless the branch is `feature/001-health-endpoint` and status is
empty. This is the branch-before-repository-mutation boundary.

## 5. Create the small SDD

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-sdd --quick-flow for feature 001-health-endpoint.
    Before code, create a minimal complete SDD with:
    - GET /health returns status 200 and {"status": "ok"};
    - /version and unknown paths retain current behavior;
    - no network, framework, authentication, persistence, or deployment work;
    - tests are derived before implementation;
    - one bounded implementation task and one focused commit.
    Show assumptions and stop on any material product decision.
    ```

!!! info "Agent does automatically"

    The SDD workflow assembles each artifact through its scaffold, runs clarify,
    checklist, plan, analyze, and validation gates, and updates derived indexes.

Expected tree addition:

```text
specs/001-health-endpoint/
  _ai_sdlc/
    plan.toon
    state.toon
  decision-log.md
  requirements.md
  design.md
  test-cases.md
  qa.md
  tasks.md
  plan.md
```

`AC` means acceptance criterion: observable behavior the owner can accept.
`TC` means test case: setup, action, and expected result used to verify it.
Representative trace:

```text
AC-001: GET /health returns 200 and {"status": "ok"}.
AC-002: Existing /version and unknown-path behavior remains unchanged.
TC-001 -> AC-001: call /health and compare exact status/body.
TC-002 -> AC-002: run existing regression tests.
T001 -> AC-001, AC-002, TC-001, TC-002: implement and validate the route.
```

!!! warning "Human checkpoint"

    Review acceptance before implementation. Confirm that health means process
    availability only; it does not claim dependency readiness. The agent must
    not silently expand this product/operations boundary.

## 6. Implement without closing the task yet

!!! example "Tell your agent"

    ```text
    Implement only T001 from specs/001-health-endpoint.
    Add the /health test first, preserve existing behavior, and run focused
    tests. Do not mark T001 complete yet: this tutorial will exercise an
    unexplained failing-evidence gate before final acceptance.
    Do not add a web framework or deployment configuration.
    ```

Expected behavior:

```python
>>> route("/health")
(200, {"status": "ok"})
```

Expected trusted suite at this point: three passing tests—the new health case
and both existing regressions.

## 7. Create real failing evidence and recover safely

This deliberate regression exercise activates an intentionally wrong test and
runs the complete suite. It proves that failure blocks acceptance and that
recovery removes only untrusted evidence.

!!! terminal "Run in terminal — non-zero is expected"

    ```bash
    cp deliberate_unknown_route_regression.py.disabled test_deliberate_unknown_route_regression.py
    "$PYTHON_BIN" -m unittest -v
    ```

Expected: four tests run, the deliberate test fails because it expects status
200 for `/missing`, and the real unknown-path test still expects and receives
404. The command exits non-zero.

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-validation --quick-flow for specs/001-health-endpoint.
    Diagnose the current failing suite before changing product code or evidence.
    Map the failed expectation to AC-002 and the authoritative regression test.
    Keep T001 incomplete until the trusted suite reruns successfully. Do not
    weaken AC-002, delete the real regression, or treat every failed assertion
    as proof of a product defect.
    ```

Correct diagnosis: the temporary test contradicts accepted AC-002. Remove only
that disposable probe and rerun trusted evidence.

!!! terminal "Run in terminal — exact safe repair"

    ```bash
    rm test_deliberate_unknown_route_regression.py
    "$PYTHON_BIN" -m unittest -v
    git status --short
    ```

Expected: three tests pass; the temporary file is gone; status contains only
the feature's SDD, `app.py`, and `test_app.py` changes.

!!! example "Tell your agent"

    ```text
    The trusted three-test rerun passed. Record exact evidence against AC-001,
    AC-002, TC-001, and TC-002; then check T001 in tasks.md. Regenerate plan.md
    and _ai_sdlc/plan.toon with the installed plan_links.py --write
    --quick-flow command and verify it with --check. Do not edit either plan
    projection directly or record the deliberately invalid probe as passing
    evidence.
    ```

## 8. Validate the real result

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-validation --quick-flow for specs/001-health-endpoint and the
    current diff. Write the reviewed argv plan below to
    specs/001-health-endpoint/_ai_sdlc/validation-plan.json, finalize
    validation.md with the intended AC/TC mapping and residual risks, execute
    the canonical runner, verify its receipt, and only then complete validation
    state. Do not substitute prose that merely says PASS.
    ```

Reviewed plan:

```json
{"schema":"ai-sdlc-validation-command-plan/v1","commands":[{"id":"V001","argv":["python3","-m","unittest","-v"],"trace_ids":["AC-001","AC-002","TC-001","TC-002"]},{"id":"V002","argv":["git","diff","--check"],"trace_ids":["AC-001","AC-002"]}]}
```

!!! terminal "Run in terminal"

    ```bash
    "$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/state_machine.py begin \
      --feature 001-health-endpoint --workspace implementation \
      --skill ai-sdlc-validation --quick-flow
    "$PYTHON_BIN" .agents/skills/ai-sdlc-validation/scripts/run_validation.py \
      --root . \
      --plan specs/001-health-endpoint/_ai_sdlc/validation-plan.json \
      --output specs/001-health-endpoint/_ai_sdlc/validation-receipt.json \
      --quick-flow
    "$PYTHON_BIN" .agents/skills/ai-sdlc-validation/scripts/run_validation.py \
      --root . \
      --plan specs/001-health-endpoint/_ai_sdlc/validation-plan.json \
      --output specs/001-health-endpoint/_ai_sdlc/validation-receipt.json \
      --verify --quick-flow
    "$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/state_machine.py complete \
      --feature 001-health-endpoint --workspace implementation \
      --skill ai-sdlc-validation \
      --artifacts specs/001-health-endpoint/validation.md --quick-flow
    git diff --check
    git status --short
    ```

Expected: both receipt commands have exit code zero, verification says the
receipt is current, validation state is `done`, and scope is limited to the
SDD, validation evidence, `app.py`, and `test_app.py`.

## 9. Prepare one traceable commit

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-commit-prep --quick-flow for
    specs/001-health-endpoint and task T001. Stage only related files, validate
    readiness, use a conventional commit with Spec, Task, and exact validation
    evidence, then report the final hash and working-tree status.
    ```

Expected subject:

```text
feat(health): add process health endpoint
```

A passing outcome is a clean tree and one commit from which another reviewer
can reconstruct intent → acceptance → test → implementation → evidence.

## 10. Open, review, and accept the increment

Follow [Open, review, and merge a change](../how-to/review-and-merge.md). In
this local fixture, inspect the commit rather than pushing to a real host. The
product owner (or delegated outcome owner) must confirm that `/health` means
process liveness and that the response matches AC-001; an independent engineer
must review the code and current three-test evidence. Agent self-review is not
acceptance. Preserve the disposition using
[Record product acceptance](../how-to/record-product-acceptance.md), including
the exact reviewed commit and AC/TC evidence. Because this decision necessarily
references the implementation commit, record it in a separate reviewed evidence
commit (or the protected pull-request decision system) before merge; do not
amend the already reviewed implementation commit and invalidate its hash.

Expected final evidence:

- the reviewed commit hash;
- AC-001 and AC-002 mapped to current passing output;
- no cache, installer surprise, or unrelated file in the commit;
- explicit product acceptance and reviewer disposition.

## 11. Clean up

!!! terminal "Run in terminal"

    ```bash
    cd /tmp
    rm -rf "$TUTORIAL_ROOT"
    if test -n "${CANDIDATE_PARENT:-}"; then rm -rf "$CANDIDATE_PARENT"; fi
    ```

The guarded second removal applies only when Step 0 created the public-site
candidate clone. Only remove these disposable paths. Never use cleanup commands
on a real consumer repository or its authoritative artifacts.
