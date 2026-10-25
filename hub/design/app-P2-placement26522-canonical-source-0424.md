Implemented P2/A3 strict canonical-parent correction.

- Discrepancy: `parent_revision.payload.occurrences[].shot_revision_id`, `string → string`.
- Correction derives the new pin only from the authoritative native patch, preserves all other parent fields strictly, and verifies physical shot/child identity.
- Added controls rejecting stale whole-parent, wrong-physical, sibling, and opaque mutations.
- No production code or setup/waits changed.

Tests:

- Required support controls: 3/3 passed.
- Asset receipt controls: 123/123 passed.
- TypeScript project checks: all 3 passed under lock.
- Focused spec typecheck: passed.
- Scoped ESLint: passed, 0 warnings.
- `git diff --check`: passed.

Source baseline: `1e34f8eac5e3d5a54dbba12d538a7f3bf8509b66`

Changed-file hashes:

- Spec: `3eaacef417e15d03b9f6c9b073453b6702c97020a8854c292cfe88811cdf82bb`
- Support control: `9ad099eae7684858b2a1dce0d9fd9405265b712915c7073db1635871534e7286`

Existing ledger: The retained evidence supports exactly one native authoritative parent projection; no product defect was inferred. The later `shot_revisions` assertion remains unchanged because it was unreached.

Commit message and `DONE` marker were written. Independent protected review remains.