"""Command-line helpers for the LLM lab skeleton."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lab.costing import estimate_from_spec, format_estimate
from lab.routing import providers_for
from lab.validation import validate_spec


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="llm-lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="validate an experiment spec")
    validate_parser.add_argument("spec", type=Path)

    estimate_parser = subparsers.add_parser("estimate-cost", help="estimate training cost")
    estimate_parser.add_argument("spec", type=Path)

    route_parser = subparsers.add_parser("route", help="print preferred providers for a job type")
    route_parser.add_argument("job_type")

    args = parser.parse_args(argv)

    if args.command == "validate":
        return _validate(args.spec)
    if args.command == "estimate-cost":
        return _estimate(args.spec)
    if args.command == "route":
        return _route(args.job_type)

    parser.error(f"unknown command: {args.command}")
    return 2


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _validate(path: Path) -> int:
    spec = _load_json(path)
    issues = validate_spec(spec)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1
    print(f"OK: {path}")
    return 0


def _estimate(path: Path) -> int:
    spec = _load_json(path)
    issues = validate_spec(spec)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1
    print(format_estimate(estimate_from_spec(spec)))
    return 0


def _route(job_type: str) -> int:
    try:
        providers = providers_for(job_type)
    except KeyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("\n".join(providers))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

