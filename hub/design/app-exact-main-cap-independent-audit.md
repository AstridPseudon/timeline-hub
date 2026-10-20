# Exact MAIN cap: independent read-only audit

**Confirmed counterexample, audit complete.** The unchanged held App test fails on the exact captured single-occurrence closure: required hold4 / frame105 opacity0.5 / excluded frame120 becomes hold5 / opacity1 / a layer at120. All39 original neighboring projection tests pass. No product/test edits, new field, operation, policy, pin change or KEEP request. The owner11:59 MAIN golden remains accepted; escalation12:19 is already filed. This finding corrects the assumption that the current App path already matches that golden for this exact closure; it does not reverse the decision.

## Sources and minimal counterexample

- Read PLAN, the11:59 decision in `managers/app/INBOX.md:984`, `app-main-cap-half-golden.md`, `viewing-main-image-cap-actual-reference.md`, the source-vector READY/replay/closure artifacts, and the existing Agent visual-contract sources. Historical renderConfig proposals stay withdrawn.
- Held App HEAD `a26c7ad5e9eb41185dd68a553b08ff338144fd73` (parent `cee35da4b1ed653db50dd9d5c26693fab00f04ad`), normal013/public12. Tests use read-only `/tmp/app-coherent-deps12/node_modules`, Composition0.0.12, private cache and one worker.
- Exact raw closure: `design/handoff-vw-m3-main-image-cap-source-vector-raw-closure.json`, byte-equal to App `src/tools/video-editor/data/mainImageCap.fixture.json`, SHA256 `ad3d0ad35876665489080703c2323a8840c9187428dbe28a913e8ab4ada53f04`. One image at0, hold5, fade_out1; one occurrence at0, duration4000ms; numeric30fps. No next occurrence was added.
- Original MAIN Agent/render source `a411628f8fd6129f9c58c332019b56769d997384`, archived by the source-vector producer; original locked Composition0.0.6. The accepted physical reference is the existing central three-still run named in `viewing-main-image-cap-actual-reference.md`: metadata120 frames, f90 RGB240, f105 RGB122/124/130 over background5/8/20, median source-over fraction0.5. No pixels were rerendered here, and PNG alpha is not layer opacity.

| Consumer, same exact closure | Occurrence/render bound | Clip hold | f105 opacity | Half-open end |
| --- | --- | --- | --- | --- |
| Original MAIN managed resolver → projector → materializer → serializer, replayed here | 4000ms | 4 | 0.5 in accepted MAIN capture | 120 |
| Current Agent native opener → candidate compiler, pure probe | placement/publication retain4000ms | authored child remains5 | not a pixel/evaluator claim | not a render interval |
| Current Agent existing render projector, pure probe | output extent4000ms | 4 | 0.5 when bounded clip is passed to public12 | 120 via Agent frame helper |
| Held App actual loader → adapter → canonical resolver → public12 | effective bound5000ms | 5 | 1 via actual App opacity helper | layer still exists at120 |

Original MAIN pure replay produced **all seven outputs byte-for-byte equal** to the frozen source-vector artifacts: projected config, managed registry, materialized timeline, serialized timeline, template props, static-analog props and trace. This traverses the original existing helpers, not a reconstructed cap. Static image URL binding remains the explicitly labelled executable analog; no live Runtime or asset server was started.

## Where the cap survives, and where it is replaced

1. App `src/integrations/runtime/dataProvider.ts:598` reads the immutable closure through `loadRuntimeShotCompositionAtHead`; `runtimeGraphToContract` at2028, specifically2088–2098, copies `duration_ms:4000`. `shotCompositionAdapter.ts:224` prepares it as `durationMs:4000`. The loader does not lose it.
2. `canonicalCompositionState.ts:64` selects the ordinary default `projectCanonicalComposition`. In `shotCompositionProjection.ts:505–513`, `timelineContentExtentMs` sees5000ms, and `timelineOccurrenceEffectiveDurationMs` replaces the occurrence duration. `shotCompositionTiming.ts:135–143` considers content and the next same-lane start only. With no next occurrence, it returns5000; stored4000 is not consulted. `effectiveOccurrence = {...occurrence, durationMs: effectiveDurationMs}` is the exact substitution seam.
3. `projectClip` at427–434 writes `canonicalTiming.durationMs:5000` and `occurrenceDurationMs:5000`; its existing default clamp at440–450 then has no4s boundary to apply. The returned clip hold is5. The immutable source graph itself is preserved.
4. App `compositions/playerEvaluation.ts:20–29,58–60,80–87` supplies that selected clip/config to the public compiler and scene evaluator. Public12 `dist/chunk-DMRW7SC3.js:571–590` already reads the existing `canonicalTiming` occurrence extent for its frame cap. It cannot recover4000 after being supplied5000. An end cap alone also does not shorten the source opacity clock: unchanged public `clipOpacity` gives0.5 for the existing bounded MAIN hold4 input and1 for the legitimate raw hold5 unit at105. The raw unit is a different input, not contrary evidence to MAIN.
5. Agent `astrid/core/timeline/shot_composition_projection.py:272–290,308–330,593–610,652–660` already consumes the stored occurrence window and emits the bounded ordinary clip hold4 plus `outputs[].duration_ms:4000`. That projector is byte-identical between original MAIN and accessible Agent HEAD `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`. `packs/rendering/actions/render/managed_timeline.py:893,963,1123–1138` and `sdk/timeline/commit.py:739` use this same projector. No second projector was introduced.

**An existing bounded render input already carries the correct answer:** the Agent projected ordinary config has hold4, and its output extent is4000ms. The App prepared occurrence also retains4000 before substitution. The accessible native `open_authoring_bundle`/`compile_authoring_candidate` probe preserves4000 through publication without altering the closure. Separately, `sdk/timeline/compiler.py:114` yields the authored child interval[0,5), frames0–150; this is not the bounded render projection. Conflating that intermediate interval with final render input would recreate the mismatch.

The original editor positive is materially different. `shotComposition.fixture.json:146–147` stores occ-1 duration2000 but starts occ-2 at4000. `shotCompositionProjection.test.ts:481–520` substitutes a5s child, requires default hold4 and explicit local/unclamped hold5, and checks occurrenceDurationMs4000. The same effective-duration helper derives min(5000, next-start4000)=4000. A blanket min(stored duration, content duration) would make this passing editor assertion hold2. It is therefore not a justified repair. App's timing helper is also unchanged from App `origin/main` `17e46de99`; this audit does not classify the mismatch as newly introduced by normal013/public12.

**Smallest owner seam:** App's selection of the effective occurrence supplied to its default canonical projection, coordinated with the Agent's existing bounded render-projector result. The issue is upstream of public compilation/evaluation. Owners need to reconcile that join against both the exact single-occurrence golden and the unchanged2000→next4000 editor positive. This audit does not select a fallback rule, flip clamp defaults, reactivate renderConfig, or assert that the existing Agent config can be wired into every App consumer without further qualification.

## Commands and results

Run directory: `/home/user/work/wt/app-m3-exact-main-cap-independent-audit`. Define:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
N="$O/workers/app-m3-exact-main-cap-independent-audit/notes"
F="$O/design/handoff-vw-m3-main-image-cap-source-vector-"
```

Only this worker's `node_modules` link temporarily selected private12; an EXIT trap restored `/home/user/work/app/node_modules`. No file/link/cache inside either dependency tree was changed. `$N/vitest.config.ts` imports this worktree's standard config, aliases Composition and its peers to private12, and sets cacheDir inside `$N`.

```sh
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts \
  src/tools/video-editor/data/shotCompositionProjection.test.ts
```

**Exit1; 1 failed/1 passed file; 1 failed/39 passed tests;3.77s.** `$N/targeted.log` records exactly three soft failures in the exact-closure test: hold5 vs4, f105 opacity1 vs0.5, and a layer at120 vs none. Compiler presence, f90 control, identity/content-frame checks and closure preservation pass. No assertion was edited, skipped, disabled or marked expected-to-fail.

Original MAIN pure replay (source tar extracted only into `$N/main-source`):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$N/main-source" \
  /home/user/work/venv-agent/bin/python "${F}replay.py" "$N/replay-"
```

**Exit0**, raw5 → projected4 → serialized4, fps30, image digest unchanged. Log `$N/main-replay.log`; byte comparison of all seven replay outputs against `${F}` originals passed. The extracted temporary source was removed after verification; the immutable source archive remains at `${F}main-source.tar.gz`.

Accessible Agent native/projector and public-opacity probes:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent \
  /home/user/work/venv-agent/bin/python "$N/agent-probe.py" \
  src/tools/video-editor/data/mainImageCap.fixture.json
node "$N/public-opacity-probe.mjs"
git diff --check
```

**All exit0.** Outputs retained in `$N/agent-probe.json`, `$N/public-opacity-probe.json`. These are pure probes, not additional main-suite tests. Native publication keeps4000, bounded projector hold4/end120, authored timing end150; public12 bounded f90/f105=1/0.5 and raw f90/f105=1/1. Byte checks against HEAD preserve the exact regression, fixture and entire original clamp suite; hashes and MAIN/Agent projector equality are in `$N/preservation.json`. Worktree remains clean; the only deliverable content is this shared report.

No installs, shared dependency/cache/venv/runtime writes, product/test changes, render/browser/socket/tsc/full suite, central test request, git mutation or owner-decision reversal. No unified pixel/audio parity, real Runtime acceptance/certification, owner-film behavior or Gate6 closure is claimed. Implementation remains unresolved at the already escalated owner seam; this read-only audit is not blocked. Next step: orchestrator/area owners use these two unchanged positives to qualify their smallest existing-path reconciliation, then re-run the retained exact test.
