---
title: Your first 30 minutes
description: Verify installation, learn the invocation model, inspect a real request, and stop at the first human checkpoint.
---

# Your first 30 minutes

Use a disposable branch or low-risk repository. The goal is not to ship code in
30 minutes; it is to prove that the agent can discover the harness, ground a
recommendation, explain its authority, and leave a usable handoff.

## Minute 0–5: verify the environment

!!! terminal "Run in terminal — consumer repository"

    ```bash
    git status --short
    python3 --version
    DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
    ```

Expected: a clean or understood Git tree, Python 3.10+, and installed AI SDLC
skills for the agent you are about to use.

## Minute 5–10: choose one real request

Pick a request with a clear outcome and low blast radius, such as a health
endpoint, validation message, small read-only report, or focused test gap. Avoid
authentication, money movement, destructive migrations, production access, or
cross-service redesign for this first session.

Write down:

- the desired outcome;
- who cares about it;
- what must not change;
- known risk or uncertainty;
- what evidence would make you comfortable continuing.

## Minute 10–15: ask the navigator

!!! example "Tell your agent"

    ```text
    Use ai-sdlc-navigator --quick-flow.
    Read the repository without modifying it. For the request below, report:
    detected context and exact evidence anchors; one required next action;
    optional actions; blockers; reasons; invocation; expected artifact.

    Request: <your bounded request>
    Must not change: <your constraint>
    ```

!!! info "Agent does automatically"

    The navigator inventories installed skills and inspects branch, feature,
    state, specs, and repository signals. It should not create or edit artifacts.

Expected response: an `ai-sdlc-handoff/v1` result with evidence-backed routing.
If it presents a generic menu without explaining repository evidence, ask it to
show the anchors or stop.

## Minute 15–20: understand the recommendation

Ask four questions:

1. Is the recommended skill appropriate for the missing evidence?
2. Is it read-only or will it write a routed artifact?
3. Why is quick flow safe here, or why is full flow required?
4. What human decision or checkpoint occurs before code or a protected mutation?

Use the [glossary](../foundations/glossary.md) and
[responsibility model](../foundations/responsibilities.md) rather than guessing.

## Minute 20–25: run one bounded skill

!!! example "Tell your agent"

    ```text
    Use <recommended-skill> --quick-flow.
    Follow the navigator handoff. Before writing anything, state the inputs,
    target path, authority boundary, expected output, and validation command.
    Stop if a material decision or permission is missing.
    ```

The exact skill depends on the request. It may create context, a small SDD, a
QA gap report, a validation plan, or a review. The agent should use its packaged
helpers automatically and return the common handoff.

## Minute 25–30: inspect and stop

!!! terminal "Run in terminal"

    ```bash
    git status --short
    git diff --check
    ```

!!! warning "Human checkpoint"

    Review every created or changed file. Confirm the artifact belongs at its
    documented route, assumptions are visible, no secret or unrelated file was
    included, and the validation result matches the claim. Do not continue to
    implementation merely because the agent suggests a next command.

You are ready for the [first feature tutorial](../tutorials/first-feature.md)
when you can distinguish agent instructions from terminal commands and explain
what evidence the first skill added.
