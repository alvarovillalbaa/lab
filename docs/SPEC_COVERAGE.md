# Spec Coverage

This file maps the pasted request and `docs/specs/` inputs to concrete repo
artifacts. It should be updated whenever implementation moves from skeleton to
real training code.

Status values in this file describe whether the requirement is covered by the
current planning/scaffold artifact. They do not claim that paid GPU training,
provider deployment, or model release has already happened.

## User Mission

| Requirement | Artifact | Status |
| --- | --- | --- |
| Learn how to train LLMs | `docs/STEP_BY_STEP.md`, local tiny trainer milestone | Documented |
| Prove competence publicly | `reports/templates/*`, `docs/STEP_BY_STEP.md` public proof standard | Skeleton |
| Discover and prove improvements | ablation plan in `docs/STEP_BY_STEP.md` | Documented |
| Lowest practical cost, even if slower | cost CLI, routing policy, budget gates | Skeleton |
| Pretraining, post-training, serving | experiment configs and architecture lanes | Skeleton |
| Advanced distillation | distillation phase and future data engine contract | Documented |
| Autonomous GPU workload allocation | scheduler phase and routing policy | Documented |
| Self-improvement LLMs | bounded self-improvement phase | Documented |
| From-scratch development where useful | local tiny model path first | Documented |
| Use open-source systems where sensible | OLMo-core, TorchTitan, TRL, vLLM, eval harnesses documented | Documented |
| Full-scale production development, not MVP framing | complete factory roadmap and release standard | Skeleton |

## `docs/specs/providers.md`

| Input | Artifact | Status |
| --- | --- | --- |
| Everything locally and from-scratch | local lane is mandatory in README and architecture | Skeleton |
| Base10 for serving | documented as Baseten/Base10 serving adapter | Skeleton |
| Thinking Labs Machine | documented as Thinking Machines Lab Tinker post-training adapter | Skeleton |

## `docs/specs/libraries.md`

| Input | Artifact | Status |
| --- | --- | --- |
| PorTAL | tracked in README and `docs/decisions/experiment-decisions.md` until role is pinned | Needs human clarification |

## `docs/specs/human-steps.md`

This spec file is empty. Derived human gates live in
`docs/HUMAN_GATES.md`.

## `docs/specs/steps.md`

| Section | Artifact | Status |
| --- | --- | --- |
| Define experiment | `docs/decisions/experiment-decisions.md`, `docs/STEP_BY_STEP.md` | Skeleton |
| Core technical stack | `docs/ARCHITECTURE.md`, `pyproject.toml` | Skeleton |
| Compute strategy | `src/lab/costing.py`, configs | Skeleton |
| Public proof standard | `reports/templates/*` | Skeleton |
| Repository layout | repo scaffold | Skeleton |
| Tiny trainer | planned in `docs/STEP_BY_STEP.md` | Documented |
| Infrastructure baseline | `infra/*`, docs | Skeleton |
| Data pipeline | `data/*`, docs | Skeleton |
| Tokenizer | `data/tokenizer`, docs | Skeleton |
| Model architecture | `docs/STEP_BY_STEP.md` | Documented |
| Pretraining ladder | configs and docs | Skeleton |
| Post-training | docs and configs | Skeleton |
| Distillation system | docs and future module boundary | Documented |
| Self-improvement loop | docs | Documented |
| GPU scheduler | `src/lab/routing.py`, docs | Skeleton |
| Evaluation | docs and future config boundary | Documented |
| Serving | serving config and docs | Skeleton |
| Safety/governance | `docs/HUMAN_GATES.md`, `docs/ARCHITECTURE.md` | Skeleton |
| Timeline | `docs/STEP_BY_STEP.md` | Skeleton |
| Public report sections | report templates | Skeleton |
| Innovation bets | `docs/STEP_BY_STEP.md` | Documented |
| What not to do | gates and docs | Skeleton |
| First execution plan | README and `docs/STEP_BY_STEP.md` | Skeleton |

## `docs/specs/steps-follow-ups.md`

| Section | Artifact | Status |
| --- | --- | --- |
| Provider split | `docs/ARCHITECTURE.md`, provider configs | Skeleton |
| Manual decisions | `docs/decisions/experiment-decisions.md`, `docs/HUMAN_GATES.md` | Skeleton |
| Tinker optional/core decision | `docs/decisions/experiment-decisions.md` | Skeleton |
| Baseten serving/training decision | `docs/decisions/experiment-decisions.md`, provider config | Skeleton |
| Raw GPU provider choice | `docs/decisions/experiment-decisions.md`, provider config | Skeleton |
| Legal/data posture | `docs/HUMAN_GATES.md` | Skeleton |
| Eval gates before training | `docs/HUMAN_GATES.md` | Skeleton |
| 48-hour plan | README and `docs/STEP_BY_STEP.md` | Skeleton |
| Multi-provider factory | `docs/ARCHITECTURE.md`, routing config | Skeleton |
| Own GPUs first-class provider | local provider config | Skeleton |
| Training libraries | `docs/LIBRARIES_AND_PROVIDERS.md` | Skeleton |
| Post-training libraries | `docs/LIBRARIES_AND_PROVIDERS.md` | Skeleton |
| Serving libraries | `docs/LIBRARIES_AND_PROVIDERS.md` | Skeleton |
| Data stack | `docs/LIBRARIES_AND_PROVIDERS.md` | Skeleton |
| Tokenizer stack | `docs/LIBRARIES_AND_PROVIDERS.md` | Skeleton |
| Evaluation stack | `docs/LIBRARIES_AND_PROVIDERS.md` | Skeleton |
| Orchestration | docs and routing | Skeleton |
| Storage stack | architecture docs | Skeleton |
| Observability | `docs/LIBRARIES_AND_PROVIDERS.md`, architecture docs and report templates | Skeleton |
| System dependencies | `docs/LIBRARIES_AND_PROVIDERS.md` | Skeleton |
| Provider routing policy | `src/lab/routing.py`, `configs/providers/routing.json` | Skeleton |
| Clean architecture | repo structure | Skeleton |
