# FINAL PASS — harness mismatch only

Reviewed the exact safe diagnostic, run log, App assertion, and Agent provider source.

- Actual run: 1 pass / 1 fail; second POST reached Runtime 409.
- Expected path: `config/clips/id:<rightId>/app/astrid`
- Actual path: `config/clips/id:<rightId>/at`
- The trim declares `at=2`; the accepted Agent move changes `at` to `3`. Provider rebase guards correctly emit `value_conflict` at the changed declared-read path (`_commit_patch.py:296–309, 886–902`).
- D16 permits this earlier refusal. The smallest valid harness change is replacing only the concrete expected path with `at`.

No weakening is required: retain the existing 409, conflict shape, refusal, recovery-message, outbox, rollback, raw-field, sibling, history, receipt/head, owner, and legacy-route assertions. Do not broaden the oracle to accept either path.

Evidence checks:

- Safe diagnostic matches the production artifact byte-for-byte; SHA256 `9aa108b2…ac6a3e`.
- 28 mounted records, 2 POSTs, 1 outbox owner.
- `git status --short`: clean.
- `git diff --check`: pass.
- Reused central run `bin/request-test app-P1-actual-caller-sol-2242 ap2-P1-chain-h6 --no-cache`: exit 1, one pass/one failure. No duplicate browser/service run performed.

Recovery visibility was false at the failure snapshot, but later assertions were unreachable; eventual UI recovery and complete rollback remain UNKNOWN. Whole P1 remains NO-GO until the one-line harness adjustment is applied and the named run passes.

Commit message and `DONE` marker were created.