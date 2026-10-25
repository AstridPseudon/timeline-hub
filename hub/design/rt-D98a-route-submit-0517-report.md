## D98a report

- Registered one private Runtime suite row using CAS, UTC backup, outside-row byte comparison, and atomic restoration.
- Central request ID: `rt-D98a-route-submit-0517-rt-D98a-route-submit-0517-1025052025-32278`
- Result: **FAIL**, exit `1`; 3 tests, 3 errors, 0 failures, 0 skips, XML time `5.505s`.
- Observer was active/restored for the actual pytest PID and captured 3 refusal records.
- First mismatch in all records: `commands[0].command.authorship`, ordinal `0/0`; submitted `absent` vs recorded `object`; 29 safe mismatches each.
- D82 boundary: recorded command-envelope mismatch; exact owner **UNKNOWN**. No source repair or retry made.
- Positive control: preflight `0`, body/route `17`, one active/restored witness. Omitted-activation poison: exit `1`, zero body.
- Same-ID `wait-test` re-read: exit `1`, same terminal failure.
- `suites.conf` restored byte-identically; row count `0`. Worktree clean; `git diff --check` passed.
- Evidence: `788K`, under limit. Commit message and `DONE` written.

Recommended next step: Agent/provider owner should investigate command recording/normalization for the observed envelope mismatch before any future rerun.