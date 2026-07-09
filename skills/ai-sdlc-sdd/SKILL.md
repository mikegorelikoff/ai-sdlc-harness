---
name: ai-sdlc-sdd
description: AI SDLC repository spec-driven development workflow. Use when Codex receives a medium or large feature, refactor, API change, architecture change, provider integration change, or any request that must follow requirements, design, test cases, QA planning, tasks, implementation, and validation.
---

# AI SDLC SDD

## Purpose

Create, update, validate, and enforce the AI SDLC five-file SDD package for medium and large changes before implementation expands.

## Inputs

- Read `AGENTS.md` for change classification and repository workflow rules.
- Collect the user request, affected systems, and likely spec name.
- Search existing `specs/` folders for a matching active or historical spec.
- Use `$ai-sdlc-asana-traceability` to find or create related Asana traceability before implementation.
- Use `$ai-sdlc-ba`, `$ai-sdlc-test-cases`, and `$ai-sdlc-qa` when those phases are incomplete.
- Read existing code only after the spec intent and affected surface are clear enough to avoid scope drift.

## Steps

1. Classify the change as small, medium, or large using `AGENTS.md`.
2. Use the small-change path only for typo fixes, tiny bug fixes, test-only fixes, log text changes, or other no-contract changes.
3. For medium or large work, find a matching `specs/NNN-short-name/` folder or create the next numbered folder.
4. Treat the full folder name as the canonical delivery ID; do not rely on the numeric prefix alone.
5. Add or update `specs/spec-registry.md` for tracked governance or delivery-critical work.
6. Ensure these files exist before implementation:
   - `requirements.md`
   - `design.md`
   - `test-cases.md`
   - `qa.md`
   - `tasks.md`
7. Write requirements before design; write design before implementation tasks.
8. Run the clarify gate after requirements are current:

   ```bash
   python3 .codex/skills/ai-sdlc-sdd/scripts/check_clarify.py specs/NNN-feature-name
   ```

9. Record Asana traceability or a documented no-ticket exception in `requirements.md`.
10. Derive test cases before writing tests.
11. Derive QA acceptance and regression scope before final validation.
12. Write task entries with explicit `Output:` and `Refs:` metadata for new or updated active specs.
13. Run the checklist gate before implementation tasks expand:

   ```bash
   python3 .codex/skills/ai-sdlc-sdd/scripts/check_checklist.py specs/NNN-feature-name
   ```

14. Implement only tasks described in `tasks.md`.
15. Mark task checkboxes complete only after code, docs, or validation actually satisfy the task.
16. Run the analyze gate before implementation handoff or commit prep:

   ```bash
   python3 .codex/skills/ai-sdlc-sdd/scripts/analyze_spec.py specs/NNN-feature-name
   ```

17. Validate the active spec:

   ```bash
   python3 .codex/skills/ai-sdlc-sdd/scripts/validate_spec.py specs/NNN-feature-name
   ```

18. Use workflow-state status when the next phase is unclear:

   ```bash
   python3 .codex/skills/ai-sdlc-sdd/scripts/sdd_status.py --spec specs/NNN-feature-name
   ```

19. Report compliance, completed tasks, validation, and open risks.

## Output Spec

Use this completion report:

```text
SDD compliance:
- Spec: specs/NNN-feature-name
- Change size: small | medium | large
- Asana: task_gid URL | documented no-ticket exception
- Requirements: updated | unchanged with reason
- Design: updated | unchanged with reason
- Test cases: updated | unchanged with reason
- QA: updated | unchanged with reason
- Tasks: completed task numbers and remaining task numbers
- Validation: command -> outcome
- Scope control: no drift | drift and spec update
- Residual risk: none | concrete issue
```

Quality gate:

- Pass when the five-file package exists, required sections are populated, Asana traceability is recorded, tasks match implementation, and the validator passes.
- Fail when code starts before missing spec artifacts are created, when implementation exceeds `tasks.md`, when the clarify/checklist/analyze gates fail, or when task checkboxes are marked complete without evidence.

## Examples

Spec folder shape:

```text
specs/177-codex-skill-instruction-upgrade/
  requirements.md
  design.md
  test-cases.md
  qa.md
  tasks.md
```

Completion report sample:

```text
SDD compliance:
- Spec: specs/177-codex-skill-instruction-upgrade
- Change size: medium
- Asana: 1215001164529861 https://app.asana.com/...
- Requirements: updated
- Design: updated
- Test cases: updated
- QA: updated
- Tasks: 1-10 completed
- Validation: python3 .codex/skills/ai-sdlc-sdd/scripts/validate_spec.py specs/177-codex-skill-instruction-upgrade -> passed
- Scope control: no drift
- Residual risk: none
```

Invalid counter-example:

```text
Implemented feature; will write spec later.
```

Reject this for medium and large work because the spec is the source of truth.

## Edge Cases

- Reuse an existing active spec when its requirements clearly match the user request.
- Create a new spec when an existing completed or archived spec is only historically related.
- Add `TODO(dm): exact question` when a required decision cannot be discovered and guessing would affect scope, contract, security, or rollout.
- Use `Assumptions`, `Open Questions`, and `Decision Status` sections in `requirements.md` for clarify-gate evidence.
- Update the spec first when code and spec conflict during an active change.
- Treat unlisted historical numbered specs as `unclassified` until `specs/spec-registry.md` says otherwise.
- Do not treat scaffolded historical `qa.md` or `test-cases.md` files with unresolved TODOs as validated evidence.

## Scope Boundary

- Do not replace BA, test-case, QA, review, security, validation, or commit-prep skills; route to them when their phase is needed.
- Do not implement major features without requirements, design, test cases, QA, and tasks.
- Do not create Asana tasks directly from this skill; use `$ai-sdlc-asana-traceability`.
- Do not run broad validation by default; use `$ai-sdlc-validation` for command selection.
