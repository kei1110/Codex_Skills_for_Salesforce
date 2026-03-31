#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from overlay_resolver import OverlayError, resolve_overlay, resolve_overlay_path
from static_analysis import evaluate_thresholds


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate static analysis thresholds against overlay quality gates.")
    parser.add_argument("--repo", help="repo overlay slug under overlays/repos/")
    parser.add_argument("--overlay", help="overlay path relative to repository root")
    parser.add_argument("--report", action="append", default=[], help="normalized report JSON path")
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        overlay_path = resolve_overlay_path(repo=args.repo, overlay=args.overlay)
        resolved, _ = resolve_overlay(overlay_path)
        reports = [json.loads(Path(path).read_text(encoding="utf-8")) for path in args.report]
        blocking_rules = resolved["quality_gates"]["static_analysis"]["blocking_rules"]
        result = evaluate_thresholds(
            reports,
            resolved["quality_gates"]["static_analysis"]["thresholds"],
            blocking_rules=blocking_rules,
        )
    except (OverlayError, OSError, json.JSONDecodeError) as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
