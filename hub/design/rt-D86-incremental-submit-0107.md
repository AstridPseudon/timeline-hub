# D86 Incremental Main Qualification Report

Completed one meaningful incremental MAIN submission using the existing D73 route.

- Selected and validated 268 eligible nodes.
- Excluded numeric9 as pending; preserved 308-row explicit remainder and D87 retired-row accounting.
- Bound released Runtime `a3cd1a32`; preserved `agent-remotion-0013` profile identity.
- Captured Agent/App/Composition checkout receipts and path-sensitive source/test hashes.
- Verified CAS registry backup and outside-row byte equality.
- Controls passed: bash syntax, positive exit 17 once, wrong-SHA poison with zero calls, and missing-input refusal.

Commands/results:

- `bash -n ...`: pass
- `python3 -m py_compile tools/install_p4_launcher.py`: pass
- `git diff --check`: pass
- Service ID: `agent-d86-incremental-main-1025011156-10077`
- Same-ID wait completed: exit 1
- Result: `39 failed, 30 passed, 176 errors in 111.59s`
- Automatic verdict: `NO-GO`
- First routed exception: `CommandError: missing or ambiguous identity 'occ-a'` in the occurrence-media family.

The earlier no-body submission failed before pytest because a private launcher variable was missing; it was repaired before the single meaningful body. No retry, repair, broad diagnosis, full suite, D59 credit, D88 prototype use, product/test changes, or dependency changes were made.

Durable evidence is under [evidence/rt-D86-incremental-submit-0107](/home/user/work/wt/rt-D86-incremental-submit-0107/evidence/rt-D86-incremental-submit-0107). Route sources are under [tools/main_affected_batch_d86_incremental](/home/user/work/wt/rt-D86-incremental-submit-0107/tools/main_affected_batch_d86_incremental).