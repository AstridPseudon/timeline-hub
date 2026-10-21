# AP2 M2 selected DEV mount precondition source correction

## Result

The selected DEV fixture now restores the original startup precondition at all
three original boundaries using the existing App mount DOM:

- after the initial `page.goto()`;
- after the first existing `page.reload()` following P2/source removal; and
- after the second existing `page.reload()` before draft recovery.

Each boundary calls a local `expectAppMounted(page)` helper that waits for the
first child under `#root` to be attached with the original `expectConnected`
timeout budget of 20 seconds. The helper is startup-only. It does not assert,
derive, or replace the selected timeline, clip, parameter, P1 schema pin, or
any other fixture/data authority.

## Why this is the existing startup signal

Source review verified the signal rather than adding a DOM hook:

- `index.html` starts with an empty `#root`.
- `src/app/main.tsx` calls `renderApp(rootElement)` only after the existing
  startup imports and `initializeWorkspaceRuntimeIdentity()` finish.
- `src/app/bootLayer.ts` defines its existing first-frame readiness as a
  non-empty root (`root.childElementCount > 0`) plus the existing
  `data-boot-hold` condition. The fixture uses only the root-child mount
  portion, matching startup precondition intent and leaving workspace/data
  readiness to the original `openSeededTimeline` and selected assertions.
- `src/tools/video-editor/pages/VideoEditorPage.tsx` uses `data-boot-hold`
  while workspace state settles; this is not used as P1 or timeline authority.

The same-origin DEV RuntimeConnectionGate intentionally does not provide the
hosted status-pill selector, so the impossible `expectConnected` literal was
not restored. Hosted callers remain unchanged.

## Preserved scope

Only `tests/e2e/local/three-products.selected-param-dev.spec.ts` changed. The
approved `a0a73dae3` seeded timeline, exact clip, params surface, P1 scope,
P1/P2/refusal/draft/lost-ACK/restart/retry/undo/zero-legacy assertions, and
both original reloads are unchanged. No product, bootstrap, route, shared
harness, navigation, retry, recovery action, timeout increase, or new readiness
flag/DOM hook was added.

Live hosted `expectConnected` callers remain:

- `tests/e2e/local/support/app.ts` (the helper definition);
- `tests/e2e/local/direct-journey.spec.ts`;
- `tests/e2e/local/three-products.spec.ts`;
- `tests/e2e/local/shot-name-command.spec.ts`;
- `tests/e2e/local/track-label-command.spec.ts`;
- `tests/e2e/local/clip-delete-command.spec.ts`; and
- `tests/e2e/local/parent-trim-command.spec.ts`.

The selected DEV spec is intentionally no longer one of those callers.

## Existing diagnostic artifacts

Available retained artifacts from the earlier central run:

- `.../central-trace/driver.stderr` (6,599 bytes): central driver/build
  stderr, containing Browserslist, PostCSS, Rollup circular-chunk, and Vite
  reporter warnings. It is not a dedicated Vite child-server stderr stream
  and contains no exact pending dependency error.
- `.../three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/trace.zip`
  (178,729 bytes): retained browser trace.
- `.../three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/error-context.md`
  (11,701 bytes): retained failure context.

No dedicated Vite child stderr artifact is present under the retained worker
artifacts. No new harness instrumentation was added.

## Verification

Passed:

```text
git diff --check
exit 0

npm exec -- eslint --no-cache tests/e2e/local/three-products.selected-param-dev.spec.ts
exit 0

npm exec -- playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list
exit 0; Total: 1 test in 1 file
```

The changed-path check reports only:

```text
tests/e2e/local/three-products.selected-param-dev.spec.ts
```

The browser case, localhost/live sockets, central gate, and full suite were
not run, per task instructions. The source-only change is therefore not an
actual-case qualification.

## Next step

Run the one selected DEV case through the central test service on this exact
source tree. If it still fails before `#root` mounts, the failure remains a
cold DEV module-graph/bootstrap issue owned by the App source path; do not
increase this fixture timeout or add a recovery workaround.
