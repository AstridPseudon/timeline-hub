# App stored-cap final ES2020 handoff

This is the reviewed 22-file stored-occurrence-cap unit from `b1ef4b9b910ba72375c34cf319692f90d22edc25`, updated only for ES2020-safe own-property checks. The complete patch and file list are `app-stored-cap-final-es2020.patch` and `app-stored-cap-final-es2020.files.txt`.

## Exact compatibility delta from `4720a864c81dc7002a9e95dbacf10cec8df5da81`

The final working tree changes exactly these two expressions, with no raw-basis, lib-target, test, or other product change:

```diff
diff --git a/src/tools/travel-between-images/components/shotTimelineDataProvider.ts b/src/tools/travel-between-images/components/shotTimelineDataProvider.ts
@@
-        if (rawApp && Object.hasOwn(rawApp, key)) {
+        if (rawApp && Object.prototype.hasOwnProperty.call(rawApp, key)) {

diff --git a/src/tools/video-editor/lib/serialize.ts b/src/tools/video-editor/lib/serialize.ts
@@
-    if (rawApp && Object.hasOwn(rawApp, key)) {
+    if (rawApp && Object.prototype.hasOwnProperty.call(rawApp, key)) {
```

## Identities

| Item | SHA / value |
| --- | --- |
| Base commit | `b1ef4b9b910ba72375c34cf319692f90d22edc25` |
| Base tree | `8d8a10b057ed31fed69517e18a23b8ec3811447a` |
| Reviewed cap commit | `4720a864c81dc7002a9e95dbacf10cec8df5da81` |
| Reviewed cap tree | `aa9eb31281e915fe32e7af6e4c7a30a2ff85e8ad` |
| Pre-harness compatibility commit | `1fe351b9847d35db66ab294a6edf631447fa78ce` |
| Pre-harness HEAD tree | `f447f69b6e94ccb8bf2d2fdfe868579e662cbd31` |
| Final working tree (uncommitted provider delta) | `8465cfeec6a77ed66b6a150205ddca768476e8e4` |
| Harness commit | pending worker exit |
| `serialize.ts` SHA256 | `7bdf715abaa480b8170c6b4ab079db316a162891b938855511dc6423eb464864` |
| `shotTimelineDataProvider.ts` SHA256 | `70d6d5e845065a361c0088ccc4974262fe9978042344a891847b5ecee3ebfd4c` |
| Complete 22-file patch SHA256 | `5d19bf81ebeda6338bb3ac45b58931a4bc257ae29baff08ce5fc7d1c7d4d3bdd` |
| Complete file-list SHA256 | `406a984fbf170b1e11ff4c49bdf55427ac5ab98fd09e8705a8dfc1da6132f454` |
| Files in complete patch | 22 |

## Evidence

Using read-only `/tmp/app-coherent-deps12/node_modules`, an owned `/tmp/app-m3-stored-cap-popup-es2020-fix/review-cache`, `--configLoader=runner --no-cache --maxWorkers=1`, and the repo-local `__dirname` preload:

```sh
env -u ASTRID_CHECKOUT node --require /tmp/app-m3-stored-cap-popup-es2020-fix/dirname-preload.cjs \
  /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config /tmp/app-m3-stored-cap-popup-es2020-fix/review-vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts \
  src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/travel-between-images/components/ShotTimelinePreview.test.ts
```

Result: exit 0; 5 test files, 179 tests passed, 0 failed.

```sh
node /tmp/app-coherent-deps12/node_modules/eslint/bin/eslint.js \
  --no-cache --report-unused-disable-directives --max-warnings 0 \
  src/tools/video-editor/lib/serialize.ts \
  src/tools/travel-between-images/components/shotTimelineDataProvider.ts
```

Result: exit 0; no diagnostics. `git diff --check` also passes.

The cap-unit audit over all 22 files found no remaining production `Object.hasOwn` occurrence. Existing test-only occurrences remain outside this two-expression product delta; the one newly added test occurrence is unchanged to preserve the exact `4720` delta and because no test change was requested. No full/project TypeScript check, build, browser, socket, install, merge, parity, or pixel/audio claim was made. KEEP for Viewing review; no merge/parity claim.
