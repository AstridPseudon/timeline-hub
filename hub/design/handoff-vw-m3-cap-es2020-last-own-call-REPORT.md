# vw-m3-cap-es2020-last-own-call

## Result

Applied the requested one-line ES2020 compatibility correction in
`src/tools/travel-between-images/components/shotTimelineDataProvider.ts`:

```diff
-if (rawApp && Object.hasOwn(rawApp, key)) {
+if (rawApp && Object.prototype.hasOwnProperty.call(rawApp, key)) {
```

No producer policy, pin, DTO, wire, metadata, serialization, or public
behavior change was made. `git diff --check` passed; the worktree diff is one
file, one insertion, one deletion.

## Tests

The exact handoff project command was first run against the shared read-only
dependency graph:

```text
node /home/user/work/app/node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --pretty false
```

It no longer reported TS2550 at `shotTimelineDataProvider.ts:146`, but exited
2 on ten unrelated Composition API errors because the shared package was
`@banodoco/timeline-composition` 0.0.8 while this App tree pins the private
0.0.12 artifact.

Using a private temporary path overlay of the tracked
`vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz` (no shared files
changed), the same project typecheck passed:

```text
node /home/user/work/app/node_modules/typescript/bin/tsc -p /tmp/vw-m3-es2020-check.A7yRhS/tsconfig.overlay.json --noEmit --pretty false
exit 0
```

The existing related test also passed with a private Vite cache:

```text
node /home/user/work/app/node_modules/vitest/vitest.mjs run --config /tmp/vw-m3-es2020-check.A7yRhS/vitest.overlay.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/travel-between-images/components/ShotTimelinePreview.test.ts
1 file passed, 25 tests passed, exit 0
```

No full suite, browser, render, socket, network, install, or shared-cache
mutation was performed.
