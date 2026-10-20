# Current ordinary014 adoption blocker

## Peer answer

The remaining ordinary014 adoption blocker is the `cd0` owner-strict parent
marker transition in `tests/test_timeline_clip_replacement.py`. It is a
test/source-cohort boundary, not a Runtime product, schema, generated-client,
artifact, or release defect.

Current `tl/integration` already has the exact narrow transition (blob
`43a9743a746bbcb8a7b56f6c7e7a5c2ab3a5d735`):

1. `test_native_parent_clip_swap_route_refuses_parent_ownership_on_current_schema`
   sends the real current-schema request and strictly asserts the
   `ValidationError` that `parent` is not one of `shared`/`occurrence`.
2. `test_native_parent_clip_swap_route_replaces_parent_media` retains the
   complete acceptance body and all positive assertions under a strict,
   narrowly raised `ValidationError` xfail naming schema 0.2.14 and ledger
   D04.

The reviewed ordinary014 candidate `202074110717146fc7f08af2306a8dd7f695b0b1`
was explicitly reviewed as missing this `cd0` transition; its carried test
still has the older imperative/non-strict xfail. The private test-only carry
report records the exact successor test blob
`65f5c22d40da230b368f3c7d3b77bb9ca127aafc`, equivalent to the reviewed `cd0`
blob `cd0b0dcbea57c2a140e970eda59bea1161d6ff06`, with evidence of
`1 passed, 1 xfailed, 23 deselected`. That carry changes no product bytes,
schema, DTO, artifact, pin, or release metadata.

Therefore the adoption hold is: carry this exact test-only `cd0` transition
onto the final ordinary014 Runtime/Agent cohort, preserve the full positive
acceptance body, and qualify that same cohort. Do not invent a new release or
mutate the ordinary014 artifacts to make the marker green. The current public
schema still correctly refuses `parent`; the positive becomes live only with
the coordinated 0.2.14 parent-ownership schema adoption.

Sources checked: `runtime-ordinary202-final-handoff.md` § Required boundary,
`runtime-carrier-cd0-marker-carry.md` § Test contract/Evidence, and the current
`tests/test_timeline_clip_replacement.py` plus the unchanged ordinary014
candidate test.
