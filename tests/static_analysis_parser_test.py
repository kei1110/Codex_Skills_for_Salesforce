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
            {"summary": {"critical": 0, "warning": 1, "advisory": 0}},
            {"summary": {"critical": 1, "warning": 0, "advisory": 2}},
        ]
        result = static_analysis.evaluate_thresholds(
            parsed_results,
            {"critical_max": 0, "warning_max": 2, "advisory_max": None},
        )
        self.assertEqual("FAIL", result["status"])
        self.assertEqual({"critical": 1, "warning": 1, "advisory": 2}, result["summary"])


if __name__ == "__main__":
    unittest.main()
