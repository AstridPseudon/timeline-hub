# Parent final95 driver composition and preflight

## Result

Composed the existing parent driver from the correct base `da6d910f` / tree
`6809757f`, then applied only the approved selector delta from `fb07523d`.
The only product worktree change is:

`tests/e2e/local/support/run-parent-manual-drop-evidence.sh`

The current final95 source guard, current tuple metadata, evidence handling,
environment, and test source remain unchanged. The old `fb07523d` App tree
guard (`78f37842`) and old metadata (`3c4f` / `202074` / `a0`) were not copied.

Because the existing `probe` only checks the evidence trap, I added a small
`preflight APP_ROOT` mode that uses the same `run_gate` guard as `run` and
invokes the existing transformed `normal014-app-central.sh preflight`.
No second validator or source authority was added. The preflight entry point
was not executed: the existing underlying preflight performs a hosted build,
private dependency installation, Chromium validation, and Playwright
collection, all explicitly out of scope for this task.

## Checks

All commands were run without a build, browser, socket, central request, full
suite, or install.

- `sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh` — passed.
- `sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe` — passed.
- `git diff --check` — passed.
- The exact run guard checks against a clean `da6d910f` source snapshot
  (`merge-base` ancestry, clean status, tree `6809757f`) plus the existing
  `normal014-source-common.sh` `verify_app_source` guard — passed.
- Controlled source-guard negatives using the same existing helper — all
  refused: old tree `78f37842`, wrong source `fb07523d`, wrong runtime-lock
  pin, and missing `APP_ROOT_TREE` provenance.
- Existing actual selector argv, with private temporary/cache/output paths:

  `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list`

  — passed and listed exactly one case at
  `three-products.spec.ts:1440`.
- The old bootstrap selector with `--list` — refused with `Error: No tests
  found` and zero tests.
- Static transformed-runner inspection — passed: the required-case summary
  remains exact, while the actual run selector is the approved manual-drop
  substring.

The mounted source-only preflight itself is intentionally unverified because
running it would violate the no-build/no-install boundary. No mounted ADD
body, recovery, reload, retry, undo, raw/opaque, or `zeroLegacy` behavior is
qualified here, and no actual request was made.

## Candidate identity and durable staging

- Candidate parent commit: `da6d910f7ab3dfc71142ece7f632d43341238882`.
- Candidate parent tree: `6809757f93ca5e166b24b8bc0160ca09005e984a`.
- Working-tree driver SHA-256: `038e73f7b903b31bd073bce2c9f5e84a1beb5991c38c97620e9d920448ef9366`.
- Working-tree driver Git blob: `1e9235496acb53b61f51fb151e9cca7de7a38433`.
- Binary diff SHA-256: `29fd05d688409d8af34e66eed0aefb27001393d565167f376de448c6ec853927`.

The harness should commit this one-file candidate with the supplied commit
message. After review, durable staging must copy this final driver byte-for-
byte and record the resulting SHA-256 separately. Do not stage the whole
`fb07523d` file, and do not submit a central request from this worker. The
eventual run must continue to use the service's `author0230` snapshot and the
closed `da6d910f/tree6809757f` source guard.

## Live callers

Registered driver callers remain `scratchpad/orch/tests/suites.conf:34`, `:42`,
`:105`, and `:106`; no suite file was changed here. The mounted product path is:

`TimelineEditorCore.tsx:941` → `useExternalDrop.ts:612-630` →
`external-drop-utils.ts:275,375` → `useAssetManagement.ts:274-309` →
`useTimelineCommandsService.ts:458-500` →
`useTimelineCommandSession.ts:271-284`.

## Commit message

`fix(app): compose final95 parent driver preflight`

The commit message was written to the requested worker commit-message path.
