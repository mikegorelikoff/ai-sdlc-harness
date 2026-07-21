#!/usr/bin/env python3
"""Discover and validate compatible AI SDLC module manifests."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA = "ai-sdlc-module/v1"
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class Module:
    """Validated module discovery record."""

    module_id: str
    version: str
    kind: str
    api_min: str
    api_max: str
    requires: tuple[str, ...]
    skills: tuple[tuple[str, str], ...]
    description: str
    manifest: str
    compatible: bool


def version(value: object) -> tuple[int, int, int] | None:
    """Parse strict three-part semantic version identity."""
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        return None
    return tuple(int(part) for part in value.split("."))  # type: ignore[return-value]


def safe_path(root: Path, value: object) -> Path | None:
    """Resolve a repository-relative path without traversal."""
    if not isinstance(value, str) or not value:
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def read_manifest(root: Path, path: Path, harness_version: tuple[int, int, int]) -> tuple[Module | None, list[str]]:
    """Read and validate one module manifest."""
    prefix = path.relative_to(root).as_posix()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"{prefix}: cannot read manifest: {exc}"]
    if not isinstance(value, dict):
        return None, [f"{prefix}: manifest must be an object"]
    errors: list[str] = []
    allowed = {"schema", "id", "version", "kind", "harness_api", "skills", "requires", "description"}
    unknown = sorted(set(value) - allowed)
    if value.get("schema") != SCHEMA:
        errors.append(f"{prefix}: schema must be {SCHEMA}")
    module_id = value.get("id")
    if not isinstance(module_id, str) or not ID_PATTERN.fullmatch(module_id):
        errors.append(f"{prefix}: invalid module id")
    module_version = version(value.get("version"))
    if module_version is None:
        errors.append(f"{prefix}: version must use x.y.z")
    if value.get("kind") not in {"core", "optional"}:
        errors.append(f"{prefix}: kind must be core or optional")
    api = value.get("harness_api")
    api_min = version(api.get("min")) if isinstance(api, dict) else None
    api_max = version(api.get("max_exclusive")) if isinstance(api, dict) else None
    if api_min is None or api_max is None or api_min >= api_max:
        errors.append(f"{prefix}: harness_api requires a valid min < max_exclusive range")
    requires = value.get("requires", [])
    if not isinstance(requires, list) or not all(isinstance(item, str) and ID_PATTERN.fullmatch(item) for item in requires) or len(requires) != len(set(requires)):
        errors.append(f"{prefix}: requires must contain unique module IDs")
        requires = []
    skills_value = value.get("skills")
    skills: list[tuple[str, str]] = []
    if not isinstance(skills_value, list):
        errors.append(f"{prefix}: skills must be an array")
    else:
        for index, item in enumerate(skills_value, start=1):
            if not isinstance(item, dict) or set(item) != {"name", "path"}:
                errors.append(f"{prefix}: skill {index} requires only name and path")
                continue
            name, skill_path = item.get("name"), item.get("path")
            resolved = safe_path(root, skill_path)
            if not isinstance(name, str) or not ID_PATTERN.fullmatch(name):
                errors.append(f"{prefix}: skill {index} has invalid name")
            elif resolved is None or not (resolved / "SKILL.md").is_file():
                errors.append(f"{prefix}: skill {name} path does not contain SKILL.md")
            else:
                skills.append((name, str(skill_path)))
    if len({name for name, _ in skills}) != len(skills):
        errors.append(f"{prefix}: duplicate skill names inside module")
    if unknown:
        errors.append(f"{prefix}: unknown fields: {', '.join(unknown)}")
    if errors:
        return None, errors
    assert isinstance(module_id, str) and isinstance(value["version"], str) and isinstance(api, dict) and api_min is not None and api_max is not None
    compatible = api_min <= harness_version < api_max
    return Module(module_id, value["version"], value["kind"], api["min"], api["max_exclusive"], tuple(requires), tuple(skills), str(value.get("description", "")), prefix, compatible), []


def discover(root: Path, harness: str) -> tuple[list[Module], list[str]]:
    """Discover all manifests and validate registry-wide invariants."""
    harness_version = version(harness)
    if harness_version is None:
        return [], ["harness version must use x.y.z"]
    modules: list[Module] = []
    errors: list[str] = []
    for path in sorted((root / "modules").glob("*/module.json")):
        module, manifest_errors = read_manifest(root, path, harness_version)
        errors.extend(manifest_errors)
        if module:
            modules.append(module)
    ids = [item.module_id for item in modules]
    for duplicate in sorted({item for item in ids if ids.count(item) > 1}):
        errors.append(f"duplicate module id: {duplicate}")
    owners: dict[str, str] = {}
    for module in modules:
        for skill, _ in module.skills:
            if skill in owners:
                errors.append(f"duplicate skill ownership: {skill} in {owners[skill]} and {module.module_id}")
            owners[skill] = module.module_id
        for required in module.requires:
            if required not in ids:
                errors.append(f"module {module.module_id} requires missing module {required}")
    if not any(item.kind == "core" for item in modules):
        errors.append("module registry requires one core module")
    return modules, errors


def config_enabled(path: Path | None) -> tuple[set[str], list[str]]:
    """Read optional enabled module IDs from resolved configuration."""
    if path is None:
        return set(), []
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        enabled = value.get("values", {}).get("modules", {}).get("enabled", [])
    except (OSError, json.JSONDecodeError, AttributeError) as exc:
        return set(), [f"cannot read resolved config: {exc}"]
    if not isinstance(enabled, list) or not all(isinstance(item, str) for item in enabled):
        return set(), ["resolved config modules.enabled must be a string array"]
    return set(enabled), []


def toon(value: object) -> str:
    """Escape one scalar for TOON."""
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def render_toon(modules: list[Module], enabled: set[str], harness: str) -> str:
    """Render bounded module and skill discovery output."""
    skills = [(module, name, path) for module in modules for name, path in module.skills]
    lines = ["schema: ai-sdlc-module-discovery/v1", f"harness_api_version: {harness}", "", f"modules[{len(modules)}]{{id,version,kind,compatible,enabled,requires,manifest}}:"]
    for module in modules:
        is_enabled = module.kind == "core" or module.module_id in enabled
        lines.append("  " + ",".join((module.module_id, module.version, module.kind, "yes" if module.compatible else "no", "yes" if is_enabled else "no", "/".join(module.requires), module.manifest)))
    lines.extend(["", f"skills[{len(skills)}]{{module,name,path,compatible,enabled}}:"])
    for module, name, path in skills:
        is_enabled = module.kind == "core" or module.module_id in enabled
        lines.append("  " + ",".join((module.module_id, name, path, "yes" if module.compatible else "no", "yes" if is_enabled else "no")))
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(modules: list[Module], enabled: set[str], harness: str) -> str:
    """Render human-readable module discovery output."""
    lines = ["# AI SDLC Module Discovery", "", f"- Harness API: `{harness}`", "", "| Module | Version | Kind | Compatible | Enabled | Skills |", "| --- | --- | --- | --- | --- | ---: |"]
    for module in modules:
        is_enabled = module.kind == "core" or module.module_id in enabled
        lines.append(f"| `{module.module_id}` | `{module.version}` | `{module.kind}` | `{'yes' if module.compatible else 'no'}` | `{'yes' if is_enabled else 'no'}` | {len(module.skills)} |")
    lines.extend(["", "## Compatible Skills"])
    for module in modules:
        if module.compatible:
            lines.extend(f"- `{name}` from `{module.module_id}` at `{path}`" for name, path in module.skills)
    return "\n".join(lines).rstrip() + "\n"


def atomic_write(path: Path, content: str) -> None:
    """Write a discovery projection atomically."""
    if any(component.is_symlink() for component in (path, *list(path.parents)[:4])):
        raise SystemExit(f"ERROR: output path contains symlink component: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    """Discover compatible core and optional modules."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--harness-version", default="1.0.0")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--enable", action="append", default=[])
    parser.add_argument("--format", choices=("markdown", "toon"), default="markdown")
    parser.add_argument("--write-root", type=Path)
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
        print("ERROR: module discovery is read-only; it cannot change lifecycle state")
        return 1
    root = args.root.resolve()
    modules, errors = discover(root, args.harness_version)
    configured, config_errors = config_enabled(args.config)
    errors.extend(config_errors)
    enabled = configured | set(args.enable)
    available_ids = {item.module_id for item in modules if item.compatible}
    errors.extend(f"enabled module is unavailable or incompatible: {item}" for item in sorted(enabled - available_ids))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    machine = render_toon(modules, enabled, args.harness_version)
    human = render_markdown(modules, enabled, args.harness_version)
    if args.write_root:
        atomic_write(args.write_root / "modules.md", human)
        atomic_write(args.write_root / "_ai_sdlc/modules.toon", machine)
    print(machine if args.format == "toon" else human, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
