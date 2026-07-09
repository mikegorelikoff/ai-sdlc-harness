# Flow Modes

Every skill supports two explicit execution modes. The AI assistant reads the
requested mode, applies the matching behavior, and passes the same mode to
helper scripts so generated artifacts, state transitions, and validation
strictness stay consistent.

## Quick Flow

`--quick-flow` means the AI prioritizes fast, high-quality progress with the
available evidence.

Behavior:

- use available context and repository evidence;
- avoid questions unless continuing creates material product, security,
  compliance, data-loss, or irreversible implementation risk;
- record assumptions and important defaults in `decision-log.md`;
- rely on `specs-index.toon` before opening broad artifact sets;
- run only focused checks that are relevant and cheap.

Quick flow is not permission to invent requirements. It is permission for the AI
to make documented, low-risk assumptions and keep moving when the missing
information does not create material risk.

## Quick Flow Outputs

In quick flow, the AI produces:

- concise artifact drafts;
- explicit assumptions in the artifact body;
- `artifact_metadata.flow_mode: "quick"`;
- decision-log rows for material assumptions;
- updated specs indexes after file writes;
- a short residual-risk note when broader checks are skipped.

## Full Flow

`--full-flow` means the AI prioritizes verification, traceability, and
confidence before final handoff.

Behavior:

- ask concise clarification questions when material inputs are missing;
- verify upstream and downstream artifacts;
- verify `decision-log.md`, `state.toon`, metadata, and specs indexes;
- treat incomplete predecessor stages as blockers;
- run or recommend the skill-appropriate validation and review gates.

## Full Flow Outputs

In full flow, the AI produces:

- artifact drafts or updates with verified sources;
- explicit blockers and open questions when material inputs are missing;
- `artifact_metadata.flow_mode: "full"`;
- updated `decision-log.md` entries for accepted assumptions or scope choices;
- updated `state.toon` when lifecycle progress changes;
- refreshed TOON and Markdown specs indexes;
- validation evidence or a clear explanation of blocked validation.

## Precedence

If both flags are supplied, `--full-flow` wins because it is stricter.

When neither flag is supplied, the skill follows its default behavior and chooses
the least risky path for the request size and domain.

## AI Failure Modes

The AI must not:

- ask long clarification loops in quick flow for non-blocking gaps;
- silently assume material scope, security, compliance, or data-loss behavior;
- claim full-flow readiness without checking artifacts, decisions, state, and
  validation evidence;
- pass a different flow flag to helper scripts than the one used by the skill.
