Blocked on the underlying cause; no product or test changes made.

The actual element failure is at `three-products.p2-elements-assets.spec.ts:390`: the dialog’s `applied` status is absent after **5000 ms**, while `Applying…` remains disabled. No missing-head refusal appears. Request/reply assertions, parameter ownership, canonical checks, reload and undo were not reached.

The mounted control differs materially: it supplies a plain provider object with mocked basis/identity/asset reads and binds production `RuntimeDataProvider.commitTimeline`. The actual page uses a `RuntimeDataProvider` instance and the native fixture. The retained snapshot cannot distinguish admission refresh, owner/session readiness, capture/flush/transport, or subsequent query invalidation.

Actual preflight records connected/fresh-settled-owner observations, but lifecycle diagnostics are `UNKNOWN`; they do not establish the original element case’s state.

Focused verification:

```bash
NODE_OPTIONS=--import=/tmp/w-34c7cc72bc/preload.cjs \
/opt/node20/bin/node node_modules/vitest/vitest.mjs run \
--config /tmp/w-34c7cc72bc/current.config.mjs --configLoader runner \
--no-cache --maxWorkers=1 --no-file-parallelism \
src/tools/video-editor/contexts/VideoEditorProvider.staging.test.tsx \
src/tools/video-editor/runtime/element-adapter.test.ts \
src/tools/video-editor/runtime/admitted-elements.hosted.test.ts
```

**3 files, 32 tests passed.** `git diff --check` passed; worktree remains clean at `9b810408cc`, tree `9a37265f0286`. Existing 690-test qualification was reused; no full suite, browser, backend or original journey rerun.

Separate unreached oracle mismatch: original `assertRequestV2` forbids `reads`, while the mounted catalog witness requires them. This belongs to the Proof/P2 oracle owner and does not explain line 390.

Recommendation: producer0648 should supply safe same-case phase/owner/outbox observations locating the pending await before any repair. Commit message and `BLOCKED` marker written.