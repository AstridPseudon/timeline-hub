Implemented the F-ABA row return.

- Updated [`tests/suites.conf.candidate`](/home/user/work/wt/agt-F-ABA-row-return-0825/tests/suites.conf.candidate) to target Agent `0c2c28da` / tree `4ce9de…`.
- Added strict Agent/Runtime cleanliness checks and loaded auth-file SHA guard.
- Added [`tests/suites.conf.candidate.request.md`](/home/user/work/wt/agt-F-ABA-row-return-0825/tests/suites.conf.candidate.request.md) with the canonical later request.
- Live registry and original test body unchanged.

Validation passed:

- `bash -n tests/suites.conf.candidate`
- Source-target import/tree/hash guard
- Candidate serialization and request checks
- `git diff --check`

Original ABA test, full/browser suites, and live service request were not run. Commit message and `DONE` marker are prepared.