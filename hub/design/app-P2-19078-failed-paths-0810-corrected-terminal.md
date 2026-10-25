# Corrected terminal summary: actual19078

This summary is separately authored from the retained artifacts. The original producer note `early-P2-terminal.md` is preserved unchanged despite its arithmetic typo.

## Counts

- Readiness: **1 PASS / 1**, separate from the original tour.
- Original: **4 PASS / 2 FAIL / 1 ERROR / 1 NOTRUN**, exit 1.
- Overall service: **FAIL**. The four PASS cases are not independently re-verdicting here; they remain owned by the sole independent pass review. This summary does not call the service PASS or independent GO.

| Case | Result | First unmet predicate |
| --- | --- | --- |
| Popup ADD | PASS | — |
| Popup SWAP | FAIL | `three-products.p2-popup.spec.ts:495`: accepted response status 200; observed 409 `history_unavailable` |
| Parent move | PASS | — |
| Transition clear, single | PASS | — |
| Transition clear, bulk | PASS | — |
| Element apply | FAIL | `three-products.p2-elements-assets.spec.ts:1037`: dialog status did not contain `applied` within the existing 5s assertion |
| registerAsset | NOTRUN | Serially not run after an earlier failure |
| Automatic child placement | ERROR | `three-products.p2-elements-assets.spec.ts:1263`: commit response wait timed out at 90s; later page-close is teardown evidence |

## Finite source attribution

- **SWAP:** the popup action intends `occurrence.swap-media`; the retained popup trace proves a real POST with status 409 and reason `history_unavailable`. No accepted receipt, canonical outcome, or Undo request was observed. The one Runtime namespace with raised/409 phase ordinals is recorded in the JSON packet, but its correlation to SWAP is UNKNOWN.
- **Element:** the element action intends a `doc.patch`, but the completed request body operation is UNOBSERVED. Retained trace activity includes POSTs with incomplete status; do not infer no POST. The first missing seam is the UI `applied` status at line 1037, with no accepted receipt/reload/Undo outcome.
- **Placement:** the embedded-shot file drop intends `occurrence.add-media`. The retained path includes the placement trace’s POST activity, but no commit response was observed by the test. The first missing seam is the 90s response wait at line 1263; transport/server outcome, canonical reload, and guarded inverse outcome are UNKNOWN.

The full placement source chain is mounted gesture/capture → prepared task admission → persisted placement continuation → task poll/selected output → capture into A2 outbox → canonical Runtime commit → authoritative closure/history → reload → guarded `timeline.inverse`. Static source anchors and retained artifact hashes are in `notes/19078-failed-paths.json`.

## Diagnostic boundary

All six retained phase files and all six retained stderr files were searched. The final stderr’s bounded diagnostic is `catchall:runtime_protocol.errors.ProtocolError` with redacted frames `_lookup:215`, `evaluate:168`, `__enter__:141`, `_read_transaction:310`, `_store_version:265`. Namespace-to-gesture correlation is UNKNOWN for all three failures. No Runtime repair or waiver is justified by this packet.

## Readiness and next step

The packet is a new 19078 evidence handoff only. It does not grant final-tour credit or an independent GO. Runtime’s existing source owner should consume the bounded 409/pending seam; any Runtime code decision remains in the Runtime lane. A qualified final tour remains a separate future decision.
