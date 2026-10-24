## D43 Runtime accounting

Result: **25 of the original 36 failures remain open; 11 are closed.**

Baseline `runtime-full-1024005856-29085`:

- Runtime `458595850c`, tree `703b1aac`
- `6479 passed, 36 failed, 26 skipped, 15 xfailed, 0 errors, 0 XPASS`
- External tuple: Agent `b61cebe8`, App `7135ac72`, Composition `635f4de0`

Current integrated source: Runtime `36760ee0ad4b`, tree `11389911c2e`.

### Closed: 11 nodes

| Original nodes | Proof / integrated head | Current body/source |
|---|---|---|
| `test_artifact_manifest.py::test_committed_artifact_manifest_is_current` | `runtime-R0-manifest-integrated-0128`; `db11ea829`, tree `a92a576a` | Exact manifest test/body retained; current source blob `2fff9a4c`. Runtime R0 owner. |
| `test_recorded_responses.py::test_rerecording_is_byte_identical_to_committed_responses` | `runtime-D39-D40-integrated-0246`; `f3208b26b`, tree `c4bcf929`; 162 passed | Same byte-identity predicate retained; response cases truthfully migrated to `retired_route_410` and `commit_conflict_409`. Current blob `297b8813`. Runtime R5/conformance. |
| `test_recorded_responses.py::test_unnormalized_bodies_satisfy_their_contract_schema[publish_conflict_409]` | Same D39 proof | Closed through the required semantic migration: canonical `commit_conflict_409` preserves the 409 conflict body, while the retired route is explicitly 410. The original parameter name is no longer present. |
| `test_spec_reference.py::test_parent_receipt_compaction_preserves_publication_integrity` | `runtime-R5-receipt-integrated-0157`; `28bb65668`, tree `a952265a`; 2 passed | Original receipt/replay/compaction predicates retained on authenticated commit path. Current blob `7a4d8e83`. |
| `test_stage1_runtime_contract_completion.py::test_http_target_mutations_require_idempotency_key` | Same receipt proof | Original key/no-write predicates retained, with current commit and retired-route checks. Current blob `2856cab5`. |
| Six speed nodes: `None`, `speed1`, `3/2` × `child`, `parent` | `R5-full-speed` review/current port; integrated Runtime `28bb65668`, tree `a952265a`; 14-case proof | All six original inputs and SQL/CAS no-write assertions retained. Current blob `be5e7c9f`. |

### Still open: 25 unchanged selectors

No integrated proof on `36760` exists for either family. Later source/static evidence is not credited as closure.

**Headless overwrite — 10 nodes**

Proof/source evidence: `runtime-headless-effect-review-0349` / held source `ddaa6aed`; not an ancestor of `36760`. Current test body remains unchanged from the original census, blob `aa7756ba`.

Remaining cause: Agent authoritative mirror-effect recording loses the root `clips` removal in `_commit_patch.py`; owner **Agent R1/G4**.

- `test_empty_default_over_authored_headless_shell_is_refused_untouched`
- `test_empty_default_over_empty_headless_shell_is_refused_untouched`
- `test_empty_default_on_a_fresh_timeline_is_accepted_and_replays`
- `test_empty_parent_over_hidden_nonempty_content_of_a_headless_timeline_is_refused_untouched`
- `test_genuinely_empty_headless_timeline_still_accepts_expected_head_null`
- `test_cas_correct_republish_after_reading_the_head_is_accepted`
- `test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[timeline_references]`
- `test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[timeline_shots]`
- `test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[snapshot]`
- `test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[dependency]`

**Legacy occupancy — 15 nodes**

Proof/source evidence: `runtime-occupancy-faithful-review-0317`, prepared static source `3441bc34`; not an ancestor of `36760`. Current test body remains unchanged, blob `0ef27428`.

Remaining cause: Agent lacks the authenticated cross-timeline historical physical-shot/pin carrier required by the original reuse cases; owner **Agent G4**. Runtime’s authentication seam is qualified, but the original integrated behavior is not.

- `test_legacy_publication_refuses_unrelated_destination_before_any_write[False-False]`
- `test_legacy_publication_refuses_unrelated_destination_before_any_write[False-True]`
- `test_legacy_publication_refuses_unrelated_destination_before_any_write[True-False]`
- `test_legacy_publication_refuses_unrelated_destination_before_any_write[True-True]`
- `test_exact_f1_over_http`
- `test_legacy_occupied_destination_without_shot_head_is_not_adopted[False]`
- `test_legacy_occupied_destination_without_shot_head_is_not_adopted[True]`
- `test_legacy_current_closure_update_and_exact_retry_precede_live_checks`
- `test_legacy_current_destination_requires_verified_current_closure[receipt]`
- `test_legacy_current_destination_requires_verified_current_closure[occurrence]`
- `test_legacy_current_destination_requires_verified_current_closure[digest]`
- `test_legacy_current_destination_requires_verified_current_closure[projection]`
- `test_legacy_current_destination_requires_verified_current_closure[removed]`
- `test_legacy_historical_reuse_keeps_newer_global_shot_head[False]`
- `test_legacy_historical_reuse_keeps_newer_global_shot_head[True]`

Configured exclusions and different Agent/source pins were not used to claim closure. No full suite or tests were run. `git diff --check` passed; worktree is clean. No product, test, generated, client, pin, or artifact changes were made. Commit message and `DONE` marker were written.