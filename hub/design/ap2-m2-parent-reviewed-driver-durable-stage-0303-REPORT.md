# Parent reviewed-driver durable delivery

Completed the delivery-only handoff. The approved driver was copied byte-for-byte to the durable worker record:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-reviewed-driver-durable-stage-0303/run-parent-manual-drop-evidence.sh`

The durable file is 9,218 bytes, mode 755, and compares equal to Git object `fb07523d5d5c3f268c205b3f50a337b686357ea4` (`tests/e2e/local/support/run-parent-manual-drop-evidence.sh`). Its blob is `b760038b142e02e37b7879852c9f0be263bbf5ab`; its SHA256 is `9c3bd0c88df9290d78a3ba5838bb177f90d31494f5a235b9f7ea4682f05b877`.

Registered one new test-service row in `scratchpad/orch/tests/suites.conf`:

`app ap2-m2-parent-reviewed-driver-durable-stage-0303-e2e-integration env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-reviewed-driver-durable-stage-0303/run-parent-manual-drop-evidence.sh run "$PWD"`

New-row SHA256 (including its newline): `1f3e29f4560af0b9c7afc5cba5475482790519eda1f5b92fb90256462a9a3545`.

The old row was not edited. Its exact row SHA256 is `c4adb58aed2169d2344895912306651b1eb5842bbb6f6cb8edacf8d757394bc3`:

`app ap2-parent-mounted-add-da6d-final95-e2e-integration env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh run "$PWD"`

## Frozen source and callers

The frozen product/test source remains commit `da6d910f7ab3dfc71142ece7f632d43341238882`, tree `6809757f93ca5e166b24b8bc0160ca09005e984a`. The old driver bytes at that source have SHA256 `dca0da4b28547ae4296428f2bef529534f69c211bb6403f6b634e4177738206c`; they were not changed.

Current suite allow-list callers containing this driver name are:

- `suites.conf:34` — old relative `ap2-m2-parent-final-frozen-existing-add-0236` row.
- `suites.conf:42` — separate retained-evidence worker-record driver.
- `suites.conf:105` — old relative `ap2-parent-mounted-add-da6d-final95-e2e-integration` row.
- `suites.conf:106` — this new durable-driver row.

The two relative callers remain intentionally live and unchanged. The new row is the only caller of the reviewed durable copy.

## Guard evidence

No product, test-source, bootstrap, mixed-selector, shared dependency, artifact, or Git metadata files were modified. The source helper remains hashed `3dc9034586bf8c6fe2ff877b44fd1cbbabfb4eeeb1472fe009bad6d677811014`; the source runner remains hashed `8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e`.

The unchanged helper still selects `final95:parent` as `da6d910f/tree6809757f`, rejects other source roles, checks synthetic-commit ancestry, exact App tree and clean status, checks the locked App pin hashes, checks the locked graph/archive and Composition artifact, imports the Agent/Runtime modules, collects the native parent replacement test, checks producer ancestry, and verifies exact Agent/Runtime/producer HEAD trees. The approved durable bytes retain their exact evidence metadata pins (`agent=3c4f6de4fa777323b3386c01c7266b619b86af6d`, `runtime=202074110717146fc7f08af2306a8dd7f695b0b1`, `producer=a0dca16975dfe8f5e762703b99d9791a16cf7fd7`); no pin was edited.

The relocation/source-only check generated the approved driver’s temporary source runner, confirmed its absolute `normal014-source-common.sh` import, parent manual-drop required case, and parent `ACTUAL--list` selector. The unchanged bootstrap rows remain separate in `suites.conf:35-36`.

## Checks run

- `sh -n /tmp/.../run-parent-manual-drop-evidence.sh` — passed.
- From `/tmp`, `NORMAL014_RECORD_DIR=... sh /tmp/.../run-parent-manual-drop-evidence.sh probe` — passed; disposable probe evidence was cleaned up.
- Source-only transformed-runner syntax and selector checks — passed; parent selector present, bootstrap selector absent from the generated parent runner.
- `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR=... node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list` — passed; collected exactly 1 test:
  `three-products.spec.ts:1440:1 › M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data`.
- Exact old/new suite-row assertions — passed.
- `git status --short --branch` — clean worktree.

No browser, socket, build, install, full suite, or central actual request was run. No blocker was found. Recommended next step: the manager submits exactly one justified central rerun using the new named suite against the frozen `author0230`/`da6d910f` source only.
