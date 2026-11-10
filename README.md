# Lab

Last updated: 2026-11-10

An AI research laboratory that assembles independently usable tools into
reproducible experiments. Lab owns integrated configurations, research questions,
compatible combinations and cross-component reports. Reusable product behavior
lives in its component repository.

## Ecosystem

The expanded catalogue contains **17 component repositories**, plus the existing
open-evals platform and umbrella Lab: **19 repositories**. Five component
libraries are implemented; twelve homes currently contain specifications. The
Open Evals SDK is a separate client package inside the existing open-evals repo,
a client distribution in that repository.

| Component repository | Responsibility | Current scope |
| --- | --- | --- |
| [experiment-kit](https://github.com/alvarovillalbaa/experiment-kit) | Common experiment records and a separate LLM validation profile | Implemented library and CLI |
| [verification-runtime](https://github.com/alvarovillalbaa/verification-runtime) | Objective verification with candidate/reference identities | Implemented exact-match library and CLI; other adapters planned |
| [research-artifacts](https://github.com/alvarovillalbaa/research-artifacts) | Artifact resolution, transfer, cache and byte integrity using existing backends | Planned specification |
| [compute-economics](https://github.com/alvarovillalbaa/compute-economics) | Caller-assumption compute/cost estimates and cost-ledger conventions | Implemented library and CLI |
| [compute-planner](https://github.com/alvarovillalbaa/compute-planner) | Provider recommendations and job ordering from explicit values | Implemented library and CLI |
| [compute-runners](https://github.com/alvarovillalbaa/compute-runners) | Explicit job execution, lifecycle, cancellation and receipts | Planned specification |
| [model-data](https://github.com/alvarovillalbaa/model-data) | Dataset curation, splits, manifests, encoding and packing | Planned specification |
| [model-tokenizers](https://github.com/alvarovillalbaa/model-tokenizers) | Tokenizer training, inspection, comparisons and artifact policy | Planned specification |
| [model-architectures](https://github.com/alvarovillalbaa/model-architectures) | Model definitions, forward/generation/cache and weight compatibility | Planned specification |
| [model-pretraining](https://github.com/alvarovillalbaa/model-pretraining) | Base/continued pretraining, checkpoint resume and portable export | Planned specification |
| [model-posttraining](https://github.com/alvarovillalbaa/model-posttraining) | SFT, preference and reward-based adaptation of an existing model | Planned specification |
| [model-distillation](https://github.com/alvarovillalbaa/model-distillation) | Teacher eligibility, verification-result binding and preference-data construction | Implemented library and CLI |
| [model-serving](https://github.com/alvarovillalbaa/model-serving) | Model loading and endpoint launch/status/request/stop | Planned specification |
| [inference-benchmarks](https://github.com/alvarovillalbaa/inference-benchmarks) | Endpoint-independent workloads and performance measurement | Planned specification |
| [research-controller](https://github.com/alvarovillalbaa/research-controller) | Bounded model-research sequencing, candidate state and promotion policy | Planned specification |
| [ml-foundations](https://github.com/alvarovillalbaa/ml-foundations) | ML implementations from scratch and reference comparisons | Planned specification |
| [rl-environments](https://github.com/alvarovillalbaa/rl-environments) | Reusable dynamics, tasks, observations, actions and rewards | Planned specification |

[open-evals](https://github.com/alvarovillalbaa/open-evals) remains the evaluation and system-prompt improvement
platform. Its Python SDK supplies the optional application-evidence connection.

The former model-training repository is now model-pretraining, and the former
model-inference repository is now model-serving. Their repository identities and
Git histories are preserved. Post-training and inference measurement have their
own product homes.

## Install a chosen combination

Lab 0.4 keeps the base installation small and exposes independent optional
profiles:

| Installation selector | Adds to experiment-kit in the base install |
| --- | --- |
| `.` | Experiment validation only |
| `.[economics]` | compute-economics |
| `.[planning]` | compute-planner |
| `.[compute]` | compute-economics and compute-planner |
| `.[verification]` | verification-runtime |
| `.[distillation]` | model-distillation and its verification-runtime dependency |
| `.[evals]` | Open Evals Python SDK |

Selectors compose. For the CPU fixture workflow, use compute plus distillation:

```sh
python3 -m pip install '.[compute,distillation]'
llm-lab validate configs/experiments/lab_20m_tiny_pretrain.json
llm-lab validate configs/experiments/cpu_smoke.json --profile record
llm-lab estimate-cost configs/experiments/lab_124m_pretrain_smoke.json
llm-lab route pretrain_smoke
llm-lab verify configs/experiments/verification.json
llm-lab smoke --code-ref "lab@$(git rev-parse HEAD)"
```

The program executes on CPU using authored teacher-response fixtures. It
calculates a **hypothetical token-based GPU training estimate** from authored
parameter, token, hardware and price assumptions, then passes that estimate to
a planning job. The result labels the estimate as authored assumptions and
`observed_billing: false`. No GPU training or billed provider execution occurs.

`estimate-cost` delegates to compute-economics; `route` delegates to
compute-planner. The planner has no mandatory economics dependency. Optional
SDK evidence delivery uses the `evals` profile and the
[Open Evals integration guide](docs/references/open-evals-integration.md).

## Versions, review and proof

The [composition manifest](src/lab/composition.json) records exact source
revisions, declared combinations and review state. Existing-repository changes
remain in review PRs; newly established repositories use their own main branches.
A repository rename preserves history but does not merge its scope changes.
Use the manifest's selected revision rather than assuming the latest main
contains an unmerged interface. No public package-registry release is implied.

Current product-split verification belongs in the
[expanded installed-package result](docs/results/2026/11-10/product-installed-package.md)
and its [machine-readable receipt](docs/results/2026/11-10/product-installed-package.json).
Read those outcomes and limits for the exact revisions checked. The
[first-stage result](docs/results/2026/11-10/installed-package.md) remains
historical evidence for the earlier packages and combinations.

## Work across repositories

[Architecture](docs/ARCHITECTURE.md) ·
[Canonical ownership](docs/references/component-ownership.md) ·
[Interfaces and handoffs](docs/references/interfaces.md) ·
[Integration backlog](docs/IMPLEMENTATION_BACKLOG.md) ·
[Recovery procedure](docs/runbooks/recovered-laptop.md) ·
[Original inventory](docs/sources/repository-split-map.json) ·
[Current recovery map](docs/sources/repository-split-v3-map.json) ·
[Rename/expansion aliases](docs/sources/expanded-repository-aliases.json)

Components declare their own dependencies and run without Lab or sibling-path
imports. Lab connects pinned packages and explicit artifacts; it does not share
one mutable environment across every product.

Existing [nanochat](https://github.com/alvarovillalbaa/nanochat) and [autoresearch](https://github.com/alvarovillalbaa/autoresearch) retain their fork
identities and can be selected as optional implementations.
[my-evals](https://github.com/alvarovillalbaa/my-evals) owns portable personal task suites. The separate
evaluation-lab research project retains its own contracts and licensing.

The damaged laptop is outside this source baseline.
[Human gates](docs/HUMAN_GATES.md) and
[experiment decisions](docs/decisions/experiment-decisions.md) retain ownership
of budget, data/teacher rights, provider access and scientific release claims.

MIT covers authored Lab code/documentation; third-party inputs retain their
terms. Large datasets and model artifacts stay outside Git with exact references
and content hashes.
