# Agent review: tl/vw-m3-live-scene-join-r2 (630c9d0a9)

**Verdict: APPROVE, for the inactive seam only.** No blocking defect found. The branch does not satisfy the D09 source-identity join and does not activate anything; both remain open Agent-owner work.

## Scope checked

- Merge-base: `86d7cf9b1fcaab7afb7a2e1ba66f57ef84935e31` (`git merge-base tl/integration tl/vw-m3-live-scene-join-r2`).
- Diff `86d7cf9b..tl/vw-m3-live-scene-join-r2`: 3 files, 351 insertions, 5 deletions. Only these are touched:
  - `astrid/packs/rendering/actions/timeline_visualize/composed_frame.py` (new `CaptureSceneLabels`, `copy` import)
  - `astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py` (`SceneLabel`, `labels_for_scene`, optional `capture=` branch, `draw_labels` tweaks)
  - `tests/packs/rendering/test_capture_scene_labels.py` (new, 20 cases)
- Read: `handoff-vw-m3-live-scene-seam-review-REPORT.md` and `handoff-vw-m3-live-scene-join-r2-REPORT.md` in the design dir.
- I did not run the tests. Viewing's claimed results (53 passed across the four files, lint, `git diff --check`) are unverified here. The branch is not checked out in my worktree, and I was read-only.

## Checklist

| Requirement | Result |
|---|---|
| No scene evaluation in the save path | Pass. The only new calls to `host_frames_at` sit in `CaptureSceneLabels.observe`, which nothing calls. No save or export code is touched. |
| No source authority, provider, compiler or pin change | Pass. Product diff is two files, neither touching providers, compiler or pins. The public12 artifact appears only in test env defaults. |
| No production caller (inactive) | Pass. `git grep` on the branch finds no caller of `CaptureSceneLabels`. `overlay_labels_frame` is called without `capture=` at `fast_lane.py:742` and `layers/builtin.py:507`; both keep the legacy path. |
| Unknown scene checks stay advisory | Pass. `visible`, `opacity` and `bounds` that come back unknown go to the legend as "unknown" text. They never raise and never hide a label. Query unavailability raises by design, so no stale facts are shown. |
| Same registry, theme, merged props, candidate and revision/occurrence identity (D09) | **Not satisfied by this seam, and not claimed.** The adapter accepts whatever `props`, `basis` and `source_identity` the caller gives it. It checks only equality with its own detached copy. `source_identity` is an opaque string. The review report says this, and the join stays held. |
| Never defaults to empty assets or builtin theme | Pass. Product code has no defaults for props or theme. The `builtin_theme()` and empty `assets` in the test fixtures are test-only. `builtin_theme()` returns a deep copy, so the stale-input tests do not leak state. |
| No colon-ID parsing, no second projector | Pass. Addresses come from the owner-supplied map (`addresses[layer["clipId"]]`), and `observe` requires exact ID-set equality with that map. No `split(":")` and no projector call. |
| Only the stated 3 files | Pass (confirmed by `git diff --name-only`). |
| Named tests exist, no skip or xfail | Pass. `grep -i skip|xfail|fails` on the new test file returns nothing. The 20 cases match the report's count: 1 + 3 + 2 + 5 + 1 + 1 + 1 + 1 + 1 + 4. |

## Behaviour of legacy paths

- Legacy `Visible` items (`onscreen.py`) have no `visible` attribute. `getattr(item, "visible", True)` therefore returns `True`, so the boxed/legend split is unchanged for them.
- Legacy opacity is always a float, so the new `opacity is None` branches do not fire for them.
- `legend = [i for i in shown if i not in boxed_all]` is the exact complement of the old filter, so the legacy legend set is unchanged.

## Findings (none blocking)

1. **Failed first `observe` leaves the adapter "already used".** `self._frames` is set before validation. A mismatch on the first call therefore makes every retry report "already used" instead of the real cause. Consider assigning `_frames` only after validation, or accept it as a one-shot policy.
2. **Malformed props raise `KeyError`, not `SceneQueryUnavailable`.** `observe` reads `clip["id"]` and `answer["layers"]` directly. This is low risk because the owner passes validated props. Still, it breaks the module's "refuse with the named error" pattern.
3. **`retain` checks keys and file existence only.** Its docstring says the owner must supply only the fresh batch. The review report already accepts this as an owner-attested limit.
4. **Lazy import inside `labels()`.** Acceptable for the cycle, but worth a comment if it stays.

## What the Agent-owned wiring still needs

These are unchanged from the report and are required before any activation:

1. **Source binding in `prepare_filmstrip` / `RemotionFrameProvider` (`filmstrip_execution.py` ~1771).** Carry the same retained revision/candidate/closure and the projector's exact compiled-ID to address map, including nonvisual clips. Do not parse the colon-composed ID.
2. **Basis.** Derive `fps_rational`, width and height from `_canonical_profile(timeline_path, _load_registry_mapping(assets_path), theme_path)`, computed from the same frozen inputs. Convert fps only at the numeric API boundary. Do not use the merged theme canvas or thumbnail size.
3. **Callback binding.** `tl/integration` already has `on_scene_props` in `rendering/renderers/remotion/run.py` (lines 1035, 1169, 1387, 1425), called as `on_scene_props(merged_props, frame_numbers)`. That matches `observe(props, frames)`. Inside it, validate the final staged Root timeline, materialized assets and resolved theme against the owner-held source before constructing the adapter with those exact props. Note that `observe` requires `frames` to be sorted and unique. The callback must pass the actual frame tuple, not planned metadata frames.
4. **Per invocation.** Construct a new adapter in both `_PersistentRemotionRenderer.__call__` and `_SharedRemotionOwner.render`. Do not reuse it on the warm session. Call `retain()` only with the complete fresh `dict[int, Path]` from `capture_remotion_frames`, before temp files are removed. Pass the same adapter and source identity to `overlay_labels_frame`. Cache-only cards keep the legacy fallback. Never pass a combined cached and fresh map to `retain()`.
5. **Public12.** The seam tests run against public12 (`0a7b6152…`). Production still pins public10, so public12 adoption is a separate owner prerequisite.

## Recommended next steps

- Land this seam as inactive, or hold it until the wiring is ready.
- Agent wires items 1–4 above, then runs the central targeted lane (`test_capture_scene_labels.py` plus the four neighbour files). Do not run this review's results as evidence of activation.
- If the owner decides not to activate, delete the class, `labels_for_scene`, the `capture=` branch and the test file together, as the report says.
- Optional: share the duplicated host fixture provisioning with `test_scene_host.py` once public12 lands. Do not add a new test-host abstraction for this alone.
