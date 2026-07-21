---
title: "Source reuse and adaptation"
description: "Maintainer policy for researching, transforming, attributing, and refreshing external learning sources."
---

# Source reuse and adaptation

The Learn curriculum is original repository documentation. External resources
help maintainers find missing concepts, verify current facts, and improve
teaching design. They are not templates. The operating rule is **adopt the
idea, not the wording**.

## Source classes

The machine-readable authority is
[`docs/_data/content_sources.yml`](../../_data/content_sources.yml). Each record
uses one of four classes:

- `internal-authority` defines harness behavior and must point to the canonical
  repository owner.
- `adaptable-with-verification` has a verified license that permits adaptation,
  but this project still prohibits one-to-one copying.
- `reference-only` may verify facts or reveal curriculum gaps. Do not adapt its
  distinctive prose, examples, diagrams, checklists, or structure.
- `unavailable-or-unclear` cannot inform published curriculum content.

Public availability is not permission. A repository-level license does not
automatically cover embedded media. A source with unclear ownership stays
unused until an individual rights check is complete.

## Required adaptation record

Before a source affects a page, record its canonical URL, exact Git revision or
review date, current license evidence, consulted sections, adopted concepts,
excluded material, destination pages, and reviewer. The adaptation summary
must explain all of the following:

1. the general idea selected;
2. why it belongs in this curriculum;
3. how it was translated into harness terminology;
4. which original harness example or exercise replaced the source example;
5. how the result differs in structure and wording;
6. what was deliberately not imported.

“Used as inspiration” does not pass review. Git sources require a release, tag,
or full commit. Web guidance requires an actual review date. Every Learn page
declares only the sources that materially informed that page and repeats the
transformation in its visible **Sources and adaptation notes** section.

## Review for similarity and provenance risk

The source-provenance reviewer compares the finished page with the consulted
material. The reviewer looks for sentence-by-sentence paraphrase, preserved
heading order, renamed examples, copied quiz logic, unattributed combinations,
and claims that the source does not support. This review identifies risk; it is
not legal approval.

If similarity is material, remove the affected passage and write again from the
harness learning objective and repository evidence. If a license or source
version cannot be verified, remove its influence and mark the record
`unavailable-or-unclear`. Add `THIRD_PARTY_NOTICES.md` only when actual reused
code, media, quotation, or a license condition requires it. A registry entry by
itself does not imply copied content.

## Freshness and change control

Recheck vendor behavior and security guidance before each material curriculum
release. Recheck other web sources at least annually or when a learner reports
a contradiction. A changed source does not automatically change harness
behavior. Repository-owned contracts remain authoritative.

Run the documentation validation suite after every source declaration change.
Unknown identifiers, missing dates, unpinned Git sources, unavailable sources,
and `adapted` use of a `reference-only` source fail validation.

## Related maintainer guidance

See [Curriculum governance](curriculum-governance.md) for module ownership,
page depth, accessibility, review, and publication gates. See the canonical
[Maintainer guide](../../maintainers/index.md) for repository-wide ownership.
