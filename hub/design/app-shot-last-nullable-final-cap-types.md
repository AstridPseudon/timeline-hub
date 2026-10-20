# App final nullable shot capture type fix

## Result

Fixed only the final nullable diagnostic in
`src/tools/video-editor/commands/shotSetCapture.ts`. `apply` now stores the
validated `supplied.select` in a typed local before using it from the nested
`assign` function. The command, record, reads, guards, bindings, and writes
retain the same string values and serialized bytes. No validator, API, `any`,
suppression, field, frame, or semantic behavior was added.

The approved cap source was composed in this working tree from the exact
30-path delta `dca891972840f502c974fbf3c3b1d585855842c1` relative to its
read-only merge parent `c57dcc26162642f503532f143ceb96bb185273aa`, applied on
current integration `9b14bf9f793830156a80e249e65f7f4496c62853`. All 30 cap
paths are present, and current Home/Facade/recovery/source changes were kept.
The final tree is uncommitted; the harness will assign its tree hash.

## Environment

- Approved Composition archive SHA-256:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Corrected private13 overlay: 77 regular files, version `0.0.13`.
- Overlay `package.json` SHA-256:
  `7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61`.
- Overlay `dist/evaluation.d.ts` SHA-256:
  `fb7226d0e817c15931593a1493646248a7de34bda1be3c80b615b6d02912d285`.
- The shared `0.0.10` package was not used for the project typecheck and no
  shared dependency or cache was changed.

## Tests

Nearest shot controls:

```text
node /home/user/work/app/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/shotSetCapture.test.ts src/tools/video-editor/commands/shotSetSession.test.ts src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts
```

Result: 3 files passed, 11 tests passed, exit 0.

Targeted lint and whitespace check:

```text
node /home/user/work/app/node_modules/eslint/bin/eslint.js --no-cache --max-warnings 0 src/tools/video-editor/commands/shotSetCapture.ts
git diff --check
```

Result: both passed, exit 0.

One actual project typecheck, using the private source leaf and private13
overlay, under the required lock:

```text
flock -x /home/user/work/.app-tsc.lock \
  env NODE_OPTIONS=--max-old-space-size=4096 \
  node <private-leaf>/node_modules/typescript/bin/tsc \
  --noEmit -p <private-leaf>/tsconfig.app.json --pretty false
```

Result: exit 2. The final nullable `shotSetCapture.ts` diagnostic is absent.
One unrelated current-integration diagnostic remains:

```text
src/integrations/runtime/dataProvider.ts(1637,42): error TS7053: Element implicitly has an 'any' type because expression of type 'string' can't be used to index type 'MediaSelection'.
```

The temporary private leaf was removed after the check. No full suite,
browser, install, build, or broad test was run. Viewing fallback ACK remains
separate and was not changed.

## Decisions and limits

The read-only three-way merge check found no conflicts. A direct three-way
`git apply` could not acquire the read-only worktree index lock, so the same
approved 30-path patch was applied plain to the working tree; no refs, index,
or shared dependency files were changed. The final project typecheck is not
zero because of the unrelated `dataProvider.ts` diagnostic above; fixing it
would exceed this task's scope.
