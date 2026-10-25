# D134 selected-schema independent review

## Verdict: FAIL_SOURCE_CONTROL_DRIFT

The four-file scope is one file, and the seven UNKNOWN node inputs/bodies remain byte-for-byte unchanged. The blocking issue is the three supposedly new-v2 stale-base requests: their original source is API v1/native and omits all v2 control fields. Adding `label`, `merge`, and `reads` changes protected authored input and request identity, then makes the status assertions pass under a newly selected request class. C0 preserves omitted-control ABI-1 callers and reserves `merged` for genuinely new v2 landings; it does not authorize rewriting an existing caller body merely to update the expected status.

The replacement for the retired publisher is source-consistent at the payload level: it registers the existing provider, uses the canonical commit route, performs a guarded root `doc.patch`, deep-copies the exact pristine parent payload, and asserts the accepted payload is unchanged. The HTTP lost-ACK/restart/pin/dynamic-base behavior remains unverified because the central route failed before collection. No body was run after the source verdict failed.

## Findings

1. `v2_request` at lines 415–417 changes the original request controls created by `case.request` at lines 174–178. Restore the original bodies unless an approved D50/D120 principle authorizes this exact C0 correction.
2. The three `rebased`→`merged` assertions at lines 768 and 1001 are not independently justified after the body mutation. Keep genuine new-v2 coverage separate from these ABI-1 original-purpose cases.
3. The HTTP node is unqualified, not passed or failed: central precollection failed, and the task forbids hidden retries or fixture workarounds.
4. The setup is not source-exact: the old authored payload omitted `config.clips`, while the new bootstrap baseline supplies `config.clips: []`. The new self-equality assertion proves only the changed baseline, not equivalence to the retired setup. Preserve the old payload shape before any body rerun.

## Conserved scope

- Only `tests/sdk/test_timeline_selected_schema_runtime.py` differs from base.
- The seven UNKNOWN node bodies are exact: `test_pre_enforcement_alias_history_reopens_with_current_authority`, `test_mixed_pack_readmission_keeps_old_and_new_native_param_sources`, `test_native_disjoint_staged_label_and_inverse_preserve_opaque[False]`, `test_native_disjoint_staged_label_and_inverse_preserve_opaque[True]`, `test_native_inverse_then_selection_and_params_use_staged_pin`, `test_native_equal_json_opposite_selection_order_and_inverse_restore`, and `test_native_retained_schema_replay_inverse_reload_and_exact_retry`.
- Their source hashes and assertion counts are recorded in `predicate-map.json`.
