# Import recovered laptop work

Last updated: 2026-11-10

## Preserve before routing

1. Preserve the intact recovered Git objects/refs, dirty files, untracked files
   and unique artifacts before opening tools that write to the recovery copy.
   Keep private data and credentials outside public repositories.
2. Identify the recovery's actual merge bases. Compare against original Lab main
   `36bb3839f1bc166fa54824fd8457b28ca5189dae` and the preserved documentation
   baseline `ba67e510bab2703b1042993744ce099490221c1f`; neither proves this Mac
   contained the newest laptop work.
3. Use [the first migration inventory](../sources/repository-split-map.json) for
   original path/hash matching, then
   [the expanded map](../sources/repository-split-v3-map.json),
   [the expansion aliases](../sources/expanded-repository-aliases.json) and each
   component's own relocation record for the current owner. The first inventory
   is historical evidence and must not be rewritten to hide later moves.

Before routing recovered changes, check the preserved local inventories from Lab:

```sh
python3 -B scripts/check-product-provenance.py --workspace ..
```

This reads explicit component checkouts and Git objects without fetching or
changing them. Structural matches guide review; they do not replace reviewing
the recovered implementation.

## Route through the expanded boundaries

| Recovered responsibility or former location | Current owner / routing |
| --- | --- |
| Common research metadata or original Lab validation | experiment-kit |
| Original Lab or compute-planner costing primitives | compute-economics; review explicit-rate and hour-unit API changes |
| Routing and scheduling policy | compute-planner |
| Job/backend execution lifecycle | compute-runners |
| Corpus curation, data splits and document/shard manifests | model-data |
| Tokenizer fitting, vocabulary/normalization policy and comparison | model-tokenizers |
| Former model-training base/continued training and resume/export | model-pretraining |
| Former model-training SFT, preference and reward adaptation | model-posttraining |
| Objective answer verification and generic verification execution | verification-runtime |
| Teacher/task/response eligibility and preference construction | model-distillation |
| Model math/configuration, forward/generation/cache and weight compatibility | model-architectures |
| Generic artifact resolution/transfer/cache/byte integrity | research-artifacts |
| Former model-inference endpoint loading/lifecycle and raw telemetry | model-serving |
| Former model-inference workload/metric aggregation and comparisons | inference-benchmarks |
| Bounded model-research candidate sequencing and promotion policy | research-controller |
| Educational ML implementations or reusable environment dynamics | ml-foundations or rl-environments according to semantics |
| Reusable evaluation/scoring or prompt-improvement behavior | open-evals |
| Study-specific integrated configurations and reports | Lab |

Repository identity and Git history are preserved for model-training to
model-pretraining and model-inference to model-serving. Verify the repository ID
and recorded commit; URL redirects alone are insufficient if a former name is
ever reused.

The model pair relocation records are `docs/sources/repository-expansion-map.json`
at their selected revisions. Model-data's tokenizer split records
`docs/sources/tokenizer-boundary-map.json`. Economics retains its extraction
records under `docs/sources/`. Resolve all references at the manifest/alias
registry's exact selected revisions, including unmerged review branches.

## Integrate and verify

4. Export one coherent change per owner on a new branch. Inspect actual imports,
   inputs/outputs and behavior when a recovered file spans several responsibilities;
   filenames alone do not decide its destination.
5. Adapt interfaces and declared dependencies. Keep competing implementations
   and negative results available; do not overwrite a current owner with an
   unexamined recovered copy.
6. Link cross-repository PRs, verify each changed component independently, then
   update Lab's pins and affected installation/integration checks. A new source
   path or green prior receipt does not prove a changed combination.
7. Record recovered revisions, old/new paths, hashes, decisions, tests, failures
   and unresolved artifacts. Preserve scientific failures and exact study inputs.
8. Retire temporary recovery copies only after unique source/history/artifacts
   are verified preserved. Recovery does not authorize private-data publication,
   paid jobs, releases or broad cleanup.

Future reusable work starts in its canonical component home. Lab changes when
integrated configurations, compatible combinations or shared study reports change.
