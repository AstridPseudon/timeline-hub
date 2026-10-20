# App full-suite classification: root 8bd8f741

Date: 2026-10-20 UTC  
Run: `app-full-main574-public13-root8bd8f741-agent8130-w704cb468-integration-1020161424-26611`

## Result

The central test service reached a terminal result after 1,409 seconds:

```text
Test Files  3 failed | 1485 passed (1488)
Tests       13 failed | 19040 passed | 3 expected fail (19056)
exit=1; postflight_exit=0
```

The only expected failures were the three pre-existing authorized drag markers. There were 13 actual failures in three test files; no additional actual failure was found.

The nearest baseline was the prior Root7413 run: 1,478/1,478 test files passed, 18,912 tests passed, and only the same three authorized expected failures. The current run adds ten test files and has 128 more passing tests, but also the 13 actual failures listed below.

## Actual failures and classification

### 1. App bootstrap ordering: 1 failure

File: `src/app/main.bootstrap-order.test.tsx`

Failure:

```text
main entry bootstrap order > waits for extension runtime initialization before rendering the app
expected renderApp not to have been called, but it had been called once
```

Nearest source evidence: `e4b199066` changed `src/app/main.tsx` to call `initializeVideoEditorExtensionRuntime()` synchronously, then await only `initializeWorkspaceRuntimeIdentity()`. The same commit changed `initializeVideoEditorExtensionRuntime` to a synchronous best-effort analytics install with no release-config wait. The restored test still supplies a deferred promise and expects the old async contract.

Classification: one stale/restored test contract against the current synchronous extension-runtime implementation. This is an actual suite failure, not an authorized expected failure. The manager should decide whether the current synchronous behavior is settled; if so, update this test's contract without weakening the behavior assertion.

Narrow repro: the file reproduced `1 failed | 3 passed` with the private Vitest preload.

### 2. Timeline save/signature identity: 4 failures

File: `src/tools/video-editor/lib/timeline-save-utils.test.ts`

Failures:

1. `assembleTimelineData produces consistent output with the resolved-config signature`
2. `buildDataFromCurrentRegistry materializes rows from clip geometry while keeping soft-tag groups unchanged`
3. `repairs legacy pinned groups to soft-tag clipIds without re-projecting clip geometry`
4. `applies commands and uses inverse transactions to undo them`

All four narrow failures show the same delta: current assembled `resolvedConfig`/stable signatures contain derived `clip.label` fields, while the old expected objects do not. Examples are `video.mp4`, `audio.mp3`, `next.png`, and `asset-1.mp4`.

Nearest source evidence: `574e97f44` (`fix(gallery, timeline): the gallery opens on a tab with items; clips have readable names`) added `clipDisplayNames.ts` and `assembleTimelineData` now derives labels at `timeline-data.ts:456-476`. The four restored test blobs are byte-identical to the passing Root7413 blobs.

Classification: one integration mismatch, counted as four actual failures. The new readable-label behavior is present, but the restored identity/signature assertions were not reconciled with the label-bearing projection. This is not four independent save or inverse defects. The manager should decide whether labels are display-only and must be excluded from identity/signatures, or whether these tests should explicitly expect the new labels.

### 3. Preview projection identity: 8 failures

File: `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx`

Failures:

1. `delivers paired canonical-shot candidate geometry through project/saving, then the accepted pinned closure`
2. `keeps retained B local at its original base through prefix A acknowledgement and observed C`
3. `installs an accepted same-content config generation despite the unchanged editor signature`
4. `refuses metadata-only certification of delivered frames and clears only target notices`
5. `keeps a complete paired config labelled while an independent canonical target read is unavailable`
6. `cancels older paused command inputs and delivers the newest generation with its own label`
7. `coalesces playing command inputs on one frame without delivering the superseded acceptance`
8. `remounts across project and timeline scopes while a command generation is queued`

All eight fail at exact object-identity assertions because the delivered config now includes derived labels: `alpha-image`, `alpha-audio`, `beta-image`, and `alpha-copy-image`. The lifecycle labels and timing assertions otherwise proceed to the identity checks.

Nearest source evidence: the same `574e97f44` label projection described above. The restored preview test blob is byte-identical to the passing Root7413 blob.

Classification: one label/projection compatibility mismatch, counted as eight actual failures. No separate preview lifecycle regression is evidenced by this run.

## Exact run, limits, and preflight/postflight

The central service ran the requested existing run only; no new full request was made:

```text
npm test -- --maxWorkers=2 --configLoader=runner --no-cache
```

Preflight commands recorded by the service:

```text
node config/vite/timelineCompositionPackage.test.mjs
vitest compiledAudioSourceClock+continuousPCM.contract(+lifetime)
vitest commitSession
```

Observed preflight checks passed:

- `runtime.lock.json` verified.
- 65 pinned Astrid source files verified.
- 155 `vendor/astrid-browser` files verified.
- 20 `@astrid-public` imports verified.
- No placeholder smoke tests found.
- Known-failure audit: 3 authorized expected-failure markers, 0 forbidden markers.
- Postflight: `postflight_exit=0`; source/pins/external tuple checked.

Not run by this worker: install, build, TypeScript compilation, browser/e2e, or any extra full suite. The narrow repros used Vitest only, with `--no-cache` and the private snapshot preload; no shared dependency or cache path was written.

The first narrow command omitted the central preload and failed during Vitest config loading with `ReferenceError: __dirname is not defined`. This was an environment/setup invocation error, not product evidence. The corrected narrow commands used the same preload as the central runner and produced the classifications above.

## Source and package hashes

Current source tuple required by the run:

```text
App expected SHA:       ea38656fe62950440b36cafee780698cff2c3f9c
App tree:               8bd8f741f7c8b28b8682aa960a658417f70c8522
Test snapshot head:     ba4215d03205f18fc22aca4fe2ca0f35de5fab98
Agent SHA/tree:         8130a401bf44a518d5a40ae274d398b8c560be55 / 236c3e57e0265c52b81ba8085de3193026176bff
Runtime SHA/tree:       2c4ac180c2220bdad966bc01e95ad230e99ce26a / 7ab412cc4bcbe517efcfa806e092336390312e18
Composition archive:    0.0.13, 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738, 58,477 bytes
Astrid public bundle:   680d1aa4f1f9576d65a603472f1dd7fc0ae9ccd1 / tree 07ce61f24ec38a1a60c4a981b6bd666f4971bd67
```

Current App file hashes recorded before the run:

```text
package.json:    a2ac9c9d946bd2d0ee1b2283154d94adad926f6282fff4417aeaf7520f138437
package-lock:   7f1bfcea48cef38d4c6f1163aa34190b8d5e71c9f08c7378e01a962d6696fc14
runtime.lock:   550de9dc3269380c79f44a6db4c87a5d5459058d550ae49e635a6dda809e76a2
```

The worker worktree remained clean; no source changes were made.

## Recommended next steps

Resolve the two current-main/test-restoration contract mismatches: settle the synchronous extension bootstrap expectation, and settle whether derived clip labels are excluded from canonical identity/signatures or are part of the expected projection. Then rerun the central full suite on the resulting tree. Do not reclassify these 13 failures as expected failures or weaken/delete/skip the tests.
