"""Scheduler scoring primitives for cost-aware LLM research portfolios."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Job:
    job_id: str
    job_type: str
    expected_value: float
    expected_cost_usd: float
    risk: float
    deadline_hours: float | None = None


def value_per_dollar(job: Job) -> float:
    denominator = max(job.expected_cost_usd, 0.01) * max(job.risk, 0.01)
    return job.expected_value / denominator


def cheapest_first(jobs: list[Job]) -> list[Job]:
    return sorted(jobs, key=lambda job: (job.expected_cost_usd, -job.expected_value, job.job_id))


def value_first(jobs: list[Job]) -> list[Job]:
    return sorted(jobs, key=lambda job: (-value_per_dollar(job), job.expected_cost_usd, job.job_id))


def fifo(jobs: list[Job]) -> list[Job]:
    return list(jobs)

