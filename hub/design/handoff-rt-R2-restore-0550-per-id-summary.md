# R2 restore finite handback

This is a derived, redacted handback from the completed central runs. It is
not a whole-proof approval. The original XML, logs, commands, request bodies,
credentials, URLs, and stack traces remain in the prior worker's private
evidence and are not copied here.

## Runs

| central ID | role | Agent provenance | Runtime provenance | result |
| --- | --- | --- | --- | --- |
| `rt-R2-restore-candidate-main-0525-r2-restore-oldred-overlay-0525-1025053322-31475` | baseline old-RED | commit `6cd767b6afd157b3f12e14dde5e9ef50dcb1f70a`, tree `2082bb633865cd504193efa58017b6eb17e555c1` | commit `0c62dfa63db9ff608ac9338388431e31a814e080`, tree `e22cdd54b668acea9fe593e6724b34d1a56f7530` | 1 failed, 3 passed, 1 error |
| `rt-R2-restore-candidate-main-0525-r2-restore-newgreen-preflightfix-0525-1025053518-30269` | candidate | commit `8aa672530c2ecf1a66dac2d8e38fc1e60262a8b1`, tree `531ae5d01d6dc817e13dbdb4f7f3a17644c3b4ce` | commit `0c62dfa63db9ff608ac9338388431e31a814e080`, tree `e22cdd54b668acea9fe593e6724b34d1a56f7530` | 4 passed, 1 error |

The baseline is the genuine parent checkout; the candidate is the genuine
reviewed Agent checkout. App commit `1e34f8eac5e3d5a54dbba12d538a7f3bf8509b66`
and Composition commit `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` are unchanged
across both runs. Runtime is the requested Base0c62. No retry or re-collection
is represented by this handback.

## Per-test outcomes

| selector (short form) | old-RED `...31475` | candidate `...30269` | first exception / sanitized location when non-pass |
| --- | --- | --- | --- |
| `test_id5_public_undo_of_restore_preserves_authenticated_effect_order` | FAIL | PASS | old-RED: `astrid.sdk.timeline.sync.CommitConflict`; `astrid/sdk/timeline/sync.py:556`, `_flush`, provider-response/conflict surfacing |
| `test_last_write_clear_undo_restore_and_restore_inverse` (historical ID5 setup control) | ERROR during setup | ERROR during setup | `astrid.sdk.timeline.emitter.DocumentPatchError`; `astrid/sdk/timeline/emitter.py:304`, `emit_document_commands`, retained-fixture setup; underlying `CommandError` at `astrid/sdk/timeline/_doc_patch.py:300`, `validate_payload`, contradictory-parent-mirror validation |
| `test_original_capture_claims_are_verified_before_refresh` | PASS | PASS | — |
| `test_reversed_inverse_target_order_is_refused_without_partial_acceptance` | PASS | PASS | — |
| `test_undo_detects_aba_and_unchanged_write_publications` | PASS | PASS | — |

The ID5 refusal's existing Runtime predicate is
`runtime_protocol/timeline_commit_auth.py:1495`,
`_inverse_stage_boundaries`, and the Agent `_flush` frame above is its
client-side surfacing point. The historical setup error is not attributed to
Runtime: its observed owner is the Agent emitter/validator setup path. No
common cause is inferred.

## Verdict

Candidate regression plus the three strict controls are finite PASS evidence
only. Because the unchanged historical setup control errors in both runs, the
five-selector run is not full GREEN and does not establish whole-proof R2.
The candidate remains unmerged/held pending an independently qualified or
repaired historical setup control.
