# Producer complete execution prerequisite diagnosis — 1132

## Verdict and scope

**Diagnosis complete; five-control closure BLOCKED by one proven control-assertion contradiction. No preflight, control, startup probe, browser, build, socket, service request, full suite, install, or actual test ran.** MAIN packets remain **NOT READY**. This packet is tied to the current local Node 22 installation and original graph paths; it makes no MAIN Node 20 or portability claim.

The source is unchanged: `5863411a8c2400db719b5385002b05af0a2b3891`, tree `31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89`. The strict chain is `5863411a → b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7 → 17d2518c341c47a2d8634047b400399886da3a2a`; baseline tree remains `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`. No product/spec/helper/operation/pin/guard semantics changed.

Permitted repairs completed:

1. Restored only the absent ignored keeper `node_modules` symlink to **exactly `/home/user/work/app/node_modules`**, after source, ancestry, clean-status, four source-file hashes, ignored-path status, shared TSX entry/loader/manifest hashes, executable/realpath, and locked Composition checks. No shared dependency or file beneath that link was written. `keeper-repair.json` records the checks.
2. Made one owned copy of the eight positive artifacts, rebinding all internal 1113 worker paths to this worker and recomputing hashes from leaves upward. Each artifact reverses exactly to its 1122/1113 original. This fixes the copied harness's otherwise escaping 1113 dispatch and retention paths. The harness and launch stub themselves are byte-identical to 1122; the stub also matches 0935/0945. The original negative graph remains unchanged.

Read the PLAN and 1113/1122 reports, 0935 refusal correction, 0945 aggregate hash repair/readback, and 0954 strict ancestry proof. The earlier claim of a complete runnable five-control closure is contradicted by the still-retained temp assertion described below. I did not reinterpret the ancestry guard or repair control logic under a data/environment-only brief.

## Absolute paths and anchor convention

`P` = `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132`

`K` = `/home/user/work/wt/app-pin-5863411a`

`O` = `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`

`G` = `O/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph`

`B` = `O/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts` (live negative-control dependency).

All `P/...:line` anchors below identify the exact exported files. `K/...:line` identifies unchanged producer source. Copies of the eight negative artifacts are exported in `P/before-artifacts`; the unchanged harness still reads the original **B**, rather than those convenience copies. Full original paths, realpaths, hashes, and line-numbered edges are recorded in the JSON inventories; no prefix is a proposed portability alias.

## Executed graph, by mode

| Mode | Actual branch and statements | Files/tools required before reaching the next stage |
|---|---|---|
| preflight | custody:38–95 → physical:12–35 → owned runner:63–285 → public13:4–295 → custody format probe:92 | All source/keeper/link/tool/hash gates first. Owned runner performs 13 aggregate checks, creates forwarding/temp environment, then calls public13 with `PUBLIC13_PREFLIGHT_ONLY=1`. Public13 performs 11 checks, clones fixed Agent/Runtime into one private run root, constructs/attaches private graph, resolves Vite and Composition, exits before flock/build. After cleanup, custody loads the format probe through the original shared TSX. |
| startup | custody:94 → startup-only gate:22–90 → startup probe:1–88 | Performs source preflight first; creates physical `/tmp/tla-startup-*`, source clones, cache paths, fixed Python/browser env; TSX imports harness; negative planted symlink test and positive Runtime/door health test start daemons and sockets. **Not authorized or run.** |
| list | custody:95 → physical → owned runner mode=list → public13 → flock `sh -c` | Same source/private graph setup, hosted build, forwarding branch selects exactly `playwright test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts --list`; validates `Total: 1 test in 1 file` and rejects zero tests. A list is not a source-only/no-build mode. **Not run.** |
| final run | original registered outer guards → custody run → physical → owned runner → public13 → npm forwarder → Playwright → config/global setup/spec/fixtures/browser/Runtime | Exact registration was rebound only by paths, gate digest, source HEAD/tree; reverse proof saved. Positive child has no `--list`. Exactly one passed or failed test must be reported consistently with child status. Nonzero exits retain evidence then clean private environment. **Not authorized or run.** |

The eight artifacts are six shell scripts and two TypeScript modules, not eight unconditional shell processes. No shell artifact sources another file with `.`/`source`; dispatch uses `sh` or the executable retention helper. The owned runner re-enters itself as a private `npm` symlink. Preflight reaches the module-format probe, **not** the startup probe.

### Five copied control modes

`P/outer-controls-run.py:10–35` derives ROOT/ORCH from its own real path, reads the original suites.conf registration, writes three registration snapshots when actually invoked, and depends on `launch-tool-stub.py`. `:37–111` creates a new per-case temporary fixture, copies five real keeper files, binds a fake KEEP and Agent/Runtime directories, links the immutable graph, translates all paths and dependent hashes, reverse-proves the translation, installs seven private stub links, then dispatches the registered shell at `:112`. No such fixture was created here.

| Case | Source and stub mode | Required result/assertions | Static diagnosis |
|---|---|---|---|
| before | B, failure | outer status 1; **one custody shell, zero child, zero build stub**; no packet | OLD custody refuses before source dispatch because current source spec/helper hashes differ. Correct shell/child assertions are already at `:121–130`. But `:135–138` reads nonexistent `temps.jsonl` and expects one leaked later-stage temp. **Deterministic harness failure.** |
| after | P/artifacts, failure | 4 shell order; 1 child; 1 build stub; complete retained failure packet | All static file/hash/path dependencies available after rebind. Stub plants DOM context/trace/child log, outer verifies exact bytes, status, checksums. Not run. |
| absent-output | P/artifacts, absent | same 4/1/1; retention must fail, no complete SHA256SUMS packet | Child fails without planted trace/context. Helper's required-file assertions fail; public cleanup must propagate failure and restore link. Not run. |
| copy-failure | P/artifacts, copy-failure | same 4/1/1; planted cp error 23; no complete packet | Only retention `cp -a` is faulted; all private cleanup still expected. Not run. |
| success | P/artifacts, success | status 0; same 4/1/1; no retained failure packet; no private run root/dist/temp leaks | Stub reports one passed child; production npm forwarding/cleanup bodies remain real. Not run. |

The expected dispatch order is custody → physical → owned runner → public13. The inner `sh -c` is audited but excluded from the four-shell count (`:119`). `launch-tool-stub.py` uses `/usr/bin/python3`; stubs git clone/reset/ref/status, node graph/resolver/version/cohort boundaries, build npm, flock, and Playwright, while real shell bodies, path/hash tests, filesystem construction, copying, retention, and cleanup execute. `mktemp` invokes `/usr/bin/mktemp` and logs its result; `cp` normally execs `/usr/bin/cp`. Fixture executable Playwright is the same stub dispatched by its basename. `/usr/bin/true`, `/bin/sh`, `/bin/bash`, `/usr/bin/sha256sum`, and ordinary coreutils remain external prerequisites. `CONTROL_CONFIG` is written at `outer:110` and exported at `:111` **before** any stub reads/audits it (`stub:5–12`). All seven stub symlinks must resolve to the exact existing script, not a missing copied filename.

## Complete failure set and repair boundary

| Finding | Exact evidence | Disposition |
|---|---|---|
| Missing launch stub in 1113 | 1113 report; copied stub is independently SHA-verified below | Fixed by exact copy in 1122 and this packet; no new stub logic. |
| Missing keeper node_modules | custody:66; physical:32; startup-only:32; public13:83–84 | Fixed authorized ignored link only, after exact checks; clean status remains empty. |
| Copied artifacts still pointed into 1113 | 1122 custody:5–9, physical:9, startup-only:8–11, owned:76/230, public13:31; harness:64/86–91 maps only selected source root | Fixed together in P with computed transitive hashes and eight reverse proofs. All positive internal edges now stay in P and translate into the control fixture. Prior packets untouched. |
| `before` temp expectation contradicts early refusal | OLD custody:85–86 precede `:95`; runner mktemp only `:221`; outer:135 reads temp log unconditionally and :138 demands one later-stage leak | **OPEN, cannot repair by restoring env/files/paths/hashes.** Requires authorized harness logic correction, or a changed decision about the early-refusal contract. Faking a temp event would corrupt evidence. |
| Build preflight env absent/ineffective | `PUBLIC13_BUILD_PREFLIGHT_PASS` unset here and omitted from original registration; public13:298–309 inner sh has no `set -e` | Not a deterministic launch blocker: failed `test` at :307 is followed by npm at :308, whose status is returned. Record as an unenforced precondition; do not set it to 1 as invented build evidence or strengthen the guard in this task. |

**Concrete open setup/closure gap count: 1** (the `before` temp assertion). The four positive modes have no remaining identified static setup gap. No dynamic execution success is claimed. MAIN tool/runtime/path qualifications and all actual test results remain unverified; those are separately withheld claims, not silently fixed prerequisites.

Independent review, requested only after identifying the necessary logic discrepancy, confirmed the contradiction and the permissible data-only path/hash repair. Saved at `P/independent-custody-review.md`. Minimal future harness correction would read an absent temp log as no events **only for the before path** and assert zero created/leaked temps for that early refusal, keeping all other cleanup/dispatch/evidence expectations. This is a proposal for orchestration, not an applied change or a test expectation weakened here. The original `before` test has never reached a passing assertion result in 1113/1122.

## Source, keeper, object, and hash closure

- Keeper HEAD/tree, both ancestry equalities, clean status, KEEP marker, source wrapper committed and working bytes, spec/helper/config bytes all match. Baseline-to-source diff is exactly wrapper/spec/helper; config unchanged. BODY `36dd91257fd13dcad0d58b48c790caa5063b4c8c`, tree `d908845dbc8e5ebf96698d08621557e904f20c52`, is present. Approved-delta check still binds actual HEAD ancestry and permits only the wrapper after the source.
- Agent object `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`, and Runtime object `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`, exist at the exact original repository paths with empty porcelain output. Their local repository HEADs are unborn; this does **not** fail these gates, which validate explicit commit objects rather than requiring current source HEAD. No checkout/reset/clone was done by this worker.
- Original 0945 schema is recomputed rather than copying its prior `match` booleans: **51 hash/identity guards, 20 path bindings, one producer-version value guard**. Precisely, those 51 contain **30 SHA-256 values and 21 40-hex commit/tree identities**; prior prose calling every one 64-hex was inaccurate. Composition version tests remain 0.0.13. Producer version remains `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, contract artifact count 75.
- All required existing path bindings exist and realpaths match their respective policy. `EVIDENCE_ROOT` is intentionally future-created at owned runner:230–231, not a missing preflight input. Its physical parent is present. The graph/archive/retention/KEEP/TSX paths are inventoried individually. `guard-readback.json` records every guard and its newly computed target/result; none was removed.
- App files SHA-256: wrapper `329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`; spec `6666c0365d13f302725788e6fbfcce9e0fb283e4b30c40661886522a67f270e6`; helper `df1faac404b69efa8a5fb06297814e6ca3b5d52b4a5856633706c7ac2e3ae949`; config `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`.

## Graph, archives, actual package destinations, and toolchain

`G/node_modules` is a physical directory. Its 423 top-level entries were enumerated, scoped entries expanded, 531 package manifests read with realpaths and SHA-256, and every declared executable target checked for existence/executability without running it. `timeline-theme-2rp` is an existing non-package directory with no manifest; the construction loop's explicit ENOENT continuation handles it. It is not evidence of a failed package install. All graph links are retained; no link inside any graph/shared install was added or replaced.

The graph archive is 300830720 bytes, SHA-256 `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`. Its embedded `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz` hashes to `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` and contains 77 files. **All 77** installed original-graph Composition files match the corresponding archive bytes, not merely the two guarded files. Manifest SHA is `7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61`; evaluation SHA is `e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155`.

The original shared App install currently contains **Composition 0.0.8**, not 0.0.13. That original link is required for custody and TSX; it must not be mistaken for the effective rendering dependency. At public13:169–212, exactly one Composition package is copied/dereferenced into private `RUN_ROOT/node-modules`; other packages are symlinks to the original graph, with a private `.bin`. At :224–228 only the keeper link and new private Agent/remotion links are attached to that private graph. At :269–290 the unchanged code asserts App and SDK createRequire paths, both Vite resolution paths, version, hashes, and `clipOpacity`. The exported inventories record the intended private physical destination and current original package destinations. Those runtime resolver assertions were **not executed** here. No 0.0.10 source/declaration was promoted into a loaded package, and no install was used to reconcile declarations with the authorized graph.

Local binaries: `/opt/node22/bin/node` **v22.22.0**; npm **10.9.4**; TSX **4.21.0**; Vite **5.4.21**; Playwright/test/core **1.60.0**; React **18.3.1**; Remotion **4.0.509**. TSX cli/bin hash `8729ecfb90d9d568939e4190e6f1d3317c946583b7d37a776e0c23a21c021cf8`, loader `0b1c5b86192772fe9257710e739959cee5947c11ae1f93b61abfaa9b80c6def1`, manifest `6e764b21991c21595441f82387c1451ccd10a3e7a3f0973cc5e3649a12dea7d2`. Linux native SWC and both top-level/nested Vite esbuild executable packages exist. Full binary paths/hashes and package manifests are in environment/package/import inventories; binaries were not built or installed.

Host Python `/usr/bin/python3` is **3.13.16** (also stub shebang). Producer Python is the exact virtualenv entrypoint `/home/user/work/venv-app2-native/bin/python`, **3.12.3**. Preserve that venv entrypoint even though its realpath resolves to `/usr/bin/python3.12`; invoking the realpath would discard its dependencies. The venv has jsonschema 4.26.0, referencing 0.37.0, attrs 26.1.0, jsonschema-specifications 2025.9.1, rpds-py 2026.9.1, PyYAML 6.0.3, typing_extensions 4.16.0 and six tool distributions recorded in metadata inventory. Runtime's declared runtime requirements jsonschema/referencing are present. Agent's entire optional/tool SDK dependency list is **not installed** here and is not a required import of this neutral producer harness; optional timeline check's numpy/PIL path is explicitly outside this selected flow. No claim of a generally provisioned Agent environment is made.

Other checked tools: Git 2.43.0, GNU tar 1.35, flock/util-linux 2.39.3, OpenSSL 3.0.13, ffmpeg 6.1.1; sh/bash/coreutils paths and checksums recorded. Chromium path `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` exists and was hashed, **never invoked**, so browser compatibility/version execution is not qualified.

## Recursive imports, profiles, manifests, and credentials

`import-inventory.json` records a static TypeScript-AST superset of **4390 files, 20020 import edges**, with file hashes, importer line anchors, type-only classification, resolved physical package locations, and all 50 nonliteral import/glob sites. It begins at both probes, harness, config, producer spec, global setup, hosted build, real HTML entry `src/app/main.tsx`, TSX cli/loader, Vite, Playwright, and Composition evaluation. It follows source aliases into frozen Agent **blobs read as data without checkout**, the App's existing bundled public browser source, relative imports, package entrypoints, and ESM export branches. All three source Git trees are exported as path→blob manifests. There are no missing seed files.

The preflight module-format path is small: `.mts` → `K/tests/e2e/local/support/harness.ts` → runtime `config/vite/projectElementSelection.ts` plus Node builtins; type-only `@banodoco/timeline-schema` is erased. No DirectHarness constructor/start method runs in the format probe. Source-only probe success itself remains unverified.

The final spec graph is spec → support/app → support/harness plus producer helper → scene-phase/transcript extension modules → sourceMap and their recursive modules. Producer config imports direct config, which names `tests/e2e/local/global-setup.ts`; global setup imports hosted-build-origin and node-package-manager, then only builds if dist is not current and hosted. Hosted build invokes Vite with `config/vite/vite.config.ts`; its full config import graph (policy, proxies/security, Runtime client, admissions/selection, generation composition, source/catalog validation, bundle budgets, fonts, relay, share metadata, installer assets) is included. Frozen Agent whole-Tool catalog and both declared bound files pass exact hash/size checks in `archive-and-catalog.json`.

Finite build globs were expanded: **61** frozen Agent element TS/TSX modules, **10** vendored font assets, **1** blog Markdown input. Probe dynamic harness URLs are explicitly bound to the harness seed. `virtual:astrid-element-admissions` is generated by `config/vite/astridElementAdmissions.ts:142–175`; absent project-scoped options yields an empty admission selection. The optional URL import at `runtime/admitted-elements.ts:59` requires an admitted selection and is not an ambient package fallback. No project admission profile or external credential was synthesized.

The 34 unresolved static package edges are retained and classified in the inventory: conditional non-Linux SWC/native alternatives and wasm fallback; optional websocket accelerators bufferutil/utf-8-validate; macOS fsevents; optional PnP/source-map tooling; Electron/BiDi branches; one erased dnd-kit type import. They are not 34 missing required Linux runtime packages. This is **static dependency coverage**, not an assertion that every conditional branch executes. Arbitrary dynamic package loaders and browser-generated module execution cannot be proven by pretending a syntax check is a run. All such sites remain visible; no browser/build/import execution was performed to resolve them.

`python-import-inventory.json` records **105** Python modules and **1370** import sites across the frozen Runtime package and optional Agent timeline provider, with Git blob and SHA-256 identities. Selected final fixture starts `runtime_protocol.cli create/start` with explicit Runtime+Agent PYTHONPATH, **neutral profile** (no `--authoring-profile astrid`, no worker profile). Its start/seed/credential statements are `harness.ts:443–503, 556–571, 751–777`; no Agent CLI/dev-selected-element methods are called by this producer fixture. Runtime's referenced JSON/schema resources are covered by the frozen tree manifest.

At actual fixture startup, a new physical harness temp contains realm/support, TLS certificate/key, audit log, discovery, owner/worker token files, and generated product credential JSON. OpenSSL generates the local certificate (`harness:176`), Runtime creates/protects its own roots, owner token is read solely from new support/credentials, then Runtime mints product credentials and writes JSON mode 0600 (`:556–571`). `ASTRID_RUNTIME_CREDENTIAL` means a **file path**, never a token value. No ambient API key/cloud account is needed for this selected journey. Credentials, caches, source checkout contents, and browser profiles are excluded from retained evidence. No credential contents or environment secrets were inspected or exported.

## Runtime variables before writes and cleanup

`shell-execution-ledger.json` preserves **898** source statements with absolute file and line anchors across positive/negative chains, covering every variable-bearing and filesystem/dispatch statement. The following establishes the ordering and physical destinations rather than treating filenames mentioned in comments as execution.

| Established before write/dispatch | Source anchors and lifetime |
|---|---|
| `MODE`, keeper/service HEAD/tree, artifact/tool hashes, KEEP, source refs | custody:38–87; physical:12–32. All checked before creating private environment. Keeper clean check includes untracked files; ignored node_modules checked separately. |
| `APP_ROOT`, `RUN_MODE`, source/baseline/BODY, graph/cohort/disk/isolation/argv | owned:63–219. No list/temp root before these checks. NPM_FORWARDER must be unset/0 at entry or mode=preflight is rejected before normal setup. |
| `LIST_ROOT`, `REAL_NPM`, `SCRIPT_PATH`, `LIST_LOG` | owned:221–228. mktemp under physical caller TMPDIR/default /tmp, mkdir bin, capture original npm **before** replacing PATH, create private npm symlink, initialize empty child log before later failure retention. |
| `EVIDENCE_ROOT`, `DURABLE_ROOT` | owned:229–245. Only run mode mkdirs physical P/evidence; unique failure timestamp+PID child must not exist. preflight/list unset durable root. |
| Forwarder mode/root/log/real npm, private PATH, `PUBLIC13_PREFLIGHT_ONLY` | owned:237–253. Exported before public13 or any npm-forwarder invocation; preflight sets 1, other modes unset. |
| `SHORT_ENV_ROOT`, `SHORT_APP_ROOT`, physical realm TMP root, XDG config/cache | owned:259–279. Unique physical `/tmp/tla-*`; `a` aliases real keeper; physical parent, not that alias, is exported for Runtime realm paths. Cleanup replaces initial trap and deletes **both** list and short roots. |
| `PREFLIGHT_ONLY`, `RUN_ROOT`, original node_modules target, ATTACHED_PATHS | public13:12–16,115–155. Require no preexisting `.public13-effective-ordinary`; create private subdirectories, capture original link, install EXIT/HUP/INT/TERM cleanup before source clones/graph attachment. |
| Source clones, private node-modules and `.bin` | public13:157–228. Only the new run-root clones are reset; one Composition physical copy, other package links; bins validated before swapping keeper link. Agent/remotion attachments must be absent. No mutation resolves into shared node_modules. |
| Source/Python heads, browser/output/cache env, TMPDIR, NODE_OPTIONS | public13:230–246. Explicit frozen clone paths; exact venv paths; `/opt/pw-browsers`; private pw/npm/browser/vite/tmp paths; Python no-bytecode/no-user-site; Node 4096 MiB; unset public source/dist overrides. |
| `SOURCE_NODE_MODULES`, `PRIVATE_NODE_MODULES`, expected Composition hashes; APP_ROOT/AGENT_ROOT | public13:169,248–250. Provided directly on each inline Node invocation before it reads env. No ambient NODE_PATH may select Composition instead of guarded private resolution. |
| Retention arguments, physical paths, child status/log, absent destination | helper:4–29. Only failures; all absolute, real run root, ordinary mode, nonzero status; create unique durable child, refuse symlinked output before copying. Require DOM context/trace then identity and sorted SHA256SUMS (`:33–62`). |

Vite 5 does **not** read `VITE_CACHE_DIR` itself as a cacheDir override; default resolves `node_modules/.vite` (`vite/dist/node/chunks/dep-BK3b2jBa.js:66507–66509`). Here that directory resolves into the **private** run graph while attached, not a shared install. Vite config ESM bundling creates a transient adjacent `.timestamp-*.mjs` and removes it in finally (`:66968–66981`); this lies beside keeper config and must not survive. TSX uses `os.tmpdir()/tsx-<uid>` (`tsx/dist/temporary-directory-CwHp0_NW.mjs:1`), so the next worker must supply a physical **owned** TMPDIR before the outer format probe. No TSX/Vite cache was created by this diagnosis. Browser profiles derive from private short TMPDIR; Runtime realm TMPDIR is explicitly rebound to the physical short parent by the npm forwarder.

On nonzero public13 exit, retention runs **before** link/temp cleanup; retention failure also forces final failure. Cleanup unlinks only ATTACHED_PATHS, restores the original keeper link, removes only untracked dist, then deletes private run root. Owned wrapper subsequently deletes list/short roots. Successful actual runs create no failure packet. The control harness independently verifies restored exact link, absent dist/run root, no temp leaks (except its contradictory OLD before assertion), and durable packet checksums. Failures between initial public13 mkdir and trap installation remain an existing narrow cleanup window; no behavior was redesigned here.

Disk snapshot was **13531748 KiB free**, exceeding unchanged **10485760 KiB** floor. Disk and lock availability are time-varying and must be reevaluated by their existing gates; no new floor was invented. Lock path `/home/user/work/.app-m1-browser.lock` exists and is physical; diagnosis did **not** acquire it. Final original command checks it nonblocking; runner uses `flock -w 600`. Controls stub both lock operations. Actual direct door defaults to **17340**; origin/runtime select free ephemeral ports; no port/socket availability was tested. PLAYWRIGHT_PORT/BASE_URL do not substitute for the actual direct-door env. Node20/MAIN compatibility and available ports/locks are explicitly unqualified.

## Exact next closure and withheld execution

Files `P/next-preflight.sh.txt`, `P/next-five-controls-BLOCKED.sh.txt`, and `P/finalrun-NOT-AUTHORIZED.sh.txt` contain syntax-checked literal commands. They were **not executed**. Paths are bound to P and K; extraction into an arbitrary directory is not supported. The central suites.conf registration was read/snapshotted, never modified.

For a separately authorized next worker using this same local Node22/original graph, with a physical owned TMPDIR and no stale run/control directory, the complete preflight entry is:

```sh
cd /home/user/work/wt/app-pin-5863411a
sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132/artifacts/producer-startup-custody-gate-0717-owned.sh preflight
```

Its complete static closure is the exported positive eight files, original keeper+KEEP, shared exact TSX tool dependency, frozen Agent/Runtime object stores, original G graph/archive, venv, Vite config/source/catalog graph, and available private temp/disk paths, all inventoried above. It must run on the original physical keeper or a captured clean checkout with the **same source tree**, not this task's unrelated integration worktree HEAD.

The retained five-control entry is:

```sh
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132/outer-controls-run.py
```

It has both eight-file graphs, five keeper source inputs, exact stub/interpreters/tools, original suites.conf registration line, source object stores, and original dependency graph available. Its **runnable dispatch closure is complete**, but its **pass closure is not**: it deterministically fails at the known before-temp assertion. Do not spend a third executor attempt on it. Orchestration must authorize/correct that specific assertion first, preserving the settled one-shell early refusal and all four positive-case evidence/cleanup assertions. Then only the separately authorized next preflight/control attempt should be run once; do not run the finalrun data file, list, startup, build, or actual lane from this diagnosis.

## Validation commands and results

From this worker's process, exactly these saved command entrypoints were used for mutation/audit/syntax work (P is the absolute path above):

```text
python3 P/prepare-closure.py
  PASS source/ancestry/clean/dependency checks; original ignored link restored;
  eight data-only reverse proofs; exact copied harness/stub. Run once; restoration
  intentionally refuses to overwrite an existing link, so do not rerun it blindly.
python3 P/audit-inputs.py
  PASS 51 guard rows, 20 paths, cohort/version 75, archive count 77,
  531 package manifests and declared binary targets; no producer code executed.
node P/import-inventory.cjs
  PASS final static inventory: 4390 files / 20020 edges / 50 nonliteral sites /
  34 conditional unresolved package edges / 0 missing seed files.
python3 P/validate-syntax.py
  PASS 6 Python files compiled in memory, 12 shell artifacts (positive+before),
  4 .mts files checked, 3 literal command files parsed, inventory JS checked.
```

Read-only Git show/status/diff/check-ignore/ls-tree/cat-file, stdlib tar/hash/catalog comparison, AST Python parse and venv metadata inspection also passed; snapshots are exported. The first inventory draft incorrectly treated the intentionally manifest-less theme directory as required; inspection of public13's ENOENT continuation corrected **only the diagnostic script**. An early Node-based parser tried spawning git and received sandbox `EPERM`; Git bytes were instead supplied by Python's read-only cat-file reader, without executing source or relaxing permissions. Parser seed/path/ESM/glob handling was corrected before the final inventory above. These are diagnostics-tool iterations, not preflight/control attempts. Temporary 9 MB parser source carrier was removed. Product suites were **not run** because this brief explicitly prohibits them; syntax/static checks are not a substitute for those future results.

## Artifact manifest and final state

The exact per-file export list, modes, sizes and SHA-256 values are in the adjacent `ap2-m2-producer-complete-execution-prereqs-diagnosis-1132-MANIFEST.json`; every exported file is also in `SHA256SUMS` inside the small `ap2-m2-producer-complete-execution-prereqs-diagnosis-1132-closure.tar.gz`. The archive excludes logs, temporary parser content, node_modules, venvs, build output, browser output, and credentials. Its external dependency bindings deliberately remain at their original paths.

Positive artifact manifest:

```text
producer-physical-keeper-gate-0717-owned.sh  d9ecc3ade14746c559c46c68046eec3f71ecac5c37f9218cb575a9e2057a6238
producer-public13-runner-0717-owned.sh  b21d9ccd1dfc31b81d38e2e19c78ca4d53ca3a3a7a5c74f82c7bffb533fe9d13
producer-retain-failure-artifacts-0753.sh  dab4e885cedbde6273139d3b4350cacdd33020e63773f9c71e0289ab78ddea75
producer-runner-0717-owned.sh  84031e301827518c2b981c585e812c5a5ad3d00727105c1b8515a6e1209a54fa
producer-startup-custody-gate-0717-owned.sh  02d831e05094586d3771424ac43cacb602799c691ec40423fb370891ba1cb16e
producer-startup-module-format-probe-0717-owned.mts  d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3
producer-startup-only-gate-0717-owned.sh  4ce9e7f4fc0eb6c6a7b32b784cd3ea64f598b4169fa49ba2a99126237dc4a5df
producer-startup-only-probe-0717-owned.mts  a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f
```

Exact launch stub SHA-256: `4299795135db4be3b83b41d9034cb1519b529925865222f9af866029df9264b7` (0755). Original control harness SHA-256: `ff1ae8404f39d765b01429ce706fa0affb6a163b632c20506a9705f103ec7234` (unchanged). Before graph, original registration, reverse proofs, independent static review, source trees, package/import/env/variable ledgers, catalog/archive comparison, syntax validator and next-command data are all included and checksummed.

App task worktree and keeper remain clean; only the explicitly authorized ignored keeper link changed outside P/design. Shared graph/install/venv, all prior evidence (including original 19080/failure packets), refs, integration worktrees and suites registration were not modified. No commit/merge/rebase/checkout/push occurred. Commit message is recorded in the assigned worker path. BLOCKED records the one unrepairable-under-this-brief pass-closure gap; no DONE success marker is fabricated.
