# MAIN17 refresh on current integration

Applied the exact eight-file `44f0b9ca9` → `17e46de99` delta on integration `35820a6`, retaining integration command recovery. The supplied harness merge parent is MAIN17; workers do not create commits or merge metadata.

## Exact sources

- Integration SHA: `35820a603a623e83c16a59cc397dd3079b228011`; tree `ee34b6a1b24ccb76133edc9223d5030c3be4310e`.
- MAIN17 SHA: `17e46de99b7cef52fe494de1703a9865a8d4be24`; tree `eb32d1320db5af90e706b71aea8c05c2e1eb121a`.
- MAIN17 parent: `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa`.
- Reconciled source tree, excluding this new design report: `3340e128af4dd8fe79a8fe1016b23666c6ea8eb5`. Computed with Git blob/tree hashing without writing Git objects; the same calculation reproduces the integration tree exactly.
- Intended merge parents, in order: integration SHA above, then MAIN17 SHA above. The manager must check the actual committed parents and MAIN17 ancestry after the harness exits.

## Reconciliation

`git diff 44f0b9ca9 17e46de99b7cef52fe494de1703a9865a8d4be24 | git apply --check` passed; the same diff was applied with `git apply`.

- `src/tools/video-editor/components/TimelineEditor/TimelineCanvas.tsx`
- `src/tools/video-editor/components/TimelineEditor/TrackLabel.tsx`
- `src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx`
- `src/tools/video-editor/components/TimelineEditor/TrackListRenderer.tsx`
- `src/tools/video-editor/components/TimelineEditorShellCore.test.tsx`
- `src/tools/video-editor/components/TimelineEditorShellCore.tsx`
- `src/tools/video-editor/components/TimelineMobileInspectorDialog.tsx`
- `src/tools/video-editor/lib/mobile-sheet.ts`

Six paths equal MAIN17 byte-for-byte. Only `TimelineEditorShellCore.tsx` and its test differ from MAIN17: their existing integration command recovery import/rendering, conflict handling and three recovery tests remain. All 5,903 unrelated tracked files equal integration byte-for-byte, including reviewed server proxy paths, CORS, public aliases, Composition root8, Runtime client 0.2.1 and parity code.

MAIN17 owns the touch track sheet (rename, shared desktop settings, add video/audio, confirmed delete), tapping the selected armed clip to release Move/Trim and reopen its sheet, and Gallery/Ask Astrid with no Text button. The upstream tests and behavior are retained exactly. The former touch-Agent-only track policy is superseded where MAIN17 replaces it. No additional behavior expectations were rewritten. The three original `it.fails` markers in `useClipDrag.test.tsx` and that entire file remain byte-identical to integration.

## Targeted verification

Run from `/home/user/work/wt/app-m2-main17-true-refresh`:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-true-refresh/vitest.private.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx src/tools/video-editor/components/TimelineEditorShellCore.test.tsx src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx src/tools/video-editor/lib/mobile-interaction-model.test.ts src/tools/video-editor/lib/mobile-interaction-conformance.test.tsx src/tools/video-editor/lib/timeline-dom.test.ts src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.test.tsx src/tools/video-editor/components/TimelineEditor/TimelineEditor.test.ts src/tools/video-editor/components/TimelineEditor/ClipAction.test.tsx src/tools/video-editor/components/TimelineEditorShellToolbar.test.tsx src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts src/tools/video-editor/hooks/useClipDrag.test.tsx src/tools/video-editor/components/TimelineCommandRecovery.test.tsx src/integrations/runtime/dataProvider.parity.test.ts > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-true-refresh/targeted.log 2>&1
```

Exit 0: **14 files passed; 455 tests passed; 3 expected fail (458 total)**, 65.28 seconds. The two directly changed test suites plus canvas exercise the eight changed paths; neighboring mobile policy/conformance, editor/core, track management, clip gestures, shell toolbar, command recovery and provider parity also passed. `git diff --check` passed.

The worker's private `standard8/node_modules` borrows read-only dependency entries from `/tmp/app-m2-coherent-deps8/node_modules` and contains its own extracted Composition 0.0.8 package. Archive SHA256 `93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa`, all 77 package files, React/React DOM 18.3.1 and Remotion/player 4.0.509 were verified. Vitest 4.1.5 ran with caches disabled, runner config loading, a private `cacheDir`, and one worker. No shared dependencies, caches, venvs or runtimes were written. The worktree's ignored node_modules link was restored afterward.

No full suite, tsc, build, browser, localhost suite or install was run. Real touch/browser gesture arbitration and a mounted Runtime round trip are unverified here. The manager owns the single post-batch full after the final root composition.

## Later root/mobile-label port adjustments

Compared against later root/pin `171a259acbeb3ced855ca8f72fed0943a2f5a5cb` and wrapper `cee35da4b1ed653db50dd9d5c26693fab00f04ad`; those changes are not adopted here.

- `src/tools/video-editor/components/TimelineEditor/TrackLabel.tsx`: retain MAIN17's TrackSheet and TrackSettingsFields. Later root's `nameInputProps`/captured draft/error lifecycle currently belongs to the desktop input; pass it into the new sheet's Name input too, rather than leaving its immediate `onChange(track.id, { label })` callback. Preserve capture before typing, original guards, explicit unchanged-value intent, clean-draft release and retained draft/error on refusal. Account for sheet-close/unmount while an input is focused.
- `src/tools/video-editor/components/TimelineEditor/TrackListRenderer.tsx`: combine MAIN17's `onAddTrack` plumbing and memo equality with later root's `onTrackLabelEditStart` plumbing/equality.
- `src/tools/video-editor/components/TimelineEditor/TimelineCanvas.tsx`: pass both `onAddTrack` and later root's label-start port through to TrackListRenderer.
- `src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx`: retain MAIN17's sheet positives; reconcile later root's Agent-only touch test with the new sheet (opening it may defer capture until input focus), and exercise actual sheet rename/capture, remote change, explicit restored value, empty value, refused capture and retained draft. Do not weaken positive behavior expectations.
- `src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.tsx` and `src/tools/video-editor/hooks/useTimelineTrackManagement.ts`: the later root supplies the capture port here; preserve that wiring. Its label branch refuses ordinary `handleTrackPopoverChange` patches, so the MAIN17 sheet input must use the capture port in the same downstream step.

The current refresh includes neither the later desktop captures nor root12/native-gesture/pin changes. The shared mobile sheet constant and shell gesture/no-Text behavior must survive the later composition.

## Report retention

The repository ignores `design/*.md` through its existing `*.md` rule. This report exists at the requested path and is retained by the worker KEEP marker, but the harness's plain `git add -A` will not include it. No ignore rule was changed, preserving the unrelated-path boundary. If the report must enter Git, the manager/harness must force-add this exact file before creating the merge commit; the source-only tree hash above excludes it.
