# F-D89 protected review — M2 placement

Verdict: `PASS_SOURCE` for `85e04640c6ce33319b1679324499a16c9b201236` only.
This is an independent source/static verdict, not behavioral closure and not pooled with Projection9.

## Identity and scope

- Candidate: `85e04640c6ce33319b1679324499a16c9b201236`, `test(timeline): F-D86 align M2 parent clip mirrors`.
- Own parent/authorbase: `6386c700ee56264aebe12da4558ac74dda0d60ca`.
- Candidate diff: only `tests/editing_conformance/test_recipe_m2_auto_placement.py`, 4 insertions and 3 deletions.
- Candidate blob: `5146188c84a4911ff42ff5c39be5b9da650f8cc5ebdf80bb4900903dad90f861`.
- The two neighboring M2 family files are unchanged; their candidate hashes are
  `033deddcf43a49967c92a0a8fe827d96c0ea758bf071026f5629ec3606e728a6` and
  `51c047472cf0677baf5ce9d0c252afa00b28ccda09b1b2cb60f7ed674e7e8af9`.

The independent shared fixture dependency is tracked separately: occurrence48 birth/reload is `095177db7903075eaa9cae35308b28492a74a008`, adopted by normal home `25c1e182614145c54decb07afc384180cc8e7e34`. Its corrected helper blob is `b42079e3b350212109b63aa86bd0eb145444843b`; the older authorbase helper blob is `41955cb4275d71538ce8dfb232b68c1a4d53a35f`. The occurrence48 review independently reported PASS; it is not used as M2 behavioral proof here.

## Before/after input and topology map

Before, `GenuineTimeline.create` normalizes the actual `inputs(kind)` document by replacing the `picture` registry key with the admitted old media alias, updating its generation/variant identity, and rewriting only direct `payload['clips']` rows. In `document_fixture`, the parent has two physical clip lists: `payload['clips']` and `payload['config']['clips']`, deep-copy mirrors with the same ids, track, asset, at, hold, and opaque fields. The original candidate therefore left the nested mirror at `picture` while the direct mirror became the old alias, which is the reported contradictory-mirror setup error.

After, the same normalization runs over both `payload['clips']` and `payload['config']['clips']`. It changes only the intended asset reference in each mirror; registry media/generation/variant, parent/shot/internal topology, occurrence placement, timing, fps, numeric values, opaque fields, sibling/shared physical sources, and the old/new/verified media inputs remain otherwise untouched. No guard, baseline comparison, or assertion was weakened.

The retained operation topology is unchanged: the genuine Runtime bootstrap creates the parent and occurrence, the recipe emits one completion placement command, and the original execute/replay/inverse/redo/provider paths remain in place. The normal source helper’s birth/reload correction is an independent dependency and is not folded into this verdict.

## Predicate/AST preservation

The protected actual census records 20 selectors: 16 observed setup errors and 4 `NO_JUNIT_CASE` diagnostics. The module AST has 19 top-level `test_` definitions; all 19 names and complete function ASTs compare exactly between the candidate and its parent, including decorators, parameters, `pytest.raises` contexts, assertions, and branches. The retained test IDs are:

`test_portable_goldens`, `test_exact_capture_replay_inverse_and_redo`, `test_anchor_after_starts_at_the_anchor_end_with_the_completion_default`, `test_absent_anchor_appends_at_the_lane_end_and_is_recorded`, `test_absent_anchor_on_an_empty_lane_starts_at_the_occurrence_start`, `test_video_duration_is_supplied_or_defaults_and_never_exceeds_the_verified_media`, `test_the_exact_completed_variant_is_bound_and_siblings_are_untouched`, `test_shared_parent_and_unbound_owners_are_refused_without_touching_input`, `test_unverified_or_unsupported_media_is_refused`, `test_an_anchor_with_unusable_timing_refuses_instead_of_falling_back`, `test_replay_conflicts_when_the_anchor_moved_meanwhile_and_a_rebuild_follows_it`, `test_replay_conflicts_when_the_lane_end_moved_meanwhile_and_a_rebuild_follows_it`, `test_a_clip_moving_onto_the_lane_conflicts_with_the_recorded_lane_end`, `test_the_saved_fallback_time_and_track_win_and_stay_fixed_when_siblings_move`, `test_the_saved_preferred_track_wins_with_a_present_anchor`, `test_a_deleted_saved_track_refuses_instead_of_recomputing_another_lane`, `test_a_birth_cannot_appear_through_both_occurrences_after_a_retarget`, `test_replay_refuses_when_the_anchor_was_deleted_meanwhile_and_a_rebuild_falls_back`, `test_provider_accepts_completion_placement_with_exact_undo_and_redo`.

## Checks

Passed:

- in-memory `compile()` for exact baseline and candidate sources;
- scoped Ruff, baseline from `git show` and candidate;
- scoped mypy, baseline via `--shadow-file` and candidate;
- `git diff --check`.

No pytest, collection, test/function/fixture execution, Runtime service, build, browser, render, or probe was run. The prior 16 setup-error / 4 unknown diagnostics are preserved as diagnostics, not converted into a behavioral PASS. Functional MAIN proof remains mandatory.

## Handoff

Request the normal original-author fixture merge and verify the exact home/integration blob before behavioral qualification. Never merge a review branch. The source/static PASS does not close the Runtime setup or the 4 unknown cases.
