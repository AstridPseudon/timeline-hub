# App2 old shared-request closure

Root reviewed: `e245a4791f9270177408a7745d8397ad7b6f81a1` (current merge parents `dcb9f9c7095b0a8438291c8949029122c7c98ad3` and `058d10d4f38488f515b9672b0cde40813ef8ea6b`). No branch was reset, checked out, merged, or pushed.

## Source-request results

| Source request | Candidate | Result | Exact current-source evidence |
| --- | --- | --- | --- |
| `tl/ap2-m2-duplicate-current-real-consumer` | `d3792aabdc8592be5f72321faa7143e9b76d1c26` | REFUSED / SUPERSEDED by `8cfcee9c0403d113463c7859f6c835d3bfd79668` | The donor's native duplicate port is present at `8cf:src/tools/video-editor/commands/commitSession.ts:370-401`; the mounted clean-session fence is at `8cf:src/tools/video-editor/hooks/useTimelineCommandSession.ts:199-206`; the App wiring is at `8cf:src/tools/video-editor/hooks/useTimelineState.ts:1225` and `8cf:src/tools/video-editor/components/AstridTimelineEditor.tsx:397-406`. The donor regression tests are also present at `8cf:src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts:84-132` and `8cf:src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx:273-303`. |
| `tl/ap2-m2-element-current-real-consumer` | `ea82d7a3581ec97e9e3e31d06bfda481529ab1f3` | REFUSED / SUPERSEDED by `8cfcee9c0403d113463c7859f6c835d3bfd79668` | The donor's mounted element facade is wired at `8cf:src/tools/video-editor/contexts/VideoEditorProvider.tsx:747-752`; the test fixture, mounted-port assertion, and assertion are at `8cf:src/tools/video-editor/contexts/VideoEditorProvider.test.tsx:199-200`, `353-355`, and `1465-1467`. |
| `tl/ap2-m2-parent-real-prepared-caller-repair` | `5ae77819ead824ea2bdd6041010142b8d055feb4` | REFUSED / SUPERSEDED by `8cfcee9c0403d113463c7859f6c835d3bfd79668` | The donor's production caller hunks are exact in `8cf:src/tools/video-editor/components/AstridTimelineEditor.tsx:587`, `8cf:src/tools/video-editor/hooks/useAddVariantAsGeneration.ts:94-99`, and `8cf:src/tools/video-editor/hooks/useSwitchToFinalVideo.ts:84-90`, `204`, and `243`. The donor's additional focused test hunk (`useAddVariantAsGeneration.test.tsx`) is not copied verbatim into `8cf`; the production behavior is already awaited and this is recorded as a test-evidence difference, not silently treated as ancestry. |
| `tl/ap2-m2-element-library-overlay-real-consumer` | `7f32b769cd61f73ea45b76eba98db61073ac924e` | APPLIED missing reviewed hunks to this working tree | Native overlay types/port and exact retry test are in `src/tools/video-editor/commands/elementGesture.ts:50-72` and `src/tools/video-editor/commands/commitSession.test.ts:31-56`; session routing is in `src/tools/video-editor/commands/commitSession.ts:523-594`, `src/tools/video-editor/hooks/useTimelineCommandSession.ts:182-195`, and `src/tools/video-editor/hooks/useTimelineState.ts:1368`; real consumers are in `src/tools/video-editor/components/ElementsLibraryPanel.tsx:50`, `85-116` and `src/tools/video-editor/components/PropertiesPanel/PropertiesPanelBody.tsx:213-257`, `561-587`. `git diff 7f32b769c --` is empty for the five untouched donor files, confirming those hunks were applied exactly. |

The overlay merge kept the current root's own None/name/prompt/automatic, newProvider/Generic/media, duplicate, parent-media, and shot-set sections. Shared files were merged around those sections; no donor branch was replayed wholesale.

## Superseded related sources

- `c4148a52afd01b90a09a1cd0f08cb1024caadc13` (old verified-media wrapper) is superseded by `0096ba86d09560b6581f23228167777d4ec47e88`: its exact Runtime client/provider implementation is the second-parent source `63ee3080ed4fe5cedcbaa5eedaf5bc51d5ae125b`, with the stronger selection-frozen/mismatch-checked facade used by the `0096` merge. No code from `c414` was applied.
- `b58f4f1b53f85fa6c2f15a8aabf144460a75300c` (media-selection carrier) is superseded by `308ac52ad7f9f171f2aa677cae898e2012912afe`; `b58` is an ancestor of the `308` carrier fix-forward. No code from `b58` was applied.

## Controls

Passed:

```text
./node_modules/.bin/vitest run --no-cache --no-file-parallelism --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/components/ElementsLibraryPanel.test.tsx \
  src/tools/video-editor/contexts/VideoEditorProvider.test.tsx
  4 test files, 145 tests passed
git diff --check
```

Not run: full suite, browser/e2e, localhost/live sockets, `tsc`, install, shared-write checks, or private-13/cache controls.
