from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from scripts import doctor


class DoctorTest(unittest.TestCase):
    def test_resolve_codex_home_prefers_argument(self) -> None:
        resolved = doctor.resolve_codex_home("/tmp/codex-home-test")
        self.assertEqual(Path("/tmp/codex-home-test").resolve(), resolved)

    def test_build_report_json_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = doctor.build_report(Path(tmp))
        self.assertIn(report["status"], {"OK", "WARN", "FAIL"})
        self.assertIsInstance(report["checks"], list)
        self.assertTrue(any(item["name"] == "python" for item in report["checks"]))
        self.assertTrue(report["next_actions"])

    def test_missing_toolkit_link_is_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            checks = doctor.check_skill_links(Path(tmp))
        toolkit = next(item for item in checks if item["name"] == "toolkit_link")
        self.assertEqual("WARN", toolkit["status"])

    def test_existing_correct_toolkit_link_is_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            (codex_home / "skills").mkdir()
            (codex_home / "salesforce-kit").symlink_to(doctor.REPO_ROOT)
            checks = doctor.check_skill_links(codex_home)
        toolkit = next(item for item in checks if item["name"] == "toolkit_link")
        self.assertEqual("OK", toolkit["status"])


if __name__ == "__main__":
    unittest.main()
