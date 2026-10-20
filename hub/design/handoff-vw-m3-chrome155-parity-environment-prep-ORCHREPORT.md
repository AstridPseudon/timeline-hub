# Chrome155 native-codec environment preparation complete; actual run held

Read PLAN first. Base App 1e13eadfc6ba5f96a1cd570893bd3743fed5f666. Changed only existing parity harness/spec source-version arguments/direct tests/tsconfig and added browser-profile.ts, browser-profile.test.ts, playwright.viewing-parity.native-codec.config.ts. No product paths, auth/provider/Agent/Runtime/pins, fixture, comparator, diagnostic classification or download assertions changed. All seven approved fda6 product paths remain byte-identical (scope-check.json). The brief's final seven product paths are preserved, not reimplemented.

## Result and choices

Added a finite pair of profiles: chromium141 (default, unchanged installed executable/version) and explicit native-codec-chrome155 (/opt/google/chrome/chrome, 155.0.8059.84). A separate config names only the latter project, importing the existing original config. Metadata selects the same shared harness and all four original cases. No global PLAYER_BROWSER flip, arbitrary env executable, browser fallback, duplicate harness or product flags. Unknown profile values refuse before source reads/launch. The exported PLAYER_BROWSER remains the original141 default.

sourceVersions(profile) now records the ACTUALLY selected Player executable/profile/full SHA256/expected version and verifies those exact bytes, plus unchanged CPU export headless1194 full bytes. All sourceVersions call sites in the four-case spec and browser lifecycle select the actual project profile; the post-render check selects the recorded profile. Browser launch uses that verified path and must report the exact pinned version. Teardown checks the same profile even after a launch/test failure. Existing peer77 and six graph guards stay intact. Expected155 version derives from retained calibration1020045451-13230 and offline installed dpkg metadata; no browser --version or actual decode was executed here.

Original141 config is BYTE UNCHANGED. Normalizing only the four sourceVersions arguments makes the spec byte-identical to base, proving every existing case/expectation remains. Fixture/media/comparator/frames/download/diagnostics are byte-identical. Thus actual admitted-task/location/full200/hash/nativeBlob transfer, ffprobe/full-artifact, 12-frame/RGB2/.1%, negative controls, strict nativeMediaError and cancellation qualification requiring the actual same-case video currentSrc/metadata/error-null are preserved. No waiver based on canPlayType, calibration or synthetic media flags.

New controller is CONDITIONAL READY only. It pins this environment-only source and exact diagnostic peer tuple, full selected Chrome directory/export browser directory/Playwright directory/Node bytes, Node20.19.4, clean peer heads/trees, central snapshot dev/inode/.git/content, actual flock, unique grant/one-shot, QUIET, and finally/postflight including failures. frozenDimensionUnitReady=false explicitly prevents an actual run even with a grant while the separate dimension proposal is uncombined. Manager must replace that hold with concrete reviewed fixture/config identity AFTER both final reviews and orchestrator environment approval, then freeze the combined candidate. No running worker branch adopted. README gives exact gates and proposed manager-only central registration/request.

## Exact validation commands and results

Working directory /home/user/work/wt/vw-m3-chrome155-parity-environment-prep. Absolute managers/viewing/QUIET.md was absent before CPU work. All logs outside repository. Define:

```sh
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
OWN=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-chrome155-parity-environment-prep
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/browser-profile.test.ts
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/harness.test.ts
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/download.test.ts
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/diagnostics.test.ts
"$NODE" node_modules/eslint/bin/eslint.js playwright.viewing-parity.native-codec.config.ts tests/e2e/timeline/player-export-frame-parity.spec.ts tests/e2e/timeline/viewing-parity/browser-profile.ts tests/e2e/timeline/viewing-parity/browser-profile.test.ts tests/e2e/timeline/viewing-parity/harness.ts tests/e2e/timeline/viewing-parity/harness.test.ts --max-warnings 0
"$NODE" node_modules/typescript/bin/tsc --project tests/e2e/timeline/viewing-parity/tsconfig.json --noEmit
```

Profile4/4, harness5/5, download58/58, diagnostics141/141 PASS exit0, no skipped/failed (208 total). Scoped lint PASS exit0. Typecheck exit2 ONLY unchanged tests/e2e/local/support/harness.ts:630 TS2352 clips/never[]; output byte-identical to completed predecessor's typecheck.log. No changed-file type errors. New tests cover default141, explicit155 config identity, same shared suite/options, unknown names/path/prototype/nonstring refusal, full file hashing past first chunk, and postflight refusal on selected profile/browser bytes/export bytes changes.

```sh
"$NODE" node_modules/playwright/cli.js test --config playwright.viewing-parity.config.ts --list
"$NODE" node_modules/playwright/cli.js test --config playwright.viewing-parity.native-codec.config.ts --list
"$NODE" "$OWN/run-native-codec-parity.mjs" --freeze
ASTRID_CHECKOUT=/home/user/work/wt/vw-m3-host-agent-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/vw-m3-runtime-source-lease2 TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/composition ASTRID_REMOTION_PROJECT_DIR=/home/user/work/wt/vw-m1-ssr-snapshot/remotion ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell "$NODE" --import tsx "$OWN/run-native-codec-parity.mjs" --verify-sources
ASTRID_CHECKOUT=/home/user/work/wt/vw-m3-host-agent-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/vw-m3-runtime-source-lease2 TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/composition ASTRID_REMOTION_PROJECT_DIR=/home/user/work/wt/vw-m1-ssr-snapshot/remotion ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell "$NODE" --import tsx "$OWN/verify-selected-profiles.mjs"
"$NODE" --check "$OWN/run-native-codec-parity.mjs"
bash -n "$OWN/setup-native-codec-parity.sh"
git diff --check
git apply --reverse --check "$OWN/environment.patch"
```

All PASS exit0. Original141 and named155 each collect exactly4 cases; collection only, no execution/globalSetup. Source preflight verifies exact clean b70/9f9/f816/ff053 peers, both77 Composition graphs, both six-file render graphs, exact installed8 artifact, package versions, CPU browser1194, full selected155 executable and full environment directory bytes/Node20.19.4. Offline dual-profile check verifies complete sourceVersions differ ONLY in selected Player identity; every other field including peer graphs and CPU export executable/hash is equal. Controller/setup syntax, whitespace, complete patch reverse applicability and scope checks PASS. Initial multi-file node --test smoke also passed; the per-file runs above are the detailed counted unit evidence.

Prepared source: 5953 files / SHA256 a228c554799f595da3d7ce763f62284ad93021e90bcc748f21e46fabbcf73700. This is NOT a final combined candidate or current tuple qualification. source-freeze.json records full environment hashes. No actual browser/render/socket/central/full/install/network/service run, suite registration, grant or run marker was performed. No build output/temp files in worktree. No push/git mutation.

## Hold and next steps

Bounded prep is complete. Actual four-case MP4/frame evidence remains UNVERIFIED and ungranted until manager reviews this patch AND separate normal-profile-native fixture proposal and receives orchestrator environment approval. Then combine reviewed changes, replace the explicit controller dimension hold with concrete native fixture/config checks, re-freeze final source and repeat collection/offline preflight before a unique central one-shot. Do not claim calibration/unit/preflight as a product pass. Current Runtime/public10/source tuple unchanged; consumed b70/9f9/f816 + installed8 stays labelled DIAGNOSTIC. No M3/gate/adoption claim.

## Flat handoff files (COMMS04:50)

All following files copied directly to ORCH/design/ with prefix handoff-vw-m3-chrome155-parity-environment-prep-. Restore original basenames together outside the repo when using the controller. environment.patch includes all7 changed/new repo paths and applies on the stated completed base; original test config/fixture/comparator are preserved.

- design/handoff-vw-m3-chrome155-parity-environment-prep-ORCHREPORT.md
- design/handoff-vw-m3-chrome155-parity-environment-prep-README.md
- design/handoff-vw-m3-chrome155-parity-environment-prep-environment.patch
- design/handoff-vw-m3-chrome155-parity-environment-prep-run-native-codec-parity.mjs
- design/handoff-vw-m3-chrome155-parity-environment-prep-setup-native-codec-parity.sh
- design/handoff-vw-m3-chrome155-parity-environment-prep-source-freeze.json
- design/handoff-vw-m3-chrome155-parity-environment-prep-source-preflight.json
- design/handoff-vw-m3-chrome155-parity-environment-prep-source-preflight.log
- design/handoff-vw-m3-chrome155-parity-environment-prep-verify-selected-profiles.mjs
- design/handoff-vw-m3-chrome155-parity-environment-prep-selected-profiles.json
- design/handoff-vw-m3-chrome155-parity-environment-prep-scope-check.json
- design/handoff-vw-m3-chrome155-parity-environment-prep-profile-tests.log
- design/handoff-vw-m3-chrome155-parity-environment-prep-harness-tests.log
- design/handoff-vw-m3-chrome155-parity-environment-prep-download-tests.log
- design/handoff-vw-m3-chrome155-parity-environment-prep-diagnostics-tests.log
- design/handoff-vw-m3-chrome155-parity-environment-prep-lint.log
- design/handoff-vw-m3-chrome155-parity-environment-prep-typecheck.log
- design/handoff-vw-m3-chrome155-parity-environment-prep-collection-141.log
- design/handoff-vw-m3-chrome155-parity-environment-prep-collection-155.log
