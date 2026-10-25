## Report — P2/A3

Implemented source-first media identity checks across parent and child registry oracles.

Cause: generation/variant IDs were derived from selection only. Now they derive from authoritative `/media-imports`, then selection is required to preserve the exact pair and closed five-field shape.

Base: `4b633d09a796f4c14a2a388c28c46dfc52b055c5`

Changed blobs:

- Spec: `54ee61cb3c6495ec481f42701c5b26bb4407a6dc`
- Helper: `b955a3b829337c1460844739f8d4fbe2740b2d96`
- Helper test: `da75f00ac541b8bd0c8dca6a32a0249f6296361f`

Checks passed:

- Node20 controls: 26/26
- Semantic + geometry Vitest: 18/18
- Root/app/node TypeScript no-emit with `--incremental false`
- Scoped ESLint `--max-warnings=0`
- `git diff --check`

Mutation coverage includes swapped, missing, extra, wrong-pair, and wrong-object identity cases. Raw ABI, manifest digest, top-level registry, config absence, closure, old assets, reload, history, and Undo predicates remain intact.

No browser/service/full suite was run. Independent diff review remains pending; I did not self-approve or merge. Commit message and `DONE` marker were created.