# Libraries And Providers

This file records the provider and library choices from `docs/specs/` in one
place. Live pricing, product access, and exact version compatibility must be
verified before paid runs.

## Provider Strategy

Use a multi-provider LLM factory:

1. Local/from-scratch first for credibility.
2. Raw GPU providers for pretraining scale.
3. Tinker for managed post-training when access is available.
4. Baseten for public serving and optional managed training.
5. SkyPilot/provider adapters for routing, recovery, and cost-aware scheduling.

## Provider Roles

| Provider | Use | Priority |
| --- | --- | --- |
| local | tiny trainer, smoke runs, evals, local serving benchmark | mandatory |
| local_slurm | multi-GPU or multi-node pretraining | high when hardware exists |
| local_k8s | serving, batch eval, dashboards | high when hardware exists |
| Baseten | public endpoint, deploy-from-checkpoint, optional training | high |
| Tinker | SFT, DPO, RL, distillation, self-distillation | high if access exists |
| Lambda | simple H100/B200-style raw GPU nodes | high |
| CoreWeave | Kubernetes-native serious GPU workloads | high |
| RunPod | cheap smoke jobs and disposable workers | medium |
| Together | teacher inference, endpoints, possible clusters | medium |
| Fireworks | teacher APIs and fine-tuning comparisons | medium |
| GCP TPU | JAX/MaxText TPU lane only | optional |
| Azure/OCI/AWS | enterprise or reserved scale | optional initially |

## Training Libraries

Primary:

- PyTorch.
- OLMo-core.
- TorchTitan.
- Transformers.
- Accelerate.
- Safetensors.
- Hugging Face Datasets.
- Tokenizers.
- SentencePiece.

Scale/performance:

- FSDP2 / DTensor / DeviceMesh.
- Megatron-Core.
- NeMo.
- DeepSpeed ZeRO.
- FlashAttention.
- Transformer Engine.
- Liger Kernel.
- Triton.

TPU lane only:

- JAX.
- Flax.
- Orbax Checkpoint.
- MaxText.

## Post-Training Libraries

- Tinker for managed SFT, DPO, RL, distillation, and self-distillation.
- TRL for local SFT/DPO/GRPO.
- PEFT for LoRA/QLoRA.
- verl for serious RL research.
- OpenRLHF for Ray/vLLM-style RLHF.
- Ray for rollouts, evals, and distributed workers.

## Serving Libraries

Default:

- vLLM.

Additional:

- SGLang for structured, cached, multi-turn, and agentic workloads.
- TensorRT-LLM/Triton for optimized NVIDIA production path after stability.
- llama.cpp/GGUF for local quantized demos.

Avoid as a new default:

- TGI, unless a specific deployment requires it.

## Data Libraries

- Hugging Face Datasets.
- DataTrove.
- Dolma Toolkit.
- PyArrow.
- Polars.
- DuckDB.
- fsspec.
- s3fs/gcsfs/adlfs.
- boto3.
- smart_open.
- zstandard.
- xxhash.
- datasketch.
- simhash.
- ftfy.
- trafilatura.
- resiliparse.
- Presidio analyzer/anonymizer.
- fastText or lingua language detection.

## Evaluation Libraries

- lm-evaluation-harness.
- Inspect AI.
- LightEval.
- OpenAI Evals for app/workflow eval patterns.
- pytest or unittest.
- hypothesis.
- promptfoo or deepeval for app-level checks when useful.

## Orchestration

- Slurm for serious synchronous training.
- Kubernetes/Kueue for provider-native batch and serving control plane.
- SkyPilot for cross-provider launcher and recovery.
- Ray for rollouts, evals, data jobs, and RL workers.
- Argo Workflows for repeatable workflows.
- Terraform/Pulumi/Ansible for infrastructure.

## Storage

Source of truth:

- S3-compatible object storage.

Local/performance layers:

- NVMe cache.
- NFS for small clusters.
- Lustre/WEKA/VAST/Parallelstore-style systems only when needed.

Rule:

Provider-local filesystems are never the only copy.

## Observability

- W&B or MLflow for experiment tracking.
- Prometheus and Grafana for metrics.
- NVIDIA DCGM Exporter for GPU telemetry.
- OpenTelemetry for traces, logs, and metrics.
- Loki or Elasticsearch for logs.
- nsys/ncu for profiling.

Required metrics:

- Training loss.
- Validation loss.
- Tokens/sec.
- Tokens/sec/GPU.
- MFU.
- GPU utilization.
- GPU memory.
- Dataloader wait time.
- Checkpoint write time.
- Checkpoint size.
- Cost per 1B tokens.
- Eval score by domain.
- Serving time-to-first-token.
- Serving output tokens/sec.
- Serving p50/p95/p99 latency.

## System Dependencies

NVIDIA nodes:

- Ubuntu 22.04 or 24.04.
- NVIDIA driver.
- NVIDIA Container Toolkit.
- Docker or containerd.
- NCCL.
- cuDNN.
- Fabric Manager where required.
- OFED/MOFED for InfiniBand.
- NCCL tests.
- iperf3.
- nvidia-smi.
- nsys.
- ncu.
- dcgmi.

Kubernetes clusters:

- Kubernetes.
- Helm.
- NVIDIA GPU Operator.
- NVIDIA Network Operator.
- Kueue.
- Prometheus Operator.
- Grafana.
- Loki or Elasticsearch.
- Argo Workflows.
- Argo CD.
- cert-manager.
- external-secrets.
- ingress-nginx or Envoy Gateway.

Slurm clusters:

- Slurm.
- Munge.
- Enroot and Pyxis, or Apptainer.
- NFS or Lustre client.
- NCCL tests.
- node exporter.
- DCGM exporter.

## Explicit Open Items

- Confirm whether "Base10" means Baseten for this project.
- Clarify the expected role of PorTAL.
- Confirm Tinker access and supported export path.
- Verify current provider pricing and availability before paid runs.
- Verify model/data licenses before training or release.

