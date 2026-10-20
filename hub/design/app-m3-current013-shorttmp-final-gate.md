# App current013 short-TMP final browser gate

## Result

The bounded corrected run reached real Chromium 141 successfully with the diagnosed short temporary path, then stopped on the first actual product/provider failure. It is **not qualified** and is **blocked** pending manager follow-up.

Central TestID: `app-m3-current013-shorttmp-final-gate-e2e-shorttmp-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020135002-10356`

Named suite: `e2e-shorttmp-public-current013-b1ef4b9-d8749a9-2c4ac18-integration`

Exact request:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m3-current013-shorttmp-final-gate e2e-shorttmp-public-current013-b1ef4b9-d8749a9-2c4ac18-integration --files three-products
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-m3-current013-shorttmp-final-gate-e2e-shorttmp-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020135002-10356 1
```

Result: **exit 1, 124 seconds; 1 failed, 6 did not run**. The hosted build passed: Vite transformed 5,567 modules and completed in 1m12s. Chromium launched and the first page opened; this is not the prior SIGTRAP.

First failure, unchanged original case `tests/e2e/local/three-products.spec.ts:341`:

```text
astrid call exited 1: -m astrid timelines publish d0b6f454-dd5e-4a7a-be41-3e480130e96f --project direct-journey-e9f6c6 -m agent: marker --idempotency-key f2-case1 --json
unstructured - this is a bug.
tracked timeline publication requires a timeline command
recovery: retry the command; if it repeats, report this bug
```

This is a concrete pinned Agent/provider product failure, not an HTTP/UI assertion failure and not a browser launch failure. Per the brief, the three regular label cases and the separate cold-open case were not submitted and have no TestIDs.

## Frozen inputs and environment

| Input | HEAD | TREE |
| --- | --- | --- |
| App | `b1ef4b9b910ba72375c34cf319692f90d22edc25` | `8d8a10b057ed31fed69517e18a23b8ec3811447a` |
| Agent/provider | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` | `75354d38c898729bac09619679f5421faba319ed` |
| Runtime/producer | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |

`ASTRID_CHECKOUT` was the exact Agent keeper; `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST` were unset. The normal tracked browser bundle was verified before and after: 155 browser provenance files, 20 public-host imports, and canonical source hash `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`. Normal vendor verification passed: 65 pinned build inputs and 155 `vendor/astrid-browser` files.

The Runtime contract remained 0.2.13, schema `8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, artifact `6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, with all 75 manifest artifacts and both normal locks unchanged. Composition 0.0.12 remained SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, all 77 regular members, and expected peers.

The runner assigned `TMPDIR=/tmp/tl13-e2e-8d8a` last, after private npm/Playwright/XDG cache assignments; long XDG paths were retained as authorized by the diagnosis. The log printed the actual profile and final launch arguments:

```text
TMPDIR=/tmp/tl13-e2e-8d8a
user-data-dir=/tmp/tl13-e2e-8d8a/playwright_chromiumdev_profile-iGqidZ
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --disable-field-trial-config --disable-background-networking --disable-background-timer-throttling --disable-backgrounding-occluded-windows --disable-back-forward-cache --disable-breakpad --disable-client-side-phishing-detection --disable-component-extensions-with-background-pages --disable-component-update --no-default-browser-check --disable-default-apps --disable-dev-shm-usage --disable-edgeupdater --disable-extensions --disable-features=AvoidUnnecessaryBeforeUnloadCheckSync,BoundaryEventDispatchTracksNodeRemoval,DialMediaRouteProvider,GlobalMediaControls,HttpsUpgrades,LensOverlay,MediaRouter,PaintHolding,ThirdPartyStoragePartitioning,Translate,Auto-DeElevate,RenderDocument,OptimizationHints,msForceBrowserSignIn,msEdgeUpdateLaunchServicesPreferredVersion --enable-features=CDPScreenshotNewSurface --allow-pre-commit-input --disable-hang-monitor --disable-ipc-flooding-protection --disable-popup-blocking --disable-prompt-on-repost --disable-renderer-backgrounding --force-color-profile=srgb --metrics-recording-only --no-first-run --password-store=basic --use-mock-keychain --no-service-autorun --export-tagged-pdf --disable-search-engine-choice-screen --unsafely-disable-devtools-self-xss-warnings --edge-skip-compat-layer-relaunch --disable-infobars --disable-search-engine-choice-screen --disable-sync --enable-unsafe-swiftshader --headless --hide-scrollbars --mute-audio --blink-settings=primaryHoverType=2,availableHoverTypes=2,primaryPointerType=4,availablePointerTypes=4 --no-sandbox --no-sandbox --disable-dev-shm-usage --no-proxy-server --host-resolver-rules=MAP astrid.test 127.0.0.1, MAP evil.test 127.0.0.1, MAP *.supabase.co 127.0.0.1:1, MAP *.supabase.in 127.0.0.1:1 --ignore-certificate-errors-spki-list=k3h++6wpzkdROiRqKXhvGiqAPkXkL8SxzGKcUS2AvSk= --ip-address-space-overrides=127.0.0.1:37145=public --user-data-dir=/tmp/tl13-e2e-8d8a/playwright_chromiumdev_profile-iGqidZ --remote-debugging-pipe --no-startup-window
```

Chrome was the preinstalled `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, version `141.0.7390.37`, SHA256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`. No browser install, Chromium 155, frame grant, source overlay, provider fake, stale dist, assertion change, or HOME reassignment was used.

## Boundary evidence and prior evidence

The source end guard passed with the same App tree and both normal source heads. The normal vendor verifier, tracked public-source verifier, all-75 artifact/lock check, public12 77-file check, and private module overlay/cache checks passed after the failed lane. The short temporary root was removed. The App worktree remained clean with no tracked or untracked changes.

The Chromium diagnosis remains valid: TestID `app-m3-chromium141-launch-diagnose-chromium141-launch-diagnose-integration-1020133523-30467` passed with one long-TMP SIGTRAP reproduction and three short-TMP actual JavaScript/DOM passes. Historical restore evidence may be cited honestly: TestID `app-m3-current013-restore-consumer-gate-restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration-1020130731-30085` passed 2 tests on the earlier App tree; its provider/restore inputs were byte-equal to this pair. It does not qualify this final browser journey.

## Limits and next step

M1/Gate-5 actual UI acceptance is blocked at the first case. The six later cases, regular labels, separate cold-open, full App suite, frame/PCM parity, and owner-film viewing remain unverified. Manager follow-up should investigate the exact `timelines publish` contract mismatch in the frozen Agent/provider pair and schedule a new bounded run only after that decision; no automatic browser rerun is justified by this result. Root merge is not ready from this gate.
