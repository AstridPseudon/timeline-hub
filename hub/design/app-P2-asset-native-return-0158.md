PASS — P2 native Undo oracle tightening completed.

Changed only:

- `tests/e2e/local/three-products.p2-elements-assets.spec.ts`
- `tests/e2e/local/support/p2-elements-assets-receipt.test.mjs`

Predicate map:

- Native request: removed `objectContaining`; now exact envelope, project/timeline scope, command, fields merge, empty reads, source, and step shape.
- Authoritative command: exact keys and fixed inverse fields; strict expect/authorship relationships; structured reads, selections, bindings, resolved, and created.
- Authoritative step: exact envelope, nonempty patch/dependencies, strict patch/read structures.
- History recorder: exact record fields, command/read/selection identity, write cardinality, dependencies, derived writes, and binding variants.
- Added malformed reply/history mutations for missing, extra, wrong, and empty metadata.
- Preserved document-patch atomic/no-read predicates and all asset, registry, placement, reload, legacy-route, and Undo behavior checks.

Tests passed:

- Required Node lanes: 24 passed.
- Root/app/node TypeScript checks with `--noEmit --incremental false`: passed.
- Scoped ESLint with `--max-warnings 0`: passed.
- `git diff --check`: passed.
- Protected blob hashes unchanged.

Sources reviewed included `commit-v2.md`, production `dataProvider.ts` Undo caller, author0142/reviewer0149 reports, Agent recording/inverse source, and retained original15897 output.

Existing ledger: original run15897 passed readiness but failed at the first native Undo predicate because the generic request oracle incorrectly required `merge: atomic`; no new original or browser run was performed.

Created required `DONE` marker and P2 commit message.