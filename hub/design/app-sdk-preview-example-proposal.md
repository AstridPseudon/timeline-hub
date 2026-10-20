# App SDK preview-example proposal handoff

## Scope

Reviewable patch only; no App product files were modified in this worker worktree.

Patch:
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-sdk-preview-example-proposal.patch`

The patch changes only the existing public transcript example and its existing SDK governance test:
- `src/examples/transcript-panel-example.ts`
- `src/sdk/examples-governance.test.ts`

## Baseline and exact failures

On the untouched baseline, the governance test reports 624 tests with exactly two failures:
- public export `PanelFrameAnchor` is imported by at least one example
- public export `PanelPreviewService` is imported by at least one example

Command:
```sh
npm exec -- vitest run --config config/testing/vitest.config.ts src/sdk/examples-governance.test.ts
```

Observed result: 622 passed, 2 failed. The failure assertions are in `src/sdk/examples-governance.test.ts:527`.

## Proposed usage

The existing `src/examples/transcript-panel-example.ts` imports the surrounding public panel contracts but currently does not import or use the two new UI contracts. The patch:

1. imports `PanelFrameAnchor` and `PanelPreviewService` from `@astrid/editor-sdk`;
2. adds `previewTranscriptWordOnHover` to the same example;
3. reads the optional `props.video?.preview` and returns `undefined` when the panel is hidden, preview is unavailable, or timing is not previewable;
4. derives the anchor from the hovered target's actual `getBoundingClientRect()` into a named `PanelFrameAnchor`;
5. calls `showFrame` with the projected timeline seconds and returns cleanup that calls the returned handle's `dispose()`;
6. adds one governance contract assertion for geometry, optional-service absence, and disposal.

The caller lifecycle is explicit: invoke the returned cleanup from hover leave and from the panel's hidden/unmount teardown. This mirrors the existing host behavior rather than adding a new SDK feature.

## Unmodified source paths and usage proof

These paths were inspected but left unmodified:

- `/home/user/work/wt/app-m4-sdk-preview-example-proposal/src/sdk/ui.ts:20-38` — defines `PanelFrameAnchor`, `PanelPreviewService.showFrame`, and optional `PanelVideoAdapter.preview`.
- `/home/user/work/wt/app-m4-sdk-preview-example-proposal/src/tools/video-editor/components/PropertiesPanel/TranscriptPanel.hover.test.tsx:54-75` — constructs the optional preview service and verifies the typed anchor.
- `/home/user/work/wt/app-m4-sdk-preview-example-proposal/src/tools/video-editor/components/PropertiesPanel/TranscriptPanel.hover.test.tsx:89-145` — covers delayed hover, DOM geometry, leave disposal, hidden/scroll/unmount cleanup.
- `/home/user/work/wt/app-m4-sdk-preview-example-proposal/vendor/astrid-browser/astrid/packs/rendering/ui/transcript/TranscriptPanel.tsx:589-599` — production panel gets the hovered element's `getBoundingClientRect()`, calls `preview.showFrame`, and clears the handle on mouse leave.

The patch extends the already-existing public `src/examples/transcript-panel-example.ts`; it does not alter the SDK interfaces, production panel, preview renderer, or governance coverage policy.

## Future validator

After the orchestrator assigns ownership and applies the patch, run exactly:

```sh
npm exec -- vitest run --config config/testing/vitest.config.ts src/sdk/examples-governance.test.ts
```

Expected scope is the governance file only; the patch should remove the two baseline failures and preserve all original assertions. No full project, build, browser, TypeScript compiler, install, or live-client validation is claimed here.

## Checks performed here

- `git apply --check --whitespace=error /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-sdk-preview-example-proposal.patch` — passed.
- In-memory virtual-source TypeScript transpile for the proposed example and governance test — passed.
- No repository product modification was made.

