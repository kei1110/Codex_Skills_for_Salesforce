#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict
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


def _aggregate_findings(parsed_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
    for result in parsed_results:
        tool = result.get("tool", "unknown")
        for finding in result.get("findings", []):
            key = (tool, finding["rule"], finding["severity"])
            entry = grouped.setdefault(
                key,
                {
                    "type": "static_analysis",
                    "tool": tool,
                    "rule": finding["rule"],
                    "severity": finding["severity"],
                    "count": 0,
                    "files": [],
                },
            )
            entry["count"] += 1
            if finding.get("file") and finding["file"] not in entry["files"]:
                entry["files"].append(finding["file"])
    order = {"Critical": 0, "Warning": 1, "Advisory": 2}
    return sorted(
        grouped.values(),
        key=lambda item: (order.get(item["severity"], 99), item["tool"], item["rule"]),
    )


def _suggest_next_actions(reasons: list[dict[str, Any]], status: str) -> list[str]:
    actions: list[str] = []
    seen: set[str] = set()
    rule_actions = {
        "ApexCRUDViolation": "CRUD/FLS ガード実装を確認",
        "Security-ApexCRUDViolation": "CRUD/FLS ガード実装を確認",
        "AvoidGlobalModifier": "2GP 公開境界への影響を確認",
        "Security-ApexSharingViolations": "sharing と入口制御を確認",
    }
    severity_actions = {
        "Critical": "Critical 指摘を解消するまで release を進めない",
        "Warning": "Warning 指摘の運用影響と追加テスト要否を確認",
        "Advisory": "Advisory 指摘の優先順位を整理",
    }
    for reason in reasons:
        for candidate in (rule_actions.get(reason["rule"]), severity_actions.get(reason["severity"])):
            if candidate and candidate not in seen:
                seen.add(candidate)
                actions.append(candidate)
    if status == "PASS":
        return []
    if not actions:
        actions.append("静的解析結果の根拠を確認して対応方針を決める")
    return actions


def evaluate_thresholds(
    parsed_results: list[dict[str, Any]],
    thresholds: dict[str, Any],
    *,
    blocking_rules: list[str] | None = None,
) -> dict[str, Any]:
    summary = {"critical": 0, "warning": 0, "advisory": 0}
    for result in parsed_results:
        result_summary = result["summary"]
        for key in summary:
            summary[key] += result_summary[key]

    status = "PASS"
    critical_max = thresholds.get("critical_max")
    warning_max = thresholds.get("warning_max")
    advisory_max = thresholds.get("advisory_max")
    triggered_levels: set[str] = set()
    if critical_max is not None and summary["critical"] > critical_max:
        status = "FAIL"
        triggered_levels.add("Critical")
    elif warning_max is not None and summary["warning"] > warning_max:
        status = "CONDITIONAL"
        triggered_levels.add("Warning")
    elif advisory_max is not None and summary["advisory"] > advisory_max:
        status = "CONDITIONAL"
        triggered_levels.add("Advisory")

    reasons = [
        reason
        for reason in _aggregate_findings(parsed_results)
        if reason["severity"] in triggered_levels
    ]
    return {
        "status": status,
        "summary": summary,
        "reasons": reasons,
        "next_actions": _suggest_next_actions(reasons, status),
        "blocking_rules_applied": list(blocking_rules or []),
    }
