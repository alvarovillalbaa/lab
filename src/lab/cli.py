"""Lab composition commands; reusable behavior lives in component packages."""
import argparse
import json
import sys
from pathlib import Path

from experiment_kit import validate_record, validate_spec


def main(argv=None):
    parser = argparse.ArgumentParser(prog="llm-lab")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("spec", type=Path)
    validate.add_argument("--profile", choices=("llm", "record"), default="llm")
    sub.add_parser("estimate-cost").add_argument("spec", type=Path)
    sub.add_parser("verify").add_argument("request", type=Path)
    sub.add_parser("route").add_argument("job_type")
    sub.add_parser("smoke").add_argument("--code-ref", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            spec = json.loads(args.spec.read_text(encoding="utf-8"))
            if not isinstance(spec, dict):
                raise ValueError("spec must be an object")
            issues = (validate_spec if args.profile == "llm" else validate_record)(spec)
            if issues:
                for issue in issues:
                    print(f"ERROR: {issue}", file=sys.stderr)
                return 1
            print(f"OK: {args.spec}")
        elif args.command == "estimate-cost":
            from compute_economics import estimate_from_spec, format_estimate
            spec = json.loads(args.spec.read_text(encoding="utf-8"))
            if not isinstance(spec, dict):
                raise ValueError("spec must be an object")
            issues = validate_spec(spec)
            if issues:
                for issue in issues:
                    print(f"ERROR: {issue}", file=sys.stderr)
                return 1
            print(format_estimate(estimate_from_spec(spec)))
        elif args.command == "verify":
            from verification_runtime.cli import main as verify_main
            return verify_main([str(args.request)])
        elif args.command == "route":
            from compute_planner import providers_for
            print("\n".join(providers_for(args.job_type)))
        else:
            from .workflow import run_smoke
            print(json.dumps(run_smoke(code_ref=args.code_ref), indent=2))
    except ImportError as exc:
        profiles = {"estimate-cost": "economics or compute", "route": "planning or compute", "verify": "verification or distillation", "smoke": "compute and distillation"}
        print(f"Missing optional component: {exc.name}. Install Lab's {profiles.get(args.command, 'required')} profile.", file=sys.stderr)
        return 2
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
