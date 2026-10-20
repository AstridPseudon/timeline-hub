# Agent owner review: tl/vw-m3-scene-current-owner-unit (de62afbb) into tl/integration

Reviewer: worker `agt-review-scene-current-owner` (read-only; no repo changes, no commit-msg).

**Verdict: APPROVE, bounded to the scene-label join the unit claims, with the conditions in section 6.** No blocking defect found. The D09 *check* half is not in this unit and stays open. Tests were not re-run by me (see section 7).

---

## 1. Scope checked

- Merge-base `git merge-base tl/integration tl/vw-m3-scene-current-owner-unit` = `931d7ec56dadffc2efdc893fec80b4c4aadf8a8e`, which is the current tl/integration head. The unit is a fast-forward candidate; there are no textual conflicts with integration today.
- Diff `931d7ec5..de62afbb`: 5 paths, +811/-19.
  - `astrid/sdk/timeline_filmstrip.py`
  - `astrid/packs/rendering/actions/timeline_visualize/composed_frame.py`
  - `astrid/packs/rendering/actions/timeline_visualize/filmstrip_execution.py`
  - `astrid/packs/rendering/actions/timeline_visualize/filmstrip_cards.py`
  - `tests/packs/rendering/test_scene_source_carry.py` (new, 582 lines)
- Matches the five paths named in `design/handoff-vw-m3-scene-current-final-review-REPORT.md`. Nothing else changed: `run.py`, `service.py`, providers, compiler, pins, schemas, `tests/sdk/test_capture_closure_source.py` are untouched.
- Read: the handoff report; the closed escalation `escalations/closed/viewing-20261020T0438Z-d09-caller-source-join.md` (the 04:44 D09 rules); `agent-review-live-scene-join-r2.md` and `agent-review-viewing-landings-0745.md` (my earlier approvals); `agent-pcm-source-carry.md` and `agent-pcm-compile-idempotence.md`.

## 2. Checklist

| Requirement | Result | Evidence |
|---|---|---|
| Five paths are the only ones changed | **Met** | `git diff --name-status 931d7ec5..de62afbb` lists exactly the five above. |
| Saving stays renderer-free | **Met** | The only new scene evaluation is `host_frames_at`, called from `CaptureSceneLabels.observe`. That runs only from `RemotionFrameProvider._observe_scene`, installed by `prepare_filmstrip` on the `composed_frame_capture` branch. `prepare_filmstrip` callers are visualize only: `fast_lane.py`, `timeline/cli_visualize.py`, `sdk/invocation.py` (filmstrip review). No save/commit/apply code is touched. |
| Unknown scene checks stay advisory | **Met for labels** | `labels_for_scene` drops a label only when `visible is False`. Unknown `visible`/`opacity` stays shown (opacity `None` is kept by the `attach_frame_addresses` filter). Unavailable query raises, which fails the capture; it does not change a label to unknown. No new blocking check is added. |
| No source authority / provider / compiler / pin change | **Met** | No change to `remotion_runtime.py`, providers, `Timeline` compile, schemas, or `run.py`. The only compile-domain touch is `prepare_filmstrip`'s fps derivation (see 6.5). |
| Retained source validated against the real unsliced compiled inputs; not reconstructed from authored stamps or colon-IDs | **Met, with a note** | The source is `_open_current_input_closure` / `_open_candidate_input_closure` output (the projector's compiled config). `RemotionFrameProvider.__init__` recomputes `source_identity` from `{authority, config, registry}`, requires `Timeline.load(timeline_path).to_config() == Timeline.from_config(config).to_config()`, requires the materialized registry to equal the retained registry, and re-derives `scene_clips` from `config` and compares. No colon parsing; the `source_clip_id`/`occurrence_id` come from the `app.astrid_shot_composition` fields that the projector writes into the retained config. See 6.4 for the caveat. |
| Final-Root callback failure behaviour | **Fail-closed, as decided** | See section 3. |
| Fresh-only labels: cached/stale frames never labelled fresh | **Met** | See section 4. |
| Tests named exist; no new skip/xfail | **Met** | `grep -n skip|xfail|fails` on the new file returns nothing. The named tests exist (section 5). The closure-source file is unchanged, so its 9 strict xfails are unchanged. |
| D09 rules: same resolved registry, theme, merged props, post-resolve candidate and revision/occurrence identity reused for labels | **Met for labels** | Section 3. The *check* half of D09 ("reused for check and labels") is not in this unit. |
| No default to empty assets or builtin theme in the join | **Met, with a note** | The join uses the same `_resolved_theme_for_render` and `_load_registry_mapping` as run.py, so the theme compared is the theme the render used. It is never a new default. But see 6.2: the visualize route never supplies `theme_path`, so both sides are builtin. |
| Interplay with PCM source carry (slice in the compiled domain) | **Compatible now; one trap for the PCM join** | See 6.3. |

## 3. Final-Root callback: behaviour and semantics

Call site: `run.py:1169-1170`, `if on_scene_props is not None and frame_numbers is not None: on_scene_props(merged_props, frame_numbers)`. This is after `props_path.write_text` and before Node runs. `merged_props` is the final Root input (same timeline, theme, assets as the render).

Behaviour when the observer runs:
- `_observe_scene` raises `SceneQueryUnavailable` on any mismatch: frames not equal to the requested fresh frames, source bytes changed, theme differing from the resolved theme, timeline differing from the retained compiled timeline (only the reserved `__astridAssets` is allowed to differ), staged asset bytes or digests differing, registry differing, or canonical basis differing.
- The exception is not caught in `run.py`. It propagates through `capture_remotion_frames` → `worker.capture` → `RemotionFrameProvider.capture`. The `except BaseException` path unlinks the destinations just written in that call, forces the session closed, and re-raises. No cache entries are written (cache writes come after the copy loop). No scene facts are retained.
- If the observer is never called on a composed capture, `capture` raises `RuntimeError("capture did not observe final scene props")`. Also fail-closed.

Matches the decided semantics. The earlier scene hook review (`agent-review-viewing-landings-0745.md`, item 2) recommended recording "fail-closed" for the observer, and the 04:44 D09 rule says the join must not default to unavailable. This unit does the fail-closed version.

Owner note, not a blocker: the blast radius is the whole composed-frame capture, not only the labels. A source mismatch in the observer fails the frames too. That is the decided semantics, but it should be stated in the owner's film-viewing list.

Earlier-review finding 1 (failed first `observe` leaves the adapter "already used") is moot now. `_observe_scene` builds a new `CaptureSceneLabels` on every callback. A second callback in the same capture is refused by `_pending_scene is not None`.

## 4. Fresh-only labels

- `RemotionFrameProvider.capture` resets `scene_capture`, `_pending_scene` and `fresh_scene_frames` at the start of every call.
- `_fresh_requested` is set to exactly the miss frames before `worker.capture`. The observer requires the callback frames to equal it.
- After the copy loop succeeds, `retain(produced)` requires `set(produced) == set(self._answers)` and every produced file to exist. Only then is `scene_capture` set and `fresh_scene_frames = set(produced)`.
- `scene_for_frame(frame)` returns the capture only for frames in `fresh_scene_frames`. Cache-hit frames return `None`, so `attach_frame_addresses` and `_contact_overlay_for_layers` use the legacy `addresses_at` / `overlay_labels_at` path. Legacy is labelled as legacy, never as scene-fresh.
- Cache writes happen after `retain`. A failed capture writes no cache entries, so a later cache hit cannot be a frame that failed the scene check.
- `close(force=True)` clears all of it. `close()` (non-forced, which `execute_filmstrip` calls after `build_filmstrip_pack`) keeps it for `attach_frame_addresses`, which is the intended order.

Verified by reading. The test `test_mixed_cached_and_fresh_batch_has_facts_only_for_observed_frames` covers it, but I did not run it.

## 5. Named tests (exist in `tests/packs/rendering/test_scene_source_carry.py`, no skip/xfail)

- `test_real_projector_carries_opaque_occurrences_and_all_clip_ids`
- `test_actual_source_join_queries_historical_scene_and_overlay` (parametrized)
- `test_mixed_cached_and_fresh_batch_has_facts_only_for_observed_frames`
- `test_failed_capture_or_copy_exposes_no_scene_and_removes_partial_files` (parametrized: capture, missing, copy, query, frames, no_callback, extra)
- `test_final_props_must_match_the_same_frozen_source_before_query` (timeline, theme, assets, late_source)
- `test_materialized_and_retained_sources_cannot_be_substituted` (identity, timeline, registry, map, occurrence)
- `test_canonical_basis_uses_whole_partial_canvas_and_rational_rate`
- `test_persistent_renderer_forwards_final_props_callback`
- `test_candidate_retains_real_compiled_candidate_and_base_label`
- `test_historical_capture_and_managed_labels_name_their_consumed_revision`
- `test_wrong_canonical_basis_cannot_query`
- `test_wrong_materialized_media_cannot_query` (digest, locator, metadata)
- `test_execute_handoff_uses_actual_provider_and_public_labels_in_exported_pack`
- `test_staged_element_asset_substitution_fails_before_query`
- `test_source_join_preserves_empty_and_unknown_transport_answers`
- `test_staged_element_asset_map_is_bound_before_query` (missing, extra, outside)
- `test_sdk_source_reaches_real_final_staging_callback` (parametrized)

## 6. Conditions and caveats

1. **Commit message count is wrong.** The commit body says "Validate with the exact direct batch: 201 passed and 9 existing xfailed". The Viewing report gives 79 + 125 + 7 direct, and 18 passed / 9 xfailed for the closure file, 229 passed in total. Correct the body to the reproduced counts before the commit goes in.
2. **D09 check half is not in this unit.** The rule says the join must be reused "for check and labels". The unit wires labels only (`attach_frame_addresses`, `_contact_overlay_for_layers`). `layers/builtin_checks.py` and `motion/lint.py` do not consume scene facts here. Keep the check half open in the D09 record. Do not describe this unit as the complete D09 join.
3. **PCM trap.** `run.py:1169` calls the observer on `merged_props` after `props_path.write_text` and before Node. The observer requires the final timeline to equal the retained compiled unsliced timeline, except for `__astridAssets`. The PCM design puts its audio helper call "after `merged_props` and before `props_path.write_text` (`:1167`)" and may add `audio.render_source` to clips (`agent-pcm-source-carry.md` §2 and §3). Either change alters the observed timeline, so the observer would fail closed for every composed capture that carries an authored audio clip. When the PCM join lands, either keep the helper after the observer, or extend the observer's explicit allowance to the render-source field with a test. Do not widen it silently. The compile-idempotence result (`compile(compile(x)) == compile(x)` on 64 fixtures) is consistent with the observer's compiled-domain comparison, so the slice domain question is settled in the observer's favour.
4. **Production shape not verified.** Two equalities are exact and would fail closed on every capture if the production inputs differ from the tests:
   - `self._registry != self.snapshot["registry"]` in `__init__`. The materialized `assets_path` file must equal the retained registry exactly. The `file` locator is stripped only on the props side in `_observe_scene`, not on this side.
   - `scene_clips` relies on `app.astrid_shot_composition` stamps in the retained config. These are projector output, hashed into the identity, and re-derived in `__init__`, so this is self-consistency rather than colon parsing. But the mapping is not an independent authority. The fallback `source_clip_id = clip_id` also uses the raw ID if the stamp is missing.
   Verify both against one real materialized composed capture before activation. I did not run a production capture.
5. **Behaviour change in `prepare_filmstrip` fps.** Previously `fps` came from `theme_overrides.visual.canvas.fps` with a fallback to 30 on bad values. It now comes from `resolve_render_profile(config, registry).fps_rational` with no runtime theme. Consequences:
   - A malformed canvas (for example a non-integer fps) that used to fall back to 30 now raises from `_fps_fraction` / `_positive_dimension` during capture preparation. The fail is earlier and louder, which is arguably right, but it is a new failure mode.
   - The envelope profile is built from the builtin theme, not the runtime theme. The provider later overwrites `snapshot["fps_rational"]` with the canonical profile, which does use the runtime theme. So the envelope and executed profiles can differ if a runtime theme canvas differs. No production caller passes `theme_path` on this route (see 6.2), so this is latent today.
   Ask Viewing for one test on a malformed override, or accept the change in writing.
6. **Theme on the visualize route.** `filmstrip_execution` passes `getattr(args, 'theme_path', None)`. No visualize caller sets `theme_path` (`timeline_visualize/run.py` and the fast lane do not). So `_resolved_theme_for_render` returns `builtin_theme()` plus overrides on both the render side (`run.py`) and the labels side. The join is consistent with the real render, which is the D09 requirement, but it means the runtime-pinned theme does not reach visualize captures. If the owner intends runtime theme on this route, `theme_path` must be threaded, and then the observer will fail closed until it is. Record this as an open item.
7. **Other notes, not blocking:**
   - `_observe_scene` reads `entry["digest"]` etc. and calls `.removeprefix` on it. A `None` digest raises `AttributeError`, not `SceneQueryUnavailable`. It still fails closed, because the exception propagates.
   - `RemotionFrameProvider.__init__` deep-copies the snapshot and also writes `fps_rational`, `duration_frames` and `resolved_theme` back into the caller's `snapshot` dict. Callers rely on that today. The change is intentional but silent.
   - The labels are not marked UNCERTIFIED on the authoring-preview (working-copy) branch. Its content is the candidate's compiled config, and the identity covers `working_copy`, so the labels are grounded. The 2026-10-20 "UNCERTIFIED" decision was about certification, which this unit does not claim.

## 7. Tests: what I ran

- I did **not** re-run the test suites. An attempt to run pytest on an export of `de62afbb` under the shared venv (`/home/user/work/venv-agent`) was refused for approval by the sandbox. I did not work around that.
- Viewing's cited results (from `handoff-vw-m3-scene-current-final-review-REPORT.md`; that report says an independent reviewer reproduced them in a clean frozen worktree):
  - `test_scene_source_carry.py` + `test_capture_scene_labels.py`: 79 passed (17.47s)
  - six neighbouring capture/labels/SDK/cards files, `-k 'not test_pack_'`: 125 passed / 3 deselected
  - four exact executor nodeids: 7 passed
  - `tests/sdk/test_capture_closure_source.py`: 18 passed / 9 existing strict xfailed
  - ruff on the direct tests: clean; `git diff --check`: exit 0
  - total 229 passed, 9 xfailed, 0 failed
- Not run by me: any full suite, `make check`, or any Remotion/browser/socket lane. Per the orchestrator rule, a full suite must go through the central test service, and this review did not request one.

## 8. Conflicts expected with integration

- **Today:** none. The integration head is the merge-base.
- **Unmerged branches that touch the same files** (not ancestors of tl/integration; verified by `git merge-base --is-ancestor` and `git diff --name-only 931d7ec5...<branch>`):
  - `tl/vw-m3-scene-stage-four` (`09cfd10a`, 57 paths): `composed_frame.py`, `filmstrip_cards.py`, `filmstrip_execution.py`, `timeline_filmstrip.py`, `run.py`, `fast_lane.py`, `overlays/labels.py` and more. Expect textual conflicts in all of these.
  - `tl/vw-m3-uncertified-capture-labels` (`2a862eaf`): the same five files, plus `service.py`, `provenance.py` and `inspection_contract.py`.
  - `tl/vw-m3-scene-stage-three` (`7b8c4dc4`): overlaps with the same files.
  - The second of these to land conflicts with this unit. Pick the one that matches the owner's intended scene-label design and have the other rebased onto it. Do not merge two competing joins.
- **Already merged, no conflict:** `tl/vw-m3-live-scene-join-r2` (`630c9d0a`, `CaptureSceneLabels` and labels), the observer hook `tl/vw-m3-current-capture-scene-hook` (`18ec2b57`, `run.py` `on_scene_props`), and the D09 caller join `tl/agt-d09-caller-join` (`4a75f68f`).
- **PCM branches** (`tl/agt-m2-pcm-source-carry-design` `02e440df`, `tl/agt-m3-pcm-source-phase` `01d82c55`, `tl/agt-pcm-compile-idempotence` `408f3ba3`): none of the five paths overlaps by name. The expected conflict is adjacency in `run.py` around 1104-1170, plus the semantic trap in 6.3.

## 9. Recommendation

Accept this exact candidate into tl/integration as the bounded labels join, after the commit-message count is corrected (6.1). Record in the D09 notes that the check half and the production-shape checks (6.4) are still open. Before the PCM source-carry lands, the observer's allowance must be settled (6.3). The owner should see section 3's blast-radius note and 6.5's fps change in the film-viewing list.
