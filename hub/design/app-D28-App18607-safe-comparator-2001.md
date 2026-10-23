# D28 App18607 safe comparator handoff — corrected finite report

## Scope and verdict

This is the finite, report-only correction required by the independent
`app-D28-comparator-review-2005` FAIL. It uses only retained artifacts; no
live probe, body rerun, environment triage, browser/service access, build,
preflight, collector, or Git mutation was performed. ProofSol1950 retains
ownership of the environment-equivalence and causal verdict.

The retained run is `app-P1-local-OPS-1830-ap2-P1-chain-h6-1023185313-18607`,
an actual direct-service run, not a synthetic or control run. It was requested
at `2026-10-23T18:53:13Z`, ended at
`2026-10-23T19:05:41.146658791Z`, ran for `744s`, and exited `1` with exactly
**1 PASS / 1 FAIL**. Environment equivalence remains **NOTPROVEN** and actual
cause remains **UNKNOWN**.

Case 1 passed in `27.4s`. Case 2 failed before its second commit: the retained
diagnostic saw `2` expected posts and `1` observed post; the original
`expect.poll` timed out after `90000ms`, then the failing-test `afterEach`
timed out after `300000ms`. The Agent move, HTTP 409 refusal, and App
rollback/message assertions were unreached. This does not assign cause to App,
Agent, Runtime, mounted save, outbox, or recovery.

Read-only retained inputs were the exact safe packet
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-P1-18607-result-custody.safe.json`,
the run summary under
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-P1-local-OPS-1830-ap2-P1-chain-h6-1023185313-18607/summary`,
the 1830 Remotion receipt
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-remotion-app-p1-787-2a9-1830.env`,
and the 1829 provision report
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/provision/venv-agent-child-app-p1-787-2a9-1829.txt`.
The prior raw files, logs, request, summary, and receipts were not modified.

## Field/source/member/line/case matrix

| Requested field | Bounded result | Retained source/member and line/case |
| --- | --- | --- |
| Startup boundary | `D21 passed; actual body executed` | Safe packet `preflight`; retained summary and original log |
| Backend, door, editor addresses; compiled Runtime HTTP base | `NOTCAPTURED` | No retained safe field supplies these values |
| WebSocket enabled/host/path | `NOTCAPTURED`; browser state remains `UNKNOWN` | No retained safe field supplies a WebSocket endpoint; the retained transport evidence is not a browser-state proof |
| Health / realm / handshake | Four retained readonly records and one retained wire-head record have status `200`; this is not a health, realm, authorization, or connectedness proof | Safe packet collector records; route/method observations only |
| Allowed-origin equality | `NOTCAPTURED` | No inference from source, setup, or `200` status |
| Credential/session presence | `NOTCAPTURED` | Values and auth scope intentionally excluded |
| Mounted project/timeline equality | `UNKNOWN` | Retained displayed/provider identity is not a mounted-equality proof |
| Actual authoring profile / quick descriptor | `NOTCAPTURED` | No retained body-safe field |
| Actual daemon Python | `NOTCAPTURED` | CLI/preflight receipts do not attribute the daemon |
| Actual `astrid.sdk.timeline.commit` origin | `NOTCAPTURED` | CLI/preflight origins are explicitly separate from daemon attribution |
| Actual `runtime_protocol` origin | `NOTCAPTURED` | CLI/preflight origins are explicitly separate from daemon attribution |
| Public Node executable | `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node` | Retained 1830 Remotion env receipt |
| Node / npm versions | Node `v20.19.4`; npm `10.8.2` | Retained 1830 Remotion receipt/provision report |
| Public Remotion project | `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830` | Retained 1830 Remotion env receipt |
| CLI installed `astrid` origin | `/home/user/work/venv-agent-child-app-p1-787-2a9-1829.partial.20261023T182941Z-12784/lib/python3.13/site-packages/astrid/__init__.py` | Retained 1829 provision report, `installed_import_origins` |
| CLI installed `astrid_runtime` origin | `/home/user/work/venv-agent-child-app-p1-787-2a9-1829.partial.20261023T182941Z-12784/lib/python3.13/site-packages/astrid_runtime/__init__.py` | Retained 1829 provision report, `installed_import_origins` |
| CLI installed `runtime_protocol` origin | `/home/user/work/venv-agent-child-app-p1-787-2a9-1829.partial.20261023T182941Z-12784/lib/python3.13/site-packages/runtime_protocol/__init__.py` | Retained 1829 provision report, `installed_import_origins` |
| CLI installed `astrid_runtime_client` origin | `/home/user/work/venv-agent-child-app-p1-787-2a9-1829.partial.20261023T182941Z-12784/lib/python3.13/site-packages/astrid_runtime_client/__init__.py` | Retained 1829 provision report, `installed_import_origins` |
| Playwright path/version | `NOTCAPTURED` | The retained summary supplies the invocation, not a browser path/version |
| Build command / dist path | Exact build command and dist path `NOTCAPTURED`; mode is `direct hosted dist`; retained log says hosted dist was current and build was skipped | Retained summary/log |
| Final application-row projection/hash | `NOTCAPTURED` | Diagnostic row hashes below are not a final application-state projection |
| Basis | `fields`; one basis item; `13` reads; field read states `UNKNOWN`, collection read `NOTCAPTURED` | Retained diagnostic records |
| Owner aggregate | `ownerCount=1`, `hasIdleOwner=true`; connection state `UNKNOWN` | Retained diagnostic records; no owner identity is reported |
| Safety/classifier denial | **STOP** | No alternate route or settings were used or proposed |

## Presence-only command environment

The exact retained body command explicitly removes `NODE_PATH` with `env -u
NODE_PATH`, so its **body-command presence is false**. It explicitly assigns
`NODE_OPTIONS` and `PYTHONPATH`, so their **body-command presence is true**.
This is a command-level observation, not a claim about every child process.

| Key | Body-command presence |
| --- | --- |
| `NODE_PATH` | `false` — explicitly removed |
| `NODE_OPTIONS` | `true` — explicitly assigned |
| `PYTHONPATH` | `true` — explicitly assigned |
| `ASTRID_QUICK_DESCRIPTOR` | `NOTCAPTURED` (not an unset claim) |
| `ASTRID_APP_DIRECT_DIST` | `NOTCAPTURED` (not an unset claim) |
| `ASTRID_APP_DIRECT_DOOR_PORT` | `NOTCAPTURED` (not an unset claim) |
| `ASTRID_APP_DIRECT_ORIGIN_PORT` | `NOTCAPTURED` (not an unset claim) |
| `VITE_RUNTIME_ORIGIN` | `NOTCAPTURED` (not an unset claim) |
| `VITE_WORKSPACE_RUNTIME_EXPECTED_*` | `NOTCAPTURED` (not an unset claim) |

No full environment, `PATH`, credentials, tokens, principals, realm values,
auth scope, headers, cookies, raw responses, unsanitized console/trace, or raw
log hash is included.

## Source, snapshot, member, and case identities

The selected source identities recorded for the actual clean run are App
`2107e1870e51c650d59315f4cc1ab6af338f198c` with tree
`a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`, Agent
`78738040d72ce74c42ddf7731221aecb06f9246d` with tree
`e77ea239789dd8ae9103c68fef79b49329cf2c6e`, Runtime
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` with tree
`f79a2355cfb39d9ada7721978bd20d5702105778`, and Composition
`635f4de06fda22a85fc2e4cfc764d0153a4c9f40` with tree unavailable. These are
selected source identities, **not** a synthetic snapshot tuple. Synthetic
`%H/%P/%T` are **UNKNOWN**; `%P` is unavailable, and no tuple is reconstructed
without authenticated Git-object evidence.

| Case/member | Retained line/boundary | Result |
| --- | --- | --- |
| `tests/e2e/local/three-products.p1-chain.spec.ts` case 1 | Source member begins at line `1055`; execution log line `9` | **PASS**, accepted split, merged trim after Agent edit, lost-ACK restart and exact retry; `27.4s` |
| Same test, case 2 | Source member begins at line `1223`; expected-post assertion at line `1255`; failing `afterEach` begins at `1043` | **FAIL** before second commit: expected `2`, received `1`; original assertion and `afterEach` timed out; Agent move/409/refusal and rollback/message checks unreached |
| `tests/e2e/local/p1-diagnostic-safety.ts` / retained diagnostic record | Safe-packet diagnostic line `10` | Line hash `623197e4bdc045754664412d01c9953c2ac12563dd378c1bdab14634dd02e079`; source-range hash `6400ec8183c629b1d83b9e578b62357cfd3b951f51f46574ec6ad59e73c1405d` |
| `tests/e2e/local/p1-diagnostic-safety.ts` / retained diagnostic record | Safe-packet diagnostic line `11` | Line hash `d9988f19348c0b7eeeb153b77bced2ee33457abdac6ffacf654e329c33c2192c`; source-range hash `ce8095346127435092a1a91279ee788513734695f34179fdd14cfa905ab0c59e` |
| Capped diagnostic record | Safe-packet line `12` | Capped/unparseable; unavailable suffix and final-row projection remain `NOTCAPTURED` |

The line-10/line-11 values are **diagnostic line/source-range hashes**. They
are not `suites.conf` execution-row hashes and must not be presented as such.

## Sanitized finite command projection

The retained exact public command is:

`npm run test:e2e:three-products -- tests/e2e/local/three-products.p1-chain.spec.ts`

Its retained Playwright projection is:

`playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.p1-chain.spec.ts`

For finite comparison, the sanitized command projection is the following two
lines, with assignment values intentionally removed:

```text
env -u NODE_PATH NODE_OPTIONS=<assigned> PYTHONPATH=<assigned> npm run test:e2e:three-products -- tests/e2e/local/three-products.p1-chain.spec.ts
playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.p1-chain.spec.ts
```

SHA-256 of that exact two-line UTF-8 projection (including its terminating
newline) is
`952564c4e3a49dc3da1ec59e1c60f8bfb76edff43f92f93b917d58485fd07bcc`.
This is a command-projection hash, not a raw-row, environment, response, or
log hash.

## Custody and unchanged wire boundary

Retained raw-log custody remains `26,440` bytes / `62` lines; safe-export
verification passed before and after export, and raw bytes were not rewritten.
The detailed capped record remains explicitly truncated/lost. No credentials,
auth keys, principals, realm values, tokens, auth scope, raw responses, full
request bodies, full success receipts, full environment, or unsanitized trace
is disclosed.

The production caller remains the mounted outbox. The full-v2 request boundary
is unchanged: `api_version`, `project_id`, `timeline_id`, `base_revision_id`,
`base_publication_id`, `commands`, `label`, `steps` (`id`, `label`, `intent`,
`tags`, `command_ordinals`, `patch`, `reads`), `merge`, `reads`, `key`,
`dry_run`, `source`, `rationale`, and `group_id`. Accepted, merged,
historical-rebased data and receipts, plus `head`, `document`, `records`,
`dependencies`, `effects`, `steps`, `history`, `undo_steps`, `preview`,
`would_status`, `conflict`, `current`, `invalid.code`, `invalid.path`,
`invalid.hint`, and `invalid.suggested_command`, remain unchanged.

## Checks and limitations

This correction changed only this absolute flat report and the normal owner
report outside the App repository. Tests, typecheck, and lint are **N/A** for
this read-only artifact correction. No product, test, preflight, browser,
body, service, build, environment, graph, binary, or Git change was made.
The App worktree remains clean. ProofSol1950 should continue the separate
environment-equivalence/causal assessment; no alternate setting or new probe
is authorized by this report.

