---
name: ai-sdlc-working-backwards-discovery
description: Use when a user needs a staged working-backwards interview to clarify the customer problem, audience, value proposition, business case, MVP, requirements, risks, and success metrics before any PRFAQ is written. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
---

# ai-sdlc-working-backwards-discovery: Working Backwards Discovery

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-working-backwards-discovery`
- Primary audience: PM
- Supporting audience: BA, Delivery
- Audience tags: PM, BA
- SDLC stage: Discovery / initiative framing
- Purpose: Run the discovery interview that turns an initiative idea into a structured, business-grounded definition.
- Output: Structured discovery notes, clarified assumptions, open questions, and PRFAQ-ready facts

### 0.1 Required Inputs

- Initiative idea or product problem.
- Known customer, user, or stakeholder context.
- Business goal, constraint, or launch driver if available.

### 0.2 Clarification Rules

- Ask concise questions before finalizing when role, artifact, requirements, scope, audience, or constraints are unclear.
- If optional information is missing, mark it as `TBD`, `Not provided`, or `Assumption` instead of inventing it.
- Separate confirmed facts from assumptions and open questions.
- Do not proceed to downstream synthesis when a required upstream artifact or decision is missing.

### 0.2.1 Flow Mode Flags

- Support two explicit execution flags: `--quick-flow` and `--full-flow`.
- If both flags are supplied, `--full-flow` takes precedence because it is the stricter mode.
- `--quick-flow`: move fast, make high-quality progress with available context, avoid clarification questions unless continuing would create material product, security, compliance, data-loss, or irreversible implementation risk.
- In `--quick-flow`, use documented assumptions, recommended defaults, existing repository patterns, and the nearest available artifact evidence; record important assumptions and decisions in `decision-log.md`.
- In `--quick-flow`, run only focused checks that are directly relevant, cheap, and likely to catch regressions for the requested work; report any skipped broader checks as residual risk.
- `--full-flow`: ask concise clarification questions when inputs, scope, ownership, acceptance criteria, or decisions are unclear; do not silently assume material requirements.
- In `--full-flow`, verify upstream and downstream artifacts, decision-log entries, traceability links, acceptance criteria, and validation evidence before finalizing.
- In `--full-flow`, run or recommend the skill-appropriate gates, reviews, scripts, and validation commands needed for end-to-end confidence; document any blocked verification explicitly.
- When neither flag is supplied, follow the skill default rules and choose the least risky behavior for the request size and domain.

### 0.3 Output Rules

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, `specs-refiniment/<feature-name>/<file.md>` workspace, stakeholder context, or user-provided source material.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.

### 0.4 Artifact Routing

- Maintain a feature decision log whenever this skill records, resolves, changes, or depends on a product, delivery, QA, security, validation, branching, implementation, or rollout decision.
- For PM, BA, QA, Delivery, discovery, planning, refinement, and readiness work, write decisions to `specs-refiniment/<feature-name>/decision-log.md`.
- For developer implementation SDD work, write decisions to `specs/<feature-name>/decision-log.md`.
- Each decision-log entry must include date, decision, context or evidence, options considered when relevant, owner, status, and links to affected artifacts, tasks, tests, or validation evidence.
- Use this exact decision-log structure:

  ```markdown
  # Decision Log

  | ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | DEC-001 | YYYY-MM-DD | proposed / accepted / superseded / rejected | role or name | concise decision | source facts, artifact links, or evidence | option A; option B; recommended default | affected docs, tasks, code, tests, or rollout notes | requirement IDs, test IDs, validation commands, PRs, commits, or tickets |
  ```

- When writing or updating files, place PM, BA, QA, Delivery, discovery, planning, refinement, and readiness artifacts at `specs-refiniment/<feature-name>/<file.md>`.
- Use the path pattern `specs-refiniment/<feature-name>/<file.md>`; choose a stable feature slug when known, otherwise use `tbd-<short-topic>` for `<feature-name>`.
- Do not write this skill's output into `specs/`; that folder is reserved for developer implementation SDD artifacts.
- If the user explicitly asks to convert a refined artifact into developer implementation work, hand off to `$ai-sdlc-sdd`.

## 0.5 Feature State Machine

- Maintain feature lifecycle state in TOON at `specs-refiniment/<feature-name>/state.toon` for refinement work and `specs/<feature-name>/state.toon` for implementation work.
- Before executing this skill for a feature, check the state machine with `python3 skills/_shared/state_machine.py check --feature <feature-name> --skill <this-skill-name> --workspace <refinement|implementation> --quick-flow|--full-flow`.
- When this skill starts durable work, mark it in progress with `begin`; when the skill's required artifact or review is complete, mark it done with `complete` and include `--artifacts <path>` plus `--decision-ref DEC-###` when a decision was involved.
- In `--full-flow`, do not proceed when predecessor stages are incomplete, another lifecycle skill is active, or the state file reports a blocker.
- In `--quick-flow`, a predecessor skip is allowed only when continuing is low risk and the command includes `--assumption "..."` or `--decision-ref DEC-###`; record the same assumption or decision in `decision-log.md`.
- Use `python3 skills/_shared/state_machine.py status --feature <feature-name> --workspace <refinement|implementation> --format toon` to emit compact LLM-readable state before choosing the next skill.
- The state machine is feature-scoped: do not reuse a `state.toon` across unrelated feature folders.

## 0.6 Artifact Metadata And Metatags

- Every Markdown artifact generated or updated by this skill must start with an `artifact_metadata` YAML frontmatter block before the first visible heading.
- Use schema `ai-sdlc-artifact-metadata/v1` and keep these fields current: `feature`, `artifact`, `path`, `workspace`, `skill`, `flow_mode`, `state_file`, `decision_log`, `status`, `owner`, `created_at`, `updated_at`, `trace_ids`, `related_artifacts`, `validation`, and `metatags`.
- `metatags` must include at minimum `ai-sdlc`, the workspace (`refinement` or `implementation`), this skill name, the artifact type or filename stem, and a lifecycle/status tag such as `draft`, `review`, `approved`, or `validated`.
- When `--quick-flow` is active, set `flow_mode: quick`, keep assumptions visible in the body, and add tags for major defaults or unresolved risk only when they help retrieval.
- When `--full-flow` is active, set `flow_mode: full`, keep blockers and validation evidence reflected in `status`, `validation`, `trace_ids`, and `related_artifacts`.
- Update metadata whenever the artifact path, status, owner, trace links, validation evidence, related artifacts, or decision references change.
- Metadata is an index for routing, retrieval, and traceability; it does not replace the artifact body, `decision-log.md`, or `state.toon`.

## 0.7 Specs Index

- Before searching across feature folders, inspect the compact LLM index first: `specs-refiniment/specs-index.toon` for refinement work or `specs/specs-index.toon` for implementation work.
- Use the human-readable index at `specs-refiniment/specs-index.md` or `specs/specs-index.md` when reporting feature coverage, artifact inventory, or handoff status to people.
- After this skill creates or materially updates an artifact, refresh the matching workspace index with `python3 skills/_shared/ai_sdlc_specs_index.py --workspace <refinement|implementation> --quick-flow|--full-flow`.
- In `--quick-flow`, rely on `specs-index.toon` to choose the smallest relevant artifact set before opening files.
- In `--full-flow`, verify the updated artifact appears in both `specs-index.toon` and `specs-index.md` before final handoff.
- The specs index summarizes artifact metadata and state; it does not replace reading the selected source artifacts when details, approvals, or validation evidence matter.

## References

- Use `scripts/discovery_interview_plan.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/interview-framework.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- Run `scripts/discovery_interview_plan.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied.
- Quick flow analysis: `python3 skills/ai-sdlc-working-backwards-discovery/scripts/discovery_interview_plan.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-working-backwards-discovery/scripts/discovery_interview_plan.py --feature <feature-name> --full-flow <input.md>...`
- To emit the canonical artifact skeleton and decision-log row without writing files, add `--emit-template --emit-decision-log-entry`.
- To create the routed artifact and `decision-log.md`, add `--write`; then review and fill the generated TBD fields before final output.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Run the discovery interview that turns an initiative idea into a structured, business-grounded definition.

## Use When

- The user wants a PRFAQ but the initiative is still fuzzy.
- The user needs help clarifying customer pain, target audience, business goals, requirements, and risks.
- The user wants a critical product partner who will challenge vague statements.

## Do Not Use When

- The initiative already has a validated, clear requirements package and only needs final document drafting.
- The task is technical implementation planning without business discovery.

## Workflow

1. Start at Stage 1 initiative context.
2. Ask a maximum of 5 to 7 questions at a time.
3. After every answer, summarize facts, assumptions, contradictions, and open questions.
4. Challenge vague wording until it becomes measurable, observable, or testable.
5. Stay in the current stage until the clarity bar is met.
6. Do not hand off to synthesis until the discovery minimums are present.

## Interview Rules

- Ask for real examples and current workarounds.
- Separate facts from assumptions and hypotheses.
- Keep decisions made distinct from decisions still needed.
- Push back if the MVP becomes a disguised full roadmap.
- Capture risks, dependencies, and out-of-scope items as they appear.

## Framework

Use `references/interview-framework.md` for the staged question structure.

## Completion Criteria

- Target customer is specific.
- Customer problem and current workaround are clear.
- Value proposition is explicit.
- Business objective and MVP are defined.
- Success metrics, risks, and dependencies are materially captured.
