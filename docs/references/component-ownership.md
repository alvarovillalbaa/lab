# Component ownership

Last updated: 2026-11-10

Five component libraries are implemented; twelve are planned specifications.
The existing Open Evals platform and umbrella Lab complete the nineteen-repository
ecosystem. Product ownership below is distinct from implementation status.

| Owner | Canonical responsibility | Outside its responsibility |
| --- | --- | --- |
| [experiment-kit](https://github.com/alvarovillalbaa/experiment-kit) | Common research-record validation and the separate legacy LLM profile | Data preparation, compute policy, execution and scoring |
| [verification-runtime](https://github.com/alvarovillalbaa/verification-runtime) | Objective verification execution, generic result identities and diagnostics; exact-match v1 implemented | Teacher rights, preference selection, reward mapping, evaluator catalogue/scoring/gates |
| [research-artifacts](https://github.com/alvarovillalbaa/research-artifacts) | Planned generic artifact resolve/transfer/cache/integrity and byte provenance using existing backends | Dataset semantics, model compatibility, optimizer resume, promotion policy and a new object store |
| [compute-economics](https://github.com/alvarovillalbaa/compute-economics) | Workload compute/cost estimates, explicit assumptions, hour units and cost-ledger conventions | Live price discovery, billing measurement, job order, allocation and budget enforcement |
| [compute-planner](https://github.com/alvarovillalbaa/compute-planner) | Ordered provider recommendations, FIFO, cheapest-first and value/risk-aware job order | Workload cost formulas, mandatory estimator dependencies and execution |
| [compute-runners](https://github.com/alvarovillalbaa/compute-runners) | Explicit job submission/status/cancellation/logs and observed execution receipts | Model algorithms, scheduling objectives, evaluation scoring and endpoint serving policy |
| [model-data](https://github.com/alvarovillalbaa/model-data) | Dataset/document/shard schemas, ingestion, curation, splits, mixing, encoding/packing, lineage and data cards | Tokenizer fitting/policy and semantic ownership of teacher/task/verifier/preference records |
| [model-tokenizers](https://github.com/alvarovillalbaa/model-tokenizers) | Tokenizer training, vocabulary/special-token/normalization policy, inspection, comparisons and artifact/cards | Corpus curation, split construction and dataset packing |
| [model-architectures](https://github.com/alvarovillalbaa/model-architectures) | Planned model definitions/configuration, initialization, forward/generation/cache and weight-format compatibility | Optimization/data iteration, trainer state, endpoint lifecycle |
| [model-pretraining](https://github.com/alvarovillalbaa/model-pretraining) | Architecture selection, from-scratch/continued pretraining, resume and portable base export | SFT/preference/reward adaptation, serving and benchmark methodology |
| [model-posttraining](https://github.com/alvarovillalbaa/model-posttraining) | Existing-model SFT, preference and reward-based adaptation, resume and adapted-model/adapter export | Base pretraining, synthetic data generation, environment dynamics and generic scoring |
| [model-distillation](https://github.com/alvarovillalbaa/model-distillation) | Teacher/task/response contracts, eligibility, external verification-result binding, preference-data construction and related lineage | Objective verifier execution, student optimization, endpoint serving and general scoring |
| [model-serving](https://github.com/alvarovillalbaa/model-serving) | Model loading/format compatibility, runtime adapters, endpoint launch/status/request/stop and raw telemetry | Workload protocols, performance aggregation, training and release promotion |
| [inference-benchmarks](https://github.com/alvarovillalbaa/inference-benchmarks) | Independent workloads, bounded dispatch, latency/throughput/concurrency/memory/cost measurement and comparisons | Endpoint lifecycle, training and general quality/safety scoring |
| [research-controller](https://github.com/alvarovillalbaa/research-controller) | Bounded model-research sequencing, candidate/attempt state, limits and promotion policy | Trainer algorithms, evaluation scoring, prompt optimization and production publication |
| [ml-foundations](https://github.com/alvarovillalbaa/ml-foundations) | Educational ML implementations, numerical explanation and controlled reference comparisons | A general trainer, evaluation service or unimplemented algorithm claim |
| [rl-environments](https://github.com/alvarovillalbaa/rl-environments) | Environment dynamics, observations, actions, rewards, termination and task protocols | Model-training algorithms and generic evaluation-platform behavior |
| [open-evals](https://github.com/alvarovillalbaa/open-evals) | Evaluation definitions/results/gates, system-prompt improvement and SDK evidence transport | GPU execution and model-weight training orchestration; a trace write does not run evaluation |
| Lab | Integrated experiments, study-specific configurations, declared compatible combinations and reports | Reusable component engines and their release ownership |

## Important seams

Economics returns an estimate with explicit assumptions. Planning consumes
ordinary expected-cost values and can operate without that estimator. Runners
execute an explicit selection; a planning recommendation is not spend approval.

Data preparation may consume an external tokenizer. Tokenizer policy does not
move into a dataset pipeline. Model-distillation owns teacher/task/response/
verifier/preference record semantics; model-data preserves such producer records
without taking semantic ownership.

Post-training accepts external base models and does not require pretraining.
Inference benchmarks accept external targets and do not require model-serving.
Research-controller consumes evaluator outcomes; Open Evals remains the scoring
and prompt-improvement owner. Controller model promotion is not endpoint rollout.

[Interfaces and API changes](interfaces.md) describe these handoffs. The
[composition manifest](../../src/lab/composition.json) owns exact selected
revisions and review state. Candidate status persists while existing-repository
changes await review, independently of which local checks have passed.
