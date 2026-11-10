# CLOUS LLM Lab

This repo is a reproducible LLM training lab blueprint. The goal is not to claim
frontier-scale training on day one. The goal is to build and publish a complete
training factory:

```text
data -> tokenizer -> pretraining -> post-training -> distillation -> evals -> serving -> cost ledger -> public report
```

The default proof path is local and from-scratch first. External services are
adapters:

- Baseten, called "Base10" in the notes, for public serving and managed training
  only after local proof paths exist.
- Thinking Machines Lab Tinker for post-training, RL, DPO, and distillation
  loops when access is available.
- Raw GPU providers through provider adapters for serious pretraining.
- PorTAL is tracked as a user-named library/research item until its exact role is
  pinned down.

## Current Status

This repo currently provides the planning and execution skeleton:

- Master step-by-step plan: [docs/STEP_BY_STEP.md](docs/STEP_BY_STEP.md)
- Human decisions and gates: [docs/HUMAN_GATES.md](docs/HUMAN_GATES.md)
- Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Libraries and providers: [docs/LIBRARIES_AND_PROVIDERS.md](docs/LIBRARIES_AND_PROVIDERS.md)
- Implementation backlog: [docs/IMPLEMENTATION_BACKLOG.md](docs/IMPLEMENTATION_BACKLOG.md)
- Spec coverage audit: [docs/SPEC_COVERAGE.md](docs/SPEC_COVERAGE.md)
- Decision template: [docs/decisions/experiment-decisions.md](docs/decisions/experiment-decisions.md)
- Experiment configs: [configs/experiments](configs/experiments)
- Provider configs: [configs/providers](configs/providers)
- Public proof templates: [reports/templates](reports/templates)
- Local validation CLI: [src/lab](src/lab)

## Local Validation

No GPU or external service is required for the current validation path.

```bash
PYTHONPATH=src python3 -m lab.cli validate configs/experiments/lab_20m_tiny_pretrain.json
PYTHONPATH=src python3 -m lab.cli estimate-cost configs/experiments/lab_124m_pretrain_smoke.json
PYTHONPATH=src python3 -m unittest discover -s tests
```

Or run the bundled check:

```bash
sh scripts/validate-lab.sh
```

## First Execution Milestones

1. Fill [docs/decisions/experiment-decisions.md](docs/decisions/experiment-decisions.md) with budget, data, model, provider, license,
   and success-gate choices.
2. Run the local validation checks above.
3. Implement the tiny 20M to 60M from-scratch transformer and train on a tiny
   corpus.
4. Add tokenizer/data-pipeline code and produce deterministic manifests.
5. Run `lab-124m` smoke pretraining with checkpoint resume and generation.
6. Add post-training with TRL locally, then Tinker when access is available.
7. Add verifier-gated distillation data generation.
8. Serve a model locally with vLLM, then expose a Baseten endpoint.
9. Publish run cards, model cards, data cards, eval reports, logs, and cost
   ledger.
