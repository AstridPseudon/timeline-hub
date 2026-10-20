# Authorized SDK preview example fix

Applied the authorized `design/app-sdk-preview-example-proposal.patch` only to:

- `src/examples/transcript-panel-example.ts`
- `src/sdk/examples-governance.test.ts`

The example now uses the public optional `PanelPreviewService`, derives a real
`PanelFrameAnchor` from `getBoundingClientRect()`, passes projected timeline
seconds to `showFrame`, and returns cleanup that disposes the returned handle.
The governance test adds coverage for geometry, optional-service absence, and
disposal. All pre-existing governance cases and assertions remain unchanged.

## Baseline and final counts

Baseline was the authorized base `tl/integration` at source SHA
`1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff` (the short pin was `1be0efdde`).
The recorded baseline governance result was **624 total: 622 passed, 2
failed**. The exact old failed-node names were:

- `public export "PanelFrameAnchor" is imported by at least one example`
- `public export "PanelPreviewService" is imported by at least one example`

Final governance result: **625 passed, 0 failed**. The neighboring hover suite
result: **5 passed, 0 failed**. The combined requested lane result: **630
passed, 0 failed** across 2 files.

Final modified-source fingerprints:

- `src/examples/transcript-panel-example.ts` — SHA-256
  `17fef03da859238d6a8052b4ad1b737fc97477e0c4a33d07ad80a37c5cb6b5fe`
- `src/sdk/examples-governance.test.ts` — SHA-256
  `7ee6268f3117f12001020cbad3a26ec1483114264878ab02de1f768ff1b114e0`
- authorized two-file diff — SHA-256
  `2b0462df63a45350d11b48ac13d8040981d6b15585a6f281f145f10d185e0516`

## Exact checks

```text
npm exec -- vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/sdk/examples-governance.test.ts src/tools/video-editor/components/PropertiesPanel/TranscriptPanel.hover.test.tsx
PASS — 2 files, 630 tests

npm exec -- vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/sdk/examples-governance.test.ts
PASS — 1 file, 625 tests

npm exec -- vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/video-editor/components/PropertiesPanel/TranscriptPanel.hover.test.tsx
PASS — 1 file, 5 tests

node_modules/.bin/tsc -p tsconfig.sdk-example-check.json --noEmit
PASS — narrow real TypeScript program rooted at the actual example, resolving current @astrid/editor-sdk exports; no emit

node_modules/.bin/eslint src/examples/transcript-panel-example.ts src/sdk/examples-governance.test.ts --max-warnings 0
PASS — no warnings

git diff --check
PASS
```

The narrow TypeScript config was temporary, used the repository's real SDK
barrel and `@/*` aliases, and was removed after the check. No project tsc,
full suite, build, browser, install, live socket, or baseline-record update
was run.

## Decisions and limits

No new design decision was needed: the settled grant and proposal were applied
as written. No SDK API, renderer, production panel, or other App path changed.
The harness may commit the two source changes; baseline records remain for
manager review as required.
