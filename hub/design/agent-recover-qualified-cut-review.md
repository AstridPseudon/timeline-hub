# Agent recover qualified-cut review

## Verdict

**HOLD / REJECT the exact tree `7d9860fc43940a1e0bb6e6d9820d1909869e14c2`** against the actual merge base `f82da322077ed0ac0c58966a0815b5ffc02fc0cc`. The review found one blocking, directly reproducible regression in a touched unit lane. No product files were changed by this review.

## Blocking defect

`astrid/sdk/timeline/sync.py:363-368` converts a `WorkspaceClientError` with `code == "transport_error"` into a bare `ConnectionError` only when the request contains `timeline.restore`. This is a silent public transport-error translation and breaks the existing stable `WorkspaceClient` error contract. The durable flight is still retained before the exception, so this is not evidence of lost data, but the touched test suite is red and callers now receive a different exception for the same ambiguous transport state.

The exact failure is:

```text
tests/sdk/test_timeline_sync.py::test_restore_lost_ack_retries_exact_request_after_reload
E   ConnectionError: response lost after acceptance
```

The unchanged assertion at `tests/sdk/test_timeline_sync.py:226` expects `WorkspaceClientError`, matching the ordinary commit path. Remove the restore-only translation (and keep the exact in-flight body/key) or obtain an explicit contract decision before changing the existing assertion. This review does not approve rewriting that passing behavior test to accommodate the new exception type.

## Scope and conversion checks

- `RemoteTimelines.recover` now resolves through the canonical list, forwards the listed `timeline_id`, preserves caller `expected_version`/`version`, and forwards the idempotency key. It does not silently translate a historical request into `timeline.restore`.
- Catalog visibility remains outside film history: the real-HTTP test compares the accepted history before/after catalog archive/recover, checks stale CAS and wrong-project refusal, and verifies the fresh old-flat request is a visible 410 naming `timeline.restore`.
- The latest test captures `archive_again_version` as a scalar before the next archive (`tests/sdk/test_timeline_checkout_history_runtime.py:302`), so its replay CAS is not an alias through a later mutable response. The exact accepted catalog replay is exercised after the catalog version advances.
- `TimelineSession.restore` records a sole native `timeline.restore` command with both `revision_id` and `content_digest`; the native unit tests cover exact request shape, durable flight persistence, reload retry, and key/body equality. The real-HTTP test covers pending-intent refusal and final retry receipt.
- Closure/CAS/history/draft/retry coverage is otherwise mapped one-to-one in the converted test: snapshot closure (parent, child shot/internal revisions, media headers), catalog CAS/refusal, unchanged commit history, consumed-draft undo/redo behavior, and exact retry identity are retained.

One non-blocking coverage weakness remains: after the final native restore, the real-HTTP test asserts only the restored parent row (`tests/sdk/test_timeline_checkout_history_runtime.py:389-391`), not the complete canonical document/child/media closure. The Runtime candidate's corresponding original integration test compares the full restored canonical document to the retained `before` closure. The Agent test's earlier `afcb326c` form also used the parent-only assertion, so this is reported as a recommended strengthening rather than a newly introduced product-loss claim.

## Evidence

Review tree and base:

- Source: `tl/agt-m2-recover-current-server-final-gate`, `7d9860fc43940a1e0bb6e6d9820d1909869e14c2`
- Actual merge base: `f82da322077ed0ac0c58966a0815b5ffc02fc0cc`
- Runtime qualification pin in the test: `3b900c377e7126e14eeb92dc2ce73114cbda5a0e`

Commands:

- `pytest -q tests/sdk/test_native_timeline_facades.py tests/sdk/test_timeline_sync.py tests/v10/test_domain_cli_projects_timelines.py` — **189 passed, 1 skipped, 1 failed** (the restore lost-ack exception mismatch above).
- `git diff --check f82da322..HEAD` — passed.
- The supplied prior qualification for `test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore` is **1 passed in 7.27s** against Runtime `3b900c3`; I did not rerun the live HTTP test per the no-duplicate-live-run instruction.

## Merge-forward overlap

`53af5383` integration has one overlapping file: `astrid/sdk/timeline/sync.py`. Its WC7 changes add `explicit_outbox` handling in `open` and `_flush(..., prepare=...)`; preserve those hunks when resolving this cut. The recover branch's restore method and transport handling must be reconciled manually. Do not copy either branch's whole file over the other. The other integration changes (`generic_host.py`, Remotion root preparation, native checkout, and their tests) do not overlap this delta.

Recommended next steps: resolve the transport exception contract and rerun the three-file targeted command; then strengthen the real-HTTP final restore assertion to compare the complete retained closure if full closure preservation is required at this gate. No full/browser/live suite was run.
