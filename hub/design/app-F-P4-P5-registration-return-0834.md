## Result: PREPARED, not READY

Corrected the two review findings without modifying App source, suites, kit, locks, generated files, design docs, or registrations. The old draft remains preserved.

### Exact future rows

```text
agent p4-v2-http-nodes env -u PYTHONPATH -u PYTHONUSERBASE -u PYTHONHOME -u PYTHONNOUSERSITE bash -c '<inline fail-fast guard>; exec "$CHILD_PYTHON" -I -P -m pytest -q -m integration "$@"' -- 
runtime first-capture-integration env -u PYTHONPATH -u PYTHONUSERBASE -u PYTHONHOME -u PYTHONNOUSERSITE bash -c '<same inline fail-fast guard>; exec "$CHILD_PYTHON" -I -P -m pytest -q -m integration tests/test_timeline_commit_integration.py'
runtime marked-integration env -u PYTHONPATH -u PYTHONUSERBASE -u PYTHONHOME -u PYTHONNOUSERSITE bash -c '<same inline fail-fast guard>; exec "$CHILD_PYTHON" -I -P -m pytest -q -m integration "$@"' --
```

Requests:

```text
request-test integration:agent p4-v2-http-nodes --files "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document"

request-test integration:runtime first-capture-integration
request-test integration:runtime marked-integration --files tests/test_timeline_commit_crash.py
```

The guard requires exact Agent/App/Runtime SHA, tree, parent, clean-checkout, child, backend, client, graph, receipt, and import-origin values; verifies receipt/report hashes and markers; then invokes only the authenticated child with `-I -P`. Missing or malformed values fail before pytest/import/body execution. No generic source-precedence `PYTHONPATH` overlay remains.

### Validation

- Corrected guard `bash -n` — PASS
- Provenance Python compile — PASS
- Mock `integration:agent` dispatch: argc 4 and quoted `--files` — PASS
- Missing, malformed, incorrect-target, and malformed child-receipt refusals — PASS; fake pytest marker was not reached
- `git diff --check HEAD` — PASS
- Worktree clean

P4 remains exactly 3 nodes. P5 remains 14 integration plus 24 crash cases; original 52 cases and P3 reset precondition retained. Existing `commit-integration` retained.

### Remaining inputs

Final Agent/App tuples, authenticated child and graph receipts, and final installed origins remain unavailable. Known Runtime producer metadata remains `becfe6db…` / tree `7edc08…`; no final qualification is claimed. All four artifact mappings remain recorded: three match, while generated contract metadata is stale; no compatibility credit.

No tests, collection, import, backend, HTTP, install, provisioning, registration, service request, or full suite was run.

Commit message written; empty `DONE` marker created.