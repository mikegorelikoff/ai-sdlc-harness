# Apply Preview Contract

Apply preview is a read-only compilation of validated semantic deltas against
the current canonical target bytes.

## Outputs

- `_ai_sdlc/apply-preview.json` contains target before and after hashes,
  unified diffs, conflicts, stale references, reopen actions, required gates,
  authority limits, and the preview fingerprint.
- `apply-preview.md` renders the same review surface for people.

## Conflict rules

Block apply when a canonical requirement block is absent or ambiguous, a
rename targets an inline requirement without a distinct name boundary, or
another validated active change touches the same target and requirement ID.
Never guess which block or concurrent proposal should win.

## Impact and gates

Exact downstream references to modified, removed, or renamed IDs become stale
and require revalidation. Preview always requires current delta validation and
owner approval. It adds change-impact, cross-artifact, new-owner, and security
policy gates when evidence triggers them.

## Fingerprint

The preview fingerprint covers the current delta fingerprint, before and after
target hashes, diffs, conflicts, stale evidence, reopen actions, gates, and
authority. Any target, delta, or analysis drift invalidates a saved preview.
