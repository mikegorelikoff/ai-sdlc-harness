# Change Set Contract

## Authority

A change workspace is non-authoritative proposal evidence. Canonical target
files, their owning lifecycle artifacts, accepted decisions, organization
policy, and Git history retain authority. Creation and validation never imply
approval.

## Required shape

```text
changes/<change-id>/
  proposal.md
  design.md
  tasks.md
  deltas/index.md
  evidence/index.md
  _ai_sdlc/change-set.json
  _ai_sdlc/change-set.toon
```

The ID uses lowercase letters, digits, and single hyphens. Targets use
repository-relative POSIX paths, contain no empty, dot, or parent segments, and
cannot point into `changes/`.

## Intake lifecycle

1. Emit the proposed record without writes.
2. Create the complete workspace atomically.
3. Review and update human proposal content.
4. Validate structure and fingerprint.
5. Author requirement deltas in the later delta stage.

## Safety invariants

- Refuse an existing destination.
- Do not read or write target contents during creation.
- Sort and deduplicate targets before fingerprinting.
- Write every artifact inside a temporary sibling directory and rename the
  directory only after validation succeeds.
- Treat `_ai_sdlc/change-set.{toon,json}` as complete projections of the human proposal, not
  permission to alter canonical truth.
- Require a later preview, policy gate, approval, and atomic apply workflow for
  any authoritative mutation.

## Required proposal headings

- Goal
- Motivation
- Scope
- Out of Scope
- Canonical Targets
- Authority And Approval
- Assumptions And Open Questions

Design and tasks may remain explicitly pending at intake, but their files and
metadata must exist so later workflows have stable routes.
