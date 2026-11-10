# Expanded split verification storage exception

Last updated: 2026-11-10

The owner explicitly approved a new task-scoped 256 MiB exception for build and
installation verification of the expanded split, with cleanup afterward.
The previous exception is closed and is not reused.
The standard preflight immediately before preparation reported 11.4 GiB free
against 34.0 GiB required; this explicit exception covers only the bounded run.

This scope covers the new compute-economics package, compute-planner 0.2.0,
Lab's updated composition/profiles, and unchanged component/SDK dependencies
needed for those combinations. Planned repositories require documentation,
ownership, provenance, and navigation checks, not invented runtimes.

Use one task-owned directory for temporary source exports, backend wheels,
Git mirrors, caches, runtime environments, and logs. Measure its allocated
bytes while child processes run and stop if the cap is exceeded. Preserve
bounded results and failures, verify no process uses its generated files, then
remove only task-created files. The general storage reserve remains unchanged.

Closed after verification: peak task use was 41.26 MiB, no open files were
reported, and all temporary environments plus the task directory were removed.
See [the acceptance receipt](expanded-installed-package.json).
