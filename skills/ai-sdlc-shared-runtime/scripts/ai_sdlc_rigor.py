#!/usr/bin/env python3
"""Select an explainable risk-adaptive AI SDLC rigor profile."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass


PROFILE_ORDER = ("patch", "standard", "assured", "regulated")
FACTOR_NAMES = (
    "blast_radius",
    "irreversibility",
    "ambiguity",
    "security_data",
    "compliance",
    "external_dependencies",
    "architectural_novelty",
    "rollout_complexity",
)


@dataclass(frozen=True)
class RigorDecision:
    """Explainable adaptive rigor selection."""

    automatic_profile: str
    requested_profile: str
    minimum_profile: str
    effective_profile: str
    total_score: int
    reasons: tuple[str, ...]


def profile_max(*profiles: str) -> str:
    """Return the strictest profile."""
    return max(profiles, key=PROFILE_ORDER.index)


def automatic_profile(factors: dict[str, int]) -> tuple[str, list[str]]:
    """Classify risk factors without user or organization overrides."""
    total = sum(factors.values())
    reasons: list[str] = []
    if factors["compliance"] >= 2:
        reasons.append("compliance risk requires regulated evidence")
        return "regulated", reasons
    if factors["security_data"] == 3:
        reasons.append("critical security or data risk requires regulated evidence")
        return "regulated", reasons
    critical = [name for name, score in factors.items() if score == 3]
    if critical:
        reasons.append("critical factors require assured rigor: " + "/".join(critical))
        return "assured", reasons
    elevated = [name for name, score in factors.items() if score >= 2]
    if total >= 10 or len(elevated) >= 3:
        reasons.append("combined elevated risk requires assured rigor")
        return "assured", reasons
    if total >= 4 or elevated:
        reasons.append("non-trivial delivery risk requires standard rigor")
        return "standard", reasons
    reasons.append("risk is local, reversible, and sufficiently clear for patch rigor")
    return "patch", reasons


def decide(
    factors: dict[str, int],
    *,
    requested: str | None = None,
    minimum: str = "patch",
    quick_flow: bool = False,
    full_flow: bool = False,
) -> RigorDecision:
    """Resolve automatic, explicit, and protected minimum rigor."""
    automatic, reasons = automatic_profile(factors)
    flow_request = "assured" if full_flow else "patch" if quick_flow else ""
    requested_profile = requested or flow_request or automatic
    if requested:
        reasons.append(f"explicit profile requested: {requested}")
    elif full_flow:
        reasons.append("--full-flow requests at least assured rigor")
    elif quick_flow:
        reasons.append("--quick-flow requests patch rigor when risk permits")
    effective = profile_max(automatic, requested_profile, minimum)
    if PROFILE_ORDER.index(effective) > PROFILE_ORDER.index(requested_profile):
        reasons.append(f"requested rigor was raised to {effective} by risk or protected minimum")
    if PROFILE_ORDER.index(minimum) > PROFILE_ORDER.index(automatic):
        reasons.append(f"organization minimum raised rigor to {minimum}")
    return RigorDecision(automatic, requested_profile, minimum, effective, sum(factors.values()), tuple(reasons))


def toon(value: object) -> str:
    """Escape one TOON scalar."""
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def render_toon(factors: dict[str, int], decision: RigorDecision) -> str:
    """Render compact machine output."""
    lines = [
        "schema: ai-sdlc-rigor/v1",
        f"automatic_profile: {decision.automatic_profile}",
        f"requested_profile: {decision.requested_profile}",
        f"minimum_profile: {decision.minimum_profile}",
        f"effective_profile: {decision.effective_profile}",
        f"total_score: {decision.total_score}",
        "",
        f"factors[{len(factors)}]{{name,score}}:",
    ]
    lines.extend(f"  {name},{score}" for name, score in factors.items())
    lines.extend(["", f"reasons[{len(decision.reasons)}]{{message}}:"])
    lines.extend(f"  {toon(reason)}" for reason in decision.reasons)
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(factors: dict[str, int], decision: RigorDecision) -> str:
    """Render human-readable decision output."""
    lines = [
        "# AI SDLC Adaptive Rigor",
        "",
        f"- Automatic profile: `{decision.automatic_profile}`",
        f"- Requested profile: `{decision.requested_profile}`",
        f"- Protected minimum: `{decision.minimum_profile}`",
        f"- Effective profile: `{decision.effective_profile}`",
        f"- Total score: `{decision.total_score}`",
        "",
        "## Factors",
    ]
    lines.extend(f"- `{name}`: `{score}`" for name, score in factors.items())
    lines.extend(["", "## Reasons"])
    lines.extend(f"- {reason}" for reason in decision.reasons)
    return "\n".join(lines).rstrip() + "\n"


def factor_score(value: str) -> int:
    """Parse a factor score in the inclusive 0-3 range."""
    score = int(value)
    if score not in range(4):
        raise argparse.ArgumentTypeError("factor score must be 0, 1, 2, or 3")
    return score


def main() -> int:
    """Parse risk factors and render the effective rigor profile."""
    parser = argparse.ArgumentParser(description=__doc__)
    for name in FACTOR_NAMES:
        parser.add_argument("--" + name.replace("_", "-"), type=factor_score, default=0)
    parser.add_argument("--profile", choices=PROFILE_ORDER)
    parser.add_argument("--minimum-profile", choices=PROFILE_ORDER, default="patch")
    parser.add_argument("--format", choices=("markdown", "toon"), default="markdown")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    args = parser.parse_args()

    if args.begin_state or args.complete_state:
        print("ERROR: rigor selection is read-only; the owning workflow controls lifecycle state")
        return 1
    factors = {name: getattr(args, name) for name in FACTOR_NAMES}
    decision = decide(
        factors,
        requested=args.profile,
        minimum=args.minimum_profile,
        quick_flow=args.quick_flow,
        full_flow=args.full_flow,
    )
    renderer = render_toon if args.format == "toon" else render_markdown
    print(renderer(factors, decision), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
