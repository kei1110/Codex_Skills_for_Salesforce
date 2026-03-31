#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from overlay_resolver import OverlayError, resolve_overlay, resolve_overlay_path


def _add(target: dict[str, list[str]], bucket: str, path: str, reason: str, reasons: list[dict[str, str]]) -> None:
    if path not in target[bucket]:
        target[bucket].append(path)
        reasons.append({"path": path, "why": reason})


def _changed_files(args: argparse.Namespace) -> list[str]:
    changed = list(args.changed_file or [])
    if args.changed_files_file:
        changed.extend(
            line.strip()
            for line in Path(args.changed_files_file).read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    if not changed:
        raise OverlayError("changed file が指定されていません")
    return changed


def _workspace_root(args: argparse.Namespace) -> Path:
    return Path(args.workspace_root).resolve()


def _read_if_exists(workspace_root: Path, relative_path: str) -> str | None:
    target = workspace_root / relative_path
    if target.is_file():
        return target.read_text(encoding="utf-8")
    return None


def _extract_apex_symbols(content: str) -> set[str]:
    symbols = set(re.findall(r"\bnew\s+([A-Z][A-Za-z0-9_]*)\s*\(", content))
    symbols.update(re.findall(r"\b([A-Z][A-Za-z0-9_]*)\s*\.", content))
    symbols.update(re.findall(r"Database\.executeBatch\(\s*new\s+([A-Z][A-Za-z0-9_]*)", content))
    return symbols


def _extract_lwc_dependencies(content: str) -> tuple[set[str], set[str]]:
    apex_classes = set(re.findall(r"@salesforce/apex/([A-Za-z0-9_]+)\.", content))
    components = set(re.findall(r"from\s+['\"]c/([A-Za-z0-9_/-]+)['\"]", content))
    return apex_classes, components


def _match_apex_class_paths(symbols: set[str], apex_roots: list[str], workspace_root: Path) -> list[str]:
    paths: list[str] = []
    builtins = {"Database", "System", "Schema", "Test", "Trigger", "Math", "JSON", "String", "Date", "Datetime"}
    for symbol in symbols:
        if symbol in builtins:
            continue
        for root in apex_roots:
            candidate = f"{root.rstrip('/')}/{symbol}.cls"
            if (workspace_root / candidate).is_file() and candidate not in paths:
                paths.append(candidate)
    return paths


def _match_lwc_component_paths(components: set[str], lwc_roots: list[str], workspace_root: Path) -> list[str]:
    paths: list[str] = []
    for component in components:
        name = component.split("/")[-1]
        for root in lwc_roots:
            candidate = f"{root.rstrip('/')}/{name}"
            if (workspace_root / candidate).exists() and candidate not in paths:
                paths.append(candidate)
    return paths


def _package_directories(workspace_root: Path) -> list[str]:
    sfdx_project = workspace_root / "sfdx-project.json"
    if not sfdx_project.is_file():
        return []
    try:
        payload = json.loads(sfdx_project.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    package_dirs: list[str] = []
    for item in payload.get("packageDirectories", []):
        if isinstance(item, dict) and item.get("path"):
            package_dirs.append(str(item["path"]).rstrip("/"))
    return package_dirs


def _package_for_path(path: str, package_dirs: list[str]) -> str | None:
    matches = [candidate for candidate in package_dirs if path.startswith(candidate.rstrip("/") + "/") or path == candidate]
    if not matches:
        return None
    return max(matches, key=len)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prune Salesforce context based on changed files.")
    parser.add_argument("--repo", help="repo overlay slug under overlays/repos/")
    parser.add_argument("--overlay", help="overlay path relative to repository root")
    parser.add_argument("--changed-file", action="append", default=[], help="changed file path")
    parser.add_argument("--changed-files-file", help="file that contains changed file paths")
    parser.add_argument("--workspace-root", default=".", help="workspace root for lightweight dependency lookup")
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        overlay_path = resolve_overlay_path(repo=args.repo, overlay=args.overlay)
        resolved, _ = resolve_overlay(overlay_path)
        changed_files = _changed_files(args)
        workspace_root = _workspace_root(args)
    except (OverlayError, OSError) as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    selected = {"source": [], "docs": [], "tests": [], "metadata": []}
    reasons: list[dict[str, str]] = []
    docs = resolved["docs"]
    security_paths = resolved["source"]["permissionsets"] + resolved["source"]["permissionsetgroups"] + resolved["source"]["profiles"]
    apex_roots = resolved["source"]["apex"]
    lwc_roots = resolved["source"]["lwc"]
    package_dirs = _package_directories(workspace_root)

    for changed in changed_files:
        _add(selected, "source", changed, "changed file", reasons)

        if changed.endswith(".cls") and not changed.endswith("Test.cls"):
            sibling = changed.replace(".cls", "Test.cls")
            _add(selected, "tests", sibling, "apex test heuristic", reasons)
            content = _read_if_exists(workspace_root, changed)
            if content:
                for candidate in _match_apex_class_paths(_extract_apex_symbols(content), apex_roots, workspace_root):
                    if candidate != changed:
                        _add(selected, "source", candidate, "apex dependency heuristic", reasons)
            for doc in docs["specs"] + docs["technical"]:
                _add(selected, "docs", doc, "apex change doc heuristic", reasons)

        if changed.endswith(".trigger"):
            handler = changed.replace("/triggers/", "/classes/").replace(".trigger", "Handler.cls")
            handler_test = changed.replace("/triggers/", "/classes/").replace(".trigger", "HandlerTest.cls")
            _add(selected, "tests", handler, "trigger handler heuristic", reasons)
            _add(selected, "tests", handler_test, "trigger test heuristic", reasons)
            content = _read_if_exists(workspace_root, changed)
            if content:
                for candidate in _match_apex_class_paths(_extract_apex_symbols(content), apex_roots, workspace_root):
                    _add(selected, "source", candidate, "trigger dependency heuristic", reasons)

        if "/lwc/" in changed:
            component_dir = changed.split("/lwc/")[0] + "/lwc/" + changed.split("/lwc/")[1].split("/")[0]
            _add(selected, "source", component_dir, "lwc component heuristic", reasons)
            _add(selected, "tests", f"{component_dir}/__tests__", "lwc test heuristic", reasons)
            content = _read_if_exists(workspace_root, changed)
            if content and changed.endswith(".js"):
                apex_classes, components = _extract_lwc_dependencies(content)
                for candidate in _match_apex_class_paths(apex_classes, apex_roots, workspace_root):
                    _add(selected, "source", candidate, "lwc apex dependency heuristic", reasons)
                for candidate in _match_lwc_component_paths(components, lwc_roots, workspace_root):
                    _add(selected, "source", candidate, "lwc component dependency heuristic", reasons)
            for doc in docs["screens"] + docs["specs"]:
                _add(selected, "docs", doc, "lwc doc heuristic", reasons)

        if any(token in changed for token in ("/permissionsets/", "/permissionsetgroups/", "/profiles/")):
            for path in security_paths:
                _add(selected, "metadata", path, "security metadata heuristic", reasons)
            for doc in docs["specs"] + docs["technical"]:
                _add(selected, "docs", doc, "security doc heuristic", reasons)

        if any(token in changed for token in ("/flows/", "/objects/", "/approvalProcesses/", "/recordTypes/")):
            for doc in docs["specs"] + docs["screens"] + docs["technical"]:
                _add(selected, "docs", doc, "metadata change doc heuristic", reasons)
            _add(selected, "metadata", changed, "metadata change", reasons)

        package_dir = _package_for_path(changed, package_dirs)
        if package_dir:
            _add(selected, "metadata", package_dir, "package boundary heuristic", reasons)

    result = {
        "repo": args.repo or resolved["name"],
        "changed_files": changed_files,
        "selected": selected,
        "reasons": reasons,
    }
    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
