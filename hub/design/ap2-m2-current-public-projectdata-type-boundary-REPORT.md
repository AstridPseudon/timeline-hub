# Current public project-data type boundary

## Result

Fixed only the three local TypeScript staging boundaries in
`src/tools/video-editor/commands/projectDataMember.ts`:

- pass the value validated by `assertFiniteJson` into `jsonBytes` at line 108;
- make the extension-total `reduce` accumulator explicitly numeric at line 189;
- make merge lowering require only its used `value`/`mode` fields at lines 212–215.

No command shape, dispatch, public schema, generated type, pin, DTO, guard,
fallback writer, or test expectation changed. The existing finite-JSON,
reserved-key, namespace-shape, size/count, leaf/container, ordering, merge,
and mixed-batch refusal behavior is unchanged.

## Pin and resolution evidence

The App lockfile points at public013 and its local tarball is authentic:

- `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz` version: `0.0.13`;
- SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`;
- the lockfile SHA-512 integrity exactly matches the tarball.

The shared HOME install is not that pin: Node resolves
`/home/user/work/app/node_modules/@banodoco/timeline-composition/package.json`,
which reports version `0.0.8`. It was not modified. The helper does not import
Composition, so this stale HOME package cannot justify a public013-related
change to the helper or its generated types.

## Diagnostics and checks

Before the edit, a private current-source overlay reported only these seven
diagnostics, all in `projectDataMember.ts`: TS2345 at 108; TS18047 and TS2365
at 189; TS18047 and TS2365 at 190; and TS2345 at 266. After the edit:

```text
./node_modules/.bin/tsc -p private-current-source-overlay/tsconfig.json --pretty false
=> passed (0 diagnostics)

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts
=> 2 files, 25 tests passed

./node_modules/.bin/eslint src/tools/video-editor/commands/projectDataMember.ts --max-warnings 0
=> passed

git diff --check
=> passed
```

The private overlay and its logs were removed after the check. No full suite,
browser, localhost, socket, provider/Door/native, dependency install, or
release check was run.

## Decision / handoff

The sound correction is local to the public helper's staging types; no private
392 counterpart or membership path was touched. No blocker remains for this
bounded type task. The shared HOME package should be refreshed to public013 by
the environment owner before relying on broad package diagnostics; that is
outside this worker's allowed scope.
