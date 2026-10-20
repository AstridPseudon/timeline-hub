# WC4 original-pin final deletion gate

## Verdict

**APPROVE** candidate tree `cd13be81bf14c05e5acc7089a1e66d109000c61d` on
base commit `8e3107853d17453758a933d1f47215cc1c002660`.

The candidate has exactly the reviewed 20 paths (`+2299/-144`). The reviewed
authority implementation is byte-identical to `6868e16a590af64fc764159489b8e4ed22f526d`
for `_selected_param_authority.py` and `commit.py`. The helper files
`remote.py`, `_clip_scalar_commands.py`, and `_recording.py` are byte-identical
to `20f1b2902f7155cb271213abc184e5c2ec4aafd2`. The only additional product glue
is:

- request-local adaptation of authenticated public history and accepted
  canonical revision closures for the existing resolver;
- `ctx.prior_records` handoff and the existing staged-inverse guard composition;
- seven existing-generated-client facade lines for the two verified-document
  reads and their fixed operation allowlist.

There is no new authority store, cache, journal, validator, endpoint, DTO,
schema, generated client, or pin/lock change. The accepted legacy fixture is
unchanged (`accepted.zip` SHA256
`79f881f95ce13338ee8cd5490529c43a55523819792eed682160a9042770dc56`).

## Behavior reviewed

- Same-element HOLD does not reselect or read portable inputs.
- Changed/clear PARAM preserves the accepted P1 selection and exact P/E/O
  record; ordinary PARAM cannot bootstrap authority or use manifest order/current
  admission as an escape.
- P1 max-10 remains authoritative after P2 max-20 admission, source removal,
  restart, and paginated history: seed 16 refuses before POST/head/database
  writes; seed 8 and clear succeed. An intentional real revision reselection
  uses P2 and accepts 16.
- Digest-only legacy HOLD succeeds; a real legacy revision change visibly
  refuses with the existing re-admit message outside save.
- The authentic legacy-alias inverse positive retains its original selected
  identity, opaque data, object-read identity, inverse/redo, and retry claims.
- Exact pending body/key/base and acknowledged/rebased ACK history remain
  guarded. F1 earlier-staged-record strict inverse remains negative, while
  disjoint and reverse-order cases remain positive.

No old positive assertion was weakened, skipped, or converted to xfail. The
candidate has no new xfail/skip markers in the reviewed files.

## Evidence run

All candidate tests ran from private `git archive` copies; shared worktrees,
venvs, runtimes, fixtures, and caches were not modified. No full suite, browser,
socket, or App journey was run.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private-candidate> ASTRID_RUNTIME_CHECKOUT=<private-runtime> \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration \
  tests/core/test_timeline_element_publication_runtime.py::test_param_only_helper_preserves_original_pin_without_reselection \
  tests/core/test_timeline_element_publication_runtime.py::test_helper_retains_max10_after_max20_restart_and_explicit_revision_reselection \
  tests/core/test_timeline_element_publication_runtime.py::test_legacy_same_selected_hold_reload_inverse_retry \
  tests/core/test_timeline_element_publication_runtime.py::test_preexisting_element_hold_flight_retries_exact_body \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_pre_enforcement_alias_history_reopens_with_current_authority \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_native_inverse_refuses_earlier_unchanged_selection_atomically \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_native_disjoint_staged_label_and_inverse_preserve_opaque \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_native_inverse_then_selection_and_params_use_staged_pin \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_native_birth_without_selection_cannot_authorize_param \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_native_retained_schema_replay_inverse_reload_and_exact_retry \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_native_equal_json_opposite_selection_order_and_inverse_restore \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_native_rebase_after_v2_and_selection_removal_uses_original_object
25 passed in 28.50s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private-candidate> \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_selected_param_authority.py \
  tests/sdk/test_timeline_selected_schema.py::test_inverse_of_older_param_record_uses_only_selected_identity \
  tests/sdk/test_timeline_selected_schema.py::test_new_valid_selected_param_compiles_commits_reloads_and_roundtrips \
  tests/sdk/test_timeline_selected_schema.py::test_noop_declared_value_clear_and_opaque_values_preserve_literal_state
30 passed in 22.06s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private-candidate> \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/core/test_timeline_element_publication.py \
  tests/sdk/test_timeline_sync.py \
  tests/editing_conformance/test_recipe_clip_set_element.py
133 passed in 14.56s

/home/user/work/venv-agent/bin/ruff check --no-cache [all changed Python files except inherited remote.py]
All checks passed!

git diff --check 8e3107853d17453758a933d1f47215cc1c002660 \
  cd13be81bf14c05e5acc7089a1e66d109000c61d
passed
```

`remote.py` retains the base tree's 121 Ruff diagnostics byte-for-byte; it has
no new diagnostics. The integration branch at `6a6d92d3` and current Agent
integration head `725d335d` have no changed-path intersection with the 20
candidate paths. Their outside changes are the declared Scene/test-fixture
and rendering-service/window-input work.

## Old publisher deletion and replacement ledger IDs

The deleted path is the old `astrid/sdk/timeline_elements.py:update_parent_element`
whole-document publisher: `resolve_admitted_element` plus authoring
`validate_authoring_candidate`/`publish_authoring_candidate`, the local mirror
and legacy-app mutation, and the nested `Writer.publish_parent_composition`
call through `owner._typed('publish_parent_composition', ...)` (base lines
33-71). The candidate now stages native `clip.set-element`, `clip.set`, and
`clip.set-params` commands through the durable session and `/v1` commit.

Use these replacing test IDs in the manager ledger after merge:

- `tests/core/test_timeline_element_publication.py::test_sameclip_exacthead_publication_preserves_closure_and_user_params`
- `tests/core/test_timeline_element_publication.py::test_stale_head_and_concurrent_cas_reject_without_rebase`
- `tests/core/test_timeline_element_publication.py::test_bad_duration_never_publishes`
- `tests/core/test_timeline_element_publication.py::test_unadmitted_owner_and_sourceclip_reject`
- `tests/core/test_timeline_element_publication_runtime.py::test_public_helper_restart_exact_retry_later_head_inverse_redo`
- `tests/core/test_timeline_element_publication_runtime.py::test_public_helper_element_only_keeps_literal_params_and_exact_inverse`
- `tests/core/test_timeline_element_publication_runtime.py::test_public_helper_optional_session_rebases_over_disjoint_edit`
- `tests/core/test_timeline_element_publication_runtime.py::test_public_helper_scope_and_identity_refusal_is_atomic`
- `tests/core/test_timeline_element_publication_runtime.py::test_public_helper_native_refusal_preserves_error_and_flight`
- `tests/core/test_timeline_element_publication_runtime.py::test_param_only_helper_preserves_original_pin_without_reselection`
- `tests/core/test_timeline_element_publication_runtime.py::test_helper_retains_max10_after_max20_restart_and_explicit_revision_reselection`
- `tests/core/test_timeline_element_publication_runtime.py::test_helper_param_cannot_bootstrap_unselected_clip`

## Prerequisites / boundaries

1. Manager-controlled merge onto the current integration branch must preserve
   the empty path intersection verified above, then rerun the manager's normal
   post-merge targeted qualification.
2. Keep the existing F1 strict-inverse evidence attached to the Agent merge;
   this approval verifies its negative/disjoint/reverse composition, not a new
   Runtime or release-wide claim.
3. App authenticated provider, outbox, browser, and App journey qualification
   remains a separate gate. Renderer/pixel/audio, full-suite, `make check`, and
   macOS claims are not supplied here.
