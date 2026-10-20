# App MAIN574 impact map (read-only)

Compared incoming `574e97f44a81e0ec1a896fc3fb8626deb2f1edf0` (the five commits
`8a8a32186`, `e4b199066`, `2fa200ce1`, `94262ee21`, `574e97f44`) with
`17e46de99b7cef52fe494de1703a9865a8d4be24`. The refresh worker resolved the
tree on integration; this is an overlap map, not a second merge. No tests were
run here. `full7413` remains historical and is not evidence for MAIN574.

## Classification

- **UI-only:** `8a8a32186` moves touch from sheets to the Video | Inspector |
  Extensions tabs (`TimelineEditorShellCore.tsx`, `PropertiesPanel/*`, timeline
  label/list/canvas); `e4b199066` completes the extension host/Transcript;
  `2fa200ce1` changes the calm preview row, timeline picker and touch seek;
  `94262ee21` changes chat-tab lifecycle. Preserve MAIN mobile tabs, extension
  host, and chat/gallery/clip names. Their e2e layout/gesture changes are not
  capture or authoring changes.
- **Data/display path:** `574e97f44` adds generation source-name metadata in
  `src/tools/video-editor/contexts/VideoEditorProvider.tsx:583-591`, accepts
  those registry fields in `lib/timeline-domain.ts:227-241`, and derives
  display labels in `lib/timeline-data.ts:459-477` (consumed by
  `TimelineEditor/ClipAction.tsx` and `PropertiesPanel/ClipPanelBody.tsx`).
  This changes registry/display projection bytes, not timing, command capture,
  or legacy writer traffic. `timeline-asset-plans.ts` is the source metadata
  ingress; `clipDisplayNames.ts` is the naming authority.

## Candidate joins and smallest rechecks

| Candidate | Exact overlap with MAIN574 | Required current-root recheck |
|---|---|---|
| Stored cap `3a4350f9d` | No path overlap. Its seams remain `data/canonicalCompositionState.ts:62`, `PreviewPanel/useVideoEditorPreviewSurface.tsx:35-53`, `lib/serialize.ts:24-103`, and `data/shotCompositionProjection.ts:428-436`. MAIN574 now gives `timelineData.resolvedConfig` view labels and admits registry name fields. | Re-run the cap candidate's existing `canonicalCompositionState.mainImageCap.test.ts`, `useVideoEditorPreviewSurface.storedCap.test.ts`, `serialize.test.ts`, `useTimelinePersistence.test.tsx`, and `useTimelineSave.draftConfig.test.ts` on the refreshed root, plus the new `clipDisplayNames.test.ts`/`timeline-data.test.ts`. Verify labels stay view-only, the stored scalar is still stripped, raw same-name fields are restored, and config/fact/vector/extent delivery remains paired. No new pixel capture is implied. |
| PCM13 `d08e969b0` | No path overlap. `compositions/AudioTrack.tsx`, `compiledAudioSourceClock.ts`, the PCM contract/lifetime tests, package/lock, and public13 archive are byte-equal to the candidate. | No PCM source rework. Keep the public13 identity check; if conflict resolution changes `VideoEditorProvider.tsx`, run the existing two-file PCM13 targeted lane because that shared provider is the only indirect join. |
| Native frame fixture `f8d2b887` / final `e4c7a379` | No path overlap. The five-file fixture unit is `tests/e2e/timeline/viewing-parity/{fixture.ts,harness.ts,native-fixture-helper.py,native-fixture.integration.test.ts}` plus `tests/e2e/local/support/harness.ts`; all are byte-equal to the candidate. | Source-manifest/fixture identity check only. Reuse the existing named native-fixture central lane when the composed tree is authorized; do not relabel an old run or add a new capture here. |
| Native None `d36fe2e9` | Three source paths overlap: `components/PropertiesPanel/ClipPanelBody.tsx`, `PropertiesPanel/PropertiesPanel.tsx`, and `contexts/VideoEditorProvider.tsx`. The native clear/capture/session files and markup are otherwise untouched. | Preserve the existing desktop `three-products.spec.ts:293-304` transition selector and bulk `:1380-1385`, including `Effects` → `None`. On touch, verify the retained Inspector tab still exposes the same transition control; do not alter the native clear assertions or fallback-retirement boundary. |
| Parent delete `b91aa0c16` | No path overlap with its source or e2e files. MAIN574's Inspector/delete presentation is an indirect UI join only. | Keep `tests/e2e/local/clip-delete-command.spec.ts:197-345` selectors (`.clip-action[data-clip-id]`, `Delete clip`, recovery/Undo) and zero-legacy assertions unchanged; only confirm the refreshed Inspector still reaches the same action. |
| Embedded shot name `5d9626a68` | No path overlap: `tests/e2e/local/shot-name-command.spec.ts`, `support/app.ts`, `support/harness.ts`, and its Playwright config remain byte-equal. | No markup rewrite. Confirm the existing `span[title="Click to edit shot name"]` and input assertions still target the shot name; `ClipAction.tsx` keeps `shotName` ahead of the new `clip.label`. |
| Automatic placement `c34cf6ae4` | One shared source path: `contexts/VideoEditorProvider.tsx`. MAIN574 adds generation display metadata at registration; automatic host binding (`taskEventsReady`/`subscribe`) and `commands/{editorImagePlacement,nativePlacementCapture,placementRequester,sessionPlacement}.ts` are otherwise unchanged. No automatic e2e markup is changed. | Recheck the existing automatic source/contract lane and the generation/asset-plan tests after resolving the shared Provider. Verify metadata does not alter captured media selection, reserved bytes/keys, task fencing, or legacy traffic; do not activate or broaden automatic placement. |

## Byte-equal boundaries

The cap candidate's capture/serialization files, PCM13 consumer/archive and
lock, native-frame five-file unit, delete/shot-name/automatic command sources,
and the None/delete/shot-name/automatic e2e markup are not MAIN574 edits. The
only data-bearing refresh join is asset metadata → registry → resolved display
labels; the remaining MAIN574 changes are selector/layout, extension-host, chat,
gallery-tab, or naming presentation. Keep the MAIN mobile tabs, extension host,
and chat/gallery/clip naming while preserving all existing passing behavior
tests one-for-one. No product edit, test execution, full/tsc/build/browser/
socket/install run, or current-freshness claim was made by this map.
