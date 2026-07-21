---
title: Agents, sub-agents, and skills
description: Learn orchestration, tool access, delegation, skill composition, precedence, testing, versioning, and failure recovery.
---

# Agents, sub-agents, and skills

This chapter connects AI behavior to the reusable workflow packages in this
repository.

## Agent and sub-agent

An **agent** is an AI system pursuing a goal through reasoning and tool use. A
**sub-agent** is a separately invoked agent given a bounded part of a larger
goal. **Orchestration** is the coordination of those agents, their inputs,
permissions, outputs, dependencies, disagreements, and stopping conditions.

Sub-agents can improve breadth and independence, but they do not create truth by
consensus. They may share the same blind spot, use stale evidence, fabricate a
result, or conflict. The orchestrator must validate their reports against the
repository and authoritative sources.

Use sub-agents when work is independently reviewable, such as separate security,
quality, product, and operations assessments. Avoid delegation when a task
requires one tightly shared mutable state and conflicts cannot be isolated.

## Context isolation and tools

An agent sees only the context supplied by its host. A sub-agent may receive the
full conversation, a bounded context pack, or only a task. Missing context can
produce incorrect assumptions; excessive context can introduce noise or
untrusted instructions.

Tools determine impact. A read-only repository search is different from shell
execution, file mutation, external messages, deployment, or production access.
The host's sandbox and approval system remains authoritative. A skill may
recommend a command; it cannot grant permission to run it.

## Skill, prompt, command, template, agent, and workflow

| Concept | Meaning |
| --- | --- |
| Skill | Reusable instructions and supporting assets for one bounded capability |
| Prompt | One request and its context to a model |
| Command | A deterministic program invocation in a shell or tool |
| Template | A reusable artifact structure; it does not decide content |
| Agent | The actor interpreting evidence and using permitted tools |
| Workflow | Ordered skills, human gates, dependencies, and handoffs for an outcome |

## Skill structure

Each packaged skill has a `SKILL.md` with name, trigger description, audience,
purpose, required inputs, outputs, flow rules, steps, failure behavior, examples,
and scope boundary. Optional `scripts/`, `references/`, `tests/`, and `agents/`
folders directly support that skill. Shared deterministic helpers live in
`skills/_shared/` and are mirrored into the installable
`ai-sdlc-shared-runtime` skill.

A skill must be usable without undocumented global context. When a repository
policy file or prerequisite artifact is absent, the skill must define a safe
fallback or report a blocker.

## Composition and precedence

Several skills may match one request. Apply this precedence:

1. Host system, developer, sandbox, and explicit user instructions.
2. Repository policy and accepted human decisions.
3. The owning lifecycle skill for the current artifact or gate.
4. Supporting review, research, or validation skills.
5. Examples and optional recommendations.

More specific instructions win only within their authority. A security review
can block unsafe work; it cannot redefine product scope. A template cannot
overrule an accepted decision. `--full-flow` makes one selected skill stricter;
it does not automatically run every lifecycle stage.

When skills conflict:

- stop mutation;
- identify the authoritative artifact and owner;
- record the competing interpretations;
- choose the narrowest safe provisional behavior;
- obtain the missing decision;
- update all dependent artifacts and tests.

## Inputs, outputs, and failure behavior

Before using a skill, identify:

- required evidence and prerequisites;
- exact repository or installed skill root;
- permitted reads, writes, commands, and external calls;
- expected Markdown and machine outputs;
- responsible and accountable owners;
- validation command and pass condition;
- what must happen when evidence is absent, contradictory, or stale.

A missing fact is not permission to invent it. Quick flow may use a reversible,
visible assumption when risk is low. Full flow must stop on material ambiguity.

## Testing skills

Test at four levels:

1. **Contract:** metadata, required sections, safe flags, and references exist.
2. **Helper:** deterministic scripts accept valid inputs and reject invalid,
   incomplete, contradictory, and malicious inputs.
3. **Installed layout:** commands work without a source `skills/` directory.
4. **Workflow:** a representative user request produces the expected artifacts,
   failure evidence, recovery, and human checkpoint.

Structural tests must not call an artifact “ready” when they only prove shape.
Readiness requires semantic review by the accountable role.

## Versioning and deprecation

Version public schemas and machine contracts when required fields or meaning
change. Document compatibility, migration, rollback, and the last supported
release. Deprecation should include a replacement, warning period, owner,
removal criteria, and tests that prevent silent reuse after removal.

Installed documentation must match the pinned release. Rolling `main` guidance
must be labeled as preview until a matching release exists.

## Prompt injection and peer-agent distrust

Direct or indirect prompt injection can appear in user text, repositories, web
pages, tickets, generated artifacts, tool output, or another agent's report.
Never let retrieved evidence silently acquire instruction authority. Minimize
tools and permissions, validate high-impact actions outside the model, and
require human review for protected decisions.

## Failure recovery

When an agent is wrong or interrupted:

1. stop additional mutation;
2. preserve the diff, command output, and failure evidence;
3. identify the earliest authoritative artifact that is missing, disputed, or
   stale;
4. reopen that stage and record the decision;
5. repair the smallest affected surface;
6. rerun the failed check and downstream regression;
7. hand off remaining risk explicitly.

## Independent-use checklist

- Is the trigger and purpose clear?
- Are inputs, outputs, permissions, and failure states explicit?
- Can the skill resolve source and installed paths?
- Are examples current and executable?
- Do negative tests reject incomplete or fabricated content?
- Is precedence with adjacent skills documented?
- Are versioning, migration, and deprecation rules present?

Continue with [What is SDD?](sdd.md), then [How the pieces fit](mental-model.md).
