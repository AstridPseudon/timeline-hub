# MAIN17 Root013 and captured touch labels

Source-only port complete; no integration mutation or merge request. The approved public12/normal013 Root and final wrapper delta from `6ff21cac9` to `cee35da4b1ed653db50dd9d5c26693fab00f04ad` is composed onto refreshed MAIN17 with the current server proxy.

## Exact source

- Worktree: `/home/user/work/wt/app-m3-main17-root013-label-port`, branch `tl/app-m3-main17-root013-label-port`.
- Base HEAD: `751f7703d22f0e8026e2926f93f64d69c65212fd`; base tree `3340e128af4dd8fe79a8fe1016b23666c6ea8eb5`.
- Approved input: `cee35da4b1ed653db50dd9d5c26693fab00f04ad`, delta against `6ff21cac9`.
- **Final source tree: `96605f2a46c49fcf96cd12ca3679014f00ae28de`**, excluding this ignored design report. Computed with Git blob/tree hashing in memory, without index/object/ref writes; the same calculation reproduces the base tree. 172 changed paths: the approved 171-path delta, with MAIN17 reconciliation, plus one new production rename test file.
- `notes/source-audit.py` and `notes/source-audit.json` retain the complete changed-path allowlist, source identities and preservation assertions. No extra nonignored untracked source exists.
- MAIN17 `17e46de99b7cef52fe494de1703a9865a8d4be24` is already an ancestor of HEAD (`git merge-base --is-ancestor 17e46de99 HEAD`, exit 0).

## Reconciliation and preserved behavior

Five existing files need combined source: `TrackLabel.tsx`, `TrackListRenderer.tsx`, `TrackListRenderer.test.tsx`, `TimelineCanvas.tsx`, and `TimelineCanvas.test.tsx`, all under `src/tools/video-editor/components/TimelineEditor/`. Every other approved path equals the approved bytes, except the shared Vite config's clean three-way combination with the existing server proxy. All unrelated tracked paths equal base.

The touch TrackSheet receives the same `nameInputProps`, captured finish callback, draft and error lifecycle as the desktop name input. Focus captures before typing. Polls, ACKs and changed callback props never replace that original capture. A clean focus releases without submitting; typing away and back submits explicit original-value intent. Empty string remains `{values:{label:''},clear:[]}`; explicit clear remains distinct in the native capture/gesture tests, with no invented clear UI.

MAIN17's immediate detached presentation callback contract remains. Mounted native editing uses `handleTrackLabelEditStart`, not the popover's label patch path. Capture/submit refusal leaves the typed draft and visible reason, and retries use the original command. Touch errors render inside the open sheet and remain visible beside the row after closure. Closing a focused sheet finishes once; normal blur followed by close does not retry a refusal twice. A stable input ref also finishes a dirty focused input removed without blur, using the latest finish function and original capture. Clean close releases capture before the next edit.

Both `onAddTrack` and `onTrackLabelEditStart` survive Canvas/TrackListRenderer/row forwarding and memo equality. MAIN17's actual TrackSheet, shared settings, add video/audio, confirmed delete, no-Text shell and tap-to-release Move/Trim behavior remain. The four MAIN17 paths outside the reconciled set (shell source/test, inspector, mobile-sheet constant) are byte-equal to base. MAIN17's existing positive tests are retained; focused neighbors passed.

The six server paths are:

- `config/vite/runtimeProxy.ts`
- `config/vite/vite.config.ts`
- `scripts/dev-local-workspace.mjs`
- `scripts/runtime-discovery-proxy-operation.test.mjs`
- `scripts/runtime-discovery-proxy.d.mts`
- `scripts/runtime-discovery-proxy.mjs`

Five equal current `35820a603` bytes. The shared `config/vite/vite.config.ts` equals a clean three-way merge of base/current server and the approved package-alias removal; existing operation transport/admission/CORS code is preserved. All seven `three-products.spec.ts` journeys and their approved helpers/config are byte-equal to cee35da4. Provider parity source is also unchanged. No renderConfig, cap-policy adjustment, nativeNone/PARAM/automatic requesting or browser-host cohort was added. The separately escalated exact single-occurrence cap mismatch remains outside this port.

## Pins and dependencies

- Normal Runtime producer: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, producer tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Client/contract: `workspace.v1`, `0.2.13`.
- Schema: `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`.
- Artifact: `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.
- `runtime.lock.json` and all three generated files are byte-equal to cee35da4. All 13 lock destinations match pinned producer bytes and hashes. Both final wrapper files are byte-equal to cee35da4.
- Public12 archive: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; 77 unique regular safe package members, all equal to the private installed package. Resolver tests verify shared React 18.3.1 and Remotion 4.0.509 peers.

Tests used `workers/app-m3-main17-root013-label-port/private12/node_modules`: read-only borrowed dependency links from `/tmp/app-coherent-deps12/node_modules`, with a private extracted immutable public12 package. Only this worktree's ignored node_modules link was redirected. It remains pointed at the retained private12 overlay for final-pair work. No install, shared dependency/venv/runtime mutation or shared tool-cache write was performed. Vitest used runner loading, `--no-cache`, a private cacheDir/TMPDIR, one worker and no file parallelism. Test scratch was cleaned; logs, private config/overlay and audit helpers are retained outside the repo. No build output or temp files remain in the worktree.

## Old/new expectation pairs

Only the staged 44f Agent-only/no-capture expectations were superseded. MAIN17 positives were not rewritten.

| Staged old expectation (each phone/tablet) | New MAIN17 positive |
| --- | --- |
| `keeps %s track selection agent-owned without starting label capture` (TrackListRenderer) | Retain MAIN17's real sheet opening/selection/add/delete tests; extend captured-name tests to the actual sheet input, with focus capture, remote label changes, original guards, explicit restored value, empty input, capture/submit refusal and retained draft. |
| `keeps %s track selection agent-owned without forwarding label capture` (Canvas) | `forwards the phone/tablet name edit through the canvas and memoized row`, asserting selection, actual sheet, capture, delayed finish, rename and Add video forwarding. |

The historical c866 cases named `captures the phone/tablet edit before typing and retains it across a remote label change`, `submits an empty phone/tablet name on blur as a value`, and `keeps phone/tablet input and a visible reason after command refusal` now have new passing counterparts through MAIN17's real TrackSheet. The two historical Canvas forwarding cases likewise have real-sheet counterparts. This is new MAIN17 evidence, not a retrospective pass for the removed c866 controls. Desktop assertions remain and run alongside phone/tablet.

`TrackLabel.command.test.tsx` additionally mounts the production `useTimelineTrackManagement` callback with real `captureTrackLabel`/`finishTrackLabel`, proving native original guards, opaque preservation, clean release/recapture, Unicode/empty/restored intent, capture/submit refusal, and focused close/unmount behavior. Only the final session handoff is spied; no Runtime acceptance is implied.

Only the three original `useClipDrag.test.tsx` `it.fails` markers remain; the whole file equals base. No new fail/skip/todo markers were added.

## Exact verification

All commands ran in the assigned worktree. `O` denotes the orchestration root and `W=$O/workers/app-m3-main17-root013-label-port`.

Final focused command: `bash "$W/notes/run-focused.sh" > "$W/notes/focused.log" 2>&1`, exit 0. **36 files passed; 1,165 passed / 3 original expected failures (1,168 total)**, 129.44 s. Exact script contents:

```sh
#!/bin/bash
set -eu
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W="$O/workers/app-m3-main17-root013-label-port"
env TMPDIR="$W/notes/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "$W/notes/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
 src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx \
 src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx \
 src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx \
 src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.test.tsx \
 src/tools/video-editor/components/TimelineEditor/TimelineEditor.test.ts \
 src/tools/video-editor/components/TimelineEditor/ClipAction.test.tsx \
 src/tools/video-editor/components/TimelineEditorShellCore.test.tsx \
 src/tools/video-editor/components/TimelineEditorShellToolbar.test.tsx \
 src/tools/video-editor/components/TimelineCommandRecovery.test.tsx \
 src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx \
 src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx \
 src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts \
 src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
 src/tools/video-editor/hooks/useTimelineOps.test.ts \
 src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
 src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
 src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
 src/tools/video-editor/hooks/useClipDrag.test.tsx \
 src/tools/video-editor/commands/trackLabelCapture.test.ts \
 src/tools/video-editor/commands/trackLabelGesture.test.ts \
 src/tools/video-editor/commands/commitSession.test.ts \
 src/tools/video-editor/commands/commitOutbox.test.ts \
 src/tools/video-editor/compositions/vendoredTimelineCompositionAliases.test.ts \
 src/tools/video-editor/compositions/installed-themes.test.ts \
 src/tools/video-editor/compositions/playerEvaluation.test.ts \
 src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx \
 src/tools/video-editor/compositions/TimelineRenderer.test.tsx \
 src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
 src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx \
 src/tools/video-editor/compositions/AudioTrack.test.tsx \
 src/tools/video-editor/data/shotCompositionProjection.test.ts \
 src/tools/video-editor/lib/mobile-interaction-model.test.ts \
 src/tools/video-editor/lib/mobile-interaction-conformance.test.tsx \
 src/tools/video-editor/lib/timeline-dom.test.ts \
 src/integrations/runtime/client.test.ts \
 src/integrations/runtime/dataProvider.parity.test.ts \
 --reporter=default --reporter=json --outputFile.json="$W/notes/focused.json"
```

This includes 27 production-component rename cases, session/outbox recovery, initial and accepted projection, opaque/history safety, explicit native clears, package registries/media behavior, MAIN17 sheet/shell/move neighbors and provider parity.

Additional final checks:

```sh
node --test --experimental-test-isolation=none scripts/testing/current013-integration.test.mjs
node --test --experimental-test-isolation=none config/vite/timelineCompositionPackage.test.mjs
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
node scripts/vendor-lock.mjs check runtime.lock.json
node node_modules/eslint/bin/eslint.js src/tools/video-editor/components/TimelineEditor/TrackLabel.tsx src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx src/tools/video-editor/components/TimelineEditor/TrackListRenderer.tsx src/tools/video-editor/components/TimelineEditor/TimelineCanvas.tsx
python3 -B "$W/notes/source-audit.py" > "$W/notes/source-audit.json"
git diff --check
```

All exit 0. Wrapper **15/15** passed; package resolver **9/9** passed; no skips. ESLint produced no warnings/errors. Source audit verifies all tracked paths against approved/current source, the pin/producer/archive identities, MAIN17 protection, unchanged seven journey bodies and original three markers. The initial two-suite rename probe passed 129/129 and the initial production probe passed 25/25; final focused results above supersede both. The audit helper was corrected for tracked symlink reads and anchored journey counting; neither correction changed product/tests.

## Remaining gates and handoff

No local source blocker. No full suite, project tsc, build, browser, localhost/live socket, actual paired Runtime/Agent acceptance/reload/restart/undo, actual seven-journey execution, rendered pixel/audio parity, owner-film or macOS qualification was run. Unit media/receipt fixtures and mocked wrapper controls do not replace those gates.

Manager next: review this exact source tree and harness commit, preserve the retained worktree/private12/producer for the final pair, bind the actual matching Agent SHA with final App TREE in the reviewed wrapper command, then run the manager-owned post-final-source project checks and central pair/browser/full qualification. Keep the cap mismatch escalation separate. This worker did not alter integration, commit, merge, rebase, checkout, push or call request-merge/request-test.

This report is copied to ORCH/design and worker/report.md. The local `design/*.md` copy is ignored by existing repo policy and excluded from the source tree hash; the manager may retain it externally or explicitly force-add it later, which would change the tree identity.
