#!/usr/bin/env python3
"""Reusable per-skill test contract for AI SDLC helper scripts.

Every skill owns `tests/test_scripts.py`, and each of those tests delegates to
this module. Keeping the assertions here gives every skill identical coverage
without copying a large test body into 26 directories.
"""

from __future__ import annotations

import argparse
import os
import py_compile
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"


def _write(path: Path, text: str) -> None:
    """Write dedented fixture text for temporary contract tests."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def _run_script(path: Path, *args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    """Run a helper script with a safe pycache location and captured output."""
    env = os.environ.copy()
    env["PYTHONPYCACHEPREFIX"] = "/tmp/ai-sdlc-harness-pycache"
    return subprocess.run(
        [sys.executable, str(path), *args],
        cwd=cwd,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _script_paths(skill_dir: Path) -> list[Path]:
    """Return runtime helper scripts for one skill."""
    return sorted((skill_dir / "scripts").glob("*.py"))


def _is_cli_script(path: Path) -> bool:
    """Detect scripts that expose an argparse command-line interface."""
    return "ArgumentParser" in path.read_text(encoding="utf-8")


def _is_artifact_profile_script(path: Path) -> bool:
    """Detect wrappers around the shared artifact-profile helper."""
    text = path.read_text(encoding="utf-8")
    return "emit_profile_report(" in text and "build_parser(" in text


def run_skill_script_contract(skill_dir: Path) -> None:
    """Assert the standard script contract for one skill directory."""
    scripts = _script_paths(skill_dir)
    if not scripts:
        raise AssertionError(f"{skill_dir.relative_to(ROOT)} has no scripts directory content")

    for script in scripts:
        # Compilation catches syntax/import-time problems without executing the
        # workflow logic.
        cache_name = str(script.relative_to(ROOT)).replace("/", "__") + ".pyc"
        py_compile.compile(
            str(script),
            cfile=str(Path("/tmp") / "ai-sdlc-harness-pycache" / cache_name),
            doraise=True,
        )

        if _is_cli_script(script):
            # Every CLI script must expose help so agents can inspect usage
            # without reading implementation code.
            help_result = _run_script(script, "--help")
            if help_result.returncode != 0:
                raise AssertionError(f"{script.relative_to(ROOT)} --help failed:\n{help_result.stderr}")
            if "usage:" not in help_result.stdout.lower():
                raise AssertionError(f"{script.relative_to(ROOT)} --help did not print usage")

        if _is_artifact_profile_script(script):
            help_result = _run_script(script, "--help")
            for flag in ("--section", "--finalize", "--decision-row", "--max-artifact-tokens"):
                if flag not in help_result.stdout:
                    raise AssertionError(f"{script.relative_to(ROOT)} --help missing {flag}")
            # Artifact-profile scripts must honor both flow modes and emit the
            # deterministic skeletons used to save prompt tokens.
            for flag, expected in (("--quick-flow", "Assumption/default"), ("--full-flow", "Open questions/blockers")):
                result = _run_script(
                    script,
                    "--feature",
                    "skill-contract",
                    flag,
                    "--emit-template",
                    "--emit-decision-log-entry",
                    str(README),
                )
                if result.returncode != 0:
                    raise AssertionError(f"{script.relative_to(ROOT)} {flag} failed:\n{result.stderr}")
                for marker in (
                    f"Flow mode: {flag.removeprefix('--').removesuffix('-flow')}",
                    "Target artifact:",
                    "Decision Log Entry",
                    "Artifact Template",
                    expected,
                ):
                    if marker not in result.stdout:
                        raise AssertionError(f"{script.relative_to(ROOT)} {flag} output missing {marker!r}")

            with tempfile.TemporaryDirectory() as temp_dir:
                # `--write` is verified in a temp directory so tests do not touch
                # the repository's real specs/specs-refiniment trees.
                cwd = Path(temp_dir)
                input_file = cwd / "notes.md"
                _write(input_file, "# Notes\n\nREQ-001: Customer needs a faster workflow with AC-001.")
                result = _run_script(
                    script,
                    "--feature",
                    "write-contract",
                    "--quick-flow",
                    "--write",
                    str(input_file),
                    cwd=cwd,
                )
                if result.returncode != 0:
                    raise AssertionError(f"{script.relative_to(ROOT)} --write failed:\n{result.stderr}")
                if "## Written Files" not in result.stdout or "decision-log.md" not in result.stdout:
                    raise AssertionError(f"{script.relative_to(ROOT)} --write did not report written files")


def main() -> int:
    """Run one per-skill contract without dynamically importing test code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    requested = args.skill_dir
    if requested.is_symlink():
        parser.error("skill_dir must not be a symlink")
    try:
        skill_dir = requested.resolve(strict=True)
    except OSError as exc:
        parser.error(str(exc))
    skills_root = (ROOT / "skills").resolve()
    if skill_dir.parent != skills_root:
        parser.error("skill_dir must be one direct, non-symlinked child of the repository skills directory")
    try:
        run_skill_script_contract(skill_dir)
    except AssertionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Skill script contract passed: {skill_dir.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
