#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StaticAnalysisError(RuntimeError):
    pass


def severity_from_pmd(priority: Any) -> str:
    try:
        value = int(priority)
    except (TypeError, ValueError) as exc:
        raise StaticAnalysisError(f"invalid PMD priority: {priority}") from exc
    if value <= 2:
        return "Critical"
    if value == 3:
        return "Warning"
    return "Advisory"


def severity_from_sfdx_scanner(severity: Any) -> str:
    text = str(severity).lower()
    if text in {"1", "high", "critical", "error"}:
        return "Critical"
    if text in {"2", "medium", "moderate", "warning"}:
        return "Warning"
    return "Advisory"


def _summary(findings: list[dict[str, Any]]) -> dict[str, int]:
    summary = {"critical": 0, "warning": 0, "advisory": 0}
    for finding in findings:
        summary[finding["severity"].lower()] += 1
    return summary


def parse_pmd_json(payload: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for file_entry in payload.get("files", []):
        filename = file_entry.get("filename")
        for violation in file_entry.get("violations", []):
            findings.append(
                {
                    "severity": severity_from_pmd(violation.get("priority")),
                    "rule": violation.get("rule"),
                    "file": filename,
                    "line": violation.get("beginline"),
                    "message": violation.get("description"),
                }
            )
    return {"tool": "pmd", "summary": _summary(findings), "findings": findings}


def parse_sfdx_scanner_json(payload: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for result in payload.get("result", []):
        for violation in result.get("violations", []):
            findings.append(
                {
                    "severity": severity_from_sfdx_scanner(violation.get("severity")),
                    "rule": violation.get("ruleName") or violation.get("rule"),
                    "file": violation.get("fileName") or violation.get("file"),
                    "line": violation.get("line"),
                    "message": violation.get("message"),
                }
            )
    return {"tool": "sfdx-scanner", "summary": _summary(findings), "findings": findings}


def parse_report(path: Path, parser_name: str) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if parser_name == "pmd-json":
        return parse_pmd_json(payload)
    if parser_name == "sfdx-scanner-json":
        return parse_sfdx_scanner_json(payload)
    raise StaticAnalysisError(f"unsupported parser: {parser_name}")


def evaluate_thresholds(parsed_results: list[dict[str, Any]], thresholds: dict[str, Any]) -> dict[str, Any]:
    summary = {"critical": 0, "warning": 0, "advisory": 0}
    for result in parsed_results:
        result_summary = result["summary"]
        for key in summary:
            summary[key] += result_summary[key]

    status = "PASS"
    critical_max = thresholds.get("critical_max")
    warning_max = thresholds.get("warning_max")
    advisory_max = thresholds.get("advisory_max")
    if critical_max is not None and summary["critical"] > critical_max:
        status = "FAIL"
    elif warning_max is not None and summary["warning"] > warning_max:
        status = "CONDITIONAL"
    elif advisory_max is not None and summary["advisory"] > advisory_max:
        status = "CONDITIONAL"
    return {"status": status, "summary": summary}
