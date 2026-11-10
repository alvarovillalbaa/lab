# Product split acceptance

Last updated: 2026-11-10

Status: source checks passed; wheel/fresh-install acceptance awaits the owner's
new task-scoped storage exception. This is an incomplete verification gate.

The [JSON result](product-installed-package.json) records the checked source
commits. Three verification-runtime, four model-distillation and nine Lab
integration cases passed. Source CLI demonstrations passed for the independent
exact-match verifier and distillation fixture. No provider or model was called.

Required next coverage is seven wheels, six standalone component/SDK installs
with their declared dependencies, and nine Lab profiles: base, verification,
economics, planning, compute, distillation, evals, CPU and full. Distillation 0.2
must resolve its pinned verification-runtime dependency through the real package
metadata; source-root imports do not prove that installation path.

Storage Guard reported 8.4 GiB free versus 34.0 GiB required. The owner's
local storage policy stops builds/installs after
a failing check. A new 256 MiB exception with measured usage and cleanup was
requested. Prior exceptions are closed and are not reused. No approval is
inferred from elapsed time or the previous approvals.

The [previous expanded receipt](expanded-installed-package.md) remains valid
historical proof for its earlier revisions. It does not establish installation
of verification-runtime, distillation 0.2 or Lab 0.4.

Architecture and artifact homes contain independent contracts and source lineage,
not model or storage engines. Exact-match is the current verifier adapter;
code/math/schema/environment/citation execution remains planned. No GPU, paid
execution, deployed service, real evaluation or scientific result is established.
