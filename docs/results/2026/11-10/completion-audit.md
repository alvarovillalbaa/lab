# Repository separation acceptance audit

Last updated: 2026-11-10

The original request and the owner's subsequent choices define this audit:
nine public MIT repositories, planner/runner separation, descriptive names,
standalone SDK packaging, six explicitly planned component homes, and publication
through unmerged review PRs.

## Requirements and current evidence

| Requirement | Authoritative evidence | Verdict |
| --- | --- | --- |
| Locate or bring Lab locally | Lab, original migration checkout, and component checkouts; original source remains preserved | Verified |
| Create the agreed repository homes | Nine public repositories, MIT license recognition, and recorded GitHub heads | Verified |
| Move available code to relevant owners | Complete 57-file source/destination/hash inventory and exact extraction snapshots | Verified |
| Independently install and use implemented components | Five wheels built; four separate fresh component/SDK runtime environments; installed imports and CLI commands checked outside source | Verified on Python 3.14.7 |
| Stack components in multiple combinations | Six fresh Lab profiles: base, compute, distillation, evals, CPU, full; packaged resources loaded and exact dependency Git origins checked | Verified for selected combinations |
| Reuse Open Evals | SDK stays in open-evals, installs without optimizer dependencies, and is consumed in evals/full profiles | Verified within the agreed SDK scope |
| Consider existing projects | Catalogue preserves optional nanochat, autoresearch, my-evals, and separate evaluation-lab ownership/licensing | Verified for catalogue integration |
| Preserve history and existing work | Original July main and October documentation head retained as ancestors; original checkout preserved | Verified |
| Enable future development across repos | Canonical component ownership, separate project instructions/manifests, optional dependency profiles | Verified |
| Prepare for later laptop recovery | Recovery runbook and complete source/destination/hash map; no recovered work is claimed | Verified for migration preparation |
| Distinguish code from planned projects | Three new component libraries and six specification homes remain labelled correctly | Verified against the approved scope |
| Publish through review PRs without merging | Lab PR #2 and Open Evals PR #1 are published and left open | Verified |
| Preserve checks and failures | Initial source receipts, installed receipt with command/build logs and initial DNS failure, wheel/source hashes, and cleanup evidence | Verified |

## Installed acceptance

[Installed acceptance](installed-package.md) records the successful wheel and
fresh-environment checks at their exact source revisions. Source-path tests were
not substituted for installation proof. The Lab runtime, package metadata,
checker, and composition resource match the checked source; follow-up changes
are documentation and evidence only.

The first direct build failed on PyPI DNS. Its log is retained. Build inputs
were then fetched using available HTTPS transport and verified against PyPI
SHA-256 metadata. Task-local mirrors fetched from GitHub supplied the unchanged
declared Git dependency URLs; installed commit identities matched the manifest.

The owner approved the requested 256 MiB task-specific exception. Peak observed
allocated temporary storage was 36.25 MiB. All disposable environments, source
exports, mirrors, build caches, wheels, logs, and the runner were removed after
receipt readback and an open-file check. The normal storage policy still applies
to future tasks.

## Intentional limits

Both migration PRs remain open for owner review as requested. Six project homes
contain specifications; new training, inference, data, environment, and GPU
engines were outside the approved extraction implementation. Laptop recovery is
future work. SDK HTTP was mocked; live provider/hosted acceptance, other Python
versions/platforms, deployment, and scientific model performance are not claimed.

Links: [migration result](repository-split.md),
[installed receipt](installed-package.json),
[source map](../../../sources/repository-split-map.json),
[Lab PR](https://github.com/alvarovillalbaa/lab/pull/2),
[SDK PR](https://github.com/alvarovillalbaa/open-evals/pull/1).
