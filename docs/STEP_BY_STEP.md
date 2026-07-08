# Full Step-by-Step LLM Lab Plan

This plan consolidates the pasted mission and every spec in
`docs/specs/`. It is intentionally staged: the lab proves competence through
reproducibility, controlled experiments, and public artifacts before spending
money on larger training runs.

## 0. Define the Experiment

1. Do not claim "frontier model" as the first milestone.
2. Claim a reproducible, frontier-style training factory:
   data, tokenizer, pretraining, midtraining, post-training, distillation,
   evaluation, serving, cost ledger, and public report.
3. Use local/from-scratch execution as the credibility anchor.
4. Use managed providers only behind explicit adapters.
5. Freeze the public claim in `DECISIONS.md` before GPU spending.

Deliverables:

- `DECISIONS.md`.
- Public claim.
- Budget cap.
- Initial model ladder.
- Success gates.

## 1. Choose the Core Stack

1. Use Python 3.11 or 3.12.
2. Use standard-library validation first so the repo works locally without GPU
   dependencies.
3. Use OLMo-core or TorchTitan for serious pretraining.
4. Use TRL locally for first SFT/DPO/GRPO experiments.
5. Use Tinker for managed post-training when available.
6. Use vLLM for local serving and Baseten for public serving.
7. Use lm-eval, Inspect AI, LightEval, and custom verifier evals.
8. Use SkyPilot, Slurm, Kubernetes/Kueue, and provider adapters for orchestration
   after local execution works.

Deliverables:

- Dependency groups documented.
- Provider abstraction.
- First local configs.
- Validation CLI.

## 2. Build the Repository Contract

1. Keep one canonical experiment spec that can route to multiple providers.
2. Keep provider configs separate from experiment configs.
3. Require run cards, model cards, data cards, eval reports, and cost ledgers for
   public proof.
4. Keep human decisions in `DECISIONS.md`, not implicit in code.
5. Keep every generated dataset/model/checkpoint traceable to source manifests.

Deliverables:

- `configs/experiments/*.json`.
- `configs/providers/*.json`.
- `reports/templates/*`.
- `docs/SPEC_COVERAGE.md`.

## 3. Phase 1: Tiny From-Scratch System

Goal: train a 20M to 60M decoder-only transformer from scratch on a tiny corpus
and serve generated text locally.

Steps:

1. Implement tokenizer loading.
2. Implement packed dataset loading.
3. Implement decoder-only transformer blocks.
4. Implement RoPE.
5. Implement RMSNorm.
6. Implement SwiGLU MLP.
7. Implement causal attention.
8. Implement AdamW.
9. Implement warmup plus cosine or warmup-stable-decay schedule.
10. Implement checkpoint save/load.
11. Implement eval loss.
12. Implement text generation.
13. Implement simple chat wrapper.
14. Export to Transformers-compatible format if practical.

Success criteria:

- Loss decreases.
- No NaNs.
- Checkpoint resume works.
- Generation produces coherent-ish samples.
- Run card and cost ledger are filled.

## 4. Phase 2: Infrastructure Baseline

Steps:

1. Create CUDA/PyTorch training image.
2. Create data-processing image.
3. Create eval image.
4. Create serving image.
5. Create distillation image.
6. Pin CUDA, NCCL, PyTorch, framework commits, dataset hashes, and tokenizer
   hashes.
7. Run one-node training before multi-node training.
8. Track loss, validation loss, tokens/sec/GPU, MFU, GPU memory, dataloader time,
   checkpoint time, eval scores, and cost per billion tokens.

Success criteria:

- Container builds are reproducible.
- A smoke run can resume after interruption.
- Metrics and cost ledger are captured.

## 5. Phase 3: Data Pipeline

Steps for every document:

1. Normalize Unicode.
2. Strip boilerplate.
3. Detect language.
4. Remove extremely short or long garbage.
5. Remove duplicated paragraphs.
6. Exact dedup.
7. Fuzzy dedup.
8. Quality score.
9. Toxicity, safety, and PII tagging.
10. Domain classification.
11. License and source tracking.
12. Tokenize.
13. Pack fixed-length sequences.
14. Shard deterministic files.
15. Build manifests with hashes.

Required data mixes:

- `baseline_mix`: FineWeb/Dolma-style baseline.
- `quality_mix`: stricter quality filters.
- `reasoning_code_mix`: more code, math, and science.

Success criteria:

- Deterministic manifests.
- Token counts by source/domain/license.
- Reproducible train/validation split.
- No data source without rights metadata.

## 6. Phase 4: Tokenizer

Steps:

1. Train an internal tokenizer even if comparing to an existing tokenizer.
2. Start with byte-level BPE or Unigram.
3. Use 32k vocab for small models and 50k to 64k for 1B+ models.
4. Include BOS, EOS, PAD, UNK, system, user, and assistant tokens when chat is in
   scope.
5. Evaluate compression by domain: web, code, math, Spanish, tables, and long
   documents.

Success criteria:

- Tokenizer card.
- Compression table.
- Hash-pinned tokenizer artifact.

## 7. Phase 5: Model Architecture

Baseline:

1. Dense decoder-only causal LM.
2. RMSNorm.
3. SwiGLU.
4. RoPE.
5. Grouped-query attention for larger models.
6. No dropout or very low dropout.
7. Context length 2048 or 4096.
8. Long-context extension as a separate stage.

Model ladder:

- `lab-20m` or `lab-60m`: mechanics and local proof.
- `lab-124m`: mandatory smoke and ablation target.
- `lab-350m`: mini scaling target.
- `lab-1.3b`: first serious public release.
- `lab-3b`: strong competence proof.
- `lab-7b`: stretch only after 3B.

## 8. Phase 6: Pretraining Ladder

Smoke run:

1. Train 124M on 100M to 500M tokens.
2. Prove loss decreases.
3. Prove checkpoint resume.
4. Run eval.
5. Generate samples.
6. Export checkpoint.

Mini scaling:

1. Train 124M on the three data mixes.
2. Train 350M on the best two mixes.
3. Choose the final mix by eval-per-dollar.

1.3B:

1. General pretraining.
2. High-quality cooldown or midtraining.
3. Optional long-context extension.
4. Base eval.
5. Freeze and release base checkpoint before post-training.

3B:

1. Run only after 1.3B is stable.
2. Publish full throughput, cost, eval, failure, and reproducibility report.

## 9. Phase 7: Training Configuration

Defaults:

- AdamW.
- Betas 0.9 and 0.95.
- Weight decay 0.1.
- Grad clip 1.0.
- bf16 precision.
- Warmup plus cosine or warmup-stable-decay.
- Warmup 1 to 2 percent of total steps.
- Sequence length 4096 for 1B+.
- Global batch 0.5M to 4M tokens.
- Checkpoint every 500 to 2000 steps.
- Eval every 250 to 1000 steps.
- Fixed versioned heldout validation.

Stop immediately if loss spikes without recovery, MFU is far below target,
dataloader stalls, checkpoints cannot resume, contamination is found, or
validation diverges unusually early.

## 10. Phase 8: Post-Training

SFT:

1. Use a fixed chat template.
2. Mask user/system tokens in loss.
3. Use permissive instruction data.
4. Include tool-use, refusal, safety, and formatting examples.
5. Evaluate every checkpoint.

Preference optimization:

1. Start with DPO.
2. Add IPO, KTO, ORPO, or GRPO as ablations.
3. Use chosen/rejected pairs from teachers, humans, and verifiers.

RL with verifiable rewards:

1. Start with math exact answers, code unit tests, JSON schema validation,
   retrieval citation checks, and tool-use success.
2. Use verl or OpenRLHF only after local TRL loops are stable.

Safety post-training:

1. Refusal data.
2. Jailbreak evals.
3. Harmful request evals.
4. PII leakage tests.
5. Hallucination/factuality tests.
6. Prompt-injection tests.
7. Deployment moderation layer.

## 11. Phase 9: Distillation System

Architecture:

```text
prompt/task generator
teacher registry
multi-teacher response generation
verifier/judge ensemble
preference pair builder
curriculum sampler
student trainer
evaluator/gatekeeper
lineage database
```

Steps:

1. Build teacher registry with license, strengths, weaknesses, cost, and allowed
   distillation status.
2. Generate tasks by domain: math, code, science, instruction following, tool
   use, long context, summarization, structured output, safety, multilingual.
3. Generate 2 to 5 teacher responses where allowed.
4. Use objective verifiers first: code tests, math checkers, JSON schema, tool
   success, citation span checks, safety classifier.
5. Build preference pairs from verified chosen/rejected outputs.
6. Add hard negatives.
7. Train curriculum from easy to hard and short to long.
8. Prioritize examples where the student is wrong, teachers disagree, or reward
   uncertainty is high.

Research ablations:

- Single teacher vs multi-teacher.
- LLM judge vs objective verifier.
- Random synthetic vs uncertainty-selected data.
- SFT only vs SFT plus DPO.
- SFT plus DPO vs SFT plus GRPO.
- Dense post-training vs specialist modular post-training.

## 12. Phase 10: Bounded Self-Improvement

Steps:

1. Student generates tasks.
2. Teacher/verifier filters tasks.
3. Student attempts tasks.
4. Objective verifier scores attempts.
5. High-quality traces become training data.
6. Candidate model trains.
7. Candidate is evaluated on frozen holdout sets.
8. Candidate is promoted only if it improves without regressions.

Promotion gates:

- Base capability does not drop beyond tolerance.
- Target domain improvement is statistically meaningful.
- Safety does not regress.
- Instruction following does not regress.
- Contamination checks are clean.
- Synthetic data diversity does not collapse.
- Improvement per dollar beats baseline.

## 13. Phase 11: Autonomous GPU Workload Allocation

Steps:

1. Classify workload types: data cleaning, tokenization, teacher generation,
   evals, 124M/350M ablations, 1B/3B training, RL rollouts, serving benchmarks.
2. Avoid heterogeneous GPUs inside one tightly coupled training job unless the
   framework supports it well.
3. Optimize the whole research portfolio, not one run.
4. Compare FIFO, cheapest-first, fastest-first, value-per-dollar, Bayesian,
   preemption-aware, and portfolio policies.
5. Track GPU utilization, idle GPU-hours, failed GPU-hours, preemption recovery,
   queue wait, cost per experiment, cost per benchmark improvement, wall-clock
   time to decision, and ablations per USD 1000.

## 14. Phase 12: Evaluation

Base evals:

- Validation loss by domain.
- Perplexity/bits-per-byte slices.
- ARC, HellaSwag, PIQA, Winogrande, MMLU-style tasks.
- GSM/math.
- HumanEval/MBPP-style code.
- Long-context retrieval when trained.

Chat evals:

- Instruction following.
- Format following.
- Tool-call correctness.
- Pairwise comparisons.
- Human spot checks.
- Calibrated LLM judge.
- Safety/refusal evals.

Research eval rule:

For every claimed improvement, compare baseline plus one change with the same
data budget, training budget, eval suite, random seeds where possible, and
confidence intervals or bootstrap.

## 15. Phase 13: Serving

Steps:

1. Export HF safetensors.
2. Export vLLM-compatible checkpoint.
3. Export SGLang-compatible checkpoint if needed.
4. Export GGUF quantized model for local demo when practical.
5. Serve base, SFT, DPO/RL, distilled, and quantized variants.
6. Measure p50/p95 time-to-first-token, output tokens/sec, max concurrency, GPU
   memory, cost per 1M input tokens, cost per 1M output tokens, and quality loss
   from quantization.
7. Build a simple chat UI and OpenAI-compatible `/v1/chat/completions` endpoint.

Provider rule:

- Baseten is the public serving default.
- Local/self-hosted vLLM is the reproducibility benchmark.

## 16. Phase 14: Security, Safety, and Governance

Minimum standards:

1. No private data without rights.
2. No benchmark contamination.
3. No hidden closed-source data in public claims.
4. Document all synthetic data sources.
5. Store prompts and responses with lineage.
6. Filter PII.
7. Run harmfulness and jailbreak evals.
8. Put a safety gateway in front of public demos.
9. Isolate training and serving infrastructure.
10. Never expose internal vLLM/SGLang worker ports directly to the public
    internet.

## 17. Timeline

48-hour vertical slice:

1. Hours 0 to 2: fill decisions, provider access, budget, success gates.
2. Hours 2 to 8: repo skeleton, configs, validation, reports, adapters.
3. Hours 8 to 16: tiny from-scratch smoke run.
4. Hours 16 to 28: Tinker or TRL post-training track.
5. Hours 28 to 36: distillation engine.
6. Hours 36 to 44: Baseten/local serving.
7. Hours 44 to 48: public proof package.

Six-month path:

1. Weeks 1 to 2: foundation and tiny model.
2. Weeks 3 to 4: data pipeline, tokenizer, 124M smoke.
3. Weeks 5 to 6: mini ablations and scheduler prototype.
4. Weeks 7 to 10: 1.3B base.
5. Weeks 11 to 14: post-training.
6. Weeks 15 to 18: distillation and self-improvement.
7. Weeks 19 to 24: 3B flagship.
8. Stretch: 7B only after 3B reports are public.

## 18. Public Proof Standard

Publish:

1. Base, midtrained, SFT, preference/RL, distilled, and quantized weights when
   rights allow.
2. Training code, pinned commits, Dockerfiles, and launch scripts.
3. Data recipes, filters, dedup logic, sampling weights, and token counts.
4. Tokenizer and tokenizer card.
5. Training logs and loss curves.
6. Cost ledger.
7. Evaluation report.
8. Ablation report.
9. Serving endpoint and latency/throughput report.
10. One-command reproducibility kit for the smoke run.

