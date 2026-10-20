# AP2-M2 ordinary hold-shape review and gate

## Decision

**Approve the bounded producer expectation conversion; central integration gate failed, so the candidate is not integration-qualified.**

Compared `17655a570f92229635092013f28d2c5025f31ef0` with `ebb762a774bd997b836947cbecc0828f797cbcfe`. The candidate changes same-track scene-marker hold members from `{ values: { hold }, clear: [] }` to exact `{ hold }`, updates the one-to-one producer expectations, and adds a regression for move + hold while retaining an existing transition.

The conversion is bounded and uses the existing generic path: exact hold is classified as supported, captured as guarded `clip.set` through `setClip`/`executeClipSet`, and paired with the existing guarded ordinary `clip.move`. The generic batch prevalidates and captures on copied authored state, preserving atomic refusal; the session still uses the normal prepared-basis/outbox enqueue path. No native timing, transition, draft, or safety guard is bypassed. Cross-track and mixed batches retain the legacy `{ track, at }` / `{ hold, mode: 'merge' }` producer shape unchanged. No shared core edit was made.

## Verification

- `npm exec vitest run --no-cache --configLoader=runner src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts` — PASS, 2 files / 60 tests.
- `npm exec vitest run --no-cache --configLoader=runner src/tools/video-editor/commands/ordinaryScalarMember.test.ts` — PASS, 1 file / 7 tests.
- `npm exec eslint -- --max-warnings 0 src/tools/video-editor/dev/scene-phase-markers/extension.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts` — PASS.
- `git diff --check` — PASS.

Central gate was requested exactly once through the service:

```text
request-test ap2-m2-ordinary-real-move-first-post-fix e2e-m2-ordinary-integration
wait-test ap2-m2-ordinary-real-move-first-post-fix-e2e-m2-ordinary-integration-1020201335-22464
```

Result: **FAIL, exit 1, 174s, 1 failed**. Chromium smoke and hosted Vite build passed, but `tests/e2e/local/three-products.spec.ts:1222` timed out with `wire.posts.length === 0` after clicking `scene-markers-move-shots`. This is a product-path failure before Runtime acceptance/retry/restart/undo, not a browser or central-service environment failure. No rerun was made.

## Unverified / next step

The central journey remains unverified beyond the first no-POST assertion. Debug the central App path from `scene-markers-move-shots` through `moveExistingShotsToMarkers`, `ctx.creative.timeline.apply`, generic capture, and outbox dispatch; then run the named central gate once on the resulting new tree.
