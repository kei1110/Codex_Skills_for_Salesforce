#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prune Salesforce context based on changed files.")
    parser.add_argument("--repo", help="repo overlay slug under overlays/repos/")
    parser.add_argument("--overlay", help="overlay path relative to repository root")
    parser.add_argument("--changed-file", action="append", default=[], help="changed file path")
    parser.add_argument("--changed-files-file", help="file that contains changed file paths")
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        overlay_path = resolve_overlay_path(repo=args.repo, overlay=args.overlay)
        resolved, _ = resolve_overlay(overlay_path)
        changed_files = _changed_files(args)
    except (OverlayError, OSError) as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    selected = {"source": [], "docs": [], "tests": [], "metadata": []}
    reasons: list[dict[str, str]] = []
    docs = resolved["docs"]
    security_paths = resolved["source"]["permissionsets"] + resolved["source"]["permissionsetgroups"] + resolved["source"]["profiles"]

    for changed in changed_files:
        _add(selected, "source", changed, "changed file", reasons)

        if changed.endswith(".cls") and not changed.endswith("Test.cls"):
            sibling = changed.replace(".cls", "Test.cls")
            _add(selected, "tests", sibling, "apex test heuristic", reasons)
            for doc in docs["specs"] + docs["technical"]:
                _add(selected, "docs", doc, "apex change doc heuristic", reasons)

        if changed.endswith(".trigger"):
            handler = changed.replace("/triggers/", "/classes/").replace(".trigger", "Handler.cls")
            handler_test = changed.replace("/triggers/", "/classes/").replace(".trigger", "HandlerTest.cls")
            _add(selected, "tests", handler, "trigger handler heuristic", reasons)
            _add(selected, "tests", handler_test, "trigger test heuristic", reasons)

        if "/lwc/" in changed:
            component_dir = changed.split("/lwc/")[0] + "/lwc/" + changed.split("/lwc/")[1].split("/")[0]
            _add(selected, "source", component_dir, "lwc component heuristic", reasons)
            _add(selected, "tests", f"{component_dir}/__tests__", "lwc test heuristic", reasons)
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
