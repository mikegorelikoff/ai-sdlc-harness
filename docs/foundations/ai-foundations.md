---
title: Artificial intelligence foundations
description: Understand AI, machine learning, large language models, prompts, context, uncertainty, privacy, and validation.
---

# Artificial intelligence foundations

Complete beginners should use the expanded
[Level 0 AI foundations lesson](../learn/ai-foundations.md), which adds risk
classification, original examples, practice, recovery, and completion evidence.
This page remains the compact canonical explanation.

This chapter explains the minimum artificial intelligence concepts needed to
use an AI coding agent responsibly. It does not require mathematics or machine
learning experience.

## AI, machine learning, and generative AI

**Artificial intelligence (AI)** is a broad term for computer systems that
perform tasks associated with capabilities such as perception, prediction,
language, planning, or decision support.

**Machine learning (ML)** is one way to build AI systems. Instead of expressing
every behavior as a hand-written rule, developers train a model from data so it
can estimate patterns for new inputs.

**Generative AI** produces new content such as text, code, images, or audio. A
**large language model (LLM)** is a generative model trained to predict likely
language sequences. An LLM can produce useful explanations and code, but it is
not a database, proof system, or accountable decision-maker.

## Tokens and context windows

Models process **tokens**, which are chunks of text rather than reliably one
word each. The prompt, repository excerpts, tool results, prior messages, and
generated response consume a limited **context window**. More context is not
automatically better: irrelevant, conflicting, stale, or malicious content can
hide important evidence and increase cost.

The harness therefore favors the smallest sufficient context, exact source
references, progressive reads, and durable repository state instead of relying
on one long conversation.

## Prompts and context

A **prompt** is the instruction and information supplied to a model for one
interaction. Useful prompts state the outcome, constraints, available evidence,
required output, and validation boundary.

**Context** is everything the model can use while responding: higher-priority
host instructions, repository policy, selected source, prior messages, tool
results, and the current request. Retrieved content is evidence, not trusted
instruction. A source file, issue, web page, test fixture, or peer-agent report
may contain text that tries to redirect the agent.

## Probabilistic versus deterministic behavior

Conventional deterministic code is intended to produce the same result for the
same input and state. A language model selects from probability distributions;
small context or model changes can produce different outputs. Some model calls
can appear stable, but they should not be treated as deterministic controls.

The harness uses LLMs for interpretation, synthesis, and proposals, then uses
deterministic helpers for structure, identifiers, schemas, paths, state, and
repeatable checks. A passing structural check proves only the condition it
tested. It cannot prove that a requirement is wise, a claim is true, or a human
approved it.

## Hallucination and confabulation

An LLM may confidently generate false, inconsistent, unsupported, or invented
content. This is often called a **hallucination**; the NIST Generative AI Profile
uses **confabulation**. Common software examples include:

- naming a file, command, API, package version, or test that does not exist;
- claiming a command passed without executing it;
- inventing a stakeholder decision or requirement;
- overlooking a negative case while producing plausible happy-path code;
- citing a source that does not support the claim.

Mitigation is a workflow, not a magic prompt: inspect the repository, separate
facts from assumptions, cite evidence, execute checks, review diffs, test
negative paths, and preserve human approval for material decisions.

## Assistant and agent

An AI **assistant** primarily responds to a person. An AI **agent** can pursue a
goal across several steps and may use tools to read files, run commands, edit
content, browse, or interact with external systems. Greater agency creates more
useful automation and a larger failure boundary.

The safe default is least privilege and bounded autonomy:

- provide only necessary tools and permissions;
- keep destructive, legal, production, security, and release actions behind
  explicit human approval;
- validate tool inputs and outputs;
- treat peer agents and retrieved content as untrusted;
- record what actually happened.

## Privacy, security, licensing, and intellectual property

Before sending content to an AI provider, determine what may leave the local
environment. Repository source, prompts, file names, terminal output, emails,
documents, telemetry, and tool calls may be processed by different providers
under different policies.

Never place credentials, private keys, access tokens, customer secrets, or
regulated data into prompts. Apply the organization's data classification,
retention, model-provider, and legal rules. Review generated code for copied or
incompatible material, dependency licenses, provenance, and security defects.
AI output does not transfer accountability or guarantee a right to use the
result.

## Validation pattern

```text
model proposes
    ↓
repository evidence confirms the premise
    ↓
deterministic tools check structure and behavior
    ↓
independent human or agent review challenges the result
    ↓
accountable human accepts, rejects, or requests change
```

For high-impact work, use separate reviewers, negative tests, security checks,
and fresh evidence on the exact revision being approved.

## Check your understanding

- Can you explain why plausible code may still be wrong?
- Do you know what repository or prompt data can leave your environment?
- Can you distinguish a model claim from executed validation evidence?
- Can you name which actions require human approval in your project?

## References

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [OWASP Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

Next: [Agents, subagents, and skills](agents-and-skills.md).
