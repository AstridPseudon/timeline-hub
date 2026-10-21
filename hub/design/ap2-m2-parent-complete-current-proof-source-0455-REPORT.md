# App2 M2 parent complete current proof source

## Result

Prepared the final parent proof source on current App HOME base
`bc6f9dd39c7e5154ddf075cb87b7202cf5702e65` (base tree
`4cd13d09b7cffd60612d8521f1a2921ca4e762d2`).

Before editing, verified that both required ancestors are present:

- local skeleton `5d36b0e53ff0d17ef045e226a6e6ca7584322858`;
- existing ADD-port forwarding merge `968bbad09449f419ab63782fca49cad805068333`, including forwarding parent `940b7f42a9042f12c81d3370acf90ddf7ca6e3d6`.

Ported only the two frozen proof-file changes from
`b833512fcb5ef07013c47fcf8c75c4a083048d99` /
tree `a95793cc2179200dd9ef5fe551360a4f6f965ea1`:

- `tests/e2e/local/support/run-parent-manual-drop-evidence.sh`: restored the frozen existing parent proof driver, final95 parent role metadata, preflight mode, ancestry guard, and zero-test/failure-trap behavior.
- `tests/e2e/local/three-products.spec.ts`: restored strict HTTP 404 and the exact `not_found` response body for the wrong verified selection.

The second file retains the current HOME mounted ADD path and all existing raw/opaque/order, lost-ACK, reload/restart, exact-body/key retry, undo, and zero-legacy assertions. Qualified native bootstrap and initializer code were not edited. No shared helper, wrapper, graph, source authority, or product code was added; driver metadata is exactly the frozen packet, with no invented or changed pin.

Changed live callers: none. Only the two requested proof files are modified.

## Checks

All passed:

- `sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh`
- `TMPDIR=<private temp> NORMAL014_RECORD_DIR=<private temp>/evidence sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe` — zero-test child refused; failure-trap evidence copied before cleanup.
- `TMPDIR=<private temp> PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list` — exactly 1 test collected.
- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.spec.ts`
- `git diff --check`
- `git diff --exit-code b833512f -- tests/e2e/local/support/run-parent-manual-drop-evidence.sh tests/e2e/local/three-products.spec.ts` — both proof files match the frozen packet.
- Diff scope check — exactly the two requested files; no `src` or shared helper changes.
- Normal ignored `node_modules` symlink retained; it resolves to `/home/user/work/app/node_modules`.
- Worker-record `KEEP` created.

No build, browser execution, mounted actual, or full suite was run, as required.

## Decision / next step

The shared `normal014-source-common.sh` helper was intentionally not edited. After the harness commits/freezes this source, the next binding task should update only its closed `final95:parent` case to the resulting exact App SHA/tree and preserve every other role and guard. The final post-harness commit/tree is not available in this worker because Git metadata is read-only.

