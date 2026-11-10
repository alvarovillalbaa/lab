# Lab agent instructions

- Lab assembles independent research components. Read README.md and docs/ARCHITECTURE.md first.
- Check src/lab/composition.json and docs/references/component-ownership.md before implementing a feature.
- Implement reusable behavior in its owning repository. Never restore extracted source copies or import from a sibling checkout.
- Experiment configurations and integrated research reports belong here. Keep component changes and integration changes separately reviewable.
- Preserve docs/sources/pre-split and the migration map for recovered-laptop reconciliation.
- Keep datasets, checkpoints, credentials, caches, and large artifacts out of Git.
- Provider jobs, model downloads, deployment, and publication of scientific claims require their existing human gates.
- Run narrow checks for changed behavior and git diff --check. Fresh installs/builds must pass Storage Guard first.
