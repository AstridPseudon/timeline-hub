# G5 SDK retained-restore oracle — 1941

## Disposition

Implemented the single allowed C0 identity correction on Agent base 697c8fd3b51562fb18e45dedecc56723984db2eb.

Only tests/sdk/test_timeline_checkout_history_runtime.py changed, and only the existing second test function changed. The old full-document equality was replaced by a receipt-bound deep copy of original whose only changed field is base_parent.publication_id. The test additionally checks the exact base_parent pair and digest, retains full Checkout(expected).document() equality, and explicitly verifies the full runtime canonical document in source_mapping['_runtime_document'].

This is stronger/equivalent for the C0 property: it preserves equality for every authored field, source pin, null/opaque value, child/internal/media closure, and canonical runtime document while allowing the one identity C0 requires to change—the fresh publication receipt for the restored original revision. The pre-existing assertions that the accepted revision is original and the new receipt differs from the preceding accepted receipt remain verbatim. All consumed-draft and fresh-step undo/redo guards remain verbatim.

## Actual control

The authentic archive preflight passed with SHA256 2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3, schema 31, exact restored head pair (a3e671256f1c42b8837d3e118c97b21b, txn-11c90075be6c4c8bb9e2627366f0fe4f), 3 shots, 3 internal timelines, 5 media objects, 0 documents, and credential scan 0. The actual target node passed once in 18.91s. The final explicit inequality assertion was added after that one permitted live run; no second live run was made. The captured accepted reply directly proves the assertion, and the final source body lock/AST checks passed.

The actual restore packet recorded:
- accepted revision a3e671256f1c42b8837d3e118c97b21b;
- new restore receipt txn-52aa7c96dd514e0696f91ee9f5b3c5c7, distinct from the preceding accepted publication txn-2e638b9ae3594440a8f5ce0f74f7e427;
- canonical parent digest sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb;
- full retained closure: 3 shots, 3 internals, 5 media, 0 documents.

The public success body of the second reset’s open_bundle call was not available to the permitted observer. The test’s successful continuation and the captured accepted reply/private closure are reported; no body or identity was reconstructed or inferred.

Agent identity was 697c8fd… / tree 7aea57b…; Runtime identity was 2a9e347… / tree f79a235…. The child observer recorded 37 lines, 13 seam entries, 13 exits, 0 seam exceptions, 0 observer failures, and 0 credential findings. Auth/module origins were stable, including Agent commit/sync and Runtime auth/timeline_commit_auth.

## Exact checks

- Scoped Ruff: 4 findings in the changed test file, with exact identities equal to the unmodified 697c… file (F401, F811, I001, F811); no new diagnostic.
- Private Mypy on the changed file: Success: no issues found in 1 source file, identical on the unmodified 697c… file.
- Vendor lock: ok runtime.lock.json (matches producer manifest).
- Artifact manifest: artifacts.json is current.
- git diff --check: pass.
- AST comparison: only the retained-restore function differs; the other three original functions are AST-identical.
- D21 body locks: the other three original function hashes remain exact; the final adapted function hash is recorded in the packet manifest.

Prior allowed evidence is reused without repetition: 127 retained-history tests, 16 current-pair controls, source regression set 35, Ruff 2148/2148, Mypy 1911/1911, and the other three original 1937 qualification bodies passing. No repeat FOUR, c271/9/14/40/281/58, full, P1/P4, browser, or live socket suite was run.

The first private preflight attempt failed before pytest because the child log environment variable was omitted, causing sitecustomize to open . as a file. It was corrected by setting a private TMPDIR log path; the corrected preflight passed before the one target-body run.

## Evidence and limits

Worker report: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restore-oracle-1941/report.md

Packet manifest: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restore-oracle-1941/evidence/packet-manifest.json

Lossless packet archive: 998,536 bytes, SHA256 c692f3665bfc3e0f18acfdd7b99b196c66b3dffddf32a51e2d4aaa4563fb1fd9.

This remains G5 draft test-source work only. It does not claim whole-G5 approval, P1 GO, merge, activation, Runtime repair, or deletion. Independent review of the one-test diff and packet manifest is the recommended next step.

