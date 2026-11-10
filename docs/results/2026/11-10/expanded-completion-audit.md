# Expanded split completion audit

Last updated: 2026-11-10

The expanded ecosystem contains fourteen component repositories, existing
Open Evals and umbrella Lab. Five additional repositories were published on
main: compute-economics, model-tokenizers, model-posttraining,
inference-benchmarks and research-controller. All are public and MIT licensed.

Model-training became model-pretraining with repository ID 1452711751 preserved;
model-inference became model-serving with ID 1452712112 preserved. Scope changes
remain in their review PRs. Their Git histories, original refs and migration
source identities remain available.

| Review | State |
| --- | --- |
| [Lab #2](https://github.com/alvarovillalbaa/lab/pull/2) | Expanded integration and migration; open |
| [Planner #1](https://github.com/alvarovillalbaa/compute-planner/pull/1) | Economics extraction; open |
| [Data #1](https://github.com/alvarovillalbaa/model-data/pull/1) | Tokenizer extraction; open |
| [Pretraining #1](https://github.com/alvarovillalbaa/model-pretraining/pull/1) | Separate post-training; open |
| [Serving #1](https://github.com/alvarovillalbaa/model-serving/pull/1) | Separate benchmarking; open |
| [Open Evals #1](https://github.com/alvarovillalbaa/open-evals/pull/1) | Existing SDK packaging review; preserved open |

No PR was merged. The older Lab documentation PR #1 was preserved. The
[live remote snapshot](expanded-repositories-remote.json) records repository
identities, visibility, detected licenses and open review heads. Lab main still
predates this migration; its MIT license is in the review branch.

[Installed acceptance](expanded-installed-package.md) passed six wheel builds,
five independent installations and eight Lab profiles from frozen source
revisions. Eight focused Lab source checks also passed. Lab runtime/package
metadata remain identical to the checked source `d9044c9`; later changes are
documentation, recovery tooling and evidence. The approved storage exception is
closed, with all disposable verification resources removed.

The [V2 map](../../../sources/repository-split-v2-map.json) and
[checker](../../../../scripts/check-expanded-provenance.py) account for 57
original files, 55 intermediate files, four pinned component maps, 26 original
section routes and 171 destination checks. Both historical repository aliases
match the identity registry. All 26 frozen archive hash checks passed. Tampered
V1 hashes, changed alias IDs and an omitted original were correctly rejected.
V1 and pre-split sources remain byte-identical. Economics' exact extraction
snapshot and subsequent explicit-price/hour-unit correction are recorded
separately.

The [provenance result](expanded-provenance.json) records those checks. The
[local-state receipt](expanded-local-state.json) verifies all fifteen component/
Open Evals checkouts are clean, selected revisions remain reachable, and current
implemented code matches the selected commits. Sixty-two relative links in the
active Lab documentation resolve; whitespace checks pass.

The four implemented component libraries remain independently installable;
ten other homes contain planned specifications. The recovery map supports later
laptop reconciliation but contains no recovered-laptop data. CPU fixtures,
mocked SDK transport and offline mirror-backed dependency resolution do not
establish GPU training, paid execution, deployed services or scientific results.
