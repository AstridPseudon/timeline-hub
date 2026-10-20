# Refreshed root: reviewed single-parent native split port

Completed the bounded source task on `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c`. Applied only the cumulative reviewed delta `c866da88 → 2e9ea4cbf340bc7fa091129e9e5f1603c5bbb030` (d111 primitive, 1a2 ingress, 2e9 shared native collection preflight). Restored exactly the two approved CORS files from `7bb885b63`, absent from this base. No KEEP or integration/release approval is requested.

## Scope, source parity and decisions

The exact allowlist is **18 files**, rather than 17: 16 split paths plus the two approved CORS files. Whole old-c866 source was not imported. `git apply --check` accepted the reviewed split patch against this refreshed base, followed by applying that patch without Git index/ref operations. No other operation, None/PARAM/delete/autoport/cohort dependency, Runtime/schema/generated/package change or root renderConfig field was added.

- Eight of ten split product files are byte-equal to the reviewed tip. The two exceptions are `useTimelineState.ts` and `useTimelineState.types.ts`: their only edits from this refreshed base add the reviewed split port/import/dependency wiring; their newer MAIN mobile, geometry, no-mode, render/download and other surrounding code stays intact. Two imported tests, the Python verifier and golden are also byte-equal to the reviewed tip. Exact path hashes/parities are in `notes/audit.json`.
- Both CORS files are byte-equal to `7bb885b63`; the helper handles configured HTTP(S) gateway origins and the unchanged managed-object predicate. Direct tests retain custom/blob/data/signed/protocol-relative/other-origin behavior. No auth or provider change.
- Kept the reviewed conservative known single RAW-parent cohort. The session calls the same `parentClipSplitRows` as native capture, including divergent mirrors; no duplicate mirror policy. Opaque `app.canonical` is authored data, never ownership authority. Group/multi/occurrence/unsupported positive paths retain their existing writers. Once capture starts, errors remain visible with draft retained and no snapshot fallback.
- The existing authoring ID seam reserves one right ID before preview; exact native source window/time/speed/rational-fps capture, full guards, created identity, and native left/right row preview flow through the existing prepared map, capture/finish/submit, session and durable outbox. Selected/context-menu/playhead/SDK hook ingress stays on that shared path for supported inputs. Imported duplicate invocation/finish/submit, abandoned capture, unmount and recovery cases are intact. These are mounted hook/session tests, not real browser events.
- Added four cases in the two imported split test files: unknown-ACK A followed by split B and an ordinary move suffix C, with explicit retry and reload variants; B capture before A ACK and completion afterward without recapture; and mounted A/B retaining their local draft while an ordinary snapshot suffix is visibly refused. They assert no append-triggered retry, exact persisted A body/key, unchanged B/C commands/claims and dependent bases, no recapture/new IDs on recovery, local provenance and no snapshot write. The existing move policy quantizes C's requested 6 seconds to 6.006 at 30000/1001 fps; the test preserves it.
- AST comparison confirms all **47 imported test callback bodies unchanged**. Three new callback bodies expand to four new cases. The existing helper now dispatches move previews/execution as well as split so the mixed suffix test uses the established recorder and compiler. No existing passing behavior was weakened or marked failing.

## Exact allowlist and size

Against the assigned root: **+4,486/-39**, net **+4,447** lines. Changed product paths only: **11 paths, 3,949 → 4,554 lines, +644/-39, net +605**. Tests/verifier/golden contribute +3,842 lines, including the unchanged reviewed 2,524-line golden. This is a changed-path census, not the entire App Timeline core or the four-repo target.

| Path | Added | Removed |
| --- | ---: | ---: |
| `src/shared/lib/media/mediaCrossOrigin.test.ts` | 30 | 0 |
| `src/shared/lib/media/mediaCrossOrigin.ts` | 18 | 6 |
| `src/tools/video-editor/commands/clipSplitCapture.test.ts` | 463 | 0 |
| `src/tools/video-editor/commands/clipSplitCapture.ts` | 357 | 0 |
| `src/tools/video-editor/commands/clipSplitGesture.test.ts` | 72 | 0 |
| `src/tools/video-editor/commands/clipSplitGesture.ts` | 132 | 0 |
| `src/tools/video-editor/commands/commitSession.split.test.ts` | 355 | 0 |
| `src/tools/video-editor/commands/commitSession.ts` | 67 | 1 |
| `src/tools/video-editor/commands/fixtures/clip_split_parity.py` | 23 | 0 |
| `src/tools/video-editor/commands/fixtures/recipe_m2_clip_split.json` | 2524 | 0 |
| `src/tools/video-editor/hooks/clip-editing/types.ts` | 2 | 0 |
| `src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts` | 28 | 29 |
| `src/tools/video-editor/hooks/useClipEditing.ts` | 4 | 0 |
| `src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx` | 375 | 0 |
| `src/tools/video-editor/hooks/useTimelineCommandSession.ts` | 16 | 2 |
| `src/tools/video-editor/hooks/useTimelineCommandsService.ts` | 15 | 0 |
| `src/tools/video-editor/hooks/useTimelineState.ts` | 3 | 1 |
| `src/tools/video-editor/hooks/useTimelineState.types.ts` | 2 | 0 |

## Root preservation

`notes/audit.json` records **40 protected files byte-identical to the assigned root**, including MAIN render/admission/download pipeline and controls, Runtime provider/client/connection/two-reading boot, auth/App root, chat/proxy, bootstrap metadata CAS, shell/mobile single portal and lifecycle tests, ShotEditor, save barrier, canonical and raw shot projections, preview composition, TrackLabel/TrackListRenderer/TimelineCanvas, package/lock and all generated Runtime surfaces. The only timeline-state edits are the reviewed split port wiring. Existing label explicit-input-intent source/tests are untouched; the passing neighbour suites cover label intent, after-ACK original guards, accepted/local/cold/recovered projection, render/download, mobile behavior and shell lifecycle.

The public12 artifact remains unchanged, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. Runtime lock remains the **development-only 0.2.9 source DTO** producer `94114269d1ce23ab3224d7eca5a85138ce2b5fed`. This work does not qualify a current safe Runtime release or matching deployment pair. No new render-facing config field, root render clock policy, package pin or download owner was introduced.

## Exact verification

Working directory: `/home/user/work/wt/app-m2-refreshed-split-source-port`. Node 22.22.0, Vitest 4.1.5, public Composition 0.0.12, React 18.3.1, Remotion 4.0.509. During verification only this worktree's own `node_modules` symlink pointed at the pre-existing read-only `/tmp/app-coherent-deps12/node_modules`. Shared dependency files, links and caches were not changed. Every Vitest invocation used runner config loading, disabled caches and one worker. The preload only supplies `__dirname` for the repository's existing config; no product/bundler configuration was edited. The original `/home/user/work/app/node_modules` link is restored before handoff.

```sh
N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-split-source-port/notes
node --require "$N/runner.cjs" node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/clipSplitCapture.test.ts \
  src/tools/video-editor/commands/clipSplitGesture.test.ts \
  src/tools/video-editor/commands/commitSession.split.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx \
  src/tools/video-editor/commands/clipMoveCapture.test.ts \
  src/tools/video-editor/commands/trackLabelCapture.test.ts \
  src/tools/video-editor/commands/trackLabelGesture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/commands/authoringBundle.test.ts \
  src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts \
  src/tools/video-editor/commands/authoringBundle.sharedOpaqueRemap.test.ts \
  src/tools/video-editor/commands/semanticGestures.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/hooks/useClipEditing.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx \
  src/tools/video-editor/lib/timeline-patch.test.ts \
  src/tools/video-editor/components/TimelineEditor/ClipAction.test.tsx \
  src/shared/lib/media/mediaCrossOrigin.test.ts \
  src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx \
  src/tools/video-editor/hooks/useRenderState.test.tsx \
  src/tools/video-editor/hooks/useTimelineRenderRequest.test.tsx \
  src/tools/video-editor/components/TimelineRenderControls.test.tsx \
  src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx \
  src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx \
  src/tools/video-editor/components/TimelineEditorShellCore.test.tsx \
  src/tools/video-editor/lib/mobile-interaction-conformance.test.tsx \
  src/tools/video-editor/data/canonicalCompositionState.test.ts \
  src/tools/video-editor/data/shotCompositionProjection.test.ts \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx \
  src/integrations/runtime/dataProvider.test.ts \
  src/integrations/runtime/opaqueRootWriters.test.tsx
```

**PASS, exit 0: 38 files / 1,551 tests**, 110.07 seconds. Full output: `notes/targeted.log`; exact file list: `notes/targeted-files.txt`. This is a bounded split-and-neighbours selection, not a full suite. No central full-suite request was made.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python src/tools/video-editor/commands/fixtures/clip_split_parity.py
```

**PASS, exit 0: 1/1 native split command, complete record, authored after, inverse and redo verified**. Read-only Agent source head at execution: `5430a9719542880ddf295ae0acd181270aac42ac`. `notes/native-parity.log`. Python bytecode writes disabled; shared venv untouched. This is a native in-process recipe check, not Runtime acceptance.

```sh
node node_modules/eslint/bin/eslint.js $(cat "$N/lint-files.txt") --max-warnings 0
node "$N/test-preservation.cjs"
node scripts/quality/check-known-failures.mjs
git diff --check
```

All **PASS, exit 0**. Lint: all 16 changed TS/TSX files, no diagnostics (`notes/lint.log`). Preservation: 47 original callbacks retained (`notes/test-preservation.log`). Failure guard: three existing authorized drag markers, zero forbidden (`notes/known-failures.log`). Whitespace check has no output. All previously existing root tests outside the two exact CORS files are byte-unchanged; imported source tests retain their bodies.

Earlier bounded split-only commands used the same flags and the four split test files. First run: 121 pass / 3 failures solely in new tests (incorrect `expect.from` assertion rather than native written-field guards, and calling explicit retry before B's append/pump settled). Second run: 122 pass / 2 failures solely in the new move suffix cases expecting unquantized 6 rather than existing 6.006. Corrected those new assertions/waiting only; no product change. Logs: `notes/split-tests.log` and `notes/split-final.log`. The final 1,551-pass run includes all four files and all four new cases.

## Limits and next steps

No source-task blockers or deviation from PLAN decisions. No full suite, build, project TypeScript check, install, browser, localhost/live socket or integration mutation was run. No actual Runtime/Agent pair, browser key/context-menu/reload, real process restart, publication-history guarded undo, decoded audiovisual parity, current release compatibility or zero legacy HTTP traffic is claimed. The App inverse case uses an in-process saved-document stand-in; native inverse parity does not close the real guarded-undo journey. Unsupported writers intentionally remain, so there is no broad editing or writer-retirement claim.

Next: orchestrator reviews this exact bounded tree, then separately authorizes qualification of the matching safe Runtime/Agent/public12/App tuple, actual browser reload/explicit retry/guarded undo and observed zero-legacy behavior for this supported cohort. Keep broader M2/Gate 5/Gate 6 closure open. The render golden and root renderConfig decision remain with their owner.

No commit/merge/rebase/checkout/push/ref deletion was run. No other worktree or shared dependency was edited. Handoff files: worker `report.md`, `commit-msg`, `DONE`; no KEEP. No build output or temporary files remain in the worktree; reproducible logs/support live under this worker's named shared notes path.
