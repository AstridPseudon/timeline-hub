# App current013 reset final executor

Source: `/home/user/work/wt/app-m3-current013-reset-final-executor`

## Change

- Base: `tl/app-m3-current013-gate5-shared-seed-reset` at `571e93a15b946983b38f7054ae2d01b573cc6b9b`.
- App source tree for the central snapshot: `bb7fe5640bd8cf5b9bf846de92e24fdffa9e9bdf`.
- Known approved b1 source: `b1ef4b9b910ba72375c34cf319692f90d22edc25`, tree `8d8a10b057ed31fed69517e18a23b8ec3811447a`.
- Exact b1-to-current setup delta: 6 insertions in `tests/e2e/local/three-products.spec.ts`, SHA256 `32edc19c668c054aa2281942b1f0d90f56c773e3fd22a346002a6c175ffbf502`.
- Product/test change: line 1021 now calls `await openCommandTimeline(page, harness, seed3);` before the existing Gate 5 UI 5→0 reset. No assertions, pin values, product code, fixtures, or other cases changed.

## Central source tuple and guards

- Agent: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, tree `75354d38c898729bac09619679f5421faba319ed`.
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Runtime schema: `8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`; artifact manifest count 75; Composition archive SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 regular files.
- Public source override and direct App dist were unset. Chromium was `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, version `141.0.7390.37`, SHA256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`.
- Normal fresh hosted build completed. Private node-module overlay and private caches were used. Source, vendor, artifact, peer, and audit start/end guards passed.

## Central run

Requested suite ID: `app-m3-current013-reset-final-executor-e2e-reset-current013-bb7fe564-setup32edc19c-e2e-integration-native-1020140929-22448`.

Exact lane command:

```text
npm run test:e2e:three-products -- --grep 'M1 real'
```

Result: `FAIL`, exit 1, 121 seconds. Three tests were selected serially. The first original M1 durability case failed before its journey because `TIMELINE_BUNDLE_RUNTIME_HEAD` was absent inside the Playwright child; the Gate 5 and dependency-conflict cases did not run. The source tuple logged Agent `d8749a9...` and Runtime `2c4ac18...`; the App `appHead` was the central snapshot identity and was not used as the source-tree gate.

The runner then stopped on the required shared-cache postflight: only the directory mtime of shared `/home/user/work/app/node_modules/.vite-temp` changed (`cache-start` vs `cache-end`); source and artifact guards passed. Labels3 and separate cold-open1 were not requested after the first actual failure.

No full suite, project typecheck, install, local browser/socket run, frame/PCM lane, or automatic rerun was performed.
