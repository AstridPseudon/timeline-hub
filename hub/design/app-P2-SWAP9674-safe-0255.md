# P2 popup SWAP retained safe return

Read-only handback from the current D66 packet. No product or test files were changed.

## Proven facts

- Readiness passed: 1 test, 0 failures, exit 0.
- The page trace contains exactly two commit POSTs. The source flow proves the first is the popup SWAP A2 initial commit and the second is the native Undo inverse: `commitFromGesture` captures commit responses, `runPopupCase` performs SWAP, and `assertReloadUndo` clicks Undo before calling `accepted`.
- Initial SWAP: POST observed from `2026-10-25T02:40:46.359Z` through `2026-10-25T02:41:04.922371Z` (18,563.371 ms), HTTP 200, `{data, receipt}`, `data.status=accepted`; provider `astrid-v1` and compiler `authoring-bundle-1` are present. The pre-Undo reload/readback and selected-label assertions passed.
- Undo-intended POST: observed from `2026-10-25T02:41:16.044Z` through `2026-10-25T02:41:22.674725Z` (6,630.725 ms), HTTP 503, `code=not_ready`, `details.reason=runtime_unavailable`, and no receipt. The first failed predicate is `accepted(inverse)` at source line 495, called from line 902.
- Restored canonical and final-history assertions were not reached. Eventual Undo outcome is unknown.

## Runtime phase limits

`runtime-private/p2-commit-phase.jsonl` is schema version 1 with 128 events across request ordinals 1–3, counted 46/64/18. Ordinal-to-action correlation is unknown: the retained stream has no action labels or ordinal header. Ordinals 1 and 2 have HTTP-200 terminal events; ordinal 3 ends after provider start with no terminal event. Truncation is not declared, but the stream cannot close the Undo outcome.

## Safe artifact custody

The JSON companion contains SHA-256 and byte-size records for `manifest.json`, `readiness.xml`, `p2-popup-swap.xml`, `error-context.md`, and `trace.zip`, plus the source hash and redaction limits.

Raw authorization, request bodies, idempotency keys, URLs, project/timeline/revision/publication/receipt/request IDs, and private frame data are intentionally omitted. No proof closure is claimed.
