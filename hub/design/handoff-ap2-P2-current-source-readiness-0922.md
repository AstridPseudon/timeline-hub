# Handoff: ap2-P2-current-source-readiness-0922

## Result

**SOURCEPREP / source PASS; behavior unverified.** Reviewed actual App `ff2d3c1d76c454f0402e48a42335d466a853cfe1`, tree `84634e56df1aa205405e4a9301a8e6d3bd274f6f`. This is preparation only; no P2 behavior pass or H3 GO.

The original P2 spec is unchanged and identity-proven: `HEAD` and integrated `cffa91c93e80717cec1a4e740fae67140394eb88` both contain blob `45a8088fafd72a462409e444c0294e8a35682a0f`, from donor `67eda18032b6ed0f14856a9ce148fb3ba7b630c1`. Current owner merges consumed are move `f2d6d62c7`, Undo `2980bbe06`, shared `7fd2a6d0c`, child `476033c85`, provenance `e90090991`; current owner head is `ff2d3c1d7`.

## Original specs and mounted caller

Exact discovery command:

```text
./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.p2-tour.spec.ts --list
```

It listed exactly:

- line 564 — `P2 mounted single parent move: v2 commit, exact field delta, reload and guarded Undo`
- line 595 — `P2 mounted transition None single: raw clear preserves opaque data/order and guarded Undo`
- line 613 — `P2 mounted transition None bulk: atomic raw clears preserve unknown fields/order and guarded Undo`

Source tracing confirms `useTimelineState` → `useTimelineSave.localDocumentSave` → `timelineLocalSaveHandoff` → `LocalSaveSession/outbox` → `RuntimeDataProvider.commitTimeline` → generated client. Guarded Undo calls the same handoff and emits exact `timeline.inverse`; there is no snapshot fallback. Move keeps the singleton gesture read basis through `useClipDrag`/`useTimelineTrackManagement`; single and bulk transition `None` use the mounted Properties Panel/editing path and durable document-patch capture. Child placement binds `ownerRef=occurrence:<occurrenceId>`, `timelineRef=context.timelineId`, and a fresh destination `shot_id`, then uses the existing outbox fork path after verifying one canonical occurrence and distinct/unoccupied source/destination identities; sibling identity is not inferred or broadcast. The spec captures the full v2 request/reply/history contract, exact field deltas, raw absence/opaque/order preservation, reload, inverse, and zero new legacy writes.

## Checks and limits

- Discovery above: **PASS**, 3 listed, none executed.
- Scoped ESLint (`--max-warnings 0`) over the original spec and mounted save/history/move/transition/placement/data-provider callers: **PASS**.
- `git diff --check`: **PASS**.
- `node scripts/vendor-lock.mjs check config/astrid-cli-surface/vendor.lock.json`: **PASS**.
- `runtime.lock.json`: **PASS**, locked Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc`, tree `9853574865f25e08284e82ffb26c0bdecaa16a30`.
- Private Composition archive: sidecar/public hash **PASS**, `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`; 80 extracted files; all eight public exports imported from a private symlinked package graph.

Exact current caller blobs: `timelineLocalSaveHandoff.ts=1c6176d2abc3d06f5b27b7c391a2c22c292ea4d1`, `useTimelineSave.ts=0f888f7c843ce7f8179c70b34b373a030c00d22a`, `useTimelineHistory.ts=b0ede1df74c2ae96f20a304191617f4b7482b638`, `useClipDrag.ts=108f86f7180b882cda4356d1ed4f1e8ff7684b73`, `useTimelineTrackManagement.ts=40b12a5d0cadc282400a304efe52dd3fffb247d7`, `localSaveSession.ts=83d2166d57c05980d3bd8ebc9bbd79a37c3c5e44`, `ClipTransitionSection.tsx=72e39df2877bff03a2e986d22c55713a31755a59`, `BulkClipPanelBody.tsx=066fcc46fa4b05b6715f0edb093250abd8a16f88`, `dataProvider.ts=fea25c9f28fa617eb3cf252a0a86818ef1218be2`.

No body/browser/service/build/full/socket run. No App typecheck rerun: known JSON repair `0b6b5b6b7` and helper `11b57` remain pending owner merge, as directed. Farm is down; Proof owns the eventual one original P2 tour. Later OPS must use the existing `P2` row in `scratchpad/orch/managers/app2/STATUS.md` and these exact selectors, without adding a new tour.
