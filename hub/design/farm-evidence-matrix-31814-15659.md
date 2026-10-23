# Farm evidence matrix: P2 31814 (+ preflight 14651) and P3 15659 (+ preflight 17114, bench2 preflights)

Producer: tf-evidence-matrix (the sole Farm producer, per D28). Date: 2026-10-23.
Scope: read-only over retained artifacts only. No browser, HTTP, service, test, build, graph, install, provision or remote probe. Nothing was modified or deleted.
Extends `design/farm-evidence-packet-31814-15659.md`, which is not redone here. Values are sanitized: no principals, credentials, headers, cookies, PATH or env dumps, request, transaction or revision identifiers.
`$ORCH` = `scratchpad/orch`. Paths below are relative to `$ORCH` unless absolute.

## 0. Key and runs

| Mark | Meaning |
| --- | --- |
| value | read from the retained file; citation is `file:line` |
| DECLARED | written in the row command text only; runtime presence not captured |
| INFERRED | follows from a passing assertion or stage in a retained log; the value itself is not printed |
| NOTCAPTURED | no retained text records it |
| NOTREACHED | the run stopped before the stage that would produce it |
| LOST | the artifact was present in the earlier packet and is absent on disk now (checked) |
| UNAVAILABLE | cannot be produced from retained files |

| Column | Run | Folder (under `tests/`) |
| --- | --- | --- |
| A | P2 body 31814, suite `ap2-P2-exact8`, requested 19:22:38Z | `app-ap2-P2-exact8-1023192238-31814/` |
| B | P2 preflight 14651, GREEN | `app-ap2-P2-exact8-preflight-1023192026-14651/` |
| C | P3 body 15659, suite `ap2-P3-gate5-h6-0348`, requested 19:06:26Z | `app-ap2-P3-gate5-h6-0348-1023190626-15659/` |
| D | P3 preflight 17114, GREEN | `app-ap2-P3-gate5-h6-0348-preflight-1023190416-17114/` |
| E1 / E2 / E3 | bench2 preflights 3794 / diag 29449 / diag2 30416 (earlier P3 preflight rows) | `app-ap2-P3-gate5-h6-0348-preflight-1023183150-3794/`, `…-preflight-diag-1023183451-29449/`, `…-preflight-diag2-1023183732-30416/` |

Inline P3 preflights: C ran its own preflight inside the body command, with diagnostics in `workers/tf-p3-bench2/p3-preflight.D79IrN/`. D's diagnostics are in `workers/tf-p3-bench2/p3-preflight.KA6ys9/`. E1, E2 and E3 used `…cyAmBC/`, `…pw4JrP/` and `…5m6Mmf/`.

Result of each run, from its `summary` line 1: A `fail exit=1 in 204s`; B `pass exit=0 in 97s`; C `fail exit=1 in 224s`; D `pass exit=0 in 97s`; E1 `fail exit=1 in 139s`; E2 `fail exit=1 in 107s`; E3 `pass exit=0 in 103s`.

## 1. What changed versus the existing packet

1. **The P2 snapshot commit is recovered.** Run A's snapshot is `39de9599896473ddbaa682cceca4d89a23b6ccea`. Its parent is `2107e1870`, its tree is `a3ff3584`, it is dated 2026-10-23 19:22:40Z, and its subject is `test snapshot app-ap2-P2-exact8-1023192238-31814`. It is an unreachable object in the shared object store and is on no ref. The existing packet noted that `snap` records tree, key and worktree but not the commit. The commit is recoverable by subject match.
2. **Run C's in-run Agent identity is logged, and it is `079580ca`.** `log.txt:12` (C) logs `appHead 43b71a9e…`, `astridHead 079580ca…`, `runtimeHead 2a9e347f…`, plus vendor locks and schema digests. `43b71a9e` is C's own snapshot commit, with parent `2107e1870`, tree `a3ff3584`, dated 19:06:37Z. The `ext` value `78738040` is declared metadata and was not the executed Agent. This resolves the identity conflict for C only. A has no in-run tuple, so its Agent identity is still the row pin plus an `ext` value that disagrees (see §6).
3. **The LOST items are confirmed absent.** `Glob` finds no `.test-app-ap2-P2-exact8-1023192238-31814` and no `.test-app-ap2-P3-gate5-h6-0348-1023190626-15659` directory, so their `test-results/` trace, error-context and snapshot folders are gone.
4. **`43b71a9e` now exists locally.** The Sol handoff and the existing packet say `git cat-file -e 43b71a9e` fails. `git cat-file -t` returns `commit` in this session, and the object is the C snapshot described above. This is a conflict of observations, not of content. The object's own metadata matches the packet.
5. **The P3 private graph is gone.** C and D used `/tmp/w-79d31cf50f/tf-p3-run4/private/node_modules`. That path no longer exists, so their composition and Playwright versions cannot be re-read. The P2 graph (`workers/tf-p2-run/graph/private/node_modules`) still exists.

## 2. Field 1: startup, public backend, door, editor, Runtime base, WS

| Field | A 31814 | B 14651 | C 15659 | D 17114 | E1 / E2 / E3 |
| --- | --- | --- | --- | --- | --- |
| Startup completion or error class | Completed to test start: `Running 8 tests using 1 worker` (`log.txt:8`). No startup error text. | Pass, exit 0 (`summary:1`). Native-seed GREEN (`log.txt:1`). | Completed through native seed (`log.txt:2`) and vendor-lock check (`log.txt:3`). Failed at owner predicate (`log.txt:13`, `:18`). | Pass, exit 0 (`summary:1`). `PREFLIGHT GREEN; body not run` (`log.txt:4`). | E1: fail after native seed; failing stage NOTCAPTURED (`log.txt:1–2` only; diagnostics show no error text). E2: fail at `realpath …/node_modules: No such file` (`log.txt:3`), a diagnostic-only mount gap. E3: pass, but `DIAG ONLY: private GRAPH mount and 80-file guard skipped` (`log.txt:3`), so E3 is not the exact environment. |
| Public resolved backend host and port | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| Hosted build origin (build-time, not Runtime) | None. The row's `npm run build` writes no origin line. | None. | `http://127.0.0.1:17340`, built by `npm run build:hosted` (`workers/tf-p3-bench2/p3-preflight.D79IrN/global-setup.log:1`) | `http://127.0.0.1:17340` (`…KA6ys9/global-setup.log:1`) | E1, E2, E3: same origin (`…cyAmBC/`, `…pw4JrP/`, `…5m6Mmf/` `global-setup.log:1`) |
| Door host, port, prefix | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| Editor origin | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| Editor path | `/tools/video-editor` (the `page.goto` in the failing source, `log.txt:35`) | n/a | n/a (path not in retained text) | n/a | n/a |
| Compiled Runtime HTTP base | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| WebSocket enabled, sanitized host or path | NOTCAPTURED. The handoff's source inspection says timeline saves and polls are HTTP; that is not run evidence. | same | same | same | same |

## 3. Field 2: health, realm, handshake, basis, allowed origin, credentials, mounted equality

| Field | A 31814 | B 14651 | C 15659 | D 17114 | E1 / E2 / E3 |
| --- | --- | --- | --- | --- | --- |
| Health, realm, handshake | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| Basis route, method, status, stage (native seed, not browser) | INFERRED: `GET …/timelines/{t}/commits?limit=50`, status 200 and `page.head` equal to the accepted revision and publication, from the passing native-seed stage (`log.txt:1`; the assertion text is in `summary:2`). | INFERRED, same route and assertion (`log.txt:1`). | INFERRED, same route and assertion (`…D79IrN/trivialboot.log:1`; `log.txt:2`). | INFERRED, same (`…KA6ys9/trivialboot.log:1`; `log.txt:2`). | INFERRED, same (`log.txt:2` of each E run). |
| Basis route in the browser | NOTREACHED or NOTCAPTURED. Browser traffic is not in retained text. | NOTREACHED (no browser stage) | NOTCAPTURED. The in-browser GET was in the lost trace. | NOTREACHED | NOTREACHED |
| Allowed-origin equality | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| Credential or session present (boolean) | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| Mounted project and timeline equality (boolean) | NOTREACHED. The comparisons are at `elements-assets.spec.ts:169` and `tour.spec.ts:147`, after the connected assertion that failed. | NOTREACHED | NOTREACHED. The owner predicate timed out first. | NOTREACHED | NOTREACHED |
| Mounted connection status | Element absent, not wrong state: `runtime-connection-status` not found, 5000 ms timeout (`log.txt:20–31`, the elements case at `:166`; `log.txt:84–95`, the tour case at `:144`). | NOTREACHED | NOTREACHED | NOTREACHED | NOTREACHED |
| Other backend answer seen | Popup fixture commit answered HTTP 422, expected 200 (`log.txt:56–65`). Body: `validation_error`, `details.code: capture_mismatch`, `status: invalid`, `conflicts: []`, `suggested_command: timeline edit`. Base and current identifiers are equal; values withheld. This shows a backend answered, not that it was healthy. | none | Owner claim predicate: `ready` expected `true`, received `false`, after a 90000 ms ceiling (`log.txt:18–33`, `:37`). Predicate source `log.txt:39–41`. Notice text collected but not printed. | none | none |

## 4. Field 3: authoring profile, daemon Python, module origins, Agent and Runtime source

| Field | A 31814 | B 14651 | C 15659 | D 17114 | Source |
| --- | --- | --- | --- | --- | --- |
| Authoring profile or quick-descriptor present | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | Not in row text or any retained log. |
| Daemon Python, declared | `/home/user/work/venv-agent-child-ap2-current-079-2a9-1743/bin/python`, passed as `ASTRID_PYTHON` and `ASTRID_RUNTIME_PYTHON` (`summary:2`). | same | same (`summary:2`) | same | row text |
| Daemon Python, asserted | INFERRED. The `actual-beforeAll` stage asserts `runtimePython() === ASTRID_RUNTIME_PYTHON` and passed (`tests/app-…31814/summary:2`, `workers/tf-p2-run/actual-beforeAll.log` 0 bytes). | INFERRED (`summary:2` of 14651) | INFERRED (the same assertion is in the body, `summary:2`) | INFERRED | row text |
| Daemon module paths, `astrid.sdk.timeline.commit`, `runtime_protocol` | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED (the row checks `astrid.sdk` imports, not paths) | NOTCAPTURED (`summary:2`, imports only) | |
| CLI-preflight module origins (provisioning) | `tests/provision/venv-agent-child-ap2-current-079-2a9-1743.txt:6–10`. These are `…/venv-agent-child-…partial.20261023T182854Z-5021/lib/python3.13/site-packages/{astrid,astrid_runtime,runtime_protocol,astrid_runtime_client}/__init__.py`. They are the staging path, not the final venv path. The final path is recorded only in `queue/done/childvenv-…:42`. | same | same | same | |
| In-run module file, logged by the test process | NOTCAPTURED (no tuple) | NOTCAPTURED | `astridFile = /home/user/work/wt/agt-pin-079580ca/astrid/__init__.py` (`log.txt:12`). Whether this is the daemon or the CLI is not stated. | NOTCAPTURED | |
| Agent source commit, in run | NOTCAPTURED. Row pin `079580ca…` (`summary:2`). The row's git guard passed (`summary:2`, stage progression), so the checkout was at the pin. | NOTCAPTURED (row pin; guard passed) | value `079580ca46af77e0292d49dc34386b25c8391f99` (`log.txt:12`) | row pin, guard passed (`summary:2`) | |
| Agent `ext` (declared external pin) | `9a095a95178e0bb89ef3b2024d6502d47b35ac25` (`ext:1`), which disagrees with the row pin. Declared metadata, not verified in run. | same (`ext:1`) | `78738040d72ce74c42ddf7731221aecb06f9246d` (`ext:1`), which disagrees with the in-run `079580ca`. | `78738040…` (`ext:1`) | |
| Runtime source commit, in run | NOTCAPTURED; row pin `2a9e347f`; guard passed | same | `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` (`log.txt:12`) | same as C | |
| Vendor lock and schema digests | NOTCAPTURED | NOTCAPTURED | `log.txt:12`: app and astrid `source_commit 34eac004…`, `producer_version sha256:d5f98db3…`, `schemaDigest sha256:35c2d9c5…` | NOTCAPTURED | |
| CLI provisioning source identities | `queue/done/childvenv-venv-agent-child-ap2-current-079-2a9-1743:1` gives `agent=079580ca`, `runtime=2a9e347f`, `requirements/proof.lock`, lock `236d5be9…`. `tests/provision/…txt:2–5` agrees. `queue/done/childvenv-…:43` says `imports validated: astrid astrid_runtime runtime_protocol astrid_runtime_client`. | same | same | same | |

Why this matters: every row invocation sets `PYTHONPATH="$PWD:$RT:$AG"` (the App worktree, the Runtime checkout and the Agent checkout) and then runs the child-venv interpreter (`summary:2` of A, B, C and D). If the daemon inherits that environment, its `astrid` and `runtime_protocol` imports resolve to the checkouts, not to the venv copies in the provisioning report. The daemon's environment is not captured, so this is UNKNOWN, not established.

## 5. Field 4: per-stage presence, Node and npm paths, build command

Presence is by row text or by retained log. No runtime environment was captured.

| Name | A 31814 | B 14651 | C 15659 | D 17114 |
| --- | --- | --- | --- | --- |
| `ASTRID_QUICK_DESCRIPTOR` | NOTCAPTURED (absent from row text and all retained logs) | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| `ASTRID_APP_DIRECT_DIST` | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| `ASTRID_APP_DIRECT_DOOR_PORT` | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| `ASTRID_APP_DIRECT_ORIGIN_PORT` | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| `NODE_PATH` | DECLARED absent: every invocation uses `env -u NODE_PATH` (`summary:2`) | DECLARED absent (`summary:2`) | DECLARED absent (`summary:2`) | DECLARED absent (`summary:2`) |
| `NODE_OPTIONS` | DECLARED. Build step `--max-old-space-size=6144` (`summary:2`, `npm run build`). Preflight and body env base `6144`. Body invocation `6144`. | DECLARED `6144` (env base and build) | DECLARED. Global-setup and preflight env base `6144`. Body invocation `--max-old-space-size=4096` (`summary:2`). | DECLARED `6144` (env base) |
| `PYTHONPATH` | DECLARED `$PWD:$P2RT:$P2AG` (checkout paths) | DECLARED same form | DECLARED `$PWD:$P3RT:$P3AG` | DECLARED same form |
| `VITE_RUNTIME_ORIGIN` | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |
| `VITE_WORKSPACE_RUNTIME_EXPECTED_*` | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED | NOTCAPTURED |

The `ASTRID_*` set above is what the row exports. A also carries `ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages` (`tests/agent-remotion-ap2-current-079-2a9-1743.env:4`). That is a third Python source, separate from the child venv. The Remotion receipt's first line is the PATH, which is withheld; it prepends the Node 20 toolchain bin directory.

**Paths and versions (public).**

| Item | Value | Source |
| --- | --- | --- |
| Node executable | `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, `v20.19.4` | `tests/agent-remotion-ap2-current-079-2a9-1743.env:3`. The row check `"$NODE" --version = v20.19.4` passed in A, B, C and D, by stage progression (`summary:2`). |
| npm CLI | `$(dirname NODE)/../lib/node_modules/npm/bin/npm-cli.js` → `/home/user/work/toolchain/node-v20.19.4-linux-x64/lib/node_modules/npm/bin/npm-cli.js`, version `10.8.2` | `summary:2` (row check); `queue/done/runtime-agent-remotion-ap2-current-079-2a9-1743:11` |
| Remotion project | `/home/user/work/runtimes/agent-remotion-ap2-current-079-2a9-1743`, lock `f4fc0a32…be18d` | `tests/agent-remotion-ap2-current-079-2a9-1743.env:2`; `queue/done/runtime-…:16` |
| Playwright, A and B graph | `@playwright/test` `1.60.0` at `workers/tf-p2-run/graph/private/node_modules/@playwright/test/package.json:3` (current file state; the row does not check it) | file read |
| Playwright, shared App install | `1.60.0` at `/home/user/work/app/node_modules/@playwright/test/package.json:3`. App `package.json:164` has `^1.60.0`. | file read |
| Playwright, C and D graph | UNAVAILABLE (graph path deleted). Shared install is `1.60.0`, which is inference only. | |
| `@banodoco/timeline-composition`, A, B graph | `0.0.14` (`workers/tf-p2-run/graph/private/node_modules/@banodoco/timeline-composition/package.json:3`); the row asserts 80 files and 0.0.14, and passed | `summary:2` |
| `@banodoco/timeline-composition`, C, D (run-time) | 0.0.14 by the row assertion, which passed (C and D reached GREEN and the body). Graph gone now. | `summary:2` |
| `@banodoco/timeline-composition`, shared install | `0.0.13` (`/home/user/work/app/node_modules/@banodoco/timeline-composition/package.json:3`). The P3 run did not use it. | file read |

**Build commands.**

| Run | Exact command (row text) | Mode | Output and dist |
| --- | --- | --- | --- |
| A | `NODE_OPTIONS=--max-old-space-size=6144 npm run build >"$ORCH/workers/tf-p2-run/hosted-build.log" 2>&1` (`summary:2`) | Vite production; `vite v5.4.21 building for production` (`hosted-build.log:5`) | `dist/` in the App worktree; `✓ built in 1m 3s` (`hosted-build.log:112`); sha `327b69cd…` verified |
| A | Beforeall stage writes to `$ORCH/workers/tf-p2-run/actual-beforeAll.log` | none | 0 bytes; sha `e3b0c442…` verified. Last writer is A, so this file reflects A |
| B | Same build command, to the same `hosted-build.log`; this file was overwritten by A | Vite production | Build output for B is lost |
| C | Build by `global-setup` under `ENV_BASE` (`NODE_OPTIONS=--max-old-space-size=6144`), `node --import tsx --input-type=module -e 'import setup from "./tests/e2e/local/global-setup.ts"; await setup()'`. It runs `npm run build:hosted` for `http://127.0.0.1:17340` (`D79IrN/global-setup.log:1`). | Vite production (`:6`) | `dist/` in `/home/user/work/wt/.test-app-ap2-P3-gate5-h6-0348-1023190626-15659` (worktree path in `D79IrN/global-setup.log:16`; the directory is now absent); `✓ built in 1m 3s` (`:113`) |
| D | Same as C, for `http://127.0.0.1:17340` | Vite production | `KA6ys9/global-setup.log:113`: `✓ built in 1m 5s` |
| E1 / E2 / E3 | As C | Vite production | `cyAmBC`: 1m 31s. `pw4JrP`: 1m 12s. `5m6Mmf`: 1m 9s. (`global-setup.log:113` each.) |

Build output caveat: the 'OOM' justification for raising the heap in A is not supported by retained files. The only retained build log is a successful build. The packet already says this and this matrix confirms it.

## 6. Field 5: final row projections, hashes, snapshots, owner records

**Row projections (sha256 of the command bytes after `app <suite> `, no trailing newline; `tests/suites.conf`).** `suites.conf` is still `64afaf615665def79f3660d771f17e226c83fa58223417f5dd11d8cc6227d61d`, unchanged since the packet.

| Row | Line | Bytes | sha256 | Status |
| --- | --- | --- | --- | --- |
| `ap2-P2-exact8` body (A) | 158 | 12,368 (packet) | `7ee460f69cbeb6224adc42f08af65fa9be5e7182776adfde91f0edfc78933daa` | verified now |
| `ap2-P2-exact8-preflight` (B) | 159 | 11,814 (packet) | `f3d02ff945ee5d83f85696f9258655ca166323b236be1851e392b8381d1e1e41` | verified now |
| `ap2-P3-gate5-h6-0348` body (C) | 154 | 23,792 | `b40072a8b8c5b13dd71618b4e0efda6f33e33030269838b179a65829b5cdcf3b` | computed now, not in the earlier packet |
| `ap2-P3-gate5-h6-0348-preflight` (D) | 155 | 23,343 | `20a9702ae3d3fe9e94b7feb35183510b25399a7f93bf8845a67da9302141208f` | computed now |

P2 body changes 1–6 and the ratified Node path, log redirects and build heap are in the packet §1. The P3 rows use the same Remotion Node path and the same `hosted` build via global-setup. The P3 rows have no `npm run build` step, so the P2 log-redirect edits do not apply to them except for `global-setup.log` and `actual-beforeAll.log`, which are written to the bench2 diagnostic folders.

**Historical App snapshots (`%H / %P / %T`).**

| Run | %H (snapshot) | %P | %T | Date (UTC) | Subject |
| --- | --- | --- | --- | --- | --- |
| A, P2 31814 | `39de9599896473ddbaa682cceca4d89a23b6ccea` | `2107e1870e51c650d59315f4cc1ab6af338f198c` | `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c` | 19:22:40 | `test snapshot app-ap2-P2-exact8-1023192238-31814` |
| B, P2 preflight 14651 | `ad415533cb3b9f25dac5c2ed768167b630061ce0` | `2107e1870…` | `a3ff3584…` | 19:20:40 | `test snapshot app-ap2-P2-exact8-preflight-1023192026-14651` |
| C, P3 15659 | `43b71a9e3e09097367556a1c04558f66aad7a3ff` | `2107e1870…` | `a3ff3584…` | 19:06:37 | `test snapshot app-ap2-P3-gate5-h6-0348-1023190626-15659` |
| D, P3 preflight 17114 | `e028c1323235f0c321ca8867e99381d541909baa` | `2107e1870…` | `a3ff3584…` | 19:04:22 | `test snapshot app-ap2-P3-gate5-h6-0348-preflight-1023190416-17114` |
| E1 3794 | `f7da74962a0ea24ac955e1b3fe6dc405feea6f65` | `2107e1870…` | `a3ff3584…` | 18:32:03 | `…preflight-1023183150-3794` |
| E2 29449 | `05a14e4b76cb17accbd5dc3973768fb3d72afdbf` | `2107e1870…` | `a3ff3584…` | 18:35:03 | `…preflight-diag-1023183451-29449` |
| E3 30416 | `11a152ab0bc897339608097854bad8fc66ced3e6` | `2107e1870…` | `a3ff3584…` | 18:37:33 | `…preflight-diag2-1023183732-30416` |

Reference: `2107e1870e51c650d59315f4cc1ab6af338f198c` has parent `3a0d76503a11451f91a5c9b18f9fcb74d009b247`, tree `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`. All snapshots above are unreachable objects found by `git fsck --unreachable` and read with `git show -s`.

The snapshot tree is the App tree and the in-run `appHead` of C equals its snapshot commit. So the in-run HEAD of A is inferred to be `39de9599`, but it was not logged in-run.

**Retained connected or owner records (read-only, no re-run).**

| Run | Case | Time | Error class |
| --- | --- | --- | --- |
| A | `elements-assets.spec.ts:376`, mounted element edit | 5000 ms, `openTimeline` at `:166` (`log.txt:20–31`) | `runtime-connection-status` element not found. Not a wrong state. |
| A | `tour.spec.ts:564`, mounted single parent move | 5000 ms, `openCommandTimeline` at `:144` (`log.txt:84–95`) | Same class |
| A | `popup.spec.ts:807`, mounted ADD fixture | HTTP 422 at `commitFixtureCommand` (`log.txt:56–65`) | `validation_error`, `capture_mismatch` |
| C | `three-products.spec.ts:1533`, M2 gate 5 | 90000 ms predicate, `openCommandTimeline` at `:1275` from `:1537` (`log.txt:18–33`) | Owner not claimed: `ready` false. Predicate fields are `ownerId` new, `pending` false, `intents` empty, `notice` (text not printed). |
| B, D, E1–E3 | preflights | none | none recorded |

Five A tests did not run (`log.txt:122`). The log does not say why. Source-derived reason: each spec file has `test.describe.configure({ mode: 'serial' })`, so a failure in one test skips the rest of that file. This is source-derived, not captured.

**LOST, confirmed absent.** Trace, error-context and snapshot folders for A and C: none exist on disk (`Glob` on `/home/user/work/wt/.test-app-…`).

## 7. Verified hashes (sha256, read now)

| File | Verified value |
| --- | --- |
| `tests/app-ap2-P2-exact8-1023192238-31814/log.txt` | `5cf1a7a8b14bd7afe8c796164ce63605bfbe7500670b943e323fdfd84bed3eb3` (matches packet) |
| `tests/app-ap2-P3-gate5-h6-0348-1023190626-15659/log.txt` | `d3d07149d0fc6951cb2befe7d60023487c47f9e341896fbdd45ea21f64248a43` (matches) |
| `tests/app-ap2-P2-exact8-preflight-1023192026-14651/log.txt` | `6862c59ca8638158e3b621bd761a313a3f7d20dd38d5d40f93d3aae4f58c11df` (matches) |
| `tests/app-ap2-P3-gate5-h6-0348-preflight-1023190416-17114/log.txt` | `f86ff99032e8da2e76fd63551e5cb3c9a315798eda402b44df9c7c5a40864f52` (new) |
| `workers/tf-p2-run/hosted-build.log` | `327b69cd97b3c7c9997bac0dbf0f9503ac9f7d9675c8627c2e446e1d7fff5725` (matches) |
| `workers/tf-p2-run/actual-beforeAll.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, 0 bytes (matches) |
| `…p3-preflight.D79IrN/trivialboot.log` and `…KA6ys9/trivialboot.log` | both `c969e85b96362e40624007944deb1916810a59d2a8b11cb1b81c03a97704e464` (matches) |
| `tests/suites.conf` | `64afaf615665def79f3660d771f17e226c83fa58223417f5dd11d8cc6227d61d` (unchanged) |

## 8. Discrepancies and open items for app2 and the orchestrator

1. **Agent identity, P2 A.** Row pin `079580ca`; `ext` `9a095a95`; no in-run tuple. Still unresolved. For C, the in-run tuple resolves it to `079580ca`, which makes `78738040` in `ext` the wrong declared metadata. A's `ext` is also declared metadata. Treat it that way unless an in-run tuple for A shows otherwise.
2. **Daemon environment.** Every row sets `PYTHONPATH` to the checkouts. The daemon's environment is not captured. Whether it imports checkout or venv modules is UNKNOWN.
3. **Provisioning origins point to the staging path.** `tests/provision/…txt:6–10` records `…partial.20261023T182854Z-5021/…`, while the receipt gives the final path. The rename is not recorded. Treat the recorded origins as historical.
4. **Bench2 E3 PASS is not exact.** It skipped the graph mount and the 80-file guard (`E3 log.txt:3`).
5. **Graph re-verification for C and D is impossible.** Their graph path was deleted. The P2 graph is still present.
6. **43b71a9e discrepancy.** Sol's `cat-file` says absent; now present, and it is C's snapshot. Content matches.
7. **Earlier packet errors remain corrected.** The "8 passed" claim and the build-OOM justification are still unsupported.

## 9. Process notes

- Read-only throughout. Only `Glob`, `Grep`, `Read` and single-operation `git -C <repo> cat-file`, `show`, `fsck --unreachable` and `log --all` calls were made. The `fsck` and `log --all` searches read only. No file was written under the App, Agent, Runtime or Composition repos, and nothing was installed, built or run.
- Several Bash calls were refused by the command reviewer. The first required approval for a compound read, and a later one used a shell variable and a write into the worker `tmpdir` pointer file. I did not retry them. I switched to read-only tools or single operations that do the same reads. No file was written to `tmpdir`.
- The NODE_OPTIONS values above are the command text, not runtime values, and they are not secret. Other env names are presence-only, and where the runtime is not captured they are NOTCAPTURED.
