# App current cap/provider assembly gate

## Verdict

**PASS for the current cap/provider source assembly; READY for the next central full/Viewing fixture as a bounded source candidate.** This is not an all-viewer or release-ready claim. D10 installed-hostfix deletion remains held, and the actual project typecheck remains nonzero on five unrelated provider/media diagnostics.

## Pinned source

- HEAD: `dcb9f9c7095b0a8438291c8949029122c7c98ad3`
- Tree: `5b23f2005f4e00c30177e417b1e2898dc1210603`
- HEAD is a descendant of cap `a8283307a` and Provider ports `8cfcee9c0`.
- Worktree was clean before and after qualification; no product files, refs, integration worktrees, shared dependencies, or shared caches were modified.

## Source assembly checks

- Expected cap union: **30/30 files present**.
- The one derived `storedOccurrenceDurationMs` producer, raw-basis serializer stripping/restoration, and config/projection-fact/compiled-vector/extent pairing are present across bootstrap, local, recovery, accepted, Player, still, and client-render paths.
- Provider/session seams are present for scalar/name, Generic, Element, occurrence duplicate, and parent media ports; the native `None` path remains in the shared command-session controls.
- No production `Object.hasOwn` remains in the cap paths. Test-only historical assertions were unchanged.
- `git diff --check`: PASS.

## Dependency identity

Tests and the valid typecheck used the private13 runner/overlay and the immutable Composition 0.0.13 package, never the shared 0.0.10 install.

- Composition archive: 77 regular members; SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- App package/lock resolve `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz` / version `0.0.13`.
- Peer versions: React/ReactDOM `18.3.1`; Remotion, `@remotion/player`, `@remotion/media`, and `@remotion/layout-utils` `4.0.509`.
- The shared install was read only to confirm it is forbidden (`0.0.10`); it was not used for qualification.

## Targeted evidence

All Vitest runs used the private13 Vitest binary, current-worktree root, private Composition aliases, `--configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism`, and an owned temporary cache location.

Exact command prefix:

```text
env -u ASTRID_CHECKOUT node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/dirname-preload.cjs /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/private13/node_modules/vitest/vitest.mjs run --config /tmp/app-m3-current-cap-provider-assembly-gate-v13.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism
```

The three invocations appended these exact file groups:

```text
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx src/tools/video-editor/lib/canonicalRenderBounds.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts

src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/hooks/useTimelinePersistence.test.tsx src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/commands/ordinaryScalarMember.test.ts src/tools/video-editor/lib/clipDisplayNames.test.ts src/tools/travel-between-images/components/ShotTimelinePreview.test.ts src/tools/travel-between-images/pages/ShotEditorView.test.tsx

src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx src/tools/video-editor/hooks/useRenderState.test.tsx
```

1. Cap/raw/evaluator controls: **6 files, 82 tests passed** — initial read, lifecycle, stored-cap delivery, render bounds, serialization/raw stripping, and main-image evaluator.
2. Provider/None/generic shared-hook controls: **17 files, 360 tests passed** — `VideoEditorProvider`, timeline command session/projection/persistence/draft, Generic, Element, scalar, name, occurrence duplicate, parent media, popup/shot preview, and current ShotEditorView.
3. Still/client-render boundary controls: **3 files, 82 tests passed** — `TimelineFramePreview`, preview surface, and `useRenderState`.

The stored-cap/evaluator tests exercise 4000/4500 delivery and the real evaluator boundary: 4000 has frame 105 opacity 0.5, frame 119 active, frame 120 empty; 4500 differs at frame 105 and remains active at frame 120. Viewing's existing negative/non-finite fallback approval for `dca891972` was reused; the already-proven omission negative was not rerun.

An initial private Vitest config attempt had a package-alias prefix error (five Composition-dependent suites failed to resolve while 37 unrelated tests passed). The temporary alias ordering was corrected; the three final runs above are the source results.

## One valid project typecheck

Exact command, under the shared lock and with the requested memory limit:

```text
flock -x /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/private13/node_modules/typescript/bin/tsc --noEmit -p /tmp/app-m3-current-cap-tsc-valid.opMd1j/tsconfig.app.json
```

Result: **exit 2, exactly five diagnostics; zero cap-file diagnostics**:

- `src/tools/video-editor/hooks/useTimelineCommandsService.ts:453:5` — mixed sync/async `addClip` implementation does not satisfy overloads (`TS2322`).
- `:1153:35` and `:1175:35` — `DataProvider` cast lacks `getProjectVerifiedMedia` (`TS2352`).
- `:1158:90` and `:1187:78` — provider `projectId` is `string | null`, expected `string` (`TS2322`).

The first incomplete overlay setup was discarded because it omitted top-level `config`/`supabase` links and produced path-resolution errors; it was not counted as the project result. The final complete-overlay run above is the qualification result.

## Boundary and next step

The cap/provider source is ready for the next central full/Viewing fixture at the pinned SHA/tree. It is **not** an all-viewer-ready claim: D10's installed-hostfix deletion remains held pending its owner packet/integration, and the five unchanged provider/media type diagnostics remain open. No full suite, install, browser, live socket, physical parity, or broad 706/omission rerun was performed.
