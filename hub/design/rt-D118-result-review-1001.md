# D118 independent D54a result/source classification review

Ask: independent read-only review of the exact D54a 23-node replacement scope.
Owner: Runtime worker rt-D118-result-review-1001.
By: 2026-10-25.

## Verdict

**FAIL — corrective classification required.** The upstream run itself is valid for the bounded scope: exactly 16 runnable counterparts, 15 PASS, 1 FAIL, 0 ERROR, plus 7 source-absent nodes. The author README incorrectly labels all 15 upstream-PASS/current-FAIL rows NEW-OURS.

Fourteen PASS-upstream rows have identical function bodies and the same scenario as current. With current recorded as failed and pristine upstream passed, and with no approved replacement or changed purpose established, they are REG. The one changed-body host row is NEW-OURS because its current12/Remotion registry-context read expectation is an approved replacement case. The render row is UNKN: its upstream failure is RenderExportRefused at test line 109 with renderer status 1, while the retained current failure is at test line 134 and has no retained exception class/detail.

| classification | count |
|---|---:|
| PRE | 0 |
| REG | 14 |
| NEW-OURS | 8 |
| UNKN | 1 |

## Provenance and run checks

- Pristine Agent: 08e6b905114a3ee2b05c3e7980421f26b4abf15c; tree 2694ae8d2709526b40fa037bda8b159cf412769d; clean.
- Pristine Runtime: d4f496ec4fbcae7a1f3a51d47ed5147c561117ad; tree 1d3e06f4d59ed6d459646d24ab185c36eb5be075; clean.
- Current review base was Runtime d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e; no product files were modified.
- Central result: rt-D118-upstream23-0951-d118-upstream23-targeted-1025095559-19404, raw exit 1, 15 passed, 1 failed, 0 errors.
- Final JUnit XML SHA-256: 84fcd41802112834d34164636d7ea5e59632826ae5e9e43bca45ac40a957ad12; first-run XML retained with SHA-256 b7c68509b300bb94b3188d2b5cf3e0a0041a93f4a9adf07059d66cefae51d1a2.
- Final child origins for astrid, astrid_runtime, astrid_runtime_client, runtime_protocol, runtime_protocol.canonical_schema, and runtime_protocol.contract_metadata resolve only under the pristine Agent/Runtime roots. The shared-venv probe records current integration modules as available but not admitted. The first-run missing-runtime_protocol failure is retained and excluded from final result classification.

## Corrected per-ID map

| ID | class | current | upstream | body equal | current location | upstream location | function/source basis |
|---|---|---|---|:---:|---|---|---|
| tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_passes_inventory_identity_and_restarts_on_change | **NEW-OURS** | failed | PASS | false | tests/sdk/test_host_bootstrap_source_identity.py:223 | tests/sdk/test_host_bootstrap_source_identity.py:218 | test_bootstrap_passes_inventory_identity_and_restarts_on_change / test_bootstrap_passes_inventory_identity_and_restarts_on_change; approved current12/Remotion body |
| tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_stops_on_correlated_terminal_registration_failure | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:363 | tests/sdk/test_host_bootstrap_source_identity.py:348 | test_bootstrap_stops_on_correlated_terminal_registration_failure / test_bootstrap_stops_on_correlated_terminal_registration_failure; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-25-ready-True-25-None] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:727 | tests/sdk/test_host_bootstrap_source_identity.py:636 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-None-ready-False-300.0-None] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:731 | tests/sdk/test_host_bootstrap_source_identity.py:640 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-25-ready-True-25-None] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:727 | tests/sdk/test_host_bootstrap_source_identity.py:636 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-120-None] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:731 | tests/sdk/test_host_bootstrap_source_identity.py:640 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-terminal-False-1-None] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:731 | tests/sdk/test_host_bootstrap_source_identity.py:640 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_pid-False-1-None] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:731 | tests/sdk/test_host_bootstrap_source_identity.py:640 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_birth-False-1-None] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:731 | tests/sdk/test_host_bootstrap_source_identity.py:640 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_instance-False-1-None] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:731 | tests/sdk/test_host_bootstrap_source_identity.py:640 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_source-False-1-None] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:731 | tests/sdk/test_host_bootstrap_source_identity.py:640 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-None] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:731 | tests/sdk/test_host_bootstrap_source_identity.py:640 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-400-ready-True-400-400] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:727 | tests/sdk/test_host_bootstrap_source_identity.py:636 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-150.3-30] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:731 | tests/sdk/test_host_bootstrap_source_identity.py:640 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-30] | **REG** | failed | PASS | true | tests/sdk/test_host_bootstrap_source_identity.py:731 | tests/sdk/test_host_bootstrap_source_identity.py:640 | test_startup_budget_polling_preserves_identity_and_original_cleanup / test_startup_budget_polling_preserves_identity_and_original_cleanup; exact body/function |
| tests/sdk/test_timeline_script.py::test_runtime_pin_flow_returns_old_script_after_binding_rebind | **NEW-OURS** | failed | ABSENT | false | tests/sdk/test_timeline_script.py:276 | — | test_runtime_pin_flow_returns_old_script_after_binding_rebind / test_runtime_pin_flow_returns_old_script_after_binding_rebind; no exact upstream body/function |
| tests/timeline/test_authoring_media.py::test_public_document_swap_and_residual_patch_use_original_sequential_closure[True] | **NEW-OURS** | failed | ABSENT | false | ../rt-pin-1daca2a3/runtime_protocol/service.py:2524 | — | test_public_document_swap_and_residual_patch_use_original_sequential_closure / absent; no exact upstream body/function |
| tests/timeline/test_authoring_media.py::test_public_document_swap_and_residual_patch_use_original_sequential_closure[False] | **NEW-OURS** | failed | ABSENT | false | ../rt-pin-1daca2a3/runtime_protocol/service.py:2524 | — | test_public_document_swap_and_residual_patch_use_original_sequential_closure / absent; no exact upstream body/function |
| tests/timeline/test_authoring_media.py::test_public_document_compound_inverse_restores_exact_original | **NEW-OURS** | failed | ABSENT | false | ../rt-pin-1daca2a3/runtime_protocol/service.py:2524 | — | test_public_document_compound_inverse_restores_exact_original / absent; no exact upstream body/function |
| tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba | **NEW-OURS** | failed | ABSENT | false | — | — | test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba / absent; no exact upstream body/function |
| tests/packs/rendering/test_render_export_task_adapter.py::test_render_export_adapter_writes_real_mp4_and_is_callable | **UNKN** | failed | FAIL | true | tests/packs/rendering/test_render_export_task_adapter.py:134 | tests/packs/rendering/test_render_export_task_adapter.py:109 | test_render_export_adapter_writes_real_mp4_and_is_callable / test_render_export_adapter_writes_real_mp4_and_is_callable; failure detail/location differ |
| tests/packs/rendering/test_render_export_task_adapter.py::test_forced_caption_uses_server_owned_executable_routing_and_isolation | **NEW-OURS** | failed | ABSENT | false | tests/packs/rendering/test_render_export_task_adapter.py:360 | — | test_forced_caption_uses_server_owned_executable_routing_and_isolation / test_forced_caption_uses_server_owned_executable_routing_and_isolation; no exact upstream body/function |
| tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight | **NEW-OURS** | failed | ABSENT | false | tests/packs/video_editing/test_runtime_publication_chain.py:676 | — | test_d13_installed_native_preflight / absent; no exact upstream body/function |

## Input limits and decisions

- Current exception class/detail is absent from the retained D54a current handoff for every current failure; the map records that absence rather than inventing an exception.
- Same-file proximity is not treated as scenario equivalence. The seven source-absent nodes, plus the changed-body current-only host row, are NEW-OURS.
- The render row is not promoted to REG or PRE; the exception/location mismatch leaves it UNKN.
- Historical 924-runtime isolation remains UNCERTAIN outside this exact 23-node scope. No claim is made that all 23 historical cases are resolved.

The complete hash/function/exception/location map is in design/rt-D118-result-review-1001.json; source-audit, comparison, XML, and provenance paths are retained in the D118 handback manifest.

