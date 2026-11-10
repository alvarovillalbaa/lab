# Lab

Last updated: 2026-11-10

An AI research laboratory that assembles independent tools into reproducible
experiments. Reusable implementations live in their component repositories;
Lab owns integrated configurations, research questions, compatibility records,
and cross-component reports.

## Components

| Repository | Purpose | Current scope |
| --- | --- | --- |
| [experiment-kit](https://github.com/alvarovillalbaa/experiment-kit) | Validate reproducible research records independently of training frameworks. | Library and CLI |
| [compute-planner](https://github.com/alvarovillalbaa/compute-planner) | Estimate training compute, rank jobs, and choose candidate providers without executing them. | Library and CLI |
| [compute-runners](https://github.com/alvarovillalbaa/compute-runners) | Execute an explicit job on a chosen backend, independently of how it was scheduled. | Specifications; implementation planned |
| [model-data](https://github.com/alvarovillalbaa/model-data) | Prepare versioned datasets and tokenizer artifacts for independent model consumers. | Specifications; implementation planned |
| [model-training](https://github.com/alvarovillalbaa/model-training) | Train and adapt models from explicit data/model inputs, locally or through external execution backends. | Specifications; implementation planned |
| [model-distillation](https://github.com/alvarovillalbaa/model-distillation) | Construct verifier-gated preference data from explicitly permitted teacher responses. | Library and CLI |
| [model-inference](https://github.com/alvarovillalbaa/model-inference) | Serve explicit model artifacts and measure inference behavior through documented workloads. | Specifications; implementation planned |
| [ml-foundations](https://github.com/alvarovillalbaa/ml-foundations) | Implement ML algorithms from scratch and compare them with reference implementations under reproducible protocols. | Specifications; implementation planned |
| [rl-environments](https://github.com/alvarovillalbaa/rl-environments) | Provide reusable environments and task protocols for independent reinforcement-learning consumers. | Specifications; implementation planned |
| [open-evals](https://github.com/alvarovillalbaa/open-evals) | Evaluation and prompt improvement | Existing platform; standalone Python SDK packaging in [PR #1](https://github.com/alvarovillalbaa/open-evals/pull/1) |

## Install a chosen combination

Python 3.11+. The base install contains experiment validation; choose optional
profiles only when needed:

```sh
python3 -m pip install .
python3 -m pip install '.[compute,distillation]'
llm-lab validate configs/experiments/lab_20m_tiny_pretrain.json
llm-lab validate configs/experiments/cpu_smoke.json --profile record
llm-lab route pretrain_smoke
llm-lab smoke --code-ref "lab@$(git rev-parse HEAD)"
```

The CPU smoke composes validation, job ordering, provider recommendations, and
preference-pair construction using authored fixture responses. It performs no
training, teacher inference, GPU allocation, or service call.
`estimate-cost` retains the original command and delegates to compute-planner.

Dependencies are pinned to full Git commit SHAs. The
[composition manifest](src/lab/composition.json) records declared combinations
and their status; it is not an attestation of a running environment.
The manifest remains a candidate while integration PRs and fresh-install proof
are pending. No public package-registry availability is assumed.

For an optional Open Evals connection, install `.[evals]` and follow the
[SDK integration guide](docs/references/open-evals-integration.md). Evidence
delivery and evaluation execution are separate operations.

## Working across repositories

[Architecture](docs/ARCHITECTURE.md) ·
[Ownership and interfaces](docs/references/component-ownership.md) ·
[Integration backlog](docs/IMPLEMENTATION_BACKLOG.md) ·
[Recovery procedure](docs/runbooks/recovered-laptop.md) ·
[Migration map](docs/sources/repository-split-map.json)

Component source and tests must work without Lab. Each component has its own
environment and release cycle. Lab uses versioned dependencies and explicit
artifacts, without submodules or an environment shared by every project.

Existing [nanochat](https://github.com/alvarovillalbaa/nanochat) and
[autoresearch](https://github.com/alvarovillalbaa/autoresearch) retain their fork
identity and can be selected as optional training/research implementations.
[my-evals](https://github.com/alvarovillalbaa/my-evals) owns portable personal
task suites. The separate evaluation-lab research project keeps its own
contracts and licensing; its code is not redistributed here.

## Status and proof

The source checks, publication receipt, and remaining limits are recorded in
[the migration result](docs/results/2026/11-10/repository-split.md).
The recovered laptop is outside this baseline.
[Human gates](docs/HUMAN_GATES.md) and
[experiment decisions](docs/decisions/experiment-decisions.md) remain in force
for budget, data rights, providers, and claims.

MIT covers the authored Lab code and documentation; third-party assets and
dependencies retain their own terms. Large datasets and weights remain outside
Git, referenced by immutable revision and content hash.
