# HOME HOLD — 2026-10-21 11:00 UTC
DO NOT EXECUTE prompt packet until current-preserving source r45 is committed and final SHA/tree/runner hash is bound. Prior READY text below was source preparation only, superseded. Existing AutoDisable PASS must not replay. This distinct prompt proof has not been requested from main yet.

# Main prompt-only Settings proof packet

**Status: READY for the central Main95 preflight/list gate; actual browser execution is intentionally unrun here.**

This packet selects exactly one new prompt case. It does not replay the already-approved `SettingsAutoDisable` PASS.

## Scope and source approval

- Staged source role: local `tl/app-m2-settings-prompt-native-proof-source-r43`, base commit `f18ec17cc45de18c3355e01170d3e868db17e4b7`, base tree `353e0282064f1179f37b8f9eab2d707a7beae02f`.
- Hub branch `hub/timeline/app/tl/app-m2-settings-prompt-native-proof-source-r43` remains the approved callback source `cd927abfa09b6f8571cfeb282763855af3e44541`, tree `d0fb6127a1f648d49a496cce997b3ed577a8d413`. The staged source changes only `tests/e2e/local/shot-name-command.spec.ts` relative to that callback.
- The only packet setup correction is the literal `SETTINGS_CASE` and its discovery labels in `scripts/testing/main95-prompt-settings-integration.mjs`; they now equal the exact new test title:

  `M2 real embedded settings prompt: native shot.set preserves exact raw settings, retries after restart, and undoes through Runtime`

- The harness must record the final post-commit App 40-character SHA/tree for the source guard; do not substitute a moving branch or an uncommitted tree. The base identity above is retained for provenance.

## Product/source approval boundary

The source path is native. `BatchSettingsForm` renders `#batchVideoPrompt` and calls `onBatchVideoPromptChange` from the mounted `BatchModeContent` path. The approved `cd927` callback is unchanged: `handleBatchVideoPromptChange` calls `onSettingsIntent({ prompt })` before updating the local draft; `ShotEditorView` supplies `handleSettingsIntent`, which captures the occurrence-owned `shot.set` command. The new case checks the emitted Runtime command, including `op: 'shot.set'`, occurrence selector, prompt-only values, reads, and absence of `parent_composition`; it is not an SDK/private settings write.

The new case retains all required assertions:

- initial and accepted/reloaded raw settings preserve `negativePrompt: null` and `x_settings_opaque`;
- accepted prompt write is exact and prompt-only;
- a lost acknowledgement is retried after page/runtime restart with identical body and idempotency key;
- Runtime inverse undo restores the accepted prompt state;
- legacy composition-revision POST traffic is exactly `[]`.

These are product/source assertions only. No browser, Runtime door, actual prompt journey, build, install, graph construction, or full suite was run by this worker.

## Frozen roles and graph

Reuse the existing Main95 runner and guards in `scripts/testing/main95-prompt-settings-integration.mjs` and `playwright.shot-name.config.ts`; no new framework or shared-state change is permitted.

| Role | Required identity |
|---|---|
| Agent execution | `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556` |
| Agent public vendor | `091aa23ec83ea05ffd3b0115a640230d51c8c429`, tree `e3ae90fe482ba6cad6c3f94069127faf76ebceb6` |
| Runtime producer/execution | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Composition | `0.0.13`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, exactly 77 regular archive members |
| Browser | `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`, `Chromium 141.0.7390.37` |
| Node | `/opt/node20/bin/node` via `PATH=/opt/node20/bin:/usr/local/bin:/usr/bin:/bin`; central host must verify the requested Node `20.19.4` before actual execution |

The reusable private graph is `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules`, a real non-symlink directory, with READY/LEASE records certifying the all-77 Composition graph and Playwright `1.60.0`. It is read-only for this packet. The App shared `/home/user/work/app/node_modules` remains untouched.

## Central command

Run once through the central service after the harness has committed the source-setup correction and substituted its final App SHA/tree. The `SKIP_BROWSER` form is the required preflight/list invocation; omit only that variable for the later single actual journey.

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env \
  -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST -u NODE_PATH \
  PATH=/opt/node20/bin:/usr/local/bin:/usr/bin:/bin \
  TIMELINE_MAIN95_PROMPT_RUN=1 \
  TIMELINE_MAIN95_PROMPT_SKIP_BROWSER=1 \
  TIMELINE_MAIN95_PROMPT_APP_TREE=<FINAL_APP_TREE_FROM_HARNESS> \
  TIMELINE_MAIN95_PROMPT_AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
  TIMELINE_MAIN95_PROMPT_RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
  TIMELINE_MAIN95_PROMPT_RUNNER_SHA256=sha256:b7d0732b02a533a091c76bb7a163376900725db1b5ac067979a638134800ed88 \
  ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6efc8150 \
  TIMELINE_MAIN95_PROMPT_VENDOR_CHECKOUT=/home/user/work/wt/agt-pin-091aa23e \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
  TIMELINE_MAIN95_PROMPT_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  TIMELINE_MAIN95_PROMPT_PRIVATE13_NODE_MODULES=/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules \
  TIMELINE_MAIN95_PROMPT_PRIVATE13_READY=/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/READY \
  TIMELINE_MAIN95_PROMPT_PRIVATE13_LEASE=/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/LEASE \
  TIMELINE_CURRENT013_AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
  TIMELINE_CURRENT013_RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
  TIMELINE_CURRENT013_PUBLIC_SOURCE_SHA256=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738 \
  TMPDIR=/tmp/tl-main95-settings-prompt-current/short \
  HOME=/tmp/tl-main95-settings-prompt-current/home \
  XDG_CACHE_HOME=/tmp/tl-main95-settings-prompt-current/xdg \
  PWTEST_CACHE_DIR=/tmp/tl-main95-settings-prompt-current/pw-cache \
  VITE_CACHE_DIR=/tmp/tl-main95-settings-prompt-current/vite-cache \
  PLAYWRIGHT_OUTPUT_DIR=/tmp/tl-main95-settings-prompt-current/output \
  NODE_OPTIONS=--max-old-space-size=4096 \
  /opt/node20/bin/node scripts/testing/main95-prompt-settings-integration.mjs
```

The shell wrapper must create each listed private directory with mode `0700`, verify `realpath "$TMPDIR" = "$TMPDIR"`, and reject any `XDG_*`/cache path of length 100 or more. It must preflight exact source HEAD/tree, clean source checkouts, runtime locks/metadata, the all-77 graph, browser executable/hash/version, unset credential/direct-dist overrides, and the final runner SHA before invoking Node. Retain stdout/stderr, discovery output, source pre/post checks, and the final postflight record.

## Evidence recorded here

- `node --check scripts/testing/main95-prompt-settings-integration.mjs` — PASS.
- `node --test scripts/testing/main95-prompt-settings-integration.test.mjs` — PASS, 1/1 file.
- Targeted Vitest using private cache paths — PASS, 3 files / 37 tests.
- Private-overlay Playwright discovery with the exact prompt grep — PASS: `shot-name-command.spec.ts:431:1`, `Total: 1 test in 1 file`; zero failures. The App `node_modules` link was restored afterward.
- Pin probes — PASS for Agent6ef, vendor091, Runtime95, Composition 77/77, and Chromium hash/version.
- Local shell had `NODE_PATH` set before the probe; the packet explicitly unsets it, along with `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST`.
- Local `/opt/node20/bin/node` reports `v20.20.0`; this is not claimed as the requested `20.19.4`. Central preflight must verify that exact Node requirement before actual execution.

The prompt browser journey, Runtime retry/restart, raw readback, inverse, and zero-legacy behavior remain **unverified actual evidence** until the central service runs the one selected case. Do not report this packet as a product PASS.
