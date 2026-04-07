#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
LOCAL_VENV_SETUP = "python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt"


def inject_repo_site_packages() -> None:
    lib_dir = REPO_ROOT / ".venv" / "lib"
    if not lib_dir.is_dir():
        return
    for site_packages in sorted(lib_dir.glob("python*/site-packages")):
        site_packages_str = str(site_packages)
        if site_packages_str not in sys.path:
            sys.path.insert(0, site_packages_str)


inject_repo_site_packages()


def _check(name: str, status: str, message: str, fix: str | None = None) -> dict[str, str]:
    result = {"name": name, "status": status, "message": message}
    if fix:
        result["fix"] = fix
    return result


def resolve_codex_home(value: str | None = None) -> Path:
    return Path(value or os.environ.get("CODEX_HOME") or (Path.home() / ".codex")).expanduser().resolve()


def check_python() -> dict[str, str]:
    if shutil.which("python3"):
        return _check("python", "OK", "python3 is available")
    return _check("python", "FAIL", "python3 is missing", "python3 をインストールしてください")


def check_pyyaml() -> dict[str, str]:
    try:
        import yaml  # noqa: F401
    except ModuleNotFoundError:
        return _check(
            "pyyaml",
            "FAIL",
            "PyYAML is missing",
            LOCAL_VENV_SETUP,
        )
    return _check("pyyaml", "OK", "PyYAML is available")


def check_codex_home(codex_home: Path) -> dict[str, str]:
    if codex_home.exists():
        return _check("codex_home", "OK", f"CODEX_HOME is {codex_home}")
    return _check("codex_home", "WARN", f"CODEX_HOME does not exist yet: {codex_home}", f"mkdir -p {codex_home}")


def check_skill_links(codex_home: Path) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    skills_target = codex_home / "skills"
    toolkit_target = codex_home / "salesforce-kit"
    if skills_target.is_dir():
        checks.append(_check("skills_dir", "OK", f"skills directory exists: {skills_target}"))
    else:
        checks.append(_check("skills_dir", "WARN", f"skills directory is missing: {skills_target}", "./scripts/bootstrap-kit.sh"))

    expected_toolkit = REPO_ROOT.resolve()
    if toolkit_target.is_symlink():
        current = toolkit_target.resolve()
        if current == expected_toolkit:
            checks.append(_check("toolkit_link", "OK", f"salesforce-kit points to {current}"))
        else:
            checks.append(
                _check(
                    "toolkit_link",
                    "FAIL",
                    f"salesforce-kit points to a different location: {current}",
                    "既存 link を見直して ./scripts/bootstrap-kit.sh を再実行してください",
                )
            )
    elif toolkit_target.exists():
        checks.append(
            _check(
                "toolkit_link",
                "FAIL",
                f"salesforce-kit exists but is not a symlink: {toolkit_target}",
                "既存ディレクトリを整理して ./scripts/bootstrap-kit.sh を再実行してください",
            )
        )
    else:
        checks.append(_check("toolkit_link", "WARN", "salesforce-kit link is missing", "./scripts/bootstrap-kit.sh"))
    return checks


def check_repo_assets() -> list[dict[str, str]]:
    expected = [
        REPO_ROOT / "scripts" / "resolve-overlay.py",
        REPO_ROOT / "scripts" / "validate-overlays.py",
        REPO_ROOT / "scripts" / "validate-skills.sh",
        REPO_ROOT / "scripts" / "discover-overlay.py",
    ]
    results: list[dict[str, str]] = []
    for path in expected:
        if path.is_file():
            results.append(_check(path.name, "OK", f"{path.name} is available"))
        else:
            results.append(_check(path.name, "FAIL", f"{path.name} is missing", "リポジトリ内容を確認してください"))
    return results


def run_check(command: list[str], name: str, ok_message: str) -> dict[str, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        return _check(name, "FAIL", f"{name} could not start: {exc}", "依存関係と script 権限を確認してください")
    if completed.returncode == 0:
        return _check(name, "OK", ok_message)
    stderr = (completed.stderr or completed.stdout).strip().splitlines()
    tail = stderr[-1] if stderr else f"{name} failed"
    return _check(name, "FAIL", tail, f"{' '.join(command)}")


def recommended_presets() -> list[str]:
    return [
        "minimal: salesforce-review, salesforce-release-check, salesforce-quick-test, salesforce-perm-check",
        "standard: minimal + salesforce-flow-review + salesforce-smoke-check + salesforce-package-release",
        "ta-full: all skills",
    ]


def build_report(codex_home: Path) -> dict[str, Any]:
    checks = [check_python(), check_pyyaml(), check_codex_home(codex_home)]
    checks.extend(check_skill_links(codex_home))
    checks.extend(check_repo_assets())

    pyyaml_ok = next(check for check in checks if check["name"] == "pyyaml")["status"] == "OK"
    if pyyaml_ok:
        checks.append(run_check([sys.executable, "scripts/validate-overlays.py"], "validate_overlays", "overlay validation passed"))
        checks.append(run_check(["/bin/bash", "-lc", "./scripts/validate-skills.sh"], "validate_skills", "skill validation passed"))
    else:
        checks.append(
            _check(
                "validate_overlays",
                "WARN",
                "overlay validation skipped because PyYAML is missing",
                LOCAL_VENV_SETUP,
            )
        )
        checks.append(
            _check(
                "validate_skills",
                "WARN",
                "skill validation skipped because PyYAML is missing",
                LOCAL_VENV_SETUP,
            )
        )

    statuses = {item["status"] for item in checks}
    overall = "OK"
    exit_code = 0
    if "FAIL" in statuses:
        overall = "FAIL"
        exit_code = 2
    elif "WARN" in statuses:
        overall = "WARN"
        exit_code = 1

    next_actions = [
        "./scripts/bootstrap-kit.sh",
        "python3 scripts/doctor.py --json",
        "python3 scripts/discover-overlay.py --workspace-root /path/to/salesforce-repo --name \"My Repo\" --pretty",
    ]
    return {
        "status": overall,
        "exit_code": exit_code,
        "checks": checks,
        "presets": recommended_presets(),
        "next_actions": next_actions,
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [f"[{report['status']}] Salesforce Codex kit doctor"]
    for check in report["checks"]:
        lines.append(f"[{check['status']}] {check['name']}: {check['message']}")
        if check.get("fix"):
            lines.append(f"  fix: {check['fix']}")
    lines.append("NEXT:")
    for item in report["next_actions"]:
        lines.append(f"- {item}")
    lines.append("PRESETS:")
    for item in report["presets"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Diagnose Salesforce Codex kit installation health.")
    parser.add_argument("--json", action="store_true", help="output machine-readable JSON")
    parser.add_argument("--codex-home", help="override CODEX_HOME")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = build_report(resolve_codex_home(args.codex_home))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
    return int(report["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
