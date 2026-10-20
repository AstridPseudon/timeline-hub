# Agent private952 HTTP result

## Qualification

PASS — exact manager-requested pair `28209`, and only that pair.

- Agent source: `909bfad8f9ae22d3e4b0dbb83fdcc07bcf1169c` / tree `3775e2e00c9e45999f6c0277f4dbc323079749b0`
- Runtime: `rt-pin-95202c2b` (tree `d438d3e2…`)
- Result folder: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-private952-http-reload-finish-private952-sockets-integration-1020193342-28209`
- Exact result: `44 passed in 55.07s`, exit `0`

## Original assertions

All passed; no successful node was rerun.

- `test_native_sheet_current_runtime.py::test_http_semantic_batch_original_pins_reload_inverse_redo`: `4/4` (`python`, `cli`, `sheet-python`, `sheet-cli`). Original pins, semantic payload, canonical lifecycle, reload, inverse/undo, and redo assertions passed.
- `test_native_sheet_current_runtime.py::test_http_sheet_lost_ack_restart_exact_retry_original_guards_and_aba`: `1/1`. Lost-ACK acceptance, durable restart recovery, exact retry identity/body, no recapture, original guards, and A→B→A guarded-undo refusal passed.
- `test_native_batch_ingress.py`: `40/40`. Accepted-v1 raw/captured batch publication, reload, inverse/redo, lost-ACK/restart exact retry, dependent suffix, ABA/delete-recreate, original-pair pinning, atomic refusal, boolean/numeric retry identity, explicit pin/parser, preview, and concurrent-ACK assertions all passed.

## Scope

The predecessor's bounded `astrid/sdk/remote.py` canonical-image conversion is validated by this pair. It canonicalizes only the reloaded source closure through existing image fieldsets; raw GET rows, payloads, pins, ordering, identities, opaque data, and history remain preserved. No further source/test fix is needed.

This is private native HTTP evidence only. It does not adopt public013/ordinary014, mutate private357/613 or Runtime952 health/artifact/rawbundle inputs, refresh captures, create fake history, or establish a full-suite, browser, public-release, or integration claim. The transport and command records remain the existing `workspace.v1` / schema-version-1 path; no separate v2 wire-protocol run is claimed.

Use this result for the private RT08 replacement qualification only. Keep pin adoption and public/integration claims separate.
