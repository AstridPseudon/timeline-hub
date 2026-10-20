# Selected CLI credential-file fixture source

## Result

Repaired the selected project-pack fixture's Agent child environment in
`tests/e2e/local/support/harness.ts`. The existing Runtime provisioner still
writes the already-issued selected credential as the existing `{token,
actor_id}` JSON file under the harness's private temporary root with mode
`0600`; `ASTRID_RUNTIME_CREDENTIAL` now carries that file's absolute path,
matching the frozen Agent CLI contract. The bearer token is no longer placed
in that child environment.

The browser/Door transport is unchanged: `startSelectedParamDevServer()`
continues to use `WORKSPACE_RUNTIME_TOKEN_FILE` for the product credential.
No Agent shim, product API, credential type/store/endpoint, inline token, pack
ID/history fabrication, or readiness/authority relaxation was added.

Added one offline regression covering path-versus-token semantics, restrictive
file mode and preservation of browser credential transport, plus harness
temporary-root cleanup/idempotent teardown after setup failure. It starts no
Runtime, browser, socket, or live transport.

## Verification

Passed:

- `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts` — 2 tests passed.
- Existing selected controls: `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/commands/selectedParamPort.test.ts src/tools/video-editor/commands/selectedParamAuthority.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx` — 6 files, 71 tests passed.
- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts tests/e2e/local/support/selected-param-credential.test.ts` — passed.
- `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- `./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list` — exactly 1 test listed.
- `git diff --check` — passed.

Not run: the real selected gate, `request-test`, browser/socket execution,
full suites, or any central qualification. Those remain pending independent
fixture-custody approval.

## Decisions and next steps

The existing credential-file carrier was reused because it already matches the
normal Runtime/Agent file shape and cleanup root. The focused helper makes the
child-only path boundary directly testable without changing product behavior.
The orchestrator should run the selected real gate only after custody review.
