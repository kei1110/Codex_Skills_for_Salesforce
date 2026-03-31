from __future__ import annotations

import unittest
from pathlib import Path

from scripts import static_analysis


FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "static-analysis"


class StaticAnalysisParserTest(unittest.TestCase):
    def test_parse_pmd_json_maps_severity(self) -> None:
        parsed = static_analysis.parse_report(FIXTURE_DIR / "pmd-report.json", "pmd-json")
        self.assertEqual("pmd", parsed["tool"])
        self.assertEqual({"critical": 1, "warning": 1, "advisory": 1}, parsed["summary"])
        self.assertEqual("Critical", parsed["findings"][0]["severity"])

    def test_parse_sfdx_scanner_json_maps_severity(self) -> None:
        parsed = static_analysis.parse_report(
            FIXTURE_DIR / "sfdx-scanner-report.json",
            "sfdx-scanner-json",
        )
        self.assertEqual("sfdx-scanner", parsed["tool"])
        self.assertEqual({"critical": 1, "warning": 1, "advisory": 1}, parsed["summary"])
        self.assertEqual("Critical", parsed["findings"][0]["severity"])

    def test_evaluate_thresholds(self) -> None:
        parsed_results = [
            {
                "tool": "pmd",
                "summary": {"critical": 0, "warning": 1, "advisory": 0},
                "findings": [
                    {
                        "severity": "Warning",
                        "rule": "AvoidDebugStatements",
                        "file": "force-app/main/default/classes/Foo.cls",
                    }
                ],
            },
            {
                "tool": "sfdx-scanner",
                "summary": {"critical": 1, "warning": 0, "advisory": 2},
                "findings": [
                    {
                        "severity": "Critical",
                        "rule": "Security-ApexCRUDViolation",
                        "file": "force-app/main/default/classes/Foo.cls",
                    },
                    {
                        "severity": "Advisory",
                        "rule": "CodeStyle-Naming",
                        "file": "force-app/main/default/classes/Foo.cls",
                    },
                ],
            },
        ]
        result = static_analysis.evaluate_thresholds(
            parsed_results,
            {"critical_max": 0, "warning_max": 2, "advisory_max": None},
            blocking_rules=["Critical が 1 件でもあれば FAIL"],
        )
        self.assertEqual("FAIL", result["status"])
        self.assertEqual({"critical": 1, "warning": 1, "advisory": 2}, result["summary"])
        self.assertEqual(["Critical が 1 件でもあれば FAIL"], result["blocking_rules_applied"])
        self.assertEqual(1, len(result["reasons"]))
        self.assertEqual("Security-ApexCRUDViolation", result["reasons"][0]["rule"])
        self.assertTrue(result["next_actions"])


if __name__ == "__main__":
    unittest.main()
