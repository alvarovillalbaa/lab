# Third product split audit

Last updated: 2026-11-10

Status: implementation and requirements migration published; fresh-install
verification remains incomplete pending a new owner storage exception.

The ecosystem now has seventeen components, existing Open Evals and Lab: nineteen
repositories. Five component libraries are implemented; twelve homes contain
planned specifications. The three additions are public MIT repositories on main:

| Product | Delivered scope | Evidence |
| --- | --- | --- |
| [verification-runtime](https://github.com/alvarovillalbaa/verification-runtime) | Standalone exact-match package/CLI and generic result identities; broader objective adapters planned | Three source cases and CLI passed; exact source lineage archived |
| [model-architectures](https://github.com/alvarovillalbaa/model-architectures) | Independent model-math/configuration/forward/cache/weight-compatibility contract | Original model sections and prior pretraining projections preserved with hashes; engine remains planned |
| [research-artifacts](https://github.com/alvarovillalbaa/research-artifacts) | Generic resolve/transfer/cache/integrity contract using existing storage backends | Exact source fragment and internally consistent tiny artifact reference; materializer remains planned |

## Code, ownership and composition

Model-distillation 0.2 removes its old verifier/result exports and imports the
exact verification-runtime dependency. Teacher eligibility remains independent
of answer correctness. Pair construction rejects mismatched subject IDs and
changed candidate/reference bytes. Four focused distillation checks passed.
Open Evals retains evaluator definitions, composition, scoring, runs and gates.

Lab 0.4 pins every selected commit, exposes verification independently, and
includes the verification result in its CPU fixture. Nine source integration
cases passed. All nine declared/checker profiles agree, including the transitive
distillation dependency. Runtime/package inputs remain identical to checked
source `fd8f16a8f238c3f2d2d5a18f53e9a3999e776de8`; later changes are docs,
recovery tooling and evidence. All eighteen component/Open Evals checkouts were
clean and their selected revisions reachable during the local audit.

The [V3 recovery map](../../../sources/repository-split-v3-map.json) chains the
unchanged V1/V2 maps. [Provenance checks](product-provenance.json) cover all 57
original files, 55 earlier and 31 new intermediate files, 69 new destination
checks, five new section routes and two original route refinements. The prior
171 destination checks still pass. Five incomplete/tampered V3 cases were
rejected. Frozen source archives and prior installed receipts are unchanged.

Sixty-seven relative links across the checked living Lab/new-product docs
resolve. Whitespace checks pass. The original damaged-laptop implementation
remains outside the baseline; these maps prepare its later reconciliation.

## Publication and remaining gate

The [remote snapshot](product-repositories-remote.json) records nineteen public
repository identities, branch heads, detected licenses and open reviews. The
three new main branches match their selected source commits. Existing changes
remain reviewable and unmerged:

- [Lab #2](https://github.com/alvarovillalbaa/lab/pull/2): integration, documentation and recovery.
- [Distillation #1](https://github.com/alvarovillalbaa/model-distillation/pull/1): external verification dependency and policy boundary.
- [Pretraining #2](https://github.com/alvarovillalbaa/model-pretraining/pull/2): architecture boundary, stacked on preserved pretraining #1.

Other existing reviews and histories are preserved. Gateway, safety-gateway and
provider-adapter repositories remain conditional candidates from the assessment;
this migration establishes the three explicitly recommended product homes.

[Installed acceptance](product-installed-package.md) is still pending. Seven wheel
builds, six independent installs with declared dependencies and nine Lab profiles
must pass for the changed APIs. Source checks and older installed receipts do not
substitute for that proof. Storage Guard reported 8.4 GiB free against 34 GiB
required; a new 256 MiB task exception with measurement/cleanup was requested.
Neither earlier exception is reused. No build/install has started without it.

No code sandbox, symbolic verifier, model architecture engine, artifact transfer,
GPU job, deployed endpoint or scientific improvement is claimed by this source
migration. Those capabilities retain their explicit planned/observational limits.
