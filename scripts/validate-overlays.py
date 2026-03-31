#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from overlay_resolver import OverlayError, REPO_ROOT, load_overlay_file, normalize_overlay, resolve_overlay, validate_overlay_shape


def iter_overlay_files() -> list[Path]:
    return sorted((REPO_ROOT / "overlays").glob("**/overlay.yaml"))


def should_allow_blank_name(path: Path) -> bool:
    return "_template" in path.parts


def validate_file(path: Path) -> list[str]:
    raw = load_overlay_file(path)
    errors = validate_overlay_shape(raw, path, allow_blank_name=should_allow_blank_name(path))
    resolved = None
    if not errors and not should_allow_blank_name(path):
        try:
            resolved, _ = resolve_overlay(path)
        except OverlayError as exc:
            errors.append(str(exc))
    normalized = resolved or normalize_overlay(raw)
    if not should_allow_blank_name(path) and normalized.get("kind") == "repo":
        if normalized["schema_version"] != 3:
            errors.append(f"{path}: schema_version 3 が必要です")
        if not normalized["packaging"]["package_dirs"]:
            errors.append(f"{path}: packaging.package_dirs は repo overlay で必須です")
        if not (
            normalized["source"]["apex"]
            or normalized["source"]["lwc"]
            or normalized["source"]["triggers"]
            or normalized["source"]["objects"]
        ):
            errors.append(f"{path}: source に主要 metadata path が必要です")
        if not normalized["quality_gates"]["blocking_rules"]:
            errors.append(f"{path}: quality_gates.blocking_rules は repo overlay で必須です")
        if not (
            normalized["security"]["permission_sets"]["user"]
            or normalized["security"]["permission_sets"]["admin"]
            or normalized["security"]["permission_sets"]["elevated"]
            or normalized["security"]["permission_set_groups"]
        ):
            errors.append(f"{path}: security に Permission Set または PSG の定義が必要です")
        static_analysis = normalized["quality_gates"]["static_analysis"]
        allowed_parsers = {"pmd-json", "sfdx-scanner-json"}
        for command in static_analysis["commands"]:
            if not isinstance(command, dict):
                errors.append(f"{path}: static_analysis.commands は map の list である必要があります")
                continue
            for key in ("name", "run", "parser"):
                if not command.get(key):
                    errors.append(f"{path}: static_analysis.commands に {key} が必要です")
            if command.get("parser") and command["parser"] not in allowed_parsers:
                errors.append(f"{path}: unsupported static analysis parser `{command['parser']}`")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate overlay manifests.")
    parser.add_argument("--overlay", help="validate one overlay path relative to repository root")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    targets = [REPO_ROOT / args.overlay] if args.overlay else iter_overlay_files()
    errors: list[str] = []
    for target in targets:
        if not target.is_file():
            errors.append(f"{target}: overlay が見つかりません")
            continue
        errors.extend(validate_file(target))

    if errors:
        for error in errors:
            print(f"[error] {error}", file=sys.stderr)
        return 1

    print("[ok] overlay 構成は整合しています")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
