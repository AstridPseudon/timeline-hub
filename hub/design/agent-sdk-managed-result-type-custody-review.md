# Agent SDK managed-result type/custody delta review

**Disposition: APPROVE.**

Reviewed exact commit `dad121f6bba9b3c9b8d3b2139230d785b7222fc9` / tree `9ef6e18ed86a7a141913fd413cca150d4c712a15` on `tl/agt-m4-mypy-sdk-managed-result-boundaries-0650`. The five-file diff is annotation-only except for the `create_timeline_view` key invariant assertion; source/candidate selection and final managed-result checks are unchanged.

The managed Scene path still rejects caller source/authority/certification inputs, selects saved/candidate captures through `prepare_filmstrip`, treats labels as comparison targets rather than authority, verifies managed/artifact digest and size, reads only the managed CAS bundle, validates its ZIP manifest and `scene-answers.json`, and converts stale/missing/mismatched results to advisory `UNAVAILABLE`. No caller JSON certifies a result. View creation remains an explicit write: `_typed` supplies a key, retries reuse the supplied original key, and a new logical `visualize(..., mode="inputs")` call gets a fresh key. Generated client, pin, schema, and DTO content are untouched.

Independent pure controls: **19 passed in 1.05s**. The worker's original evidence remains **16 passed, 2 existing skips** for source/candidate/Scene controls and **6 passed** for view retry/read-path controls. No actual capture, Node/native renderer, browser, full replay, or global typecheck was run. No missing proof or issue was identified in this type-only delta.
