#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from static_analysis import StaticAnalysisError, parse_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse static analysis reports into normalized JSON.")
    parser.add_argument("--parser", required=True, help="pmd-json or sfdx-scanner-json")
    parser.add_argument("--input", required=True, help="report file path")
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = parse_report(Path(args.input), args.parser)
    except (OSError, StaticAnalysisError, json.JSONDecodeError) as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
