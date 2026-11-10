# Installed package acceptance result

Last updated: 2026-11-10

Status: passed. [Machine-readable receipt](installed-package.json) includes
source revisions, wheel hashes, actual tool versions, installed module origins,
42 command results, and bounded build/check logs.

## Executed checks

- Five isolated PEP 517 wheel builds: experiment-kit, compute-planner,
  model-distillation, open-evals-sdk, and Lab.
- Four separate fresh runtime environments, each containing only its component
  package: imports and installed console commands passed; the SDK transport check
  passed with mocked HTTP.
- Six separate Lab environments: base, compute, distillation, evals, CPU
  (compute + distillation), and full (compute + distillation + evals).
- Lab profiles resolved their actual declared dependencies. Installed Git commit
  identities matched the pinned composition. No editable install or source-path
  substitution was accepted.
- The packaged Lab composition resource loaded from site-packages. Installed
  CPU/full commands completed the authored fixture workflow outside checkouts.
- Missing optional compute was handled in profiles that deliberately omit it.

The checked Lab source is f4c40d3c9146d739579ff32acbf1ae2d8a2e6b8a.
Component and SDK source revisions are listed in the receipt.

## Failed attempt and transport

The initial direct build failed when uv could not resolve PyPI DNS. That failure
and its log are retained. Three bootstrap wheels were fetched through available
HTTPS transport and matched to the SHA-256 values in PyPI metadata. Subsequent
isolated builds used that local wheel directory.

Git dependencies retained their original URLs and commit pins. A task-only Git
configuration redirected transport to temporary mirrors fetched from GitHub.
Installed direct_url metadata proved the expected commits. This is offline
installation acceptance, not a claim that unrestricted online package-manager
networking worked in the execution environment.

Build tools: Python 3.14.7, uv 0.10.3, setuptools 84.2.1. These actual versions
are recorded inputs, not new runtime dependencies of the packages.

## Storage and remaining limits

The owner approved a task-scoped 256 MiB exception. Peak observed allocated
temporary storage was 38,010,880 bytes (36.25 MiB), sampled while children ran.
All disposable environments, source exports, mirrors, build caches, wheels,
and task logs were removed after canonical receipt readback and an open-file
check. The task directory is absent. Temporary/toolchain paths in preserved
logs are normalized; source revisions, wheel hashes, and outcomes are retained.

No Python runtime, model weights, GPU libraries, database, or provider workload
was downloaded or executed. SDK requests used mocked transport. Cross-platform
and other Python versions were not tested. The six planned repositories remain
specifications, and both integration PRs remain open for owner review.

The original storage failures and source-only checks remain historical evidence
in [the initial migration result](repository-split.md). This installed result
closes its installation/wheel acceptance gap.
