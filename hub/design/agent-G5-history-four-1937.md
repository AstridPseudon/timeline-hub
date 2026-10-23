# G5 SDK authority qualification — 1937

## Disposition

One authorized original FOUR qualification ran once on the independently reviewed retained-history source `697c8fd3b51562fb18e45dedecc56723984db2eb`: **3 passed, 1 failed** in 96.65s. The failed test is `test_retained_restore_does_not_reopen_consumed_draft_steps` at line 283. No retry, source change, assertion weakening, merge, activation, whole-G5 approval, or P1 GO claim was made.

## Preflight

The corrected 1907 observer parent/shim/hook were copied into worker-owned scratch. The report-all/archive preflight passed: authentic archive SHA256 `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`, normal verify and restore, exact head pair `(a3e671256f1c42b8837d3e118c97b21b, txn-11c90075be6c4c8bb9e2627366f0fe4f)`, 3 shots, 3 internals, 5 CAS media objects, registry, explicit nulls, opaque fields, legacy word, and zero credential findings. Collection-only found exactly 4 tests and ran no bodies. Body locks were `all_match=true`; diff, cleanliness, vendor lock, and artifact manifest passed.

Actual identities were Agent `697c8fd3b51562fb18e45dedecc56723984db2eb`, tree `7aea57b12f578469632f06831ce8b2046d40fada`, and Runtime `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree `f79a2355cfb39d9ada7721978bd20d5702105778`. The stale catalog `d9e2…` string was not treated as authority. Auth module origins/hashes were stable before/after (`runtime_protocol/auth.py=f45941cf…`, `runtime_protocol/timeline_commit_auth.py=3b812936…`); observer delegation had 56 entries and 56 exits, zero seam exceptions, and zero observer failures.

## Actual cause and limits

The restore request was accepted with the original revision and a new receipt publication. The second `_reset_base()` returned and the draft loaded. The only observed mismatch was `base_parent.publication_id`; content digest and revision remained exact. No direct `open_bundle` HTTP success body was emitted by the permitted observer, so that result is recorded as unavailable; no exception was observed and test continuation proves the reset did not raise.

This assigns the observed failure to the Agent test/contract oracle, not Runtime. The later no-unsent-draft undo/redo guards and fresh-step undo/redo assertions were unreached. The source seam remains the conditional owner only for a future direct payload/closure mismatch.

## Evidence

Durable evidence is in the worker report and [packet manifest](../workers/agt-G5-history-four-1937/evidence/packet-manifest.json). The lossless compressed packet archive is 4.6 MiB with SHA256 `fab4d94a0b105be635e695edd333d2e2c1e435fb09f37063a7e352b825e9569e`; it contains 41 runtime boundary packets, 8 Agent-validation packets, metadata, and the 123-line child observer log. Observer delegation recorded 56 entries and 56 exits with zero seam exceptions/observer failures; auth origins/hashes were stable before/after. Credential findings are zero.

This is a bounded qualification result only. The next decision belongs to the Agent retained-restore test/contract owner; do not interpret it as whole-G5 activation or P1 approval.
