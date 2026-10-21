# App2 M2 producer ownership carrier safety review

## Verdict

**APPROVE the bounded source repair only:** exact candidate commit `9a5e9ed6c7a9cb43ee15a721029ecd0be5612d59`, tree `d1483e3edfbc3b8b0db2615cb719c08c2902cc44`.

This approves the four-path producer repair for the compiler/reader ownership-carrier scope proven below. It does **not** approve the actual mounted-route gate, public activation, or closure of the data-safety row. The browser/Runtime-door proof remains required.

## Review basis

- Read the settled PLAN, App2 `STATUS.md`/`INBOX.md`, latest HOME App status, prior negatives report 0200, and the held safety review 0202.
- The exact repair is four changed paths only:
  - `src/tools/video-editor/dev/transcript-lane/extension.ts`
  - `src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx`
  - `src/tools/video-editor/dev/scene-phase-markers/extension.ts`
  - `src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts`
- No shared `useTimelineOps`, generic capture, timeline-patch compiler, DTO, pin, timing policy, store, writer, or public API changed.
- The diff is minimal: `168 additions / 8 deletions`; the deletions are the old unowned payload shape and expected Scene patch literals. No original positive assertion was removed or weakened.
- Existing guards remain strict: transcript operations require `managed === true` and the active `managedBy`; Scene alignment applies only to clips with the same ownership pair.

## What is proven and approved

The repair carries the existing ownership metadata through fields that the compiler preserves:

- Transcript `clip.update.app` now carries `managedBy` beside `__generated__`.
- Scene fresh-shot `clip.update.app` now carries `managedBy` in both create builders; the existing `clip.add.app.managedBy` remains unchanged for direct patch consumers.
- Focused tests exercise fresh producer output -> existing compiler -> serialized reload/reader -> second owned operation. They also deep-compare foreign-owned and user-authored clip records after the second operation.
- The repaired Scene test explicitly asserts `classifyGenericPatch(firstPatch) === 'mixed'`, retaining the existing refusal rather than bypassing it.

The original 0200 RED/GREEN evidence is retained: the two ownership negatives failed before the guards and the repaired baseline passed 492 tests. The repair adds the two reload/second-operation controls; the exact focused central run passed:

```text
8 test files, 494 tests passed
```

Command:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-ownership-active-route-repair-0210 targeted --files "src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx src/tools/video-editor/dev/transcript-lane/__tests__/fixtureProvider.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/lib/timeline-reader.test.ts src/tools/video-editor/lib/managed-object-guard.test.ts"
```

The central service reported candidate tree `d1483e3edfbc3b8b0db2615cb719c08c2902cc44`, matching the exact repair tree. The repair worker also reported targeted ESLint passing and `git diff --check` passing; I independently re-ran `git diff --check` on the exact base-to-candidate diff, with no output/errors.

Reported repair lint command:

```text
node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 src/tools/video-editor/dev/transcript-lane/extension.ts src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx src/tools/video-editor/dev/transcript-lane/__tests__/fixtureProvider.test.ts src/tools/video-editor/dev/scene-phase-markers/extension.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx eslint.strict-debt.js
# passed
git diff --check
# passed
```

The corresponding wait command was:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-producer-ownership-active-route-repair-0210-targeted-1021021546-4131
```

## Actual route status and prerequisite

Route success is **not** claimed from the direct builder/compiler tests. The active normal route still classifies these producer batches as `mixed`: generic capture supports structural `clip.add` but does not support the app-bearing/non-scalar `clip.update`, so `useTimelineOps` atomically refuses the batch. The repair intentionally leaves that refusal intact. Native mixed members therefore remain unsupported in the current pinned route.

The frozen route-preparation worker added a focused mounted-route case and support adapter, with ESLint, `git diff --check`, and Playwright collection passing (`1 test collected`). It did not run a browser, localhost, Runtime socket, or gate. Its refusal branch preserves the visible `Native patch refused` result and checks protected data; its accepted branch is only a future assertion path.

The exact actual route still needed, after the repaired source and a compatible native carrier are integrated with the normal Runtime/door/outbox cohort, is:

1. Seed one mounted `/tools/video-editor` timeline through the existing publication helper with transcript/Scene inputs plus one foreign-owned and one user-authored clip in each relevant lane.
2. Invoke the real transcript Regenerate and Scene Create/Move controls; observe the normal `/commit` request and accepted revision, or record the visible atomic refusal if the mixed native members remain unsupported.
3. On an accepted path, reload/read the raw accepted timeline and verify fresh transcript and Scene outputs retain `app.managedBy`, then perform a second owned regenerate/alignment.
4. Assert no submitted operation targets either protected ID, compare every authored field and list order byte-for-byte after each action and reload, and repeat the lost-ack retry with an identical request body.

Until that real route run exists, this is source approval only; it is not actual-route approval or a claim that the producer success path works.

## Changed live callers

No caller implementation changed. The affected live callers are:

- `renderTranscriptAsCaptions` in `transcript-lane/extension.ts` calls `buildTranscriptCaptionPatch`.
- `createShotsFromMarkers` in `scene-phase-markers/extension.ts` calls the fresh-shot builders.
- `alignShotsToTransitions` and `ScenePhaseMarkersPanel` continue to enter the existing Scene create/move paths.

## Tests not run

No browser, localhost, Runtime socket, actual gate, or full suite was run by this review. The frozen route-preparation case was collected only. No production edit was made by this review.

## Next step

Keep the exact source candidate eligible for the bounded merge review, but require the mounted real-route proof above before claiming data-safety closure or enabling the producer success path. If the route still refuses, retain and report that refusal; the next implementation prerequisite is an approved native capture member/carrier that preserves existing producer app metadata through the normal command/session path, with no new DTO, store, writer, pin, or shared-file bypass.
