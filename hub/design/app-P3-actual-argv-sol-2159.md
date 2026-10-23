**NOTREADY — argv carrier fixed; preserved caller still fails qualification.**

Changed only row 245, `app ap2-P3-gate5-h6-0348`, in `suites.conf`: six quote escapes added, totaling 24 bytes. Used `shlex.quote` on the retained intended inner artifact. Inner script, native helper’s 21 assertions, history checks, receipts, guards, leaf command, and original final selector remain unchanged. Atomic replacement/readback preserved all 246 other rows.

Actual whole-outer interception proved:

| Capture | argc | Argument byte lengths | Payload equality |
|---|---:|---|---|
| Before | 5 | `2, 4425, 364, 376, 23767` | FAIL |
| After | 2 | `2, 28941` | BYTE-EXACT PASS |

The corrected call receives exactly `-c` and one complete payload argument.

Validation performed, with `$TMPDIR=/tmp/w-b9c96d1f25`:

- `/bin/bash -n "$TMPDIR/after.outer"` — PASS.
- `/bin/bash -n "$TMPDIR/intended.inner"` — PASS.
- `/bin/bash "$TMPDIR/static.prefix"` — exit 0; authentic source, managed-store, receipt, origin, integrity, and Node/npm checks pass. Stops before setup.
- `/bin/bash` against `badApp.prefix`, `badAgent.prefix`, `badTree.prefix`, `badBody.prefix`, `badReceipt.prefix`, and `badPath.prefix` — all exit 2 with NOTREADY/body-NOTRUN.
- `python3 "$TMPDIR/qualify-caller.py"` — actual argv equality and success/export-eval PASS; **fail-fast qualification FAIL**.
- Read-only diagnostic of the complete retained source-guard span — **52/58 checks pass; six fail**.
- `git diff --check` — PASS; App worktree remains clean.

Two independent blockers remain:

1. Exit 17, inner syntax failure, and eval syntax failure all continue into the preserved outer tail. Each attempts `unlink`; the interceptor refused the operation. No dependency mutation occurred.
2. Retained guards expect an older HEAD, tree, parent, harness blob, and two copies of the old `useTimelineSave.test.tsx` SHA. These disagree with required target `6c33025bb50783a7c325250de27e3bdef45577cb`, tree `80addcc5dede29e27fd4ab8e31c347e6e432efb2`. Product projection differs from `2107e187…` only in the seven D29 harness paths; original body blob remains `37caf28577d42fbe98afd2320dffa3c72e6e74b1`.

SHA256 evidence:

| Item | SHA256 |
|---|---|
| Updated row, including newline | `aa7c2b14c7812b43f2dd6e17afa4311c012ac3200b221f7ce5b4aae5ededcfae` |
| Outer command | `9c6f4baa294d39eb42612f7d6e3bf08a3e470f315ecf8bf09d0851817b460d42` |
| Exact inner payload | `23111506eaa17ce3e11c3db71aa71a93245bad7ac89b95aaaf0cfa51ece97880` |
| Captured complete corrected argv, NUL-separated | `c573197ffcc1fcbd7802a59532aac27ee581a57d1f1d66d35c8da6e888a683cb` |
| Complete source-guard span | `d39f9328ebf8d88f5d0a1732347d332a8ab8ab5af092c0dcff8aedf78cf7ea0e` |
| Unchanged complete post-payload tail, 14,800 bytes | `11e9191f033e36fb50df21de1873a4fb2a18dc11b2f9da64dd65778d55126e06` |
| Unchanged invocation tail, starting at HEAD guard | `d0c93c346e869af3579ae3d3da22c92e0fab070c9a2220992b595ef46dce7a3e` |
| All outside-row bytes | `6c661621ab4026bac6b3b4a1bd70e88db7b44084886074ce9d924b108f715c35` |

CN2147/RN2049, Agent `079580ca…`, Runtime `2a9e347f…`, Node `v20.19.4`, npm `10.8.2`, and managed-store paths remain unchanged. Authenticated receipt hashes remain child `a25c3495…`, runtime `e1e522e2…`, provision `3ccb8c98…`.

Original failed result 5262 remains untouched: 564-byte log, SHA256 `89d00c1d1df9584a4ed799e5bfd0e909ad7c4bb3524d881c408a360b19a872eb`. No setup, seed, backend, browser, leaf, original body, provisioning, dispatcher, or full suite was run.

I preserved the tail and guards because changing them exceeds the settled scope. Wrote the P3 commit message and `BLOCKED`; no `DONE`. Next step requires the orchestrator’s decision on those two caller defects.