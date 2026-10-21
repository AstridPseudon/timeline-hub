# App automatic current-main command custody review

Verdict: **HOLD — necessary literal corrections remain.** I did not edit or
execute the packet's browser actual. The packet's source/spec/config tuple is
otherwise the correct current source: App `1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf`
(`8e242d1497841f391b6152ecd8d204143fa03b52`), Agent
`6efc81500a0e0688c2bb41e736503f0fc3e04abb`, Runtime
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, and runner SHA
`7ea0243ab6760d5fb06d17cf7e673f338549206090799c4946d532c3926d5d1f`.
The packet's App ancestry claims are true: both `02ac224cd3c0d376f08b6129f58ded624f3e400d`
and `da5d6d564af58ad06f126188c25e9a47f4e45be4` are ancestors of App1490.

## Necessary corrections

1. Add a real `--list` precheck before the one actual. Run the exact
   `npm exec -- playwright test --config playwright.auto-real-proxy.config.ts
   tests/e2e/local/auto-real-proxy.spec.ts --list` from `APP`, with the same
   child environment as the actual, and fail unless exit status is 0, the
   named file/title occurs exactly once, and the output says `Total: 1 test in
   1 file`. The config source is `playwright.auto-real-proxy.config.ts:5-14`
   (`testDir`, `testMatch`, one worker, zero retries, retained trace), and the
   only test is `tests/e2e/local/auto-real-proxy.spec.ts:311`.
   The packet currently asserts one test only in prose.

2. Correct the preflight environment-unset check. Packet line 179,
   `! env | grep ...`, runs in the outer shell after the `env -i` child has
   exited; it does not inspect the preflight or future actual process. Replace
   it with an executable check run under the same `env -i` assignment (or a
   shell-local `env -i ... node -e` check) for `NODE_OPTIONS`, `NODE_PATH`, all
   `LD_*`, and `PYTHONHOME`. Do not use the outer environment as evidence.

3. Carry the runner's source/identity environment into the direct actual.
   The direct command must include the six source SHA/tree variables, `RUN=1`,
   `TIMELINE_AUTO_REAL_PROXY_RUNTIME_PRODUCER_CHECKOUT`,
   `TIMELINE_AUTO_REAL_PROXY_DEPENDENCY_ROOT`,
   `TIMELINE_AUTO_REAL_PROXY_PRIVATE_ROOT`,
   `TIMELINE_AUTO_REAL_PROXY_RECORD_DIR`, and the literal runner digest; also
   carry `TIMELINE_BUNDLE_AGENT_HEAD` and `TIMELINE_BUNDLE_RUNTIME_HEAD` and
   `TSX_DISABLE_CACHE=1`. These are the inputs required by
   `scripts/testing/auto-real-proxy-main95.mjs:204-248` and the child values
   normally added by `:414-435`. The direct `npm exec` bypasses
   `runRealProxyGate` (`:503-540`), so without this addition it does not
   preserve the runner's effective child context or durable failure-record
   binding.

4. Make exact source and keeper checks executable, not prose. Before the list
   or actual, assert with `git` that `APP` HEAD is exactly App1490, its tree is
   the literal App tree, it is clean, and both approved fixes are ancestors;
   assert the private App `node_modules` symlink resolves exactly to
   `$GRAPH/node_modules`, the graph is physical/symlink-free, and its installed
   Composition/React/React-DOM/Remotion/Player/Three/**Playwright and
   `@playwright/test`** versions are the required exact versions. The existing
   runner checks most package/archive facts at
   `scripts/testing/auto-real-proxy-main95.mjs:325-345`, but does not check the
   graph's symlink-free property or Playwright versions. It also has an App
   guard defect at `:387-395`: App `checkIdentity` receives the current HEAD as
   `expectedHead`, so it checks the App tree but not that current HEAD equals
   the declared App SHA. The packet must supply the missing literal HEAD
   check. Also assert the Runtime manifest SHA
   `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`;
   `checkManifest` at `:294-300` checks producer/version/count but does not
   compare that digest.

5. Add the missing runtime-temp guard. Define and pass
   `XDG_RUNTIME_DIR=$MAIN/run/<short-name>` in both preflight and actual;
   create it before either command, require it and `TMPDIR` to be physical,
   non-symlink, mode `0700`, and assert the resolved temp/profile/socket path
   strings are each under 100 characters. The packet creates/checks only
   `$MAIN/run/t` and does not set `XDG_RUNTIME_DIR`. The existing harness uses
   `tmpdir()` for `mkdtempSync` at `tests/e2e/local/support/harness.ts:461-465`,
   so the short `TMPDIR` must be the effective parent, not merely a prose
   prerequisite.

6. Set `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers` in the preflight too. The
   actual has both Chromium variables, but the preflight has only
   `PLAYWRIGHT_CHROMIUM_EXECUTABLE` (packet lines 165 and 205-206). Verify
   `$NODE --version` is exactly `v20.19.4`; the runner validates Chromium at
   `:352-357`, but neither packet preflight nor runner validates the Node
   binary's version string.

7. Close the private-cache/overlay gap explicitly. The runner normally creates
   a private Vite/Rollup overlay and private `.vite`/`.vite-temp` at
   `scripts/testing/auto-real-proxy-main95.mjs:438-467`. The direct command
   does not call that code. App Vite config has no `cacheDir` use for
   `VITE_CACHE_DIR`, so that variable alone does not redirect Vite's default
   `node_modules/.vite`. Because this packet intentionally points App's
   `node_modules` at a private graph, precreate and assert the graph's
   `node_modules/.vite` and `.vite-temp` are physical private directories and
   assert the shared `/home/user/work/app/node_modules` realpath and contents
   are unchanged. Do not rely on a cleanup command; preserve the durable
   evidence tree.

8. Add executable postflight checks after the actual (while preserving its
   exit status): exact App/Agent/Runtime HEAD/tree and clean status, runner and
   archive hashes, Runtime manifest hash, private graph/package identities, and
   shared-node_modules realpath/write invariants. The packet's lines 256-259
   currently require these only as prose. The direct command has no runner
   `finally` block and therefore has no automatic source/graph postflight.

## Checks that pass as written

- `testDir`, `testMatch`, argv, timeout/worker/retry settings, and the exact
  one-test title are consistent between the existing config/spec and the
  packet. The fixed door is checked by `DirectHarness.start()` at
  `tests/e2e/local/support/harness.ts:461-479`; Runtime, discovery-proxy, and
  Vite ports are allocated natively with port 0 by the existing harness/spec
  (`auto-real-proxy.spec.ts:153-180`). No replacement readiness protocol or
  hard-coded child port is introduced.
- Runtime and credential assembly remains existing harness behavior: the
  Runtime starts with the pinned checkout and dynamic port at
  `harness.ts:516-520`, product credentials are provisioned and written mode
  `0600` at `:573-587`, and the browser receives the credential path through
  existing Vite environment assembly (`auto-real-proxy.spec.ts:165-185`). No
  credential token is added to the packet command.
- Chromium is pinned by the runner's exact path/version/hash guard and the
  direct actual supplies both Chromium variables. App Composition archive
  hash `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  Agent public12 archive hash `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`,
  and Runtime95 manifest source were verified read-only from the pinned source
  repositories.
- Status-zero semantics do not invent failures for unrelated ACP chatter.
  `auto-real-proxy.spec.ts:324-326` records page/console/request-failure
  diagnostics only; relevant HTTP failures are retained only for
  `/api/runtime` and `/runtime-config/v1/operation` at `:327-335`, and
  `expectConnectedWithDiagnostics` fails on readiness at `:289-307`, not on
  arbitrary console text. The final assertions separately require zero legacy
  writer POSTs and the expected task/read/output/media-selection/commit
  traffic at `:500-505`.

## Prior evidence read / scope

The retained r39/r40 evidence was read. The first 29120 boundary was the
existing 60-second `Generate image` readiness wait; its retained classified
HTTP list was empty, and generic browser 503 console lines did not identify a
route or cause. I did not reinterpret that result or rerun the old case. The
approved 209 source report (`design/app-public12-native-none-source.md`) was
read only for provenance; no semantic re-review was performed.

## Tests

Pure targeted tests only; no browser, actual, build, install, socket/live
Runtime, or graph creation was run:

```text
node --test scripts/testing/auto-real-proxy-main95.test.mjs tests/e2e/local/support/auto-real-proxy-observation.test.mjs
PASS — 2 test files, 2 passed, 0 failed, 0 skipped/todo; exit 0.
```

Recommended next step: apply the literal packet corrections above, obtain a
fresh source-only preflight/list-1 result, then perform the one authorized
actual once. Do not treat this review as actual qualification.

## HOME final disposition — 2026-10-21 11:12 UTC
The historical HOLD above applied to the original direct-command packet. It is RESOLVED for the rewritten existing-runner packet by r56, with every listed finding addressed, shell syntax and both original runner/observation controls passing. Product/source/runner implementation bytes are unchanged; no new wrapper or custody authority was introduced. HOME authorizes ONE main actual only after the rewritten complete preflight and exact list1 pass. The old10:40 dispatch hold is SUPERSEDED. This is owner disposition of concrete corrections, not a fabricated independent review or browser pass.
Authoritative current request: design/run-on-main-app-automatic-current.md, SHA-256 516fe8fffc2b68c58f5a4668a5944489d156fed0a66bfa884ac9937b42cd61a0. If this checksum is absent on main, wait for sync; do not use the old packet or infer approval from an older Status line. The first main response REFUSED-PREFLIGHT started0 processes/tests and consumed no actual; retain that result as historical refusal. Source remains exact1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf/tree8e242d1497841f391b6152ecd8d204143fa03b52.
