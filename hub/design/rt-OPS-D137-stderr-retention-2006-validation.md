# D137 validation

Commands and results:

- `bash -n ops-child-custody/make-child-venv ops-child-custody/install-prep/apply-reviewed-maker.sh` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v` — PASS, 42 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -B ops-child-custody/install-prep/dry_run_controls.py` — PASS.
- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/install-prep/*.py` — PASS.
- `python3 -m compileall -q -d <worker tmpdir> ops-child-custody/tests ops-child-custody/install-prep` — PASS.
- Exact embedded verifier comparison — PASS; STORE_PY and STORE_VERIFY hashes unchanged.
- `git diff --check` — PASS.

The D137 decision helper accepted an exact private decision record with
WITHDRAWN/NOTRUN E2E, candidate hash/size, and a 40-hex source commit. No
installer, Store, child request, fixture body, acquisition, or production
request ran. Independent review and real CAS installation remain pending.

