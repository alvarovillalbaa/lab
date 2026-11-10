# Component interfaces and handoffs

Last updated: 2026-11-10

This reference separates implemented package interfaces from planned behavioral
seams. It does not declare an implemented wire format for the twelve planned homes.
Exact code revisions and supported combinations are pinned in
[the composition manifest](../../src/lab/composition.json).

## Implemented packages

| Producer | Input | Output / consumer |
| --- | --- | --- |
| experiment-kit | Common research record or explicit legacy LLM spec | Validation issues; no execution or artifact download |
| compute-economics | Model/token workload plus explicit GPU/rate/utilization/overhead assumptions | Compute, elapsed/aggregate GPU-hours and estimated cost |
| compute-planner | Job values and job type | Job ordering and candidate provider recommendations |
| verification-runtime | Subject ID, candidate text and explicit reference | Generic verdict with raw candidate/reference hashes and versioned exact-match identity |
| model-distillation | Task, permitted teacher responses and bound verification results | Eligible verified/preference-data records |
| Open Evals SDK | Explicit service/key configuration and actual application evidence | Existing authenticated service transport; trace delivery does not execute evaluation |

### Costing API ownership in the expansion

Import `CostEstimate`, `estimate_from_spec` and `format_estimate` from
`compute_economics`. The old compute-planner costing module/exports and native
estimate-cost command are removed in planner 0.2; no forwarding copy remains.
Lab 0.4 retains `llm-lab estimate-cost` and delegates it to economics.

The estimator's `wall_clock_hours` is elapsed time and
`aggregate_gpu_hours` sums GPU use. The ambiguous `raw_gpu_hours` field was
replaced. Cost uses aggregate GPU-hours and the explicitly supplied hourly rate.
A missing rate is rejected; zero is an explicit caller assumption, not a default
or observed invoice. Current estimates model token-based language-model GPU
training and do not estimate CPU/MPS or serving workloads.

A caller can place the returned estimated cost into `Job.expected_cost_usd`.
The planner imports no economics implementation and may accept another
estimator's values. Neither component allocates resources or enforces billing.

## Verification ownership

Import VerificationResult and verify_exact_match from verification_runtime.
Model-distillation 0.2 removes those exports and declares the exact runtime dependency.
Its pair builder validates subject/candidate/reference binding and teacher eligibility.
The verifier has no teacher policy. The current exact-match adapter does not execute
code or implement math, schema, environment or citation checking; those are planned.
Open Evals keeps evaluator composition, scoring, runs and gates.

## Planned artifact and control seams

| Producer / owner | Handoff | Independent consumer |
| --- | --- | --- |
| research-artifacts | Materialized/verified bytes, immutable references and observed integrity receipts | Any compatible dataset, training, serving or external consumer |
| model-architectures | Model configuration, forward/generation/cache and compatible weights | An external trainer, inference runtime or probe without the pretraining toolkit |
| model-data | Dataset/corpus/split/shard references with hashes and lineage | Tokenizer tooling, trainers or another data consumer |
| model-tokenizers | Tokenizer artifact, format/backend identity, normalization and special-token policy | Any compatible data pipeline, trainer or inference consumer |
| model-pretraining | Portable base weights/config/tokenizer references; resumable state separately | Post-training, serving or external evaluation |
| model-posttraining | Adapted model or base-dependent adapter with parent/method/data identities | Serving or evaluation without adopting the base trainer |
| model-serving | Endpoint/protocol/capability binding, lifecycle identity and raw observations | Any client or benchmark harness |
| inference-benchmarks | Frozen workload/target bindings and measured outputs/errors/metric coverage | Performance reports and external evaluation consumers |
| compute-runners | Explicit command/workload, resources, inputs and destinations to an execution identity/status/receipt | Any planner/controller that supplies authorized work |
| research-controller | Candidate/attempt identities, bounded sequencing and promotion proposals over supplied adapters | Lab or another research program |
| rl-environments | Explicit observation/action/reward/termination contract | A compatible trainer or external evaluator |

Artifact references should preserve immutable source identity, content hashes,
format compatibility, parent lineage and applicable rights. No single shared
Python class or new central schema package is required by this document.

Measurements need their observation source and coverage. Client latency differs
from server observations; estimated/target-reported/billed cost remain distinct.
Unobservable memory, price or remote version identity stays unknown. A declared
endpoint model version is not immutable-deployment proof.

## Current CPU demonstration

Lab executes validation and preference construction over authored fixtures on
CPU. It separately models hypothetical GPU training from authored assumptions,
uses the estimate in a planning job, and marks `observed_billing: false`.
The result's actual CPU timestamps do not become GPU runtime or billing evidence.

Any SDK call is explicit and optional. Planned model training, serving,
benchmarking, runner and controller capabilities need their own implementations
and acceptance evidence before an integrated model workflow can claim them.
