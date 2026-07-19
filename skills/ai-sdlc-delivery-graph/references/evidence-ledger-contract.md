# Evidence Ledger And Freshness Contract

## Source records

Evidence producers write `ai-sdlc-evidence-source/v1` manifests below an
`evidence/` directory using the `.evidence.json` suffix. A manifest identifies
the evidence artifact, exact captured hash, lifecycle subjects, producer,
capture and optional expiry time, direct file dependencies, and upstream
evidence records. Repository-relative paths may not be absolute, traverse
parents, escape through symlinks, or target generated ledger output.

## Freshness

The ledger recalculates every artifact and dependency hash at `--as-of` time.
Missing bytes produce `missing`; changed bytes produce `stale`; elapsed expiry
produces `expired`. Any record depending on a non-fresh evidence record becomes
`stale` with `upstream-not-fresh`. Propagation iterates to a fixed point, so a
stale root is visible through every downstream evidence path.

Unknown or ambiguous graph subjects fail closed. Duplicate evidence IDs,
unknown evidence dependencies, and evidence dependency cycles are errors rather
than silently incomplete coverage.

## Coverage and identity

Coverage counts only `fresh` evidence. Requirements with stale, expired, or
missing proof remain uncovered. Every output record includes current hashes,
reason codes, resolved feature-scoped subjects, upstream state, source manifest,
and a deterministic fingerprint. The ledger fingerprint includes graph identity,
source manifests, current file identities, `as_of`, coverage, and stale paths.
