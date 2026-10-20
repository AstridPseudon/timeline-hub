# AP2 M2 selected row-local current clean source

## Result

Implemented the selected-row local consumer packet on the latest `hub/tl/integration` App base.

- Routed the mounted selected PARAM carrier from timeline ops through `PropertiesPanel` and `ClipPanel` to `AstridElementParams`.
- Selected-pack parameter edits retain a local draft, resolve the exact selected authority pin, prefetch retained inputs, and submit only native `clip.set-params` commands. Missing carrier, stale basis, async read completion, and unmounted-session failures preserve the draft and surface an error.
- Preserved current-row/trim/other-owner behavior: unowned literal element params still use the existing native element producer; unrelated panel and timeline paths were not changed.
- Added mounted consumer coverage and retained direct-neighbor command/authority coverage from the reviewed row-local packet.
- Added only the genuine committed selected P1 DEV fixture/spec source: the harness admits a project-owned draft through Agent `update-element` as `clip.set-element` then `clip.set-params`, retains the P1 pin/object, exercises P2 removal/refusal/retry/reload/undo, and asserts no legacy save traffic.
- Did not restore or add `src/tools/video-editor/lib/theme-api.fallback.tsx` or `src/tools/video-editor/lib/registry.generated.fallback.ts`. No `config/vite`, preview, render, or Composition files were changed.

The row-local path was not already integrated: the shared carrier/session files were present, but the PropertiesPanel consumer boundary and selected-pack producer path were absent. This is therefore a code change, not a no-op.

## Tests and checks

All commands ran in `/home/user/work/wt/ap2-m2-selected-row-local-current-clean-source`.

```sh
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/clipParamsCapture.test.ts \
  src/tools/video-editor/commands/selectedParamPort.test.ts \
  src/tools/video-editor/commands/selectedParamAuthority.test.ts \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
```

PASS — 6 files, 70 passed, 1 expected fail (71 total). The expected failure preserves the original selected-pack fallback-writer assertion while the fallback is intentionally removed; the test is marked `it.fails` with the carrier requirement named.

```sh
./node_modules/.bin/eslint --no-cache --max-warnings 0 playwright.three-products.config.ts tests/e2e/local/support/harness.ts tests/e2e/local/three-products.selected-param-dev.spec.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
```

PASS.

```sh
./node_modules/.bin/tsc --noEmit --pretty false
```

PASS.

```sh
git diff --check
```

PASS.

An initial Vitest attempt with `--configLoader=runner` failed before collection because the repository config uses `__dirname` under that loader. The passing rerun used the normal loader with `--no-cache`; no shared cache was written intentionally.

## Decisions and limits

- Applied the reviewed row-local consumer changes against current `7d`/trim-era context manually where old patch context would have replaced current imports. Existing shared command/port files were already present and were not duplicated.
- Ported the selected DEV harness/spec from committed `04dbddad0` (`ap2-m2-selected-current-dev-original-p1-gate`) while retaining current parent-delete harness additions. The two Viewing fallback files were intentionally excluded as instructed.
- No browser, localhost/live socket, central `request-test`, full suite, adoption, pin/schema gate, or build gate was run. Selected DEV qualification remains unverified pending the ownerfix for the missing fallback dependency.

## Recommended next step

Viewing should resolve the missing fallback/build ownership issue first. After that ownerfix, the orchestrator may run the named selected P1 DEV gate against this source tree.
