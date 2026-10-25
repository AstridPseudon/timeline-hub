# D115 independent protected PURPOSE review

Verdict: **PASS_SOURCE** for the fixture-purpose disposition. This is not a
functional PASS and does not authorize changing the 17 exact-missing cases.

## Finding

The authored 27-row map is source-accurate. The D108b 2016-result outcome table
contains all 27 exact ordinals, with exact node-id matches and `error` outcome
for each. The ten rows marked `d107_exact_approved` are an exact selector-set
match to the ten-row D107 predicate TSV; the remaining seventeen are not added
to D107.

The shared Runtime path is real and common:

`tests/editing_conformance/test_commit_runtime_m1.py:34-56` →
`tests/timeline_commit_film_fixture.py:28-44` →
`tests/precut_realm_fixture.py:46-176` → committed `precut-v31` archive.

The archive has the retained transcript, text-binding, media, reference,
publication and receipt rows, but its historical timeline
`dependency_manifest.documents` is empty. The M1 setup then authors the
legacy `word:word-1` declaration. The failure is therefore an intentionally
authored historical unpinned input, not a setup generator dropping an
authenticated document pin. I found no evidence for a generator pin-loss
cause, and no generic legacy retirement is justified.

The actual current producer citation is Agent
`tests/editing_conformance/native_word_anchor_fixture.py:69-116`, consumed by
`tests/editing_conformance/test_timing_retained_inputs.py:129-146`: it creates
the transcript through Runtime, commits a current anchor with an explicit
document pin, then clears that authored choice. This is a valid existing
current construction, but D107’s `test_m1_current_equivalent.py` candidate is
not in the current Agent `tl/integration` worktree. The ten-case current route
is consequently source-approved/behavior-pending, not functionally proven by
this review.

## Exact disposition

The ten D107-approved selectors remain exactly the ten M1 selectors in the
map (ordinals 1085, 1091, 1100, 1106, 1112, 1116, 1121, 1126, 1131, 1138).
Their existing replacement citations are the D107 current predicate TSV and
PASS_SOURCE review, paired with the real current producer route above and the
existing legacy-archive read proof. This review does not claim those current
tests have run or merged.

The exact-safe 17 subset remains `legacy_only_exact_missing`:

- Native checkout (4): 1143 move/trim lost-ACK; 1147 touching-peer move/trim;
  1152 attached parameter CLI ingress/history; 1159 authenticated v1
  commit/reload/undo with renderer stopped.
- Native frontends (3): 1165 and 1171 sheet lost-ACK/attached-suffix guard
  variants; 1180 checkout-first sheet refusal and draft preservation.
- Owned move (6): 2913 parent asset clear; 2923 parent transition clear;
  2927 parent trim stale rebase; 2940 parent split stale rebase; 2958
  parent delete stale rebase; 2996 ambiguous owner/mixed edits.
- Parent-track-related (2 + 1 batch): 3651 parent label after move; 3653
  native label then Python suffix; 3649 grouped parent-track create/move
  batch inverse.
- Scalar (1): 3654 move then scalar outbox handoff/inverse.

Exact selector IDs for that 17-row subset are:

```text
1143 tests/editing_conformance/test_commit_runtime_native_checkout.py::test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[False]
1147 tests/editing_conformance/test_commit_runtime_native_checkout.py::test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[True]
1152 tests/editing_conformance/test_commit_runtime_native_checkout.py::test_attached_param_commands_keep_exact_cli_ingress_and_unchanged_write_history
1159 tests/editing_conformance/test_commit_runtime_native_checkout.py::test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable
1165 tests/editing_conformance/test_commit_runtime_native_frontends.py::test_sheet_lost_ack_attached_suffix_restart_exact_retry_and_peer_guards[False]
1171 tests/editing_conformance/test_commit_runtime_native_frontends.py::test_sheet_lost_ack_attached_suffix_restart_exact_retry_and_peer_guards[True]
1180 tests/editing_conformance/test_commit_runtime_native_frontends.py::test_checkout_first_refuses_sheet_suffix_keeps_draft_and_pending_intent
2913 tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_asset_clear_lost_ack_reload_retry_undo
2923 tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_transition_clear_lost_ack_reload_retry_undo
2927 tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_trim_stale_rebase_lost_ack_reload_retry_undo
2940 tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_split_stale_rebase_lost_ack_reload_retry_undo
2958 tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_delete_stale_rebase_lost_ack_reload_retry_undo
2996 tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_ambiguous_owner_and_mixed_edits_keep_original_draft
3649 tests/editing_conformance/test_commit_runtime_parent_track_batch_inverse.py::test_grouped_parent_track_create_move_reload_undo_redo
3651 tests/editing_conformance/test_commit_runtime_parent_track_label.py::test_move_then_parent_label_reload_inverse_preserves_newer_disjoint_move
3653 tests/editing_conformance/test_commit_runtime_parent_track_label.py::test_native_label_cli_lost_ack_then_python_suffix_keeps_original_claims
3654 tests/editing_conformance/test_commit_runtime_scalar.py::test_move_then_scalar_outbox_handoff_reload_and_guarded_inverse
```

The full selector names and purposes remain in
[`rt-D115-fixture-purpose-0934.exactsafeIDmap.json`](rt-D115-fixture-purpose-0934.exactsafeIDmap.json);
the grouping above is only a safe coverage summary, not a family-level
replacement claim.

## Minimum remaining-coverage question

Owner decision required before any extension: “Which of these exact 17
selectors, if any, must receive current success, and what exact current
producer/anchor choice is authorized for each?” If the answer is yes, perform
a new selector-specific source review using the existing pinned current
producer route, retain each original predicate and legacy read, and obtain
independent functional proof. Do not rewrite the shared pre-cut fixture,
author pins, add guards, or retire all legacy cases by family.

No source, test, generated file, pin, registry, archive, SQL, collector,
body, or Runtime contract change was made. C0 request/reply semantics
(including request base/commands/label/steps/patch/reads/merge/key,
accepted/merged canonical receipt/head/effects/bindings/dependencies,
conflict/invalid and dry-run behavior) remain unchanged.
