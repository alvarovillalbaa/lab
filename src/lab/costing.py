"""Cost and compute estimates for LLM training experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


FLOPS_PER_PARAM_TOKEN = 6


@dataclass(frozen=True)
class CostEstimate:
    parameters: int
    tokens: int
    gpu_count: int
    gpu_tflops: float
    gpu_hourly_usd: float
    utilization: float
    overhead_multiplier: float

    @property
    def training_flops(self) -> float:
        return FLOPS_PER_PARAM_TOKEN * self.parameters * self.tokens

    @property
    def raw_gpu_hours(self) -> float:
        sustained_flops_per_hour = (
            self.gpu_count * self.gpu_tflops * 1_000_000_000_000 * 3600 * self.utilization
        )
        if sustained_flops_per_hour <= 0:
            raise ValueError("sustained FLOPs per hour must be positive")
        return self.training_flops / sustained_flops_per_hour

    @property
    def raw_cost_usd(self) -> float:
        return self.raw_gpu_hours * self.gpu_count * self.gpu_hourly_usd

    @property
    def realistic_cost_usd(self) -> float:
        return self.raw_cost_usd * self.overhead_multiplier


def estimate_from_spec(spec: dict[str, Any]) -> CostEstimate:
    model = spec.get("model", {})
    resources = spec.get("resources", {})
    budget = spec.get("budget", {})
    training = spec.get("training", {})

    return CostEstimate(
        parameters=int(model["parameters"]),
        tokens=int(training["tokens_target"]),
        gpu_count=int(resources.get("gpus", 1)),
        gpu_tflops=float(resources.get("gpu_tflops", 82.0)),
        gpu_hourly_usd=float(resources.get("gpu_hourly_usd", 0.0)),
        utilization=float(resources.get("utilization", 0.35)),
        overhead_multiplier=float(budget.get("overhead_multiplier", 2.0)),
    )


def format_estimate(estimate: CostEstimate) -> str:
    return "\n".join(
        [
            f"parameters: {estimate.parameters}",
            f"tokens: {estimate.tokens}",
            f"training_flops: {estimate.training_flops:.3e}",
            f"raw_gpu_hours: {estimate.raw_gpu_hours:.2f}",
            f"raw_cost_usd: {estimate.raw_cost_usd:.2f}",
            f"realistic_cost_usd: {estimate.realistic_cost_usd:.2f}",
        ]
    )

