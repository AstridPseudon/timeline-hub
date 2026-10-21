# Runtime WC8 current-preserving oracle correction — 2026-10-21

Status: **READY**. The diagnosed test-only correction is applied and verified,
and the independent assertion review `rt-m2-wc8-params-final-oracle-review-0920`
has terminally APPROVED the exact reviewed test blob. No final actual or
remote HOME merge is submitted by this worker; the manager may authorize the
single final actual on the committed current successor.

## Exact source and tree

- Current staging/base: `ab12f5457cb0ca1253873806187dd2508391c7dc`, tree
  `0bf2e698b0668e4f3fbfdf1f507aacc9619806b9`.
- Diagnosed correction parent: `33f88975eea0006a624c5e0a95bd2fd307695028`,
  tree `45a46eeda044f33c99f0fb118cc6cd0da373d5dd`.
- Reviewed correction: `5c00518939fdfe8f064a9713a9a91ea2746513fe`, tree
  `254d2e975ef06b14214db08ebb439a579042e926`.
- Approved product source: `c0671afddb34f4fe6b8ca66f511df9fc530cc344`.

The final new-test blob is exactly the reviewed blob
`f561128f89b756eb3c624264a81a0e1402032872`.

## Three-path allowlist and preservation check

The inherited current port's complete three-path allowlist is:

1. `astrid/sdk/timeline_sheet.py` — blob
   `6ae8d494d6684a9706ef533f825d419f34bf8d42`;
2. `tests/sdk/test_timeline_sheet_native.py` — blob
   `ced2be78f65d48028061fd0c1cd8a3cf604d495f`;
3. `tests/editing_conformance/test_native_sheet_ordinary_runtime.py` — the
   diagnosed new actual test, now reviewed blob
   `f561128f89b756eb3c624264a81a0e1402032872` (prior current blob
   `5bf1c4da617de0d172749a934b5bdc58ef8f1e4f`).

The first two blobs are byte-identical to both current staging `ab12f5457`
and approved product `c0671afdd`. The only worktree path changed from current
staging is the third path. The outside-allowlist tracked-blob check is clean:
`git diff --name-status HEAD --` reports only that third path, and
`git diff --check` passes. Existing HOME `b8bbb5cf1` preservation checks,
public95 checks, and C13 references remain untouched. The correction replaces
only the diagnosed final-head oracle with a full pre/post history snapshot and
adds redo publication ancestry checks.

## Author, review, and actual scope

- Correction author/source: commit `5c0051893` (authored `Claude`), ported
  without product changes or bulk file copying.
- Independent review: `rt-m2-wc8-params-final-oracle-review-0920` APPROVE for
  exact blob `f561128f89b756eb3c624264a81a0e1402032872` (SHA-256
  `e001ccb91bc88807e77a86e753ff90713698b5ad85e2c4811398f61df112cad4`). The
  review verified the new publication/history edge, original basis/native
  witness, outbox/history preservation, and no-HTTP stale refusal; it found
  no smallest correction.
- Actual scope: no HTTP/integration execution, full suite, render, browser,
  install, pin, schema, or product run was made. The manager may authorize one
  final actual only after the exact independent APPROVE and on the committed
  current successor.

## Evidence

Direct permitted neighbors:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
tests/sdk/test_timeline_sheet_native.py \
tests/editing_conformance/test_native_sheet_current.py
111 passed in 13.50s
```

Corrected-node collection (no test execution):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
-p no:cacheprovider --collect-only -m integration \
tests/editing_conformance/test_native_sheet_ordinary_runtime.py::\
test_current014_detached_opaque_null_rename_uses_retained_basis_and_guarded_http
1 test collected in 1.28s
```

The repository-default collection was first filtered by `not integration` and
reported zero selected nodes; it was not an execution. The explicit marker
collection above is the valid node-count evidence.

The prior corrected actual remains the known held failure: redo publishes the
same revision with a new publication identity, so the old equality oracle was
wrong. This worker did not replay it or submit a new actual.
