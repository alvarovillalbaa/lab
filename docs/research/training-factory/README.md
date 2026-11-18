# Training factory research

Last updated: 2026-10-10

Status: proposed research structure derived from the existing lab blueprint.
No experiment or hypothesis has been accepted or executed by this migration.

## Ordered questions

1. Which local smoke path produces reproducible checkpoints and generation?
2. Which data sources and teacher licenses allow the intended experiment?
3. Which provider and serving choices satisfy the approved budget and success gates?
4. What role, if any, should the user-named PorTAL library play?

## Hypotheses and reasoning

- A tiny local run can establish reproducibility before a paid provider run.
  The existing [architecture](../../ARCHITECTURE.md) makes that local lane mandatory.
- Explicit lineage and licensing gates can prevent ambiguous training inputs.
  The [decision record](../../decisions/experiment-decisions.md) leaves these choices open.
- Provider suitability depends on the measured workload and approved cost cap.
  Repository adapter choices are proposed paths, not benchmark results.

## Method and evidence

Resolve the human gates first, then follow the existing experiment configs and
validation owners. Record measurements, versions, costs, limitations and source
hashes in dated results, and link them here when available. Existing context:
[blueprint](../../../README.md), [human gates](../../HUMAN_GATES.md),
[libraries and providers](../../LIBRARIES_AND_PROVIDERS.md).

## Next action

Have the owner fill the decision record's budget, data, license and success
criteria. Research planning does not authorize paid runs or public claims.
