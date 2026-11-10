# Architecture

The lab uses one experiment contract and multiple execution backends.

```text
experiment spec
  -> provider router
  -> local trainer / OLMo-core / TorchTitan / TRL / Tinker / Baseten / vLLM
  -> artifacts
  -> evals
  -> reports
```

## Execution Lanes

### Local From-Scratch Lane

Use for:

- Tiny transformer.
- 20M to 60M smoke training.
- Unit tests.
- Data pipeline tests.
- Local generation.
- Local vLLM benchmark when a compatible model exists.

This lane is mandatory because it proves the lab is not only provider glue.

### NVIDIA/PyTorch Lane

Use for:

- OLMo-core pretraining.
- TorchTitan experiments.
- Megatron/NeMo experiments when needed.
- Slurm or Kubernetes/Kueue execution.
- SkyPilot routing to raw GPU providers.

### Managed Post-Training Lane

Use for:

- Tinker SFT, DPO, RL, and distillation when access exists.
- TRL as local fallback.
- verl/OpenRLHF for scaled RL after local loops work.

### Serving Lane

Use for:

- Baseten public endpoint.
- Local/self-hosted vLLM benchmark.
- SGLang for structured and multi-turn workloads.
- TensorRT-LLM/Triton only after model stability.

## Provider Interface

Every provider adapter should implement:

```text
submit_job()
cancel_job()
get_logs()
get_metrics()
sync_data()
upload_checkpoint()
download_checkpoint()
launch_endpoint()
stop_endpoint()
estimate_cost()
```

## Canonical Storage Rule

Object storage is the source of truth.

- Local NVMe is cache.
- Parallel filesystems are performance optimizations.
- Provider-specific paths must never be the only copy.
- Every dataset shard, tokenizer, checkpoint, and eval result must have a hash.

## Routing Policy

Routing is job-type based:

- `pretrain_smoke`: local, RunPod, Lambda.
- `pretrain_serious`: local Slurm, Lambda, CoreWeave, OCI, Azure.
- `data_processing`: local CPU, Kubernetes batch, cloud batch.
- `teacher_generation`: local vLLM, Together, Fireworks, Baseten.
- `posttraining_sft`: Tinker, TRL locally, Baseten Loops.
- `posttraining_rl`: Tinker, verl, OpenRLHF.
- `evals`: local, cheap GPUs, managed endpoints.
- `serving_public`: Baseten first.
- `serving_benchmark`: local vLLM first.

## Security Boundaries

- Provider credentials never go in configs.
- Public demos must use a safety gateway.
- Internal vLLM/SGLang ports must not be exposed directly.
- Distillation data must include license/source metadata.
- Commercial API outputs require legal review before model training.

