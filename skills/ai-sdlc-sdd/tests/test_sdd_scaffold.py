#!/usr/bin/env python3
"""End-to-end tests for stdin-driven SDD artifact assembly."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "skills/ai-sdlc-sdd/scripts"
SCAFFOLD = SCRIPTS / "sdd_artifact_scaffold.py"
sys.path.insert(0, str(SCRIPTS))


def load_module(name: str, path: Path):
    """Load one SDD script module for direct deterministic assertions."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SPEC_HELPERS = load_module("sdd_scaffold_spec_helpers", SCRIPTS / "spec_helpers.py")
PLAN_LINKS = load_module("sdd_scaffold_plan_links", SCRIPTS / "plan_links.py")
CHECK_CLARIFY = load_module("sdd_scaffold_check_clarify", SCRIPTS / "check_clarify.py")
CHECK_CHECKLIST = load_module("sdd_scaffold_check_checklist", SCRIPTS / "check_checklist.py")
ANALYZE = load_module("sdd_scaffold_analyze", SCRIPTS / "analyze_spec.py")
VALIDATE = load_module("sdd_scaffold_validate", SCRIPTS / "validate_spec.py")


def section_body(artifact: str, section: str, index: int) -> str:
    """Return meaningful fixture content that satisfies downstream SDD gates."""
    if artifact == "requirements" and section == "Acceptance Criteria":
        return "- AC-001: Given valid input, when the scaffold finalizes, then it reports success."
    if artifact == "requirements" and section == "Out of Scope":
        return "- Direct manual editing of generated artifacts."
    if artifact == "requirements" and section == "Open Questions":
        return "- No open questions remain."
    if artifact == "requirements" and section == "Decision Status":
        return "- All blocking decisions resolved."
    if artifact == "test-cases" and section == "Scenario Matrix":
        return "- TC-001 covers AC-001 with a successful finalize scenario."
    if artifact == "tasks":
        task_id = f"T{index + 1:03d}"
        return f"- [ ] {task_id}. Complete {section.lower()} work.\nOutput: {section} complete.\nRefs: AC-001"
    if artifact == "qa" and section == "Validation Commands":
        return "- `python3 validate_spec.py specs/123-stdin-sdd --quick-flow`"
    return f"- Content for {artifact} / {section}."


class SddArtifactScaffoldTests(unittest.TestCase):
    """Assemble all source artifacts through stdin and run the SDD gates."""

    def test_generated_package_passes_sdd_gates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_dir = Path(temp_dir) / "specs/123-stdin-sdd"
            spec_dir.mkdir(parents=True)

            for artifact, sections in SPEC_HELPERS.SDD_ARTIFACT_SECTIONS.items():
                for index, section in enumerate(sections):
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(SCAFFOLD),
                            str(spec_dir),
                            "--artifact",
                            artifact,
                            "--section",
                            section,
                            "--quick-flow",
                        ],
                        input=section_body(artifact, section, index),
                        text=True,
                        check=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                result = subprocess.run(
                    [
                        sys.executable,
                        str(SCAFFOLD),
                        str(spec_dir),
                        "--artifact",
                        artifact,
                        "--finalize",
                        "--quick-flow",
                    ],
                    text=True,
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

            args = SimpleNamespace(
                feature="123-stdin-sdd",
                quick_flow=True,
                full_flow=False,
                artifact_status="draft",
                artifact_owner="TBD",
                artifact_tag=[],
            )
            machine_plan = spec_dir / "_ai_sdlc/plan.toon"
            machine_plan.parent.mkdir(parents=True, exist_ok=True)
            machine_plan.write_text(PLAN_LINKS.build_plan_toon(spec_dir, args), encoding="utf-8")
            (spec_dir / "plan.md").write_text(PLAN_LINKS.build_plan(spec_dir, args), encoding="utf-8")

            self.assertEqual(CHECK_CLARIFY.validate(spec_dir), [])
            self.assertEqual(CHECK_CHECKLIST.validate(spec_dir), [])
            self.assertEqual(ANALYZE.validate(spec_dir), [])
            requirements = (spec_dir / "requirements.md").read_text(encoding="utf-8")
            self.assertIn('status: "review"', requirements)
            self.assertNotIn("ai-sdlc:empty", requirements)

            errors: list[str] = []
            for artifact, sections in SPEC_HELPERS.SDD_ARTIFACT_SECTIONS.items():
                markdown = (spec_dir / f"{artifact}.md").read_text(encoding="utf-8")
                errors.extend(VALIDATE.validate_sections(f"{artifact}.md", markdown, sections))
            errors.extend(VALIDATE.validate_tasks((spec_dir / "tasks.md").read_text(encoding="utf-8")))
            errors.extend(VALIDATE.validate_plan((spec_dir / "plan.md").read_text(encoding="utf-8")))
            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
