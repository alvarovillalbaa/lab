Here is the plan I would run. I’m going to be blunt: the right goal is **not** “train a frontier model.” The right goal is **build and publish a complete, reproducible, frontier-style LLM training factory**: data → tokenizer → pretraining → midtraining/continued pretraining → post-training → distillation → evaluation → serving → cost accounting → public technical report. That is enough to prove you know how to do the real thing.

## 0. Define the experiment correctly

Your public claim should be:

> “We trained an LLM from scratch end-to-end, built the full training and serving stack, reproduced current industry-standard stages, and tested novel improvements in compute allocation, self-improvement, and distillation under controlled ablations.”

That is a much stronger and more credible claim than “we trained a big model.”

Use **OLMo 3** as the openness benchmark. OLMo 3’s release is valuable because it includes the full model flow: model stages, checkpoints, data, and dependencies, not just final weights. That is the standard you should copy for credibility. ([allenai.org][1])

Your target should be:

| Target    |                                 Purpose | Recommendation               |
| --------- | --------------------------------------: | ---------------------------- |
| 124M–350M | Learning, CI, debugging, data ablations | mandatory                    |
| 1B–1.5B   |            First serious public release | mandatory                    |
| 3B        |         Strong “I can train LLMs” proof | recommended                  |
| 7B        |                            Stretch goal | only after 1B/3B stack works |

Do **not** start with 7B. That is how people burn money and learn nothing.

---

# 1. Pick the core technical stack

Do not build every low-level component from scratch. Build the parts where you want to innovate. Use battle-tested systems for distributed training, checkpointing, tokenization, serving, and evals.

## Recommended stack

| Layer                         | Primary choice                                                                            | Why                                                                                                                                                                                                                                   |
| ----------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Training framework            | **OLMo-core** or **TorchTitan**                                                           | OLMo-core gives you open-model-flow alignment; TorchTitan is clean PyTorch-native large-scale training code. TorchTitan is designed for rapid experimentation and large-scale generative AI training. ([olmo-core.readthedocs.io][2]) |
| NVIDIA-heavy production stack | **NeMo**                                                                                  | NeMo covers large-scale pretraining, post-training, RL, data curation, evaluation, and deployment components. ([NVIDIA Docs][3])                                                                                                      |
| Data curation                 | Dolma Toolkit, DataTrove/FineWeb pipeline, custom filters                                 | FineWeb and Dolma are strong open baselines. FineWeb is 18.5T+ cleaned/deduplicated English web tokens; Dolma is a 3T-token open corpus with tooling. ([Hugging Face][4])                                                             |
| Data research benchmark       | **DataComp-LM / DCLM**                                                                    | DCLM is explicitly built for data-filtering experiments from 412M to 7B models and evaluates across 53 downstream datasets. ([DataComp][5])                                                                                           |
| Post-training                 | TRL first; verl/OpenRLHF when scaling RL                                                  | TRL supports SFT, DPO, GRPO, and distillation trainers; verl and OpenRLHF are stronger for scalable RL workflows. ([Hugging Face][6])                                                                                                 |
| Evaluation                    | lm-evaluation-harness + Inspect AI + custom evals                                         | lm-eval is a standard open framework for many LLM tasks; Inspect AI is a frontier-eval framework from the UK AI Security Institute/Meridian Labs. ([GitHub][7])                                                                       |
| Serving                       | vLLM primary; SGLang for structured/cached workloads; llama.cpp for local quantized demos | vLLM supports high-throughput serving, quantization, OpenAI-compatible APIs, parallelism, and many architectures; SGLang targets low-latency/high-throughput production serving. ([vLLM][8])                                          |
| Avoid for new serving         | TGI as primary                                                                            | Hugging Face says TGI is in maintenance mode and recommends vLLM or SGLang for new Inference Endpoints. ([Hugging Face][9])                                                                                                           |
| Workload orchestration        | SkyPilot + Slurm/Kueue/Ray                                                                | SkyPilot supports managed jobs and spot recovery; Kueue is Kubernetes-native batch/HPC/AI job queueing; Slurm is the classic cluster workload manager. ([SkyPilot Docs][10])                                                          |

My recommendation: **OLMo-core for the main training pipeline**, **TRL for first post-training**, **verl or OpenRLHF for RL**, **vLLM for serving**, **lm-eval + Inspect for evaluation**, and **SkyPilot + your own scheduler layer** for the GPU allocation research.

---

# 2. Compute strategy and realistic budget

Use the standard rough compute estimate:

[
\text{training FLOPs} \approx 6 \times \text{parameters} \times \text{tokens}
]

For minimal cost, use the Chinchilla-style rule as your baseline: roughly scale model size and training tokens together; in practical terms, many people use about **20 training tokens per parameter** as a planning anchor. The Chinchilla paper’s core result was that compute-optimal training scales model size and token count together, correcting the old habit of training models too large on too few tokens. ([arXiv][11])

Current public GPU prices vary constantly, but as a live public reference, RunPod lists H100 PCIe at **$2.89/hr**, H100 SXM at **$3.29/hr**, A100 PCIe at **$1.39/hr**, and RTX 4090 at **$0.69/hr** on its pricing page. ([Runpod][12])

These are optimistic compute-only estimates, assuming good utilization and excluding storage, failed jobs, idle time, data processing, evals, and retries. Multiply by **1.5–2.5×** for a real budget.

| Run                | Params | Tokens | Assumed hardware           | Approx compute-only GPU cost | Why                                          |
| ------------------ | -----: | -----: | -------------------------- | ---------------------------: | -------------------------------------------- |
| Smoke              |   124M |   2.5B | 1× RTX 4090                |             ~$7 raw GPU cost | proves codepath                              |
| Mini               |   350M |     7B | 8× RTX 4090                |            ~$60 raw GPU cost | data/filtering ablations                     |
| Public v0          |   1.3B |    26B | 8× H100                    |           ~$550 raw GPU cost | first serious end-to-end model               |
| Strong small       |     3B |    60B | 8× H100                    |          ~$2.9k raw GPU cost | credible public model                        |
| 7B compute-optimal |     7B |   140B | 64× H100 or 8× H100 longer |           ~$16k raw GPU cost | stretch                                      |
| 7B overtrained     |     7B |     1T | 64× H100 or longer         |          ~$110k raw GPU cost | closer to modern strong small-model practice |

The **1.3B and 3B runs** are the sweet spot. They are large enough to force you to solve real LLM-training problems, but small enough that mistakes do not bankrupt you.

---

# 3. Public proof standard

You want to “prove the world” you know how to do it. That means publishing more than a Hugging Face model.

Publish these artifacts:

1. **Model weights**: base, midtrained, SFT, preference/RL, distilled, quantized.
2. **Training code**: pinned commit hashes, Dockerfiles, exact launch scripts.
3. **Data recipes**: sources, filters, dedup logic, sampling weights, token counts.
4. **Tokenizer**: training corpus sample description, vocab size, special tokens.
5. **Training logs**: loss curves, throughput, GPU utilization, restart events, eval curves.
6. **Cost ledger**: GPU-hours, storage, failures, eval costs, inference costs.
7. **Evaluation report**: base benchmarks, chat benchmarks, safety benchmarks, contamination checks.
8. **Ablation report**: one table per claimed improvement.
9. **Serving endpoint/demo**: vLLM endpoint, quantized local model, latency/throughput report.
10. **Reproducibility kit**: one command to reproduce the 124M smoke run.

This matters. A weak model with a transparent, reproducible training report is more impressive than a slightly better model with no credible process.

---

# 4. Repository layout

Create a serious monorepo from day one.

```text
llm-lab/
  configs/
    pretrain/
    midtrain/
    sft/
    dpo/
    grpo/
    distill/
    serve/
  data/
    manifests/
    schemas/
    filters/
    tokenizer/
  src/
    training/
    data_pipeline/
    distillation/
    scheduler/
    evaluation/
    serving/
    safety/
    utils/
  infra/
    docker/
    skypilot/
    slurm/
    k8s/
    terraform/
  reports/
    run_cards/
    model_cards/
    data_cards/
    eval_reports/
  notebooks/
    scaling_laws/
    loss_analysis/
    data_quality/
  tests/
    unit/
    integration/
    smoke_training/
```

Every run gets a `run_card.yaml`:

```yaml
run_id: pretrain_1b_v03
model_size: 1.3B
tokens_target: 26B
sequence_length: 4096
global_batch_tokens: 2_000_000
data_mix: data_mix_v04
tokenizer: tokenizer_v02
framework: olmo-core
hardware: 8xH100
precision: bf16
checkpoint_interval_steps: 1000
eval_interval_steps: 500
budget_cap_usd: 2000
git_commit: ...
docker_image: ...
```

---

# 5. Phase 1 — learn by building the smallest full system

Before scaling, build a toy trainer yourself.

## Goal

Train a **20M–60M decoder-only transformer** from scratch on a tiny corpus and serve it.

## Build manually

Implement:

1. tokenizer loading
2. packed dataset loader
3. transformer block
4. RoPE
5. RMSNorm
6. SwiGLU MLP
7. causal attention
8. AdamW
9. cosine or warmup-stable-decay schedule
10. checkpoint save/load
11. eval loss
12. text generation
13. simple chat wrapper
14. vLLM/Transformers export path if possible

This teaches you the mechanics. Then stop writing your own trainer. Move to OLMo-core/TorchTitan.

## Deliverable

A blog post: **“Training a tiny LLM from scratch: every tensor, every bug, every metric.”**

This is not for performance. It is for credibility and personal understanding.

---

# 6. Phase 2 — infrastructure baseline

## 6.1 Containerize everything

Create images for:

```text
llm-train: CUDA + PyTorch + OLMo-core/TorchTitan
llm-data: data processing + tokenization + dedup
llm-eval: lm-eval + Inspect + custom evals
llm-serve: vLLM + SGLang + monitoring
llm-distill: teacher generation + judging + filtering
```

Pin:

```text
CUDA version
NCCL version
PyTorch version
training framework commit
dataset manifest hash
tokenizer hash
```

## 6.2 Use one-node training first

Your first serious target should run on **one 8-GPU node**. Avoid multi-node complexity until you have stable:

* throughput
* checkpointing
* resume
* evals
* data streaming
* loss curves

Multi-node bugs are expensive.

## 6.3 Logging

Track:

| Metric                  | Why                      |
| ----------------------- | ------------------------ |
| train loss              | basic health             |
| validation loss         | overfitting/data quality |
| tokens/sec/GPU          | throughput               |
| MFU                     | training efficiency      |
| GPU memory              | sharding/batch tuning    |
| dataloader time         | data bottlenecks         |
| checkpoint time         | failure recovery         |
| eval scores             | capability               |
| cost per billion tokens | financial control        |

Use W&B, MLflow, or a self-hosted stack. Public W&B reports are useful for credibility.

---

# 7. Phase 3 — data pipeline

Data will decide most of the model quality. Treat data as the main research object.

## 7.1 Start from open corpora

Use a mix like:

| Source                                             | Use                                          |
| -------------------------------------------------- | -------------------------------------------- |
| FineWeb sample/full                                | web backbone                                 |
| Dolma                                              | open reproducible corpus                     |
| code datasets with permissive licenses             | coding                                       |
| Wikipedia / books / papers where licensing permits | knowledge and long-form                      |
| synthetic instruction data                         | post-training, not base pretraining at first |
| your own generated tasks                           | distillation/self-improvement                |

FineWeb is useful because it releases both a large cleaned/deduplicated corpus and reproduction code; Dolma gives a transparent open-data baseline and toolkit. ([Hugging Face][4])

## 7.2 Data processing steps

For each document:

1. normalize Unicode
2. strip boilerplate
3. detect language
4. remove extremely short/long garbage
5. remove duplicated paragraphs
6. exact dedup
7. fuzzy dedup
8. quality score
9. toxicity/safety/PII tagging
10. domain classification
11. license/source tracking
12. tokenize
13. pack into fixed-length sequences
14. shard into deterministic files
15. build manifest with hashes

Manifest example:

```json
{
  "shard_id": "fineweb_en_000123",
  "source": "fineweb",
  "tokens": 104857600,
  "documents": 392144,
  "language": "en",
  "dedup_version": "minhash_v03",
  "quality_filter": "qclf_v02_threshold_0.72",
  "license": "ODC-BY-1.0",
  "sha256": "..."
}
```

## 7.3 Build three data mixes

Do not use one mix. Use three:

| Mix                  | Purpose                             |
| -------------------- | ----------------------------------- |
| `baseline_mix`       | mostly FineWeb/Dolma-style          |
| `quality_mix`        | stricter quality filters, less data |
| `reasoning_code_mix` | more code/math/science              |

Run all three at **124M/350M scale** before choosing the 1B/3B mix.

## 7.4 Data research opportunity

Your first publishable research contribution could be:

> “A cheap multi-stage data filter that improves downstream score per training dollar.”

Use DCLM-style controlled evaluation: same model, same tokens, same compute, only data filter changes. DCLM exists exactly because data curation can be studied systematically across model scales. ([DataComp][5])

---

# 8. Phase 4 — tokenizer

Train your own tokenizer, even if you later compare against an existing one.

## Recommended tokenizer plan

| Parameter       | Recommendation                                             |
| --------------- | ---------------------------------------------------------- |
| Type            | BPE or Unigram                                             |
| Vocab size      | 32k for small models, 50k–64k for 1B+                      |
| Training sample | 10B–50B characters from final data mix                     |
| Special tokens  | BOS, EOS, PAD, UNK, system/user/assistant if chat          |
| Code support    | ensure indentation and common code tokens are handled well |
| Evaluation      | compression ratio by domain                                |

Tokenizer eval table:

| Dataset slice | chars/token | tokens/doc | unknown rate | notes |
| ------------- | ----------: | ---------: | -----------: | ----- |
| web           |             |            |              |       |
| code          |             |            |              |       |
| math          |             |            |              |       |
| Spanish       |             |            |              |       |
| tables        |             |            |              |       |

Even if the final model is English-heavy, include multilingual slices in tokenizer testing so you understand the tradeoff.

---

# 9. Phase 5 — model architecture

Start with a dense decoder-only transformer. Do not start with MoE.

## Baseline architecture

Use a modern Llama-like architecture:

* decoder-only causal LM
* RMSNorm
* SwiGLU
* RoPE
* grouped-query attention for larger models
* no dropout or very low dropout
* tied or untied embeddings, but document the choice
* context length 2048 or 4096 for base pretraining
* long-context extension as a separate stage

## Suggested model ladder

| Name     | Params | Layers |    Hidden | Heads |   Seq len |
| -------- | -----: | -----: | --------: | ----: | --------: |
| lab-124m |  ~124M |     12 |       768 |    12 |      2048 |
| lab-350m |  ~350M |     24 |      1024 |    16 | 2048/4096 |
| lab-1.3b |  ~1.3B |     24 |      2048 | 16/32 |      4096 |
| lab-3b   |    ~3B |     32 | 2560/3072 |    32 |      4096 |
| lab-7b   |    ~7B |     32 |      4096 |    32 |      4096 |

Exact shapes should be chosen to fit your framework and GPU memory.

## Research architecture track

Only after the dense baseline works, test:

1. hybrid attention/RNN layers
2. sliding-window attention
3. sparse attention
4. MoE
5. modular expert post-training

Hybrid architectures are a serious research direction. Ai2’s Olmo Hybrid replaced many attention layers with Gated DeltaNet-style recurrent layers and reported large token-efficiency gains in controlled comparisons, so this is a credible place to explore improvements. ([allenai.org][13])

---

# 10. Phase 6 — pretraining ladder

## 10.1 Smoke run

Train 124M on 100M–500M tokens.

Success criteria:

* loss decreases smoothly
* no NaNs
* checkpoints resume
* eval job runs
* model can generate coherent-ish text
* vLLM/Transformers export path works

## 10.2 Mini scaling run

Train 124M and 350M models on multiple data mixes:

```text
124M x baseline_mix
124M x quality_mix
124M x reasoning_code_mix
350M x best_two_mixes
```

Track:

* validation loss by domain
* downstream evals
* cost
* tokens/sec
* instability events

Choose the final mix based on **eval-per-dollar**, not vibes.

## 10.3 1.3B run

Train ~1.3B on ~26B tokens.

Stages:

1. general pretraining
2. high-quality cooldown/midtraining
3. optional long-context extension
4. base eval
5. release base checkpoint

Do **not** post-train until the base model is evaluated and frozen.

## 10.4 3B run

Train only after the 1.3B pipeline is stable.

The 3B run is your first serious “I can train LLMs” proof. It forces you to solve throughput, memory, checkpointing, data quality, and evals without needing frontier money.

---

# 11. Phase 7 — pretraining configuration

Use this as your starting config, then tune from smaller runs.

| Hyperparameter     | Starting point                         |
| ------------------ | -------------------------------------- |
| optimizer          | AdamW                                  |
| betas              | 0.9, 0.95                              |
| weight decay       | 0.1                                    |
| grad clip          | 1.0                                    |
| precision          | bf16; FP8 only after baseline works    |
| LR schedule        | warmup + cosine or warmup-stable-decay |
| warmup             | 1–2% of total steps                    |
| sequence length    | 4096 for 1B+                           |
| global batch       | 0.5M–4M tokens                         |
| checkpoint         | every 500–2000 steps                   |
| eval               | every 250–1000 steps                   |
| heldout validation | fixed, versioned, never trained on     |

Stop the run immediately if:

* loss spikes and does not recover
* MFU is far below target
* dataloader stalls
* checkpoints cannot resume
* eval contamination is found
* validation loss diverges from train loss unusually early

---

# 12. Phase 8 — post-training

Post-training should be treated as multiple controlled stages, not one messy fine-tune.

## 12.1 SFT: supervised fine-tuning

Goal: make the base model instruction-following.

Data:

* permissively licensed instruction data
* your synthetic instruction data
* tool-use examples
* refusal/safety examples
* formatting examples

Rules:

* use a fixed chat template
* mask user/system tokens in loss
* keep validation split by source
* avoid training on benchmark answers
* evaluate every checkpoint

Deliverable:

```text
lab-1.3b-sft
lab-3b-sft
```

## 12.2 Preference optimization

Start with DPO before PPO-style RL. DPO is simpler, cheaper, and easier to debug.

Data:

* chosen/rejected pairs
* teacher-ranked outputs
* human-labeled pairs where possible
* self-generated pairs filtered by judges/verifiers

Algorithms:

* DPO
* IPO/KTO/ORPO as ablations
* GRPO for verifiable reasoning tasks

TRL has trainers for post-training and distillation, including DPO/GRPO-style workflows; its GRPO documentation describes the online loop of generating completions, computing rewards, estimating KL, and updating the model. ([Hugging Face][6])

## 12.3 RL with verifiable rewards

Use RL only where rewards are objective:

| Domain                | Reward                               |
| --------------------- | ------------------------------------ |
| math                  | exact answer / symbolic checker      |
| code                  | unit tests                           |
| tool use              | task success                         |
| JSON/function calling | schema validation                    |
| retrieval QA          | answer contains cited source span    |
| safety                | policy classifier + human spot-check |

For scaled RL, use verl or OpenRLHF. verl integrates with FSDP, Megatron-LM, vLLM, SGLang, and supports flexible device mapping; OpenRLHF uses a Ray + vLLM distributed architecture and advertises scaling to 70B+ models. ([GitHub][14])

## 12.4 Safety post-training

Minimum safety work:

1. refusal data
2. jailbreak evals
3. harmful request evals
4. PII leakage tests
5. hallucination/factuality tests
6. prompt-injection tests for tool use
7. deployment moderation layer

Ai2’s Safety Toolkit is a good open reference point; it includes WildGuard and safety-eval resources for harmfulness/refusal style work. ([allenai.org][15])

---

# 13. Phase 9 — build the advanced distillation system

This is where you can actually innovate.

Do not think of distillation as “ask GPT-4 a bunch of questions and fine-tune.” That is amateur. Build a **data engine**.

## 13.1 Distillation system architecture

```text
Prompt/task generator
        ↓
Teacher registry
        ↓
Multi-teacher response generation
        ↓
Verifier/judge ensemble
        ↓
Preference pair builder
        ↓
Curriculum sampler
        ↓
Student trainer
        ↓
Evaluator/gatekeeper
        ↓
Lineage database
```

## 13.2 Core components

### A. Teacher registry

Track every teacher:

```yaml
teacher_id: qwen_xxx
type: open_weights
license: apache-2.0
allowed_for_distillation: true
strengths:
  - math
  - code
weaknesses:
  - safety
  - long_context
cost_per_1m_tokens: ...
latency: ...
```

Important: only train on teacher outputs when the license or provider terms allow it. Do not assume API outputs are allowed for model training.

### B. Task generator

Generate prompts by domain:

```text
math
code
science
instruction following
tool use
long context
summarization
structured output
safety/refusal
multilingual
```

Task metadata:

```json
{
  "task_id": "math_000123",
  "domain": "math",
  "difficulty": 0.72,
  "source": "synthetic_seed_v4",
  "requires_verifier": true,
  "expected_answer_type": "integer",
  "contamination_checked": true
}
```

### C. Multi-teacher generation

For each prompt:

* sample from 2–5 teachers
* use multiple temperatures
* generate concise and detailed versions
* generate chain-of-thought only when allowed and appropriate
* generate incorrect distractors for preference training
* record all metadata

### D. Verifiers

Use objective verifiers whenever possible:

| Domain    | Verifier                        |
| --------- | ------------------------------- |
| code      | run tests in sandbox            |
| math      | symbolic/numeric checker        |
| JSON      | schema validator                |
| tool use  | environment success             |
| citations | source-span checker             |
| safety    | policy classifier + spot checks |

LLM judges are useful, but never trust only an LLM judge for your core claims.

### E. Preference builder

Create preference pairs:

```text
chosen = verified correct, clear, safe, efficient
rejected = incorrect, verbose, unsafe, hallucinated, formatting failure
```

Also create **hard negatives**:

* plausible but wrong math
* code that passes simple tests but fails hidden tests
* answers with subtle instruction violations
* unsafe over-refusals
* unsafe under-refusals

### F. Curriculum sampler

Train from:

```text
easy → medium → hard
short → long
single skill → composed skill
teacher-generated → student-generated
verified → judge-assisted
```

### G. Student uncertainty sampling

Have the student attempt tasks. Prioritize examples where:

* student is wrong but teacher/verifier is right
* teachers disagree
* student confidence is high but wrong
* reward model uncertainty is high
* eval regression appears in a domain

This makes distillation compute-efficient.

## 13.3 Distillation methods to implement

| Method                            | Use                                                      |
| --------------------------------- | -------------------------------------------------------- |
| SFT distillation                  | basic teacher imitation                                  |
| Logit distillation                | only with open/local teachers where logits are available |
| Preference distillation           | DPO/IPO/KTO from teacher rankings                        |
| Process distillation              | train on verified solution traces                        |
| Rejection sampling                | sample many, keep verified best                          |
| Self-distillation                 | student generates, verifier filters                      |
| Specialist distillation           | math/code/tool/safety specialists                        |
| Router distillation               | route prompts to specialists or train MoE-style router   |
| Speculative decoding distillation | train small draft model for faster serving               |

## 13.4 Research-grade distillation experiments

Run these as controlled ablations:

| Experiment                                              | Hypothesis                                      |
| ------------------------------------------------------- | ----------------------------------------------- |
| single teacher vs multi-teacher                         | teacher diversity improves robustness           |
| LLM judge vs verifier                                   | objective verifiers reduce false positives      |
| random synthetic data vs uncertainty-selected data      | active selection improves eval-per-token        |
| SFT only vs SFT+DPO                                     | preferences improve instruction-following       |
| SFT+DPO vs SFT+GRPO on verifiable tasks                 | RL improves reasoning where reward is objective |
| dense post-training vs specialist modular post-training | specialists reduce capability interference      |

Ai2’s Branch-Adapt-Route work is relevant here: they train domain experts separately, merge into an MoE-style model, and train the router cheaply using a small stratified sample; they report that modular training avoids some cross-domain interference. ([allenai.org][16])

Your novel angle could be:

> “Distillation as an autonomous, verifier-gated, cost-aware curriculum system.”

That is a serious research direction.

---

# 14. Phase 10 — self-improvement loop

Self-improvement must be bounded. Do not let the model recursively train itself with no ground truth. That produces model collapse, benchmark hacking, and fake progress.

## Safe self-improvement loop

```text
student generates tasks
        ↓
teacher/verifier filters tasks
        ↓
student attempts tasks
        ↓
objective verifier scores attempts
        ↓
high-quality traces become training data
        ↓
candidate model trains
        ↓
candidate evaluated on frozen holdout
        ↓
only promote if it improves without regressions
```

## Promotion gates

A candidate model is promoted only if:

| Gate                  | Requirement                           |
| --------------------- | ------------------------------------- |
| base capability       | no drop beyond tolerance              |
| target domain         | statistically meaningful improvement  |
| safety                | no regression                         |
| instruction following | no regression                         |
| contamination         | clean                                 |
| diversity             | synthetic data not collapsing         |
| cost                  | improvement per dollar beats baseline |

Self-improvement research should focus on **verifiable domains first**: math, code, tool use, structured outputs, retrieval tasks. Do not start with open-ended “be more helpful” tasks.

---

# 15. Phase 11 — autonomous GPU workload allocation

This is another good innovation target.

The mistake most teams make: they optimize one training run. You should optimize the **entire research portfolio**.

## 15.1 Workload types

| Workload            | Hardware                 |
| ------------------- | ------------------------ |
| data cleaning       | CPU-heavy, cheap         |
| tokenization        | CPU or cheap GPU         |
| teacher generation  | cheap GPUs / spot        |
| evals               | cheap GPUs, batchable    |
| 124M/350M ablations | 4090/A100                |
| 1B/3B training      | homogeneous 8× H100/A100 |
| RL rollouts         | H100/A100 + vLLM         |
| serving benchmark   | target deployment GPU    |

Do not mix heterogeneous GPUs inside one tightly coupled pretraining job unless the framework explicitly supports it well. Use heterogeneity across the workload queue.

## 15.2 Scheduler objective

Your scheduler should maximize:

[
\frac{\text{expected information gain or eval improvement}}{\text{expected dollars} \times \text{risk}}
]

Each job gets:

```yaml
job_id: data_ablation_350m_quality_v05
gpu_type_options: [RTX4090, A100, H100]
min_gpus: 1
max_gpus: 8
preemptible_ok: true
checkpoint_interval_minutes: 15
expected_value: 0.73
expected_cost_usd: 120
deadline: none
risk: 0.2
```

## 15.3 Scheduler policies to compare

| Policy              | Description                                        |
| ------------------- | -------------------------------------------------- |
| FIFO                | baseline                                           |
| cheapest-first      | minimize cost                                      |
| fastest-first       | minimize wall time                                 |
| value-per-dollar    | your first real policy                             |
| Bayesian scheduler  | prioritizes uncertain high-upside experiments      |
| preemption-aware    | chooses spot only when checkpointing makes it safe |
| portfolio optimizer | balances data, training, eval, distillation jobs   |

## 15.4 Metrics

Track:

* GPU utilization
* idle GPU-hours
* failed GPU-hours
* preemption recovery time
* queue wait time
* cost per completed experiment
* cost per benchmark improvement
* wall-clock time to decision
* number of ablations completed per $1,000

This can become a legitimate systems paper/blog:

> “Cost-aware autonomous scheduling for LLM training research.”

---

# 16. Phase 12 — evaluation

Your eval suite needs three levels.

## 16.1 Base model evals

Use:

* validation loss by domain
* perplexity/bits-per-byte slices
* ARC
* HellaSwag
* PIQA
* Winogrande
* MMLU-style tests
* GSM/math
* HumanEval/MBPP-style code
* long-context retrieval if you train long context

lm-evaluation-harness supports many standard tasks, vLLM-backed evaluation, local models, adapters, and custom prompts/metrics, making it a practical backbone for this. ([GitHub][7])

## 16.2 Chat/post-training evals

Use:

* instruction-following tests
* format-following tests
* tool-call correctness
* pairwise model comparisons
* human spot checks
* LLM judge with calibration
* safety/refusal evals

## 16.3 Research evals

For every claimed improvement, run:

```text
baseline model
+ one change
same data budget
same training budget
same eval suite
same random seeds where possible
confidence interval or bootstrap
```

Do not claim “improvement” from one lucky run.

---

# 17. Phase 13 — serving

Serving is part of the experiment, not an afterthought.

## 17.1 Export formats

Produce:

```text
HF safetensors
vLLM-compatible checkpoint
SGLang-compatible checkpoint
GGUF quantized model
LoRA/adapters if used
```

llama.cpp is useful for local demos because it targets minimal setup across local/cloud hardware and supports many quantization levels. ([GitHub][17])

## 17.2 vLLM deployment

Deploy:

```text
base model endpoint
sft model endpoint
dpo/rl model endpoint
distilled model endpoint
quantized model endpoint
```

Measure:

| Metric                         | Required |
| ------------------------------ | -------- |
| p50/p95 time-to-first-token    | yes      |
| output tokens/sec              | yes      |
| max concurrent users           | yes      |
| GPU memory                     | yes      |
| cost per 1M input tokens       | yes      |
| cost per 1M output tokens      | yes      |
| quality loss from quantization | yes      |

vLLM is the right default because it supports high-throughput serving, OpenAI-compatible APIs, many quantization modes, parallelism, prefix caching, structured outputs, tool calling, and many Hugging Face architectures. ([vLLM][8])

## 17.3 Public demo

Create:

* simple chat UI
* `/v1/chat/completions` endpoint
* model card
* eval dashboard
* cost dashboard
* “compare base vs post-trained vs distilled” mode

This proves you can serve the model, not just train it.

---

# 18. Phase 14 — security, safety, and governance

Minimum standards:

1. no training on private data without rights
2. no benchmark contamination
3. no hidden closed-source data in public claims
4. document all synthetic data sources
5. store prompts/responses with lineage
6. filter PII
7. run harmfulness and jailbreak evals
8. put a safety gateway in front of public demos
9. keep training and serving infrastructure isolated
10. never expose internal SGLang/vLLM worker ports directly to the public internet

For self-improvement and autonomous agents, be extra strict: every loop needs frozen evals, objective gates, rollback, and human review.

---

# 19. Phase 15 — concrete timeline

## Weeks 1–2: foundation

Deliverables:

* monorepo
* Docker images
* tiny from-scratch transformer
* 20M–60M toy model trained
* local generation demo
* first blog post
* cost tracker

## Weeks 3–4: data pipeline

Deliverables:

* FineWeb/Dolma sample ingestion
* dedup pipeline
* tokenizer v1
* data manifests
* 124M smoke run
* eval harness connected

## Weeks 5–6: mini ablations

Deliverables:

* 124M × 3 data mixes
* 350M × 2 data mixes
* throughput report
* first data-quality ablation report
* scheduler prototype v0

## Weeks 7–10: 1.3B base model

Deliverables:

* 1.3B pretraining
* base eval report
* vLLM serving
* public base checkpoint
* model card + data card

## Weeks 11–14: post-training

Deliverables:

* SFT model
* DPO model
* GRPO/RLVR on math/code if ready
* safety evals
* chat demo

## Weeks 15–18: distillation system

Deliverables:

* teacher registry
* synthetic task generator
* verifier system
* SFT/DPO distilled model
* self-improvement loop v0
* distillation ablation report

## Weeks 19–24: 3B run

Deliverables:

* 3B base
* 3B post-trained
* 3B distilled
* serving benchmark
* full technical report

## Stretch: 7B

Do this only after the 3B model and all reports are public.

---

# 20. What your first public technical report should contain

Title:

> **Training Lab-1B: An Open End-to-End LLM Training, Distillation, and Serving Pipeline**

Sections:

1. Abstract
2. Motivation
3. Compute budget
4. Data sources
5. Data filtering
6. Tokenizer
7. Architecture
8. Training setup
9. Scaling ladder
10. Base model results
11. Post-training
12. Distillation system
13. Self-improvement experiments
14. GPU scheduler
15. Serving benchmarks
16. Safety evaluation
17. Failures and bugs
18. Cost ledger
19. Reproducibility instructions
20. Future work

The “failures and bugs” section is important. Serious people trust reports that admit what broke.

---

# 21. The three best innovation bets

## Bet 1: Cost-aware autonomous GPU allocation

This is practical and publishable. Most small labs waste money because they do not schedule research portfolios well.

Your claim:

> “Our scheduler completed more useful ablations per dollar than manual scheduling while preserving final model quality.”

## Bet 2: Verifier-gated distillation

This is probably your strongest model-quality bet.

Your claim:

> “Verifier-gated multi-teacher distillation improves reasoning/tool-use performance per synthetic token and reduces harmful hallucinated synthetic data.”

## Bet 3: Self-improvement with promotion gates

This is risky but exciting.

Your claim:

> “A bounded self-improvement loop improves verifiable tasks without degrading frozen general/safety evals.”

Do not claim recursive self-improvement. Claim bounded, measured, verifier-gated improvement.

---

# 22. What not to do

Do not:

* start with a 7B run
* train on random scraped data with no documentation
* use synthetic data without lineage
* use closed/API teacher outputs without checking terms
* tune directly on benchmark sets
* rely only on LLM judges
* publish only final weights
* claim “state of the art” without controlled baselines
* write your own distributed training framework before you have trained a model
* run RL before SFT/DPO are stable
* optimize for leaderboard score over reproducibility

The fastest way to look unserious is to train a mediocre model expensively and hide the process. The fastest way to look serious is to publish a clean, reproducible, well-instrumented model factory.

---

# 23. The exact first execution plan

Start here.

## Day 1–2

Create repo, Docker, logging, cost ledger.

## Day 3–5

Implement tiny transformer from scratch. Train on a tiny corpus. Generate samples.

## Day 6–7

Set up OLMo-core or TorchTitan. Run official/small config.

## Week 2

Build data pipeline:

```text
download sample
clean
dedup
tokenize
pack
manifest
train 124M
eval
serve
```

## Week 3

Run three 124M data ablations.

## Week 4

Train 350M. Publish first public report.

## Month 2

Train 1.3B. Post-train it. Serve it. Publish everything.

## Month 3–4

Build distillation system and self-improvement loop.

## Month 5–6

Train 3B and publish the full flagship report.

That path gives you what you want: you learn deeply, you prove competence publicly, and you create multiple real research surfaces instead of merely renting GPUs.

[1]: https://allenai.org/papers/olmo3 "[2512.13961] Olmo 3"
[2]: https://olmo-core.readthedocs.io/en/latest/overview/introduction.html?utm_source=chatgpt.com "Introduction - OLMo-core v2.5.0"
[3]: https://docs.nvidia.com/nemo/index.html "NVIDIA NeMo"
[4]: https://huggingface.co/datasets/HuggingFaceFW/fineweb "HuggingFaceFW/fineweb · Datasets at Hugging Face"
[5]: https://www.datacomp.ai/dclm/ "DataComp"
[6]: https://huggingface.co/docs/trl/en/index "TRL - Transformers Reinforcement Learning · Hugging Face"
[7]: https://github.com/EleutherAI/lm-evaluation-harness "GitHub - EleutherAI/lm-evaluation-harness: A framework for few-shot evaluation of language models. · GitHub"
[8]: https://docs.vllm.ai/ "vLLM"
[9]: https://huggingface.co/docs/inference-endpoints/en/engines/tgi "Text Generation Inference (TGI) · Hugging Face"
[10]: https://docs.skypilot.co/en/latest/examples/spot-jobs.html?utm_source=chatgpt.com "Managed Jobs - SkyPilot Docs"
[11]: https://arxiv.org/abs/2203.15556?utm_source=chatgpt.com "Training Compute-Optimal Large Language Models"
[12]: https://www.runpod.io/pricing "GPU Cloud Pricing | Per-Second H100, A100, RTX | Runpod"
[13]: https://allenai.org/blog/olmohybrid "Introducing Olmo Hybrid: Combining transformers and linear RNNs for superior scaling  | Ai2"
[14]: https://github.com/verl-project/verl "GitHub - verl-project/verl: verl/HybridFlow: A Flexible and Efficient RL Post-Training Framework · GitHub"
[15]: https://allenai.org/blog/the-ai2-safety-toolkit-datasets-and-models-for-safe-and-responsible-llms-development-10abc05f6c80?utm_source=chatgpt.com "The Ai2 Safety Toolkit: Datasets and models for safe and ..."
[16]: https://allenai.org/blog/bar "Train separately, merge together: Modular post-training with mixture-of-experts  | Ai2"
[17]: https://github.com/ggml-org/llama.cpp "GitHub - ggml-org/llama.cpp: LLM inference in C/C++ · GitHub"
