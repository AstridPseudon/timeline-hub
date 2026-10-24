## Report

Prepared a read-only DRAFT for the missing App-host registrations. No repository, suite, lock, generated, pin, ledger, design, or source files changed.

Draft rows:

```text
agent p4-v2-http-nodes env ASTRID_CHECKOUT=<FINAL_AGENT_CHECKOUT> ASTRID_RUNTIME_CHECKOUT=<FINAL_RUNTIME_CHECKOUT> PYTHONPATH=$PWD:<FINAL_AGENT_CHECKOUT> <AUTHENTIC_CHILD_PYTHON> -m pytest -q -m integration
```

Request with exactly:

```text
request-test integration:agent p4-v2-http-nodes --files "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document"
```

```text
runtime first-capture-integration env ASTRID_CHECKOUT=<FINAL_AGENT_CHECKOUT> PYTHONPATH=$PWD:<FINAL_AGENT_CHECKOUT> <AUTHENTIC_CHILD_PYTHON> -m pytest -q -m integration tests/test_timeline_commit_integration.py
runtime marked-integration env ASTRID_CHECKOUT=<FINAL_AGENT_CHECKOUT> PYTHONPATH=$PWD:<FINAL_AGENT_CHECKOUT> <AUTHENTIC_CHILD_PYTHON> -m pytest -q -m integration
```

The crash request must use:

```text
request-test integration:runtime marked-integration --files tests/test_timeline_commit_crash.py
```

Existing `runtime commit-integration` was preserved.

Counts verified by AST without test collection:

- P4: 3 exact nodes.
- Runtime integration: 14 expanded cases.
- Crash coverage: 24 cases.
- Original total: 52 cases plus the P3 reset precondition.

Mandatory final tuple remains:

```text
FINAL_AGENT_SHA/TREE/PARENTS: missing
FINAL_APP_SHA/TREE/PARENTS: missing
FINAL_RUNTIME_SHA: becfe6db88b2cc034dba3fafa6c050117cdf2b06
FINAL_RUNTIME_TREE: 7edc08e3fe94edcbc8ef695c479f4de301789b89
FINAL_RUNTIME_PARENTS: 46eb068c5adf663270512aca8a4bdd62c1488e6d c021f13afb655225570e3f0323f00a55132e8643
```

Runtime producer inventory is authentic: 79 artifacts, schema digest `sha256:4118b1…`, manifest/version hashes retained, and prior result `409 passed`.

All four Runtime→App mappings were checked. Three match; `generated-contract-metadata.ts` is stale. No compatibility credit is claimed.

Pre-install requirements remain: final clean Agent/App/Runtime checkouts and parent identities, Agent re-vendoring from Runtime `becfe…`, authenticated child/client/backend import-origin receipts, authenticated Remotion graph receipt with approved template and lock digest, and same-run report-all/fail-fast preflight. Placeholders must fail before execution.

Validation:

- `bash -n` on `test-run`, `request-test`, `request-child-venv`, `request-runtime` — PASS
- `node --check scripts/vendor-lock.mjs` — PASS
- Read-only AST node/count audit — PASS
- Four-artifact hash audit — PASS with expected metadata mismatch
- `git diff --check HEAD` — PASS
- Worktree clean
- No tests, service requests, installs, registrations, HTTP/browser runs, or full suites executed per task constraints

Harness markers written: `commit-msg` and empty `DONE`.