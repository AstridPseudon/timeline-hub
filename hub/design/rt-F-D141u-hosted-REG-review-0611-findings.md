# F D141u independent hosted REG review

Verdict: **PASS**. No findings.

The candidate is exactly Agent `57b38b5b9ce672f307afe46c61add43df6350fef`,
tree `5439ca22bc7d3cd334dce9a80a4ff0dc6827ccae`, against base
`8585ed9c0404d0187b2ce70242d25114a32747c2`, tree
`92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`. Its complete source diff is one
line in `astrid/packs/rendering/docs/scripts/timeline_document.py`, changing
the detached publication caller from `_capture_bundle` to the public `_bundle`
projection.

The production trace is genuine: the script opens `TimelineSession` with the
candidate's exact base revision/publication pair, obtains session state, calls
`_bundle`, emits the document publication commands, and later submits the
existing commit request. `TimelineSession._bundle` delegates to private
`_capture_bundle`; the latter requires the authenticated session identity and
fetches the closure with both `revision_id` and `publication_id`. `_bundle`
then removes only `source_mapping._runtime_document`, preserving the public
no-leak boundary. This retains D71 exact-pair authority and does not widen or
discard publication authentication.

The two original upstream selectors pass on the explicitly authorized final
Runtime `95d98f038320d5d46bd679ac000ab3e15825c935`, tree
`78df31d62c5b9ba4c84dee4ea346e43a767718c1`, clean at
`/home/user/work/runtime`. The exact introducers of the regression are
`8a4103dd16bb32306ca6c782dcd9a7a4a908de6d` and its repeat
`8d14d5be1887c6ae43c1c2da83219c4b2197012e`.

No source, test, fixture, authored input, schema, generated file, or pin was
changed by this review. D141r media tests and the public-marker conversion
remain unchanged. Full/core/browser/Farm/P4/P5 suites were not run.
