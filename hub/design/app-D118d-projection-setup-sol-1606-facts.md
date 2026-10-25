# D118d setup correction — static PASS, own9 NOTRUN

Only `tests/sdk/test_timeline_capture_projection.py` changed from exact base `e02180cedafa581bc8105d77341456b8b1c50b5b` (+17/-1). Original source is `20177e66564f9f91735ed1a11bac821682d60edf`.

The first correction obtains `revision_id` from `source_mapping.shots[authoring_shot_id]`, where `open_authoring_bundle` places the genuine immutable source identity. The authoring shot contains editable payload/baseline/internal fields, not that pin. The guarded source-item command otherwise retains its exact previous value, item/media values, step, scope reads, base pair, idempotency and authorization path.

The complete caller trace also exposed a later requirement: `authoring_commit_request::_read_base` loads the authenticated persisted source, and `_materialize_duplicates` compares the duplicate's supplied baselines against a copy of that source. The original fixture authors opaque source fields locally and copies them into duplicate baselines. Those fields must therefore become genuine accepted source history first. The added setup publishes the already-authored source through the existing `publish_authoring_candidate` / registered Runtime `commit_timeline` route, then rereads the accepted exact closure before the original baseline assignments and duplication. It does not inject recorder facts or modify authored values.

The Runtime route validates request/scope/path and calls the registered provider through `CommitExecutionCoordinator`. Provider `doc.patch` checks exact previous values, physical bindings and media provenance; Runtime verifies and persists the resulting canonical closure and durable receipt. The genuine current `read_document` canonical field tuples equal `_saved_document` exactly. Saved/candidate projection readers and the original complete expansion, opaque payload, pin, read-row, order and six candidate opener checks remain in place.

Source conservation PASS: all 43 original assertion ASTs are preserved; all 11 test-function ASTs (including decorators and parameters) equal original20177 and basee02180c; every original fixture statement survives in order. No authored input/golden/pin/topology/assertion was edited. The only extra assertion is the previously existing accepted-setup check (44 total before/after this continuation). Every other repository path is unchanged. Upstream `92443771676ef2bbb547d0a103d708fa8bec4c63` lacks the target file.

Runtime remains clean at `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree `de2954a0ceadb4455903d9abdfec3b773318a50f`. SHA-256 hashes of the changed file and traced reader/provider/caller files are in `source-custody.json` and were checked again at completion.

Ruff, mypy, py_compile, git diff --check and source/hash/AST/no-change checks PASS.

Own9 NOTRUN: fresh free space 4,987,809,792 bytes; required 5,000,000,000; exact shortfall 12,190,208 bytes. No floor bypass, cleanup, substitution or pytest dispatch occurred; no XML/log was produced. The original nine-node selection and complete command argv/environment are in `facts.json`.

No current product blocker is established by this source-only result. Actual arrival at the nine original assertions is unverified. Next owner: D118d orchestrator/protected reviewer; keep source held and execute the exact nine against the same clean pin once disk permits, then independently review. No full/family/service/browser/native/acquisition or held SWAP action was taken.
