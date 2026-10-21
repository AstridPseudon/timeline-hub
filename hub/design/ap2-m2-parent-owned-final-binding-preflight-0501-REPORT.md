# App2 final95 parent binding and preflight

## Result

Updated only the `final95:parent` source binding in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh`

The guarded old helper SHA was:

`b4b142931573d6954af75ee91dd5f1c2c6cbb5a97dc4c65cbdb450ceeec04cb7`

The resulting helper SHA is:

`af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`

The exact two-line diff at lines 65–66 was:

```diff
-    APP_ROOT_SHA=b833512fcb5ef07013c47fcf8c75c4a083048d99
-    APP_ROOT_TREE=a95793cc2179200dd9ef5fe551360a4f6f965ea1
+    APP_ROOT_SHA=a304dce02a185a4774ff514d5aa451c9702aa46f
+    APP_ROOT_TREE=a3c82aa91f1336b86491191acf857d88c56179b2
```

The old-hash guard matched before the edit. No other helper byte, role,
profile, pin, guard, driver, or source file was changed.

## Keeper and tuple

The final keeper was verified before editing:

- App `HEAD`: `a304dce02a185a4774ff514d5aa451c9702aa46f`
- App tree: `a3c82aa91f1336b86491191acf857d88c56179b2`
- App worktree: clean
- required skeleton ancestor: `5d36b0e53ff0d17ef045e226a6e6ca7584322858`
- required ADD forwarding ancestor: `968bbad09449f419ab63782fca49cad805068333`
- `KEEP`: present for the source keeper
- `node_modules`: symlink resolves to `/home/user/work/app/node_modules`

The bound source keeps the qualified HOME bootstrap and the original parent
ADD, durability, raw/opaque/order, retry, reload/restart, undo, and zero-
legacy assertions.

The closed final95 tuple remains:

- App pin: `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`
- Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`
- Runtime and producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00`
- artifact: `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`
- manifest: `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, 76 artifacts
- schema: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
- wire: `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`
- private graph archive: `sha256:895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- Composition archive: `sha256:9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`

The durable 0323 driver is unchanged:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-composed-driver-label-durable-stage-0323/run-parent-manual-drop-evidence.sh`

Driver SHA-256: `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0`.
Its normal caller remains:

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-composed-driver-label-durable-stage-0323/run-parent-manual-drop-evidence.sh run "$PWD"
```

Live callers were unchanged.

## Checks

Evidence was kept in the separate private directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-owned-final-binding-preflight-0501/evidence-final95-parent-a304`

The source-only final tuple preflight passed. This was the exact command
(with the private run root and temporary directory removed after completion):

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 \
  NORMAL014_RUN_ROOT=<private-evidence>/run TMPDIR=<private-tmp> \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh \
  preflight /home/user/work/wt/ap2-m2-parent-owned-final-binding-preflight-0501
```

Result: 76 artifacts verified; manifest and schema matched; the d05e marker,
locked graph, Python imports, and shell guards passed. No cohort or vendor
mismatch was found.

The requested negatives all refused as expected:

- wrong source: central preflight against `/home/user/work/app`, exit 1;
- wrong role: `NORMAL014_APP_SOURCE=bootstrap` against the parent keeper, exit 1;
- wrong graph: `verify_locked_graph` with a nonexistent private graph, exit 1;
- wrong argv: durable 0323 driver with `unsupported`, exit 2;
- zero-child: durable driver `probe`, exit 0 overall because its simulated zero-test child was refused and its evidence-first failure trap passed.

Exact one-test collection passed with the list-only command:

```sh
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR=<private-tmp> \
  node node_modules/playwright/cli.js test --config playwright.three-products.config.ts \
  --grep 'M2 real mounted manual video drop' --list
```

It collected exactly one test: `three-products.spec.ts:1440`.

Also passed:

```sh
sh -n <normal014-source-common.sh> <durable-0323-driver> <normal014-parent-media-central.sh>
```

No guard bypass, browser execution, hosted build, mounted actual, or full
suite was run. The durable wrapper's own `preflight` mode was not invoked
because it performs the prohibited hosted build and Playwright collection;
the established source-only preflight above exercises the permitted tuple and
dependency checks. No actual authorization is claimed.

## Next step

Independent custody review may review the helper hash and the private evidence
directory before any separately authorized mounted ADD. No product writer or
live caller was changed by this task.
