# D118 corrected accounting handback

Task: `rt-D118-accounting-return-1005`  
Scope: the exact D54a 23-node upstream replacement set from the immutable 09:51 handback.  
Basis: independent checked map `rt-D118-result-review-1001.{md,json,tsv}`.  
Verdict: corrected accounting only; the independent review's `FAIL` means the original labels were wrong, not that the 09:51 upstream run was invalid.

## Corrected disposition

`PRE=0`, `REG=14`, `NEW-OURS=8`, `UNKN=1` (23 total).

The exact REG14 list is:

1. `tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_stops_on_correlated_terminal_registration_failure`
2. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-25-ready-True-25-None]`
3. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-None-ready-False-300.0-None]`
4. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-25-ready-True-25-None]`
5. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-120-None]`
6. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-terminal-False-1-None]`
7. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_pid-False-1-None]`
8. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_birth-False-1-None]`
9. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_instance-False-1-None]`
10. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_source-False-1-None]`
11. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-None]`
12. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-400-ready-True-400-400]`
13. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-150.3-30]`
14. `tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-30]`

All REG14 rows are current `failed` versus pristine-upstream `PASS`, with identical function bodies (`body_hash_equal=true`) and no approved changed purpose established. The changed-body bootstrap row is NEW-OURS on the approved current12/Remotion case-purpose basis. The seven source-absent rows are NEW-OURS. The remaining render row is UNKN.

## Preserved 09:51 run and provenance

- Exact set: 23 requested; 16 runnable upstream counterparts; 15 PASS, 1 FAIL, 0 ERROR; 7 source-absent. No exclusions, skips, xfails, timeout weakening, or body rerun were introduced by this accounting pass.
- Central test service: `rt-D118-upstream23-0951-d118-upstream23-targeted-1025095559-19404`; raw exit `1`; result `15 passed, 1 failed, 0 errors`.
- Final JUnit XML SHA-256: `84fcd41802112834d34164636d7ea5e59632826ae5e9e43bca45ac40a957ad12`.
- Earlier first-run JUnit XML SHA-256: `b7c68509b300bb94b3188d2b5cf3e0a0041a93f4a9adf07059d66cefae51d1a2`; its missing-`runtime_protocol` provenance failure remains retained and is not used for final classification.
- Pristine Agent source identity: head `08e6b905114a3ee2b05c3e7980421f26b4abf15c`, tree `2694ae8d2709526b40fa037bda8b159cf412769d`; current integration source file SHA-256 `08dfa8dcafeb80c347923630864a29d58dea97e257428e204fc316567795161b`, pristine counterpart `8143c3741b1024612c6cb8017d17ee83bd69d5fb64db31fff2d25b3bf0b05362`.
- Pristine Runtime source identity: head `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`, tree `1d3e06f4d59ed6d459646d24ab185c36eb5be075`. Child imported-module/find-spec origins resolved only to the pristine Agent/Runtime roots; the shared-venv probe was not admitted.
- The original 09:51 README, manifest, comparison, outcomes TSV, final XML, and first-run XML remain immutable. Their SHA-256 values, plus the independent review artifact hashes, are recorded in the corrected JSON.

## Unknown limits and non-actions

- UNKN is only `tests/packs/rendering/test_render_export_task_adapter.py::test_render_export_adapter_writes_real_mp4_and_is_callable`. The bodies match, but the current retained failure detail is absent while pristine upstream reports `RenderExportRefused` at line 109 with renderer status 1; current retained location is line 134. This is insufficient to call REG or PRE.
- Current exception class/detail is absent from the retained current handoff for every current failure; no detail was invented and no test body was rerun.
- Historical 924-runtime isolation remains UNCERTAIN and outside this exact 23-node scope. No broad 924, core-zero, or full-suite claim is made.
- This pass performed no semantic review, body/source audit, rerun, collector change, production/test/product edit, generated-file or pin operation, credential/hub operation, denied retry, or deletion. The original worker outputs were read-only inputs.

The machine-readable corrected artifact is `rt-D118-accounting-corrected-1005.json`; its integrity checks and exact-set hash are self-contained.
