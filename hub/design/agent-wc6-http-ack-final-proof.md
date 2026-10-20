# Agent WC6 real-HTTP acknowledgement proof

## Source and fault seam

- Owned source: `tests/timeline/test_authoring_media.py`,
  `test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`.
- The old `lose_undo_ack` called `RuntimeHandler._send` first and raised
  afterwards. That could write the response and made the synthetic fixture
  exception text an unreliable assertion across HTTP.
- The corrected seam matches the existing M1 convention. For the undo request
  it requires `POST`, `/commit`, status `200`, idempotency key `wc6-undo`, and
  Runtime's deferred-response state (`_defer_response`). At that point
  `commit_timeline` has returned its durable acceptance. The fixture records
  `_prefetched_body`, then raises before calling the original `_send`, so no
  HTTP response bytes are sent.

## Public transport and durability proof

- Request: `POST /v1/projects/<project>/timelines/film/commit` with
  `Idempotency-Key: wc6-undo` and the inverse command body.
- The client observes the documented public failure:
  `astrid.sdk.workspace_client.WorkspaceClientError`, `status == 0`,
  `code == "transport_error"`. The actual transport message is
  `Remote end closed connection without response`; synthetic server-fixture
  text is not asserted.
- The persisted outbox flight retains key `wc6-undo`; its serialized body is
  byte-equal to the first HTTP body. After restart, the retry is observed with
  the same key and byte-identical body.
- The retry returns the baseline canonical document and a receipt. The test
  asserts that receipt is the accepted publication, is the durable history
  head revision/publication pair, and is present in immutable history.
- Restart keeps the original HTTP port so the intentionally stale disjoint
  session remains bound to the same Runtime identity. The redo path re-reads
  the exact old/new Runtime-verified media inputs and passes them to capture;
  the F1 guard remains active.

## Limits and result

- Product code is unchanged from `841581fc`; only the owned test fixture and
  its proof assertions changed.
- No transport, scope, permission, marker, skip, normalization, fake session,
  or SQL changes were made. Existing raw alias/payload opaque fields, mirrors,
  selection, disjoint rebase, atomic negative, exact undo/retry, redo, and ABA
  assertions remain.
- No full suite was run. The required central run was:

  `native-script-current-integration --files tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`

  with pinned Runtime checkout `7f6dd89`; result run
  `agt-m2-wc6-http-ack-proof-finish-native-script-current-integration-1020150046-28371`:
  **1 passed in 14.35s**.

