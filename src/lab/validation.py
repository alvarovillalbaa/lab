"""Validation helpers for experiment specs."""

from __future__ import annotations

from typing import Any


VALID_STAGES = {
    "pretrain",
    "midtrain",
    "sft",
    "dpo",
    "grpo",
    "distill",
    "eval",
    "serve",
    "data",
    "scheduler",
}

REQUIRED_TOP_LEVEL = {
    "experiment_id",
    "stage",
    "provider",
    "model",
    "resources",
    "data",
    "checkpointing",
    "logging",
    "budget",
    "gates",
}


def validate_spec(spec: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    missing = sorted(REQUIRED_TOP_LEVEL - spec.keys())
    for key in missing:
        issues.append(f"missing top-level key: {key}")

    stage = spec.get("stage")
    if stage is not None and stage not in VALID_STAGES:
        issues.append(f"invalid stage: {stage}")

    experiment_id = spec.get("experiment_id")
    if not isinstance(experiment_id, str) or not experiment_id.strip():
        issues.append("experiment_id must be a non-empty string")

    provider = spec.get("provider")
    if not isinstance(provider, str) or not provider.strip():
        issues.append("provider must be a non-empty string")

    model = spec.get("model", {})
    if not isinstance(model, dict):
        issues.append("model must be an object")
    else:
        _positive_int(model, "parameters", "model", issues)
        if "architecture" not in model:
            issues.append("model.architecture is required")

    resources = spec.get("resources", {})
    if not isinstance(resources, dict):
        issues.append("resources must be an object")
    else:
        _positive_int(resources, "gpus", "resources", issues)
        _positive_int(resources, "nodes", "resources", issues)
        _positive_float(resources, "utilization", "resources", issues)

    data = spec.get("data", {})
    if not isinstance(data, dict):
        issues.append("data must be an object")
    else:
        for key in ("train_manifest", "val_manifest", "tokenizer"):
            if not data.get(key):
                issues.append(f"data.{key} is required")

    checkpointing = spec.get("checkpointing", {})
    if not isinstance(checkpointing, dict):
        issues.append("checkpointing must be an object")
    else:
        _positive_int(checkpointing, "interval_steps", "checkpointing", issues)
        if not checkpointing.get("output_uri"):
            issues.append("checkpointing.output_uri is required")

    training = spec.get("training", {})
    if not isinstance(training, dict):
        issues.append("training must be an object when present")
    else:
        if training:
            _positive_int(training, "tokens_target", "training", issues)
            _positive_int(training, "sequence_length", "training", issues)

    budget = spec.get("budget", {})
    if not isinstance(budget, dict):
        issues.append("budget must be an object")
    else:
        _non_negative_float(budget, "hard_cap_usd", "budget", issues)

    gates = spec.get("gates", [])
    if not isinstance(gates, list) or not gates:
        issues.append("gates must be a non-empty list")

    return issues


def _positive_int(obj: dict[str, Any], key: str, path: str, issues: list[str]) -> None:
    value = obj.get(key)
    if not isinstance(value, int) or value <= 0:
        issues.append(f"{path}.{key} must be a positive integer")


def _positive_float(obj: dict[str, Any], key: str, path: str, issues: list[str]) -> None:
    value = obj.get(key)
    if not isinstance(value, (int, float)) or value <= 0:
        issues.append(f"{path}.{key} must be a positive number")


def _non_negative_float(obj: dict[str, Any], key: str, path: str, issues: list[str]) -> None:
    value = obj.get(key)
    if not isinstance(value, (int, float)) or value < 0:
        issues.append(f"{path}.{key} must be a non-negative number")

