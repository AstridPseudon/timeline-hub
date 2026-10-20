# ap2-m2-parent-manual-add-real-ui-source

## Result

Blocked before source changes. The current mounted UI has no path that both originates a real manual prepared-video ADD gesture and reaches the verified `addClip` command door with the original five-field Runtime `MediaSelection`.

The existing Runtime/provider/API0096 facade and the `parentClipAddMedia` editor-ops forwarding are present. However, the mounted manual file-drop path ends in local prepared-media `applyEdit`, not the native command path. Adding the browser journey now would therefore either qualify the wrong legacy path or inject a command/capture port. Both are excluded by the settled plan.

No product/shared source was changed. No test was added. No synthetic authority, pin adoption, direct command substitute, or central test request was used.

## Evidence and exact owner dependency

- `src/tools/video-editor/lib/external-drop-utils.ts:485-500` handles a real video file drop, uploads it, prepares the asset, and calls `dropAsset`.
- `src/tools/video-editor/hooks/useAssetManagement.ts:269-317` receives that prepared asset, calls `previewPreparedMediaCommand`, then applies it through `getApplyEdit()({ type: 'prepared-media', command }, ...)`. The prepared asset carries `mediaSelection`, but this producer does not call `commands.addClip`.
- `src/tools/video-editor/hooks/useTimelineCommandsService.ts:474+` has the native qualified branch, but it is only reached for a prepared asset carrying `mediaSelection` through the command service. It validates video/time/placement constraints, calls the verified Runtime facade, then submits native `clip.add-media`.
- The existing mounted generation callers in `src/tools/video-editor/hooks/useAddVariantAsGeneration.ts` and `src/tools/video-editor/components/AstridTimelineEditor.tsx` use a registered prepared asset with `afterClipId`, not the manual media-selection path.
- `src/tools/video-editor/components/useVideoEditorShellSlots.tsx` defines the built-in asset-panel slot, but `TimelineEditorShellCore.tsx` does not destructure or mount `assetPanelSlot`; the normal mounted route remains the file-drop path above.
- API0096 (`getProjectVerifiedMedia`) preserves the exact five-field selection before awaiting Runtime and refuses project/selection mismatches. Provider join `8cf` forwards `parentClipAddMedia`. Those pieces do not repair the producer-side bypass.

The App owner dependency is precise: adapt the existing manual file-drop producer, or mount the existing built-in asset panel and route its prepared result, so the real gesture invokes `useTimelineCommandsService().addClip` with the original `mediaSelection`, normal ADD placement (`afterClipId` absent), and the existing skeleton/draft/refusal semantics. It must not fall back to prepared-media `applyEdit` or a legacy snapshot on verification refusal. No new API or DTO is needed.

After that owner change lands, add one browser journey in the allowed `tests/e2e/local/three-products.spec.ts` / `support` files covering the required wrong-selection refusal/draft, real ADD, lost ACK/newer local intent, restart/retry/reload, undo, opaque preservation, no double placement, and zero-legacy proportionately. Keep public013 if supported; otherwise retain the exact staged private014 normal pair unchanged.

## Verification

Run from `/home/user/work/wt/ap2-m2-parent-manual-add-real-ui-source`:

```text
./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.spec.ts tests/e2e/local/support/app.ts tests/e2e/local/support/harness.ts
```

Passed.

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/integrations/runtime/dataProvider.test.ts
```

Passed: 3 files, 154 tests.

```text
node node_modules/.bin/playwright test tests/e2e/local/three-products.spec.ts --config=playwright.three-products.config.ts --list
```

Collection-only check passed: 9 existing tests collected; no browser, localhost, live socket, or full suite was run.

```text
git diff --check
git status --short --branch
```

Passed; worktree is clean on `tl/ap2-m2-parent-manual-add-real-ui-source`.

The central targeted request was intentionally not submitted because there is no candidate source change to qualify and the task forbids a dirty-source request. Once the owner dependency is fixed and a candidate is committed by the harness, run exactly:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-manual-add-real-ui-source targeted --files "tests/e2e/local/three-products.spec.ts tests/e2e/local/support/app.ts tests/e2e/local/support/harness.ts") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The named App three-products suite is `full-e2e-three-products`; it must remain central-only if a full browser qualification is later requested.

## Blocker

Normal UI cannot express the required native prepared-media ADD under the present integrated App authority. This is an owner/source integration dependency, not a test-fixture or browser-harness gap.
