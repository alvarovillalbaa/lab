# Further product boundaries after the sixteen-repository split

Last updated: 2026-11-10

Status: architectural recommendation, not an implemented third migration.
Reviewed Lab at `165e2467f544e0c7ddcb9b9fe87ea65f0c70a28f`, its preserved
original blueprint, current ownership/interfaces, component specifications and
distillation implementation. Three independent read-only reviews covered model,
compute/artifact and overall boundaries. No recovered-laptop code was available.

## Recommendation

Sixteen repositories are a useful checkpoint, not a demonstrated final count.
The installation results establish package independence and selected composition;
the product boundaries need separate review. Three further intended products are
well supported by the original design and the requested independent-use model.

| Proposed home | Independent contract | Current responsibility to separate |
| --- | --- | --- |
| verification-runtime | Pinned objective verifier, task/candidate artifacts and execution/resource policy produce identified verdicts, errors/timeouts, diagnostics and observation coverage | Objective verification currently grouped with distillation; future consumers include RL rewards, Open Evals and research-controller |
| model-architectures | Model configuration, initialization, forward/generation/cache behavior and portable weights compatibility work with an external trainer or inference consumer | Model implementation currently belongs to model-pretraining |
| research-artifacts | Resolve, transfer, cache and verify research artifact bytes; emit immutable references and generic provenance | Transfer/integrity behavior spans runners, dataset tooling, training and serving; experiment-kit validates references without verifying remote bytes |

These are proposed product homes, not claims of existing engines. Boundaries can
be established before recovery; recovered code determines the concrete file and
dependency migration. This recommendation does not set a fixed repository quota.

## Evidence and ownership constraints

- Original [verifiers](../../../sources/pre-split/docs/specs/steps.md) at lines
  674–685 include code sandbox tests, math, schema, environment success and
  source-span checks. Lines 550–561 reuse objective verification for rewards.
  Current [verification code](https://github.com/alvarovillalbaa/model-distillation/blob/89ae0b3b642566e385be1a292843419bb9ffbdd3/src/model_distillation/distillation.py)
  mixes exact matching with teacher eligibility and binds results to teachers.
  A general verifier runtime should separate execution/correctness evidence from
  distillation eligibility and pair policy. Open Evals retains evaluator
  definitions, composition, scoring, runs and gates. Existing string checks
  alone would justify a small package within Open Evals; the broader intended
  execution toolkit is the reason for a separate product recommendation.
- Original architecture requirements at lines 175–188 and 368–408 separate model
  math/families from optimization. Current model-pretraining README still owns
  the first model implementation. A model library can serve arbitrary trainers
  and inference consumers. Keep attention, normalization and model-family
  internals together; no repository per block or parameter count is proposed.
- Original [canonical storage rule](../../../sources/pre-split/docs/ARCHITECTURE.md)
  at lines 73–80 requires hashes across datasets, tokenizers, checkpoints and
  evaluations. Its provider interface also mixes artifact transfers with job
  operations. [experiment-kit](https://github.com/alvarovillalbaa/experiment-kit) explicitly
  does not verify remote bytes. The proposed artifact product uses existing
  storage backends; it does not invent an object store, registry service or
  mandatory universal domain schema. Dataset semantics remain with model-data,
  optimizer/resume compatibility with trainers, and promotion policy with the
  controller.

## Additional candidates and existing owners

- A model/teacher gateway is defensible if owned cross-provider generation,
  batching, streaming, cancellation, usage and capability policy form a product.
  First check/reuse existing clients and adapters. An HTTP wrapper alone does
  not establish that need. Separate this client role from server lifecycle.
- A serving safety gateway can independently protect an external endpoint;
  original blueprint lines 575 and 1006 require such a layer. Establishing its
  product scope is a further decision; no implementation was found here.
- A custom compute control plane or observability product needs an explicit
  intended service beyond adapters to the existing Slurm/Kueue/SkyPilot and
  tracking/exporter tools selected in the original follow-up design.
- Backend adapters can be separate optional distributions and later separate
  repositories when dependency/release ownership warrants it. Provider names
  alone are insufficient boundaries.
- Synthetic-data curation, response eligibility, preference construction and
  curriculum already form the intended model-distillation data engine. A second
  synthetic-data repository would overlap that scope unless ownership changes.
- Original distillation methods at lines 730–742 include logit, router and draft
  model training. Their optimization owner needs explicit clarification in
  model-posttraining; the current data primitives do not implement them. A new
  student-distillation repository is an option only for a deliberately separate
  training product.

Open Evals' local README was inspected for evaluator ownership. Targeted live
GitHub name/description searches for gateway, verifier, artifacts and architecture
repositories found no dedicated replacement for the three proposed products;
this is not an exhaustive code inventory. Matched repository names alone were
not treated as proof of their capabilities. Existing projects and their terms
must be checked before any new implementation is assigned or copied.

This review changed only this local evidence document. No repository creation,
code relocation, dependency installation, build, commit or remote publication
was performed for this reassessment.
