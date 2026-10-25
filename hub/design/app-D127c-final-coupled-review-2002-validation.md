# Validation

## Runtime

- Reused the required central result; did not rerun or resubmit: `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_p2_commit_phase_capture.py` — **61 passed in 3.62s** on corrected central request `30318`.
- `ruff check tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — **PASS**.
- `python - <<'PY' ... ast.parse(...) ... PY` on `tests/helpers/p2_commit_phase_capture.py` — **PASS** (read-only syntax check; no bytecode output).
- `git diff --check e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d 368f53f4454d5908c86de53d174f0bedcf23781c` — **PASS**.
- Prior Sol1935 evidence reused for Python 3.11 compilation, helper Pyright, and scoped Runtime typechecks: zero new errors; existing parent diagnostics kept separate.

## App

Reused exact final-tree binder1950 results (final test blob `558963eb...`; no App source changes were made here):

- Node 20.19.4 profiler-only command with the supported Runtime checkout override — **1 passed, 5 skipped by name pattern**.
- Node 22 combined no-live validator pattern `^(D127c reviewed-profiler validator|D127 reviewed-new validator)` — **2 passed**.
- `npx eslint tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts --max-warnings 0` — **PASS**.
- `npx tsc --noEmit --pretty false` — **PASS**.
- `git diff --check` — **PASS**.
- Read-only committed-blob guard probe (final helper hash present, old reviewed-new hash is the only `else` assertion) — **CONFIRMED D127c-F001**.
- The combined Node 20 profiler+reviewed-new pattern hung and was interrupted at exit 130 after about 136 seconds; this was disclosed by binder1950. It was not resubmitted. A second combined run was not needed: the supported Node20 profiler control passed and Node22 covered both validator nodes. Disk was 4.8 GiB, above the 4.6 GiB floor but below the 5 GiB caution threshold.

## Not run by design

No live bootstrap/source-guard body, browser, original element body, native/full/tour/Store/install/acquisition, or full suite was run. The source-guard failure was established directly from the final committed App blob and the exact final helper hash.
