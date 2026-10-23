# A4 mounted track reorder witness

Status: PASS for the requested mounted App coverage. The branch remains based at `6e04a9a9`; only the new persistence witness was added in the worktree.

## Mounted caller map

- `useTimelineTrackManagement.ts:917-938` is the actual caller. A non-no-op reorder calls the supplied `applyEdit` consumer with a `config` replacement; the test does not translate mock arguments into an intent.
- `useTimelineSave.ts:83-116, 171-211` binds that consumer to the mounted local document save when `loadTimelineCommandBasis`, `commitTimeline`, and `getRecoverableIdentity` are present. The test supplies all three plus `commitTimeline` and an IndexedDB-backed outbox.
- `timelineLocalSaveHandoff.ts:304-311` captures the canonical before/after through `session.appendDocument`, including the parent revision/content-digest root binding and the existing `Edit timeline` step metadata.
- `documentPatchIntent.ts:109-220` is exercised by that mounted append. The witness observes the resulting parent `config.tracks` `list.move`, exact `before` row, `order_before`, `after_id`, unchanged canonical wrappers, and preserved authored payloads.
- `localSaveSession.ts:152-190` is the transport join exercised by the test: it creates the registered generic `doc.patch`, v2 base pair, `steps`, `merge`, `source`, and `dry_run` request, and passes the generated idempotency key to the provider. No local executor is used.

## Old obligations -> kept/mounted witness

- Raw rows, null/false/zero values, opaque track/clip/app payloads, sibling payloads, and order: retained in `trackReorderCapture.test.ts` and additionally checked after mounted accepted adoption and refusal rollback.
- Normal reorder: newly witnessed through the real hook consumer and outbox. The request is one generic `doc.patch` with one guarded parent `list.move`, exact prior row, `order_before`, `after_id: null`, base revision/publication pair, generated key, `Edit timeline` label, and step `{id,label,intent,tags,command_ordinals,patch}` metadata.
- Accepted canonical adoption: newly witnessed; returned `r1/p1` becomes the UI head and canonical config, while opaque parent and authored payloads remain intact. The outbox accepted prefix has no remaining intents and retains the accepted result.
- Structured refusal: newly witnessed; the UI returns to `r0/p0` and original order, the structured conflict code/path/hint/message remains exposed, and the rejected durable intent retains the exact patch and post-edit canonical document.
- Malformed, missing, duplicate, foreign, lane-bearing, and stale identities: unchanged and still passing in `trackReorderCapture.test.ts`.
- Legacy same-order explicit write/record (`before === after`): unchanged and still passing in `trackReorderCapture.test.ts`.

## Honest uncovered obligation

The old capture contract explicitly records a same-order `track_order` write/record. The current mounted UI does not have that behavior: `handleMoveTrack` returns at `useTimelineTrackManagement.ts:932-935` when the calculated array is unchanged. The new mounted witness classifies this separately and asserts no provider call and no outbox intent. It does not invent a new operation, record, or changed expectation. No smallest caller correction is supported by this evidence; adding a same-order persistence side effect would be a product semantic change outside this task.

Because the current caller supplies no gesture basis for track reorder, the mounted request correctly omits declared `reads` and uses the existing `merge: 'atomic'` fallback. The test asserts this absence rather than claiming detached read metadata or parity with the legacy explicit write.

## Verification

- `NODE_OPTIONS="--import /tmp/w-e700850de7/vitest.dirname.mjs" node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/hooks/useTimelineTrackManagement.persistence.test.tsx src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts src/tools/video-editor/commands/trackReorderCapture.test.ts` — PASS, 3 files / 37 tests.
- `flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false` — PASS.
- `flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.node.json --pretty false` — PASS.
- `flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.json --pretty false` — PASS.
- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/useTimelineTrackManagement.persistence.test.tsx --max-warnings 0` — PASS.
- `git diff --check` — PASS.

No full, browser, HTTP, live-socket, dispatcher, or integration suite was run. The actual Runtime transport remains narrowly mocked at the App provider boundary, as authorized; no claim is made for live transport or same-order legacy parity.
