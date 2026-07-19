# Specification Delta Contract

## Format

Store semantic deltas as Markdown below `changes/<change-id>/deltas/`. Keep
`index.md` as the intake placeholder and use one or more descriptive files for
actual targets.

```markdown
# Specification Delta

Target: `specs/auth/requirements.md`

## ADDED Requirements

### Requirement: Session timeout
ID: FR-016

The system SHALL expire an inactive session after the configured duration.

#### Scenario: Inactive session expires
- WHEN the inactivity duration is reached
- THEN the session is invalidated
```

Supported sections are `ADDED`, `MODIFIED`, `REMOVED`, and `RENAMED
Requirements`.

## Operation rules

- `ADDED`: ID must be absent from an existing target. Include a normative
  `MUST` or `SHALL` statement and at least one scenario with WHEN and THEN.
- `MODIFIED`: ID must exist in the target. Include the complete replacement
  requirement and scenarios, not a prose diff.
- `REMOVED`: ID must exist. Include non-empty `Reason:` and `Migration:` lines.
- `RENAMED`: ID must exist. Include distinct non-empty `From:` and `To:` lines.
- One target and stable requirement ID may occur only once across the change.
- Every delta target must already appear in the parent change-set record.

## Authority and safety

Parsing and validation are read-only. The parser may read canonical target
text to prove ID presence or absence, but cannot rewrite it. A valid delta set
does not imply approval, compatibility, or permission to apply.

`_ai_sdlc/delta-set.json` is a generated projection with exact source hashes,
normalized operations, validation identity, and no mutation authority.
