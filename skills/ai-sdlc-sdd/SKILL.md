---
name: ai-sdlc-sdd
description: AI SDLC repository spec-driven development workflow. Use when Codex receives a medium or large feature, refactor, API change, architecture change, provider integration change, or any request that must follow requirements, design, test cases, QA planning, tasks, implementation, and validation.
---

# ai-sdlc-sdd: Spec Driven Development

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-sdd`
- Primary audience: Dev
- Supporting audience: BA, QA, PM
- Audience tags: Dev, BA, QA, PM
- SDLC stage: Repository SDD workflow
- Purpose: Create, update, validate, and enforce the AI SDLC five-file SDD package for medium and large changes before implementation expands.
- Output: Five-file SDD package, validation status, task alignment, and implementation handoff

### 0.1 Required Inputs

- Medium or large change request.
- Affected systems, APIs, packages, or artifacts.
- Existing spec folder or proposed feature name if available.

### 0.2 Clarification Rules

- Ask concise questions before finalizing when role, artifact, requirements, scope, audience, or constraints are unclear.
- If optional information is missing, mark it as `TBD`, `Not provided`, or `Assumption` instead of inventing it.
- Separate confirmed facts from assumptions and open questions.
- Do not proceed to downstream synthesis when a required upstream artifact or decision is missing.

### 0.3 Output Rules

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, repository, `specs-refiniment/<feature-name>/<file.md>` workspace, or user context.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.

### 0.4 Artifact Routing

- Use `specs/` only for developer implementation SDD packages and repo-governance artifacts.
- Do not place PM, BA, QA, Delivery, discovery, planning, refinement, or readiness outputs in `specs/`; those belong at `specs-refiniment/<feature-name>/<file.md>`.
- When consuming `specs-refiniment/<feature-name>/<file.md>`, treat it as upstream refinement context and create or update `specs/` only when implementation work is explicitly in scope.

## References

- Use `scripts/analyze_spec.py` when deterministic validation, planning, or formatting is required by the workflow.
- Use `scripts/check_checklist.py` when deterministic validation, planning, or formatting is required by the workflow.
- Use `scripts/check_clarify.py` when deterministic validation, planning, or formatting is required by the workflow.
- Use `scripts/resolve_active_spec.py` when deterministic validation, planning, or formatting is required by the workflow.
- Use `scripts/sdd_status.py` when deterministic validation, planning, or formatting is required by the workflow.
- Use `scripts/spec_helpers.py` when deterministic validation, planning, or formatting is required by the workflow.
- Use `scripts/test_sdd_workflow.py` only for validating helper behavior; do not load it for ordinary task execution.
- Use `scripts/test_validate_spec.py` only for validating helper behavior; do not load it for ordinary task execution.
- Use `scripts/validate_spec.py` when deterministic validation, planning, or formatting is required by the workflow.

## Purpose

Create, update, validate, and enforce the AI SDLC five-file SDD package for medium and large changes before implementation expands.

## Inputs

- Read `AGENTS.md` for change classification and repository workflow rules.
- Collect the user request, affected systems, and likely spec name.
- Search existing `specs/` folders for a matching active or historical spec.
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

9. Record implementation traceability, source artifact links, or documented no-ticket exceptions in `requirements.md`.
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

- Pass when the five-file package exists, required sections are populated, tasks match implementation, and the validator passes.
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
- Do not run broad validation by default; use `$ai-sdlc-validation` for command selection.
