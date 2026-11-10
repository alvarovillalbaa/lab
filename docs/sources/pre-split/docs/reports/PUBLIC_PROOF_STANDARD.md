# Public Proof Standard

A public release is not complete because a model exists. A release is complete
when the process is inspectable.

## Required Artifacts

1. Weights or adapters when rights allow.
2. Training code and exact launch scripts.
3. Pinned dependency and container versions.
4. Dataset recipes and source manifests.
5. Tokenizer artifact and tokenizer card.
6. Run card.
7. Model card.
8. Data card.
9. Evaluation report.
10. Cost ledger.
11. Training logs and loss curves.
12. Serving benchmark.
13. Failure and bug log.
14. Reproducibility instructions.

## Minimum Smoke Proof

The smallest acceptable proof must show:

- Loss decreases.
- Checkpoint resume works.
- Generation works.
- Eval command runs.
- Cost ledger is filled.
- Run card links the code, config, data, and model artifact.

## Improvement Claim Rule

No improvement claim is valid unless it compares:

- Baseline.
- One change.
- Same data budget.
- Same training budget.
- Same eval suite.
- Same random seeds where practical.
- Confidence interval or bootstrap when practical.

