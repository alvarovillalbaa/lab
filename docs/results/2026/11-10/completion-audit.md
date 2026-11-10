# Repository separation acceptance audit

Last updated: 2026-11-10

The original request was read again from the owner's attachment. This audit
checks that request together with the owner's subsequent choices: nine public
MIT repositories, planner/runner separation, descriptive names, standalone SDK
packaging, six explicitly planned component homes, and publication through
unmerged review PRs.

## Requirements and current evidence

| Requirement | Evidence inspected | Verdict |
| --- | --- | --- |
| Locate or bring Lab locally | Current Lab checkout and original migration checkout; both clean | Verified |
| Create the agreed independent repository homes | GitHub API returned all nine repositories, public visibility, MIT license recognition, and their recorded main SHAs | Verified |
| Move available code to relevant owners | All 57 original source hashes and every recorded destination hash checked against current files | Verified |
| Independently install and use implemented components | Package manifests, library/CLI source, and prior source checks exist; no clean installed-environment execution exists | Incomplete |
| Stack components in multiple combinations | Commit-pinned base/compute/distillation/evals profiles and packaged composition manifest; source composition checks cover the implemented CPU workflow | Source composition verified; installed combinations pending |
| Reuse Open Evals | SDK remains in open-evals; its packaging PR is open at d1002d58109156683be3ad4fc394c7cc6c534057 | Verified within the agreed SDK scope |
| Consider existing projects | Current catalogue routes nanochat, autoresearch, and my-evals as optional projects and keeps evaluation-lab's separate ownership/licensing | Verified as catalogue integration; no new runtime integration claimed |
| Preserve history and existing work | Both original July main and October documentation head are ancestors of the migration branch; original checkout remains clean | Verified |
| Allow future work in several repositories | Component ownership, separate project instructions/manifests, and pinned integration metadata are present | Verified |
| Prepare for later laptop recovery | Recovery procedure and complete source/destination/hash inventory exist; no recovered data is claimed | Verified for migration preparation; actual recovery is future work |
| Clearly distinguish code from planned projects | Three new component libraries and six specification homes remain labelled accordingly | Verified against the approved scope |
| Publish without merging existing repositories | Lab PR #2 and Open Evals PR #1 are open, unmerged, and report clean mergeability | Verified |
| Preserve a meaningful verification trail | Existing result receipts, CPU fixture output, extraction provenance, and this audit | Verified; proof limits retained |

The migrated Lab runtime, existing tests, validation script, and package metadata are
unchanged from checked source 36dbfc04b9c4ab37e07584e25afee3a18ff04e1b.
Source checks therefore still apply to those exact bytes. They do not establish
installed-package behavior.

## Outstanding acceptance gate

Storage Guard was run again and failed: 10.8 GiB free against 34 GiB required.
The existing interpreter has pip and wheel but no setuptools/build backend.
No install, build, storage-policy override, or unrelated cleanup was performed.

Independent-install acceptance requires building the four library/SDK packages
and Lab, checking each library alone outside source checkouts, checking selected
Lab installation profiles, and checking installed console commands and packaged
composition resources. The SDK network boundary can remain mocked; live provider
or hosted-service acceptance is outside this migration.

A bounded task-specific storage exception has been requested from the owner.
It is not granted by an unanswered question. Until permission or sufficient
storage exists, the full goal remains active and independent installation is
unproven. Existing PR review is intentionally left to the owner.

## Installed verification readiness

The follow-up preflight still fails: 10.9 GiB free against 34 GiB required.
The [installed acceptance procedure](../../../runbooks/installed-package-acceptance.md)
and its checker are now prepared for four independent component/SDK installations
and six Lab profiles. The checker performs no installation or build.

Checker syntax and help passed. Invoking it in the existing non-isolated
interpreter correctly returned exit 2 with the requirement for a fresh virtual
environment. This is a rejection check, not successful installed-package proof.
No package install, wheel build, storage exception, or unrelated cleanup has run.

Links: [migration result](repository-split.md),
[source map](../../../sources/repository-split-map.json),
[Lab PR](https://github.com/alvarovillalbaa/lab/pull/2),
[SDK PR](https://github.com/alvarovillalbaa/open-evals/pull/1).
