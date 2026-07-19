#!/usr/bin/env python3
"""Measure raw, compact, and targeted-reread context payloads."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from ai_sdlc_context import build_context_pack, estimate_tokens, positive_int, toon_row


def targeted_read_text(pack: str, source_text: dict[str, str]) -> str:
    """Materialize unique source lines referenced by a pack's next_reads rows."""
    in_reads = False
    selected: set[tuple[str, int]] = set()
    for raw in pack.splitlines():
        if raw.startswith("next_reads["):
            in_reads = True
            continue
        if in_reads and not raw.startswith("  "):
            in_reads = False
        if not in_reads or not raw.startswith("  "):
            continue
        values = next(csv.reader([raw.strip()]))
        if len(values) < 4:
            continue
        source, _, start, end = values[:4]
        try:
            first, last = int(start), int(end)
        except ValueError:
            continue
        for line in range(first, last + 1):
            selected.add((source, line))
    excerpts: list[str] = []
    for source, line in sorted(selected):
        lines = source_text.get(source, "").splitlines()
        if 1 <= line <= len(lines):
            excerpts.append(lines[line - 1])
    return "\n".join(excerpts)


def main() -> int:
    """Build a context pack and print informational token metrics."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--workspace", choices=["refinement", "implementation"], default="refinement")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--budget-tokens", type=positive_int)
    parser.add_argument("--required-section", action="append", default=[])
    parser.add_argument("--keyword", action="append", default=[])
    args = parser.parse_args()

    flow = "full" if args.full_flow else "quick" if args.quick_flow else "default"
    budget = args.budget_tokens or (4000 if flow == "quick" else 24000)
    pack, _, sources = build_context_pack(
        files=args.files, feature=args.feature, skill=args.skill,
        workspace=args.workspace, flow_mode=flow, budget_tokens=budget,
        required_sections=args.required_section, keywords=args.keyword,
    )
    source_text = {source.display_path: source.text for source in sources}
    raw = "\n\n".join(source.text for source in sources)
    targeted = targeted_read_text(pack, source_text)
    raw_tokens = estimate_tokens(raw)
    pack_tokens = estimate_tokens(pack)
    reread_tokens = estimate_tokens(targeted) if targeted else 0
    combined = pack_tokens + reread_tokens
    saved = raw_tokens - combined
    percent = round(saved * 100 / raw_tokens, 1) if raw_tokens else 0

    print("schema: ai-sdlc-context-benchmark/v1")
    print("quality_gate: informational")
    print(f"raw_tokens: {raw_tokens}")
    print(f"pack_tokens: {pack_tokens}")
    print(f"targeted_reread_tokens: {reread_tokens}")
    print(f"combined_tokens: {combined}")
    print(f"saved_tokens: {saved}")
    print(f"saved_percent: {percent}")
    print(f"positive_savings: {'yes' if saved > 0 else 'no'}")
    print(f"sources[{len(sources)}]{{path,status}}:")
    for source in sources:
        print("  " + toon_row((source.display_path, source.status)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
