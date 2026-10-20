# Agent cutover migration review — 2026-10-20 09:31 UTC

REJECT tl/agt-cutover-retired-writers / 2961d3ce as a combined landing.

The identity-fixture migration is a useful isolated unit: removed private _media import becomes public ingest; trusted historical setup preserves the three exact overwrite/isolation/retry assertions. Port that separately and qualify it.

The stage1 cutover changes replace successful shot create/update/reorder/remove/archive/recover and candidate-promotion behavior with retired_route expectations. In particular test_promote_candidate_receipt_replay_and_foreign_provenance_rejection loses the accepted promotion receipt, primary switch/supersession, derived invalidation and specific foreign validation assertions. Unchanged-state refusal is additional useful endpoint-denial coverage, but is not equivalent preservation of those positives. Moving stale-version conflict to the reference catalog does not preserve the shot behavior.

Required: keep the original positive expectations (strict xfail only where a real replacement is still missing), migrate them to supported guarded commands/proposals as those exist, and keep refusal tests separately. No full green or deletion claim from the 46-pass transformed suite. Five AG-CUTOVER ledger mappings are rejected/unmerged proposals until the positive replacement tests are named and pass.

The earlier worker brief allowed denial conversion too broadly. This review corrects that direction. No Runtime product rollback or writer restoration is requested.
