# ORCHREPORT — final theme and scene consistency

READY for source review on `tl/vw-m3-final-theme-render-consistency`, base `5d26afc5a6803e3549a76fb5347f6d71758fd236`. Exactly two small product fixes; no blockers or deviation from FINAL 06:18/06:20 implicit-default decision.

## Exact source diff

Four changed files, 17 insertions / 3 deletions:

- `/home/user/work/wt/vw-m3-final-theme-render-consistency/typescript/src/TimelineComposition.tsx:328`: replace root background fallback `'black'` with `DEFAULT_THEME.visual.color.bg`. Explicit resolved film themes retain precedence.
- `/home/user/work/wt/vw-m3-final-theme-render-consistency/typescript/src/scene-evaluation.ts:240`: apply reviewed own-property role lookup, followed by the existing nullish fallback (`plate` -> `picture`, every other track -> `content`). Source and ordinary scene test match the reviewed proposal at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-public-scene-role-own-keys-proposal.patch`.
- `/home/user/work/wt/vw-m3-final-theme-render-consistency/typescript/tests/theme.test.ts:54`: assert the implicit default's root canvas color in ordinary SSR; strengthen existing explicit nonblack assertion to require the root element. Existing complete default equality, explicit provider/evaluator/effect/hook checks and no-mutation assertions retained.
- `/home/user/work/wt/vw-m3-final-theme-render-consistency/typescript/tests/scene-evaluation.test.ts:45`: integrate the ordinary regression proving own JSON `__proto__` override and fallback for valid IDs `__proto__`, `constructor`, `toString`.

Exact patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency.patch`.
Absolute source file list: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-FILELIST.txt`.

No changes to `ThemeContext.tsx`, public exports, evaluation/duration math, trim/rate helpers, equality helper, package.json or lockfile. Git diff is restricted to the four files above. Complete Agent-export default remains navy #050814 / Arial / cyan; no ID restrictions, new dependency/schema/DTO/registration/refactor or copied styles. No tests skipped, disabled, deleted, marked failing or weakened.

## Exact commands and results

Working directory for all commands: `/home/user/work/wt/vw-m3-final-theme-render-consistency`. Dependencies reused through a temporary `node_modules` symlink to `/home/user/work/composition/node_modules`; no install/network. Compiled tests run directly with Node to retain individual assertions and diagnostics.

1. `npm run build:test` — PASS, exit 0, before source fixes and after final source fixes. Final log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-build-test.log`.
2. Before source fixes, after adding assertions:
   - `node --import ./typescript/tests/register-extensionless.mjs typescript/test-dist/tests/theme.test.js` — expected RED, exit 1: 2 pass / 1 fail. Ordinary implicit root assertion observes `background-color:black`; both explicit nonblack SSR cases pass. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-theme-red.log`.
   - `node --import ./typescript/tests/register-extensionless.mjs typescript/test-dist/tests/scene-evaluation.test.js` — expected RED, exit 1: 5 pass / 1 fail. Missing own `__proto__` role returns inherited object instead of `content`. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-scene-evaluation-red.log`.
3. After final source fixes, **40 targeted tests passed, 0 failed / skipped / todo**:

| Exact command | Result | Absolute log |
| --- | --- | --- |
| `node --import ./typescript/tests/register-extensionless.mjs typescript/test-dist/tests/theme.test.js` | 3 PASS | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-theme-green.log` |
| `node --import ./typescript/tests/register-extensionless.mjs typescript/test-dist/tests/scene-evaluation.test.js` | 6 PASS | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-scene-evaluation-green.log` |
| `node --import ./typescript/tests/register-extensionless.mjs typescript/test-dist/tests/scene-diagnostics.test.js` | 15 PASS | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-scene-diagnostics-green.log` |
| `node --import ./typescript/tests/register-extensionless.mjs typescript/test-dist/tests/evaluation.test.js` | 9 PASS | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-evaluation-green.log` |
| `node --import ./typescript/tests/register-extensionless.mjs typescript/test-dist/tests/registries.test.js` | 7 PASS | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-registries-green.log` |

4. `npm run build` — PASS, exit 0: registry freshness, TypeScript declarations and actual esbuild output. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-build.log`.
5. `node scripts/check-agent-default-theme.mjs /home/user/work/agent /home/user/work/venv-agent/bin/python` — PASS, exit 0: actual built public root/theme-api identity and deep equality of the entire default to real Agent builtin, schema constant and validated document. Qualified module: `/home/user/work/agent/astrid/core/theme/_schema.py`, SHA256 `d15074cb725289d336d26cfd806c6056f4da00ee9e6680adc114d5aef68d6052`. Observed Agent HEAD `ef6eec5572c5c0def7ca8a22c14caa12f24f0b82`. Complete equality result: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-agent-equality.json`.
6. `git diff --check` — PASS, exit 0.

## Exact frame expectations

- Ordinary `TimelineComposition` SSR at frame **24**, 1920x1080 / 30 fps, omitted `props.theme`: outermost canvas background **#050814**. Existing title remains #FAFAFA / Arial / 32px / weight 400 / line-height 1.2. This root expectation was RED before and GREEN after.
- Same SSR frame **24**, explicit full resolved theme and caller-resolved nested override without optional mono: outermost canvas background **#234567**, title #123456 / Film Heading / 51px / weight 300 / line-height 1.7. Entire explicit themes remain unchanged through provider, evaluator, effect props and hook. Both cases GREEN before and after.
- Scene query frame **0**, own JSON role `{"__proto__":"background"}`: role exactly **background**. Empty ordinary role map with clip ID `__proto__`, `constructor`, or `toString`: role exactly string **content** on visual track `video`. Valid IDs remain admitted. `plate` -> `picture` fallback expression is unchanged; the new ordinary regression exercises `video` -> `content`.
- Adjacent existing rational occurrence test remains GREEN: 24000/1001 fps, 1501ms occurrence cap **36**; incoming layer present at frame **35**, no layers at frame **36** with compiled incoming transitions, and native omitted-policy path still has incoming layer at frame **36**. No timing/geometry/audio math changed.

## Limits, decisions and next steps

- Only implementation choice beyond the settled patch: anchor both canvas assertions to the outermost div so nested element backgrounds cannot satisfy them. This strengthens explicit-theme preservation evidence.
- No full suite requested or run by this worker. Prior candidate's 68-pass full is historical evidence only; final source awaits the manager's ONE post-merge integration full.
- No browser, pixel/video/audio render, sockets/live hosts, install or network. SSR establishes markup behavior, not end-to-end pixel parity or consumer adoption.
- Immutable artifact hold preserved: no npm pack/version change/archive/tag/publish/integration merge. Existing old11 / SHA256 dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601 untouched. Orchestrator chooses a distinct new11 filename or version before later packaging.
- Reports/logs/patches only under absolute ORCH paths. Local `dist`, `typescript/test-dist` and temporary dependency symlink removed after checks. Product diff contains only the four reviewed source/test files.
- Next: review and integrate this small source branch through the orchestrator, run the single planned final integration full, then choose immutable artifact identity and qualify coordinated Agent/App adoption. Owner-film note stays implicit App preview black/Georgia/white -> navy/Arial/cyan; existing export default and explicit film themes preserved.

Report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-final-theme-render-consistency/ORCHREPORT.md`.
Flat design copy: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-final-theme-render-consistency-ORCHREPORT.md`.
