# Combined native1920/Chrome155 diagnostic candidate — complete preparation, no actual run

Read PLAN first. Verified completed environment prep exit0 and final branch/HEAD78599b3809f18e9e87542d71b03b92a340e1e579; completed separate fixture proposal exit0/finalc3830b789e48badc1789572d8892e71a448a5827. Read both ORCHREPORTs and proposal.patch. Both descend from completed headers1e13. No decisions were relitigated or product code changed.

## Result and decisions

Twelve changed/new test/config paths, with ONE shared four-case registration and two tiny original/native spec entries. Existing helpers take a small explicit canvas argument, default640. Original Chromium141 config AND intermediate Chrome155/original640 config remain byte-identical. New separately named normal-profile-native1920 config selects authored1920 and named Chrome155 before fixture/capture. The finite browser-profile harness is reused. No copied nine-file proposal variants adopted; no redundant adopted copies remain.

All seven approved fda6 product paths match the completed environment worker's exact hashes. Original source video generation, WAV, download observer, authority/admission/bootstrap/browser-profile helpers and ALL eight original neighboring test files remain byte-identical. verify-scope.py proves the shared four-case source is EXACTLY the predecessor after reversing ONLY import relocation/indentation, explicit canvas forwarding and dimension-specific marker/metric substitutions. Fixture source also exactly reverses to predecessor after only its import/argument/resolution substitution: canonical parent/shot/internal revision and digest construction unchanged. No task-owned profile/authority input, alternate export, product flag, tolerance change or comparator resizing.

Retained controls: actual catalog/task admission and poll, immutable task/spec/revision/source checks, location/full200/nativeBlob transfer and exact bytes/hash/association/provenance, exact downloaded/decode dimensions, every12 frames, RGB2/255 and fraction.001, native scale1/DPR1, full baseline before frame52 picture-only negative, strict nativeMediaError/auth/abort qualification. Normal profile/default1920 with absent profile is existing evidence. Old output640 is still ignored by that existing authority; this candidate does not fix or delete that product-contract diagnostic. AAC48kHz/stereo assertions are metadata, not independent PCM parity.

## Exact targeted commands and results

All commands below ran from /home/user/work/wt/vw-m3-native-frame-combined-candidate. Logs outside repo. Define:

```sh
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
OWN=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-native-frame-combined-candidate
```

Each directly executed, exit0, zero failed/skipped:

```sh
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/canvas.test.ts          # 8/8
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/download.test.ts        # 58/58
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/diagnostics.test.ts     # 141/141
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/compare.test.ts         # 3/3
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/authority.test.ts       # 2/2
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/admission.test.ts       # 5/5
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/harness.test.ts         # 5/5
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/bootstrap.test.ts       # 19/19
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/browser-profile.test.ts # 4/4
"$NODE" --import /home/user/work/wt/vw-m3-native-frame-combined-candidate/node_modules/tsx/dist/loader.mjs "$OWN/native1920-diagnostics.test.ts" # 141/141
```

245 repository unit cases +141 external native diagnostic cases =386 passes. New8 verify both native dimension guards (wrong host/canvas/truncation/extra), unchanged exact2/.001 boundaries and baseline-before-picture rejection, all45 source-marker coordinate values directly in each canvas, legacy defaults, explicit config/browser selection and shared four-case registration/order. External native diagnostics reuse ALL original141 names/expectations with only valid proof1920 dimensions and fixed-canvas helper forwarding/import paths; no altered expectation or waived failure, no copied variant lands in repo.

```sh
"$NODE" node_modules/eslint/bin/eslint.js playwright.viewing-parity.normal-profile-native1920.config.ts tests/e2e/timeline/player-export-frame-parity.spec.ts tests/e2e/timeline/player-export-normal-profile-native1920.spec.ts tests/e2e/timeline/viewing-parity/{canvas,canvas.test,cases,compare,diagnostics,fixture,frames,harness}.ts --max-warnings 0
# PASS exit0, lint.log empty.
"$NODE" node_modules/typescript/bin/tsc --project tests/e2e/timeline/viewing-parity/tsconfig.json --noEmit
# Exit2: ONLY unchanged tests/e2e/local/support/harness.ts:630 TS2352 clips/never[].
cmp -s "$OWN/typecheck.log" "$OWN/../vw-m3-chrome155-parity-environment-prep/typecheck.log"
# PASS exit0, byte-identical diagnostic, no changed-file TS error.
"$NODE" node_modules/playwright/cli.js test --config playwright.viewing-parity.config.ts --list
"$NODE" node_modules/playwright/cli.js test --config playwright.viewing-parity.normal-profile-native1920.config.ts --list
"$NODE" node_modules/playwright/cli.js test --config playwright.viewing-parity.normal-profile-native1920.config.ts player-export-normal-profile-native1920.spec.ts --project native-codec-chrome155 --list
# All PASS exit0; exactly4 identical shared case titles each, no launch/globalSetup.
```

## Frozen source/environment and guarded controller

```sh
"$NODE" "$OWN/run-native-frame-parity.mjs" --freeze
ASTRID_CHECKOUT=/home/user/work/wt/vw-m3-host-agent-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/vw-m3-runtime-source-lease2 TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/composition ASTRID_REMOTION_PROJECT_DIR=/home/user/work/wt/vw-m1-ssr-snapshot/remotion ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell "$NODE" --import tsx "$OWN/run-native-frame-parity.mjs" --verify-sources
"$NODE" --check "$OWN/run-native-frame-parity.mjs"
bash -n "$OWN/setup-native-frame-parity.sh"
python "$OWN/verify-scope.py"
git diff --check
git apply --reverse --check "$OWN/candidate.patch"
git apply --reverse --check "$OWN/combined.patch"
```

All PASS exit0. Freeze is final App5958 files / SHA2561d91c6e41eebcb0690e82fa119c7400df49d695a96fbcd3a697079e042387e46. Chrome selected ELF cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76, version155.0.8059.84, full255-file Chrome directory; CPU export1194 full12-file directory; Playwright106 files; Node20.19.4/full ELF. Environment hashes equal the completed prep except the separately named config. Version comes from retained calibration/offline dpkg metadata, not a newly launched browser.

Offline preflight verifies BOTH complete77-file Composition8 installs, BOTH six-target Remotion graphs, approved artifact/package versions, exact clean b70/9f9/f816/ff053 source leases. Full identities are in manifest.json/source-preflight.json/source-freeze.json. This consumes installed8 and historical leased peers: DIAGNOSTIC ONLY, no current/public10/public11/gate6/M3/adoption qualification.

Fresh central controller binds native1920 canvas/config/project and exact final content instead of the earlier uncombined-fixture boolean hold. It requires a NEW grant with both explicit decision references and final combined manager review. Its unique oneShot is vw-m3-native-frame-combined-candidate-20261020, exclusively consumed before actual browser work. No grant or RUN_STARTED marker exists. Guarded central .test-* snapshot requires clean source, directory/.git device+inode+contents preservation, QUIET absence and actual held flock. Source/environment/lease checks happen before globalSetup and in finally/postflight after failure too; grant bytes/flock/QUIET are rechecked. Browser launch must report exact pinned version. Four expected passes, no skipped/flaky/unexpected, no retries.

## Handoff and remaining holds

ORCHREPORT/README/commit-msg are outside repo. Flat ORCH/design copies have prefix handoff-vw-m3-native-frame-combined-candidate-; exported report, candidate.patch (base78599), combined.patch (baseheaders1e13), manifest, source freezes/preflight, controller/setup, scope checker and logs. No repo docs/build output/temp files, git mutation, push, install, network, browser/render/socket/full/test-service run or suite registration.

Preparation is complete; actual run remains ungranted. Next: manager reviews final source + both decisions (fixture approval and orchestrator environment escalation0459), reviews the exact frozen manifest, then alone creates the NEW grant/registers/requests the named DIAGNOSTIC central suite as described in README. Real saved MP4/frame/nativeMediaError behavior remains UNVERIFIED for this combined tree. The calibration is environmental evidence only. No PCM parity or gate6/current tuple claim. DONE means bounded preparation complete, not permission to run.
