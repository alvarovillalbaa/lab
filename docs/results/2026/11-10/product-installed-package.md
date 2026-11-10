# Product split installed acceptance

Last updated: 2026-11-10

Passed for Lab 0.4.0 source `0396ad6045b778ca701b5e09dca63cb36e8f2486`.
The [JSON receipt](product-installed-package.json) records source commits,
wheel hashes/metadata, commands, logs, installed module locations and Git origins.
Runtime/package inputs match the source checked at `fd8f16a`; later changes
are documentation, recovery tooling and evidence.

| Check | Result |
| --- | --- |
| Isolated PEP517 wheel builds | Seven passed: verifier, experiment-kit, economics, planner, distillation, SDK and Lab |
| Independent fresh installations | Six passed, each with only its declared dependencies |
| Fresh Lab profiles | Nine passed: base, verification, economics, planning, compute, distillation, evals, CPU and full |
| Source integration cases | Three verifier, four distillation and nine Lab cases passed |
| Installed dependency origins | All Git commit IDs match selected composition pins |

Verification-runtime 0.1.0 installs without Lab, distillation or an evaluation
service. Its installed CLI accepts correct text and rejects incorrect text.
Model-distillation 0.2.0 resolves its pinned verification-runtime dependency
through real package metadata. Its installed check confirms removed verifier
exports and rejects a result for changed candidate bytes. Independent use permits
explicit dependencies; it does not require every package to be dependency-free.

The verification-only Lab profile uses the runtime without distillation.
Other isolated profiles exercise present commands and expected missing-dependency
errors. CPU/full verify the packaged composition, direct verifier result,
preference fixture and CPU/zero-GPU resource record. Hypothetical GPU costs retain
`authored_assumptions` and `observed_billing: false`. SDK transport is mocked.

Backend wheels were downloaded through supported curl commands with a 2 MiB
per-file bound, then hash-verified. Five dependency mirrors came from canonical
checkouts; the bounded SDK mirror came directly from GitHub. All six exact
dependency commits were independently readable through GitHub's API. Original
declared URLs resolved through task-local mirrors and installed commit IDs were
checked. This establishes offline mirror-backed installation and interfaces,
not unrestricted online resolver networking or live provider/service behavior.

The owner explicitly approved the
[task-scoped 256 MiB exception](product-storage-exception.json) after a standard
preflight reported 9.6 GiB free versus 34 GiB required. Peak observed allocated
task storage was 43,999,232 bytes (41.96 MiB), sampled every 0.1 seconds during
runner child processes. All environments were removed after checks; lsof found
no open files before teardown. Canonical receipt readback and wheel hashes were
verified before removing the task directory, mirrors, cache, exports, wheels,
logs and runner. The exception is closed.

The [earlier expanded receipt](expanded-installed-package.md) remains unchanged
historical evidence. The initial pending state of this result remains in Git
history. No build/install began before the new exception was approved.

Exact matching is the implemented verifier adapter. Code/math/schema/environment/
citation execution remains planned. Architecture and artifact homes contain
independent contracts and source lineage, not model or storage engines.
No GPU training, paid execution, deployed endpoint, live evaluation or scientific
result is established by this acceptance.
