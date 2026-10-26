# Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 .../owner-sol-1647/evidence/check_jj.py`, run through the retained heavy supervisor with a private TMPDIR: **exit 0**. Fresh run ID `f3d2449da4e34df5b0da948be2e4f033`; attempt PID 5/PGID 5; explicit wait/reap; stop `null`; initial available bytes `5170794496`; retained files `8997639` bytes. Positive, scoped-CAS, eleven caller negatives, two direct D68 stage guards, direct App-tree guard, and source/worktree invariants passed.
- `ruff check --isolated --no-cache --select F .../owner-sol-1647/evidence/check_jj.py`: **exit 0**.
- AST parse, private `py_compile` to reviewer `/tmp`, and authored JSON parse: **PASS**.
- `bash -n .../base-fix-next/evidence/candidate/check.sh`: **exit 0**.
- `git diff --no-index --check` between immutable base checker and author checker: expected differing-file exit 1 with empty diagnostics; **PASS**.
- Immutable source manifest byte comparison plus all 11 candidate SHA256/mode checks: **PASS**. Original manifest SHA256 `7c3fa7c10dd4afb7e01f6af32aaf28ffb94a16c81730095d36bc514683b27852`.
- Reviewer worktree `git status --porcelain`: clean. No full suite, same33 repeat, build, install, service, browser, socket, or product test was run.
- Reviewer sampler: four valid real 5-second samples, observed PID 3, exit 0, explicit wait/reap; trace at `tmp/reviewer-5s-sampler-trace-2.txt`, minimum available bytes `5049004032`. An earlier malformed sampler trace is preserved but not used. The first required evidence sampler also exited 0 and was reaped; its valid trace remains at `disk-trace.txt`.

The author’s preserved first corrected-derivative attempt exited 1 at the ordinary umask fixture defect; it was not reclassified or deleted. The later author attempt and this independent exact run both exited 0.
