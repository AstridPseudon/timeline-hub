# ap2-m2-parent-migrated-drop-mounted-source

## Result

Added the real mounted manual prepared-video file-drop journey to the App e2e source. It uses the existing seeded Runtime video bytes, constructs a browser `File`/`DataTransfer`, and dispatches the mounted timeline wrapper's normal `dragover`/`drop` events. No fake catalog, capture port, direct commit, new UI, product/shared source, dependency, pin, or API was added.

The journey covers:

- wrong verified selection sent to the real Runtime and closed refusal with no commit, no duplicate clip, and no legacy snapshot traffic;
- original five-field `MediaSelection` equality from Runtime preparation through verified lookup and the native `clip.add-media` request;
- ordinary native ADD shape (`row`, `media`, `track`, `at`) with no replacement/removal/after-clip fields;
- lost acknowledgement, a newer dependent local track edit, exact retry after reload and Runtime restart, and recovery ordering;
- one persisted placement, opaque parent data preservation, zero legacy saves, and guarded undo of the newer local intent.

The mounted producer fix is the settled base commit `ec663e205a3f424af01a2bdf37e6cd5fba788389`; this worker only added the allowed e2e/support source on top of it.

## Changed files

- `tests/e2e/local/support/app.ts` — added `dropFileOnTimeline`, which measures the existing rendered clips and emits a real browser file-drop gesture without a fixture copy.
- `tests/e2e/local/three-products.spec.ts` — added the mounted manual-drop journey and its Runtime/command/outbox/history assertions.

## Verification

Passed directly:

```text
git diff --check
./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.spec.ts tests/e2e/local/support/app.ts
npx tsc --noEmit --pretty false --incremental false
```

Passed collection-only:

```text
node node_modules/.bin/playwright test tests/e2e/local/three-products.spec.ts --config=playwright.three-products.config.ts --list
```

Result: 10 tests collected, including the new journey. No browser was launched.

Passed direct existing support fixture unit:

```text
node --test tests/e2e/local/support/native-transition-clear.contract.test.mjs
```

Result: 1 test passed.

Passed central targeted producer qualification:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-migrated-drop-mounted-source targeted --files "src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/lib/external-drop-utils.ts") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: `ap2-m2-parent-migrated-drop-mounted-source-targeted-1020203703-24904`, 2 files / 16 tests passed, exit 0, App tree `3e3b71683d4a9fb582ddf965106b0adf4218b447`.

The requested e2e-path central targeted attempt was also made:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-migrated-drop-mounted-source targeted --files "tests/e2e/local/three-products.spec.ts tests/e2e/local/support/app.ts tests/e2e/local/support/harness.ts") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

It exited 1 because the configured App `targeted` lane is Vitest with `src/**/*.test.{ts,tsx}` only and reports `No test files found` for e2e paths. This is a harness configuration limitation, not a source assertion failure.

## Not run / remaining gate

No full suite, local browser, localhost/live socket journey, public13/private014 adoption, dependency install, schema, or API change was run. The new browser journey is collection-checked but not runtime-qualified here, as required by the brief. The next gate is the central browser three-products/manual-drop suite when the orchestrator authorizes it; it should use the existing working public13 tuple if supported, otherwise leave private014 unchanged.
