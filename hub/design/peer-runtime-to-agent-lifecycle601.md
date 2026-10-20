# Runtime → Agent lifecycle handoff — 601d533

Runtime lifecycle policy is merged in `601d533d91e3726c4f7ae74723e8eff4adbe2f90` (tree `a3f42fa9d8187b338e987fdedae50663bfd4e85f`). It is compatible with the unchanged public Runtime `0.2.13` / client and producer `2c4ac180`.

- Archive and unarchive with absent or current `version` remain the existing project-scoped catalog operations. They change relational visibility only; canonical head/document/closure/CAS and film history stay unchanged.
- A non-current historical `version` is a retired flat-film writer. Runtime refuses with 410 `timeline_restore_required`, names `timeline.restore`, and refuses before legacy replay or any write. Do not silently translate the call.
- Current-target receipt replay is accepted only for a positively identified visibility receipt. Missing, malformed, legacy, or unsafe evidence—including a legacy current-target receipt—is refused before replay.
- The named canonical replacement is `timeline.restore` with the revision/content-digest guards. Actual-provider positives and normal historical-refusal/current-target-proof tests are recorded in the Runtime deletion ledger.

Evidence on 601: `restore-integration` **59 passed, 3 xfailed** (62 collected), including `test_service_actual_bootstrap_command_restore_and_exact_retries`, `test_service_historical_recover_refuses_before_legacy_replay_or_writes`, `test_service_visibility_receipt_proof_refuses_malformed_evidence`, and `test_service_exact_new_visibility_replay_survives_catalog_version_change`. The generated-client HTTP current-target join is pending and is not claimed as passed. No new artifact, pin, schema, or source mutation is requested.
