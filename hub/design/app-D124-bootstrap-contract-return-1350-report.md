## D124 report

Implemented only the two permitted test changes:

- Fake-runtime throw control now uses the genuine retired timeline write route (`POST`), preserving 500/error/server-survival coverage.
- P2 bootstrap validation now strictly checks normal (`a17a…`) and reviewed (`6c9d…`) helper schemas, identities, bounded fields, and privacy negatives.

Tests:

- Combined requested control: **2 passed, 40 skipped**
- Normal helper P2 control: **passed**
- Reviewed helper P2 control: **passed**
- ESLint affected files: **passed**
- `tsc -p tsconfig.app.json --noEmit`: **passed**
- `tsc -p tsconfig.node.json --noEmit`: **passed**
- `git diff --check`: **passed**
- Protected original `*.spec.ts` files: unchanged
- Frozen R4 reference: all four candidate paths absent

No Runtime, product source, fixture semantics, browser, full suite, or original gate changes. No blockers.