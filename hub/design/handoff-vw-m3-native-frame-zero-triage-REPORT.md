# Frame-zero diagnosis and bounded capture fix

Base: App `4f872ca47` (`tl/vw-m3-native-frame-combined-candidate`). PLAN read first. Completed central `1020051823-16742` remains **2 PASS / 2 FAIL**, diagnostic only. Neither the full positive comparison nor the planted negative qualified. No new browser/render/socket/service/full/install/network run or central request.

**Proved primary cause: the captured Player is obscured by the Rendered film modal and its backdrop.** The original PNG visibly contains the modal, controls and Download button. Independently decoding the original admitted MP4 and calling the unchanged repository comparator reproduces exactly **2,073,545/2,073,600 outside 2/255, max203, mean72.252703**; the negative case fails its *baseline*, identically counted, mean72.185947, before any magenta patch. These are actual retained files, not replacement drawings.

The expanded retained DOM at screenshot locator resolution `before@call@1058` contains the native Player, image opacity1/object-fit:contain, black composition ground, open result popup (`z-index:110022`) and black/80 backdrop (`z-index:110020`). The trace returns frame0/paused, scale1, final frame0; viewport2000x1200 and the existing DPR1 assertion passed. The native-host stylesheet does not escape ancestor stacking contexts. A locator screenshot includes overlapping page content; native size/readiness does not prove unobscured pixels. Exact computed occlusion/bounding-box results and the full runtime React/serialized export props were not retained, so no invented values are supplied. `trace-evidence.json` expands Playwright subtree references and retains only whitelisted DOM attributes and returned values. Independent capture audit agrees: `handoff-vw-m3-native-capture-zero-audit-REPORT.md`.

Source/asset/order checks: frame0 has the single pinned still on V1, opaque, with no fade/transition/theme override; its hold ends at frame120, where video starts, ending165 exclusive. Audio is on A1. Actual DOM image URL binds the still digest `371fa835ba9c64b94118593bec78b7ae6295c44f578c1373f7efdbd06857f9c0`; both cases use this same immutable still. The normal task provenance names `TimelineComposition` and the existing donor Root; existing source-result postflight passed. No replacement evaluator, injected props, fixture/media rewrite, guessed seek time, color normalization, crop, shift, padding or threshold change.

**Applied smallest owned fix:** eight lines in `tests/e2e/timeline/viewing-parity/frames.ts` close the exact named result dialog through its normal Close button, wait for detached popup/backdrop, then execute the existing actual Player-ref seek/readiness/native screenshot/decode. `frames.test.ts` tests this public function up to its existing ref-inspection boundary; it does not emulate pixels or a decoder. The original function failed all four new assertions; fixed function passes4/4, including close failure and lingering-backdrop refusal. All original behavior expectations remain intact. No product files changed.

**Separate residual, not concealed:** the original unobstructed readiness PNG is from a *different case* and is never substituted for the positive capture. Unmodified cross-case comparison to positive export frame0 still yields526658/2073600 outside2, max20, mean3.033262. Sidebands are App RGB[0,0,0] versus export[5,6,20]. This establishes a background divergence, not parity after the capture fix. Source-derived export prop chain: retained provenance `active_theme={id:banodoco-default,path:null}` -> rendering/shared/rendering_backend/__init__.py:104 `builtin_theme()` -> renderer/remotion/run.py:1103-1110 explicit `props.theme` -> donor Root.tsx:84 -> installed Composition8 index.js:616 `props.theme.visual.color.bg`. Agent core/theme/_schema.py:177 defines `#050814`; App TimelineRenderer.tsx:1727 and installed package DEFAULT_THEME use black. Core is outside this task's write ownership. `UNAPPLIED-agent-default-background.patch` changes only that Agent-core background field to black as a concrete owner-review candidate, **not applied, not behavior-tested, not approved as a theme policy change**. `git apply --check` passes against the leased b70 Agent. Full default theme typography/accent/size also differ; the one-field proposal does not unify those or promise a green comparator.

Validation (all commands from assigned worktree; `NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node`; each CPU invocation prefixed with `sh $ORCH/workers/vw-m3-native-frame-zero-triage/cpu-guard.sh`, where `ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`). Both absolute QUIET markers were absent before these batches.

```sh
$NODE --import tsx tests/e2e/timeline/viewing-parity/frames.test.ts
# Original frames.ts: exit1, 4 FAIL (frames-red.log).
# Fixed frames.ts: exit0, 4 PASS (frames-green.log).
$NODE --import tsx tests/e2e/timeline/viewing-parity/canvas.test.ts       # exit0, 8 PASS
$NODE --import tsx tests/e2e/timeline/viewing-parity/compare.test.ts      # exit0, 3 PASS
$NODE --import tsx tests/e2e/timeline/viewing-parity/diagnostics.test.ts  # exit0, 141 PASS
$NODE node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts src/tools/video-editor/components/TimelineRenderControls.test.tsx --maxWorkers=1
# exit0, 9 PASS. Total direct final cases:165 PASS.
$NODE --import tsx --test tests/e2e/timeline/viewing-parity/frames.test.ts tests/e2e/timeline/viewing-parity/canvas.test.ts tests/e2e/timeline/viewing-parity/compare.test.ts tests/e2e/timeline/viewing-parity/diagnostics.test.ts
# exit0, 4 file-level passes. Repeated directly above because this runner hid individual case counts.
$NODE node_modules/eslint/bin/eslint.js tests/e2e/timeline/viewing-parity/frames.ts tests/e2e/timeline/viewing-parity/frames.test.ts --max-warnings 0
# exit0, empty lint.log.
$NODE node_modules/typescript/bin/tsc --project tests/e2e/timeline/viewing-parity/tsconfig.json --noEmit
# exit2: only existing local/support/harness.ts:630 TS2352 clips/never[].
cmp $ORCH/design/handoff-vw-m3-native-frame-zero-triage-typecheck.log $ORCH/workers/vw-m3-native-frame-combined-candidate/typecheck.log
# exit0: byte-identical baseline diagnostic; no changed-file error.
git diff --check
# exit0.
git apply --reverse --check $ORCH/design/handoff-vw-m3-native-frame-zero-triage-capture-fix.patch
# exit0; includes both changed/new files.
git -C /home/user/work/wt/vw-m3-host-agent-source apply --check $ORCH/design/handoff-vw-m3-native-frame-zero-triage-UNAPPLIED-agent-default-background.patch
# exit0; check only, no Agent write.
```

Offline evidence commands, exit0 (no rendering):

```sh
ffmpeg -v error -threads 1 -i /tmp/viewing-native-frame-parity-2EZi8v/player-export-normal-profi-1fbe1-al-CPU-Remotion-task-output-native-codec-chrome155/viewing-parity/final-export.mp4 -map 0:v:0 -an -frames:v 1 -threads 1 $ORCH/design/handoff-vw-m3-native-frame-zero-triage-export-frame000.png
$NODE --import /home/user/work/app/node_modules/tsx/dist/loader.mjs $ORCH/workers/vw-m3-native-frame-zero-triage/analyse.mts
python $ORCH/workers/vw-m3-native-frame-zero-triage/trace-evidence.py
```

All handoff artifacts are FLAT `design/handoff-vw-m3-native-frame-zero-triage-*`: applied capture patch, UNAPPLIED owner patch, analysis sources, exact numeric/hash evidence, filtered trace evidence, raw original positive PNG/MP4, raw cross-case readiness PNG (explicitly labelled), derived decode, red/green and targeted logs. Original retained files remain unchanged. No build/temp output remains in the worktree; no git/ref/integration/other-worker writes or commits.

Next: manager reviews the bounded capture patch and routes the default-theme field proposal to the Agent owner. A **new explicit manager grant and frozen central candidate** are required for any actual rerun. Keep the existing four cases,2/.001 and all strict diagnostics; the prior ERR_ABORTED result-video failure remains unresolved and unwaived. Retain full positive baseline before running the existing negative control. Do not describe this triage completion or the readiness/cross-case observations as partial gate qualification, PCM proof, or M3 completion.
