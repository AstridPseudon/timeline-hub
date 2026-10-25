Implemented the native Undo oracle correction.

- Source base: `74051303cb398b80fa881488ce8851f08343c970`
- Changed:
  - `three-products.p2-elements-assets.spec.ts`
  - `support/p2-elements-assets-receipt.test.mjs`
- Enforces native `timeline.inverse` with `merge: "fields"`, `reads: []`, exact command/step envelopes, authoritative reply metadata, receipt identity, history, and undo records.
- Preserved all `doc.patch` atomic/nonempty-patch assertions.
- Added 12 malformed native-envelope controls.

Tests:

- Node20 receipt/native controls: 4 passed.
- Media-import controls: 3 passed.
- TypeScript check under `/home/user/work/.app-tsc.lock`: passed.
- Scoped ESLint: passed.
- `git diff --check`: passed.
- Semantic oracle was not runnable because `@astrid/packs` is unavailable in the worker environment.
- Browser/service qualification was not run per task constraints.

Commit message written and `DONE` marked. No product behavior changed; the prior terminal NO-GO remains unaltered.