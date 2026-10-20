# App M3 Main574 bootstrap contract test

Date: 2026-10-20 UTC

## Scope and result

This is a test-only conversion for the one actual bootstrap-order failure from
`app-full8bd8-current-classification.md`. Product source was not changed.

- Assigned base commit: `d12d0909746c552dee6dac7b5d8459e8e1f27679`
- Assigned base tree: `c91e3c07f293658aa0f26dd180ac464c45b71559`
- Settled product source commit: `e4b1990667630efff626b9f031f0c972940ebc3a`
- Settled product source tree: `174902fca391db59fee6dd97cb8db4b954d4e5c3`
- Original test blob: `657ddc204660e0895ecaed349764348068f28384`
- Updated test blob: `4ca1f978a96c89e49d03687e1d332002191ecc1f`
- Changed files: 1
- Diff count: `21 insertions, 8 deletions`
- Test count retained: 5 (the bootstrap case, migration case, and both font
  `it.each` rows)

## Causal proof

`e4b199066` changed `src/app/main.tsx` to call
`initializeVideoEditorExtensionRuntime()` synchronously, await only
`initializeWorkspaceRuntimeIdentity()`, and then call `renderApp()` (current
lines 114–116). The same commit changed
`src/tools/video-editor/browser/initializeVideoEditorExtensionRuntime.ts` to a
non-async `void` function that installs best-effort analytics immediately
(current lines 16–19), with no release-config wait.

The old test supplied a deferred promise from the extension initializer and
treated that promise as the render gate. The updated one-to-one fixture supplies
a synchronous extension-install mock and keeps workspace identity deferred. It
records and asserts the exact sequence:

```text
extension-runtime-install -> workspace-runtime-identity -> render-app
```

Before identity resolves, it retains the negative guard that `renderApp` has
not been called. After identity resolves, it retains the root argument assertion
and verifies the final sequence. The migration failure guard and both font-link
cases are unchanged.

## Targeted evidence

Exact command (private `TMPDIR`, repository snapshot preload,
`--configLoader=runner`, `--no-cache`, one worker):

```text
TMPDIR="$RUN_DIR" NODE_OPTIONS="--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs" node node_modules/vitest/vitest.mjs run --configLoader=runner --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/app/main.bootstrap-order.test.tsx src/tools/video-editor/browser/initializeVideoEditorExtensionRuntime.test.ts
```

Result:

```text
Test Files  2 passed (2)
Tests       5 passed (5)
Duration    25.44s
```

No product bootstrap/source, auth-context, availability-guard, fatal-error,
build, TSC, browser, install, or full-suite changes/runs were made for this
task. The only non-test output was the existing Browserslist staleness notice.
