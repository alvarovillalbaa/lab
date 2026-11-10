# Installed package acceptance

Last updated: 2026-11-10

This procedure checks the expanded package set independently of the historical
[first-stage completion audit](../results/2026/11-10/completion-audit.md).
Installation/building still requires a passing Storage Guard preflight or the
owner's explicit task-specific exception. This procedure grants no exception.

Build six wheels: experiment-kit, compute-economics, compute-planner,
model-distillation, open-evals-sdk and Lab, from the exact declared source
revisions. Preserve the wheel hashes, build logs, source revisions, review
state and tool versions in the result.

For each of the five standalone component/SDK wheels, create a separate fresh virtual
environment and install only that package. Run the checker below from outside
the source checkouts, using the environment's interpreter:

```sh
python -I /path/to/lab/scripts/check-installed.py --distribution experiment-kit
```

Repeat with compute-economics, compute-planner, model-distillation and
open-evals-sdk. The checker
requires isolation, rejects editable/source imports and other installed
ecosystem packages, and invokes the installed console commands. The SDK check
mocks HTTP transport and sends no network request.

In eight separate fresh environments, install Lab with base, economics,
planning, compute, distillation, evals, CPU (compute plus distillation), and full
profiles. The economics-only and planning-only profiles verify that neither
requires the other. Check each with:

```sh
python -I /path/to/lab/scripts/check-installed.py --distribution clous-llm-lab --profile base
```

Use --profile economics, planning, compute, distillation, evals, cpu or full as
appropriate.
CPU/full checks additionally require --code-ref with the exact checked Lab
revision. Check the installed packaged composition resource and the actual
installed command entrypoints; source-root imports do not substitute for this.
Lab's declared profiles should also be exercised through their real dependency
declarations, retaining resolved Git revisions in the install receipt.

Record the actual source/dependency transport separately from installation
isolation. Task-local bare mirrors of canonical checkouts can supply exact
commits when network access is restricted; record how each commit's remote
availability was independently checked. Mirror-backed installation is not
unrestricted online dependency-resolution proof or a fresh remote clone.

Costing fixtures must provide an explicit hourly GPU rate. A deliberate zero
rate is an authored caller assumption; a missing rate must not silently become
zero. The CPU/full workflow uses authored GPU-training assumptions with
`observed_billing: false`; installed acceptance does not establish GPU execution
or observed billing.

The checker is Lab's acceptance tooling. Components themselves do not need Lab
installed. A checker syntax/help run or deliberate rejection of a non-isolated
environment is not installed-package acceptance.

Record expanded outcomes in
[expanded-installed-package.json](../results/2026/11-10/expanded-installed-package.json)
and [the readable result](../results/2026/11-10/expanded-installed-package.md).
The six-wheel, five-standalone and eight-profile counts above are required
coverage, not a claim that those checks have passed. Preserve the first-stage
receipts unchanged.

Retain failed attempts as evidence. Remove only task-created virtual
environments, build caches, wheels, and temporary clones after preserving the
bounded result. Keep all canonical source checkouts and user work.
