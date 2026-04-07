#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


def inject_repo_site_packages() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    lib_dir = repo_root / ".venv" / "lib"
    if not lib_dir.is_dir():
        return
    for site_packages in sorted(lib_dir.glob("python*/site-packages")):
        site_packages_str = str(site_packages)
        if site_packages_str not in sys.path:
            sys.path.insert(0, site_packages_str)


inject_repo_site_packages()

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover
    yaml = None


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_TEMPLATE: dict[str, Any] = {
    "schema_version": 3,
    "kind": None,
    "name": None,
    "inherits": None,
    "source": {
        "apex": [],
        "lwc": [],
        "triggers": [],
        "flows": [],
        "objects": [],
        "permissionsets": [],
        "permissionsetgroups": [],
        "profiles": [],
        "layouts": [],
        "recordtypes": [],
        "approval_processes": [],
        "unpackaged": [],
    },
    "docs": {
        "specs": [],
        "screens": [],
        "roadmap": [],
        "technical": [],
        "runbooks": [],
    },
    "packaging": {
        "package_dirs": [],
        "package_aliases": [],
        "namespace": None,
        "dependencies": [],
        "unpackaged_post_deploy": [],
        "install_validation": [],
        "upgrade_validation": [],
    },
    "security": {
        "permission_sets": {
            "user": [],
            "admin": [],
            "elevated": [],
        },
        "permission_set_groups": [],
        "muting_permission_sets": [],
        "custom_permissions": [],
        "licenses": [],
        "record_type_assignments": [],
        "ui_visibility": [],
    },
    "org_bootstrap": {
        "scratch_def": None,
        "default_alias": None,
        "dev_hub_alias": None,
        "feature_setup": [],
        "settings_setup": [],
        "permission_assignments": [],
        "user_setup": [],
        "seed": [],
        "manual_steps": [],
    },
    "quality_gates": {
        "api_version_check": None,
        "lint": [],
        "unit_tests": [],
        "integration_tests": [],
        "smoke_tests": [],
        "blocking_rules": [],
        "static_analysis": {
            "commands": [],
            "thresholds": {
                "critical_max": 0,
                "warning_max": None,
                "advisory_max": None,
            },
            "blocking_rules": [],
        },
    },
    "context_pruning": {
        "roots": {
            "source": [],
            "docs": [],
        },
        "dependency_hints": {
            "apex_tests": [],
            "lwc_tests": [],
        },
    },
    "notes": [],
}
ALLOWED_TOP_LEVEL = set(SCHEMA_TEMPLATE.keys())


class OverlayError(RuntimeError):
    pass


def yaml_available() -> bool:
    return yaml is not None


def require_yaml() -> None:
    if yaml is None:
        raise OverlayError(
            "PyYAML が必要です。`python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt` を実行してください。"
        )


def is_empty_value(value: Any) -> bool:
    return value is None or value == "" or value == []


def dedupe_list(values: list[Any]) -> list[Any]:
    seen: set[str] = set()
    result: list[Any] = []
    for value in values:
        marker = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if marker in seen:
            continue
        seen.add(marker)
        result.append(value)
    return result


def is_list_patch(value: Any) -> bool:
    return isinstance(value, dict) and set(value.keys()).issubset({"replace", "values", "remove"})


def apply_list_patch(base: list[Any], patch: dict[str, Any]) -> list[Any]:
    result = [] if patch.get("replace") else deepcopy(base)
    values = patch.get("values") or []
    remove = patch.get("remove") or []
    result = dedupe_list(result + deepcopy(values))
    if remove:
        remove_markers = {json.dumps(item, ensure_ascii=False, sort_keys=True) for item in remove}
        result = [
            item
            for item in result
            if json.dumps(item, ensure_ascii=False, sort_keys=True) not in remove_markers
        ]
    return result


def merge_with_template(base: Any, child: Any) -> Any:
    if isinstance(base, dict):
        merged: dict[str, Any] = {}
        child = child or {}
        if not isinstance(child, dict):
            raise OverlayError("schema merge 中に dict 以外が指定されました")
        for key, base_value in base.items():
            merged[key] = merge_with_template(base_value, child.get(key))
        return merged
    if isinstance(base, list):
        if child is None:
            return deepcopy(base)
        if isinstance(child, list):
            return dedupe_list(deepcopy(base) + deepcopy(child))
        if is_list_patch(child):
            return apply_list_patch(base, child)
        raise OverlayError("schema merge 中に list または list patch 以外が指定されました")
    return deepcopy(base) if is_empty_value(child) else child


def normalize_overlay(data: dict[str, Any]) -> dict[str, Any]:
    return merge_with_template(SCHEMA_TEMPLATE, data)


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def load_overlay_file(path: Path) -> dict[str, Any]:
    require_yaml()
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise OverlayError(f"{path}: overlay root は map である必要があります")
    return data


def _validate_against_template(template: Any, value: Any, prefix: str, errors: list[str]) -> None:
    if value is None:
        return
    if isinstance(template, dict):
        if not isinstance(value, dict):
            errors.append(f"{prefix}: map である必要があります")
            return
        unknown = sorted(set(value.keys()) - set(template.keys()))
        for key in unknown:
            errors.append(f"{prefix}.{key}: 未知の key です")
        for key, template_value in template.items():
            if key in value:
                _validate_against_template(template_value, value[key], f"{prefix}.{key}", errors)
        return
    if isinstance(template, list):
        if isinstance(value, list):
            return
        if isinstance(value, dict):
            unknown = sorted(set(value.keys()) - {"replace", "values", "remove"})
            for key in unknown:
                errors.append(f"{prefix}.{key}: 未知の list patch key です")
            if "replace" in value and not isinstance(value["replace"], bool):
                errors.append(f"{prefix}.replace: bool である必要があります")
            for key in ("values", "remove"):
                if key in value and not isinstance(value[key], list):
                    errors.append(f"{prefix}.{key}: list である必要があります")
            return
        errors.append(f"{prefix}: list または list patch である必要があります")
        return


def validate_overlay_shape(data: dict[str, Any], path: Path, *, allow_blank_name: bool) -> list[str]:
    errors: list[str] = []
    unknown = sorted(set(data.keys()) - ALLOWED_TOP_LEVEL)
    for key in unknown:
        errors.append(f"{path}: unknown top-level key `{key}`")

    if data.get("schema_version") != 3:
        errors.append(f"{path}: schema_version は 3 である必要があります")

    kind = data.get("kind")
    if kind not in {"repo", "workflow"}:
        errors.append(f"{path}: kind は `repo` か `workflow` である必要があります")

    if not allow_blank_name and is_empty_value(data.get("name")):
        errors.append(f"{path}: name は空にできません")

    for section in (
        "source",
        "docs",
        "packaging",
        "security",
        "org_bootstrap",
        "quality_gates",
        "context_pruning",
    ):
        if section in data:
            _validate_against_template(SCHEMA_TEMPLATE[section], data[section], str(path / section), errors)

    notes = data.get("notes")
    if notes is not None and not isinstance(notes, list):
        errors.append(f"{path}: notes は list である必要があります")
    return errors


def merge_overlay(parent: dict[str, Any], child: dict[str, Any]) -> dict[str, Any]:
    merged = normalize_overlay(parent)
    for section in (
        "source",
        "docs",
        "packaging",
        "security",
        "org_bootstrap",
        "quality_gates",
        "context_pruning",
    ):
        merged[section] = merge_with_template(merged[section], child.get(section))
    merged["notes"] = merge_with_template(merged["notes"], child.get("notes"))
    merged["schema_version"] = child.get("schema_version", merged["schema_version"])
    merged["kind"] = child["kind"] if not is_empty_value(child.get("kind")) else merged["kind"]
    merged["name"] = child["name"] if not is_empty_value(child.get("name")) else merged["name"]
    merged["inherits"] = child["inherits"] if not is_empty_value(child.get("inherits")) else merged["inherits"]
    return merged


def resolve_overlay_path(*, repo: str | None = None, overlay: str | None = None) -> Path:
    if bool(repo) == bool(overlay):
        raise OverlayError("`--repo` か `--overlay` のどちらか一方だけを指定してください")
    if repo:
        return (REPO_ROOT / "overlays" / "repos" / repo / "overlay.yaml").resolve()
    return (REPO_ROOT / overlay).resolve()


def resolve_overlay(path: Path, *, _stack: list[Path] | None = None) -> tuple[dict[str, Any], list[str]]:
    if _stack is None:
        _stack = []
    if path in _stack:
        chain = " -> ".join(repo_relative(item) for item in _stack + [path])
        raise OverlayError(f"継承循環を検出しました: {chain}")
    if not path.is_file():
        raise OverlayError(f"overlay が見つかりません: {path}")

    raw = load_overlay_file(path)
    allow_blank_name = "_template" in path.parts
    errors = validate_overlay_shape(raw, path, allow_blank_name=allow_blank_name)
    if errors:
        raise OverlayError("\n".join(errors))

    resolved = normalize_overlay(raw)
    parent_chain: list[str] = []
    inherits = raw.get("inherits")
    if not is_empty_value(inherits):
        parent_path = (REPO_ROOT / str(inherits)).resolve()
        parent_resolved, parent_chain = resolve_overlay(parent_path, _stack=_stack + [path])
        resolved = merge_overlay(parent_resolved, raw)

    final_chain = parent_chain + [repo_relative(path)]
    resolved["resolved_from"] = repo_relative(path)
    resolved["inherits_chain"] = final_chain
    resolved.pop("inherits", None)
    return resolved, final_chain


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resolve Salesforce overlay manifests.")
    parser.add_argument("--repo", help="repo overlay slug under overlays/repos/")
    parser.add_argument("--overlay", help="overlay path relative to repository root")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        path = resolve_overlay_path(repo=args.repo, overlay=args.overlay)
        resolved, _ = resolve_overlay(path)
    except OverlayError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    if args.pretty:
        print(json.dumps(resolved, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(resolved, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
