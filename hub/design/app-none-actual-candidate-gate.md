# App native-None actual candidate gate

Date: 2026-10-20  
Result: **FAIL — candidate not qualified; no root release or retirement claim**

## Exact candidate and environment

- App commit/tree: `0bc2d8ebbc724c54745276dffa3bd25e869e7d00` / `81cee4ec952fede797417cbd52be1b006f7a7d99`
- Agent commit/tree: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` / `75354d38c898729bac09619679f5421faba319ed`
- Runtime commit/tree: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `7ab412cc4bcbe517efcfa806e092336390312e18`
- Composition: public12 archive `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; all77 files checked
- Runtime: all75 manifest artifacts checked
- Browser: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, Chromium `141.0.7390.37`, SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`
- Overrides: `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST` unset
- Build: fresh normal hosted Vite build; no pre-existing `dist`
- Runner SHA: `e29e37f2df37630de28ae7dc8f1bc426df5c356f3b1a4e9aa14d95638b6f7fd1`
- Overlay helper SHA: `e16c122b833bd50cd8ca8fd3d1a4c179bd95812a01616afcd7be8fbe31cf6009`
- Discovery helper SHA: `126d171c5149be44abbfff8707c41900aeab7f062179f0eec6581f270713b967`

## Preflight and execution

The actual native-None spec was discovered before execution with the three-products grep and selected exactly two tests:

```text
1382  M2 native None single: ordinary default crossfade clears raw mirrors, reloads, retries exactly after restart and undoes through Runtime
1458  M2 native None bulk: one original-basis atomic clear preserves unknown revision and opaque data; real conflict retains the whole draft
Total: 2 tests in 1 file
```

The current-source control launcher passed:

```text
node --test --experimental-vm-modules tests/e2e/local/support/current013-native-none.test.mjs
```

The central, named `e2e-integration` request was keyed by the exact source tuple and runner identity:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m2-none-actual-candidate-gate e2e-native-none-81cee4ec-d8749a9e-2c4ac180-rune29e37f2-e2e-integration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"

app-m2-none-actual-candidate-gate-e2e-native-none-81cee4ec-d8749a9e-2c4ac180-rune29e37f2-e2e-integration-1020151010-9311
```

The strict preflight passed: exact 40-character tuple, all75, all77/public12, peer versions, Chrome141, no overrides, fresh `dist`, and exactly two discovered tests. The normal hosted build passed (`built in 1m 2s`).

## Product result

The runner stopped on the first product error, preserving the original assertions. The single case failed immediately after selecting the native `None` option:

```text
tests/e2e/local/three-products.spec.ts:1382
setTransitionToNone:304
expected transition control to contain: None
received: crossfade · Built-in
```

Central result: `fail`, exit `1`, duration `99s`. The bulk case at line 1458 did not run (`1 failed`, `1 did not run`). Full central log and trace are retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-none-actual-candidate-gate-e2e-native-none-81cee4ec-d8749a9e-2c4ac180-rune29e37f2-e2e-integration-1020151010-9311/log.txt`

## Partial limits and decisions

There is no evidence from this run for raw absence/reload/inverse behavior, real UI single or atomic bulk clear, lostACK/restart exact request-plus-receipt retry, same-property conflict and draft retention, or the no-legacy-traffic and original-owner guards beyond the preflight. The first product failure was a transition-control state failure, not the known root cold-start/raw-initial-view assertion; no shared-cause conclusion is made.

No App source, test, guard, or assertion was edited. No injected App command or fake provider was used. No `root-current013-READY` marker was created. No full suite, project TypeScript check, install, or framePCM run was performed.

