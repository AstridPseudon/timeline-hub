# D139 independent review validation

Result: **FAIL_SOURCE**. All author-specified validation commands passed; the
independent private adversarial controls found four source findings. No full
suite was requested or run.

## Baseline diagnostics before exclusions

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m unittest discover -s ops-d131 -p 'test*.py' -v` — PASS, 11 tests.
- `/home/user/work/venv-agent/bin/ruff check ops-d131/bench_store.py ops-d131/retire_entry.py ops-d131/test_retire_entry.py` — PASS, `All checks passed!`.

## Required acceptance commands

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m unittest discover -s ops-d131 -p 'test*.py' -v` — PASS, 11 tests.
- `/home/user/work/venv-agent/bin/ruff check ops-d131/bench_store.py ops-d131/retire_entry.py ops-d131/test_retire_entry.py --ignore EXE002,BLE001` — PASS.
- `sh -n ops-d131/install-prep/check-cas.sh` — PASS.
- Private compile using `/home/user/work/venv-agent/bin/python -B` and `compile()` for `bench_store.py`, `retire_entry.py`, `test_reserve.py`, and `test_retire_entry.py` — PASS for all four.
- `ops-d131/install-prep/check-cas.sh "$PWD" tl/rt-OPS-D131-kind-reserve-1558` — PASS; preimage `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2`, mode `0755`, no installation.
- `git diff --check` — PASS.

Additional review-only check: `git diff --check
tl/rt-OPS-D131-kind-reserve-1558..HEAD` — PASS.

## Independent private controls

- Caller age/clock control — FAIL: a temporary Store entry retired with
  caller-supplied `registered_at=2099-01-01T00:00:00Z`,
  `not_before=2099-01-01T01:00:00Z`, and `now=2099-01-01T02:00:00Z`; the
  entry had no persisted age field.
- Process race control — FAIL: a temporary process acquired cwd in the victim
  directory after the second `/proc` audit returned; retirement still returned
  `retired` and deleted the path.
- Corrupt receipt control — FAIL: malformed retired receipt path/node/lock/seq
  and suite element values were accepted by `Store.registered()`.
- Normal retention control — PASS: three temporary child entries left exactly
  two entries after ordinary `ensure`/`_evict` processing.

All private fixtures used temporary directories and were cleaned up by their
fixture lifetime. No live Store or source installation was touched.
