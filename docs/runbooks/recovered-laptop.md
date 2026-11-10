# Import recovered laptop work

Last updated: 2026-11-10

1. Preserve an intact recovery copy before opening tools that write to it:
   Git objects/refs, dirty files, untracked files, and unique artifacts. Keep
   private data and credentials outside public repositories.
2. Compare recovery refs and working files against source
   `ba67e510bab2703b1042993744ce099490221c1f` and original main
   `36bb3839f1bc166fa54824fd8457b28ca5189dae`. Later laptop commits need their
   actual merge base identified; do not assume this Mac had the newest code.
3. Use [the migration map](../sources/repository-split-map.json) to route old
   paths to current owners. Match original hashes to distinguish unchanged
   baseline files from recovered modifications. Archived paths preserve context.
4. Export one coherent change per owner on a new branch. Adapt imports to the
   new package names and declared dependencies. Keep conflicting implementations
   available for comparison instead of overwriting the new owner.
5. Link related PRs when one change crosses repositories. Verify each component
   independently, then update Lab's declared composition and integration checks.
6. Record recovered source revisions, old/new paths, hashes, decisions, tests,
   failures, and unresolved artifacts. Keep scientific negative results.
7. Only retire temporary recovery copies after unique source, history, and
   artifacts are verified preserved. Recovery itself does not authorize release
   of private datasets, paid jobs, or broad cleanup.

Future work starts directly in its canonical component repository. Lab changes
only when integrated configurations, compatibility pins, or shared reports change.
