---
name: ai-sdlc-asana-traceability
description: AI SDLC Asana traceability workflow. Use when Codex handles medium or large AI SDLC changes, creates or updates specs, prepares commit messages, or needs to find related Asana tickets by feature name, asset symbol, provider, endpoint, or user-provided task reference.
---

# AI SDLC Asana Traceability

## Purpose

Find, create, link, assign, and section-sync Asana tasks so medium and large AI SDLC changes remain traceable from spec to commit to review.

## Inputs

- Collect explicit task IDs or Asana URLs from the user or existing spec.
- Collect search terms: feature name, endpoint, provider, asset symbol, error text, workflow name, and short variants.
- Collect the active spec folder and current `requirements.md`.
- Collect whether the work is new, in progress, ready for code review, ready for test, released, or done.
- Use the `AI SDLC 2.0` project unless the user or existing ticket context indicates another project.

## Steps

1. Search Asana before implementation for medium and large work.
2. Search in this order:
   1. explicit task ID or URL
   2. exact feature, endpoint, provider, or asset symbol
   3. short variants and likely misspellings
   4. broader project terms
3. Use `search_objects` first for specific tasks.
4. Reuse an existing task only when its name, description, project, or context clearly matches the active change.
5. Create a new task when no existing task clearly matches and Asana tools are available.
6. Assign found or created active work to `me` unless the user names another assignee or the task clearly belongs to another owner.
7. Place current implementation work in `In progress`; place ready-for-review committed work in `Code review`.
8. Do not move completed, released, unrelated, or out-of-scope tasks unless the user explicitly requests it.
9. Insert the related task into `requirements.md`:

   ```md
   ## Related Asana Tickets

   - [Task name](https://app.asana.com/...) (`task_gid`)
   ```

10. Reference the same task in `design.md` when the ticket affects scope, rollout, risk, or validation.
11. Validate traceability:

   ```bash
   python3 .codex/skills/ai-sdlc-asana-traceability/scripts/check_traceability.py specs/NNN-feature-name
   ```

## Output Spec

Return this traceability report:

```text
Asana traceability:
- Search terms: exact terms used.
- Reused task: task_gid task_name URL | none.
- Created task: task_gid task_name URL | none.
- Assignment: assignee or skipped reason.
- Section sync: section name or skipped reason.
- Spec update: requirements.md updated | pending reason.
- Residual risk: none | concrete ambiguity or tool issue.
```

Quality gate:

- Pass when the spec contains a real Asana GID/URL or a documented no-ticket exception with searches and skip reason.
- Fail when a task is guessed from a weak search result, when no searches are recorded, or when task creation is skipped without explanation.

## Examples

Task creation body:

```md
Summary:
Upgrade repo-local Codex skill instructions so AI SDLC outputs are deterministic.

Description:
Current skill instructions vary in structure and edge-case handling, causing inconsistent agent outputs.

Proposed Changes:
Normalize every SKILL.md file and add a skill index.

Functional Requirements:
Every skill includes Purpose, Inputs, Steps, Output spec, Examples, Edge cases, and Scope boundary.

Expected Behavior:
A cold Codex session can apply each skill without additional context.

Acceptance Criteria:
Skill validation passes and the index lists all skills.
```

No-ticket exception:

```md
No related Asana ticket found.
Task creation skipped: Asana connector unavailable.
Searches performed:
- `codex skill instructions`
- `repo-local skills`
```

## Edge Cases

- Ask for clarification when two or more active tasks match the same feature with similar confidence.
- Reuse completed tasks only for historical traceability; create a new active task when new implementation work is required.
- Leave assignment unchanged when the task clearly belongs to another named owner.
- Report Asana tool failures and continue only when the spec records why traceability is incomplete.
- Do not create duplicate tasks when an exact active task already exists.

## Scope Boundary

- Do not post commit implementation comments; use `$ai-sdlc-asana-commit-comment`.
- Do not draft commit messages; use `$ai-sdlc-conventional-commit`.
- Do not decide implementation scope; use `$ai-sdlc-ba` and `$ai-sdlc-sdd`.
- Do not move tasks across projects unless the user or Asana context clearly authorizes the move.

## AI SDLC 2.0 Sections

- `Backlog`: `1213161266359939`
- `To do`: `1213161266359940`
- `On Hold`: `1213669404768992`
- `In progress`: `1213161266359941`
- `Code review`: `1213161266359949`
- `Ready for test`: `1213161266359950`
- `Testing`: `1213161266359951`
- `Ready for release`: `1213161266359953`
- `Released`: `1213161266359954`
- `Done`: `1213161266359955`
- `Out of Scope`: `1213776259909542`
- `Inbound`: `1214125643704563`
