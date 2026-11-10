# Expanded installed-package acceptance

Last updated: 2026-11-10

Passed for Lab 0.3.0 source `d9044c9cd0f1147fe0f965d23a609dbe0ac6599f`.
The [JSON receipt](expanded-installed-package.json) records exact source commits,
wheel hashes/metadata, commands, logs, installed module locations and Git origins.
The [first-stage receipt](installed-package.md) remains historical and unchanged.

| Check | Result |
| --- | --- |
| Isolated wheel builds | Six passed: experiment-kit, compute-economics, compute-planner, model-distillation, open-evals-sdk and Lab |
| Independent fresh installations | Five passed, each with only its component/SDK installed |
| Lab fresh-install profiles | Eight passed: base, economics, planning, compute, distillation, evals, CPU and full |
| Source integration cases | Eight passed, including economics-to-planner cost handoff |
| Exact dependency revisions | Installed Git origins match every selected manifest pin |

The economics-only profile estimates cost without a planner installation. The
planning-only profile routes jobs without economics installed. Missing optional
commands return the documented dependency error. Planner 0.2 contains no costing
module, costing exports or estimate command.

CPU/full checks validate the packaged composition, installed CLI, preference
fixture, actual CPU/zero-GPU resource record and hypothetical cost provenance:
`authored_assumptions`, `observed_billing: false`, positive estimated cost.
SDK transport is mocked; no evaluation service request is sent.

Two failed preparation attempts are retained: child-process DNS blocked the
initial packaging-tool download and sparse SDK object hydration. The supported
command path downloaded hash-verified backend wheels and a bounded SDK mirror.
Four other dependency mirrors came from canonical local checkouts. All five exact
commits were independently readable through GitHub's API. Lab's real declared
Git dependencies then resolved through task-local mirrors, with installed commit
IDs checked. This is offline installation proof, not unrestricted online resolver
proof. An earlier source check also caught the not-yet-updated manifest; it passed
after the pins were completed.

The owner approved a [new 256 MiB storage exception](expanded-storage-exception.md).
Peak observed allocated task storage was 43,266,048 bytes (41.26 MiB), sampled
every 0.1 seconds during runner child processes. Every disposable runtime
environment was removed after its check. Final task-directory teardown is
recorded in the JSON receipt after open-file and canonical-result readback checks.

No GPU training, paid execution, observed billing, deployed endpoint, live
evaluation or scientific result is established. The ten planned product homes
have specifications and provenance; this check does not turn them into engines.
