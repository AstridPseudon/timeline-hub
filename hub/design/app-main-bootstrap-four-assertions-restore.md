# App main bootstrap four-assertions restore

Date: 2026-10-20

## Change

Restored only `src/app/main.bootstrap-order.test.tsx` on source `8ffd2164bde532a50007d41376b0e10ce4d67473` (HEAD tree `6e67c65923031bc32a1502cc40d4e3b3bf123b64`). The worktree contains one modified file and no product-code change.

The source mapping is:

- Original before refresh: `0d5009e18bee8e29f894dabf5db501a0fcea750f:src/app/main.bootstrap-order.test.tsx:52-86`.
- Current restored test: `src/app/main.bootstrap-order.test.tsx:52-86`.
- The current mock setup and the existing migration/font tests were preserved.

The restored test retains all four required expectations:

1. `vi.waitFor` that the extension runtime initializer was called (`:77`).
2. `vi.waitFor` that workspace runtime identity initialization was called (`:78`).
3. The two-step bootstrap event order before identity resolves, then the final three-step order after resolution (`:79`, `:85`).
4. `renderApp` was not called while identity remained deferred (`:80`).

## Test evidence

Exact command:

```sh
TMPDIR=/tmp/timeline-app-m2-main-bootstrap-four-assertions-restore-cache \
XDG_CACHE_HOME=/tmp/timeline-app-m2-main-bootstrap-four-assertions-restore-cache/xdg \
VITEST_CACHE_DIR=/tmp/timeline-app-m2-main-bootstrap-four-assertions-restore-cache/vitest \
VITE_CACHE_DIR=/tmp/timeline-app-m2-main-bootstrap-four-assertions-restore-cache/vite \
NODE_OPTIONS='--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs' \
node /tmp/app-public13-pcm-complete-source-tsc-leaf13.01Xcjn/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism src/app/main.bootstrap-order.test.tsx
```

Result: passed; 1 test file and 4 tests passed under Vitest 4.1.5. The private13 dependency path reported React 18.3.1, React DOM 18.3.1, Remotion 4.0.509, and `@remotion/player` 4.0.509. `git diff --check` also passed.

The direct neighboring identity bootstrap test was not run because this restored test directly covers the current identity mock and passed. No full suite, project typecheck, build, install, browser/e2e, or shared-cache/dependency write was run.

## Decision / handoff

Used the exact pre-refresh test body from `0d5009e18bee8e29f894dabf5db501a0fcea750f`, adapted only by retaining the current file's unchanged mock setup. No skips, xfails, weakened assertions, new framework, or product changes were introduced.

Next step: merge the harness-produced commit containing this test-only change into the next App merge.
