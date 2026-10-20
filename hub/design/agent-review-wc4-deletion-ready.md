# WC4 deletion gate: approved

Reviewed candidate `e36b505656f5b98c8bab3495c38f5d04fe8fbee5` (`tl/agt-m2-wc4-original-pin-current-join`), parent `4ef1391c2c104d5d11b3a27265035c51be296045`, tree `cd13be81bf14c05e5acc7089a1e66d109000c61d`, against current root `8e3107853d17453758a933d1f47215cc1c002660`.

## Verdict

Approve merge and mark the WC4 helper deletion row `DELETED`, with the permanent tests retained. The old whole-parent publisher path is actually removed from the public helper, not bypassed:

- The parent version imported `validate_authoring_candidate`/`publish_authoring_candidate`, built a whole candidate, and called `owner._typed('publish_parent_composition', ...)` through a local `Writer`. Candidate `astrid/sdk/timeline_elements.py:1-254` has none of those imports, symbols, or calls.
- The candidate helper builds only `clip.set-element`, `clip.set`, and `clip.set-params` calls, stages them in the existing `TimelineSession`, and completes through `session.flush()` (`timeline_elements.py:240-243`). No publisher fallback remains in that route.
- The only public consumer route is preserved: `RemoteTimelines.update_parent_element` forwards the existing arguments plus additive `session`/`clear_params` (`astrid/sdk/remote.py:1260-1262`); the CLI still calls that method with the old argument shape (`astrid/packs/timeline/cli.py:1287-1293`). `_result` retains the old `project_id`, `timeline_id`, `expected_head`, `new_head`, `clip_id`, `element`, `duration`, `params`, `before`, receipt, and idempotency-key result fields.
- The resulting write route is the existing outbox `TimelineSession.flush` to `client.timelines.commit` (`astrid/sdk/timeline/sync.py:306-368`), i.e. the existing `/v1` timeline commit path. Remaining `publish_parent_composition` references are separate bootstrap/migration/legacy APIs and are not reachable from this helper.

## Semantic checks

- Same-element PARAM/clear emits no artificial `clip.set-element`; it resolves the accepted original P/E/O through `_selected_param_authority.resolve_selected_param_source` and the existing authenticated history/retained-document/object reads (`timeline_elements.py:204-220`). The max10 P1 → max20 P2/removal/restart case preserves P1; refusal cases produce no POST/head/database write. A real E revision change takes the explicit `clip.set-element` path and current authenticated admission (`timeline_elements.py:221-238`).
- Same-element HOLD takes only guarded `clip.set` and does not invoke selection resolution, schema/object reads, local portable authority, or re-admission. The legacy digest-only positive remains successful; missing portable data still refuses the real revision-reselection path with the existing `pack snapshot unavailable; re-admit pack` error.
- The shared authority helper is the single resolver; no second history algorithm, validator, endpoint, DTO, persistence cache, journal, schema, or generated-pin change was introduced. Source ownership is guarded by existing element identity/pack-owner checks (`timeline_elements.py:192-201`); an actually admitted foreign owner cannot overwrite the selected product.
- Pending exact body/key and acknowledged recovery preserve the original request base, including rebased acceptance, lost acknowledgement, restart, pagination, and newer disjoint head. Bool/number intent remains distinct while numeric equivalence remains accepted. Opaque fields, raw aliases, mirrors/order, registry, transcript, shot/internal data, and old return compatibility remain covered.
- Authentic old legacy-alias inverse positives and F1 staged-inverse atomic refusal/valid staged-selection cases pass. No passing behavior test was weakened, skipped, deleted, or changed to expect refusal.

## Independent targeted evidence

Tests ran from a private archive of the exact candidate SHA using the shared read-only Agent venv and Runtime locator; no source or dependency files were modified.

```text
tests/core/test_timeline_element_publication.py
38 passed in 14.56s

tests/core/test_timeline_element_publication_runtime.py -k
  public_helper_restart_exact_retry_later_head_inverse_redo
  legacy_same_selected_hold_reload_inverse_retry
  param_only_helper_preserves_original_pin_without_reselection
  helper_retains_max10_after_max20_restart_and_explicit_revision_reselection
  helper_param_cannot_bootstrap_unselected_clip
  acknowledged_rebased_lost_ack_restart_pagination_and_typed_intent
  preexisting_element_hold_flight_retries_exact_body
19 passed, 40 deselected in 29.70s

tests/sdk/test_timeline_selected_param_authority.py -k
  equal_json_opposite_pin_order_has_distinct_accepted_authority
  unchanged_param_and_clear_record_exact_source
  disjoint_peer_and_paginated_reload_preserve_direct_source
  inverse_consumed_pin_is_not_restored_authority
  param_after_inverse_uses_original_target_before_selection
  legacy_unchanged_param_requires_selection_authority
  param_cannot_bootstrap_selected_authority
  inconsistent_or_incomplete_history_never_resurrects_older_pin
17 passed, 10 deselected in 11.26s

tests/sdk/test_timeline_selected_schema_runtime.py -k
  native_inverse_refuses_earlier_unchanged_selection_atomically
  native_disjoint_staged_label_and_inverse_preserve_opaque
  native_inverse_then_selection_and_params_use_staged_pin
5 passed, 27 deselected in 8.33s

tests/core/test_timeline_element_publication_runtime.py -k
  another_actually_admitted_owner_cannot_replace_selected_owner
1 passed, 58 deselected in 2.44s

ruff check --no-cache [changed helper/authority/command/facade/test paths]
All checks passed!
git diff --check 4ef1391c..e36b5056
passed
```

No full suite, `make check`, App/current public browser, renderer/audio/pixel, or macOS gate was run or claimed. This is a source/helper WC4 deletion approval only; those other product gates remain with their owners.

