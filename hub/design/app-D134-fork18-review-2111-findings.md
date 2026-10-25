# D134 root-008 independent review

Result: **FAIL**. This is an evidence-quality failure, not proof of a product defect. The source author correctly left the two owned files unchanged and did not establish a faithful ABI-1-preserving caller correction, but two wholepath evidence defects prevent a PASS_FINITE_UNAPPLIED verdict.

## F-001 — exact member index is not byte-exact to root-008

`evidence/predicate-map.json` claims an `exact_member_index` for all 18 root-008 members, but every indexed `nodeid` omits the `tests/editing_conformance/` path prefix. The authoritative cluster JSON uses full node IDs such as `tests/editing_conformance/test_fork_abi1_binding_set.py::...`, and the map's separate `cases` entries use that full form. Independent set comparison is therefore raw unequal: 18 cluster members missing and 18 abbreviated entries extra. After adding the omitted prefix, the sets agree. The count and source files are right; the exact index is not.

## F-002 — registered-caller trace stops before the Runtime authority seam

The author maps `registered_caller` to `tests/editing_conformance/test_doc_patch_v2.py:45-50`, which is the local `submit` helper and Agent provider call, but does not bind the actual Runtime registration/acceptance path. The current source binds Runtime's trusted loader at `runtime_protocol/timeline_commit_provider.py:70-90` to `astrid.sdk.timeline.commit.create_runtime_commit_service`; Runtime acceptance derives authenticated `recorder_abi` from accepted physical bindings at `runtime_protocol/timeline_commit_store.py:1832-1853` and persists it through `_publish` at `:2058-2082`. This omission matters because the failing historical payload is not available in the retained evidence. The author must scope the caller conclusion to the two owned tests and retain the missing Runtime record/closure evidence as the outside-file seam.

## Finite causal conclusion

The owned test source explicitly preserves the ABI-1 request omission (`test_fork_abi1_binding_set.py:95-96`), while the current v2 comparator adds `label`, `merge`, `reads`, `steps`, source, rationale and group controls (`test_provider_occurrence_fork.py:27-29`). `CommitPatch.v2` is selected by those controls (`astrid/sdk/timeline/_commit_patch.py:277-295`); v2 enrichment adds physical binding fields (`:493-501`). Replacing the ABI-1 omission with the comparator setup would therefore change the request mode, authenticated binding shape, and history predicate. It is not a faithful correction for the ABI-1, malformed-recorder, caller-annotation, or history-purpose cases.

The current Agent history guard accepts a complete legacy four-binding set only when authenticated `recorder_abi` is not 2 (`astrid/sdk/timeline/commit.py:884-905`), and Runtime supplies that authority from the accepted record rather than caller annotations (`:1005-1020`; Runtime `timeline_commit_store.py:1851-1853`). The retained failure contains only the first Agent frame and a log hash, not the authenticated record, predecessor closure, output closure, or boundary fields needed to distinguish a malformed historical payload from a provider defect. The exact smallest proved owner/seam is therefore Agent provider / Runtime producer-history custody; classification remains UNKNOWN_UNAPPLIED, with no product-fault or retirement credit.

Original fork, reload, undo, redo, replay, ABA, surviving-owner, and malformed-recorder purposes remain source-conserved because both owned files are byte-identical to base and their function ASTs are unchanged. No body, replay, collection, service, socket, browser, or full suite was run.
