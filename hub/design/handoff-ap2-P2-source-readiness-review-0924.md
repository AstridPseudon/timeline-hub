# Handoff: ap2-P2-source-readiness-review-0924

## Verdict

**SOURCEPREP PASS; behavior unverified and receives no credit.** Audited App
`ff2d3c1d76c454f0402e48a42335d466a853cfe1`, tree
`84634e56df1aa205405e4a9301a8e6d3bd274f6f`, against PLAN §3 P2 and C0 §§1–5,7.
No product/test/fixture/generated/lock/package/pin/ops edits were made.

## Identity

The original donor `67eda18032b6ed0f14856a9ce148fb3ba7b630c1` and current head
both contain the exact P2 blob
`45a8088fafd72a462409e444c0294e8a35682a0f`; there is no diff in
`tests/e2e/local/three-products.p2-tour.spec.ts`. Discovery lists exactly the
three original selectors at lines 564, 595, and 613:

1. `P2 mounted single parent move: v2 commit, exact field delta, reload and guarded Undo`
2. `P2 mounted transition None single: raw clear preserves opaque data/order and guarded Undo`
3. `P2 mounted transition None bulk: atomic raw clears preserve unknown fields/order and guarded Undo`

All five reviewed source commits are ancestors of the current head: move
`f2d6d62c7`, Undo `2980bbe06`, shared `7fd2a6d0c`, child placement `476033c85`,
and split provenance `e90090991`; owner merges land through `b471e733a` and
final `ff2d3c1d7`.

## Findings

- Mounted production save is `useTimelineState → useTimelineSave.localDocumentSave → timelineLocalSaveHandoff → LocalSaveSession/outbox → RuntimeDataProvider.commitTimeline → generated client`, using `/commit` and persisted authored operands.
- Mounted Undo delegates through `useTimelineHistory`/remote handoff, emits `timeline.inverse` through the same outbox, and uses `RuntimeDataProvider.undoTimeline`; no snapshot fallback is used in this branch, including after reload.
- Move read basis remains wired through `useClipDrag`/`useTimelineTrackManagement`. Single/bulk transition-None uses mounted Properties Panel capture. The original spec asserts exact intended fields, raw absence, opaque/order/sibling preservation, canonical reload, and guarded inverse.
- Old-route source proof is complete: network listener rejects non-GET legacy/composition writes, and Runtime `/commits` reads pin the head, require only `timeline.commit`/`timeline.inverse` new entries, reject extras, and assert the final head. This is not live behavior evidence until executed.
- Child/shared physical ownership remains source-bound: `getShotPlacementTarget` requires one canonical occurrence and returns `ownerRef=occurrence:<id>`, matching `timelineRef`, and a fresh destination UUID; `buildOccurrenceForkCommand` validates source/destination and uniqueness, and `forkOccurrence` uses the existing A2 outbox/session. No sibling broadcast or guessed shot identity.
- C0 v2 request/reply fields are preserved in the original helper/types: scope/base pair, API 1, commands, label, steps/patch/reads, merge, dry-run, idempotency key, accepted/merged canonical/digest/head/receipt/records/effects/bindings/dependencies/undo/history/publisher/provider/compiler. Generated failure types retain conflict/refused/invalid plus code/path/hint/suggested command. The three original tests do not execute conflict/invalid replies.

## Exact checks

- `./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.p2-tour.spec.ts --list` — **PASS, 3 tests**.
- Scoped ESLint over the original spec and mounted save/history/move/transition/placement/data-provider callers with `--max-warnings 0` — **PASS**.
- `node scripts/vendor-lock.mjs check config/astrid-cli-surface/vendor.lock.json` — **PASS**.
- `git diff --check` and exact donor diff check — **PASS**.
- Runtime lock — **PASS**: source `34eac0041b0891e9011966b39bcbd26053fde5bc`, tree `9853574865f25e08284e82ffb26c0bdecaa16a30`.
- Private Composition — **PASS**: archive SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, 80 files, package `0.0.14`, 8 declared public exports.

## Limits / next step

No browser/body, HTTP/service, localhost, live Runtime/socket, build, full, or
central test-service run. There is no behavior pass, Runtime receipt, live
`/commits` result, reload result, Undo result, or H3 credit. Farm is down;
Proof owns the later original-tour qualification. Known owner merges `0b6b5b6b7`
(JSON repair) and `11b57f63f` (newline helper) remain pending; neither was
duplicated or rerun. After owner merge, run one Proof-owned tour using only the
three exact selectors above and retain both network and Runtime `/commits`
evidence.
