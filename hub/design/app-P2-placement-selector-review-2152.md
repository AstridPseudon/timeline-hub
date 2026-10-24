# PASS — D84 placement selector review

Applied the exact published patch to:

`tests/e2e/local/three-products.p2-elements-assets.spec.ts`

The correction qualifies both helper selectors with `occurrenceId`, preserving all waits, geometry, payload, ordering, reload, undo, and closure assertions.

Evidence:

- Node20 retained control: PASS — old selector RED, corrected selectors GREEN, strict sibling/wrong-occurrence/same-bytes negatives GREEN.
- D66 source-only original list: 8 tests in 3 files.
- All 8 isolated selectors: 1 test each.
- D66 neighbor tests: 22/22 PASS.
- TypeScript: PASS.
- ESLint: PASS.
- `git diff --check`: PASS.
- Applied diff byte-identical to published patch: PASS.
- No browser/service/original/full run, per hold and task restrictions.

Hashes:

- Base HEAD: `245742dc778977a8404be2d1a7bc3b8721267416`
- Base tree: `3b83bafa9ff9e4120f5596ddd99cd12a9ddbfd17`
- Patch SHA256: `9302b5346aa661ec989518a0932f98be23a638da69b0e1d240730b09444816be`
- Spec before: `c0624a04200c40acaf6866d270d9b9b9665b33173565ee709df384ddcdc0e797`
- Spec after: `413d314d5788021bd54ae29e03813bfac91e279d5e038d6108cbb3ae18fa4133`

Protected files remained unchanged. Only the target spec is modified.

The existing ledger is outside this worktree under the orchestrator’s `design/` area; the worker rules prohibit writing there. The exact D83/D84 ledger entry should record the above before/after hashes and the preserved predicate map.

Commit message written; `DONE` marker created.