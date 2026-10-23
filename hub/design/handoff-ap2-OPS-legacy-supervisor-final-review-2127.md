# PASS — firstreturn

The corrected source report is self-contained and fixes the sole 2123 failure: `test-run:221` removes only transient `running` and cache `.running`; retained `summary` (`212–213`), `exit`, and `status` (`221`) remain.

Evidence verified:

- Route: `request-test:2–15` → `dispatcher-daemon:8–9` → `test-run:1–36` → suite rows `tests/suites.conf:162–168`; protected row 169 excluded.
- Managed versus legacy behavior is accurately bounded by `test-run:39–40,94–100,194–205`; absent `/home/user/work/bench-store` confirms legacy direct-child semantics.
- Manifest contains exactly seven targets (`manifest.json:5–17`).
- All seven Runtime creation receipts and seven retirement refusals exist; each refusal says `target is referenced`.
- Recorded hashes match current sources.
- Universal pre-cutover run accounting and a quiescent launch boundary remain correctly **UNKNOWN**. No absent marker, current flock, or bounded metadata is treated as proof that older unleased runs were absent.
- No unsupported launcher/control-plane claim found.

Checks:

- `bash -n` on the three cited scripts: passed.
- Manifest JSON and exact-seven validation: passed.
- `git diff --check`: passed.
- Worktree status: clean.
- Product tests, typecheck, and lint: not run; source-report-only with no source changes.
- No repository or production state modified. `DONE` created; no commit message because this is report-only.