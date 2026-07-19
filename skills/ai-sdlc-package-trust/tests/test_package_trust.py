#!/usr/bin/env python3
"""Tests for package trust validation."""
from __future__ import annotations
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-package-trust/scripts/package_trust.py"
class PackageTrustTests(unittest.TestCase):
    def fixture(self, repository: Path, capabilities: list[str] | None = None, provenance: bool = True) -> tuple[Path, Path]:
        package = repository / "package"; package.mkdir(); (package / "SKILL.md").write_text("# Trusted\n", encoding="utf-8"); (package / "tool.py").write_text("print('ok')\n", encoding="utf-8")
        files = [{"path": name, "sha256": hashlib.sha256((package / name).read_bytes()).hexdigest()} for name in ("SKILL.md", "tool.py")]
        manifest = {"schema":"ai-sdlc-package/v1","id":"trusted-tool","version":"1.0.0","origin":{"type":"repository","reference":"local:test"},"harness_api":{"min":"1.0.0","max_exclusive":"2.0.0"},"capabilities":capabilities or ["filesystem.read"],"files":files,"digest":hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),"provenance":{"builder":"local-builder" if provenance else "","source_digest":"a"*64 if provenance else "","attestation":"build-1" if provenance else ""}}
        path = repository / "package.json"; path.write_text(json.dumps(manifest), encoding="utf-8"); return package, path
    def cli(self, repository: Path, package: Path, manifest: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["python3", str(SCRIPT), str(repository), "--package-root", str(package), "--manifest", str(manifest), "--allowed-origin", "repository", "--allowed-capability", "filesystem.read", "--require-provenance", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    def test_valid_package_is_deterministic_and_writes_toon(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp); package, manifest = self.fixture(repository)
            first = self.cli(repository, package, manifest, "--write", "--format", "json"); second = self.cli(repository, package, manifest, "--format", "json")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr); self.assertEqual(first.stdout, second.stdout); self.assertEqual(json.loads(first.stdout)["decision"], "allow")
            self.assertTrue((repository / "_ai_sdlc/trust/trusted-tool/decision.toon").is_file())
    def test_tamper_disallowed_capability_and_missing_provenance_deny(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp); package, manifest = self.fixture(repository, ["network.access"], False); (package / "tool.py").write_text("tampered\n", encoding="utf-8")
            result = self.cli(repository, package, manifest, "--format", "json"); self.assertEqual(result.returncode, 2); value = json.loads(result.stdout); self.assertEqual(value["decision"], "deny")
            failed = {item["code"] for item in value["controls"] if item["status"] == "fail"}; self.assertEqual(failed, {"capabilities", "integrity", "provenance"})
    def test_symlink_inventory_fails_integrity(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp); package, manifest = self.fixture(repository); (package / "tool.py").unlink(); (package / "tool.py").symlink_to(package / "SKILL.md")
            result = self.cli(repository, package, manifest, "--format", "json"); self.assertEqual(result.returncode, 2); self.assertIn("integrity-fail", json.loads(result.stdout)["reason_codes"])
if __name__ == "__main__": unittest.main()
