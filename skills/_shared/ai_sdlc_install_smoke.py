#!/usr/bin/env python3
"""Smoke-test a skill-only project installation and SDD scaffold."""

from __future__ import annotations

import argparse
import os
import re
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


def install_npx(source: str, consumer: Path, agent: str | None = None) -> None:
    """Install the local source through the pinned real Skills CLI."""
    require(run(["git", "init"], consumer), "consumer git init")
    command = [
        "npx",
        "-y",
        f"skills@{CLI_VERSION}",
        "add",
        source,
    ]
    if not agent:
        raise RuntimeError("npx installation smoke requires --agent to prevent an unbounded --all install")
    command.extend(["--skill", "*", "--agent", agent])
    command.append("-y")
    require(
        run(command, consumer),
        "Skills CLI installation",
    )
    allowed = {".agents", ".git", "skills-lock.json"}
    unexpected = sorted(path.name for path in consumer.iterdir() if path.name not in allowed)
    if unexpected:
        raise RuntimeError(
            "host-scoped installation created unexpected roots: " + ", ".join(unexpected)
        )


def resolve_source(value: str) -> tuple[str, Path]:
    """Preserve remote locators and absolutize an existing local source."""
    path = Path(value).resolve()
    return (str(path) if path.exists() else value, path)


def checkout_revision(repository: str, revision: str, destination: Path) -> None:
    """Fetch one immutable Git revision into a detached local checkout."""
    require(run(["git", "init", str(destination)], destination.parent), "source git init")
    require(run(["git", "-C", str(destination), "remote", "add", "origin", repository], destination.parent), "source remote")
    require(run(["git", "-C", str(destination), "fetch", "--depth", "1", "origin", revision], destination.parent), "source fetch")
    require(run(["git", "-C", str(destination), "checkout", "--detach", "FETCH_HEAD"], destination.parent), "source checkout")
    actual = run(["git", "-C", str(destination), "rev-parse", "HEAD"], destination.parent)
    require(actual, "source revision")
    if actual.stdout.strip() != revision:
        raise RuntimeError(f"expected source revision {revision}, found {actual.stdout.strip()}")


def verify(consumer: Path, source_checkout: Path | None = None, expected_skill_count: int = 44) -> None:
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
    config_resolver = runtime / "ai_sdlc_config.py"
    navigator = installed / "ai-sdlc-navigator" / "scripts" / "navigate.py"
    sdd_scripts = installed / "ai-sdlc-sdd" / "scripts"
    scaffold = sdd_scripts / "sdd_artifact_scaffold.py"
    commit_ready = installed / "ai-sdlc-commit-prep" / "scripts" / "check_commit_ready.py"
    config_result = run([sys.executable, str(config_resolver), "--format", "json"], consumer)
    if config_result.returncode and "--base" in config_result.stderr and source_checkout is not None:
        # v1.2.0 predates packaged defaults and requires the release checkout's
        # explicit base file. Preserve that preflight so the immutable-release
        # regression test reaches the SDD root-resolution defect it locks.
        base_config = source_checkout / "config" / "ai-sdlc.defaults.json"
        config_result = run(
            [sys.executable, str(config_resolver), "--base", str(base_config), "--format", "json"],
            consumer,
        )
    require(config_result, "installed packaged configuration defaults")
    documented_how_to_scripts = (
        installed / "ai-sdlc-host-adapter" / "scripts" / "adapter.py",
        installed / "ai-sdlc-delivery-graph" / "scripts" / "delivery_graph.py",
        installed / "ai-sdlc-delivery-graph" / "scripts" / "evidence_ledger.py",
        installed / "ai-sdlc-package-trust" / "scripts" / "package_trust.py",
        installed / "ai-sdlc-package-trust" / "scripts" / "metrics.py",
        installed / "ai-sdlc-project-context" / "scripts" / "context_engine.py",
        installed / "ai-sdlc-workflow" / "scripts" / "workflow.py",
        installed / "ai-sdlc-runtime" / "scripts" / "runtime.py",
        installed / "ai-sdlc-doctor" / "scripts" / "doctor.py",
        installed / "ai-sdlc-policy" / "scripts" / "policy.py",
    )
    for script in (runtime / "state_machine.py", navigator, scaffold, commit_ready, *documented_how_to_scripts):
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
    artifact_sections = {
        "requirements": (
            "Goal", "Problem Statement", "Scope", "Actors", "Inputs", "Outputs",
            "Functional Requirements", "Non-Functional Requirements", "Constraints",
            "Acceptance Criteria", "Out of Scope", "Assumptions", "Open Questions", "Decision Status",
        ),
        "design": (
            "Overview", "Architecture", "Components", "Interfaces and Contracts", "Data Model",
            "Error Handling", "Security Considerations", "Observability", "Risks and Tradeoffs",
            "Validation Strategy", "Migration Notes",
        ),
        "test-cases": ("Scope", "Scenario Matrix", "Layer Mapping", "Automation Plan", "Open Gaps"),
        "qa": (
            "Change Summary", "Acceptance Scenarios", "Regression Targets", "Risk Notes",
            "Validation Commands", "Manual Checks", "Signoff",
        ),
        "tasks": ("Implementation", "Testing", "Documentation"),
    }

    def section_body(artifact: str, section: str, index: int) -> str:
        if artifact == "requirements" and section == "Acceptance Criteria":
            return "- AC-001: Given an installed consumer, when all gates run, then every command exits zero.\n"
        if artifact == "requirements" and section == "Out of Scope":
            return "- Product behavior and deployment are outside this installation smoke.\n"
        if artifact == "requirements" and section == "Open Questions":
            return "- No blocking questions remain.\n"
        if artifact == "requirements" and section == "Decision Status":
            return "- All blocking decisions are resolved for this fixture.\n"
        if artifact == "test-cases" and section == "Scenario Matrix":
            return "- TC-001 covers AC-001 by executing the installed SDD and commit-readiness gates.\n"
        if artifact == "qa" and section == "Validation Commands":
            return "- Run installed clarify, checklist, plan, analysis, validation, status, and commit readiness.\n"
        if artifact == "tasks":
            task_id = f"T{index + 1:03d}"
            return f"- [ ] {task_id}. Complete {section.lower()} smoke work.\nOutput: {section} evidence.\nRefs: AC-001, TC-001\n"
        return f"- Installed smoke content for {artifact} / {section}.\n"

    for artifact, sections in artifact_sections.items():
        for index, section in enumerate(sections):
            require(
                run(
                    [
                        sys.executable, str(scaffold), str(spec.relative_to(consumer)),
                        "--artifact", artifact, "--section", section, "--quick-flow",
                    ],
                    consumer,
                    section_body(artifact, section, index),
                ),
                f"SDD {artifact} section {section}",
            )
        require(
            run(
                [
                    sys.executable, str(scaffold), str(spec.relative_to(consumer)),
                    "--artifact", artifact, "--finalize", "--quick-flow",
                ],
                consumer,
            ),
            f"SDD {artifact} finalize",
        )

    tasks = spec / "tasks.md"
    tasks.write_text(tasks.read_text(encoding="utf-8").replace("- [ ]", "- [x]"), encoding="utf-8")
    plan_links = sdd_scripts / "plan_links.py"
    require(
        run([sys.executable, str(plan_links), str(spec.relative_to(consumer)), "--write", "--quick-flow"], consumer),
        "installed plan generation",
    )
    installed_gates = (
        (sdd_scripts / "check_clarify.py", []),
        (sdd_scripts / "check_checklist.py", []),
        (plan_links, ["--check"]),
        (sdd_scripts / "analyze_spec.py", []),
        (sdd_scripts / "validate_spec.py", []),
        (sdd_scripts / "sdd_status.py", []),
    )
    for script, extra in installed_gates:
        require(
            run([sys.executable, str(script), str(spec.relative_to(consumer)), *extra, "--quick-flow"], consumer),
            f"installed {script.name}",
        )
    require(run(["git", "add", "specs"], consumer), "stage installed SDD smoke")
    require(
        run(
            [
                sys.executable, str(commit_ready), "--spec", str(spec.relative_to(consumer)),
                "--task", "T001", "--quick-flow",
            ],
            consumer,
        ),
        "installed commit readiness",
    )
    requirements = spec / "requirements.md"
    if not requirements.is_file() or 'status: "review"' not in requirements.read_text(encoding="utf-8"):
        raise RuntimeError("installed SDD scaffold did not finalize review evidence")


def main() -> int:
    """Install into a temporary consumer and execute the portable runtime."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(ROOT), help="Local checkout or pinned Skills CLI source URL")
    parser.add_argument("--mode", choices=("emulated", "npx", "npx-remote"), default="emulated")
    parser.add_argument("--agent", help="Optional Skills CLI agent target for a host-scoped smoke")
    parser.add_argument("--revision", help="Exact 40-character Git revision for npx-remote mode")
    parser.add_argument(
        "--expected-failure",
        help="Require this exact diagnostic fragment; use only to lock a documented released regression",
    )
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        print("ERROR: installation smoke cannot mutate feature state")
        return 1
    source_value, source_path = resolve_source(str(args.source))
    # The CLI runs from the disposable consumer. Resolve an existing local
    # source before changing working directories so `--source .` continues to
    # mean the harness checkout, not the empty consumer repository.
    if args.mode == "emulated" and not (source_path / "skills").is_dir():
        print(f"ERROR: source has no skills directory: {source_path}")
        return 1
    if args.mode == "npx-remote" and (not args.revision or not re.fullmatch(r"[0-9a-f]{40}", args.revision)):
        print("ERROR: npx-remote requires --revision with an exact lowercase 40-character SHA")
        return 1
    if args.expected_failure and args.mode != "npx-remote":
        print("ERROR: --expected-failure is restricted to immutable npx-remote regression checks")
        return 1
    try:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            consumer = temp_root / "consumer"
            consumer.mkdir()
            if args.mode == "npx-remote":
                source_checkout = temp_root / "harness-source"
                checkout_revision(source_value, args.revision, source_checkout)
                install_npx(str(source_checkout), consumer, args.agent)
            elif args.mode == "npx":
                install_npx(source_value, consumer, args.agent)
            else:
                install_emulated(source_path, consumer)
            installed_source = source_checkout if args.mode == "npx-remote" else source_path
            verify(consumer, installed_source if installed_source.is_dir() else None)
    except (OSError, RuntimeError) as exc:
        if args.expected_failure and args.expected_failure in str(exc):
            print(f"Known released regression reproduced: {args.expected_failure}")
            return 0
        print(f"ERROR: {exc}")
        return 1
    if args.expected_failure:
        print(f"ERROR: expected released regression did not occur: {args.expected_failure}")
        return 1
    print(
        f"Project installation valid: mode={args.mode}; installed runtime, complete SDD gates, "
        "and commit readiness passed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
