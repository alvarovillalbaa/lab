# Reassessment of Lab repository boundaries

Last updated: 2026-11-10

The owner asked whether the original Lab should become substantially more
repositories. This review challenges the current nine-component extraction
against the intended independently usable and composable product ecosystem.
It includes three independent read-only reviews of compute/data, model
workflows, and the overall ownership map.

## Conclusion

The current nine are a first partition, not a demonstrated optimal final count.
Packaging and installation checks establish that the extracted implementations
work independently and in selected combinations. They do not establish that
all planned product boundaries are sufficiently narrow.

Four additional boundaries are strongly supported by distinct independent
consumers already implied by the original blueprint:

| Current home | Revised product boundary | Independent use |
| --- | --- | --- |
| model-data | Dataset curation plus a separate model-tokenizers project | Train, inspect, compare, and distribute a tokenizer without adopting the corpus pipeline |
| model-training | model-pretraining and model-posttraining | Adapt an external checkpoint without adopting the base-model trainer |
| model-inference | model-serving and inference-benchmarks | Measure an external endpoint without operating its serving infrastructure |
| Lab's integrated workflow/research plans | Add research-controller | Coordinate bounded candidate generation, training, frozen evaluation, promotion, and rollback using interchangeable tools |

These changes would turn nine new component repositories into thirteen,
with umbrella Lab and existing open-evals bringing that illustrative ecosystem
to fifteen repositories. This is an outcome of the proposed boundaries, not
a target quota.

## Compute and other additional products

A separate compute-economics repository is defensible for the owner's GPU
orchestration vision: workload/resource assumptions produce estimates or quotes;
the planner consumes jobs and costs to choose ordering/placement; runners execute
explicitly selected work. Someone can consume the economics layer independently
or substitute their own prices and estimates.

The current costing, routing, and scheduling modules do not import each other.
Current costing is specifically a 6NT language-model GPU estimate with
caller-supplied prices. It is not a live pricing service or budget enforcement.
Current routing is static policy data and a lookup. A separate router product
would need its own capability-matching/placement interface and independent user;
extracting that lookup alone would add little standalone utility.

Other deliberate product candidates include a model-architecture library,
artifact resolution/verification/lineage tooling, and substantial execution
backend adapters. Define their independent consumers and public contracts before
assigning another canonical owner. A generic shared DTO package or one repo for
every algorithm/filter/provider is not automatically a useful product.

Provider integrations can be optional independently distributed plugins.
Python's [entry-point standard](https://packaging.python.org/en/latest/specifications/entry-points/)
supports discovering components supplied by separate distributions. Repository
placement remains a product/ownership decision.

## Concrete ownership issues

- The original bounded model self-improvement loop lacks an explicit reusable
  controller owner in the current active map. Lab can assemble demonstrations;
  open-evals owns scoring and prompt improvement. A model research controller
  would consume those results and own cross-component execution/promotion policy.
- model-data/data/schemas/README.md claims teacher/task/verifier/preference
  schemas, while their implemented dataclasses are canonical in model-distillation.
  This is a documentation ownership overlap, not evidence of duplicate engines.

## Decision rule and limits

Choose a repository around a coherent intended product with its own meaningful
inputs/outputs, installation/example, public interface, and release ownership.
Different consumers, dependency stacks, and release cadence support a split.
There is no requirement that a product already have customers or recovered code
before its intended boundary can be established.

Available source and planned requirements support the recommendations above.
The damaged laptop implementation is unavailable and may refine actual
dependencies and file allocation. No new engines, provider behavior, or recovered
work is inferred from this checkout. No repositories were created or reorganized
by this review.

Sources: [current ownership](../../../references/component-ownership.md),
[original design](../../../sources/pre-split/docs/specs/steps.md), especially
data/tokenizer phases 7/8, training phases 10–12, bounded self-improvement phase
14, GPU allocation phase 15, and serving phase 17.
