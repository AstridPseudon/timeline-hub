## Report

Changed only [three-products.p2-elements-assets.spec.ts](/home/user/work/wt/app-P2-placement31499-projected-oracle-0547/tests/e2e/local/three-products.p2-elements-assets.spec.ts:1208).

- Derived projected identity as `${seed3.occurrenceId}:${row.id}`.
- Reload now requires exactly one projected action and rejects the raw ID.
- Undo reload checks the same projected identity is absent.
- All request, canonical, physical/closure, history, receipt, zero-legacy, native undo, waits, and budgets remain unchanged.
- No product source, Runtime, Agent, Composition, ledger, or original test was modified.

Predicate map: actual31499 raw selector RED; source-derived projected selector GREEN by `shotCompositionProjection.ts:336-348` and existing integration expectation. Raw authored identity remains covered by canonical assertions. Duplicate identity is rejected via `toHaveCount(1)`. Wrong occurrence/sibling/same-bytes/physical guards remain in existing strict assertions; D105 independent mutation review is still required.

Tests:

- `node --test tests/e2e/local/support/p2-elements-assets-receipt.test.mjs tests/e2e/local/support/p2-placement-receipt.test.mjs` — 132/132 passed under Node 22.22.0; Node 20 was unavailable.
- Targeted Vitest integration — 10/10 passed.
- Three locked TypeScript projects (`tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`) — exit 0.
- Scoped ESLint — exit 0, zero warnings.
- `git diff --check` — passed.
- Playwright `--list` placement collection — exactly 1 test.
- No browser, original, full suite, service, build, install, or merge run.

Protected neighboring six SHA-256 hashes were identical before/after:

`93c2bf4c…`, `2b9723db…`, `50960dd2…`, `09f5e2c2…`, `54ea18f3…`, `0ec7bbb8…`.

Changed spec SHA-256: `c75baf23…` → `58b53d49…`; Git blob: `36b1e2c9…` → `45b78a95…`.

Mutation refusals: shared dependencies/caches were not modified. Vitest `--configLoader=runner` was unsupported by this config (`__dirname` failure); normal config with `--no-cache` passed.

D105 hold remains: independent citation/reverse-diff ownership and Luna protected review must complete before merge or any original run.

D83 ledger paragraph: “Actual31499 proved a bounded oracle identity mismatch: the immutable occurrence projection mounts the canonical child as `<occurrence-id>:<raw-clip-id>`, while the old reload predicate selected the raw ID alone. The correction derives the projected ID from the selected fixture occurrence and canonical child ID, preserving all authored, canonical, receipt, history, and guarded-undo predicates. No product behavior or Runtime wait was changed; browser acceptance remains held pending D105 citation and independent protected review.”

Commit message and `DONE` marker created.