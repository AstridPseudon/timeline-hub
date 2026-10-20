# App shot-name capture TypeScript narrowing fix

## Change

Changed only `src/tools/video-editor/commands/shotSetCapture.ts`.

- Narrowed `source_mapping` and its `shots` map before reading the source pin.
- Narrowed the source pin's `shot_id` before using it as an identity string.
- Added an explicit internal `ShotSetResult` return type for the capture apply path.
- Validated the captured bundle and command with typed locals before finishing a capture, removing the unsafe basis casts from this adapter.

The valid shot-name command shape, source dependency pin, guard values, payload writes, and recorded bytes are unchanged. No public or wire type changed.

## Exact diagnostics addressed

The composed cap check previously reported these four diagnostics in `shotSetCapture.ts`:

```text
src/tools/video-editor/commands/shotSetCapture.ts(61,18): error TS18047: 'bundle.source_mapping' is possibly 'null'.
src/tools/video-editor/commands/shotSetCapture.ts(61,40): error TS2339: Property 'shots' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'shots' does not exist on type 'string'.
src/tools/video-editor/commands/shotSetCapture.ts(145,19): error TS2322: Type 'string | null' is not assignable to type 'string'.
  Type 'null' is not assignable to type 'string'.
src/tools/video-editor/commands/shotSetCapture.ts(195,35): error TS2345: Argument of type 'JSON' is not assignable to parameter of type 'object'.
  Type 'null' is not assignable to type 'object'.
```

The first two are fixed by the `sourceMapping`/`sourceMapping.shots` object narrowing. The nullable identity is fixed by the explicit `sourceId` string guard. The `JSON`/`object` diagnostic is fixed by narrowing `basis.command` into a typed local before checking claims. The project `tsc` was not rerun here because the task explicitly assigns the single composed project check to another worker; new project-`tsc` zero diagnostics are therefore not independently verified in this worker.

The same composed check also had six unrelated Composition export diagnostics; those were not changed.

## Evidence

Targeted shot capture/session/name controls:

```text
node /home/user/work/app/node_modules/vitest/vitest.mjs run --config vitest.shot-name.config.mts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/shotSetCapture.test.ts src/tools/video-editor/commands/shotSetSession.test.ts src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts
```

Result: **3 test files passed, 11 tests passed, exit 0**.

Scoped lint:

```text
node /home/user/work/app/node_modules/eslint/bin/eslint.js --no-cache --max-warnings 0 src/tools/video-editor/commands/shotSetCapture.ts
```

Result: **exit 0**.

Additional hygiene check:

```text
git diff --check
```

Result: **exit 0**.

No full suite, project `tsc`, browser/e2e, build, install, or shared dependency/cache write was run.
