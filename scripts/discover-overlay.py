#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def list_dirs(root: Path, pattern: str) -> list[str]:
    return sorted(
        {
            rel(path.parent, root)
            for path in root.glob(pattern)
            if path.is_file()
        }
    )


def list_doc_candidates(root: Path) -> dict[str, list[str]]:
    buckets = {
        "specs": ["docs/spec*/**/*", "spec*/**/*", "requirements*/**/*"],
        "screens": ["docs/screen*/**/*", "docs/ui*/**/*", "screen*/**/*", "ui*/**/*"],
        "technical": ["docs/tech*/**/*", "docs/design*/**/*", "design*/**/*", "architecture*/**/*"],
        "runbooks": ["docs/runbook*/**/*", "runbook*/**/*", "ops*/**/*", "operations*/**/*"],
        "roadmap": ["docs/roadmap*/**/*", "roadmap*/**/*"],
    }
    result: dict[str, list[str]] = {key: [] for key in buckets}
    for bucket, patterns in buckets.items():
        seen: set[str] = set()
        for pattern in patterns:
            for path in root.glob(pattern):
                if path.is_file():
                    value = rel(path, root)
                    if value not in seen:
                        seen.add(value)
                        result[bucket].append(value)
        result[bucket].sort()
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def discover_package_dirs(root: Path) -> list[str]:
    sfdx_project = root / "sfdx-project.json"
    if not sfdx_project.is_file():
        return []
    payload = load_json(sfdx_project)
    result: list[str] = []
    for item in payload.get("packageDirectories", []):
        if isinstance(item, dict) and item.get("path"):
            result.append(str(item["path"]).rstrip("/"))
    return result


def discover_package_aliases(root: Path) -> list[dict[str, str]]:
    sfdx_project = root / "sfdx-project.json"
    if not sfdx_project.is_file():
        return []
    payload = load_json(sfdx_project)
    aliases = payload.get("packageAliases", {})
    if not isinstance(aliases, dict):
        return []
    return [{"name": key, "value": str(value)} for key, value in sorted(aliases.items())]


def classify_permission_set(name: str) -> str:
    lowered = name.lower()
    if any(token in lowered for token in ("admin", "sysadmin", "ops")):
        return "admin"
    if any(token in lowered for token in ("elevated", "power", "super")):
        return "elevated"
    return "user"


def discover_permissions(root: Path) -> dict[str, Any]:
    permission_sets = {"user": [], "admin": [], "elevated": []}
    for path in root.glob("**/permissionsets/*.permissionset-meta.xml"):
        category = classify_permission_set(path.stem.replace(".permissionset-meta", ""))
        permission_sets[category].append(rel(path, root))
    for key in permission_sets:
        permission_sets[key].sort()
    psg = sorted(rel(path, root) for path in root.glob("**/permissionsetgroups/*.permissionsetgroup-meta.xml"))
    return {"permission_sets": permission_sets, "permission_set_groups": psg}


def discover_quality_gates(root: Path) -> dict[str, Any]:
    quality = {
        "lint": [],
        "unit_tests": [],
        "integration_tests": [],
        "smoke_tests": [],
        "static_analysis": {"commands": []},
    }
    package_json = root / "package.json"
    if package_json.is_file():
        payload = load_json(package_json)
        scripts = payload.get("scripts", {})
        if isinstance(scripts, dict):
            for key in scripts:
                command = f"npm run {key}"
                lowered = key.lower()
                if "lint" in lowered:
                    quality["lint"].append(command)
                elif "smoke" in lowered:
                    quality["smoke_tests"].append(command)
                elif "integration" in lowered or "e2e" in lowered:
                    quality["integration_tests"].append(command)
                elif "test" in lowered or "jest" in lowered:
                    quality["unit_tests"].append(command)
    workflows = sorted(root.glob(".github/workflows/*.y*ml"))
    workflow_names = [path.name.lower() for path in workflows]
    if any("scanner" in name or "pmd" in name for name in workflow_names):
        quality["static_analysis"]["commands"].append(
            {"name": "sfdx-scanner", "run": "sf scanner run --format json", "parser": "sfdx-scanner-json"}
        )
    if any("pmd" in name for name in workflow_names):
        quality["static_analysis"]["commands"].append(
            {"name": "pmd", "run": "pmd check --format json", "parser": "pmd-json"}
        )
    return quality


def build_discovery(root: Path, name: str) -> dict[str, Any]:
    return {
        "schema_version": 3,
        "kind": "repo",
        "name": name,
        "source": {
            "apex": list_dirs(root, "**/classes/*.cls"),
            "lwc": list_dirs(root, "**/lwc/*/*.js"),
            "triggers": list_dirs(root, "**/triggers/*.trigger"),
            "flows": list_dirs(root, "**/flows/*.flow-meta.xml"),
            "objects": list_dirs(root, "**/objects/*/*.object-meta.xml"),
            "permissionsets": list_dirs(root, "**/permissionsets/*.permissionset-meta.xml"),
            "permissionsetgroups": list_dirs(root, "**/permissionsetgroups/*.permissionsetgroup-meta.xml"),
            "profiles": list_dirs(root, "**/profiles/*.profile-meta.xml"),
            "layouts": list_dirs(root, "**/layouts/*.layout-meta.xml"),
            "recordtypes": list_dirs(root, "**/objects/*/recordTypes/*.recordType-meta.xml"),
            "approval_processes": list_dirs(root, "**/approvalProcesses/*.approvalProcess-meta.xml"),
            "unpackaged": sorted(
                {
                    path
                    for path in (
                        list_dirs(root, "**/flexipages/*.flexipage-meta.xml")
                        + list_dirs(root, "**/applications/*.app-meta.xml")
                    )
                }
            ),
        },
        "docs": list_doc_candidates(root),
        "packaging": {
            "package_dirs": discover_package_dirs(root),
            "package_aliases": discover_package_aliases(root),
        },
        "security": discover_permissions(root),
        "quality_gates": discover_quality_gates(root),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Discover overlay candidates from an existing Salesforce repo.")
    parser.add_argument("--workspace-root", default=".", help="path to target Salesforce repo")
    parser.add_argument("--name", help="display name for discovered overlay")
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.workspace_root).resolve()
    name = args.name or root.name
    result = build_discovery(root, name)
    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
