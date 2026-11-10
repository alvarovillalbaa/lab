# Integration backlog

Last updated: 2026-11-10

Lab owns ecosystem integration, experiments and shared reports. Product engines
and their bounded implementation backlogs belong to the
[canonical component owners](references/component-ownership.md).

## Current boundary expansion

The expanded target is fourteen component repositories plus Open Evals and Lab.
Its four implemented libraries are experiment-kit, compute-economics,
compute-planner and model-distillation; ten component homes remain planned.

- Economics owns workload estimates; planning owns routing/job order; runners own execution.
- Dataset preparation consumes explicit tokenizer artifacts from model-tokenizers.
- Model-pretraining and model-posttraining exchange portable model artifacts.
- Model-serving and inference-benchmarks exchange endpoint/measurement bindings.
- Research-controller owns reusable bounded model-research orchestration.

The expanded package/profile check outcomes are recorded separately in
[expanded-installed-package.json](results/2026/11-10/expanded-installed-package.json).
The first-stage wheel/install checks remain historical evidence; they do not
prove changed economics/planner APIs or Lab 0.3.

## Next integration work

- [ ] Review and integrate the existing-repository scope changes and SDK packaging; retain the manifest's candidate state until those owner reviews complete.
- [ ] Update compatibility pins deliberately when a component's public interface changes.
- [ ] Materialize approved dataset/tokenizer/model artifacts before any real training or serving run.
- [ ] Connect a working compute runner to a planner consumer after the runner exists.
- [ ] Add tokenizer/data and pretraining/post-training artifact round trips when their engines exist.
- [ ] Measure an independently supplied serving endpoint with a working benchmark harness.
- [ ] Integrate a bounded research-controller implementation using explicit external training/evaluation adapters.
- [ ] Preserve, inspect and distribute recovered laptop work through the two-stage relocation maps.
- [ ] Resolve per-study budget, data/teacher rights, provider access and scientific release gates.

The CPU integration fixture is an implementation check over authored responses
and hypothetical compute assumptions. It does not establish GPU allocation,
observed billing, trained model capability, inference performance or promotion.
