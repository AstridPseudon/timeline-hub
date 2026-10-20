# ACP proposal fixture — post-settings current-tip qualification

## Result

QUALIFIED the approved two-line test-only fixture delta from
`f0e4917ba27005a6022b4b0103ebf2e5c9447adb` on current App integration
`75df44e99bed22db39430e420d82764126c9a316`. The worktree changes only
`src/tools/video-editor/hooks/useAgentSession.proposal-vertical.test.tsx` and
adds the valid `/events` response shape:

```ts
: url.endsWith('/events')
  ? { notifications: [], disconnected: false }
```

The original prompt request, HTTP 403, `session_not_owned` expectation, and
`proposalApply` non-call assertion remain byte-identical. The original file
body is byte-identical after removing the approved two-line insertion, and the
working-tree patch is byte-identical to `f0e4917ba`.

## Evidence

All runs used the physical dependency tree `/tmp/app-m2-coherent-deps8/node_modules`
through the manager snapshot runner, with `--configLoader=runner --no-cache`
and `--maxWorkers=1`. Shared dependencies and caches were not modified.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
  /tmp/app-m2-coherent-deps8/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  src/tools/video-editor/hooks/useAgentSession.proposal-vertical.test.tsx \
  src/tools/video-editor/hooks/useAgentSession.test.tsx \
  src/tools/video-editor/hooks/useAgentSession.projectContext.test.tsx \
  --maxWorkers=1
# PASS: 3 files, 62 tests, exit 0
```

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
  /tmp/app-m2-coherent-deps8/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  src/sdk/examples-governance.test.ts --maxWorkers=1
# PASS: 1 file, 625 tests, exit 0
```

```sh
/tmp/app-m2-coherent-deps8/node_modules/.bin/eslint \
  src/tools/video-editor/hooks/useAgentSession.proposal-vertical.test.tsx
# PASS, exit 0

git diff --check
# PASS, exit 0
```

The final one-file/two-line audit passed, including exact patch comparison to
`f0e4917ba` and removal-of-insertion byte comparison to `HEAD`.

## Scope and limitations

No product source, route, parser, credential, guard, assertion, skip, or
expected-failure marker changed. No full suite, build, browser/e2e, TypeScript
check, install, live socket, or Agent/Runtime execution was run or claimed.
The manager should merge this test-only unit individually and obtain any
separate central full-suite evidence.
