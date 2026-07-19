#!/usr/bin/env python3
"""Smoke-test a skill-only project installation and SDD scaffold."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLI_VERSION = "1.5.19"


def run(command: list[str], cwd: Path, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    """Run one smoke command with captured diagnostics."""
    environment = os.environ.copy()
    environment["DISABLE_TELEMETRY"] = "1"
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        input=input_text,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def require(result: subprocess.CompletedProcess[str], label: str) -> None:
    """Raise with complete command evidence when a smoke step fails."""
    if result.returncode:
        output = (result.stdout + result.stderr).strip()
        raise RuntimeError(f"{label} failed with {result.returncode}: {output}")


def install_emulated(source: Path, consumer: Path) -> None:
    """Copy exactly the folders Skills CLI can discover from SKILL.md."""
    installed = consumer / ".agents" / "skills"
    installed.mkdir(parents=True)
    for skill in sorted((source / "skills").iterdir()):
        if (skill / "SKILL.md").is_file():
            shutil.copytree(skill, installed / skill.name)


def install_npx(source: str, consumer: Path) -> None:
    """Install the local source through the pinned real Skills CLI."""
    require(run(["git", "init"], consumer), "consumer git init")
    require(
        run(
            [
                "npx",
                "-y",
                f"skills@{CLI_VERSION}",
                "add",
                source,
                "--all",
                "-y",
            ],
            consumer,
        ),
        "Skills CLI installation",
    )


def verify(consumer: Path, expected_skill_count: int = 44) -> None:
    """Execute installed imports, one complete write, and finalization."""
    require(run(["git", "init"], consumer), "navigator fixture git init")
    require(run(["git", "checkout", "-B", "dev"], consumer), "navigator fixture dev branch")
    require(
        run(
            [
                "git",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "-c",
                "commit.gpgsign=false",
                "commit",
                "--allow-empty",
                "-m",
                "fixture base",
            ],
            consumer,
        ),
        "navigator fixture base commit",
    )
    installed = consumer / ".agents" / "skills"
    installed_skills = [path for path in installed.iterdir() if path.is_dir() and path.name != "_shared"]
    if len(installed_skills) != expected_skill_count:
        raise RuntimeError(f"expected {expected_skill_count} installed skills, found {len(installed_skills)}")
    if (installed / "_shared").exists():
        raise RuntimeError("smoke must not depend on source-only skills/_shared")
    runtime = installed / "ai-sdlc-shared-runtime" / "scripts"
    navigator = installed / "ai-sdlc-navigator" / "scripts" / "navigate.py"
    scaffold = installed / "ai-sdlc-sdd" / "scripts" / "sdd_artifact_scaffold.py"
    for script in (runtime / "state_machine.py", navigator, scaffold):
        if not script.is_file():
            raise RuntimeError(f"installed helper missing: {script.relative_to(consumer)}")
        require(run([sys.executable, str(script), "--help"], consumer), script.name)

    routed = run(
        [
            sys.executable,
            str(navigator),
            "--intent",
            "Implement GET /health behavior while preserving existing route behavior.",
            "--format",
            "toon",
            "--quick-flow",
        ],
        consumer,
    )
    require(routed, "installed navigator routing")
    if "recommended skill is not installed" in routed.stdout:
        raise RuntimeError("navigator did not discover project-scoped installed skills")
    if "  ai-sdlc-branching," not in routed.stdout:
        raise RuntimeError("tutorial intent on dev did not route to ai-sdlc-branching")

    spec = consumer / "specs" / "001-runtime-smoke"
    sections = (
        "Goal",
        "Problem Statement",
        "Scope",
        "Actors",
        "Inputs",
        "Outputs",
        "Functional Requirements",
        "Non-Functional Requirements",
        "Constraints",
        "Acceptance Criteria",
        "Out of Scope",
        "Assumptions",
        "Open Questions",
        "Decision Status",
    )
    for section in sections:
        body = (
            "- AC-001: Given the portable runtime, when the installed helper "
            f"writes {section.lower()}, then deterministic evidence is preserved.\n"
        )
        require(
            run(
                [
                    sys.executable,
                    str(scaffold),
                    str(spec),
                    "--artifact",
                    "requirements",
                    "--section",
                    section,
                    "--quick-flow",
                ],
                consumer,
                body,
            ),
            f"SDD section {section}",
        )
    require(
        run(
            [
                sys.executable,
                str(scaffold),
                str(spec),
                "--artifact",
                "requirements",
                "--finalize",
                "--quick-flow",
            ],
            consumer,
        ),
        "SDD requirements finalize",
    )
    requirements = spec / "requirements.md"
    if not requirements.is_file() or 'status: "review"' not in requirements.read_text(encoding="utf-8"):
        raise RuntimeError("installed SDD scaffold did not finalize review evidence")


def main() -> int:
    """Install into a temporary consumer and execute the portable runtime."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(ROOT), help="Local checkout or pinned Skills CLI source URL")
    parser.add_argument("--mode", choices=("emulated", "npx"), default="emulated")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        print("ERROR: installation smoke cannot mutate feature state")
        return 1
    source_value = str(args.source)
    source_path = Path(source_value).resolve()
    if args.mode == "emulated" and not (source_path / "skills").is_dir():
        print(f"ERROR: source has no skills directory: {source_path}")
        return 1
    try:
        with tempfile.TemporaryDirectory() as temp:
            consumer = Path(temp)
            if args.mode == "npx":
                install_npx(source_value, consumer)
            else:
                install_emulated(source_path, consumer)
            verify(consumer)
    except (OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"Project installation valid: mode={args.mode}; shared runtime and SDD scaffold passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
