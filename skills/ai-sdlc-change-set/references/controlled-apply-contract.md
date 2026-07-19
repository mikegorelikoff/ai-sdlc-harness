# Controlled Apply And Archive Contract

## Approval

Apply requires an `ai-sdlc-change-approval/v1` JSON record. It must accept the
exact current preview fingerprint, identify an accountable owner and decision
reference, use an ISO timestamp, and approve every gate discovered by preview.
Missing, rejected, stale, partial, or malformed approval fails before staging.

## Transaction

1. Rebuild delta and preview from authoritative Markdown and current targets.
2. Validate approval against that preview.
3. Materialize every virtual after-state in workspace staging.
4. Copy every existing target to workspace backups.
5. Persist a recovery manifest before the first target write.
6. Replace targets one at a time using same-filesystem atomic rename.
7. If any replacement or final record update fails, restore every applied
   target from backup and remove newly created targets.
8. Mark the change `applied` only after all replacements succeed.

Multi-file atomicity is implemented as fail-safe rollback, because common
filesystems do not provide a portable transaction across separate paths. The
recovery manifest records planned hashes, applied paths, rollback status, and
errors so interrupted work remains inspectable.

## Archive

Archive is allowed only for an applied change with a completed recovery
manifest. It updates the lifecycle record and atomically moves the complete
workspace to `changes/archive/<date>-<change-id>/`. The archive retains source
deltas, preview, approval, evidence, target hashes, backups, and recovery data.

Repeated apply or archive never reapplies target changes or overwrites an
archive. It returns a safe error with the existing lifecycle state.
