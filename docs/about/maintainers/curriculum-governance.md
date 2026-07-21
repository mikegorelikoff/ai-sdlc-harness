---
title: "Learn curriculum governance"
description: "Architecture, quality, accessibility, validation, and lifecycle rules for maintaining Learn chapters."
---

# Learn curriculum governance

Learn is the curriculum layer. It teaches concepts, demonstrates decisions,
and directs practice. It does not take ownership from operational reference,
how-to, tutorial, explanation, installation, adoption, or skill pages.

## Curriculum architecture and ownership

The prerequisite sequence runs from artificial intelligence foundations to
prompting, context and verification, agents, independent review, AI-assisted
software delivery, harness operation, guided practice, and role application.
`docs/start.md` is the learning hub and remains at `/start/`. The `Learn`
subtree in `mkdocs.yml` is the only machine-readable curriculum inventory.

Keep canonical ownership explicit:

- skill behavior stays in skill reference pages;
- exact commands stay in how-to or reference pages;
- the glossary owns canonical terminology;
- `skills-by-role` owns task-to-skill discovery;
- Evidence Council and Quality Lenses keep their canonical contracts;
- installation stays in onboarding and installation guidance;
- adoption stays under Adopt;
- operational execution stays under Use.

A lesson may summarize, contrast, and demonstrate those contracts. It must link
to the owner and must not paste a complete contract to gain tokens.

## Learn page contract and depth

Every human-authored page listed under Learn follows the required front matter
and visible learner sections enforced by `learning_structure.py`. Objectives
use **Can explain**, **Can do**, and **Can prove**. Practice states permitted and
prohibited actions, produces an artifact, defines verification, and provides a
recovery path. Answers are collapsible but must explain reasoning.

`learning_tokens.py` removes YAML front matter and non-rendered maintainer HTML
comments, then measures visible Markdown with the pinned `tiktoken`
`o200k_base` encoding. The inclusive range is 6,000 to 8,000 tokens. Draft near
6,800 to 7,400 to leave editing margin.

Run Learn validation inside the pinned documentation environment described in
the [validation reference](../../reference/validation.md). A missing `tiktoken`
import is an environment failure, not permission to bypass token validation or
replace it with an approximation.

Token validity is necessary, not sufficient. Reject repeated definitions,
restated advice, pasted glossary entries, duplicated contracts, raw model
output, irrelevant history, unnecessary vendor comparison, and examples that
teach nothing new. Do not add a standalone page that cannot justify 6,000
useful tokens; consolidate its distinct material into the nearest canonical
chapter. Split a page only when each resulting chapter has a distinct outcome,
prerequisite, practice artifact, and evidence contract.

## Long-page usability and accessibility

Open with a concise summary and visible contents. Use descriptive, stable,
sentence-case headings without skipped levels. Keep paragraphs short. Put an
example beside the concept it demonstrates. Use collapsible detail for optional
depth, not essential instructions. Introduce tables in prose, keep them simple,
and avoid wide cells. Use meaningful links, useful image alternatives, and a
text cue for every state; never rely on color alone.

Review with keyboard and narrow-screen reading in mind. Decorative images add
maintenance and accessibility burden and should be omitted. Validate rendered
anchors after source validation because a Markdown link can exist while its
fragment is wrong.

## Add, merge, split, deprecate, or reorder a module

To add a module, record its missing competency, audience, prerequisites,
observable outcome, practice artifact, canonical owner, source use, and why an
existing chapter cannot hold it. Add navigation, reciprocal links, source
records, tests, and reviewer scope in the same change.

Merge overlapping modules when their outcomes, examples, and evidence are not
meaningfully distinct. Preserve public paths with an already tested redirect
mechanism; otherwise retain a concise compatibility page outside Learn. Split a
module when navigation or cognitive load harms use, not merely because it is
long. Both new pages must pass the depth and ownership tests.

For deprecation, identify inbound links, replacement material, release timing,
and responsible owner. Do not silently remove a public page. To change learning
order, update prerequisites, previous and next links, hub diagnostics, expected
levels, tests, and role fast lanes. A preference for a different outline is not
enough; show learner evidence or a prerequisite defect.

## Source research and freshness

Follow [Source reuse and adaptation](source-reuse-and-adaptation.md). Use sparse,
material sources rather than a decorative bibliography. Recheck source dates,
licenses, and pins before publication. Vendor documentation validates current
vendor behavior only; it never becomes a portable harness promise.

## Multi-role review

After the first complete, green implementation, freeze one bounded diff and
give it to independent, read-only reviewers. They report evidence, severity,
classification, confidence, accountable owner, provenance fields, and status.
The parent agent owns edits. Preserve disagreements and decide from evidence
and canonical authority, never reviewer count.

Re-run the New Learner, Documentation Maintainer, Source Provenance, and Depth
and Anti-padding reviewers after corrections. Reviewer agreement is evidence,
not approval. The repository owner retains publication authority.

## Validation before publication

Run the catalog check, source validation, standalone token report, complete
documentation tests, strict MkDocs build, rendered validation, compatibility
check, and supported installation smoke test. Record exact command outcomes.
Do not weaken a check to accommodate content. Do not report an environment-
blocked check as passing. Keep generated `site/` output untracked.

The [documentation validation reference](../../reference/validation.md) owns the
repository-wide command inventory. This page owns only the additional Learn
curriculum policy.
