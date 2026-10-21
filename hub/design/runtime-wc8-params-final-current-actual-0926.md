# WC8 opaque-parameter final current actual proof

## Result

PASS. The approved current-preserving WC8 opaque-parameter proof is ready for manager HOME merge after this worker exits. No merge was requested while the worktree is uncommitted.

## Source and allowlist

- Current base: `c4b964f6a050edf63a4278d35717e46a88a80386`, tree `d7796be264c341adbcb9765aae374b832dede144`.
- Captured R4/current comparison base: `b8bbb5cf1d7f64b6a51e762ef394c4278b3e5492`.
- Oracle source: `tl/rt-m2-wc8-params-current-oracle-port-0920`, tip `a1f0b196e5364d25581d062b60ef4ed19a6e3def`.
- Ported only the three feature paths from `b8bbb5cf1..tl/rt-m2-wc8-params-current-oracle-port-0920`:
  `astrid/sdk/timeline_sheet.py`, `tests/sdk/test_timeline_sheet_native.py`, and `tests/editing_conformance/test_native_sheet_ordinary_runtime.py`.
- Final blobs exactly match the oracle for all three paths:
  - `timeline_sheet.py`: `6ae8d494d6684a9706ef533f825d419f34bf8d42`
  - `test_timeline_sheet_native.py`: `ced2be78f65d48028061fd0c1cd8a3cf604d495f`
  - `test_native_sheet_ordinary_runtime.py`: `f561128f89b756eb3c624264a81a0e1402032872`
- The reviewed new test node AST is byte-equivalent to the oracle node. No outside path changed; the three pre-existing integration-base rendering paths remain intact.

## Preflight

The consolidated read-only preflight passed for public producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, all 76 Runtime artifacts, ordinary `6ba` contract, Composition C13 installed package `0.0.13`, Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d` / tree `6abc2f117391de8e7e35c0283f575a002199894d`, imports, source/client paths, selector, private temp, disk, and service argv. The preflight also verified the current-base allowlist and retained current rendering changes.

## Tests

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet_native.py tests/editing_conformance/test_native_sheet_current.py` — **111 passed in 13.07s**.
- `... pytest -q -o addopts= -p no:cacheprovider --collect-only -m integration tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_opaque_null_rename_uses_retained_basis_and_guarded_http` — **1 test collected in 1.34s**.
- Central request `rt-m2-wc8-params-final-current-actual-0926-rt-wc8-current14-integration-1021092844-24222`, suite `rt-wc8-current14-integration`, exact new-node selector only — **1 passed in 4.45s**, exit 0.
- Central snapshot tree: `f5ca8f0d5779d57d0cc6a0cd953bc32e2e5d3064`.

The proof preserves rename revision/data, records redo as a new publication with the expected `previous` and `undo_of` history edge, snapshots post-redo head/history/request count, and rejects the stale original `NativeSheet.native.text` without outbox mutation, HTTP calls, or accepted writes. Explicit opaque clear remains unrepresentable by the detached grammar and is not claimed.

## Decisions and limits

The current base differed from the oracle, so the feature delta was ported in three allowlisted hunks only; no bulk overwrite was used. The product remains the approved `c0671afddb34f4fe6b8ca66f511df9fc530cc344` behavior, and the reviewed corrected test blob is retained exactly. No schema, pin, private017, marker, unrelated current behavior, full suite, browser, renderer, install, direct socket, or other passing-node replay was run. The prior two fixture/oracle failures were treated as diagnosed prerequisites; this was the one authorized final actual run.

Recommended next step: after harness commit, manager may perform the remote HOME merge gate using the recorded snapshot/tree and central result.

