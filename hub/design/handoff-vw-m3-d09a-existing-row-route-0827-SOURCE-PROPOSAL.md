# VW-D09a — existing public-row route and one bounded proposal

## Finding

The current integration tree has an admitted source-bound public Scene-row carrier, but it does not reach the normal `render_curves` invocation.

The managed route is:

1. `filmstrip_execution.py:1747-1755` constructs the existing `RemotionFrameProvider` for capture mode and `filmstrip_execution.py:1812-1815` passes that same provider into `build_filmstrip_pack`.
2. `filmstrip_cards.py:1802-1804` passes the provider to `motion.sheet.build_context`.
3. `motion/sheet.py:154-188` admits only rows obtained from the provider's exact source identity and fresh/cache evidence mode, then stores them in `ctx.shared["public_scene"]`; mixed or incomplete batches clear the map.
4. The selected-call precedent consumes that carrier in `layers/builtin.py:369-441` (`_public_mouth_facts`) and `:450-473` (`render_lipsync`). Its normal and refusal controls remain the precedent at `tests/packs/rendering/test_presenter_selected_cut_aggregate.py:134-191`.
5. `motion/sheet.py:278-294` invokes layers with the same context, but `layers/builtin.py:278-289` calls `model.props_at(element, t, fps)` without passing the carrier. `motion/model.py:600-603` then calls `mouth_state`; `motion/model.py:627-636` has no source, row, address, or prepared-Root input.

Thus the answer is **carrier present in the managed context, not connected to `render_curves`**. The 18a89a0d2 selected-call precedent is an ancestry point: the relevant source migration is in `b7a7f3ff4`/`7ab874d69`; 18a89a0d2 itself is an unrelated merge. On real `origin/main` (`a411628f8fd6129f9c58c332019b56769d997384`), the curve call remains the same unbound `props_at` path; the public-row handoff is the current integration addition, not a reason to claim that origin/main already carries rows into curves.

## One minimal caller-threading proposal

Reuse the existing carrier and the existing `_public_mouth_facts` admission rules. In the two existing source files below, add only a private, optional mouth-state threading point:

- `astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py`: in `render_curves`, obtain the admitted `states` for an `am-presenter` from the already-populated `ctx.shared["public_scene"]` using `_public_mouth_facts`; pass a state only for a frame that has an admitted row.
- `astrid/packs/rendering/actions/timeline_visualize/motion/model.py`: thread that optional state through the private `props_at` → `_presenter_props` call. The default remains the current call, so callers without a row still execute `mouth_state` unchanged. This is an internal keyword-only seam, not a public API, DTO, provider, store, source factory, hash authority, renderer-save hook, or new protocol.

The migration is deliberately partial: rows absent from the managed sampled set stay on `mouth_state`; no private evaluator or geometry is deleted. The existing context carrier is the only source of authority, and its source/basis/address/evidence checks remain before state use.

## Required tests for that one proposal

Add one pure regression beside the selected-call tests in `tests/packs/rendering/test_presenter_selected_cut_aggregate.py` that supplies a complete admitted public row set to `build_context`, invokes `render_curves`, and proves the presenter `mouth` curve uses the row's `diagnostics.motion.mouth` at the same clip-local frame. The test must also prove a frame absent from the row map uses the unchanged private result.

Keep and rerun the existing controls without weakening or deleting them:

- `test_single_mode_public_mouth_facts_drive_existing_consumer` for the admitted fresh/cache selected path.
- `test_mixed_public_mouth_facts_keep_private_fallback`, `test_partial_or_default_raw_mouth_keeps_private_fallback`, and `test_planted_public_fact_failures_keep_private_fallback` for mixed, default/partial/raw-invalid, stale/forged/missing-row preservation.
- `test_scene_source_carry.py` source/basis/retained-input and incomplete-answer refusal tests.
- `test_scene_cache_payload.py` stale/forged/other-frame cache misses and failed-batch no-mint controls.
- `test_timeline_visualize_motion_views.py::test_mouth_state_matches_presenter_core_cycle` for the retained private codebook.
- `presenter_scene_capability.mjs` `states`, `clock`, `registration`, and `unknowns` modes for public codebook, clock/binding, registration, and UNKNOWN behavior.

The proposal must not change `render_lipsync`'s crop selection, strict `>2%` pixel comparison, selected-frame denominator, PNG statistics, or any unbound/default/partial/raw-invalid/mixed/stale/forged/UNKNOWN fallback. No implementation is included in this handoff; the proposal is not evidence that the curve migration is qualified.
