#!/usr/bin/env python3
"""Acceptance checks for already installed packages; never installs or builds."""
from __future__ import annotations

import argparse
import importlib
import importlib.metadata as metadata
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import MagicMock, patch


MODULES = {
    "experiment-kit": "experiment_kit",
    "compute-economics": "compute_economics",
    "compute-planner": "compute_planner",
    "model-distillation": "model_distillation",
    "open-evals-sdk": "open_evals_sdk",
    "clous-llm-lab": "lab",
}
PROFILES = {
    "base": {"experiment-kit"},
    "economics": {"experiment-kit", "compute-economics"},
    "planning": {"experiment-kit", "compute-planner"},
    "compute": {"experiment-kit", "compute-economics", "compute-planner"},
    "distillation": {"experiment-kit", "model-distillation"},
    "evals": {"experiment-kit", "open-evals-sdk"},
    "cpu": {"experiment-kit", "compute-economics", "compute-planner", "model-distillation"},
    "full": {"experiment-kit", "compute-economics", "compute-planner", "model-distillation", "open-evals-sdk"},
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def check_install(name):
    distribution = metadata.distribution(name)
    module = importlib.import_module(MODULES[name])
    location = Path(module.__file__).resolve()
    prefix = Path(sys.prefix).resolve()
    require(location.is_relative_to(prefix), f"{name} imported outside the isolated environment")
    direct = distribution.read_text("direct_url.json")
    if direct:
        require(not json.loads(direct).get("dir_info", {}).get("editable"), f"{name} is editable")
    return {
        "version": distribution.version,
        "module": "<environment>/" + str(location.relative_to(prefix)),
    }


def check_cli(name, arguments, workdir, *, expected=0):
    command = Path(sys.prefix) / "bin" / name
    require(command.is_file(), f"installed console command missing: {name}")
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    environment.pop("PYTHONHOME", None)
    result = subprocess.run(
        [str(command), *arguments], cwd=workdir, env=environment,
        text=True, capture_output=True, timeout=15, check=False,
    )
    require(result.returncode == expected, f"{name} returned {result.returncode}: {result.stderr}")
    return result.stdout


def record_fixture():
    return {
        "schema_version": 1, "experiment_id": "installed-acceptance",
        "kind": "cpu_fixture", "objective": "Exercise installed package interfaces",
        "code_ref": "authored-fixture", "seed": 0, "inputs": [],
        "resources": {"device": "cpu", "gpus": 0},
    }


def check_sdk():
    client_type = importlib.import_module("open_evals_sdk").OpenEvalsPythonClient
    response = MagicMock()
    response.__enter__.return_value.status = 202
    with patch("urllib.request.urlopen", return_value=response) as send:
        status = client_type("https://fixture.invalid", "fixture-key").submit_trace({"traceId": "fixture"})
    require(status == 202 and send.call_count == 1, "SDK transport result changed")
    request = send.call_args.args[0]
    require(request.full_url == "https://fixture.invalid/api/v1/traces", "SDK trace route changed")
    require(request.get_header("Authorization") == "Bearer fixture-key", "SDK authorization changed")
    require(json.loads(request.data) == {"traceId": "fixture"}, "SDK serialized payload changed")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--distribution", required=True, choices=MODULES)
    parser.add_argument("--profile", choices=PROFILES)
    parser.add_argument("--code-ref", help="Exact Lab source identity for the installed CPU fixture")
    args = parser.parse_args(argv)
    try:
        require(sys.flags.isolated, "invoke this checker with python -I")
        require(sys.prefix != sys.base_prefix, "a fresh isolated virtual environment is required")
        if args.distribution == "clous-llm-lab":
            require(args.profile is not None, "Lab requires an explicit installation profile")
            expected = PROFILES[args.profile] | {"clous-llm-lab"}
        else:
            require(args.profile is None, "profiles apply only to Lab")
            expected = {args.distribution}
        present = {item.metadata["Name"] for item in metadata.distributions()}
        require(not ((set(MODULES) | {"open-evals-optimizers"}) - expected) & present,
                "unexpected ecosystem packages would weaken independent-install proof")
        checked = {name: check_install(name) for name in sorted(expected)}
        cli_checks = []
        with tempfile.TemporaryDirectory(prefix="lab-installed-cases-") as temporary:
            workdir = Path(temporary)
            fixture = workdir / "cpu.json"
            fixture.write_text(json.dumps(record_fixture()), encoding="utf-8")
            if args.distribution == "experiment-kit":
                require(importlib.import_module("experiment_kit").validate_record(record_fixture()) == [],
                        "installed CPU record validation failed")
                check_cli("experiment-kit", [str(fixture), "--profile", "record"], workdir)
                cli_checks.append("CPU record")
            elif args.distribution == "compute-planner":
                output = check_cli("compute-planner", ["route", "pretrain_smoke"], workdir)
                require(output.splitlines() == ["local", "runpod", "lambda_cloud"], "provider ordering changed")
                planning = importlib.import_module("compute_planner")
                cheap = planning.Job("cheap", "evals", 1, 1, 1)
                valuable = planning.Job("valuable", "evals", 10, 2, 1)
                require(planning.value_first([cheap, valuable])[0].job_id == "valuable",
                        "installed job ranking changed")
                require(importlib.util.find_spec("compute_planner.costing") is None,
                        "planner still contains extracted economics implementation")
                require(not any(hasattr(planning, name) for name in
                                ("CostEstimate", "estimate_from_spec", "format_estimate")),
                        "planner still reexports economics")
                check_cli("compute-planner", ["estimate-cost", str(fixture)], workdir, expected=2)
                cli_checks.append("provider routing and job ordering")
            elif args.distribution == "compute-economics":
                spec = {"model": {"parameters": 10}, "training": {"tokens_target": 100},
                        "resources": {"gpus": 1, "gpu_hourly_usd": 0}}
                estimate = importlib.import_module("compute_economics").estimate_from_spec(spec)
                require(estimate.training_flops == 6000, "installed estimate changed")
                estimate_file = workdir / "estimate.json"
                estimate_file.write_text(json.dumps(spec), encoding="utf-8")
                check_cli("compute-economics", ["estimate-cost", str(estimate_file)], workdir)
                cli_checks.append("training estimate")
            elif args.distribution == "model-distillation":
                output = json.loads(check_cli("model-distillation", ["demo"], workdir))
                require(output["source"] == "authored_fixture" and output["pair"]["chosen"] == "4",
                        "installed preference fixture changed")
                cli_checks.append("preference fixture")
            elif args.distribution == "open-evals-sdk":
                check_sdk()
            else:
                check_cli("llm-lab", ["validate", str(fixture), "--profile", "record"], workdir)
                cli_checks.append("CPU record")
                workflow = importlib.import_module("lab.workflow")
                composition = workflow.declared_composition()
                require(composition["schema_version"] == 1 and "components" in composition,
                        "installed composition resource missing or invalid")
                if "compute-planner" in expected:
                    check_cli("llm-lab", ["route", "pretrain_smoke"], workdir)
                    cli_checks.append("provider routing")
                else:
                    check_cli("llm-lab", ["route", "pretrain_smoke"], workdir, expected=2)
                    cli_checks.append("missing optional planner handled")
                estimate_file = workdir / "llm-estimate.json"
                example = Path(__file__).resolve().parents[1] / "configs/experiments/lab_124m_pretrain_smoke.json"
                estimate_file.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
                if "compute-economics" in expected:
                    output = check_cli("llm-lab", ["estimate-cost", str(estimate_file)], workdir)
                    require("cost" in output.lower(), "Lab estimate command returned no cost")
                    cli_checks.append("economics estimate")
                else:
                    check_cli("llm-lab", ["estimate-cost", str(estimate_file)], workdir, expected=2)
                    cli_checks.append("missing optional economics handled")
                if {"compute-economics", "compute-planner", "model-distillation"} <= expected:
                    require(bool(args.code_ref), "CPU composition requires --code-ref")
                    output = json.loads(check_cli("llm-lab", ["smoke", "--code-ref", args.code_ref], workdir))
                    require(output["source"] == "authored_fixture"
                            and output["output"]["pair"]["chosen"] == "4",
                            "installed CPU composition failed")
                    require(output["record"]["resources"] == {"device": "cpu", "gpus": 0},
                            "CPU composition misstates executed resources")
                    estimate = output["planning"]["estimate"]
                    require(estimate["source"] == "authored_assumptions"
                            and estimate["observed_billing"] is False
                            and estimate["estimated_cost_usd"] > 0,
                            "hypothetical cost estimate lost its provenance")
                    cli_checks.append("CPU composition")
                if "open-evals-sdk" in expected:
                    check_sdk()
        print(json.dumps({"status": "passed", "distribution": args.distribution,
                          "profile": args.profile, "installed": checked, "cli_checks": cli_checks,
                          "sdk_transport": "mocked" if "open-evals-sdk" in expected else "not used"}))
        return 0
    except (RuntimeError, ImportError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
