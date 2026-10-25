# Runtime P2 SWAP 3250 bounded diagnostic

Date: 2026-10-25
Runtime worktree: `/home/user/work/wt/rt-P2-SWAP-3250-tags-1426`
Base: `453b3e6f92045980219ec4948419ee5ad25c817d`

## Result

The Runtime diagnostic candidate is implemented and source-backed. The mounted
HTTP caller scopes its public request id around the existing service call. The
existing private execution `request_id` remains independently generated. A
private diagnostic may now contain only `public_request_id_hash`, a bounded
SHA-256 value of the validated public id. The public response header/body,
strict `CommitContext`, accepted records, payloads, hashes, and provider
context are unchanged. No raw public id is logged.

An unattributed provider failure whose existing refusal reason is
`history_unavailable` is tagged `provider_history_guard`. Existing Runtime
store, port, and reference-projection tags are preserved; no guard was relaxed.
Provider failures already carrying a fixed Runtime source tag are not
overwritten.

## Public/private id mapping

`RuntimeHandler._request_id()` reads the validated `X-Request-ID` or generates
the public id; `_send()` returns that same value in the response header/body
error path. `RuntimeService._execute_timeline_commit()` separately creates the
private local `request_id` used by the diagnostic emitter. The handler's
`public_request_id_scope()` connects the two only in the private diagnostic,
one way and by hash. The service call shape remains compatible with existing
mounted callers and test doubles.

The observed production prefixes `20ef9f38` (local log) and `61c84a4e`
(SWAP public response) are therefore not treated as equal or correlated by
prefix. A same-run correlation is established only if the emitted private
`public_request_id_hash` equals SHA-256 of the retained public id.

## Fixed refusal emitter map

Provider ownership boundary: Agent `astrid/sdk/timeline/commit.py`,
`RuntimeTimelineCommitProvider.commit()` at line 1160 and its authenticated
history reads/guards at lines 669-685, 701, 783, 947, 964, 1019, 1275-1278,
and 1367 (plus the imported timeline helper modules). Agent does not expose a
Runtime source tag, so the Runtime provider boundary assigns
`provider_history_guard` only to an otherwise untagged `history_unavailable`
provider refusal. The provider's original failure envelope is retained.

Runtime store tags (31 direct guards plus two reference-projection guards):

```
store_membership_missing
store_head_missing
store_head_revision_mismatch
store_head_canonical_mismatch
store_head_catalog_corrupt
store_archived_scope_missing
store_history_entry_missing
store_history_ledger_mismatch
store_history_bound_revision_mismatch
store_history_bound_order_invalid
store_history_chain_break
store_history_through_mismatch
store_revision_scope_missing
store_revision_missing
store_revision_dependency_missing
store_shot_input_closure_ambiguous
store_shot_parent_missing
store_occurrence_rows_mismatch
store_occurrence_row_mismatch
store_dependency_rows_mismatch
store_shot_revision_scope_missing
store_history_ancestry_cycle
store_history_base_outside_ancestry
store_inverse_stage_targets_unavailable
store_request_base_mismatch
store_adopt_existing_head
store_adopt_nonempty_scope
store_adopt_existing_parent
store_adopt_legacy_shell_mismatch
store_adopt_prior_publication
store_bootstrap_unpublished_head
store_reference_projection_prepare_history
store_reference_projection_apply_history
```

Runtime port tags:

```
port_ancestor_pin_mismatch
port_ancestor_outside_request
port_history_bounds_mismatch
port_revision_outside_ancestry
port_base_pins_mismatch
port_candidate_head_unobserved
```

Source says a first SWAP at `base == current` can refuse at provider history
capture/replay, any of the store ancestry/closure/head guards above, port
ancestry/bounds guards, or reference projection prepare/apply history. Which
one is first for App 3250 cannot be proved from this source map; the retained
request and same-run facts are required. All of those refusals remain
fail-closed.

## Native proof boundary

No native 5e9ad replay was run. The retained App submission identifies the
single legitimate tuple `App fe3309db / Agent 070dfc / Runtime 5e9ad /
Composition 635f` and submission id
`app-pin-fe3309db-d73-p2-fe3309db-submit-1025140943-3250`, but the requested
safe packet `design/app-D127-full-P2-3250-terminal-1421-facts.json` is absent
from the shared design directory. Current free space is 4.6 GB, below the
5 GB native admission requirement. No body, provider profile, registry,
acquisition, private auth, raw stack, or substitute request was created.

The exact native request body/acceptance command is therefore a retained-input
dependency, not something this worker can safely reconstruct. Next command is
the existing native harness invocation using that exact submission id and the
packet's retained body, on Runtime `5e9ad1c6f7` with Agent `070dfc...`, after
the harness reports ordinary light admission at or above 5 GB. If the packet
is not published, report the missing retained request source rather than call
it a replay. Do not use the old 19078/15203 material.

## Verification

Passed:

* targeted diagnostics/routes/execution/store/port set: `210 passed`
* `git diff --check`
* Python compileall for all changed Python files

The two acceptance authorizer tests remain the known baseline failure: their
read-only authorizer denies the existing `PRAGMA data_version` in
`TimelineCommitStore._store_version()` before the replay assertion. They were
not weakened or changed. Ruff and Pyright report pre-existing diagnostics in
the large Runtime modules; no new candidate-specific diagnostic was isolated.
