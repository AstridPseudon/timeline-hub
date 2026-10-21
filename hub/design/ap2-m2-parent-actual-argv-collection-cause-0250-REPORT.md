# Parent manual ADD collection cause 0250

## Result

The 0236 failure was a selector pass-through defect in the App2 wrapper, before
any test assertion or browser request. The frozen App test source and the
normal014 source runner were not changed. The assigned App worktree changes
only `tests/e2e/local/support/run-parent-manual-drop-evidence.sh`.

The wrapper previously tried to replace a literal `--grep 'M2 real gate 5'`,
but the committed normal014 runner does not contain that argv. It assigns
`normal014_required_case` and later constructs the actual argv dynamically.
Consequently:

- PRELIST used the injected argv
  `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list`
  and collected the intended case.
- ACTUAL used the unchanged runner selector
  `--grep "^M2 real gate 5 bootstrap actual consumer: production initializer uses native create/init, exact retry, restart and guarded undo$"`
  with no file operand, so it selected the wrong case and returned `No tests
  found`.
- PRELIST and ACTUAL both use `playwright.three-products.config.ts` from the
  prepared overlay cwd (`<run-root>/app`), with the existing private-run
  variables only: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`,
  `TMPDIR=<run-root>/tmp`, `PWTEST_CACHE_DIR=<run-root>/pw-cache`, and
  `PLAYWRIGHT_OUTPUT_DIR=<run-root>/browser-output`.

The minimal wrapper fix rewrites the copied runner's required-case value to the
manual ADD case (preserving the structured exact-name summary guard), and
rewrites only its run-stage `normal014_playwright_grep` to the existing
supported substring selector. Bootstrap and private-spec/mixed-selector paths
in the source runner remain unchanged.

## Offline proof

The corrected copied-runner inspection showed:

```text
normal014_required_case='M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data'
normal014_playwright_grep="M2 real mounted manual video drop"
set -- --config playwright.three-products.config.ts --grep "$normal014_playwright_grep"
node node_modules/playwright/cli.js test "$@"
```

The exact resulting offline ACTUAL collection command was run from the App
worktree with private temporary/cache/output paths:

```text
node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list
```

Result: **PASS — 1 test in 1 file**, exactly:

```text
three-products.spec.ts:1440:1 › M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data
```

The anchored full-title selector was also checked offline and collected zero;
the supported substring is required because Playwright matches the selector
against its title path, which includes more than the displayed test title.

## Diff and identity

- Changed file: `tests/e2e/local/support/run-parent-manual-drop-evidence.sh`
- Diff: 2 insertions, 1 deletion
- Final changed-file SHA-256: `9c3bd0c88df9290d78a3ba5838bb177f90d31494f5a235b9f7ea4682f05b8775`
- Frozen normal014 runner SHA-256 remained `8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e`
- No changes to `three-products.spec.ts`, source pins, config, product code, or
  assertions.

## Live callers

- `scratchpad/orch/tests/suites.conf:34` — retained 0236 suite invokes the
  committed wrapper.
- `scratchpad/orch/tests/suites.conf:105` — frozen final95 parent ADD suite
  invokes the committed wrapper.
- The wrapper copies and invokes the existing external
  `normal014-app-central.sh`; the target case is
  `tests/e2e/local/three-products.spec.ts:1440`.
- The bootstrap normal014 suites at `suites.conf:35-36` invoke the source
  runner directly and are not affected by this parent-only copied-runner
  substitution.

## Checks

- `sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh` — PASS.
- `git diff --check` — PASS.
- `sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe` — PASS.
- Offline Playwright `--list` with the corrected ACTUAL argv — PASS, one case.

No browser, socket, central service, full suite, install, or retry was run.
The required independent process-custody review and manager new direction must
approve this exact wrapper change before one central rerun. No rerun or writer
deletion is qualified by this task.
