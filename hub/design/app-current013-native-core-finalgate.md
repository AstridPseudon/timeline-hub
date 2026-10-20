# App current013 native core final gate

## Result

The final App `b1` / tree `8d8a10b057ed31fed69517e18a23b8ec3811447a` native current013 gate is **not qualified**. The first requested native case passed; the second requested native case failed at an existing positive assertion. Per the brief, execution stopped immediately: the third native conflict case, regular-label lane, and separate cold-open lane were not run.

Central TestID for the actual lane: `app-m3-current013-native-core-finalgate-e2e-native-core-current013-b1-tree8d8a-agentd874-runtime2c4-e2e-integration-native-1020135745-7128`.

Runner-only preflight TestID: `app-m3-current013-native-core-finalgate-e2e-native-core-current013-b1-tree8d8a-agentd874-runtime2c4-e2e-integration-native-1020135652-18512`.

Result: exit 1 in 124 seconds; hosted build passed; Chromium 141 launched; 1 passed, 1 failed, 1 did not run.

## Exact command

The central named suite was `e2e-native-core-current013-b1-tree8d8a-agentd874-runtime2c4-e2e-integration-native`. Its literal command supplied the requested pins and ran:

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST \
  TIMELINE_CURRENT013_SHORT_TMPDIR=/tmp/tl13-core-b1 \
  TIMELINE_CURRENT013_APP_TREE=8d8a10b057ed31fed69517e18a23b8ec3811447a \
  TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
  TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
  ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  TIMELINE_CURRENT013_CACHE_ID='appb1ef4b9b910ba72375c34cf319692f90d22edc25-tree8d8a10b057ed31fed69517e18a23b8ec3811447a-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-tree7ab412cc4bcbe517efcfa806e092336390312e18-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-e2e-integration-native-private-node-overlay' \
  bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-native-core-finalgate/notes/run-lane.sh native
```

The exact selected subprocess was:

```text
npm run test:e2e:three-products -- --grep 'M1 real'
```

The first submission stopped in the worker-only audit because it incorrectly required the central synthetic snapshot `HEAD` to equal b1; it ran no browser/build. After correcting that runner-only check to validate the exact App tree, the actual lane was submitted once with `--no-cache` under the TestID above.

## First actual failure

The first native test passed:

```text
tests/e2e/local/three-products.spec.ts:904:1
M1 real gesture: lost durable ACK, dependent B, reopen, Runtime restart, exact retry and UI undo preserve independent Agent work
```

The second native test failed:

```text
tests/e2e/local/three-products.spec.ts:1017:1
M2 real gate 5 (M1 real mounted path): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent
```

Existing assertion at `tests/e2e/local/three-products.spec.ts:859-860` expected the submitted `clip.move` command to have `args.on: 5`. The received command had `args.on: 8.333333015441895`; base revision/publication and selection were otherwise present in the diff. This is an actual product/behavior test failure on the pinned tuple, not a browser launch or preflight failure.

The third `M1 real dependency conflict retains B original guards and pending identity` test did not run. The labels and cold-open lanes were not submitted.

## Verified inputs and postflight

- App exact tree: `8d8a10b057ed31fed69517e18a23b8ec3811447a`; requested App commit b1 `b1ef4b9b910ba72375c34cf319692f90d22edc25`.
- Agent CLI: `ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source`, commit `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, tree `75354d38c898729bac09619679f5421faba319ed`.
- Runtime/producer: `/home/user/work/wt/app-m3-runtime013-producer-source`, commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST`: unset.
- Chromium: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, version 141.0.7390.37, SHA256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`; short browser temp root was `/tmp/tl13-core-b1`.
- Normal fresh hosted build completed successfully. The build transformed 5,567 modules.
- Runtime contract remained 0.2.13 with schema digest `8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, artifact digest `6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, and all 75 manifest artifacts verified.
- Composition archive remained SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, with all 77 regular members and expected peers.
- Tracked public-browser source bundle remained SHA256 `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28` across 155 provenance files and 20 public-host imports.
- Private node-module overlay, normal locks, source/config hashes, external SHAs, and cache fingerprints passed before and after the failing lane. The App source end guard passed.

## Release facts and next step

This result does not release the gate or authorize root merge. No App product/test source, pin, fixture, or assertion was changed. Investigate the existing `clip.move` position mismatch on the exact b1/d874/2c4 tuple; rerun only after the manager makes that decision. No labels or cold-open evidence exists for this gate.
