# Installed package acceptance

Last updated: 2026-11-10

This procedure closes the independent-install gap in the
[completion audit](../results/2026/11-10/completion-audit.md).
Installation/building still requires a passing Storage Guard preflight or the
owner's explicit task-specific exception. This procedure grants no exception.

Build wheels for experiment-kit, compute-planner, model-distillation,
open-evals-sdk, and Lab from the exact declared source revisions. Preserve the
wheel hashes, build logs, source revisions, and tool versions in the result.

For each of the four component/SDK wheels, create a separate fresh virtual
environment and install only that package. Run the checker below from outside
the source checkouts, using the environment's interpreter:

```sh
python -I /path/to/lab/scripts/check-installed.py --distribution experiment-kit
```

Repeat with compute-planner, model-distillation, and open-evals-sdk. The checker
requires isolation, rejects editable/source imports and other installed
ecosystem packages, and invokes the installed console commands. The SDK check
mocks HTTP transport and sends no network request.

In separate fresh environments, install Lab with base, compute, distillation,
evals, CPU (compute plus distillation), and full profiles. Check each with:

```sh
python -I /path/to/lab/scripts/check-installed.py --distribution clous-llm-lab --profile base
```

Use --profile compute, distillation, evals, cpu, or full as appropriate.
CPU/full checks additionally require --code-ref with the exact checked Lab
revision. Check the installed packaged composition resource and the actual
installed command entrypoints; source-root imports do not substitute for this.
Lab's declared profiles should also be exercised through their real dependency
declarations, retaining resolved Git revisions in the install receipt.

The checker is Lab's acceptance tooling. Components themselves do not need Lab
installed. A checker syntax/help run or deliberate rejection of a non-isolated
environment is not installed-package acceptance.

Retain failed attempts as evidence. Remove only task-created virtual
environments, build caches, wheels, and temporary clones after preserving the
bounded result. Keep all canonical source checkouts and user work.
