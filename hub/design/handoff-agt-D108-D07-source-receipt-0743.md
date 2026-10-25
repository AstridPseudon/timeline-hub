# F-D108 D07 source receipt — exact mapping and handoff correction

This is a docs-only source receipt. The independent protected review
`handoff-agt-D108-batch-review-0737.md` gives Scope A `PASS_SOURCE`; it does
not establish functional execution. D108 actual functional coverage remains
UNPROVED and the status is SOURCE-QUALIFIED / BEHAVIOR-PENDING.

## Exact original-to-current mapping

| ID | Exact original positive helper selector | Exact current selector | Scoped status |
| --- | --- | --- | --- |
| D07-1 | `tests/test_timeline_editing_helpers.py::test_ripple_is_track_scoped_and_never_moves_audio` | `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_native_group_preserves_exact_track_scoped_ripple_timing_and_audio` | Source-qualified; behavior pending |
| D07-2 | `tests/test_timeline_editing_helpers.py::test_canonical_source_trim_speed_move_and_retime_intervals` | `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_native_speed_two_preserves_source_window_move_and_endpoint_length` | Source-qualified; behavior pending |
| D07-3 | `tests/test_timeline_editing_helpers.py::test_ripple_shifts_canonical_intervals_without_touching_audio` | `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_native_group_preserves_shifted_source_window_and_audio_bytes` | Source-qualified; behavior pending |

The authored candidate is `tl/agt-F-D108-D07-coverage-0732` at
`f45e6c732d35dc7a04cd6fc0d019f5f67bcc522b`, with candidate blob
`1b34745fca1dcc21f15267f744711eb16d4b5700` and parent blob
`62384aad61494c67a614ad1a7122fee4119e0829`. The normal merge queue receipt
is `queue/done/merge-agt-F-D108-D07-coverage-0732`, and its authoritative
normal integrated result is `b943270a9ed42bb968dbaeace7b296d9898ea21b`,
merging onto `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`. This is source
provenance, not a behavior result.

Source basis: `handoff-agt-D108-D07-source-0724.md/.json` and the existing
D07 ledger row are preserved reference inputs.

The required corrected handoff names are the exact byte copies
`handoff-agt-D108-D07-coverage-0732.md/.json`; the authored files with the
erroneous extra `F-` remain unchanged. The source handoff and review are not
amended.

The three separately approved D07 retired-policy flags remain interface-scope
facts only; no broad blanket clearance, legacy retirement, new scope, or
effective D69 closure is claimed. Static checks are not a test PASS. The
immutable full-core captured tuple is not retargeted or repeated and may not
contain these three new selectors. If they are absent from that capture,
meaningful post-core coverage remains required. No product, guard, authority,
pin, source-body, or test-body change is made by this receipt.
