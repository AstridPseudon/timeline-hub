# App M2 real embedded shot-name gate — source handoff

Status: **prepared, source/lint/discovery only**. This is not browser qualification, integration, or full writer retirement. The root cold-start/initial-basis issue remains a prerequisite owned outside this worker; this gate must fail closed until that root is READY.

## Exact source and pins

The App source starts at `09e377adbba94c99b03ecaa6936d3584c9d307eb`, tree `562236fd6330f6763f0cee263848e5ae491793e2`, on branch `tl/app-m2-shot-name-real-gate-source`. The harness will commit the following working-tree additions; the final App commit/tree are intentionally not guessed here and must be inserted into the central suite key after harness commit:

- `tests/e2e/local/shot-name-command.spec.ts` — SHA-256 `63acc8b490b6c71702d315179182530c09162c9e457730aa9d08a9e880f4a607`
- `playwright.shot-name.config.ts` — SHA-256 `7b881a373643c1aa15f9db09f9c47e888eac05ed17f361c20df69a5a10adb213`
- `tests/e2e/local/support/app.ts` — SHA-256 `754eba0a62b8e3328d02da579032658a55b412bee750ca6e3a64972bf9061e99`
- `tests/e2e/local/support/harness.ts` — SHA-256 `28715d4b3e8508a5b1b840eb57428946ee32568d445d0bc7c31f9c4f8fe9397a`

The repaired production source that this spec exercises is present in the snapshot and is not replaced by the spec:

- `ShotEditorView.tsx` `3ff46cb026aab47651087762d8169f2b9d4a756f1ebc15bc6a1248342ec76088`
- `useNameEditing.ts` `884651d931ea8d22c9fbca844fb2f9b66af0bdc6d127e5fbcf38ce3446942e25`
- `commitSession.ts` `ca0224ff5003d4b6e824f01d934654eb2564faec624103cd573f5c057a301730`
- `shotSetCapture.ts` `ed32897aa9203a6c21c627c679475daf8b6681e7a5bf071d8e4e0bf3adfe5a71`
- `shotSetGesture.ts` `3d1304f460e1f216c0f5c4056fd61a6d67359bbfb95bf312536a53ba448a1f77`
- `useTimelineCommandSession.ts` `a3a2f090498ed82772cb83d9481cbe245efad128de672abc88729274efbdd41b`

Frozen paired inputs for the central run:

- Agent: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` (full 40-character SHA; clean checkout)
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` (full 40-character SHA; clean checkout)
- Runtime producer artifact manifest: exactly 75 artifacts, producer version `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`
- Composition public12: package `0.0.12`, archive SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, exactly 77 regular archive files; Remotion peers remain `4.0.509`
- Chromium: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`
- Required source guard: `scripts/testing/current013-integration.mjs` SHA-256 `82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901`
- Public12 resolver guard: `config/vite/timelineCompositionPackage.test.mjs` SHA-256 `f2115b1e9adefb502f7141ebb7043a3aa44e68a5cade43b25a41b502cfe40740`

`ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST` must be unset. Shared node modules, runtimes, and venvs are read-only. The central runner owns private Playwright/Vite caches and uses a short `TMPDIR` under `/tmp`.

## What the one e2e case drives

The case is `tests/e2e/local/shot-name-command.spec.ts:138`, discovered through the dedicated `playwright.shot-name.config.ts`. It uses the existing direct App/Runtime harness and the seeded three-products parent composition. It never injects an App command, fake port, display ID, or synthetic editor owner.

1. Open `/tools/video-editor`, wait for the real Runtime connection and seeded parent editor, then double-click the actual `[data-shot-group-key]` label for `F2 canonical shot`. Assert the dialog carries `data-canonical-occurrence-id="f2-occurrence"`; this is the production occurrence binding.
2. Read the raw seeded shot revision before editing. Preserve and later compare `name`, `provenance`, and `x_f2_opaque` (`{owner:'f2-shot', nested:[1,{k:'v'}], flag:true}`). Click the production inline name control, then type padded Unicode `  Édit 🎬  `.
3. Assert the actual App commit is one Runtime `shot.set` command with trimmed Unicode `args.values.name`, `select: occurrence:f2-occurrence/shot`, the captured initial `base_revision_id`, original reads/dependency metadata, and no `parent_composition`. Assert the accepted canonical and raw shot payloads preserve provenance and opaque data.
4. Reload, use the parent editor's real `Undo` button, and assert the Runtime `timeline.inverse` receipt restores the exact original raw payload, not merely the displayed label.
5. Route the next real App commit through Runtime, record its exact raw body and `Idempotency-Key`, allow Runtime acceptance, then abort only the browser acknowledgement. Assert the persisted outbox outcome is `retry`, the typed name remains, and after reload/restart/recovery the retry uses byte-identical body and key and receives the same receipt. Undo that accepted retry through the real parent editor.
6. Hold the next actual App request before Runtime acceptance. Clone only its real `shot.set` command to make a direct second Runtime writer set the same shot-name leaf to `Other writer`. Release the held App request and assert Runtime returns `409`, the browser outbox is `rejected`, the exact padded draft `  same-name draft 🎬  ` remains in the real input, and no legacy composition-revision save occurred.

The spec's source guard requires full 40-character Agent/Runtime env pins and clean paired checkouts. The real harness also waits for a connected seeded editor and an existing clean command owner; it does not create a fake readiness basis. If the root cold-start path cannot establish that state, the test is blocked rather than bypassing initialization.

## Writer scope

This gate only covers the embedded canonical `ShotEditorView` path owned by the parent editor session. It does **not** claim these separate writers retired:

- `src/tools/travel-between-images/components/VideoGallery/VideoShotDisplay.tsx` — gallery/list `useUpdateShotName` mutation.
- `src/tools/travel-between-images/pages/ShotEditorView.tsx` — canonical fallback/legacy writer calls around the native branch (`updateCanonicalShotName`/`enqueueCanonicalShotPublish` and `useUpdateShotName().mutate`), plus the separate canonical settings writer.

Those paths remain named explicitly and are outside this bounded source handoff. No settings surface or product behavior was broadened.

## Central suite command

Register/run this as a named, one-worker browser suite after current-root review and the harness commit. The suite key must include the final App commit and tree, not the base values above:

```sh
app shot-name-real-gate-source-app<FINAL_APP_SHA>-tree<FINAL_APP_TREE>-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-public12
```

Its exact command body is:

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env \
  -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST \
  TIMELINE_CURRENT013_RUN=1 \
  TIMELINE_CURRENT013_APP_SHA=<FINAL_APP_SHA> \
  TIMELINE_CURRENT013_APP_TREE=<FINAL_APP_TREE> \
  TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
  TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
  TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=<CLEAN_RUNTIME_PRODUCER_CHECKOUT_AT_2C4> \
  TIMELINE_CURRENT013_PUBLIC_SOURCE_SHA256=fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28 \
  TIMELINE_CURRENT013_SETUP_SHA256=<CURRENT_ROOT_REVIEWED_SETUP_SHA256> \
  TIMELINE_CURRENT013_SHORT_TMPDIR=/tmp/tl-shot-name-real-<FINAL_APP_SHA> \
  TIMELINE_CURRENT013_CACHE_ID=app<FINAL_APP_SHA>-tree<FINAL_APP_TREE>-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-runners<FINAL_RUNNER_SHA> \
  TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
  TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
  ASTRID_CHECKOUT=<CLEAN_AGENT_CHECKOUT_AT_D874> \
  ASTRID_RUNTIME_CHECKOUT=<CLEAN_RUNTIME_CHECKOUT_AT_2C4> \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  PLAYWRIGHT_OUTPUT_DIR=/tmp/tl-shot-name-real-<FINAL_APP_SHA>/artifacts \
  PYTHONDONTWRITEBYTECODE=1 NODE_OPTIONS=--max-old-space-size=4096 TSX_DISABLE_CACHE=1 \
  node_modules/.bin/playwright test --config playwright.shot-name.config.ts
```

The central wrapper must perform the normal current013 source preflight/postflight around that command, including all-40-SHA checks, App/Agent/Runtime cleanliness, 75-artifact and 77-file public12 checks, normal vendor-lock checks, cache identity, and source-tree equality. `<FINAL_APP_SHA>`, `<FINAL_APP_TREE>`, `<CURRENT_ROOT_REVIEWED_SETUP_SHA256>`, and `<FINAL_RUNNER_SHA>` are mandatory resolved values; leaving any placeholder or using moving `/home/user/work/{agent,runtime}` heads is a refusal, not a run. Request it only after source review/current-root READY; do not request a full suite.

## Source-only evidence and remaining blocker

Passed in this worker:

```text
eslint playwright.shot-name.config.ts tests/e2e/local/shot-name-command.spec.ts tests/e2e/local/support/app.ts tests/e2e/local/support/harness.ts --ext ts --max-warnings 0
git diff --check
node --test scripts/testing/current013-integration.test.mjs       # 1 passed
TMPDIR=/tmp/tl-shot-name-discovery-final PLAYWRIGHT_OUTPUT_DIR=/tmp/tl-shot-name-discovery-final-output node_modules/.bin/playwright test --config playwright.shot-name.config.ts --list  # 1 test
```

The immutable public12 resolver guard was also run, but is **not green in this worker**: `node --test config/vite/timelineCompositionPackage.test.mjs` reports the installed shared `@banodoco/timeline-composition` as `0.0.10` where the guard requires `0.0.12`. No shared dependency was changed. This must be repaired/qualified by the central private overlay; it is not a reason to weaken the guard.

No browser, build, socket, full suite, TypeScript check, install, or central test-service request was run here. The next step is current-root readiness plus central execution of this exact named case under the frozen tuple.
