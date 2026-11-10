You can use Codex to compress the **implementation**, but you still need to make the **research, infrastructure, legal, and product decisions** yourself. In 1–2 days, the realistic target is a **serious vertical slice**: tiny/pretraining smoke run, post-training run, distillation-data pipeline, eval suite, and serving endpoint. A truly “fully scaled” experiment still depends on GPU time, provider access, data processing, and evaluation cycles.

Also: you probably mean **Baseten**, not Base10. Base10 Partners is a VC firm/content source; **Baseten** is the AI training/inference platform people are recommending.

## My recommended provider split

Use **three lanes**, not one provider for everything.

| Lane                                          | Best default                                    | Why                                                                                                                                  |
| --------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| From-scratch pretraining                      | Raw GPU cloud + OLMo-core/TorchTitan + SkyPilot | This proves you understand real training infrastructure. Managed APIs hide too much.                                                 |
| Post-training / RL / distillation experiments | Tinker, if you get access                       | Tinker is very strong for fast LoRA/SFT/RL/DPO/distillation loops on large open-weight models without managing distributed training. |
| Public serving                                | Baseten, plus self-hosted vLLM benchmark        | Baseten is good for production deployment; self-hosted vLLM gives you reproducibility credibility.                                   |

Tinker’s public docs describe it as a cloud training API where you write training loops locally while Tinker handles GPUs, with support for LoRA fine-tuning from 1B to 1T+ parameter models and algorithms including SFT, GRPO/PPO-style RL, DPO, and distillation. ([Tinker Docs][1]) Its product page emphasizes four low-level primitives: `forward_backward`, `optim_step`, `sample`, and `save_state`; it also says Tinker handles scheduling, resource management, and infrastructure reliability. ([Thinking Machines Lab][2]) That makes it a great **post-training research accelerator**, not a replacement for learning from-scratch pretraining.

Baseten is better viewed as a **training + deployment + inference platform**. Its docs say you can bring an open-source LLM, fine-tuned checkpoint, or custom model, and Baseten handles containerization, GPU scheduling across clouds, autoscaling, observability, and engine optimizations such as TensorRT-LLM compilation. ([Baseten][3]) Baseten Training is now generally available and advertises multi-node jobs, persistent storage, deploy-from-checkpoint, checkpoint resume, per-GPU/multinode metrics, and InfiniBand-backed clusters. ([Baseten][4]) That makes it a strong choice for **serving and managed training jobs**, especially if you care about shipping a public endpoint fast.

## The decisions you must make manually

### 1. Decide the public claim

You need to choose one of these claims:

| Claim                                                      |                     Feasible in 1–2 days? |               Credibility |
| ---------------------------------------------------------- | ----------------------------------------: | ------------------------: |
| “I built a full LLM training factory vertical slice”       |                                       Yes |                    Strong |
| “I trained a tiny LLM from scratch and served it”          |                                       Yes | Strong if well documented |
| “I post-trained a serious open model with RL/distillation” |                 Maybe, with Tinker access |                    Strong |
| “I trained a frontier-scale model”                         |                                        No |              Not credible |
| “I trained a 1B–3B model end-to-end”                       | No, unless most infra/data already exists |              Strong later |

For your situation, choose this:

> “In 48 hours, I built and ran an end-to-end LLM training lab: from-scratch pretraining smoke run, managed post-training, verifier-gated distillation data engine, evals, model export, and serving endpoint.”

That is a clean and defensible milestone.

### 2. Choose the model tracks

Do **not** make one model do every job. Use separate tracks.

| Track                        | Manual choice            | My default recommendation                        |
| ---------------------------- | ------------------------ | ------------------------------------------------ |
| From-scratch base model      | Architecture/size        | `lab-124m` Llama-like decoder-only transformer   |
| Serious post-training target | Open-weight model family | Qwen-family model on Tinker if available         |
| Teacher models               | Open vs API              | Prefer open-weight teachers first                |
| Serving target               | Which model to expose    | Post-trained/distilled model, not raw base       |
| Public artifact              | What to release          | Code, configs, logs, model card, evals, endpoint |

For the Tinker lane, pick one **small/medium dense model** first, not a giant MoE. Tinker’s supported-model list currently includes Qwen dense/MoE models, GPT-OSS MoE models, DeepSeek, Kimi, and Nemotron entries. ([Thinking Machines Lab][2]) Start with something like a 4B–9B dense model if available, then scale to 27B+ or MoE once your SFT/RL/eval loop works.

### 3. Decide whether Tinker is core or optional

Use Tinker if your priority is:

* fast post-training
* RL experiments
* distillation loops
* algorithm control without GPU cluster management
* LoRA/adapters on large open models

Do **not** rely on Tinker for your whole proof if your claim includes:

* from-scratch pretraining
* custom distributed-training infrastructure
* tokenizer/data-pipeline competence
* autonomous GPU scheduler research
* full control over every low-level training detail

Tinker is excellent for “I can do sophisticated post-training research.” It is weaker as evidence for “I understand pretraining infrastructure,” because the point of Tinker is to abstract away much of that infrastructure.

### 4. Decide whether Baseten is serving-only or training+serving

I would use Baseten for **serving immediately** and consider it for managed training only after the first raw-GPU pretraining run.

Recommended split:

| Use Baseten for                         | Use raw GPU for                          |
| --------------------------------------- | ---------------------------------------- |
| Public demo endpoint                    | From-scratch pretraining                 |
| TensorRT/vLLM-style optimized inference | OLMo-core/TorchTitan experiments         |
| Deploy-from-checkpoint workflow         | GPU scheduler research                   |
| Autoscaling and observability           | Low-level profiling and cost experiments |
| Production-grade API                    | Reproducibility proof                    |

Baseten’s deployment docs say Truss can package models with a config file and serve OpenAI-compatible endpoints, while Baseten engines handle low-level performance work like quantization, tensor parallelism, KV cache management, and batching. ([Baseten][3]) That is exactly what you want for the public-serving layer.

### 5. Choose raw GPU provider

For the pretraining proof, choose one raw GPU provider manually. Don’t spend a day making the perfect comparison.

My default:

| Phase      | Provider style                   | Hardware                  |
| ---------- | -------------------------------- | ------------------------- |
| Smoke run  | Cheap GPU marketplace/cloud      | 1× RTX 4090 / L40S / A100 |
| 124M–350M  | Cheap single-node                | 1–8 GPUs                  |
| 1B+        | Reliable 8× H100/A100 node       | One homogeneous node      |
| Multi-node | Only after everything else works | InfiniBand-backed cluster |

RunPod and Lambda are common low-friction choices; RunPod publishes GPU cloud pricing and says pricing depends on Pods, Serverless, and Clusters, while Lambda’s pricing page advertises on-demand GPUs, 1-Click Clusters, and Superclusters from 16 to 2,000+ H100/B200 GPUs. ([Runpod][5]) CoreWeave is more enterprise/serious-cluster oriented and advertises H200/H100-class GPU compute with a focus on consistent performance. ([CoreWeave][6])

My practical recommendation:

* **RunPod** for cheap smoke jobs.
* **Lambda** for simple, reliable 8× GPU nodes.
* **CoreWeave / Crusoe / GMI / Baseten Training** only when you need serious multi-node support or sales-assisted capacity.
* **SkyPilot** on top if you want portability and spot/preemption recovery. SkyPilot managed jobs support auto-retry, spot preemption recovery, and cleanup, which fits your “lowest cost even if it takes longer” constraint. ([SkyPilot Docs][7])

### 6. Choose the training framework

Codex can wire this up, but you need to choose.

My default:

| Need                                     | Pick                |
| ---------------------------------------- | ------------------- |
| From-scratch open-science-style training | OLMo-core           |
| PyTorch-native systems experimentation   | TorchTitan          |
| NVIDIA-heavy enterprise stack            | NeMo                |
| Fast post-training on open models        | Tinker / TRL / verl |
| Serving                                  | Baseten + vLLM      |

I would use **OLMo-core** for the first from-scratch pipeline because it is an actual large-scale distributed training library from Ai2 and is aligned with open model-flow practices. ([Olmo-core][8]) TorchTitan is also a strong option if you want a cleaner PyTorch-native research codebase for scaling experiments. ([GitHub][9])

### 7. Choose your legal/data posture

This is not optional. You need to decide:

* Which datasets are allowed?
* Which teacher outputs can be used for training?
* Which model licenses allow commercial/public release?
* Can you publish synthetic data?
* Can you publish adapters?
* Can you merge adapters into base weights?
* Can you use API outputs for distillation?

Be especially careful with commercial API teachers. OpenAI’s current Services Agreement includes a restriction against using Output to develop AI models that compete with OpenAI’s products and services, except for a permitted exception. ([OpenAI][10]) That does **not** mean “never use API outputs for anything,” but it does mean you should not casually build a public competing model from commercial API-generated distillation data without legal review.

For a clean public project, prefer:

* open-weight teacher models whose licenses allow your use
* verifier-generated labels
* human-authored or permissively licensed instruction data
* your own synthetic prompts
* public data lineage

### 8. Choose your eval gates before training

Codex can implement evals, but you must decide what counts as success.

For the 1–2 day version, use:

| Gate              | Required result                         |
| ----------------- | --------------------------------------- |
| Pretraining smoke | loss decreases, checkpoint resumes      |
| SFT               | follows chat template                   |
| Distillation      | generated examples pass verifier/filter |
| RL/verifier loop  | improves on a tiny held-out task set    |
| Serving           | endpoint works and logs latency         |
| Reproducibility   | one-command smoke run                   |
| Public proof      | run card + cost ledger + model card     |

Do not let Codex or any agent “optimize” against your hidden evals. Freeze them first.

## The concrete stack I would choose

Here is the stack I would use if the goal is maximum visible progress in 1–2 days.

| Layer                   | Choice                                                                    |
| ----------------------- | ------------------------------------------------------------------------- |
| Coding agent            | Codex                                                                     |
| Repo                    | GitHub                                                                    |
| From-scratch training   | OLMo-core                                                                 |
| Raw GPU launcher        | SkyPilot                                                                  |
| First raw GPU provider  | RunPod or Lambda                                                          |
| Post-training provider  | Tinker, if accepted/available                                             |
| Backup post-training    | TRL locally on raw GPU                                                    |
| Teacher models          | open-weight Qwen/DeepSeek/Kimi/Nemotron-class models where licenses allow |
| API teacher/judge       | only after terms review                                                   |
| Evals                   | lm-eval + custom verifier tests                                           |
| Serving                 | Baseten                                                                   |
| Repro serving benchmark | local/self-hosted vLLM                                                    |
| Weights release         | Hugging Face Hub                                                          |
| Reports                 | Markdown + W&B/MLflow screenshots + cost ledger                           |

## What Codex should do vs what you must do

| Area      | You decide                     | Codex executes                      |
| --------- | ------------------------------ | ----------------------------------- |
| Claim     | What you want to prove         | README/report structure             |
| Model     | Size, base family, teacher set | Config files, wrappers              |
| Provider  | Tinker/Baseten/raw GPU choice  | SDK integration, deployment scripts |
| Budget    | Hard cap, stop rules           | Cost tracker                        |
| Data      | Allowed sources                | Download/filter/tokenize pipeline   |
| Licensing | What can be trained/released   | License metadata checks             |
| Evals     | What counts as success         | Eval harness and dashboards         |
| Safety    | Refusal/safety boundaries      | Test prompts and filters            |
| Release   | What to publish                | Model cards, run cards, scripts     |

The most dangerous mistake is letting Codex make implicit decisions. It will happily produce a working system with bad assumptions. You need a `docs/decisions/experiment-decisions.md` file before implementation.

## `docs/decisions/experiment-decisions.md` template

Create this file and fill it manually:

```md
# Experiment Decisions

## Public Claim
We are building a 48-hour end-to-end LLM training lab vertical slice:
pretraining smoke run, post-training, distillation data engine, evals, and serving.

## Budget
Hard cap: $___
Soft cap: $___
Stop if any job exceeds $___ without producing a checkpoint.

## From-Scratch Model
Name: lab-124m
Architecture: decoder-only, Llama-like
Framework: OLMo-core
Tokenizer: [own tokenizer / existing tokenizer]
Training tokens target: ___
Sequence length: ___

## Raw GPU Provider
Primary: ___
Backup: ___
Reason: ___

## Post-Training Provider
Primary: Tinker
Backup: TRL on raw GPU
Base model: ___
Allowed use/license checked: yes/no

## Serving Provider
Primary: Baseten
Backup: vLLM self-hosted
Endpoint type: OpenAI-compatible chat completions

## Teacher Models
Allowed teachers:
- ___
- ___

Disallowed until legal review:
- ___

## Data Sources
Pretraining:
- ___

SFT:
- ___

Distillation:
- ___

## Evals
Smoke evals:
- train loss decreases
- checkpoint resumes
- generation works

Capability evals:
- ___

Safety evals:
- ___

## Release Artifacts
- code
- configs
- logs
- cost ledger
- model card
- data card
- eval report
- serving benchmark
```

## 48-hour execution plan

### Hour 0–2: manual decisions

You do this, not Codex:

1. Pick budget cap.
2. Pick raw GPU provider.
3. Request/sign into Tinker.
4. Sign into Baseten.
5. Pick from-scratch model size: `124M`.
6. Pick post-training base model: small/medium supported open model.
7. Pick release name.
8. Define success gates.

### Hour 2–8: Codex builds the repo

Give Codex tasks like:

```text
Create a monorepo for an LLM training lab with:
- OLMo-core pretraining smoke run
- tiny dataset ingestion/tokenization
- checkpoint resume test
- lm-eval wrapper
- Tinker SFT/RL placeholder integration
- verifier-gated distillation pipeline
- Baseten deployment folder
- run cards, model cards, cost ledger
- GitHub Actions for unit tests
```

### Hour 8–16: from-scratch smoke run

Run:

* 20M or 124M model
* tiny corpus
* checkpoint save/resume
* sample generation
* loss curve
* export checkpoint

This is your “I touched the real training loop” proof.

### Hour 16–28: Tinker post-training track

If Tinker access works:

* run SFT on a small instruction dataset
* run a tiny DPO/preference or verifier-RL example
* export adapter/checkpoint if supported
* evaluate before/after

Tinker docs include cookbook/tutorial coverage for supervised learning, RL, DPO/preferences, prompt/model distillation, tool use, verifiers RL, and export/publish flows. ([Tinker Docs][1])

If Tinker access does not work:

* run TRL locally on a small open model
* keep the same dataset/eval interface
* mark Tinker as future provider

### Hour 28–36: distillation engine

Build:

* prompt generator
* teacher response collector
* verifier/filter
* preference-pair builder
* lineage database
* dataset export

Do not overbuild. The first version only needs JSONL + SQLite/DuckDB.

### Hour 36–44: Baseten serving

Deploy:

* post-trained/adapted model if ready
* otherwise a known HF model behind the same API wrapper
* simple `/chat` demo
* latency/cost logging

### Hour 44–48: public proof

Publish:

* README
* architecture diagram
* run card
* cost ledger
* eval table
* loss curve
* model card
* “what worked / what failed”
* next-step roadmap

## My final recommendation

Use this combination:

1. **Codex** to build the repo, scripts, tests, dashboards, deployment glue, and docs.
2. **Raw GPU provider + OLMo-core** for the from-scratch pretraining proof.
3. **Tinker** for serious post-training/RL/distillation experiments if you get access.
4. **Baseten** for the public serving endpoint.
5. **SkyPilot** if you want your cost-aware GPU allocation research to start cleanly.
6. **Open-weight teachers first**, commercial API teachers only after terms review.

The cleanest 48-hour win is not “train the biggest model.” It is:

> “I built a reproducible LLM training lab that performs pretraining, post-training, distillation, evaluation, and serving, with clear provider choices and cost controls.”

That is what will make serious people take the project seriously.

[1]: https://tinker-docs.thinkingmachines.ai/ "Tinker - Tinker Documentation"
[2]: https://thinkingmachines.ai/tinker/ "Tinker - Thinking Machines Lab"
[3]: https://docs.baseten.co/overview "Baseten overview - Baseten"
[4]: https://www.baseten.co/blog/baseten-training-is-ga/ "Train AI Models When You Want. Deploy on Ultra Performant Infrastructure. Baseten Training Is GA."
[5]: https://www.runpod.io/pricing?utm_source=chatgpt.com "GPU Cloud Pricing | Per-Second H100, A100, RTX"
[6]: https://www.coreweave.com/products/gpu-compute?utm_source=chatgpt.com "GPUs for AI Models and Innovation"
[7]: https://docs.skypilot.co/en/svc-account-docs/examples/managed-jobs.html?utm_source=chatgpt.com "Managed Jobs — SkyPilot documentation"
[8]: https://olmo-core.readthedocs.io/en/latest/?utm_source=chatgpt.com "OLMo-core v2.5.0"
[9]: https://github.com/pytorch/torchtitan?utm_source=chatgpt.com "pytorch/torchtitan"
[10]: https://openai.com/policies/services-agreement/?utm_source=chatgpt.com "OpenAI Services Agreement"


You should build a **multi-provider LLM factory**, not a pile of provider-specific scripts.

The core rule: **one experiment spec, many execution backends**.

Your stack should have three execution lanes:

1. **NVIDIA/PyTorch lane** — your default for your own GPUs, CoreWeave, Lambda, Baseten Training, OCI, Azure, RunPod, Together GPU clusters.
2. **JAX/TPU lane** — only for Google Cloud TPU / AI Hypercomputer experiments.
3. **Managed post-training lane** — Tinker, Baseten Loops, Together/Fireworks fine-tuning where useful.

The frontier-lab reality is that no outsider knows every private internal tool. What we can copy is the **public frontier-grade pattern**: PyTorch/JAX, distributed sharding, high-performance kernels, Slurm/Kubernetes/Kueue, InfiniBand/RDMA, S3-compatible storage, strict evals, and production inference engines.

---

# 1. The stack I would choose

## Default backbone

Use this as the main stack:

| Layer                 | Default choice                                                                   |
| --------------------- | -------------------------------------------------------------------------------- |
| Main language         | Python 3.11/3.12                                                                 |
| Package manager       | `uv`                                                                             |
| Containers            | Docker + NVIDIA Container Toolkit                                                |
| Configs               | Hydra + OmegaConf + Pydantic                                                     |
| Training runtime      | PyTorch 2.x                                                                      |
| Distributed training  | FSDP2 / DTensor / DeviceMesh, Megatron-Core, TorchTitan, OLMo-core               |
| NVIDIA stack          | CUDA, NCCL, cuDNN, Transformer Engine, GPUDirect RDMA                            |
| Data pipeline         | DataTrove, Dolma Toolkit, Hugging Face Datasets, PyArrow/Parquet, Polars, DuckDB |
| Tokenizer             | Hugging Face Tokenizers + SentencePiece                                          |
| Pretraining framework | OLMo-core first, TorchTitan/Megatron-Core for scale experiments                  |
| Post-training         | Tinker, TRL, verl, OpenRLHF                                                      |
| Serving               | vLLM, SGLang, TensorRT-LLM/Triton                                                |
| Orchestration         | Slurm + Kubernetes/Kueue + SkyPilot                                              |
| Observability         | W&B or MLflow, Prometheus/Grafana, NVIDIA DCGM Exporter, OpenTelemetry           |
| Storage               | S3-compatible object storage + local NVMe cache + optional parallel filesystem   |
| Evaluation            | lm-eval-harness, Inspect AI, LightEval, custom verifier evals                    |

PyTorch FSDP shards parameters, gradients, and optimizer states, which is the basic primitive you need for memory-efficient large-model training. ([PyTorch Docs][1]) TorchTitan is the clean PyTorch-native training platform for rapid experimentation and large-scale generative AI training. ([GitHub][2]) OLMo-core is the open-science-oriented PyTorch library from Ai2 for large-scale distributed training. ([Olmo-core][3]) Megatron-Core/NeMo is the NVIDIA-style high-scale training path; NVIDIA’s public Megatron-Core material shows scaling experiments up to thousands of H100s. ([NVIDIA Developer][4])

---

# 2. Provider architecture

Create a provider interface like this:

```text
Provider
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

Then implement adapters:

```text
providers/
  local_slurm.py
  local_k8s.py
  skypilot.py
  coreweave.py
  lambda_cloud.py
  baseten.py
  tinker.py
  together.py
  fireworks.py
  runpod.py
  gcp_tpu.py
  azure.py
  aws.py
  oci.py
```

Every training job should be launched from the same experiment file:

```yaml
experiment_id: lab-124m-pretrain-v001
stage: pretrain
provider: local_slurm
fallback_providers:
  - lambda_cloud
  - coreweave
  - runpod

container: ghcr.io/your-org/llm-lab-train:cuda
framework: olmo_core

resources:
  gpu_type: any_of[h100,h200,a100,rtx4090]
  gpus: 8
  nodes: 1
  preemptible_ok: true

data:
  train_manifest: s3://llm-lab/manifests/train_v001.jsonl
  val_manifest: s3://llm-lab/manifests/val_v001.jsonl
  tokenizer: s3://llm-lab/tokenizers/tokenizer_v001/

checkpointing:
  interval_steps: 500
  output_uri: s3://llm-lab/checkpoints/lab-124m-pretrain-v001/

logging:
  wandb_project: llm-lab
  metrics_uri: s3://llm-lab/metrics/
```

This is the key design decision. Providers become execution targets, not the center of your system.

---

# 3. Providers you should use

## Provider shortlist

| Provider                                | Use it for                                                              |             Priority |
| --------------------------------------- | ----------------------------------------------------------------------- | -------------------: |
| **Your own GPUs**                       | debugging, smoke runs, permanent baseline, serving, cost control        |            mandatory |
| **CoreWeave**                           | serious Kubernetes-native GPU training/inference, production-like infra |                 high |
| **Lambda**                              | simple H100/B200 nodes and Slurm/Kubernetes clusters                    |                 high |
| **Baseten**                             | managed training jobs, deploy-from-checkpoint, public serving           |                 high |
| **Tinker**                              | frontier-style post-training API: SFT, RL, DPO, distillation            |                 high |
| **Together AI**                         | serverless teachers, dedicated endpoints, GPU clusters                  |          medium-high |
| **Fireworks AI**                        | fast model APIs, SFT/DPO/RFT fine-tuning comparisons                    |               medium |
| **Google Cloud TPU / AI Hypercomputer** | JAX/MaxText TPU experiments                                             |               medium |
| **Azure ND H100/H200**                  | enterprise NVIDIA GPU capacity                                          |               medium |
| **OCI Supercluster**                    | large reserved bare-metal/RDMA clusters                                 |               medium |
| **AWS Trainium / P5/P6**                | only if you want AWS/Neuron specialization                              | medium-low initially |
| **RunPod**                              | cheap smoke jobs and disposable experiments                             |           medium-low |
| **Hugging Face Inference Endpoints**    | quick model demos                                                       |             optional |

CoreWeave is one of the most relevant “frontier-style” providers because its docs describe Kubernetes-native GPU infrastructure, Slurm-on-Kubernetes through SUNK, and AI-focused training/inference services. ([CoreWeave Documentation][5]) CoreWeave also says world-class AI labs use Kueue on CoreWeave Kubernetes Service for training and batch inference workloads. ([CoreWeave][6]) Lambda is attractive for simpler cluster access: its docs describe single-node instances and 16–512 GPU H100/B200 clusters with Managed Kubernetes, preinstalled Kubernetes, or Slurm. ([Lambda Docs][7]) Baseten Training supports managed GPUs, Truss Train, Loops, and deploying checkpoints to production inference. ([Baseten][8]) Tinker is specifically built for managed LoRA fine-tuning from 1B to 1T+ parameter models and lets you write training loops locally while it handles GPUs. ([Tinker Docs][9])

---

# 4. Your own GPU provider

Your own GPUs should be a **first-class provider** called something like `local`.

## If you have 1 machine / up to 8 GPUs

Use:

```text
Ubuntu 22.04 or 24.04
NVIDIA driver
Docker
NVIDIA Container Toolkit
CUDA-compatible PyTorch container
MinIO
Prometheus
Grafana
DCGM Exporter
W&B or MLflow
vLLM
SGLang
```

For a single machine, do **not** start with Kubernetes. Use Docker Compose or bare Docker, plus simple launch scripts.

## If you have multiple GPU machines

Use this:

| Component                    | Choice                                     |
| ---------------------------- | ------------------------------------------ |
| Training scheduler           | Slurm                                      |
| Container runtime for Slurm  | Enroot + Pyxis, or Apptainer               |
| Serving/control plane        | Kubernetes                                 |
| GPU management on Kubernetes | NVIDIA GPU Operator                        |
| Network/RDMA management      | NVIDIA Network Operator                    |
| Batch queueing on Kubernetes | Kueue                                      |
| Monitoring                   | Prometheus + Grafana + DCGM Exporter       |
| Object storage               | MinIO                                      |
| Shared filesystem            | NFS first, then Lustre/WEKA/VAST if needed |

Slurm is still the default mental model for serious multi-node training because it is a fault-tolerant, scalable cluster management and job scheduling system. ([slurm.schedmd.com][10]) Kueue is the right Kubernetes-native queueing layer for batch, HPC, and AI/ML workloads. ([Kueue][11]) NVIDIA GPU Operator automates the NVIDIA software stack on Kubernetes, including drivers, device plugin, container toolkit, node labeling, and DCGM monitoring. ([NVIDIA Docs][12]) NVIDIA Network Operator manages RDMA and GPUDirect RDMA networking components in Kubernetes. ([NVIDIA Docs][13])

For your own provider adapter, support both:

```text
local_slurm
local_k8s
```

Use `local_slurm` for pretraining and distributed training. Use `local_k8s` for serving, batch inference, eval services, dashboards, and possibly post-training rollouts.

---

# 5. Training libraries

## Main pretraining stack

Use these:

```text
torch
torchvision
torchaudio
torchdata
torchao
transformers
datasets
safetensors
tokenizers
sentencepiece
ai2-olmo-core
torchtitan
megatron-core
nemo-toolkit
deepspeed
flash-attn
transformer-engine
liger-kernel
```

How to choose:

| Situation                                             | Use                  |
| ----------------------------------------------------- | -------------------- |
| First serious reproducible pretraining                | OLMo-core            |
| PyTorch-native systems experiments                    | TorchTitan           |
| NVIDIA-scale training / tensor + pipeline parallelism | Megatron-Core / NeMo |
| Easy memory scaling for existing code                 | DeepSpeed ZeRO       |
| Training on Google TPU                                | JAX + MaxText        |

DeepSpeed ZeRO-3 is useful because it enables models whose parameters exceed individual node memory and often requires little model-code modification. ([DeepSpeed][14]) MaxText is Google’s high-performance, scalable JAX LLM training framework targeting Cloud TPUs and GPUs. ([maxtext.readthedocs.io][15]) Google’s TPU samples include Llama pretraining examples using MaxText on TPU v6e/Trillium. ([Google Cloud Documentation][16])

## Performance kernels

Use:

```text
flash-attn
transformer-engine
liger-kernel
triton
flashinfer
```

FlashAttention-3 is optimized for Hopper GPUs such as H100/H800 and requires CUDA >= 12.3. ([GitHub][17]) Liger Kernel provides Triton kernels for LLM training and reports higher throughput and lower memory use for core primitives like RMSNorm, RoPE, SwiGLU, and fused cross-entropy. ([GitHub][18]) FlashInfer is a high-performance LLM kernel library focused on serving and inference kernels such as FlashAttention, PageAttention, and LoRA. ([docs.flashinfer.ai][19])

---

# 6. Post-training libraries

Use all of these, but with different jobs:

| Library/provider | Use                                      |
| ---------------- | ---------------------------------------- |
| **Tinker**       | managed LoRA, SFT, RL, DPO, distillation |
| **TRL**          | simple local SFT/DPO/GRPO experiments    |
| **verl**         | scalable RL/post-training research       |
| **OpenRLHF**     | Ray + vLLM RLHF/RLVR workflows           |
| **PEFT**         | LoRA/QLoRA adapters                      |
| **Accelerate**   | smaller local fine-tuning jobs           |
| **Ray**          | distributed rollouts, evals, data jobs   |

Tinker has official distillation recipes and supports teacher-supervised student training. ([Tinker Docs][20]) It also has self-distillation fine-tuning material for continual-learning-style post-training. ([Tinker Docs][21]) verl is a production-ready RL training framework for LLM post-training. ([Verl][22]) OpenRLHF is built around a Ray + vLLM distributed architecture for scalable RLHF. ([OpenRLHF][23])

My practical rule:

```text
Tinker: fastest frontier-style managed post-training.
TRL: local/simple fallback.
verl: serious RL research.
OpenRLHF: scalable Ray/vLLM RLHF alternative.
```

---

# 7. Serving libraries

Use three serving engines, not one:

| Engine                    | Use                                                                  |
| ------------------------- | -------------------------------------------------------------------- |
| **vLLM**                  | default serving engine                                               |
| **SGLang**                | structured outputs, agentic/multi-turn/RAG workloads, prefix sharing |
| **TensorRT-LLM + Triton** | maximum NVIDIA production performance once model is stable           |

vLLM provides an OpenAI-compatible HTTP server for completions and chat APIs. ([vLLM][24]) SGLang is designed for low-latency, high-throughput production serving and supports OpenAI-compatible APIs. ([SGLang Documentation][25]) SGLang also supports constrained structured outputs with JSON schema, regex, or EBNF. ([SGLang Documentation][26]) TensorRT-LLM is NVIDIA’s open-source library for optimizing LLM inference on NVIDIA GPUs, and Triton has a TensorRT-LLM backend for serving compiled engines. ([NVIDIA Docs][27])

Do **not** choose Hugging Face TGI as your new primary serving engine. Hugging Face says TGI is in maintenance mode and recommends vLLM or SGLang for Inference Endpoints. ([Hugging Face][28])

---

# 8. Data stack

Use:

```text
datasets
huggingface_hub
datatrove
dolma
nemo-curator
pyarrow
polars
duckdb
pandas
fsspec
s3fs
gcsfs
adlfs
boto3
smart_open
zstandard
xxhash
datasketch
simhash
ftfy
trafilatura
resiliparse
presidio-analyzer
presidio-anonymizer
fasttext / lingua-language-detector
```

Data sources and benchmarks:

| Asset                   | Use                                      |
| ----------------------- | ---------------------------------------- |
| FineWeb                 | web-data baseline                        |
| Dolma                   | open reproducible corpus baseline        |
| DCLM/DataComp-LM        | controlled data-curation benchmark       |
| your own synthetic data | post-training/distillation only at first |

FineWeb has more than 18.5T cleaned/deduplicated English web tokens and was built with DataTrove. ([Hugging Face][29]) Dolma is a 3T-token open corpus with web, academic, code, books, and encyclopedic material, plus the Dolma Toolkit for dataset curation. ([GitHub][30]) DataComp-LM/DCLM is explicitly designed for controlled data-curation experiments across model scales from 412M to 7B parameters and includes 53 downstream evaluations. ([DataComp][31]) DataTrove is a large-scale text processing, filtering, and deduplication library that runs locally or on Slurm. ([GitHub][32])

---

# 9. Tokenizer stack

Use:

```text
tokenizers
sentencepiece
tiktoken
```

Use Hugging Face Tokenizers for fast BPE/Unigram/WordPiece experimentation and production tokenization. The Tokenizers library is Rust-backed and designed for fast training/tokenization. ([Hugging Face][33]) Use SentencePiece when you want a classic language-independent tokenizer that trains directly from raw text with a fixed vocabulary size. ([GitHub][34])

Default:

```text
pretraining tokenizer: Hugging Face Tokenizers, byte-level BPE or Unigram
vocab size: 32k for small models, 50k-64k for 1B+
chat special tokens: system/user/assistant/eos/bos/pad
```

---

# 10. Evaluation stack

Use:

```text
lm-eval
inspect-ai
lighteval
openai-evals
pytest
hypothesis
deepeval or promptfoo for app-level tests
```

Use **lm-evaluation-harness** for standard academic/task benchmarks. It is a unified framework for testing generative language models on many tasks. ([GitHub][35]) Use **Inspect AI** for frontier-style evals, especially coding, agentic tasks, reasoning, behavior, and tool-use evals. ([Inspect][36]) Use **LightEval** when you want sample-level debugging and multiple backend support inside the Hugging Face ecosystem. ([Hugging Face][37]) OpenAI Evals is useful for custom LLM-system evals and private workflow evals. ([GitHub][38])

For your project, define these eval layers:

```text
evals/
  base_model/
    lm_eval.yaml
    perplexity_slices.yaml
  chat_model/
    instruction_following.yaml
    format_following.yaml
    safety.yaml
  reasoning/
    math_verifier.py
    code_unit_tests.py
    tool_use_envs.py
  serving/
    latency_benchmark.py
    throughput_benchmark.py
    cost_per_token.py
  regression/
    frozen_private_eval.jsonl
```

---

# 11. Orchestration and multi-provider control

Use:

```text
skypilot
ray[default,train,serve,data]
kubernetes
kueue
slurm
helm
terraform
pulumi
ansible
argo-workflows
argo-cd
```

Use **SkyPilot** as your first multi-cloud launcher because it is explicitly designed to run and manage AI workloads across AI infrastructure. ([docs.skypilot.co][39]) Its managed jobs can automatically provision temporary clusters and handle recovery, which matches your “cheapest even if slower” requirement. ([docs.skypilot.co][40]) Use **Ray** for distributed rollouts, eval sweeps, data processing, and some training workflows; Ray’s docs show FSDP2 integration for distributed PyTorch training. ([Ray][41])

My recommendation:

```text
Slurm = serious synchronous training
Kubernetes + Kueue = provider-native batch/serving control plane
SkyPilot = cross-provider launcher and cost-aware routing
Ray = rollouts, evals, data jobs, RL workers
Argo = repeatable workflows
Terraform/Pulumi = infrastructure
```

---

# 12. Storage stack

Use S3-compatible object storage as the canonical storage layer.

```text
Object storage:
  - MinIO for your own GPUs
  - AWS S3
  - GCS
  - Azure Blob
  - OCI Object Storage
  - CoreWeave AI Object Storage

Shared/parallel filesystem:
  - local NVMe cache
  - NFS for small cluster
  - Lustre / FSx for Lustre
  - WEKA / VAST for serious clusters
  - Google Parallelstore on GCP
```

CoreWeave AI Object Storage is S3-compatible and purpose-built for training datasets, model weights, and checkpoints. ([CoreWeave Documentation][42]) AWS FSx for Lustre integrates with S3 and can reduce repeated data download overhead for iterative training jobs. ([Documentación de AWS][43]) Google Parallelstore is a managed parallel file service for HPC and AI/ML workloads requiring high-throughput shared data access. ([Google Cloud Documentation][44])

Design rule:

```text
Object storage is the source of truth.
NVMe is cache.
Parallel filesystem is performance optimization.
Never make one provider’s filesystem the only copy.
```

---

# 13. Observability stack

Use:

```text
wandb
mlflow
prometheus
grafana
nvidia-dcgm-exporter
opentelemetry-sdk
opentelemetry-collector
loki or elasticsearch
nsys
ncu
py-spy
scalene
```

W&B is good for experiment tracking, evaluation, observability, sweeps, model registry, and reports. ([Weights & Biases Documentation][45]) MLflow is good if you want a more self-hostable experiment tracking and model-registry backbone. ([MLflow AI Platform][46]) NVIDIA DCGM Exporter exposes GPU metrics to Prometheus, which is exactly what you need for cluster-level GPU monitoring. ([NVIDIA Docs][47]) OpenTelemetry gives you vendor-neutral traces, metrics, and logs. ([OpenTelemetry][48])

Track these metrics from day one:

```text
training_loss
validation_loss
tokens_per_second
tokens_per_second_per_gpu
MFU
GPU_utilization
GPU_memory_used
network_tx_rx
NCCL_errors
dataloader_wait_time
checkpoint_write_time
checkpoint_size
cost_per_1B_tokens
eval_score_by_domain
serving_TTFT
serving_output_tokens_per_second
serving_p50/p95/p99_latency
```

---

# 14. Provider-specific recommendations

## A. Your own GPUs

Use for:

```text
unit tests
smoke pretraining
data pipeline testing
small SFT
small RL loops
local serving
benchmarking
regression tests
```

Install:

```text
NVIDIA driver
NVIDIA Container Toolkit
Docker
Slurm if multi-node
Kubernetes if serving/control plane
NVIDIA GPU Operator if Kubernetes
NVIDIA Network Operator if RDMA/Kubernetes
MinIO
Prometheus/Grafana/DCGM
W&B local or MLflow
```

This is your credibility anchor. Even if Tinker/Baseten/CoreWeave handle scale, your own provider proves you understand the machine.

## B. CoreWeave

Use for:

```text
serious multi-node GPU training
Kubernetes-native workloads
Kueue experiments
production-ish inference
large eval/batch inference
```

CoreWeave’s docs describe CKS as a bare-metal Kubernetes service for AI/HPC workloads and SUNK as Slurm on Kubernetes for distributed training. ([CoreWeave Documentation][5])

## C. Lambda

Use for:

```text
simple H100/B200 nodes
Slurm clusters
fast experiments where you do not want Kubernetes complexity
```

Lambda’s 1-Click Clusters are documented as 16–512 H100/B200 GPU clusters with Quantum-2 400 Gb/s InfiniBand and GPUDirect RDMA. ([Lambda Docs][49])

## D. Baseten

Use for:

```text
public serving
managed training jobs
deploy-from-checkpoint
production API demos
```

Baseten Training supports multi-node jobs, persistent storage, checkpoint-to-inference workflows, and granular metrics. ([Baseten][50])

## E. Tinker

Use for:

```text
SFT
DPO
RL
distillation
self-distillation
fast post-training experiments
```

Tinker is not the right proof for from-scratch pretraining. It is the right accelerator for post-training research.

## F. Together AI

Use for:

```text
teacher model inference
serverless open model calls
dedicated endpoints
GPU clusters when useful
```

Together’s docs describe serverless inference and GPU clusters for training, fine-tuning, and large-scale AI workloads with Kubernetes and Slurm support. ([Together AI docs][51])

## G. Fireworks AI

Use for:

```text
teacher APIs
fast inference comparisons
managed fine-tuning comparisons
```

Fireworks supports supervised fine-tuning and deployment to dedicated endpoints for fine-tuned models. ([Fireworks AI Docs][52])

## H. Google Cloud TPU

Use only if you commit to the JAX/MaxText lane:

```text
jax
flax
orbax-checkpoint
maxtext
gcsfs
tensorboard
```

Google’s TPU v5p docs describe large pod-scale configurations, and TPU v6e docs cover Trillium training with JAX and PyTorch/XLA. ([Google Cloud Documentation][53])

## I. Azure

Use for:

```text
enterprise GPU capacity
ND H100/H200 clusters
Microsoft ecosystem compatibility
```

Azure ND H100 v5 is built with NVIDIA H100 GPUs and Quantum-2 InfiniBand networking for large AI workloads. ([Microsoft Azure][54])

## J. OCI

Use for:

```text
large reserved GPU clusters
bare-metal/RDMA economics
enterprise scale
```

OCI advertises bare-metal and VM GPU instances with Blackwell, H200, H100, L40S, A100, and other NVIDIA GPUs. ([Oracle][55]) OCI also says its H200 Supercluster scales to very large GPU counts. ([Blogs de Oracle][56])

## K. AWS

Use for:

```text
AWS enterprise environments
S3/FSx/SageMaker integration
Trainium experiments
```

Do not start with Trainium unless you deliberately want the Neuron ecosystem. AWS positions Trainium for training/inference economics at scale, but it is a separate stack from your NVIDIA/PyTorch default. ([Amazon Web Services, Inc.][57])

## L. RunPod

Use for:

```text
cheap smoke jobs
single-GPU tests
preemptible experiments
short-lived workers
```

Do not make it your flagship training provider unless you have verified stability, networking, storage, and support for your specific job shape.

---

# 15. Exact dependency groups

Create a `pyproject.toml` with dependency groups like this.

## Base

```toml
[dependency-groups]
base = [
  "uv",
  "numpy",
  "scipy",
  "pandas",
  "polars",
  "pyarrow",
  "duckdb",
  "pydantic",
  "pydantic-settings",
  "hydra-core",
  "omegaconf",
  "typer",
  "rich",
  "loguru",
  "orjson",
  "ujson",
  "tqdm",
  "requests",
  "httpx",
  "aiohttp",
  "tenacity",
  "python-dotenv",
]
```

## Training

```toml
training = [
  "torch",
  "torchdata",
  "torchao",
  "transformers",
  "accelerate",
  "datasets",
  "safetensors",
  "tokenizers",
  "sentencepiece",
  "einops",
  "deepspeed",
  "ai2-olmo-core",
  "liger-kernel",
  "flash-attn",
]
```

Install TorchTitan and some Megatron/NeMo components from pinned Git commits if the package version you need is not stable enough.

## NVIDIA performance

```toml
nvidia = [
  "transformer-engine[pytorch]",
  "nvidia-ml-py",
  "pynvml",
]
```

CUDA, NCCL, cuDNN, and drivers should mostly come from the container/base image, not random pip installs. NVIDIA’s CUDA archive currently lists CUDA 13.3.0 from May 2026, and NCCL release notes list NCCL 2.30.7 as of June 2026. ([NVIDIA Developer][58])

## Post-training

```toml
posttraining = [
  "trl",
  "peft",
  "bitsandbytes",
  "ray[default,train,serve,data]",
  "openrlhf",
  "verl",
  "tinker",
]
```

## Data

```toml
data = [
  "datasets",
  "huggingface_hub",
  "datatrove",
  "dolma",
  "pyarrow",
  "polars",
  "duckdb",
  "fsspec",
  "s3fs",
  "gcsfs",
  "adlfs",
  "boto3",
  "smart_open",
  "zstandard",
  "xxhash",
  "datasketch",
  "ftfy",
  "trafilatura",
  "resiliparse",
  "presidio-analyzer",
  "presidio-anonymizer",
]
```

## Serving

```toml
serving = [
  "vllm",
  "sglang",
  "fastapi",
  "uvicorn",
  "gunicorn",
  "openai",
  "prometheus-client",
  "flashinfer-python",
]
```

TensorRT-LLM/Triton should usually be installed via NVIDIA containers or pinned NVIDIA wheels/containers, not casually mixed into the same dev environment.

## Evaluation

```toml
eval = [
  "lm-eval",
  "inspect-ai",
  "lighteval",
  "pytest",
  "hypothesis",
  "jsonschema",
  "scikit-learn",
]
```

## Orchestration

```toml
orchestration = [
  "skypilot[all]",
  "kubernetes",
  "docker",
  "paramiko",
  "fabric",
  "invoke",
]
```

## Observability

```toml
observability = [
  "wandb",
  "mlflow",
  "prometheus-client",
  "opentelemetry-api",
  "opentelemetry-sdk",
  "opentelemetry-exporter-otlp",
  "sentry-sdk",
]
```

---

# 16. System dependencies

On NVIDIA GPU nodes:

```text
Ubuntu 22.04/24.04
NVIDIA driver
CUDA-compatible driver branch
NVIDIA Container Toolkit
Docker or containerd
NCCL
cuDNN
NVIDIA Fabric Manager where required
MOFED / OFED for InfiniBand
NCCL tests
iperf3
nvtop
htop
fio
nvidia-smi
nsys
ncu
dcgmi
```

On Kubernetes clusters:

```text
Kubernetes
Helm
NVIDIA GPU Operator
NVIDIA Network Operator
Kueue
Prometheus Operator
Grafana
Loki or Elasticsearch
Argo Workflows
Argo CD
cert-manager
external-secrets
ingress-nginx or Envoy Gateway
```

On Slurm clusters:

```text
Slurm
Munge
Enroot
Pyxis
NFS or Lustre client
NCCL tests
Prometheus node exporter
DCGM exporter
```

---

# 17. The provider routing policy

Your scheduler should choose providers by job type.

```yaml
routing:
  pretrain_smoke:
    prefer: [local_slurm, runpod, lambda_cloud]
  pretrain_serious:
    prefer: [local_slurm, lambda_cloud, coreweave, oci, azure]
  data_processing:
    prefer: [local_cpu, coreweave_k8s, aws_batch, gcp_batch]
  teacher_generation:
    prefer: [together, fireworks, local_vllm, baseten]
  posttraining_sft:
    prefer: [tinker, baseten_loops, local_slurm, lambda_cloud]
  posttraining_rl:
    prefer: [tinker, verl_on_local_slurm, openrlhf_on_lambda]
  evals:
    prefer: [local_k8s, runpod, together, baseten]
  serving_public:
    prefer: [baseten, coreweave, together, hf_endpoint]
  serving_benchmark:
    prefer: [local_k8s, lambda_cloud, coreweave]
```

This avoids the big mistake: trying to make one provider perfect for everything.

---

# 18. What to avoid

Avoid these traps:

| Trap                              | Why                                                                         |
| --------------------------------- | --------------------------------------------------------------------------- |
| Building only on Tinker           | Great for post-training, insufficient proof for pretraining infra           |
| Building only on Baseten          | Good managed platform, but hides too much if your claim is infra competence |
| Starting with AWS Trainium        | Different ecosystem; useful later, distracting now                          |
| Using TGI as default serving      | It is in maintenance mode                                                   |
| Treating RunPod as flagship infra | Fine for cheap jobs, weaker for serious reproducible multi-node experiments |
| No provider abstraction           | You will rewrite everything each time                                       |
| No storage abstraction            | You will get trapped by provider-specific paths                             |
| No cost ledger                    | You cannot claim efficiency                                                 |
| No frozen evals                   | You cannot claim improvement                                                |

---

# 19. The clean architecture

Build your repo like this:

```text
llm-lab/
  configs/
    experiments/
    providers/
    clusters/
    models/
    data/
    evals/

  src/
    providers/
      base.py
      local_slurm.py
      local_k8s.py
      skypilot.py
      coreweave.py
      lambda_cloud.py
      baseten.py
      tinker.py
      together.py
      fireworks.py
      gcp_tpu.py

    training/
      olmo_core_runner.py
      torchtitan_runner.py
      megatron_runner.py
      deepspeed_runner.py
      maxtext_runner.py

    posttraining/
      trl_runner.py
      tinker_runner.py
      verl_runner.py
      openrlhf_runner.py

    data_pipeline/
      ingest.py
      clean.py
      dedup.py
      tokenize.py
      pack.py
      manifest.py

    distillation/
      teacher_registry.py
      prompt_generator.py
      response_collector.py
      verifier.py
      preference_builder.py
      curriculum.py

    evaluation/
      lm_eval_runner.py
      inspect_runner.py
      lighteval_runner.py
      custom_verifiers.py

    serving/
      vllm_server.py
      sglang_server.py
      tensorrt_triton.py
      baseten_deploy.py

    observability/
      cost_ledger.py
      metrics.py
      traces.py
      gpu_monitoring.py
```

---

# 20. My final recommendation

Use this exact provider stack:

```text
Primary own infra:
  local_slurm + local_k8s + MinIO + Prometheus/Grafana/DCGM

Primary external training:
  Lambda for simple H100/B200 clusters
  CoreWeave for Kubernetes/frontier-style infra
  Baseten Training when you want managed training + deploy-from-checkpoint

Primary post-training:
  Tinker
  fallback: TRL/verl/OpenRLHF on your own GPUs or Lambda

Primary serving:
  Baseten public endpoint
  vLLM self-hosted benchmark
  SGLang for structured/multi-turn workloads
  TensorRT-LLM/Triton for optimized NVIDIA production path

Primary data:
  FineWeb + Dolma + DCLM-style ablations
  DataTrove + Dolma Toolkit + HF Datasets + Parquet

Primary eval:
  lm-eval + Inspect AI + custom verifier evals

Primary multi-provider orchestration:
  SkyPilot + provider adapters
  Slurm for training
  Kubernetes/Kueue for batch/serving
```

That gives you a stack that looks like a serious AI lab: low-level enough to prove competence, managed enough to move quickly, and modular enough to swap providers without rewriting the experiment.

[1]: https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html?utm_source=chatgpt.com "Getting Started with Fully Sharded Data Parallel (FSDP2)"
[2]: https://github.com/pytorch/torchtitan?utm_source=chatgpt.com "pytorch/torchtitan"
[3]: https://olmo-core.readthedocs.io/en/latest/?utm_source=chatgpt.com "OLMo-core v2.5.0"
[4]: https://developer.nvidia.com/megatron-core?utm_source=chatgpt.com "NVIDIA Megatron Core"
[5]: https://docs.coreweave.com/get-started?utm_source=chatgpt.com "Get started with CoreWeave"
[6]: https://www.coreweave.com/blog/kueue-a-kubernetes-native-system-for-ai-training-workloads?utm_source=chatgpt.com "Kueue: Kubernetes-Native AI Workload Scheduling with ..."
[7]: https://docs.lambda.ai/?utm_source=chatgpt.com "Lambda Docs"
[8]: https://docs.baseten.co/training/overview?utm_source=chatgpt.com "Training on Baseten"
[9]: https://tinker-docs.thinkingmachines.ai/?utm_source=chatgpt.com "Tinker Docs - Thinking Machines Lab"
[10]: https://slurm.schedmd.com/overview.html?utm_source=chatgpt.com "Overview - Slurm Workload Manager - SchedMD"
[11]: https://kueue.sigs.k8s.io/?utm_source=chatgpt.com "Kueue - Kubernetes"
[12]: https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html?utm_source=chatgpt.com "About the NVIDIA GPU Operator"
[13]: https://docs.nvidia.com/networking/display/kubernetes2610/deployment-guide-kubernetes.html?utm_source=chatgpt.com "NVIDIA Network Operator Deployment Guide with ..."
[14]: https://deepspeed.readthedocs.io/en/stable/zero3.html?utm_source=chatgpt.com "ZeRO — DeepSpeed 0.19.2 documentation"
[15]: https://maxtext.readthedocs.io/?utm_source=chatgpt.com "MaxText — MaxText documentation"
[16]: https://docs.cloud.google.com/tpu/docs/samples?utm_source=chatgpt.com "Samples | Cloud TPU"
[17]: https://github.com/togethercomputer/flash-attention-3?utm_source=chatgpt.com "togethercomputer/flash-attention-3: Fast and memory ..."
[18]: https://github.com/linkedin/Liger-Kernel?utm_source=chatgpt.com "Liger Kernel: Efficient Triton Kernels for LLM Training"
[19]: https://docs.flashinfer.ai/?utm_source=chatgpt.com "FlashInfer 0.6.14 documentation"
[20]: https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/?utm_source=chatgpt.com "Model Distillation - Tinker Documentation"
[21]: https://tinker-docs.thinkingmachines.ai/cookbook/recipes/sdft/?utm_source=chatgpt.com "Self-Distillation Fine-Tuning (SDFT) - Tinker Docs"
[22]: https://verl.readthedocs.io/?utm_source=chatgpt.com "Welcome to verl's documentation! — verl documentation"
[23]: https://openrlhf.readthedocs.io/?utm_source=chatgpt.com "Welcome to OpenRLHF's documentation! — OpenRLHF 0.10 ..."
[24]: https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/?utm_source=chatgpt.com "OpenAI-Compatible Server"
[25]: https://docs.sglang.ai/?utm_source=chatgpt.com "Welcome to SGLang - SGLang Documentation"
[26]: https://docs.sglang.ai/advanced_features/structured_outputs.html?utm_source=chatgpt.com "Structured Outputs - SGLang Documentation"
[27]: https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/getting_started/trtllm_user_guide.html?utm_source=chatgpt.com "TensorRT-LLM User Guide — NVIDIA Triton Inference Server"
[28]: https://huggingface.co/docs/inference-endpoints/en/engines/tgi?utm_source=chatgpt.com "Text Generation Inference (TGI)"
[29]: https://huggingface.co/datasets/HuggingFaceFW/fineweb?utm_source=chatgpt.com "HuggingFaceFW/fineweb · Datasets at Hugging Face"
[30]: https://github.com/allenai/dolma?utm_source=chatgpt.com "allenai/dolma: Data and tools for generating and inspecting ..."
[31]: https://www.datacomp.ai/dclm/?utm_source=chatgpt.com "DataComp - LM"
[32]: https://github.com/huggingface/datatrove?utm_source=chatgpt.com "huggingface/datatrove: Freeing data processing ..."
[33]: https://huggingface.co/docs/tokenizers/python/latest/index.html?utm_source=chatgpt.com "Tokenizers — tokenizers documentation"
[34]: https://github.com/google/sentencepiece?utm_source=chatgpt.com "google/sentencepiece: Unsupervised text tokenizer ..."
[35]: https://github.com/EleutherAI/lm-evaluation-harness?utm_source=chatgpt.com "Language Model Evaluation Harness"
[36]: https://inspect.aisi.org.uk/?utm_source=chatgpt.com "Inspect AI"
[37]: https://huggingface.co/docs/lighteval/en/index?utm_source=chatgpt.com "Lighteval"
[38]: https://github.com/openai/evals?utm_source=chatgpt.com "openai/evals: Evals is a framework for evaluating LLMs ..."
[39]: https://docs.skypilot.co/?utm_source=chatgpt.com "SkyPilot: Manage all your AI compute — SkyPilot Docs"
[40]: https://docs.skypilot.co/en/latest/overview.html?utm_source=chatgpt.com "Overview - SkyPilot Docs"
[41]: https://docs.ray.io/en/latest/train/examples/pytorch/pytorch-fsdp/README.html?utm_source=chatgpt.com "Get started with PyTorch Fully Sharded Data Parallel (FSDP2 ..."
[42]: https://docs.coreweave.com/products/storage?utm_source=chatgpt.com "About CoreWeave Storage"
[43]: https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html?utm_source=chatgpt.com "What is Amazon FSx for Lustre?"
[44]: https://docs.cloud.google.com/parallelstore/docs/overview?utm_source=chatgpt.com "Parallelstore"
[45]: https://docs.wandb.ai/?utm_source=chatgpt.com "Weights & Biases Documentation: Build AI agents ..."
[46]: https://mlflow.org/docs/latest/ml/?utm_source=chatgpt.com "MLflow: AI Engineering Platform for LLMs, Agents, & Models"
[47]: https://docs.nvidia.com/datacenter/dcgm/latest/gpu-telemetry/dcgm-exporter.html?utm_source=chatgpt.com "DCGM-Exporter"
[48]: https://opentelemetry.io/docs/?utm_source=chatgpt.com "Documentation"
[49]: https://docs.lambda.ai/public-cloud/1-click-clusters/?utm_source=chatgpt.com "Introduction"
[50]: https://www.baseten.co/blog/baseten-training-is-ga/?utm_source=chatgpt.com "Train AI Models When You Want. Deploy on Ultra ..."
[51]: https://docs.together.ai/docs/serverless/models?utm_source=chatgpt.com "Serverless models"
[52]: https://docs.fireworks.ai/fine-tuning/fine-tuning-models?utm_source=chatgpt.com "Supervised Fine Tuning - Text"
[53]: https://docs.cloud.google.com/tpu/docs/v5p?utm_source=chatgpt.com "TPU v5p"
[54]: https://azure.microsoft.com/en-us/blog/scale-generative-ai-with-new-azure-ai-infrastructure-advancements-and-availability/?utm_source=chatgpt.com "Scale generative AI with new Azure AI infrastructure ..."
[55]: https://www.oracle.com/cloud/compute/gpu/?utm_source=chatgpt.com "GPU, Virtual Machines and Bare Metal"
[56]: https://blogs.oracle.com/cloud-infrastructure/now-ga-largest-ai-supercomputer-oci-nvidia-h200?utm_source=chatgpt.com "The Largest, Fastest AI Supercomputer in the Cloud"
[57]: https://aws.amazon.com/ai/machine-learning/trainium/?utm_source=chatgpt.com "AI Accelerator - AWS Trainium"
[58]: https://developer.nvidia.com/cuda-toolkit-archive?utm_source=chatgpt.com "CUDA Toolkit Archive"
