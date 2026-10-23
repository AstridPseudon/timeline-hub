# G5 qualified join 1902

Status: candidate source preserved; SDKFOUR qualification FAIL (3/4); P1 NO-GO. No integration merge, activation, or source repair was performed.

## Exact source union

Base: `tl/agt-G5-docs-1847`, `003013fa13e992d5c5232bc4621597778b9c393d`.

Imported exact blobs:

| source | path | resulting blob |
|---|---|---|
| `255751f40a38263b8a032d15b807a3a3e2742a9c` | `astrid/sdk/timeline/_step_undo.py` | `db1dd6cc09a6f9b7cf59f8af9e49cdb9d682eb74` |
| `255751f40a38263b8a032d15b807a3a3e2742a9c` | `astrid/sdk/timeline/inverse.py` | `1b551173ebdf7a31a012573a92a02190918218ca` |
| `255751f40a38263b8a032d15b807a3a3e2742a9c` | `tests/editing_conformance/test_inverse_aba_partition.py` | `0c23acf7599509d325c09afe02256eebe4ff50a6` |
| `255751f40a38263b8a032d15b807a3a3e2742a9c` | `tests/editing_conformance/test_nested_inverse_order.py` | `264a0b336a67e21afacb1d4f93f81e482589638d` |
| `255751f40a38263b8a032d15b807a3a3e2742a9c` | `tests/editing_conformance/test_nested_native_aggregate_partition.py` | `7bff6baef0e5c1559a401a4e812dc50756b07fae` |
| `255751f40a38263b8a032d15b807a3a3e2742a9c` | `tests/editing_conformance/test_nested_parent_mirror_ranges.py` | `d8ccb0d5db11e8645768ed683494f270292a55aa` |
| `d146b4204f6f9efa526134d810e581a282377a9a` | `astrid/sdk/timeline/_root_inverse.py` | `30f6d7803e1a76ecdcda1daf3c6d8496c7ea4d57` |
| `d146b4204f6f9efa526134d810e581a282377a9a` | `tests/editing_conformance/test_transient_root_baseline.py` | `abfc95afc351957fb19789900d4c9e01392bc963` |

The d146 report path was intentionally excluded; the brief requested only the product module and test path. `git status` showed exactly these eight paths. Outside them, base `003013fa1` is unchanged; the existing G5 retirement draft, `store.py` (75f), `_commit_patch.py` (R1 f078), `runtime.lock.json`, and frozen 34e/d106/819acf references were preserved.

## Tests and checks

- Pre-body joined guard: `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=<worktree>:<runtime> /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_transient_root_baseline.py::test_native_stage_keeps_authored_root_and_full_accepted_baseline` — **23 passed**.
- Adapted report-all/trivial boot using observer SHA `d8964223d0ffbdead0ebb6035ee98941dfa55363a9477d18d9201e02f2b2b986` and archive `g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz` — **PASS**; archive hash matched, body locks matched, credential findings `[]`.
- Unchanged FOUR, run once with the exact requested integration command and Runtime `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`: **1 passed, 3 failed**. Failures: `test_checkout_reload_undo_cli_redo_uses_retained_history`, `test_retained_restore_does_not_reopen_consumed_draft_steps`, and `test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore`. Each failed at ordinary `TimelineSession.move` with Runtime `internal_error`; no retry or assertion/body change. Observed owner boundary is the Runtime commit execution path; causal Runtime traceback was not exposed by the public error.
- Scoped Ruff on all eight paths — **PASS**. Scoped mypy on all eight paths — **PASS** (`Success: no issues found in 8 source files`).
- Ratchets — **PASS**, Ruff `2148 = 2148`, mypy `1911 = 1911`.
- `scripts/vendor_lock.py check runtime.lock.json` — **PASS**. `scripts/artifact_manifest.py --check` — **PASS**. `git diff --check` — **PASS**.

## Evidence and limits

Evidence is under the worker evidence directory. `observer-boot.json` SHA256 is `e423929eae0abbb146fbf90fdcf7c3758869e868f2b4d86bca54eca296236a65`; final `report-all.json` SHA256 is `ac2538825a06acb1bbd123f892b1f285c4e12ac2badc5b0c2f96ea72f64b2452`. All four original function body locks matched their required hashes. The observer did not create per-case packets because the failing request executes in the Runtime subprocess; therefore full private capture, source-history packet, and per-case before/after origin packet are unavailable and are not claimed. The pytest temp outboxes remain in the harness `$TMPDIR`; their hashes were recorded in the worker log.

No C0 request/reply shape, provider guard, Runtime auth, schema, pin, environment, or original test body was modified. The production caller remains the ordinary SDK checkout/free-edit/publisher/restore/undo/redo normal commit path. Independent ABA1852 remains the owner of cumulative security review; this candidate result must not be merged if that review fails.
