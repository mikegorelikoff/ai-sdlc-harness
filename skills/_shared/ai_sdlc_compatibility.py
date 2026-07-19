#!/usr/bin/env python3
"""Validate an AI SDLC release against its compatibility baseline."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from ai_sdlc_toon import encode_toon


SCHEMA = "ai-sdlc-compatibility-baseline/v1"


def load_baseline(path: Path) -> tuple[dict[str, Any], list[str]]:
    """Load the compatibility baseline safely."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read compatibility baseline: {exc}"]
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        return {}, [f"baseline schema must be {SCHEMA}"]
    return value, []


def frontmatter_name(text: str) -> str:
    """Extract the simple skill frontmatter name."""
    match = re.search(r"(?m)^name:\s*([^\s]+)\s*$", text[:1000])
    return match.group(1) if match else ""


def validate_skills(root: Path, baseline: dict[str, Any]) -> list[str]:
    """Validate stable names, documentation, and CLI flags."""
    errors: list[str] = []
    expected = baseline.get("required_skill_names", [])
    actual = sorted(path.name for path in (root / "skills").iterdir() if path.is_dir() and path.name != "_shared")
    missing = sorted(set(expected) - set(actual))
    if missing:
        errors.append("missing required skills: " + ", ".join(missing))
    for skill in expected:
        doc = root / "skills" / skill / "SKILL.md"
        if not doc.is_file():
            continue
        text = doc.read_text(encoding="utf-8")
        if frontmatter_name(text) != skill:
            errors.append(f"skill frontmatter name mismatch: {skill}")
        for contract in baseline.get("skill_doc_contract", []):
            if contract not in text:
                errors.append(f"skill {skill} missing compatibility contract: {contract}")
        scripts = [] if skill == "ai-sdlc-shared-runtime" else sorted((doc.parent / "scripts").glob("*.py"))
        for script in scripts:
            source = script.read_text(encoding="utf-8")
            if "ArgumentParser" not in source:
                continue
            help_result = subprocess.run([sys.executable, str(script), "--help"], cwd=root, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if help_result.returncode:
                errors.append(f"script {script.relative_to(root)} --help failed: {help_result.stderr.strip()}")
                continue
            for flag in baseline.get("required_cli_flags", []):
                if flag not in help_result.stdout:
                    errors.append(f"script {script.relative_to(root)} missing stable flag {flag}")
    return errors


def validate_installed_runtime(root: Path) -> list[str]:
    """Verify generated runtime bytes and a skill-only SDD execution."""
    commands = (
        [sys.executable, str(root / "skills/_shared/sync_installed_runtime.py"), "--check"],
        [sys.executable, str(root / "skills/ai-sdlc-shared-runtime/tests/test_runtime.py")],
    )
    errors: list[str] = []
    for command in commands:
        result = subprocess.run(
            command,
            cwd=root,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode:
            errors.append(
                "installed shared runtime validation failed: "
                + (result.stdout.strip() or result.stderr.strip())
            )
    return errors


def validate_config(root: Path, baseline: dict[str, Any]) -> list[str]:
    """Validate the versioned default configuration contract."""
    config = baseline.get("config", {})
    path = root / str(config.get("defaults", ""))
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read default config: {exc}"]
    return [] if value.get("schema") == config.get("schema") else ["default config schema changed"]


def validate_modules(root: Path, baseline: dict[str, Any]) -> list[str]:
    """Validate module IDs, schema, and discovery closure."""
    errors: list[str] = []
    expected = baseline.get("modules", {}).get("ids", [])
    manifests = sorted((root / "modules").glob("*/module.json"))
    actual: list[str] = []
    for path in manifests:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read module {path.relative_to(root)}: {exc}")
            continue
        actual.append(str(value.get("id", "")))
        if value.get("schema") != baseline.get("modules", {}).get("schema"):
            errors.append(f"module schema changed: {path.relative_to(root)}")
    if sorted(actual) != expected:
        errors.append(f"module IDs changed: expected {expected}; got {sorted(actual)}")
    result = subprocess.run(["python3", str(root / "skills/_shared/ai_sdlc_modules.py"), "--root", str(root), "--harness-version", str(baseline.get("harness_api_version")), "--format", "toon"], cwd=root, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        errors.append("module discovery failed: " + (result.stdout.strip() or result.stderr.strip()))
    return errors


def validate_routes_and_docs(root: Path, baseline: dict[str, Any]) -> list[str]:
    """Validate public route and install/update documentation."""
    errors: list[str] = []
    docs = [root / "README.md", root / "concepts/artifact-routing.md", root / str(baseline.get("install_update_guide", ""))]
    for path in docs:
        if not path.is_file():
            errors.append(f"missing compatibility documentation: {path.relative_to(root)}")
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.is_file())
    for name, route in baseline.get("routes", {}).items():
        if route not in combined:
            errors.append(f"documented route missing ({name}): {route}")
    for phrase in ("npx skills add", "compatibility", "update", "rollback"):
        if phrase.lower() not in combined.lower():
            errors.append(f"install/update documentation missing: {phrase}")
    return errors


def audit_subjects(
    actual: list[str], expected: list[str], allowed_prelude: list[str] | None = None,
    allow_pending_last: bool = False,
) -> bool:
    """Require the release sequence to occupy the complete audited range."""
    prefix = allowed_prelude or []
    candidates = [expected]
    if allow_pending_last and expected:
        candidates.append(expected[:-1])
    return any(actual == prefix + candidate for candidate in candidates)


def validate_git_audit(root: Path, baseline: dict[str, Any], base: str, allow_pending_last: bool) -> list[str]:
    """Validate the released roadmap as one ordered historical sequence."""
    result = subprocess.run(["git", "log", "--reverse", "--format=%s", f"{base}..HEAD"], cwd=root, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        return ["cannot audit roadmap commits: " + result.stderr.strip()]
    actual = result.stdout.splitlines()
    expected = baseline.get("roadmap_commit_subjects", [])
    allowed_prelude = baseline.get("roadmap_allowed_prelude_subjects", [])
    valid = audit_subjects(actual, expected, list(allowed_prelude), allow_pending_last)
    if valid:
        return []
    if expected:
        return ["roadmap commit subjects do not map one-to-one with T001-T015", f"expected: {expected}", f"actual: {actual}"]
    return []


def main() -> int:
    """Run release compatibility and optional Git audit gates."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--baseline", type=Path, default=Path("compatibility/baseline-v1.json"))
    parser.add_argument("--git-base")
    parser.add_argument("--skip-git-audit", action="store_true")
    parser.add_argument("--allow-pending-last", action="store_true")
    parser.add_argument("--format", choices=("markdown", "toon"), default="toon")
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
        print("ERROR: compatibility validation is read-only")
        return 1
    root = args.root.resolve()
    baseline_path = args.baseline if args.baseline.is_absolute() else root / args.baseline
    baseline, errors = load_baseline(baseline_path)
    if not errors:
        errors.extend(validate_skills(root, baseline))
        errors.extend(validate_installed_runtime(root))
        errors.extend(validate_config(root, baseline))
        errors.extend(validate_modules(root, baseline))
        errors.extend(validate_routes_and_docs(root, baseline))
        if not args.skip_git_audit:
            errors.extend(validate_git_audit(root, baseline, args.git_base or str(baseline.get("roadmap_git_base", "main")), args.allow_pending_last))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    result = {
        "schema": "ai-sdlc-compatibility-result/v1",
        "release": baseline["release"],
        "harness_api_version": baseline["harness_api_version"],
        "skills": len([path for path in (root / "skills").iterdir() if path.is_dir() and path.name != "_shared"]),
        "modules": len(baseline["modules"]["ids"]),
        "protected_skill_names": baseline["required_skill_names"],
        "protected_cli_flags": baseline["required_cli_flags"],
        "protected_routes": baseline["routes"],
        "result": "compatible",
    }
    if args.format == "toon":
        print(encode_toon(result), end="")
    else:
        print("# AI SDLC Compatibility\n")
        print(f"- Release: `{baseline['release']}`")
        print(f"- Harness API: `{baseline['harness_api_version']}`")
        print(f"- Skills: `{result['skills']}`")
        print(f"- Modules: `{len(baseline['modules']['ids'])}`")
        print("- Result: `compatible`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
