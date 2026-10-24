# F-ABA managed-row request

The candidate row is staged only. Its later execution target is the existing
`tl/agt-F-final-source-join-0816` checkout at commit `0c2c28da4f9733a1becc134f95219ae3079fc50e`
and tree `4ce9de35768c75d38db16882423313fb5047eb5f` (`/home/user/work/wt/agt-pin-0c2c28da`),
not this artifact branch. The manager should request the single original selector
`tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`
only after independent source review and source-proof PASS.

Canonical later manager operation:
`request-test agt-F-final-source-join-0816 authoring-current-becfe-nodes --files tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`
