Repaired only the owned runner and wrapper. Custody now uses normal bench-store registration/leases, fixed source pins, maker source/RECORD/client verification, and installed Composition/peer checks. Post-run custody failures return nonzero. Setup failures record `NOTRUN` without fabricated JUnit. Original selector, 12 assertions, and 30-second timeout remain intact.

Static acceptance passed:

- `PYTHONPYCACHEPREFIX="$TMPDIR/pycache" python3 -m py_compile tools/run-generic-reopen-original-0605.py`
- `/home/user/work/venv-agent/bin/ruff check --no-cache tools/run-generic-reopen-original-0605.py`
- `/home/user/work/venv-agent/bin/mypy --cache-dir "$TMPDIR/mypy-current" --follow-imports=skip tools/run-generic-reopen-original-0605.py` — zero issues; parent had one, zero new.
- `bash -n tools/run-generic-reopen-original-0605.sh`
- `git diff --check`

Parallel independent static review found no remaining repair/handoff blocker. Runtime compatibility remains unverified: no tests, Node, preflight, provisioning, or body execution occurred.

Exact handoff: worker `evidence/generic-reopen.row`. Commit message and `DONE` created. Next: obtain genuine child and independent source PASS, then manager installs the reviewed row and enqueues with `--no-cache`.

Runner SHA256: `6eb755728488122c905d8111e8e68a93d6961e679d2b10a804240b0b311b837e`.