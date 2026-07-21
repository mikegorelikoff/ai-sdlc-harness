from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_catalog import (  # noqa: E402
    DOCS as CATALOG_DOCS,
    SKILL_SELECTION_BOUNDARIES,
    SKILL_GUIDES,
    generated_outputs,
    has_cli_entry,
    script_record,
    script_sources,
    skill_frontmatter,
    skill_sources,
    validate_coverage_manifest,
    validate_script_catalog,
    validate_selection_contract,
    validate_skill_guide,
    validate_role_skill_groups,
)
from validate_docs import (  # noqa: E402
    CONTROL_PLANE_CONTRACT,
    IMPLEMENTATION_CONTRACT,
    Page,
    internal_links,
    navigation_paths,
    parse_frontmatter,
    validate_contract_matrix,
    validate_adoption_operations,
    validate_governance_contract,
    validate_links,
    validate_flows,
    validate_full_lifecycle_contract,
    validate_maintainer_contract,
    validate_maturity_contract,
    validate_navigation,
    validate_onboarding,
    validate_pilot_contract,
    validate_rollout_contract,
    validate_refinement_contract,
    validate_raci_contract,
    validate_role_skill_discovery,
    validate_root_source_text,
    validate_root_documents,
    validate_section_index,
    validate_troubleshooting_contract,
)


DOCS_ROOT = SCRIPTS.parent


class DocumentationValidationTests(unittest.TestCase):
    def test_root_documents_reject_broken_link_and_machine_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("README.md", "FAQ.md", "CONTRIBUTING.md", "SECURITY.md", "SUPPORT.md"):
                (root / name).write_text("Public documentation.\n", encoding="utf-8")
            (root / "README.md").write_text("[Missing](docs/missing.md) /Users/example/private\n", encoding="utf-8")
            errors = validate_root_documents(root)
            self.assertTrue(any("broken local link" in error for error in errors))
            self.assertTrue(any("machine-specific" in error for error in errors))

    def test_parse_material_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.md"
            path.write_text("---\ntitle: Test\ndescription: Useful\n---\n\nBody text.", encoding="utf-8")
            page = parse_frontmatter(path)
            self.assertEqual(page.metadata["title"], "Test")
            self.assertEqual(page.body, "Body text.")

    def test_navigation_paths_preserve_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mkdocs.yml"
            path.write_text(
                "nav:\n  - Home: index.md\n  - Guides:\n      - Install: how-to/install.md\n",
                encoding="utf-8",
            )
            self.assertEqual(navigation_paths(path), ["index.md", "how-to/install.md"])

    def test_relative_markdown_links_are_detected(self) -> None:
        page = Page(Path("docs/source.md"), {}, "[Target](reference/target.md#contract)")
        self.assertEqual(internal_links(page), {"reference/target.md#contract"})

    def test_broken_internal_link_reports_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            source_path = docs / "source.md"
            source_path.write_text("", encoding="utf-8")
            source = Page(source_path, {}, "[Missing](missing.md)")
            errors = validate_links([source], docs)
            self.assertEqual(len(errors), 1)
            self.assertIn("broken internal link missing.md", errors[0])

    def test_root_absolute_link_is_rejected(self) -> None:
        page = Page(Path("docs/source.md"), {}, '<a href="/missing/">Missing</a>')
        errors = validate_links([page], Path("docs"))
        self.assertTrue(any("root-absolute" in error for error in errors))

    def test_duplicate_navigation_page_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            page_path = docs / "index.md"
            page_path.write_text("---\ntitle: Home\ndescription: Home\n---\n", encoding="utf-8")
            config = root / "mkdocs.yml"
            config.write_text("nav:\n  - Home: index.md\n  - Again: index.md\n", encoding="utf-8")
            pages = [Page(page_path, {"title": "Home", "description": "Home"}, "Body")]
            errors = validate_navigation(pages, docs, config)
            self.assertTrue(any("duplicate pages" in error for error in errors))

    def test_navigation_limits_tabs_and_promotes_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            page_path = docs / "index.md"
            page_path.write_text("---\ntitle: Home\ndescription: Home\n---\n", encoding="utf-8")
            pages = [Page(page_path, {"title": "Home", "description": "Home"}, "Body")]
            config = root / "mkdocs.yml"
            config.write_text(
                "nav:\n"
                "  - Home: index.md\n"
                "  - Start:\n"
                "  - Use:\n"
                "  - Adopt:\n"
                "  - About:\n"
                "  - Maintain:\n"
                "  - Reference:\n",
                encoding="utf-8",
            )
            errors = validate_navigation(pages, docs, config)
            self.assertTrue(any("maximum is 6" in error for error in errors))
            self.assertTrue(any("first three" in error for error in errors))

    def test_onboarding_rejects_nonexistent_installer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            for relative in (
                "foundations/index.md",
                "foundations/ai-sdlc.md",
                "foundations/sdd.md",
                "foundations/why-harness.md",
                "foundations/mental-model.md",
                "foundations/responsibilities.md",
                "foundations/glossary.md",
                "onboarding/index.md",
                "onboarding/first-30-minutes.md",
                "index.md",
                "how-to/install.md",
            ):
                path = docs / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    "software development lifecycle AI SDLC specification-driven development artifact evidence gate handoff "
                    "Tell your agent Run in terminal Agent does automatically Human checkpoint",
                    encoding="utf-8",
                )
            (root / "README.md").write_text("./scripts/install.sh\n", encoding="utf-8")
            errors = validate_onboarding(root)
            self.assertTrue(any("nonexistent scripts/install.sh" in error for error in errors))

    def test_onboarding_requires_foundation_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "README.md").write_text("AI SDLC Harness", encoding="utf-8")
            errors = validate_onboarding(root)
            self.assertTrue(any("missing foundation/onboarding pages" in error for error in errors))

    def test_flows_require_complete_stage_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            for relative in (
                "flows/index.md",
                "flows/refinement.md",
                "flows/implementation.md",
                "flows/control-plane.md",
                "flows/recovery.md",
                "tutorials/first-feature.md",
            ):
                path = docs / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("incomplete", encoding="utf-8")
            errors = validate_flows(root)
            self.assertTrue(any("missing parseable exact stage table" in error for error in errors))
            self.assertTrue(any("missing runnable tutorial contract" in error for error in errors))

    def test_refinement_rejects_misassociated_artifact(self) -> None:
        text = (DOCS_ROOT / "flows/refinement.md").read_text(encoding="utf-8")
        self.assertEqual(validate_refinement_contract(text), [])
        mutated = text.replace("`discovery.md`", "`wrong-discovery.md`", 1)
        self.assertTrue(any("mis-associated canonical profile discovery" in error for error in validate_refinement_contract(mutated)))
        composite = text.replace("| Product manager | `discovery.md`", "| Product manager/BA | `discovery.md`", 1)
        self.assertTrue(any("composite Accountable" in error for error in validate_refinement_contract(composite)))

    def test_full_lifecycle_rejects_misassociated_stage_prompt(self) -> None:
        text = (DOCS_ROOT / "tutorials/full-lifecycle.md").read_text(encoding="utf-8")
        self.assertEqual(validate_full_lifecycle_contract(text), [])
        mutated = text.replace("Produce discovery.md.", "Produce wrong.md.", 1)
        self.assertTrue(any("mis-associated stage contract discovery" in error for error in validate_full_lifecycle_contract(mutated)))

    def test_flow_matrices_reject_misassociated_artifacts(self) -> None:
        implementation = (DOCS_ROOT / "flows/implementation.md").read_text(encoding="utf-8")
        self.assertEqual(
            validate_contract_matrix(
                implementation,
                "## Exact implementation contract",
                "implementation",
                IMPLEMENTATION_CONTRACT,
            ),
            [],
        )
        broken_implementation = implementation.replace("feature/<slug>", "feature/wrong", 1)
        self.assertTrue(
            any(
                "mis-associated branch contract branch" in error
                for error in validate_contract_matrix(
                    broken_implementation,
                    "## Exact implementation contract",
                    "implementation",
                    IMPLEMENTATION_CONTRACT,
                )
            )
        )

        control = (DOCS_ROOT / "flows/control-plane.md").read_text(encoding="utf-8")
        self.assertEqual(
            validate_contract_matrix(
                control,
                "## Exact control-plane branch contract",
                "control",
                CONTROL_PLANE_CONTRACT,
            ),
            [],
        )
        broken_control = control.replace("delivery-graph.{toon,json,md}", "delivery-graph.broken", 1)
        self.assertTrue(
            any(
                "mis-associated branch contract delivery_graph" in error
                for error in validate_contract_matrix(
                    broken_control,
                    "## Exact control-plane branch contract",
                    "control",
                    CONTROL_PLANE_CONTRACT,
                )
            )
        )

    def test_adoption_operations_contracts_and_mutations(self) -> None:
        self.assertEqual(validate_adoption_operations(DOCS_ROOT.parent), [])

        raci = (DOCS_ROOT / "operations/operating-model.md").read_text(encoding="utf-8")
        self.assertTrue(
            validate_raci_contract(
                raci.replace("| Problem/value accepted |", "| Wrong gate |", 1)
            )
        )

        def replace_table_cell(
            text: str, row_label: str, column: int, replacement: str
        ) -> str:
            lines = text.splitlines()
            for index, line in enumerate(lines):
                if not line.startswith(f"| {row_label} |"):
                    continue
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                cells[column] = replacement
                lines[index] = "| " + " | ".join(cells) + " |"
                return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
            self.fail(f"missing table row {row_label}")

        for authority_column in (1, 2, 3, 4):
            self.assertTrue(
                validate_raci_contract(
                    replace_table_cell(
                        raci, "Problem/value accepted", authority_column, ""
                    )
                )
            )

        pilot = (DOCS_ROOT / "adoption/pilot.md").read_text(encoding="utf-8")
        self.assertTrue(
            validate_pilot_contract(pilot.replace("| Baseline |", "| Before |", 1))
        )

        rollout = (DOCS_ROOT / "adoption/rollout.md").read_text(encoding="utf-8")
        self.assertEqual(validate_rollout_contract(rollout), [])
        self.assertTrue(validate_rollout_contract(rollout.replace("| Limited cohort |", "| Cohort |", 1)))

        governance = (DOCS_ROOT / "operations/governance.md").read_text(encoding="utf-8")
        self.assertTrue(
            validate_governance_contract(
                governance.replace("## Incident response", "## Incident notes", 1)
            )
        )

        troubleshooting = (DOCS_ROOT / "operations/troubleshooting.md").read_text(encoding="utf-8")
        self.assertTrue(
            validate_troubleshooting_contract(
                troubleshooting.replace("| Invalid or corrupt state |", "| Bad state |", 1)
            )
        )
        troubleshooting_mutations = {
            1: "Inspect prerequisites.",
            2: "Retry later.",
            3: "Looks good.",
            4: "Avoid unsafe action.",
            5: "",
        }
        for column, replacement in troubleshooting_mutations.items():
            self.assertTrue(
                validate_troubleshooting_contract(
                    replace_table_cell(
                        troubleshooting, "Install command fails", column, replacement
                    )
                )
            )

        maturity = (DOCS_ROOT / "explanation/maturity-limitations.md").read_text(encoding="utf-8")
        self.assertTrue(
            validate_maturity_contract(
                maturity.replace("## Known limitations", "## Caveats", 1)
            )
        )

        maintainer = (
            (DOCS_ROOT / "maintainers/extend.md").read_text(encoding="utf-8")
            + (DOCS_ROOT / "maintainers/release.md").read_text(encoding="utf-8")
        )
        self.assertTrue(validate_maintainer_contract(maintainer.replace("module.json", "manifest", 1)))

        internal = (DOCS_ROOT.parent / "concepts/README.md").read_text(encoding="utf-8")
        self.assertTrue(
            validate_root_source_text(
                internal.replace("<!-- public-docs-canonical:", "<!-- old-source:", 1),
                "concepts/README.md",
            )
        )

        adoption_index = parse_frontmatter(DOCS_ROOT / "adoption/index.md")
        broken_index = Page(
            adoption_index.path,
            adoption_index.metadata,
            adoption_index.body.replace("pilot.md", "missing-pilot.md"),
        )
        self.assertTrue(
            validate_section_index(
                broken_index, DOCS_ROOT / "adoption", "docs/adoption/index.md"
            )
        )

    def test_generated_catalog_closes_skill_and_script_inventories(self) -> None:
        outputs = generated_outputs()
        skills = skill_sources()
        records = [script_record(path) for path in script_sources()]
        self.assertEqual(len(skills), 44)
        self.assertEqual(len(records), 115)
        self.assertEqual(len(SKILL_SELECTION_BOUNDARIES), 44)
        self.assertEqual(validate_selection_contract(skills), [])
        self.assertEqual(validate_role_skill_groups(skills), [])
        role_page = outputs[CATALOG_DOCS / "reference/skills-by-role.md"]
        self.assertEqual(validate_role_skill_discovery(role_page), [])
        for source in skills:
            skill_id = skill_frontmatter(source)["name"]
            page = outputs[SKILL_GUIDES / f"{skill_id}.md"]
            self.assertEqual(validate_skill_guide(page, skill_id), [])

        scripts = outputs[CATALOG_DOCS / "reference/scripts.md"]
        coverage = outputs[CATALOG_DOCS / "reference/catalog-coverage.toon"]
        self.assertEqual(validate_script_catalog(scripts, records), [])
        self.assertEqual(validate_coverage_manifest(coverage, len(skills), records), [])
        self.assertTrue(coverage.startswith("schema: ai-sdlc-documentation-coverage/v1\n"))
        self.assertEqual(
            sum(record.classification == "installed runtime mirror" for record in records),
            20,
        )

    def test_generated_catalog_rejects_missing_sections_and_paths(self) -> None:
        outputs = generated_outputs()
        records = [script_record(path) for path in script_sources()]
        navigator = outputs[SKILL_GUIDES / "ai-sdlc-navigator.md"]
        broken_guide = navigator.replace("## Handoff", "## Missing handoff", 1)
        self.assertTrue(
            any(
                "missing guide section ## Handoff" in error
                for error in validate_skill_guide(broken_guide, "ai-sdlc-navigator")
            )
        )

        broken_selection = navigator.replace(
            "Use that owning skill instead", "Use that owning skill", 1
        )
        self.assertTrue(
            any(
                "non-use guidance must name a concrete alternative" in error
                for error in validate_skill_guide(
                    broken_selection, "ai-sdlc-navigator"
                )
            )
        )

        research = outputs[SKILL_GUIDES / "ai-sdlc-research.md"]
        broken_research = research.replace("### Freshness rule", "### Recency note", 1)
        self.assertTrue(
            any(
                "missing research evidence contract ### Freshness rule" in error
                for error in validate_skill_guide(
                    broken_research, "ai-sdlc-research"
                )
            )
        )
        invalid_research_json = research.replace(
            '"limitations": "Jurisdiction review is still required"',
            '"limitations": ["Jurisdiction review is still required"]',
            1,
        )
        self.assertTrue(
            any(
                "published JSON fails helper: findings 1: limitations is required"
                in error
                for error in validate_skill_guide(
                    invalid_research_json, "ai-sdlc-research"
                )
            )
        )

        package_trust = outputs[SKILL_GUIDES / "ai-sdlc-package-trust.md"]
        broken_package_trust = package_trust.replace(
            "### Branch B — Generate local metrics",
            "### Combined operation",
            1,
        )
        self.assertTrue(
            any(
                "missing branch ### Branch B — Generate local metrics" in error
                for error in validate_skill_guide(
                    broken_package_trust, "ai-sdlc-package-trust"
                )
            )
        )
        broken_branch_a = package_trust.replace(
            "**Inputs and reads.** Read the package root",
            "**Package inputs.** Read the package root",
            1,
        )
        self.assertTrue(
            any(
                "Branch A — Verify a package missing independent field **Inputs and reads.**"
                in error
                for error in validate_skill_guide(
                    broken_branch_a, "ai-sdlc-package-trust"
                )
            )
        )
        broken_branch_b = package_trust.replace(
            "**Inputs and reads.** Read only repository-local",
            "**Metrics inputs.** Read only repository-local",
            1,
        )
        self.assertTrue(
            any(
                "Branch B — Generate local metrics missing independent field **Inputs and reads.**"
                in error
                for error in validate_skill_guide(
                    broken_branch_b, "ai-sdlc-package-trust"
                )
            )
        )

        missing_path = records[0].path.relative_to(SCRIPTS.parents[1]).as_posix()
        broken_scripts = outputs[CATALOG_DOCS / "reference/scripts.md"].replace(
            missing_path, "missing/script.py"
        )
        self.assertTrue(
            any(
                missing_path in error
                for error in validate_script_catalog(broken_scripts, records)
            )
        )
        broken_coverage = outputs[
            CATALOG_DOCS / "reference/catalog-coverage.toon"
        ].replace(missing_path, "missing/script.py")
        self.assertTrue(
            any(
                missing_path in error
                for error in validate_coverage_manifest(
                    broken_coverage, len(skill_sources()), records
                )
            )
        )

    def test_published_help_commands_are_real_nonempty_clis(self) -> None:
        """Every generated direct --help invocation must execute a CLI and print usage."""
        import subprocess

        records = [script_record(path) for path in script_sources()]
        for record in records:
            if not record.invocation.endswith(" --help"):
                continue
            source = record.path.read_text(encoding="utf-8")
            self.assertTrue(has_cli_entry(source), record.path)
            result = subprocess.run(
                record.invocation.split(),
                cwd=DOCS_ROOT.parent,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 0, record.path)
            self.assertIn("usage:", (result.stdout + result.stderr).lower(), record.path)

if __name__ == "__main__":
    unittest.main()
