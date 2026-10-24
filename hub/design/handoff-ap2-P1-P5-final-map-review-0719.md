# PASS — P1–P5 corrected map review

No source, test, generated, pin, suite, or Git changes.

- P1: mounted App gestures perform split/trim via `useTimelineSave → persisted outbox → RuntimeDataProvider.commitTimeline → generated client.commitTimeline → Runtime /v1/.../commit`. Agent supplies only the intervening label/move. Preserved accepted/merged/refused, lost-ACK retry, restart, canonical history, rollback, and no-legacy-write assertions.
- P2: eight original mounted cases remain mapped across the three P2 source files: element edit, registerAsset, automatic placement, popup ADD/SWAP, parent move, and single/bulk transition clears with field preservation, reload, and guarded Undo.
- P3: preserved Gate-5 case and reset-precondition source; current App runs `23809`/`9310` remain untouched.
- P4: SDK tests are support-only. Real service nodes are:
  - `test_cli_sheet_v2_runtime_preserves_document_and_reads_back`
  - `test_http_ten_note_commit_per_step_inverse_and_redo`
  - `test_http_note_conflict_reruns_public_function_from_verified_peer_document`

  Existing route: `request-test integration:agent p4-v2-http-nodes --files "<three exact nodes>"`.
- P5: exact historical qualification remains Runtime 14 integration nodes plus 24 crash nodes (`Runtime 62c454ac/tree b84e048`, Agent `f894c3c9/tree d24f25a`). Restore crash/idempotency coverage is genuine Runtime behavior, not App authoring authority.

The HOST/repo-key correction is valid: `request-test` accepts `integration:REPO` or worker metadata, and `test-run` resolves suites by repo key. Missing `app`-prefixed Python rows does not imply missing service capability.

Remaining qualification input: App service must provide the exact final Agent/Runtime checkouts, actual registration, authenticated child/import custody, and report-all preflight. No final tuple or READY route exists yet. D48/D49 venue remains unchanged: final P1–P5 reruns belong to App’s service.

Verification:

- `git diff --check HEAD` — PASS
- Worktree status — clean
- Source identity — App `66354161950d1e747965c095ea97b881d2592708`, tree `9a37265f0286128df7e6240a9df9877d959474af`
- No tests, browser, HTTP, socket, service, or `request-test` run, as required.
