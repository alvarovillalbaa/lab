# Repository split result

Last updated: 2026-11-10

Implemented source: `36dbfc04b9c4ab37e07584e25afee3a18ff04e1b`.
Baseline: `ba67e510bab2703b1042993744ce099490221c1f`, retaining original July main and the
October documentation lineage. The previous source checkout remains clean.

## Published component repositories

All nine repositories are public, MIT-licensed, and their main heads were read
back from GitHub and matched to the declared component revisions.

| Repository | Status |
| --- | --- |
| [experiment-kit](https://github.com/alvarovillalbaa/experiment-kit) | Library and CLI |
| [compute-planner](https://github.com/alvarovillalbaa/compute-planner) | Library and CLI |
| [compute-runners](https://github.com/alvarovillalbaa/compute-runners) | Specifications; runtime planned |
| [model-data](https://github.com/alvarovillalbaa/model-data) | Specifications; runtime planned |
| [model-training](https://github.com/alvarovillalbaa/model-training) | Specifications; runtime planned |
| [model-distillation](https://github.com/alvarovillalbaa/model-distillation) | Library and CLI |
| [model-inference](https://github.com/alvarovillalbaa/model-inference) | Specifications; runtime planned |
| [ml-foundations](https://github.com/alvarovillalbaa/ml-foundations) | Specifications; runtime planned |
| [rl-environments](https://github.com/alvarovillalbaa/rl-environments) | Specifications; runtime planned |

The [Open Evals SDK PR](https://github.com/alvarovillalbaa/open-evals/pull/1)
packages the original module without changing its source bytes. Existing
repository changes remain for review; no main branch was merged.

## Checks

- 22 focused tests passed: four each for experiment-kit, compute-planner, and
  model-distillation, three for the SDK, and seven for Lab composition.
- Ten CLI checks passed, including expected errors for an unknown route and a
  missing optional component. The three independent quickstart examples passed.
- The actual CPU fixture composition passed at the source commit above.
- Python syntax and JSON/TOML metadata parsed successfully.
- All 57 original tracked files have mapped destinations. Eleven original
  extraction files and 16 archived documents retain their exact source bytes.
- Source imports use explicit component roots with the existing interpreter.
  No sibling-path assumption was added to package code or product commands.
- Whitespace checks passed with exact-copy detection for the frozen documents:
  `git diff --check --find-copies=100% --find-copies-harder`.
  Plain staged checking originally reported two inherited blank-at-EOF warnings
  in byte-preserved documents; those originals were retained unchanged.
- Current navigation is checked separately from frozen historical source links.

[Machine-readable checks](repository-split.json) ·
[CPU execution output](cpu-smoke.json) ·
[Migration map](../../../sources/repository-split-map.json)

## Remaining proof limits

The initial handoff was blocked by Storage Guard: 10.8 GiB free against
34 GiB required. Those source-only receipts remain historical evidence.
The owner subsequently approved a bounded storage exception, and
[installed package acceptance](installed-package.md) passed five wheel builds,
four standalone package installations, and six Lab profiles. Temporary files
were removed after preserving the result. No frontend build or database setup
was required for this package migration.

The workflow uses authored fixture responses. It does not establish training,
GPU allocation, provider billing, scientific model performance, or hosted
Open Evals delivery. SDK transport tests use mocks. Six component repositories
have no executable engine yet. Recovered laptop work is not included.

## Review and future work

Review PRs: [Lab #2](https://github.com/alvarovillalbaa/lab/pull/2) and
[Open Evals #1](https://github.com/alvarovillalbaa/open-evals/pull/1).
Both are open and unmerged. The existing Lab documentation PR remains untouched.

Review the Lab migration and SDK PRs. Installed acceptance has passed; the
composition remains a candidate until owner review and integration. Future
package changes require their relevant checks and the normal storage policy or
a separately approved exception. No new CI, deploy, auth, migration, or registry
publication workflow is introduced.

Use [the recovery procedure](../../../runbooks/recovered-laptop.md) for recovered
work. New reusable development starts directly in its owning repository; Lab
changes when integrated configurations or compatible combinations change.
