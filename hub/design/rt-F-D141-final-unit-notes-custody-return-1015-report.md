Implemented the D141 custody-return evidence.

- Qualified exact current targets and backups.
- Recorded `568` current outside files and reproduced earlier aggregate `eea4…7fded`.
- Preserved `FAIL_CUSTODY_LIMIT`; immediate pre-CAS map, genuine pre/post conservation, and original sampler lifecycle remain `UNKNOWN/NOT_RECOVERABLE`.
- Added durable 5-second disk trace and sampler lifecycle.

Evidence: [correction.json](/home/user/work/wt/rt-F-D141-final-unit-notes-custody-return-1015/evidence/correction.json), [source-manifest.json](/home/user/work/wt/rt-F-D141-final-unit-notes-custody-return-1015/evidence/source-manifest.json), [comparison.py](/home/user/work/wt/rt-F-D141-final-unit-notes-custody-return-1015/evidence/comparison.py).

Validation passed:

- `python3 evidence/comparison.py`
- JSON validation for all receipts
- Target/backup SHA-256 checks
- Own sampler: PID 4, exit 0, waited and reaped
- No reinstall, mutation, rerender, product tests, build, or ZIP

Commit message and `DONE` marker created.