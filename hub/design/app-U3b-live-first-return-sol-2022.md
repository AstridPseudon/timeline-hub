# U3b live refresh first return — qualification PASS; integration HOLD

Worker `app-U3b-live-first-return-sol-2022`, assigned App worktree only. Node **v22.22.0**, Vitest **4.1.5** from the read-only shared install. No full suite, browser, HTTP/seed/preflight/build/benchmark, central duplicate, Git mutation or integration request. Source qualification only; P1/P2/P3/freeze remain HOLD.

- Final **285/285 core tests**: all original 282 unchanged, including both prior failures now green, plus three appended mounted outbox cases.
- **380/380 focused upstream/chat tests**, 22 files; **39/39 Node tests**.
- App, Node and root TypeScript checks: **exit0** under the requested flock/4096 MB settings.
- **68 changed existing/new TS/TSX paths** against `e2e75b38`, lint **exit0, zero warnings**; `git diff --check` and frozen/scope audits pass.
- List-only selected journeys: **P1=2, P3=1, P2=8**. No body or browser credit.

## Changes and production-path reasoning

Only eleven worktree paths differ from task base `7978ed829e8c12ca4058676f43208a882e381966`:

1. `hooks/useTimelineCommit.ts`, `lib/timeline-mutation-engine.ts`, `lib/timeline-data.ts`, `lib/serialize.ts`: distinguish the pure legacy row projector from edits carrying an authored basis. Mounted row edits and the pure preview/apply path supply prior metadata plus explicit metadata updates. Unchanged labels restore the raw own value/presence, including a label equal to the asset filename; explicit label updates stay explicit. Resolved-config serialization uses the existing authored serializer directly, deleting the filename-equality stripping pass. Non-enumerable derived display labels distinguish copied display views from enumerable explicit label writes. No name-equality rule authorizes removing raw fields.
2. Exact `65c1771` restorations: `components/AgentChat/TourChatPanel.tsx`, its required missing `NewChatMenu.tsx`, and that menu's exact upstream test. TourChatPanel SHA256 is `b9e61ca2f0c5db8259474cdd5247a0f336a87551f528758f0d4172eb6e78e274`.
3. Necessary existing transitive components `AgentChatMenu.tsx`, `NewChatModels.tsx`, `ChatUpdateNeeded.tsx`: adapt the restored menu and tour to retained callers. The retained menu still starts chats on model selection; the new menu chooses a model and offers its separate start button. Existing introduction/copy and thinking-level layout remain for the retained menu. All 66 original menu tests, 57 parent-chat tests, 19 model-line tests and 53 exact upstream new-menu tests pass without assertion changes. Wholesale upstream replacement would have removed retained behavior, so compatibility stays at these named dependencies.
4. `hooks/useTimelineCommit.test.tsx`: append-only three-case regression, for absent label, filename-equal label and asset-ID-equal raw label. It mounts the real commit hook, production handoff and persisted outbox. Row and resolved-config edits preserve the authored raw document and emit no label changes; explicit filename-equal writes persist; explicit row clears are checked on the local materialized config. The existing handoff treats omitted fields as partial views, so these tests do **not** claim new wire-level label-clear support. Prepared-media additions also preserve the raw parent label and add no label patch.

The restored `TourChatPanel` is exercised by the existing real `BrowserTourEditor.integration.test.tsx` (bundled world admission and all three stages), not a detached substitute. Its old upstream test hosts the old AgentChatPanel tour switch, which is absent in this retained App; it was not restored. No cloud product, development extension, M5 or writer was restored.

A scope clarification was raised after observing that `commands/media.ts` and `commands/runner.ts` use the pure row projector. Further tracing and mounted outbox coverage resolved it **without extending scope**: those callers can omit a label from a normalized display config, while the existing handoff preserves omitted authored parent fields. The scratch counterexample initially asserted display-config equality and failed; the actual persisted-document regression passes. No command/media/capture/outbox/provider/client/undo/door source was edited, and no pending approval is needed for this result.

## Exact verification commands

Commands run from `/home/user/work/wt/app-U3b-live-first-return-sol-2022`. `$TMPDIR=/tmp/w-cf75147352`. Owned `vitest-preload.cjs` contains:

```js
globalThis.__dirname = '/home/user/work/wt/app-U3b-live-first-return-sol-2022/config/testing';
```

Shared `node_modules` resolves to `/home/user/work/app/node_modules`; no installation or shared cache writes. Every Vitest invocation used runner config loading and `--no-cache`.

```sh
TSX_DISABLE_CACHE=1 node --require "$TMPDIR/vitest-preload.cjs" node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useTimelinePersistence.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useTimelineCommit.test.tsx src/tools/video-editor/lib/timeline-data.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/clipDisplayNames.test.ts
```

Final **exit0, 12 files, 285 passed**, 26.32s (`logs/core-tests-final.log`). Initial combined verification had **284 pass/1 fail** in unchanged `useTimelineSave.test.tsx`, mounted Undo `invalid`, `history.canUndo` observed true at line588. No source/test change was made to that file. The same 12-file run subsequently passed 285/285 in 17.93s; the final run after appending prepared-media assertions again passed 285/285. Earlier checks on the two original failures and serializer passed 70/70. Existing React `act` warnings remain; the initial Undo timing failure is recorded, not erased or waived.

```sh
TSX_DISABLE_CACHE=1 node --require "$TMPDIR/vitest-preload.cjs" node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/app/Layout.test.tsx src/app/hooks/useOnboardingFlow.test.ts src/app/main.bootstrap-order.test.tsx src/app/main.runtime-origin.test.tsx src/app/main.welcome.test.tsx src/app/onboarding/BrowserTourEditor.integration.test.tsx src/app/onboarding/StarterProjectHandoff.test.tsx src/app/onboarding/WelcomeFlow.test.tsx src/app/onboarding/prepareStarterProject.test.ts src/app/onboarding/welcomeProgress.test.ts src/integrations/runtime/client.test.ts src/shared/components/RuntimeConnection/RuntimeConnectionPanel.test.tsx src/tools/video-editor/tour/runner/editorTourGate.test.tsx src/tools/video-editor/tour/runner/tourBeats.test.ts src/tools/video-editor/tour/runner/tourFlag.test.ts src/tools/video-editor/tour/runner/useEditorTourHost.test.tsx src/tools/video-editor/tour/timeline/EditorTourScenePresentation.test.tsx src/tools/video-editor/tour/timeline/EditorTourTimelineDriver.test.tsx src/tools/video-editor/tour/timeline/useTourMediaWarmup.test.ts src/tools/video-editor/components/AgentChat/NewChatMenu.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMenu.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChatModelLine.test.tsx
```

**Exit0, 380 passed, 22 collected files**, 123.63s (`logs/upstream-tests.log`). The retired `useOnboardingFlow.test.ts` path was an extra filter and is absent; no test is claimed for that deleted file. Early dependency checks exposed four new-menu failures (selector classes/text and introduction copy); the named transitive adapters fixed them while retaining all original expectations.

```sh
TSX_DISABLE_CACHE=1 node --import tsx --test --test-reporter=spec tests/e2e/local/p1-diagnostic-safety.test.ts tests/e2e/local/support/public-trim-preflight.test.ts tests/e2e/local/support/playwrightSkipGuard.test.ts tests/e2e/local/support/selected-param-credential.test.ts tests/e2e/local/support/timeline-scope.test.ts tests/e2e/local/support/auto-real-proxy-observation.test.mjs tests/e2e/local/support/native-transition-clear.contract.test.mjs
```

**Exit0, 39 passed, zero failed/cancelled/skipped/todo**, including the eight strict public-trim controls (`logs/node-targeted.log`).

```sh
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.node.json --pretty false
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.json --pretty false
```

All **exit0**; logs `tsc-app-final.log`, `tsc-node.log`, `tsc-root.log` are empty. Initial App types revealed the missing NewChatMenu and incompatible retained model/menu props; final types pass with the exact restored TourChatPanel.

Final lint executed the following Python subprocess; `lint-files.txt` contains all 68 ordered paths, selected from existing TS/TSX files changed against `e2e75b38` plus new TS/TSX files:

```python
paths = Path('/tmp/w-cf75147352/lint-files.txt').read_text().splitlines()
subprocess.run(['node', 'node_modules/eslint/bin/eslint.js', '--no-cache',
                '--report-unused-disable-directives', '--max-warnings', '0', *paths])
```

**Exit0, zero warnings**, final log empty. `git diff --check`: **exit0**.

```sh
PLAYWRIGHT_OUTPUT_DIR="$TMPDIR/playwright-output" TSX_DISABLE_CACHE=1 node node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.p1-chain.spec.ts
PLAYWRIGHT_OUTPUT_DIR="$TMPDIR/playwright-output" TSX_DISABLE_CACHE=1 node node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.spec.ts --grep 'M2 real gate 5 \(M1 real mounted path\)'
PLAYWRIGHT_OUTPUT_DIR="$TMPDIR/playwright-output" TSX_DISABLE_CACHE=1 node node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.p2-tour.spec.ts tests/e2e/local/three-products.p2-elements-assets.spec.ts tests/e2e/local/three-products.p2-popup.spec.ts
```

All **exit0**, selected totals **2/1/8**. Initial unfiltered P3 discovery listed 15; a first anchored title filter found zero because Playwright includes the filename prefix. The corrected unanchored exact gate selector lists one. Only discovery ran; global setup, bodies and browsers did not.

## Frozen source and ancestry audit

`python "$TMPDIR/audit.py"` and `git diff --check` **exit0**; assertions and hashes in `logs/source-audit-final.log`:

- Task base tree is exact `ce3cd515c9b2e5a54b6b148a1c4760a785f23c20`; its actual parents are **e2e75b38e29ef0f5f628d0fdab988d701205b758**, **65c1771b78ab972295d4bea91c93970e5bb65e74**, in that order. Both `git merge-base --is-ancestor <parent> HEAD` checks pass before harness commit. No future commit ID/tree is claimed.
- Runtime lock blob `2800842c772228b508ca1b7a53d799bc22df29b9` unchanged, producer pin **34eac0041b0891e9011966b39bcbd26053fde5bc**, producer stamp **sha256:d5f98db3213e91d96d4a7f5b184e17bf5268357b37dc06eaa5b568c4b788a572**. Independently hashed all **78 producer artifacts** against its manifest and verified all **13 App mappings** match pinned producer bytes and lock hashes. Edit-command schema digest remains **d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d**.
- Composition archive SHA256 **819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234**, exact SHA512 SRI matches package-lock. `package.json`, `package-lock.json`, runtime lock and entire vendor directory unchanged. No b221/ba858/popup imports or pins changed.
- Full generated contract/reply/request types, client, mounted save, handoff, outbox/session, provider, commands/capture, data and entire e2e directory remain task-base bytes. This keeps the full v2 request/reply/receipt transport, history/undo and door sources intact.
- All original mounted test bytes are an exact prefix of the appended file; upstream `timeline-data.test.ts` remains exact65c. No passing expectation was rewritten or weakened; no tests skipped, disabled or marked expected-failure.
- Original P1 source blob **feb26946d62db9a4a02dab8dca1c0dc7320f2681**, gate5 whole source **37caf28577d42fbe98afd2320dffa3c72e6e74b1**, diagnostic source/test **a49f6bfb20c21b01bc709db79d3fa3cd47b216c3 / 3b72ee8fff59b6d7e9919aa936f0ac3e6d9a4ff5**, public-trim source/test **51dc979958f140dfbb649e799363c5e0a747a2c5 / bdd3cda7e117d794f264b6c42d0b31e82fe4d573** unchanged.
- Central quick-descriptor result **1772** reused, **8 pass/exit0**, because source/test remain exact **521baa4383de5b743afc40f562d296d15ea27ff7 / 458c2fd469fbf25c26067d355e64e0bd977ba6d1**. Read its existing summary only; did not rerun the service/socket tests.

## Disposition

No blocker remains for this scoped source qualification. No label contract change or integration approval was inferred. Wire-level explicit label-clear support remains outside this change; omission remains a partial view under the retained handoff. Scratch experiments distinguish display state from authored persisted state and are not presented as end-to-end failures.

Recommend independent review of the final tree, then let the harness commit with the supplied message. Manager must run `git merge-base --is-ancestor 65c1771b78ab972295d4bea91c93970e5bb65e74 <final-worker-commit>` and verify the original e2e75 ancestry after the harness commit. Keep integration HOLD until P1/P2/P3/freeze disposition. No request to merge/integrate is made.

Reports/logs are small; all fixtures/scratch stayed in harness-cleaned TMPDIR. Shared dependencies remained read-only. Commit message and DONE written only after final qualification.
