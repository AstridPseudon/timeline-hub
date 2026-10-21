# App producer central23671 first-body diagnosis

## Result

**UNKNOWN; no App fix.** The only preserved central attempt failed before any
producer ownership action. No selector, timeout, readiness, fixture, source,
writer, or route behavior was changed.

## Exact source and result

- App source: `/home/user/work/wt/ap2-m2-producer23671-first-body-cause-0748`
- App HEAD: `6b0267c62aa8773132f1496d5014279e6c1edf61`
- App tree: `c1ac3383624322ae8d67b10dee36965670d91cd7`
- The only worktree commit is the inherited prior correction importing
  Playwright `expect` in the helper; it is not revisited here.
- Central result:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-helper-expect-import-0717-ap2-m2-producer-import-approved-one-case-0741-actual-64e7befb48c89f33-integration-1021074320-23671`
- Preserved central log: `log.txt`; request packet: `request`; status:
  `fail`. It ran exactly one collected case, with no retry.
- Failure: `tests/e2e/local/producer-ownership-current-pin.spec.ts:92`,
  `getByTestId('transcript-lane-chip')`, expected `2`, received `0` after 5s.
  The lane itself had already passed the visibility assertion at line 89.
- The log advertises `error-context.md` and `trace.zip` under the central
  `/tmp/tla-RraW8S/.../browser-output/...` path, but the central runner removed
  that temporary directory. No DOM, request-response, or trace artifact for
  the failing page remains.

## First causal path traced

1. `tests/e2e/local/support/producer-ownership-current-pin.ts:91-214`
   publishes the dedicated timeline. Its persisted bundle contains the same
   schema/provenance as the existing Main fixture:
   `astrid.transcript_segment/v1`, `source_seconds`, asset
   `current-pin-speech`, and intervals `[0,2]`, `[2,4]`, `[6,8]`.
   The media carrier is `current-pin-speech-carrier` at timeline `8`, with
   `from: 0`, `to: 4`, `speed: 1`. Therefore the first two source items should
   project to `[8,10]` and `[10,12]`; the `[6,8]` item is correctly outside the
   carrier and should be omitted.

2. Runtime/App load plumbing is present in source:
   `src/integrations/runtime/dataProvider.ts:929-943` parses and returns the
   stored bundle; `src/tools/video-editor/lib/timeline-data.ts:631-642`
   passes `loadedTimeline.bundle.itemsBySchemaRef` into timeline assembly.

3. The expected assembly is present in
   `src/tools/video-editor/data/typed/assembleDataLanes.ts:126-156,205-233`.
   Persisted items enter the source pool, then are remapped to every matching
   resolved media clip. `src/tools/video-editor/data/typed/transcriptProjection.ts:25-36`
   applies the carrier intersection and predicts exactly the two occurrences
   above.

4. The route’s lane plane is the next boundary:
   `src/tools/video-editor/data-kinds/useDataLanes.ts:92-140` selects either
   `base.resolvedConfig.clips` or `playedTimelineClips(...)`, then assembles
   the lane from the base source items. The current source also allows the
   played-shot projection to replace the direct fixture clips when
   `playedShotComposition` is active (`src/tools/video-editor/lib/timeline-shot-summaries.ts:11-54`).

5. Rendering is not the selector mismatch: the current Main renderer emits
   `data-testid="transcript-lane-chip"` for every item it receives at
   `src/tools/video-editor/dev/transcript-lane/TranscriptLaneView.ts:115-132`.
   A count of zero therefore means the failing artifact does not show whether
   the items were absent before rendering or were excluded from the mounted
   item window.

## Main comparison

The frozen Main comparison used by the prior report is object
`860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree
`ea4eabb8eb469df63fd1d515f84982d85b2f14cc`. Its existing transcript-lane
producer is present and unchanged for this boundary. The normal fixture in
`tests/e2e/local/support/harness.ts:806-834` uses the same bundle contract and
registry shape, with three source windows `[0,2]`, `[2,4]`, `[4,6]` and a
carrier at timeline `5` from `0` to `6`; its lane expectation is three
occurrences. The current fixture deliberately selects a later window at
timeline `8` and expects the two in-window items.

Main’s producer action sequence (minimal `clip.add` followed by ordered
`clip.update`) is a later action boundary. This case fails at line 92 before
that producer is invoked, so the Main producer’s carrier/action behavior is
not a causal explanation for central23671’s first failure.

## Evidence limit and required next evidence

The preserved request/log prove the failure and the fixture/source contract,
but cannot distinguish these live boundaries:

- bundle missing from the loaded timeline data;
- direct carrier clips replaced or omitted by played-shot projection;
- source-to-clip assembly producing no views; or
- views existing but being absent from the initial virtualized item window.

The next run must preserve `error-context.md` and `trace.zip` before cleanup,
or capture one read-only diagnostic snapshot at `useDataLanePlane`/lane paint
containing: loaded bundle item count, base clip count, lane clip count,
assembled transcript view count, and renderer item-window count. That evidence
is needed before any own-path defect can be proven. No retry was performed by
this worker.

## Tests and live callers

- No browser, build, daemon, socket, actual run, full suite, or test-service
  submission was performed by this worker, per task constraints.
- No targeted test was run because no correction was proven.
- Live callers changed: **none**. No product or test source was edited.
