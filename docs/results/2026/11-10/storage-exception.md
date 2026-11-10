# Installed verification storage exception

Last updated: 2026-11-10

The owner approved the previously requested task-scoped storage exception and
explicitly instructed resuming work. This approval permits at most 256 MiB of
temporary files for the remaining independent installation and wheel checks.
It does not change the general storage reserve or authorize unrelated cleanup.

Scope: build the three extracted component libraries, the existing Open Evals
SDK package, and Lab; verify four standalone installations and six selected Lab
profiles in disposable environments outside the source checkouts.

All temporary source exports, build environments, package caches, wheels,
runtime environments, and logs belong to one task directory. Track its allocated
bytes while each child runs, stop if the budget is exceeded, retain bounded
results and failures, then remove only that task's generated files. Do not
download Python runtimes, model weights, GPU libraries, or provider datasets.

The composition stays a candidate because the two migration PRs await review.
Removing the obsolete installation-pending phrase from its reason does not
claim a passing check. Installed acceptance will be recorded separately after
the actual runs.

## Execution and closure

The approved checks passed. Peak observed temporary allocation was 36.25 MiB,
and all task-created temporary files were removed after evidence preservation.
See [the installed result](installed-package.md). This exception is now consumed;
it does not authorize later installations or alter the general reserve.
