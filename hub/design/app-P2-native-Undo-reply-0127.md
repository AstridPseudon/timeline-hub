# Report

Implemented the strict native Undo/Redo reply-oracle correction.

- `assertReplyShape` now derives label/step expectations from submitted fields.
- Preserves exact omission fallbacks (`Timeline edit`, synthesized `edit` step).
- `assertRequestV2` now validates explicit Undo and Redo envelopes.
- Added controls for native replies, fallback behavior, and malformed metadata.
- Only modified:
  - `tests/e2e/local/three-products.p2-tour.spec.ts`
  - `tests/e2e/local/support/p2-parent-oracle.test.mjs`

Tests:

- Node20 parent oracle: **16/16 passed**
- Node20 transition oracle: **3/3 passed**
- Root/app/node TypeScript checks: **passed**
- Scoped ESLint: **passed**
- `git diff --check`: **passed**
- No browser, service, full suite, build, or install run.

Source:

- Base: `3a2d6067b441b8eee683f2899ee0006615aa6fb0`
- Production Undo source blob: `4bce50f28c332c6e28aa4aed635ce80e32e3de52`
- Contract SHA-256: `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`
- Actual retained parent packet: app `5f4ce933`, agent `0d142f79`, runtime `a3cd1a32`, composition `635f4de0`

The retained parent run was old-RED at `assertReplyShape` expecting `Timeline edit` while the actual native Undo reply contained `Undo timeline`. New source-derived controls are green. Independent protected review remains for the orchestrator’s review lane.

Existing ledger: A2 traced native Undo/Redo metadata to the shared inverse producer; this correction preserves explicit labels and steps while retaining contract defaults only for genuinely omitted fields. No product behavior or refusal semantics changed.

Commit message written and `DONE` marker created.