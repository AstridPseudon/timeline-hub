# Parent-media matched-proof preflight

## Result

Added only the test-local source guard `scripts/testing/current014-parent-media.mjs` and its unit test. It composes no product code and does not run the real gate. The guard requires the exact reviewed units, exact final App tree, clean source, and private dependency paths before optional Playwright collection is allowed.

## Exact approved source tuple

- Current App driver: `780c502368cb6eb379cf3848af7009067c7cd744`, tree `8eed52bb7f8555c7765a8b485e00920bbf906639`.
- Existing 622 File/media evidence source: `6221b114004e3f807e32fcf7849762514f72382a`, tree `ce6deafa32593f3791cf64b67b7b67fe9f64fe96`; the current 780 driver is the exact current evidence-driver source checked by the proposal.
- Reviewed current delivery: `2fb03f7e2a8d70ca552c6417387f03e81686791f`, parent `780c502368cb6eb379cf3848af7009067c7cd744`, tree `ffbe469ea211df1de3f5ecf57075451ce41c14f5`, carrying approved row `6c3d53a281ea326fe274a9d082f5a1e7a3489300`, tree `0b8cfa7981eb357cf66347daf5042337079247fb`.
- Independently approved HOME construction: `32e997454b76378ba04505f894cd60fcddfe95b6`, tree `c16379e633e922790206d90d284dadab34c8256b`, with only the reviewed `useTimelineState` and history-authority test paths.

The current worker HEAD contains 780, but neither `2fb03f7e2` nor `32e997454b` is an ancestor of this worker HEAD. Therefore this is a source-readiness proposal, not a false ready/gate claim. The manager must compose those exact commits (or an exact equivalent whose guarded blobs and ancestry are demonstrably identical) before running it.

## Guards included

- Exact delivery/construction/driver SHA and final App tree; clean-tree and exact blob checks for every approved delivery, HOME construction, and current driver path.
- Original evidence wrapper markers: evidence-first trap, `record_evidence`, `evidence_recorded=1`, cleanup `rm -rf -- "$run_root"`, and the exact `M2 real mounted manual video drop` selector.
- Existing public13 Composition archive SHA `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, exactly 77 safe regular files.
- Runtime producer manifest SHA `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`, artifact version `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`, schema SHA `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, and exactly 75 artifacts.
- Private node graph rejection of the shared App `node_modules`, private `.bin/vite` and Chromium ownership, Node+Vite `--version` check, distinct short/child TMPDIRs, and exact one-test Playwright collection. No install, browser, request-test, or full suite was run.
- The 622 original reload/lostACK/restart/exactretry/guardedundo/raw/order/zeroLegacy assertions remain in the reused driver; this worker did not duplicate or rewrite them. No `afterClipId`, new operation, or Runtime hold-policy behavior was introduced.

## Exports and live callers

New test-local exports are `PARENT_MEDIA_DELIVERY`, `PARENT_MEDIA_CONSTRUCTION`, `PARENT_MEDIA_DRIVER`, `PARENT_MEDIA_RUNTIME`, `PARENT_MEDIA_PUBLIC13`, `PARENT_MEDIA_ROW_TESTS`, `readParentMediaInputs`, `checkParentMediaSources`, `checkParentMediaDependencies`, `collectParentMedia`, and `runParentMediaPreflight`. No product export or live caller was changed by this worker.

The reviewed delivery's unchanged live-call chain is `handleFileDrop` (`external-drop-utils.ts`) -> `dispatchTimelineDrop` (`useExternalDrop.ts`) -> `useTimelineState.ts`; `useAssetManagement` remains wired through `installedTimelineHostServiceHooks.ts`, `timelineHostServiceHooks.ts`, and `useTimelineState.ts`, and consumed by external drop and `usePinnedShotGroups`.

## Verification

Passed:

```text
node --check scripts/testing/current014-parent-media.mjs
node --check scripts/testing/current014-parent-media.test.mjs
node --test scripts/testing/current014-parent-media.test.mjs  # 3 passed
node_modules/.bin/eslint --no-cache --max-warnings 0 scripts/testing/current014-parent-media.mjs scripts/testing/current014-parent-media.test.mjs
git diff --check
```

## Exact dependency and ready command

After the manager composes the two exact App source commits into a clean final tree, set the private checkout, private Node/Vite, private Chromium/Playwright, and private short/child TMPDIR paths from the existing normal014 source wrapper, then run from the final App root:

```sh
TIMELINE_PARENT_MEDIA_PREFLIGHT=1 \
TIMELINE_PARENT_MEDIA_COLLECT=1 \
TIMELINE_PARENT_MEDIA_APP_TREE="$(git rev-parse HEAD^{tree})" \
TIMELINE_PARENT_MEDIA_DELIVERY_SHA=2fb03f7e2a8d70ca552c6417387f03e81686791f \
TIMELINE_PARENT_MEDIA_CONSTRUCTION_SHA=32e997454b76378ba04505f894cd60fcddfe95b6 \
TIMELINE_PARENT_MEDIA_DRIVER_SHA=780c502368cb6eb379cf3848af7009067c7cd744 \
node scripts/testing/current014-parent-media.mjs
```

The one authorized actual gate, only after this command reports source ready, is the existing `ap2-m2-parent-retained-evidence-real-gate` central suite. This worker intentionally did not request it.
