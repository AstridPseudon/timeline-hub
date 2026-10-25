## FAIL_SOURCE

F-D85 scalar11/F-D86 protected review is held. No source changes were made.

Blocking finding:

- `tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py:36` calls `value_at(root, path)` with 2 positional arguments.
- `astrid/sdk/timeline/_doc_patch.py:79` defines `value_at(root, ref, path)` with 3 required arguments.
- The first `_patch` call in the seed therefore has a statically provable arity failure. Runtime bootstrap, provider registration, `commit_timeline`, accepted history, receipts, idempotency, inverse/ABA, and ABI behavior receive no functional credit.

Static conservation:

- Original parameterization, assertions, `pytest.raises`, branches, loops, and scalar/compound/separate paths remain.
- Canonical selectors remain:
  - `CHILD = occurrence:f2-occurrence/clip:f2-agent-clip`
  - `CLEAR = occurrence:f2-occurrence/clip:f2-agent-clear-clip`
  - `PARENT = parent/clip:f2-transition-clip`
- The seed statically constructs the full v2 envelope and 11 runtime command instances: parent patches, occurrence creation/placement, track creation, internal/shot revision patches, and final occurrence membership.
- Required unresolved seam: static review cannot prove accepted occurrence membership/order, physical identities, created claims, dependency records, or provider-authored history because execution is prohibited and the seed fails earlier.

Checks:

- `git diff --check HEAD^ HEAD` — PASS
- Candidate Ruff — PASS
- Parent Ruff via stdin — PASS
- Candidate mypy — PASS
- Parent mypy via `--shadow-file` — PASS
- AST-only conservation/API inspection — conservation PASS; `value_at` arity check FAIL
- No pytest, collection, helper/function, service, browser, or full-suite execution.

Source identity: HEAD `f2def38890237646943fdad185d0b21d1d7f9938`; parent `993e1e9d98463a1bfa35c611d45dd7b21e32e783`; candidate blob `851949c2bfa9df355e38d055f674bbba1e113331`.

Evidence was recorded under the worker evidence directory. Commit message and `DONE` marker were created. Recommended next step: return the exact arity defect to the normal Agent queue; do not merge this review-only branch.