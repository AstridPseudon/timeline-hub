# App stored-cap ES2020 compatibility handoff

The reviewed stored-occurrence-cap candidate remains the complete 22-file patch from `b1ef4b9b910ba72375c34cf319692f90d22edc25` through `4720a864c81dc7002a9e95dbacf10cec8df5da81`. The updated complete patch is [app-stored-cap-es2020-compat.patch](app-stored-cap-es2020-compat.patch), and its complete file list is [app-stored-cap-es2020-compat.files.txt](app-stored-cap-es2020-compat.files.txt).

## Compatibility delta

Only `src/tools/video-editor/lib/serialize.ts` changes after `4720a864…`:

```diff
-    if (rawApp && Object.hasOwn(rawApp, key)) {
+    if (rawApp && Object.prototype.hasOwnProperty.call(rawApp, key)) {
```

This preserves the existing own-property semantics and avoids the unchanged App ES2020-lib `TS2550`. No lib target, scalar, raw/view behavior, test, ownership rule, or cap design changed.

## Source and patch identities

| Item | SHA / value |
| --- | --- |
| Base | `b1ef4b9b910ba72375c34cf319692f90d22edc25` |
| Cap source commit | `4720a864c81dc7002a9e95dbacf10cec8df5da81` |
| Cap source tree | `aa9eb31281e915fe32e7af6e4c7a30a2ff85e8ad` |
| Cap source `serialize.ts` SHA256 | `59c0689110eca4032bfeb179f5c5c2d3d5e341086c274b69d0ffa57c9395f768` |
| Final source `serialize.ts` SHA256 | `7bdf715abaa480b8170c6b4ab079db316a162891b938855511dc6423eb464864` |
| Full b1-to-final patch SHA256 | `1f5368689ba189f138a2c0e3e4b729d9cdb676137ff4113eb64d01578fac0a16` |
| Full file-list SHA256 | `406a984fbf170b1e11ff4c49bdf55427ac5ab98fd09e8705a8dfc1da6132f454` |
| Tiny 4720-to-fix patch SHA256 | `ebe867e8b2670073e24dad66809e1150bfd1e9e60d2029029e7f82aecf9f9d15` |
| b1-to-final files | 22 |

The final pre-harness working tree differs from `4720a864…` in exactly one file, one insertion and one deletion; `git diff --check` passes. The harness commit SHA/tree is pending because the harness creates it after worker exit and is not observable from this worker.

## Scoped evidence

Using the worker-owned `private12` dependency overlay, private `TMPDIR`, the existing `snapshot-vitest-runner.cjs` `__dirname` preload, `--configLoader=runner`, `--no-cache`, one worker, and no shared dependency writes:

```sh
env -u ASTRID_CHECKOUT TMPDIR="$W/notes/tmp" \
  node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
  "$W/private12/node_modules/vitest/vitest.mjs" run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts \
  src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
```

Result: **exit 0; 4 files, 154 tests passed**.

```sh
env TMPDIR="$W/notes/tmp" \
  node "$W/private12/node_modules/eslint/bin/eslint.js" \
  src/tools/video-editor/lib/serialize.ts --max-warnings 0
```

Result: **exit 0; no diagnostics**. The initial `.bin/eslint` wrapper attempt was an overlay setup miss because hidden `.bin` links were not copied; it did not run lint. The direct private package entrypoint above is the passing lint command.

No full suite, project tsc, build, browser, socket, install, merge, push, or parity claim was made. Viewing review remains required; KEEP is left for that review.
