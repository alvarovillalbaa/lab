# Migration sources

Last updated: 2026-11-10

[repository-split-map.json](repository-split-map.json) inventories every file at
Lab revision ba67e510bab2703b1042993744ce099490221c1f, with original SHA-256 and
canonical destinations. The original July main and both October documentation
commits remain in Git history.

pre-split/ contains exact original documents moved with git mv. Their relative
links, old layouts, TODOs, and historical completion/provider statements are
frozen source material; current instructions are in the root README,
architecture, and component repositories. Some historical relative links target
paths that moved to another repository. They are not current navigation.

Source, test, and template copies in component extraction commits preserve the
original bytes. Later packaging commits adapt imports, add public interfaces,
normalize whitespace, and record current scope. No damaged-laptop work or
uninspected external provider documentation was ingested.
