# AP2-M2 parent consumer shared-seam review

## Verdict

**HOLD.** Do not approve `tl/ap2-m2-parent-prepared-consumer-rowlocal-restore` (`b4d443057823520e956c87e8c06c2874208eff57`) or activate `design/ap2-m2-parent-prepared-consumer-shared.patch` until the three blocking seams below are fixed and covered by focused tests.

The proposed changes are otherwise scoped as intended: HOME owns the provider-bound runtime and command construction, and the shared patch applies cleanly without introducing a second editor writer. I made no source changes.

## Blocking findings

### 1. Prepared VIDEO without selection falls through to local editing

In `src/tools/video-editor/hooks/useAssetManagement.ts` (`placePreparedAsset`, candidate lines 280–288), the native branch is guarded by both `prepared.mediaType === 'video'` and `prepared.mediaSelection`. A prepared video with no required selection therefore enters the old snapshot `prepared-media` path and calls local `applyEdit`. This violates the settled unsafe-input rule: the user must see a refusal, with the draft/catalog preserved and zero local `applyEdit`.

The same branch silently returns `false` when `commands` is missing, and silently maps native `{ok: false}` to `false`. The candidate report says these are visible refusals, but the candidate source does not call `runtime.toast` in either case.

Required minimal hunk:

- Branch on `prepared.mediaType === 'video'` unconditionally.
- Refuse a missing `prepared.mediaSelection` visibly and return `false` before any local command is built or applied.
- Refuse a missing `commands` visibly and return `false`.
- After awaiting the native result, toast the bounded native error when `result.ok` is false, then return `false`.
- Add the toast dependency to the callback dependencies.
- Retain the existing local snapshot path for legitimate image/audio and other non-qualified behavior only; do not use it as a prepared-video fallback.

### 2. Promise-returning `dropAsset` callers do not all await it

The candidate widens `handleAssetDrop` to `boolean | Promise<boolean>`, but the surrounding callers still use it synchronously:

- `src/tools/video-editor/lib/external-drop-utils.ts`: calls at approximately lines 373, 479, 497, and 521 need `await` in `handleFileDrop`.
- The multi-generation helper at approximately line 630 ignores the return value; make the helper async, await the call, and propagate the boolean.
- The single-generation helper at approximately line 734 has the same issue.
- The general asset helper at approximately lines 767 and 781 returns success without awaiting the call; make it async and propagate the result.
- `src/tools/video-editor/hooks/useExternalDrop.ts`: the dispatch paths around lines 430–450 invoke the multi-generation, single-generation, and general asset helpers without awaiting them. Those dispatch calls must await the async helpers.

The current synchronous checks can treat a refusal Promise as truthy. In particular, skeleton cleanup in the file-drop path can be skipped on a native refusal, while generation paths can report success and clear/advance state without knowing whether the native command succeeded. Add focused rejected-Promise/refusal tests for each path and retain the existing positive behavior assertions.

### 3. Native placement drops caller-owned target/removal intent

The candidate native call passes only `preparedAsset`, `trackId`, and `time`. It drops `forceNewTrack`, `insertAtTop`, and `removeClipId` from `placePreparedAsset`.

Those arguments are supplied by existing callers in `external-drop-utils.ts`, including new-track/top placement and generated skeleton replacement. The native command contract in `useTimelineCommandsService.ts` explicitly handles or refuses these fields. Omitting them means a successful command can place on the wrong existing track, and a skeleton `removeClipId` can be silently lost, leaving a duplicate/ghost row. It also prevents the intended visible refusal from reaching the now-awaiting caller.

Required minimal hunk: forward the relevant arguments into `commands.addClip`, including `forceNewTrack`, `insertAtTop`, and `removeClipId` when present. If a qualified native path cannot support a particular combination, refuse it visibly and let the awaited caller perform its established refusal cleanup; do not silently discard the intent and do not fall back to local `applyEdit` for qualified prepared video.

## Checks that passed

- The candidate diff is clean under `git diff --check`.
- Candidate evidence records the focused Vitest run: `useAssetManagement.mediaImport.test.tsx` and `useAssetManagement.assetDrop.test.ts`, 17 tests passed.
- Candidate evidence records ESLint on the touched App files, TypeScript `tsc --noEmit --pretty false`, shell syntax, and the focused evidence probe as passing.
- Independently ran `bash -n` on the candidate evidence wrapper: passed.
- Independently ran the wrapper `probe`: `failuretrap probe passed: evidence copied before disposable-root cleanup`; passed.
- Independently checked `git apply --check` for `ap2-m2-parent-prepared-consumer-shared.patch` against the integration App tree: passed.
- No legacy behavior assertions were removed, skipped, or weakened in the candidate test diff. The added assertions cover native success, missing commands, and native refusal, but do not cover the missing-selection fallback, toast visibility, caller awaits, or dropped placement/removal fields.

No browser, socket, request-test, or full suite was run, per task scope.

## Positive seam review

- The native command freezes the five selection fields in the parent session capture before the sole provider verification await; the current `capture` path copies/finalizes the row, media, generation, basis, and display-head values before `getProjectVerifiedMedia` is awaited.
- The shared patch binds the provider-backed runtime to the current project and uses the existing store/command construction. It does not replace the stale-adapter, selected-track, or trim authority ports, and it does not add a second local editor mutation path.
- Existing legitimate nonfilm catalog/image/audio behavior remains on its prior path in the candidate; the required correction is specifically to prevent prepared VIDEO lacking selection from entering that path.
- The candidate evidence wrapper retains the current15 custody controls, records evidence before disposable-root cleanup, and bounds/sanitizes copied failure context. Its source pin is truthful for the currently qualified old gate (`expected_app_tree=78f3784287d78fc92677ebe5eb710d162b0f50ae`, the approved `b107...` source, with the recorded Agent/Runtime/producer pins), but it is not a qualification of candidate `b4d443057` (`985cbf81294157d1064780954bfd947c174564c2`). A new current source pin/gate is required after the consumer fixes; no gate evidence is being claimed here.

## Recommended next steps

Implement only the three minimal hunks above, add focused refusal/await/target-intent regressions while preserving all positive assertions, rerun the focused App tests/types/lint/probe, then obtain a fresh current qualified source pin before any broad integration run.

