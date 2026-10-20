# Final bounded handoff: `vw-m3-main-parity-final-handoff`

Decision: **APPROVE the exact test-only branch `701491b76f2f0af9cfcebacab74fc76adf220430` for App-owner handoff.** This is not an actual frame/audio parity qualification.

## Tree and scope

- Ancestor: `667498cc49b4ec2b1ccd3a515eb87311c5126c93`.
- Port: `877b7f33eb5fc8afe035d984d976683702819101`.
- Type-only follow-up: `701491b76f2f0af9cfcebacab74fc76adf220430`.
- Current CORS reference: `7bb885b638838588a0dff81b64b7c34960ac07f3`; its only source-tree delta against this branch is the pre-existing `mediaCrossOrigin.ts` and test pair. The parity branch has no `src`, `vendor`, manifest, lockfile, render, download, admission, provider, or pin changes relative to `667498cc`.
- `git diff --check 667498cc 701491b`: PASS.
- Exact patch: [handoff-vw-m3-main-parity-final-handoff.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-parity-final-handoff.patch).
- Exact file list: [handoff-vw-m3-main-parity-final-handoff.filelist](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-parity-final-handoff.filelist).

The only modified tracked file is `tests/e2e/local/support/harness.ts`; the other 31 paths are test/config additions. The type-only `TimelineClip[]` annotations emit identical JavaScript before/after (`transpiled_equal=true`), so runtime behavior is unchanged. No `320784f828a4` product helper changes are present; `src/tools/video-editor` and `src/integrations/runtime` are byte-unchanged from the ancestor.

The port retains MAIN's actual `Rendered film` dialog `Download` button, managed-object URL, filename and explicit blob fallback path. The neighboring App render-control/useRenderState tests pass.

The guard contract remains explicit: original 640x360 is the default; native 1920x1080 uses its separate config and 2000x1200 viewport; Chrome `155.0.8059.84` is named separately; RGB channel threshold is `2` and outside fraction is `.001`; the Composition manifest remains `77` files; each consumer has six peer pins; source tuple, immutable artifacts, finally-postflight, fresh grant, flock and absent `QUIET.md` remain fail-closed requirements.

## Checks run on this exact tree

- `/tmp/vw-m3-agent-gate-node20.19.4/bin/node --require <no-sockets.cjs> --import tsx --test tests/e2e/timeline/viewing-parity/*.test.ts`: **11/11 files, 0 failures, 0 skipped; PASS**. Includes offline fixture/media/decoder plumbing; no browser, Runtime, HTTP, or local socket.
- `node_modules/typescript/bin/tsc.js --noEmit ... tests/e2e/local/support/harness.ts tests/e2e/timeline/viewing-parity/*.ts tests/e2e/timeline/player-export*spec.ts playwright.viewing-parity*.ts`: **PASS**.
- `node_modules/eslint/bin/eslint.js ... --report-unused-disable-directives --max-warnings 0 --no-cache`: **PASS**.
- `node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/components/TimelineRenderControls.test.tsx src/tools/video-editor/hooks/useRenderState.test.tsx`: **2 files, 82 tests, PASS**.
- Playwright discovery only, with the socket-deny preload and no browser launch:
  - `playwright test --list --config playwright.viewing-parity.config.ts`: **4 cases listed**.
  - `playwright test --list --config playwright.viewing-parity.normal-profile-native1920.config.ts`: **4 cases listed**.
- TypeScript transpile comparison of `harness.ts` at `877b7f33` versus `701491b`: before/after emitted SHA-256 both `691abf4346ee8fadc3f69c22b0b555f24a7516dae410bc9928631a0c9148e02e`; **identical**.

## Limits

No central/full suite, browser, local listener, Runtime, HTTP, product render, capture, source tuple, fresh grant, flock-held run, or audio/pixel parity claim was made. The safe final tuple remains pending owner-matched App/Agent/Runtime/Composition pins and a fresh manager-controlled launch. No product edits were made.
