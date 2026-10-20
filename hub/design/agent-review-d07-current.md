# Agent D07 cut review — 2026-10-20 UTC

## REJECT

`tl/agt-m2-d07-retime-cut` at `225ae22f` is not approved against
`c456b328`.

The relocation itself is behaviorally sound: the target `units.py` keeps the
old exact arithmetic and the target SDK facade points the five time helpers
and `grid` at that module. A read-only target-source smoke passed rational
`Fraction` FPS, affine source/timeline conversion at non-unit speed,
half-open interval quantization, and collapsed-range rejection. There are no
live Python importers/callers of the deleted detached `retime` or
`retime_with_ripple` names.

### Required coverage fix

`tests/test_timeline_editing_helpers.py` deletes three positive behavior
blocks, but the remaining tests do not provide exact native/compiler
replacements for all of them. The replacement mapping is:

| Removed positive | Existing replacement that does cover part of it | Missing proof |
| --- | --- | --- |
| `test_canonical_source_trim_speed_move_and_retime_intervals` | `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_trim_hold_is_source_time_and_playback_duration_applies_speed`; `tests/editing_conformance/test_recipe_m1_commands.py::test_trimmed_positive_speed_nonzero_occurrence_and_sibling_isolation`; `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_rational_fps_source_contact_and_half_open_intervals_are_not_requantized` | The detached test's combined move + endpoint-length-change assertion is only re-run through the detached `move` helper in the new test, not through one named native/compiler replacement. |
| `test_ripple_is_track_scoped_and_never_moves_audio` | `tests/packs/timeline/test_cli_edit_flags.py::test_insert_time_moves_everything_after_it_later`; `tests/sdk/test_timeline_checkout.py::test_close_gap_before_a_word_ripples_everything_after` | No existing test asserts the same operation shifts only later visual siblings on one track, leaves an audio clip's `(at, from, to)` unchanged, and extends the parent from `2` to `2.5`. |
| `test_ripple_shifts_canonical_intervals_without_touching_audio` | `tests/sdk/test_timeline_media_verbs.py::test_trim_slip_and_move_keep_the_window_equal_to_the_hold`; `tests/editing_conformance/test_recipe_m1_commands.py::test_trimmed_positive_speed_nonzero_occurrence_and_sibling_isolation` | No existing native/compiler test asserts that the shifted later visual sibling retains its literal source window `(from, to) == (8, 9)` while audio remains unchanged. |

Add or identify one actual supported native/compiler replacement for the two
ripple positives and name it explicitly. It must assert the old positive
state, not merely that retired names are absent: visual first clip becomes
`[0, 1.5)`, later same-track visual becomes `[1.5, 2.5)` with its source
window unchanged, unrelated audio remains `[0, 2)`, and the explicit parent
extend policy produces duration `2.5`. If no supported native/compiler
operation has this semantics, the cut cannot claim the old behavior was
preserved; keep the original positive expectation (strict `xfail` only while
the authorized replacement is genuinely missing) and escalate the missing
replacement instead of deleting the proof.

Also add a public-facade assertion that `from astrid.sdk import
frame_time, source_to_timeline_time, timeline_to_source_time, quantize_time,
quantize_interval, grid` resolves to the relocated module. The current
remaining helper tests import these directly from `astrid.sdk.timeline.units`,
so they do not verify the changed lazy exports.

### Required documentation deletions

The commit removes the APIs but leaves these live prescriptions, including an
executable import example:

- `docs/timeline-authoring-capabilities.md:49-51,63`: remove the
  `retime_with_ripple` capability prose and table row; remove `retime` from
  the `move / retime` row or replace it with the named supported native path.
- `docs/timeline-editing-guide.md:302-304,314`: remove the
  `retime_with_ripple` instructions and table row; remove `retime` from the
  helper table unless it is replaced by a named supported path.
- `astrid/packs/rendering/docs/references/document-checkout.md:250-275`:
  remove both detached `retime` entries and the `retime_with_ripple` example
  import/call. Keep the relocated exact-time/quantization documentation.

Do not treat the existing Checkout `retime()` method references as the
deleted detached helper; those are a separate native Checkout API and are
covered by the native reflow tests.

## Targeted evidence

- `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_media_verbs.py tests/editing_conformance/test_recipe_m1_commands.py::test_trimmed_positive_speed_nonzero_occurrence_and_sibling_isolation tests/editing_conformance/test_recipe_m1_commands.py::test_quantization_once_with_rational_fps_and_ms_codec tests/editing_conformance/test_recipe_m2_clip_trim.py::test_trim_hold_is_source_time_and_playback_duration_applies_speed tests/editing_conformance/test_recipe_m2_clip_trim.py::test_rational_fps_source_contact_and_half_open_intervals_are_not_requantized tests/sdk/test_timeline_clip_trim_provider.py::test_move_then_trim_is_an_ordinary_native_writer_and_undo_keeps_the_move tests/sdk/test_timeline_checkout.py::test_ripple_delete_across_a_shot_boundary_keeps_audio_in_sync tests/sdk/test_timeline_checkout.py::test_close_gap_before_a_word_ripples_everything_after tests/sdk/test_timeline_checkout.py::test_a_longer_take_reflows_the_film_and_keeps_the_gap_overlays_and_music tests/sdk/test_timeline_reflow_golden.py::test_a_reflow_moves_and_stretches_a_time_lapse_as_one_unit tests/packs/timeline/test_cli_edit_flags.py::test_insert_time_moves_everything_after_it_later --tb=short` — **24 passed**.
- Read-only execution of the exact target `225ae22f:astrid/sdk/timeline/units.py` — **PASS** for rational `Fraction` FPS, non-unit source mapping, half-open quantization, and collapsed intervals.
- AST parse of all four target Python files — **PASS**.
- No full/live suite requested.

No product files were modified in this review. The reviewer's worktree is
clean.
