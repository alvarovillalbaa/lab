"""Provider routing defaults for the LLM lab."""

from __future__ import annotations


ROUTES: dict[str, list[str]] = {
    "pretrain_smoke": ["local", "runpod", "lambda_cloud"],
    "pretrain_serious": ["local_slurm", "lambda_cloud", "coreweave", "baseten_training"],
    "data_processing": ["local_cpu", "local_k8s", "coreweave_k8s"],
    "teacher_generation": ["local_vllm", "together", "fireworks", "baseten"],
    "posttraining_sft": ["tinker", "trl_local", "baseten_training"],
    "posttraining_rl": ["tinker", "verl_local", "openrlhf_lambda"],
    "distillation": ["local", "tinker", "baseten_training"],
    "evals": ["local", "runpod", "baseten"],
    "serving_public": ["baseten", "coreweave", "together"],
    "serving_benchmark": ["local_vllm", "lambda_cloud", "coreweave"],
}


def providers_for(job_type: str) -> list[str]:
    try:
        return ROUTES[job_type]
    except KeyError as exc:
        known = ", ".join(sorted(ROUTES))
        raise KeyError(f"unknown job type {job_type!r}; known job types: {known}") from exc

