# Implementation Backlog

This backlog turns the full plan into ordered work. It is intentionally not an
MVP list; it is the production roadmap staged so each layer can be proven before
the next layer spends money.

## Foundation

Status: in progress.

- [x] Create repo skeleton.
- [x] Add master step-by-step plan.
- [x] Add human decision gates.
- [x] Add spec coverage audit.
- [x] Add local config validation.
- [x] Add cost-estimation primitive.
- [x] Add provider routing primitive.
- [ ] Fill `DECISIONS.md`.
- [ ] Add real dependency groups after choosing package manager constraints.
- [ ] Add CI workflow for validation.

## Tiny From-Scratch Trainer

Status: planned.

- [ ] Tokenizer loading.
- [ ] Packed dataset loader.
- [ ] Transformer block.
- [ ] RoPE.
- [ ] RMSNorm.
- [ ] SwiGLU MLP.
- [ ] Causal attention.
- [ ] AdamW.
- [ ] LR schedule.
- [ ] Checkpoint save/load.
- [ ] Eval loss.
- [ ] Generation.
- [ ] Chat wrapper.
- [ ] Export path.
- [ ] Blog/report draft.

## Data Pipeline

Status: planned.

- [ ] Manifest schema.
- [ ] Source ingestion.
- [ ] Unicode normalization.
- [ ] Boilerplate stripping.
- [ ] Language detection.
- [ ] Length filters.
- [ ] Paragraph dedup.
- [ ] Exact dedup.
- [ ] Fuzzy dedup.
- [ ] Quality scoring.
- [ ] Toxicity/safety/PII tagging.
- [ ] Domain classification.
- [ ] License/source tracking.
- [ ] Tokenization.
- [ ] Packing.
- [ ] Deterministic sharding.

## Tokenizer

Status: planned.

- [ ] Tokenizer training config.
- [ ] Domain sampling strategy.
- [ ] Special token policy.
- [ ] Compression evaluation.
- [ ] Tokenizer card.
- [ ] Hash-pinned artifact.

## Pretraining

Status: planned.

- [ ] OLMo-core or TorchTitan runner.
- [ ] `lab-124m` smoke config.
- [ ] Checkpoint resume test.
- [ ] Generation smoke test.
- [ ] Eval wrapper.
- [ ] 124M data ablations.
- [ ] 350M data ablations.
- [ ] 1.3B run plan.
- [ ] 3B run plan.

## Post-Training

Status: planned.

- [ ] TRL local SFT runner.
- [ ] Fixed chat template.
- [ ] Loss masking.
- [ ] DPO runner.
- [ ] GRPO/verifiable reward runner.
- [ ] Tinker adapter.
- [ ] Safety dataset hooks.
- [ ] Post-training eval gates.

## Distillation

Status: in progress.

- [x] Define distillation phase in docs.
- [ ] Teacher registry schema.
- [ ] Task generator.
- [ ] Teacher response collector.
- [ ] Objective verifiers.
- [ ] Preference pair builder.
- [ ] Curriculum sampler.
- [ ] Lineage database.
- [ ] Distillation ablation runner.

## Self-Improvement

Status: planned.

- [ ] Student-generated task queue.
- [ ] Verifier filtering.
- [ ] Candidate training loop.
- [ ] Frozen holdout eval.
- [ ] Promotion gate.
- [ ] Rollback policy.

## Scheduler

Status: in progress.

- [x] Provider routing primitive.
- [ ] Job schema.
- [ ] FIFO policy.
- [ ] Cheapest-first policy.
- [ ] Fastest-first policy.
- [ ] Value-per-dollar policy.
- [ ] Bayesian policy.
- [ ] Preemption-aware policy.
- [ ] Portfolio optimizer.
- [ ] Scheduler report.

## Evaluation

Status: planned.

- [ ] Base model eval config.
- [ ] Chat eval config.
- [ ] Safety eval config.
- [ ] Custom verifier evals.
- [ ] Serving latency benchmark.
- [ ] Regression suite.
- [ ] Eval report generator.

## Serving

Status: planned.

- [ ] Local vLLM wrapper.
- [ ] Baseten deployment folder.
- [ ] OpenAI-compatible chat endpoint.
- [ ] Safety gateway.
- [ ] Latency logging.
- [ ] Cost logging.
- [ ] Base vs post-trained vs distilled comparison mode.

## Public Release

Status: planned.

- [ ] Run card.
- [ ] Model card.
- [ ] Data card.
- [ ] Eval report.
- [ ] Serving benchmark.
- [ ] Cost ledger.
- [ ] Failure and bug log.
- [ ] Reproducibility kit.

