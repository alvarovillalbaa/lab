# Migration sources

Last updated: 2026-11-10

[repository-split-map.json](repository-split-map.json) inventories every file at
Lab revision ba67e510bab2703b1042993744ce099490221c1f, with original SHA-256 and
canonical destinations. The original July main and both October documentation
commits remain in Git history.

[repository-split-v2-map.json](repository-split-v2-map.json) inherits that frozen
inventory and routes it through the expanded product boundaries. It records
renamed identities, complete intermediate inventories, section-level owners,
exact extraction snapshots and later adapted code separately. The old map's
destination names remain historical.

With the component checkouts available, run the read-only local checker from Lab:

```sh
python3 -B scripts/check-expanded-provenance.py --workspace ..
```

The explicit workspace is recovery tooling input, not a runtime sibling import.
Missing Git objects fail without lazy fetching. This check establishes local
structural provenance; it does not prove installed behavior or laptop recovery.

pre-split/ contains exact original documents moved with git mv. Their relative
links, old layouts, TODOs, and historical completion/provider statements are
frozen source material; current instructions are in the root README,
architecture, and component repositories. Some historical relative links target
paths that moved to another repository. They are not current navigation.

Source, test, and template copies in component extraction commits preserve the
original bytes. Later packaging commits adapt imports, add public interfaces,
normalize whitespace, and record current scope. No damaged-laptop work or
uninspected external provider documentation was ingested.

[repository-split-v3-map.json](repository-split-v3-map.json) adds the verifier,
model-architecture and artifact product boundaries. V1 and V2 stay unchanged.
Run the complete chain from Lab with:

```sh
python3 -B scripts/check-product-provenance.py --workspace ..
```
