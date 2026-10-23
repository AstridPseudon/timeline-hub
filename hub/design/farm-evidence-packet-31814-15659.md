# Retained-evidence packet: P2 run 31814 and P3 run 15659

Worker: tf-evidence-packet. Scope: read-only over already-retained artifacts (app2 requests 19:39Z "P2 actual FAIL retained" and 19:28Z/19:37Z "Preserve/extract existing P3 15659 trace"). No browser, HTTP, test service, graph build, npm, install or new run. Nothing was modified or deleted. Raw files are private in `workers/tf-evidence-packet/private-raw/` (not published here).

## Headline

| Item | Status |
|---|---|
| P2 31814 result | fail exit 1 in 204 s; 3 failed, 5 did not run, 0 passed (log.txt) |
| P3 15659 result | fail exit 1 in 224 s; 1 test, owner-claim predicate timeout at 90 s |
| trace.zip, error-context.md, snapshot folders for 31814 and 15659 | **LOST**. The `.test-app-*` snapshot folders are gone. Searched: `tests/` tree (no `*.zip`, no `error-context.md`), `/home/user/work/wt/.test-app-*` (none), `/home/user/work/app/test-results` (absent). |
| Mounted provider identity, basis GET, authenticated identity, owner creation, settled record, console/pageerror | **UNKNOWN**: not in any retained text. No file records them. |
| Agent head for the two runs | **Conflict, unresolved**: the row pins `079580ca…`; the run `ext` files record `9a095a95…` (P2, all preflights) and `78738040…` (P3). See §2. |

Two corrections to earlier worker documents (design/farm-p2-run.md and design/farm-p3-15659-trace-extract.md), verified below:
1. The P2 "build aborted with V8 old-space OOM" justification for change 6 is **not supported by any retained file** (§5).
2. The preflight row differs from the body row by the whole Playwright launch segment, not only "the final npm run" (§1).

## 1. Row bytes, hashes and changes (suites.conf)

Source: `tests/suites.conf` (sha256 `64afaf61…d61d`, 197,440 bytes, mtime 19:20). Lines 158 and 159 are `app <suite> <command>`; the body hash is over the command bytes after `app <suite> `, no trailing newline. Private copies: `private-raw/rows/registered-body.cmd`, `registered-preflight.cmd`.

| Row | Bytes | sha256 | Note |
|---|---|---|---|
| `ap2-P2-exact8` (registered, final) | 12,368 | `7ee460f69cbeb6224adc42f08af65fa9be5e7182776adfde91f0edfc78933daa` | changes 1–6 |
| `ap2-P2-exact8-preflight` (registered, final) | 11,814 | `f3d02ff945ee5d83f85696f9258655ca166323b236be1851e392b8381d1e1e41` | body prefix ending `… && eval "$P2_ENV"`; removes 554 bytes = ` && env -u NODE_PATH … npm run test:e2e:three-products -- <3 spec files>` |
| worker `p2-row-before.cmd` (packet row) | 12,339 | `d4f6fe75a0a9110cc82f537c56060ad6b7169ec2b92cc12e01b1c81d4950a009` | = line 77 of `design/peer-app2-to-farm-20261023T1756-P3-P2-run-handoff.md` (checked: `sed -n 77p | tr -d '\n' | sha256sum`) |
| worker `p2-row-after.cmd` | 12,326 | `685c0fead4e5e7bde3c2c95cb0d3ad41647e674b068740d4d91d3889249d585b` | changes 1–3 |
| worker `p2-row-after-node.cmd` | 12,261 | `14275712108064c789f86f88d7ee89899250fb78c7383cca97b47b16b11a916a` | changes 1–4 |
| worker `p2-preflight-after.cmd` | 11,772 | `cd2d5b6446ac0e84d24b7a1286d709e04045b6b2003bb445c1714e3e3b4a0ce2` | changes 1–4, preflight |

The worker copies stop at change 4. **The registered rows also carry changes 5 and 6**; the final hashes are the registered ones above (the worker design doc said "not recomputed after 4–6"; it is now computed).

Token-level diff, packet row (`d4f6fe75`) → registered body (`7ee460f6`), changed tokens only:

| # | Change | Before | After |
|---|---|---|---|
| 1 | `P2APP` | `58bf24ce6fc57c7477a7fa45d94b20dfb12c5e92` | `2107e1870e51c650d59315f4cc1ab6af338f198c` |
| 2 | `P2TREE` | `07f99905cb822656a2d3675a782b72e6c1fb5ecb` | `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c` |
| 3 | `GRAPH` | `…/workers/ap2-P3-env-final-0407/record/private/node_modules` | `…/workers/tf-p2-run/graph/private/node_modules` |
| 4a | Remotion Node | `NODE="/home/user/work/runtimes/$RN/.toolchain/node-v20.19.4-linux-x64/bin/node"` | `NODE=$(sed -n "s/^ASTRID_NODE_EXECUTABLE=//p" "$RENV")` |
| 4b | npm-cli path (**not in the earlier design table**) | `/home/user/work/runtimes/$RN/.toolchain/node-v20.19.4-linux-x64/lib/node_modules/npm/bin/npm-cli.js` | `"$(dirname "$NODE")/../lib/node_modules/npm/bin/npm-cli.js"` |
| 5a | build log | `npm run build >/dev/null 2>&1` | `npm run build >"$P2O/workers/tf-p2-run/hosted-build.log" 2>&1` |
| 5b | beforeAll log | `… >/dev/null 2>&1` | `… >"$P2O/workers/tf-p2-run/actual-beforeAll.log" 2>&1` |
| 6 | build heap | `npm run build` | `NODE_OPTIONS=--max-old-space-size=6144 npm run build` (build step only) |

Unchanged: all spec paths, selectors, assertion and invocation bytes, `P2A=079580ca…`, `P2R=2a9e347f…`, and the `npm run test:e2e:three-products` invocation with the three spec files.

Identity note: `P2A` in the registered row is still `079580ca46af77e0292d49dc34386b25c8391f99`.

## 2. Runner identity for run 31814 (and 15659 for comparison)

Runner files are written by `bin/test-run` (sha256 `2d124030…`). Two points about them:
- `ext` is written at line 26 from the request's declared `$EXT`. It is the **declared external pin**, not a value verified inside the run.
- `snap` records the tree, a cache key and the worktree path. It does not record the commit id or parent of the snapshot.

| Field | P2 31814 | P3 15659 |
|---|---|---|
| suite / target | `ap2-P2-exact8` / `integration:app` | `ap2-P3-gate5-h6-0348` / `integration:app` |
| requested | 2026-10-23T19:22:38Z (`nocache=1`, `files=''`) | 2026-10-23T19:06:26Z (`nocache=1`, `files=''`) |
| status / exit / wall time | `fail` / 1 / 204 s | `fail` / 1 / 224 s |
| snap tree | `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c` | `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c` |
| snap key | `a7b4682ae487b8b310659c85beca65f3` | `2d9ab762df212ae4c1bc7c5f60f7abb3` |
| ext `agent` | `9a095a95178e0bb89ef3b2024d6502d47b35ac25` | `78738040d72ce74c42ddf7731221aecb06f9246d` |
| ext `runtime` | `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` | same |
| ext `composition` | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | same |
| App head | row guard requires HEAD = `2107e1870` or HEAD's parent = `2107e1870`, with tree `a3ff3584`. The guard passed (no NOTREADY). **Head not logged in-run.** | in-run log tuple: `appHead 43b71a9e3e09097367556a1c04558f66aad7a3ff` |
| Agent head | row pin `P2A=079580ca…`; in-run **not logged** | in-run log tuple: `astridHead 079580ca…` (file `/home/user/work/wt/agt-pin-079580ca/astrid/__init__.py`) |
| Runtime head | row pin `2a9e347f…`; in-run not logged | in-run `runtimeHead 2a9e347f…` |
| Vendor/schema | not logged | `vendorLocks.app/astrid source_commit 34eac004…`, `producer_version sha256:d5f98db3…`; `schemaDigest sha256:35c2d9c5…` for app/astrid/runtime |
| Test selection | 8 tests, 3 files: tour (564, 595, 613), elements-assets (376, 467, 522), popup (807, 815) | 1 test: `three-products.spec.ts:1533` |

Git read-only checks (`cat-file`, `rev-parse`, `merge-base --is-ancestor`):
- App: `2107e1870` tree = `a3ff3584`; `43b71a9e` tree = `a3ff3584`, and `2107e1870` **is the parent** of `43b71a9e`. The P3 "App head mismatch" in the extract doc is therefore the same HEAD-or-parent case the P2 row accepts; no mismatch in tree.
- Agent: all three SHAs exist. `079580ca` is an **ancestor** of both `9a095a95` and `78738040`. So the `ext` pins name later Agent commits than the row pin. Which Agent code actually executed is **UNKNOWN** from the retained files.
- Runtime `2a9e347f` and Composition `635f4de0` exist in their repos.

Consequence for app2: the P2 31814 `ext` Agent pin (`9a095a95`) disagrees with the row's `P2A` (`079580ca`) and with the design table. Do not treat the Agent identity of 31814 as pinned until this is resolved.

## 3. Safe observations from retained artifacts

### P2 run 31814 (`log.txt` sha256 `5cf1a7a8…`, `summary` `46214ed7…`)

Retained: no trace, no error-context, no console or pageerror text, no basis-read, identity or owner records.

| Test (spec line) | Result | Observed in retained text |
|---|---|---|
| #1 elements-assets:376 | FAIL | `expect(locator('[data-testid="runtime-connection-status"]')).toHaveAttribute('data-state','connected')` → "element(s) not found", timeout 5000 ms. Failing line in the copy: `openTimeline` line 166. The element was **absent**, not in a wrong state. Error-context: LOST. |
| #2 elements-assets:467 | did not run | — |
| #3 elements-assets:522 | did not run | — |
| #4 popup:807 | FAIL | `preparePopupSeed` → `commitFixtureCommand` expected HTTP 200, got **422**. Body fields seen: `code: validation_error`; `details.code: capture_mismatch`; `details.status: invalid`; `details.conflicts: []`; `details.suggested_command: "timeline edit"`; message "doc.patch must declare every created identity". `base` and `current` identifiers are **equal** in the response (not a stale base). Identifiers and request id not copied here. Error-context: LOST. |
| #5 popup:815 | did not run | — |
| #6 tour:564 | FAIL | same `runtime-connection-status` absent at 5000 ms (`openCommandTimeline` line 144). Error-context: LOST. |
| #7 tour:595, #8 tour:613 | did not run | — |

Not observable in retained text (**UNKNOWN**): mounted project/timeline/selected identity; basis GET route, status, head pair, error codes; authenticated identity presence or scope; owner claim; settled record; console and pageerror codes and stages. Nothing is inferred.

### Preflight chain for the same row (ext all `9a095a95`)

| Run | Result | Retained reason |
|---|---|---|
| 1518-8897 | NOTREADY | `Remotion-toolchain` (hard-coded Node path; before change 4) |
| 1637-32036 | NOTREADY | `hosted-build`, `actual-beforeAll` (row then used `>/dev/null 2>&1`; no output retained) |
| 1837-12838 | NOTREADY | same; log.txt is identical to 1637's (sha `8d30bb2f…`) |
| 14651 | GREEN | "P2 D21 native-seed GREEN". No NOTREADY. The "8 passed" count is **not** in the retained summary (its `counts:` line is empty). |

### P3 run 15659 (`log.txt` sha256 `d3d07149…`, `summary` `6bd84872…`)

| Field | Observed |
|---|---|
| Test | `M2 real gate 5 (M1 real mounted path): …` at `three-products.spec.ts:1533`; "Running 1 test" |
| Phase | failed in `openCommandTimeline` (line 1275, called from line 1537), **before the gesture** |
| Failure | "the mounted editor must claim a new durable command owner before the gesture"; expected `ready: true`, received `ready: false`; "Timeout 90000ms exceeded while waiting on the predicate" |
| Predicate fields in code | new `ownerId` not in previous owners; `pending` false; `intents` empty; `notice` = `timeline-command-recovery` text |
| Owner claim | not satisfied at the 90 s ceiling. Owner id: not printed. |
| Settled record | not reached (failure is before the gesture) |
| `notice` text | **UNKNOWN**: collected but not printed |
| Basis GET (in browser) | **UNKNOWN** |
| Mounted identity, authenticated identity presence/scope | **UNKNOWN** |
| `runtime-connection-status` | not captured |
| Preflight native seed (`preflight-trivialboot.log`, sha `c969e85b…`) | "D21 full native seed: original helper assertions + authoritative history PASS". The basis route (`…/commits?limit=50`) appears only in the row command text; no status is printed. |

### Trace and error-context status

| Artifact | 31814 | 15659 |
|---|---|---|
| `trace.zip` | LOST | LOST |
| `error-context.md` | LOST | LOST |
| snapshot folder | absent | absent |

## 4. Why tests 2, 3, 5, 7, 8 did not run

The retained log records only the count (`5 did not run`, log.txt line 122). It records **no per-test reason**.

Source-derived reason (App `2107e1870`, not in the log):
- `tests/e2e/local/three-products.p2-elements-assets.spec.ts:43`, `three-products.p2-popup.spec.ts:82`, `three-products.p2-tour.spec.ts:37`: each has `test.describe.configure({ mode: 'serial' })`. In Playwright serial mode, after a test in the group fails, the remaining tests of that group are skipped. This matches the pattern: 1 failed → 2, 3 skipped; 4 failed → 5 skipped; 6 failed → 7, 8 skipped.
- `playwright.three-products.config.ts:14`: `workers: 1`. `playwright.direct.config.ts:14–17`: `fullyParallel: false`, `workers: 1`, `retries: 0`, `reporter: list`. There is **no `maxFailures`** and no `-x` in the row's invocation. The popup failure did not stop the tour file, which also shows the stop is per-group, not global.

Status: **source-derived, not recorded in the retained log.**

## 5. Sources for the receipt-bound Node path, build heap and log redirect

All offsets are byte offsets in `private-raw/rows/registered-body.cmd`.

**Receipt-bound Node (change 4)**
- Row: `RENV="$P2O/tests/$RN.env"` (offset 3174) with `RN=agent-remotion-ap2-current-079-2a9-1743`. Node is read at offset 4554: `NODE=$(sed -n "s/^ASTRID_NODE_EXECUTABLE=//p" "$RENV")`. Version checks: `"$NODE" --version = v20.19.4` and npm-cli `--version = 10.8.2` (offset ~4747–4785).
- Receipt file: `tests/agent-remotion-ap2-current-079-2a9-1743.env` (851 bytes, sha `1178ec8f…`, mtime 18:30). Key `ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`.
- Done marker: `queue/done/runtime-agent-remotion-ap2-current-079-2a9-1743` (904 bytes, sha `3e9837b1…`, mtime 18:30). It says the Remotion tree was created from agent `079580ca…` with node v20.19.4 / npm 10.8.2.
- Writer of the receipt: the step that wrote the `.env` is **not in the row or any retained log**. Its provenance is the 18:30 done marker only.
- Verified only on the runner (preflight 14651 GREEN). Node was not executed locally.

**Build-only heap (change 6)**
- Offset 6517: `NODE_OPTIONS=--max-old-space-size=6144 npm run build` (prefix on the build step only). The value `6144` already appears in the row's `ENV_BASE` (offsets ~6699 and ~11850) for every other step.
- **Justification not supported by retained evidence.** The 1637 build output was discarded (`>/dev/null`), and the 1837 build log was overwritten by later builds. The only retained build log, `workers/tf-p2-run/hosted-build.log` (13,552 bytes, sha `327b69cd…`, mtime 19:23), shows `vite v5.4.21 building for production…` and `✓ built in 1m 3s` with no heap or OOM text. The OOM statement in `design/farm-p2-run.md` is therefore **UNKNOWN / LOST**.

**Log redirect (change 5)**
- Offset 6595: `hosted-build.log`. Offset 7315: `actual-beforeAll.log`.
- `workers/tf-p2-run/actual-beforeAll.log` is **0 bytes** (sha `e3b0c442…`, the empty-file hash). The redirect captured nothing for the 31814 beforeAll.

## 6. Other retained files and corrections

- `tests/suites.conf` line 158 holds the body; the preflight is line 159.
- Design-doc table row "final npm run removed": corrected in §1 (the Playwright launch segment is removed).
- Design-doc table row for change 4 omits the npm-cli path change (4b in §1).
- Design-doc "selector count 8 passed inside the chain": not in the retained preflight summary (§3).
- Both runners wrote `test-run: line 55: …/tests/cache/<key>: No such file or directory` to `runner.log` (sha `03b987ed…` for 31814, `0105b5a7…` for 15659). Exit was already written at that line. Effect: the result was not cached. No effect on the recorded exit.
- No `EXIT-MISMATCH` marker exists in either run folder.

## 7. Hashes of raw files read (sha256)

| File | sha256 |
|---|---|
| `managers/farm/INBOX.md` | `1a8a0feca6d8b533188aa3587246082e9931feab6bb7e6cf9dd74b4f412fbfcc` |
| `design/farm-p2-run.md` | `5dd9d78f4ad4c3e73e0f3d0d3e2cdc624ebbb1b11a24b15268d191c568a6780d` |
| `design/farm-p3-15659-trace-extract.md` | `8bd6a34f23bdd6a26862790419b9b77f6e02600f1b2963b2b962c1dbc95c3c98` |
| `design/peer-app2-to-farm-20261023T1756-P3-P2-run-handoff.md` | `b0e827a43a65668bbdf4e94ae96c22aca37f082c72398cc4dfdd63db8cdd94b2` (line 77 = `d4f6fe75…`) |
| `bin/test-run` | `2d1240303c0c82bf908377eeff3323a899d8929454ac2c316b05bf076fc35d35` |
| `tests/suites.conf` | `64afaf615665def79f3660d771f17e226c83fa58223417f5dd11d8cc6227d61d` |
| `workers/tf-p2-run/p2-row-before.cmd` | `d4f6fe75a0a9110cc82f537c56060ad6b7169ec2b92cc12e01b1c81d4950a009` |
| `workers/tf-p2-run/p2-row-after.cmd` | `685c0fead4e5e7bde3c2c95cb0d3ad41647e674b068740d4d91d3889249d585b` |
| `workers/tf-p2-run/p2-preflight-after.cmd` | `cd2d5b6446ac0e84d24b7a1286d709e04045b6b2003bb445c1714e3e3b4a0ce2` |
| `workers/tf-p2-run/p2-row-after-node.cmd` | `14275712108064c789f86f88d7ee89899250fb78c7383cca97b47b16b11a916a` |
| registered body (from `suites.conf` line 158) | `7ee460f69cbeb6224adc42f08af65fa9be5e7182776adfde91f0edfc78933daa` |
| registered preflight (from line 159) | `f3d02ff945ee5d83f85696f9258655ca166323b236be1851e392b8381d1e1e41` |
| `workers/tf-p2-run/hosted-build.log` | `327b69cd97b3c7c9997bac0dbf0f9503ac9f7d9675c8627c2e446e1d7fff5725` |
| `workers/tf-p2-run/log.txt` (= `report.md`) | `892f966e8761e7407ee5c5fad23de9311af3e850ce6b4184e937055eba187400` |
| `workers/tf-p2-run/actual-beforeAll.log` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `workers/tf-p2-run/meta` | `6e967b0f1f192b61b5e4319bf048b2f3950002a6ef94c539c6a89bca55d997d4` |
| `workers/tf-p2-run/graph/build.mjs` | `4781d7accd80475939278bfb5fc7253994521f6e3c9372e77890cfd005d310c1` |
| `tests/agent-remotion-ap2-current-079-2a9-1743.env` | `1178ec8f5467c5b7c849ff854ecf31b76b63f7957d8b293596e1981d6955cb1b` |
| `queue/done/runtime-agent-remotion-ap2-current-079-2a9-1743` | `3e9837b11fac7ac8e5d7796cb2dea80181b1e806122e65eb3156428ee8f0bac2` |
| 31814 `exit` | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` |
| 31814 `ext` | `7b79b823bb82a41193d5c00d279eb0e46a8ac3bfa312f500201d0132feb8908d` |
| 31814 `log.txt` | `5cf1a7a8b14bd7afe8c796164ce63605bfbe7500670b943e323fdfd84bed3eb3` |
| 31814 `request` | `f12477ebaaf613b22cc42de31e824192ac8d3ccda36d78c8141088f7ea4f24f1` |
| 31814 `runner.log` | `03b987eddfd67b291eda3b43f3328e2affde478dc73c7ee650c0e1361474717a` |
| 31814 `snap` | `3618bc5936e2c557cfd2da4c8bbf6877d696359c070930a13e70495c1c395503` |
| 31814 `status` | `2056a28ea38a000f3a3328cb7fabe330638d3258affe1a869e3f92986222d997` |
| 31814 `summary` | `46214ed75e5dd38a4baf8ba25bfd29604b934c7c497914b97a334c47d3d86ca7` |
| 15659 `exit` | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` |
| 15659 `ext` | `5cba91fd6f9a3b1bbe329b1c11a12b2010d038dbb3b26143ebd08a865852c0ca` |
| 15659 `log.txt` | `d3d07149d0fc6951cb2befe7d60023487c47f9e341896fbdd45ea21f64248a43` |
| 15659 `request` | `1ee241dd62def52bd58a6bbda345618b820bfc905163214540773334ed4530d7` |
| 15659 `runner.log` | `0105b5a7404b0c7a380331845eea383f2bd46365a89db0293e41260bac4715fd` |
| 15659 `snap` | `82453329aa4006dc107a5932a8e7274ef0b8b6526509256de1329ee28d0be91c` |
| 15659 `status` | `2056a28ea38a000f3a3328cb7fabe330638d3258affe1a869e3f92986222d997` |
| 15659 `summary` | `6bd84872519373c253bcfd6b2db7e3cdfdc58db53ea8049a5bf9adf2844777e3` |
| preflight 1518 `log.txt` / `summary` | `2532b247b79dca8fde5e65b05033a92e6166f83de4de00315b9aae176af3e434` / `5bb55711d296cf01142ad0f354efe5793ecd38edb3a477019ed08c7a37b7ef61` |
| preflight 1637 `log.txt` / `summary` | `8d30bb2f7f905db63ac363f6e695e4be438a0119393cca8b792329ccd9510aa8` / `8a7515118529c4ac45f7c82cdfb9a889361c407edadbeee0c7ede992d4d95990` |
| preflight 1837 `log.txt` / `summary` | `8d30bb2f7f905db63ac363f6e695e4be438a0119393cca8b792329ccd9510aa8` / `9a32fb5d6d4d175d3d6df714a13f48a09239a062ee123f7da594a245f6bf91fc` |
| preflight 14651 `log.txt` / `summary` / `ext` / `status` / `exit` | `6862c59ca8638158e3b621bd761a313a3f7d20dd38d5d40f93d3aae4f58c11df` / `22c104940d636646f7e84296af262af36bdff359c47a6b4beada918e68748a15` / `7b79b823…` / `9f56e761…` / `9a271f2a…` |
| P3 `preflight-trivialboot.log` (copy) | `c969e85b96362e40624007944deb1916810a59d2a8b11cb1b81c03a97704e464` |

Private raw copies (not published): `workers/tf-evidence-packet/private-raw/31814/`, `private-raw/15659/` (all small files of each run), `private-raw/rows/` (the two row bodies, `suites.conf`, worker row copies, `hosted-build.log`).

## 8. Process notes (honest disclosure)

- Several read-only shell commands were rejected by the command reviewer (compound command, variable expansion, a `cd` before `git`). I re-expressed them as simpler read-only commands: `git -C <repo>` instead of `cd && git`, literal paths instead of variables, and the Write tool instead of a heredoc. The reads and results are the same. Nothing was written outside my worker folder and the scratch directory, and nothing was run beyond reads, `cat-file`, `rev-parse` and `merge-base`.
- The worker `tmpdir` pointer file names `/tmp/w-fed06d05e8`; scratch scripts live in my scratchpad there.

## 9. Open items for app2 / orchestrator

1. **Agent identity conflict** (§2): decide which Agent commit the P2 31814 and P3 15659 runs executed, given the row pin `079580ca` versus the `ext` pins `9a095a95` / `78738040`. Re-running is not authorized by this packet.
2. **Retract or evidence the OOM statement** for change 6 (§5); the retained build log shows a successful build.
3. **Evidence for the 31814 failures**: the trace and error-context are LOST. Any further observation needs a new authorized run; none is implied here.
4. **Correct the worker design docs**: the preflight difference, the npm-cli change, and the "8 passed" claim (§1, §3, §6).
