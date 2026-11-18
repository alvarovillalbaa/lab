# Experiment Decisions

This file must be filled before spending GPU money or publishing claims. The
system is designed so implementation can move forward locally while these
decisions remain explicit.

## Public Claim

Default claim:

> We built an end-to-end LLM training lab: local from-scratch pretraining smoke
> run, post-training path, verifier-gated distillation engine, evals, serving,
> cost ledger, and reproducibility kit.

Final public claim:

```text
TODO
```

## Budget

Hard cap USD:

```text
TODO
```

Soft cap USD:

```text
TODO
```

Stop rules:

- Stop if a job exceeds the hard cap without producing a valid checkpoint.
- Stop if checkpoint resume fails.
- Stop if eval contamination is found.
- Stop if license or data-rights status is unclear.

## From-Scratch Model

Name:

```text
lab-20m, lab-60m, lab-124m, lab-350m, lab-1.3b, or TODO
```

Architecture:

```text
decoder-only, Llama-like, RMSNorm, RoPE, SwiGLU, causal attention
```

Framework:

```text
tiny local trainer first; OLMo-core or TorchTitan for scaled training
```

Tokenizer:

```text
TODO own tokenizer or existing tokenizer
```

Training tokens target:

```text
TODO
```

Sequence length:

```text
TODO
```

## Providers

Local provider:

```text
local first; local_slurm/local_k8s when hardware exists
```

Raw GPU provider:

```text
TODO RunPod, Lambda, CoreWeave, Baseten Training, or other
```

Post-training provider:

```text
Primary: Tinker if available
Backup: TRL locally or on raw GPU
```

Serving provider:

```text
Primary: Baseten
Backup: local/self-hosted vLLM
```

User-named library/research item:

```text
PorTAL - exact role pending clarification/research
```

## Teacher Models

Allowed teachers:

```text
TODO open-weight teachers with compatible licenses
```

Disallowed until review:

```text
commercial API outputs for model training, any unclear license, any private data
```

## Data Sources

Pretraining:

```text
TODO FineWeb sample, Dolma sample, local corpus, code data with permissive license
```

SFT:

```text
TODO permissive instruction data, human-authored examples, synthetic data with lineage
```

Distillation:

```text
TODO verifier-gated outputs from allowed teachers only
```

## Evals

Smoke evals:

- Training loss decreases.
- No NaNs.
- Checkpoint resume works.
- Generation works.
- Export path works.

Capability evals:

```text
TODO lm-eval tasks, custom heldout tasks, code/math/tool-use evals
```

Safety evals:

```text
TODO refusal, harmfulness, PII leakage, prompt injection, hallucination checks
```

## Release Artifacts

- Code.
- Configs.
- Logs.
- Cost ledger.
- Run cards.
- Model cards.
- Data cards.
- Eval report.
- Serving benchmark.
- Reproducibility script.

