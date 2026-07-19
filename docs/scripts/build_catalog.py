#!/usr/bin/env python3
"""Generate deterministic MkDocs Markdown catalogs for skills and modules."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


def skill_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path.relative_to(ROOT)}: missing frontmatter")
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key in {"name", "description"}:
            values[key] = value.strip().strip('"')
    if not values.get("name") or not values.get("description"):
        raise ValueError(f"{path.relative_to(ROOT)}: missing name or description")
    return values


def load_modules() -> list[dict[str, object]]:
    modules: list[dict[str, object]] = []
    for path in sorted((ROOT / "modules").glob("*/module.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["manifest_path"] = path.relative_to(ROOT).as_posix()
        modules.append(data)
    return modules


def render_skills(modules: list[dict[str, object]]) -> str:
    owners: dict[str, list[str]] = {}
    for module in modules:
        for skill in module.get("skills", []):
            owners.setdefault(skill["name"], []).append(str(module["id"]))

    lines = [
        "---",
        "title: Skill catalog",
        "description: Every installed AI SDLC skill, its purpose, owning module, and authoritative package path.",
        "---",
        "",
        "# Skill catalog",
        "",
        "This page is generated from each package's `SKILL.md` frontmatter. The linked source is the authoritative execution contract.",
        "",
        '<div class="grid cards" markdown>',
        "",
    ]
    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        values = skill_frontmatter(path)
        skill_id = values["name"]
        module_names = " + ".join(sorted(owners.get(skill_id, []))) or "unregistered"
        source = path.relative_to(ROOT).as_posix()
        lines.extend(
            [
                f"-   **`{skill_id}`**",
                "",
                f"    `{module_names}`",
                "",
                f"    {values['description']}",
                "",
                f"    [Open package contract →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/{source})",
                "",
            ]
        )
    lines.extend(["</div>", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_modules(modules: list[dict[str, object]]) -> str:
    lines = [
        "---",
        "title: Module catalog",
        "description: Installed capability modules, compatibility ranges, dependencies, and registered skills.",
        "---",
        "",
        "# Module catalog",
        "",
        '<div class="grid cards" markdown>',
        "",
    ]
    for module in modules:
        harness = module.get("harness_api", {})
        requires = ", ".join(module.get("requires", [])) or "none"
        skills = ", ".join(item["name"] for item in module.get("skills", [])) or "none"
        lines.extend(
            [
                f"-   **{str(module['id']).replace('-', ' ').title()}** · `{module['kind']}` · `v{module['version']}`",
                "",
                f"    {module['description']}",
                "",
                f"    **Harness API:** ≥ {harness.get('min', '')} and < {harness.get('max_exclusive', '')}",
                "",
                f"    **Requires:** {requires}",
                "",
                f"    **Skills:** {skills}",
                "",
                f"    [Open manifest →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/{module['manifest_path']})",
                "",
            ]
        )
    lines.extend(["</div>", "", "Module discovery validates schema, ID uniqueness, dependency presence, API compatibility, skill paths, and protected capability rules before navigation exposes a module.", ""])
    return "\n".join(lines).rstrip() + "\n"


def generate(check: bool = False) -> int:
    modules = load_modules()
    outputs = {
        DOCS / "reference" / "skills.md": render_skills(modules),
        DOCS / "reference" / "modules.md": render_modules(modules),
    }
    drift: list[str] = []
    for path, content in outputs.items():
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                drift.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if drift:
        print("Catalog drift: " + ", ".join(drift))
        return 1
    print(f"Catalog ready: {len(list((ROOT / 'skills').glob('*/SKILL.md')))} skills, {len(modules)} modules")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when generated data is stale")
    args = parser.parse_args()
    return generate(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
