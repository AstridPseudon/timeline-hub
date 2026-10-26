# D141k independent join review

Result: `PASS_EVIDENCE`.

The completed join is mechanically correct for the bound freeze-1 evidence. It does not qualify behavior, REG/non-REG, Farm completion, or shipping.

## Findings and limits

1. `D141K-LIMIT-001` — `LIMITATION`, non-blocking. The join source manifest recorded Agent `INBOX.md` at dispatch/publication (`2,087,990` bytes, SHA-256 `cf16627f29e9f56b904fb54a33adb2a8a77541946848b5b5d7d82f7dc06f5842`). The current latest INBOX is `2,090,050` bytes, SHA-256 `ee2c97e8ee27712926ec1019501ac1d38586ba756732b6abb4c4a63e48c8f631`; its mtime is after the join manifest. The old snapshot is not reconstructible from the mutable path. This is disclosed custody scope, not evidence that the join consumed a later decision.

## Independent accounting

- Actual XML `7adf18d3a9cd20c2198d4cd4ccd7e0be59497e6111a73284c4977fe31b92b25d` parses to 9,388 unique concrete testcase IDs: 8,988 PASS, 204 FAIL, 196 ERROR, 0 SKIP.
- Declared `9561` and raw summary `173` aggregate PASS members reconcile as `9561 = 9388 + 173` and `9161 PASS = 8988 + 173`. The original `FAIL_CUSTODY_DISCREPANCY` remains unchanged; no aggregate IDs were invented.
- Pristine table `7535b9a70b0da2f36e2c9e2f0115cf70ef429d3b8152496a7f44a723033ae6a5` contains 3,082 unique concrete IDs plus 173 unnamed aggregate PASS members: 3,077 PASS, 4 FAIL, 1 ERROR.
- Concrete identity multiset reconciliation is `3,018` matched, `6,370` cut-only, `64` pristine-only, with zero duplicates. Missing exact IDs remain UNKNOWN or N/A; no implicit pass/non-REG was inferred.

## Every joined candidate

All 17 candidates are exact concrete IDs with cut non-PASS and same-kind pristine PASS. Every row has an explicit `env_sensitive_undecidable` value and reason.

### `root-043` / `tests/sdk` — 15 candidates, `env_sensitive_undecidable=y`

Reason for all 15: host-bootstrap/source-identity failure with XML evidence reporting registry discovery/original wait exit; venv-agent cannot decide matching host custody. Conditional matched-kind Farm analysis only.

- `tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_passes_inventory_identity_and_restarts_on_change`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_stops_on_correlated_terminal_registration_failure`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-25-ready-True-25-None]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-None-ready-False-300.0-None]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-25-ready-True-25-None]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-120-None]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-terminal-False-1-None]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_pid-False-1-None]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_birth-False-1-None]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_instance-False-1-None]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_source-False-1-None]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-None]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-400-ready-True-400-400]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-150.3-30]`
- `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-30]`

### `root-007` / `tests/timeline` — 2 candidates, `env_sensitive_undecidable=n`

Reason for both: exact same-kind pristine PASS and retained cut failure is not a host-sensitive class.

- `tests/timeline/test_authoring_feedback.py::test_document_publish_stdout_and_durable_receipt_contain_shared_feedback`
- `tests/timeline/test_authoring_media.py::test_document_publish_forwards_new_stale_head_to_runtime`

### Supporting `FAILS_BOTH` measurements — 4 rows, not candidates

All four are explicit `env_sensitive_undecidable=y`, with no hidden environment or product claim:

- `tests/packs/rendering/test_render_export_task_adapter.py::test_render_export_adapter_writes_real_mp4_and_is_callable` — `root-040`, import/runtime-publication environment class.
- `tests/packs/rendering/test_render_export_task_adapter.py::test_forced_caption_uses_server_owned_executable_routing_and_isolation` — `root-002`, site/generated-registry environment class.
- `tests/packs/rendering/test_live_scene_composition.py::test_real_render_scene_window_audio_and_overlay` — `root-040`, site/registry environment class.
- `tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render` — `root-002`, import/runtime-publication environment class.

Three current non-PASS IDs under the five project-only roots are `N_A`, not candidates. The remaining 376 current non-PASS rows are `UNKNOWN` because no exact pristine ID exists. Historical 370/52 and media48 material is supporting mapping only; it did not supply current outcomes.

## Source and custody

- Actual source-before and source-after are byte-identical and clean; interpreter/settings/tuple match the bound D141i record.
- The original service `24049` is a refusal before body (`exit 78`, no XML/outcomes), and was excluded.
- The new review trace is a genuine foreground 5-second trace with five one-second samples, 4,194,304 KiB virtual-memory limit, and minimum free bytes `4,662,452,224`, above the 4,000,000,000-byte stop.

No pytest, collection, product import, provider, typecheck, lint, body, retry, or product investigation was run. No product tree or original evidence was changed.
