# Human Gates

The specs make clear that Codex can build implementation scaffolding, but the
research, infrastructure, legal, and product choices must be explicit human
decisions.

## Gate 0: Claim

Decide:

- What public claim will be made.
- Whether the first public artifact is a 48-hour vertical slice, a tiny
  from-scratch model, a post-trained model, or a 1B+ release.
- Which claims are explicitly out of scope.

Required artifact:

- `docs/decisions/experiment-decisions.md` public claim section filled.

## Gate 1: Budget

Decide:

- Hard cap.
- Soft cap.
- Per-job stop threshold.
- Maximum spend before first checkpoint.
- Maximum spend before first public report.

Required artifact:

- `docs/decisions/experiment-decisions.md` budget section filled.
- `reports/templates/cost_ledger.csv` copied to a real run ledger.

## Gate 2: Data And Licensing

Decide:

- Allowed pretraining datasets.
- Allowed SFT datasets.
- Allowed teacher models.
- Which commercial APIs are disallowed until review.
- Whether artifacts can be published commercially or only for research.

Required artifact:

- Data card.
- Dataset manifests.
- Teacher registry.

## Gate 3: Provider Access

Decide:

- Local hardware profile.
- Raw GPU provider.
- Tinker access status.
- Baseten access status.
- Backup provider for every paid job.

Required artifact:

- Provider config.
- Provider routing entry.
- Secrets stored outside repo.

## Gate 4: Evals

Decide:

- Frozen smoke gates.
- Capability benchmark set.
- Safety benchmark set.
- Hidden/private eval policy.
- Promotion thresholds for candidate models.

Required artifact:

- Eval config.
- Eval report template filled for each run.

## Gate 5: Release

Decide:

- Which weights can be published.
- Which logs can be published.
- Which synthetic data can be published.
- Which endpoint is public.
- What limitations and failures must be documented.

Required artifact:

- Model card.
- Data card.
- Eval report.
- Cost ledger.
- Serving benchmark.

