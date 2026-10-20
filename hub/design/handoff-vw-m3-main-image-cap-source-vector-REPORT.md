# MAIN image / occurrence cap source fixture

**SOURCE FIXTURE READY; visual golden pending actual capture. MAIN changes hold5 to hold4 before rendering.** No product changes. All evidence is flat under this report's absolute filename prefix. Agent/compiler owner: this is contrary evidence to INBOX10:35's suggested raw5 direction; do not choose opacity1 merely from that expectation. The measured source route retains the authored closure unchanged and sends a four-second image to MAIN's renderer. Composition6's original media fade code therefore predicts opacity0.5 at frame105. This prediction is not a decoded-pixel result or an approved new golden.

## Frozen source

- Agent `origin/main`: `a411628f8fd6129f9c58c332019b56769d997384` (verified against the actual ref).
- MAIN Root SHA256: `e367f43b97d9b7ffe016257c10eb7ca6da7ffa2aa89e9539cb112104ad00e775`.
- MAIN generator SHA256: `9eb298e5536d2e17b5ae754acc0cba22ec843a911b017ca33228ec3e77cc7f1b`.
- MAIN core projector SHA256: `433dce617f10e31fe6066d55c6bff125e4328a84e01426f4d2e45756b432253a`.
- Locked Composition0.0.6: tag commit `67b8aa3d0d6831d3e3504a340ff583c3da253707`, archive SHA256 `78746170f9c337650991dacca7a303c71be89ee5e61c25ef821390c7563df87b`, **29 regular members**. Deterministic original `git archive` + `gzip -n` exactly reproduces MAIN lock integrity `sha512-QV17ysuqgzAiewEGsF84yo3DKFffLNoius5WP3yI/AKcHP2zdySrYjE5YXv6UtXgouJqxCO18/qnMNPOMgtsZg==`.
- `source-identity.json` has all MAIN source/component hashes, all29 original Composition member hashes, all post-generation member hashes and the three generated-map hashes. The generator is MAIN's original, run against MAIN's original packs. No replacement components, wrapper policy, peer graph, public12, or custom generator was used.
- `prior-proof-match.json`: the archive, every original/post-generation package member, three generated maps, and every source hash in the existing qualified90PNG MAIN6 proof match exactly. That prior proof has45MAIN +45unified frames for the independent-AM-fade case; it does **not** prove this image-cap case.

## Exact input and normal MAIN route

`raw-closure.json` is a new **synthetic executable analog**, not native App ADD output, accepted Runtime data or owner media. There is no supplied playable/native image for the requested counterexample. MAIN needs a managed image identity and bytes; the analog supplies a deterministic16×16 RGB(240,240,240) PNG with its real SHA256 `ec19e1c7d1d247d56db54f73e6514c92a82147a1b6ab59eaa30edeebca2e82b6`. The image is generated test input, never a captured frame. Synthetic parent/shot/internal pins are explicit; payload digests are computed from their payloads.

The prepared immutable closure has one visual lane, one occurrence at0 with `duration_ms:4000`, speed1, source_offset0, gain1; its internal ordinary `clipType:image` has `at:0, hold:5, effects:{fade_out:1}`. Both MAIN `output.fps` and the canvas fps are numeric30. Output uses MAIN's native `resolution/fps/file` shape. Canvas1920×1080 and builtin theme go through MAIN's normal theme resolver. No rational-object adapter or App format is passed to MAIN.

`replay.py` imports MAIN's existing `_Runtime` test transport from `tests/packs/rendering/test_managed_timeline_render.py`; no new transport/source factory or projector implementation was written. It serves this exact closure to the **unmodified** MAIN `resolve_managed_render_snapshot`. The actual route is:

1. Exact parent/shot/internal reads → `_project_exact_parent_head` → `project_runtime_parent_composition` → the shared `_project_clip`.
2. `_project_clip` computes `min(child end, occurrence end)`, and writes the resulting source-duration cap to `hold`. Here **5 becomes4**; the raw internal `hold:5` remains unchanged. This is MAIN's production projection, not a manually clamped config.
3. Normal `_render_compatible_projection`, `_normalize_pinned_element_references`, `_runtime_snapshot_registry`, and `validate_managed_render_snapshot` pass. Runtime responses are explicitly in-memory test data; this is no authority/admission claim.
4. `materialize_managed_render_snapshot` writes the actual timeline/registry. `_serialize_timeline` calls MAIN `Timeline.load(...).for_render(...).to_json_data()`: **hold remains4**. `_resolved_theme_for_render(..., None)` resolves MAIN's complete builtin export style.
5. Original `AssetMaterializer` verifies the generated PNG against its managed digest and stages its actual bytes. No HTTP server starts. Its ordinary `resolved_registry` takes a minimal static-public URL resolver for the explicitly labelled capture analog; this only supplies `file:image-cap.png`. `main-props-template.json` retains the native managed registry before URL binding; `main-props-static-analog.json` is the exact ready input for the approved static-public image analog. The timeline/theme in both are identical. The capture worker can instead bind the real `InvocationAssetServer` within its central capture lifetime.

The full `_execute_remotion_locked`, service scheduling, task admission and Runtime were **not run**. We reused its real pure prep functions and materializer. The sole capture URL adapter is identified above; it changes neither authored source nor timing. This worker used no Node dependency graph, browser, render, socket, install or network.

## Source implication for Agent

MAIN's registered Root uses its ordinary TimelineComposition; locked6's ordinary image dispatch mounts `VisualClip`, whose unchanged `useFadeOpacity` reads duration from the **projected clip hold4**. Its fade-out spans frames90–120. Consequently source predicts frame90 opacity1, frame105 opacity0.5, frame119 opacity1/30; the composition's ordinary image window is half-open0–120. Frame120 is outside the normal120-frame metadata range and must not be treated as a valid seek/capture by clamping it to119.

Raw hold5 plus a separate cap would leave the fade beginning at120 and predict opacity1 at105. That is a different clock from this frozen MAIN route. No second policy/evaluator was added to calculate a new golden. Agent must reconcile the one-compiler vector with captured MAIN evidence and escalate any intended change; this worker does not alter the settled contract.

## Verification

From `/home/user/work/wt/vw-m3-main-image-cap-source-vector`, with `W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-main-image-cap-source-vector`:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$W/prepare.py"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/main-source" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp="$W/pytest-temp" "$W/main-source/tests/timeline/test_shot_composition_projection.py" "$W/main-source/tests/packs/rendering/test_managed_timeline_render.py"
git diff --check
git status --short
```

Preparation/replay: **PASS exit0**, logged raw_hold5/projected_hold4/serialized_hold4/fps30; original generator **PASS exit0**. Original MAIN suites: **66 passed in5.86s**, no xfails/skips or changed assertions. Whitespace/status: **PASS / empty**. Final independent byte comparison: **2,414 original MAIN files unchanged after generation/tests**. Frozen flat replay: **PASS**, all seven exported outputs reproduced byte-for-byte; see flat frozen-replay-check.log. Prior MAIN6 proof identity comparison: **PASS** (map paths normalized to basenames for comparing the three generated-map dictionary keys only). Full logs are flat `targeted-main.log`, `generator.log`, `replay.log`.

Two preparatory errors were corrected before the successful run: an archive pathspec assumed a nonexistent root `conftest.py`; the first synthetic `output` used width/height/filename instead of MAIN's required resolution/file. MAIN's validator rejected the latter. Corrected only the new input fixture to MAIN's actual format; no behavior test or product rule changed.

The reproducible frozen-source archive and exact fixtures are listed in `READY.md`; its commands unpack into the consumer's OWN directory, replay the raw closure, and verify exact equality before capture. Temporary source/test directories are removed from this worker after export. No repository/build/temp changes remain. No full suite or central request was made.

## Handoff and limits

Source work is complete and unblocked. Capture is separately owned by `vw-m3-main-image-cap-render-proof` under its central-service grant and dependency/disk preflight. It must render MAIN's own registered Root/Composition6/generated registries from this frozen raw replay. The physical frame105 result and any final Agent golden remain **UNVERIFIED** here. Existing capture-worker disk/graph/grant conditions are not waived by SOURCE READY. No App/unified parity, audio, acceptance, delivery or Gate6 qualification is claimed.
