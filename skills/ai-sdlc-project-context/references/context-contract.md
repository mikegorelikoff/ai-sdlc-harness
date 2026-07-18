# Project Context Contract

High-signal sources are repository guidance, README files, package and language
manifests, Makefiles, and common CI workflows. Claims require `path:line`
anchors. The fingerprint is SHA-256 over normalized relative path and content
for every consumed source. Secret-named, environment, key, token, credential,
and certificate paths are excluded.

Canonical outputs are `project-context.md` and
`_ai_sdlc/project-context.toon`. Both use the same revision and fingerprint.
Drift is true when either differs from the current repository scan.
