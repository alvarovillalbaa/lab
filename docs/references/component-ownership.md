# Component ownership

Last updated: 2026-11-10

| Owner | Canonical responsibility | Boundary |
| --- | --- | --- |
| [experiment-kit](https://github.com/alvarovillalbaa/experiment-kit) | Common experiment metadata and the separate legacy LLM spec profile. | Dataset processing, model execution, scheduling, or scoring. |
| [compute-planner](https://github.com/alvarovillalbaa/compute-planner) | The 6NT language-model estimate, ordered provider recommendations, FIFO, cheapest-first, and risk-adjusted value ordering. | Cloud allocation, provider credentials, live pricing, training, or budget enforcement. |
| [compute-runners](https://github.com/alvarovillalbaa/compute-runners) | Local/cluster/provider execution adapters, lifecycle status, cancellation, logs, and execution receipts. | Provider ranking, research priorities, model algorithms, endpoint serving policy, or evaluation engines. |
| [model-data](https://github.com/alvarovillalbaa/model-data) | Ingestion, normalization, filters, deduplication, tokenization, packing, sharding, provenance, and data cards. | Model training, generic artifact storage services, scheduling, or evaluation scoring. |
| [model-training](https://github.com/alvarovillalbaa/model-training) | Model implementations, pretraining, SFT/DPO/RL post-training, checkpoint resume, generation smoke checks, and export. | Standalone RL environment definitions, GPU scheduling, dataset preparation, or generic eval scoring. |
| [model-distillation](https://github.com/alvarovillalbaa/model-distillation) | Task/response records, exact-match verification, eligibility gates, and preference-pair construction. | Teacher inference, a training engine, a general evaluation platform, or legal license approval. |
| [model-inference](https://github.com/alvarovillalbaa/model-inference) | Inference adapters, model endpoint bindings, request workloads, latency/throughput measurements, and export compatibility. | Training, generic GPU scheduling, a custom evaluation engine, or production deployment authorization. |
| [ml-foundations](https://github.com/alvarovillalbaa/ml-foundations) | Educational implementations, numerical explanations, correctness comparisons, frozen splits, and bounded experiments. | A claim that any algorithm is implemented yet, an evaluation service, or a generic training framework. |
| [rl-environments](https://github.com/alvarovillalbaa/rl-environments) | Environment dynamics, observations, actions, rewards, termination rules, fixtures, and task-specific validation. | LLM RL post-training algorithms, a general trainer, or the Open Evals scoring platform. |
| [open-evals](https://github.com/alvarovillalbaa/open-evals) | Evaluation definitions, execution, gates, prompt improvement, SDK evidence transport | A trace write does not execute evaluation. |
| Lab | Integrated experiments, declared compatible combinations, research notes, cross-component reports | Reusable component engines live in their owner repos. |

## Planning-to-execution handoff

A future runner accepts an explicit workload/command, working directory,
resources, input artifact references, and output destinations. It returns an
execution identity and observed lifecycle/results. Planning recommendations do
not establish access, allocation, or spend. This handoff is planned; no runner
implementation or stable wire schema is claimed.

## Artifact handoff

Model-data will produce hash-pinned datasets/tokenizers. Model-training will
consume explicit inputs and export checkpoints/models. Model-inference will
consume those models. RL environments define dynamics/tasks independently of
the trainer. Model-distillation produces permitted verified data, not a trainer.
Prefer artifact references and optional adapters over mandatory dependencies
among every component.

[Declared revisions and combinations](../../src/lab/composition.json) are
candidate integration metadata until their acceptance checks pass.
