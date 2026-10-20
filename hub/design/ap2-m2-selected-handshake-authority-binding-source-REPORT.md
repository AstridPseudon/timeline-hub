# Selected handshake authority binding — source only

## Result

Repaired the selected fixture's child environment, without changing authentication or product code. The Agent CLI now receives the existing complete `ASTRID_TIMELINE_EVAL_*` connection context used by `tests/e2e/local/support/astrid.ts`: the issuing DirectHarness Runtime's endpoint and realm, the selected actor, and its existing mode-0600 credential-file path. The ordinary `ASTRID_RUNTIME_ENDPOINT` / `ASTRID_RUNTIME_CREDENTIAL` host carriers agree with that context.

Source task complete; real selected journey **not qualified**. No browser, socket, request-test, full suite, build, App copy, package installation, shared dependency write, or wrapper execution was performed. Independent custody review remains required before a future real gate.

The assigned base is `41bf86102`, which predates the approved credential-file fix `50797493e81fd6fc1a6a61fa6ba01e65e154830d`. The resulting patch includes that approved file-path change and its two original regressions, then adds the issuer/target binding repair and one offline regression. Only these App files differ from the assigned base:

- `tests/e2e/local/support/harness.ts`
- `tests/e2e/local/support/selected-param-credential.test.ts`

## Causal evidence

Read the plan, approved-credential-real-gate-v2 report, retained sanitized `central-trace/driver.stderr`, the named central wrapper, and exact frozen Agent `8130a401bf44a518d5a40ae274d398b8c560be55` / Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` source with `git show`.

1. Agent `astrid/core/element/project_packs.py:64-66` opens `AstridClient.open_from_launcher(start_pack_host=False)` for project-pack operations. The retained trace reaches `client.py:396`, the ordinary launcher branch, then fails at the real `/v1/handshake` with `invalid bearer credential` before P1.
2. Agent `astrid/sdk/client.py:370-400` first calls `ensure_runtime()`, then reads the supplied `ASTRID_RUNTIME_CREDENTIAL` as a file path, and opens **the launcher's returned endpoint/realm/actor**. It does not select `ASTRID_RUNTIME_ENDPOINT` in that branch. Passing a correct file alone therefore binds the issuer's secret to a different endpoint.
3. Agent `astrid/sdk/storage_root.py:126-140` selects the explicit `ASTRID_RUNTIME_DATA_ROOT`. `autobootstrap.py:426-483` passes it to neutral Runtime `connect`/`up` and uses that result. The wrapper exports its independently created workspace root, source manifest and door-port override into the fixture's ambient environment.
4. DirectHarness instead creates and starts its own realm with `runtime_protocol.cli`. Its provisioner posts to **its own** `runtimeUrl + /v1/credentials`, using its own support-root owner file, then writes the selected actor's existing JSON credential file. Nothing provisions that credential into the wrapper's workspace.
5. Runtime `runtime_protocol/daemon.py:123-127` constructs the credential store under the daemon's own support root. `server.py:411-426` provisions/authenticates through that store; `auth.py:221-237` returns `invalid bearer credential` when no enabled credential matches. This is an authority/store mismatch, not a missing handshake scope or a credential JSON-format failure.

The exact target selection, using the retained run root `/tmp/ap2-m2-selected-p1.NJkY92` as `RUN_ROOT`:

| Binding | Credential issuer: DirectHarness | Original Agent CLI target: wrapper workspace |
| --- | --- | --- |
| Realm root | `<harness.tmp>/realm` | `RUN_ROOT/runtime-realm` |
| Realm identity | `runtime_protocol.cli create` result, stored as `harness.realmId` | `selected-p1-<wrapper PID>`, passed by `workspace create --realm-id` |
| Data/support root | `--support-root <harness.tmp>/support` | `ASTRID_RUNTIME_DATA_ROOT=RUN_ROOT/runtime-data`; daemon support is `RUN_ROOT/runtime-data/runtime` |
| Credential authority | `<harness.tmp>/support/credentials` | `RUN_ROOT/runtime-data/runtime/credentials` |
| Endpoint | `harness.runtimeUrl`, from its start result, `http://127.0.0.1:<harness.runtimePort>` | neutral `connect`/`up` result for `RUN_ROOT/runtime-data`; discovery under `runtime-data/runtime/discovery.json` |
| Supplied selected credential | `<harness.tmp>/selected-agent-credential.json`, issued as `astrid-selected-param` | The same file, incorrectly combined with the launcher's endpoint and expected identity |
| Browser door | Explicit harness `--door-port`, default 17340 | Ambient `ASTRID_RUNTIME_DOOR_PORT=18000 + wrapper PID % 1000` |

These are distinct realms and credential stores even though they run the same frozen Runtime source. The door-port override controls a browser listener, not the `/v1` daemon endpoint. It cannot bind the selected credential to its issuer. The sanitized trace does **not** retain the numeric daemon ports, generated harness realm UUID/tmp basename, or wrapper PID. Those concrete values cannot honestly be recovered after the wrapper removed its run directory; the source determines the paths and selection above. No live probing was performed to invent replacement observations.

Launch order also rules out minting the selected credential before the authoring restart: `seedSelectedParamDev()` awaits `enableTimelineAuthoring()` (stop/start and new endpoint discovery), then provisions the selected credential and builds the child environment. The later CLI launcher targets the wrapper workspace regardless of that correctly updated harness endpoint.

## Repair and preserved behavior

`selectedParamCliEnv()` binds all four existing CLI fields from the same harness that provisioned the credential, overriding any stale ambient context. The complete context takes Agent's existing `client.py:342-368` explicit-connection branch, also used by the neighboring three-product harness. That branch still calls ordinary `AstridClient.open()` with the owner-only file and expected realm/actor; normal health, handshake, protocol/schema and identity checks remain in place. No Agent changes or shim, new endpoint/credential type, auth bypass, public pin, save re-admission, or security change is needed. No product ownership gap was found.

The existing provisioner, selected credential file format/permissions, and harness teardown remain the carriers. The browser's `WORKSPACE_RUNTIME_TOKEN_FILE` remains the product credential path. The new offline test stubs only the provisioner's HTTP call (no sockets) and checks that its issuer URL matches the CLI endpoint, all identity fields override stale ambient values, the file is mode 0600, the browser path is preserved, and teardown removes the original file. The original two credential tests remain; failure cleanup now creates and checks removal of the actual file as well as its root.

The selected journey spec is byte-identical to approved `50797493` (SHA256 `2cd9703de2282282a477f5661d600049c8507fb93df1ef0424a06e7978a8b6a0`). Its genuine P1 admission, accepted native history, P2/source removal, P1 refusal, lost acknowledgement, exact retry/reload, undo and zero-legacy assertions are unchanged. Their live execution remains unverified by this task.

## Exact checks and results

All commands ran in `/home/user/work/wt/ap2-m2-selected-handshake-authority-binding-source`.

```sh
node --import tsx tests/e2e/local/support/selected-param-credential.test.ts
```

PASS: **3 tests** (the original 2 plus the binding regression). Also ran the requested `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts`: exit 0; on this Node/tsx combination its reporter aggregates the file as one test. Direct execution above reports all three subtests.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --no-cache --configLoader=runner --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/commands/selectedParamPort.test.ts src/tools/video-editor/commands/selectedParamAuthority.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
```

PASS: **6 files, 71 tests**, zero expected failures. The pre-existing two-line preload supplies `__dirname` for the runner loader; it was read only. Initial execution of the same Vitest command without that preload failed before tests with `ReferenceError: __dirname is not defined`. Used the existing loader workaround, without editing config or shared dependencies. Runner loading and `--no-cache` avoid writes to the shared node_modules caches.

```sh
./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts tests/e2e/local/support/selected-param-credential.test.ts tests/e2e/local/three-products.selected-param-dev.spec.ts
./node_modules/.bin/tsc --noEmit --pretty false
./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list
git diff --check
git diff --quiet -- src config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts
git status --short --untracked-files=all
```

PASS: lint, existing root typecheck invocation, whitespace, and product/spec scope check. Collection lists exactly the intended **1 test in 1 file**. Status contains only the two intended harness/test files; no build/temp output remains in the worktree. The root solution typecheck invocation is the existing preflight command, not a claim of a full application build.

## Next step

Independent custody review should confirm that the existing complete CLI connection carrier is bound to the credential issuer and that only fixture source changed. After that review, the orchestrator can separately authorize the named selected gate on the reviewed source. This task neither submits that gate nor claims P1/downstream qualification.
