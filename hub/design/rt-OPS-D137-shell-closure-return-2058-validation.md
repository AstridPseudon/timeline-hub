# D137 shell-closure validation

## Root cause and fix

The genuine 2026-10-25 request stopped at `venv-log-setup` with exit 2 because
the Store runner's serialized `STORE_CONTEXT` omitted `stage_stderr_path`.
The same closure also omitted `retain_stage_stderr`, which is reached by
`failure` after a real stage command fails. The maker now exports both helpers
alongside the existing `failure`, `run_stage`, `progress`, and `source_state`.

The regression materializes the maker's exact export declaration and executes
it through the actual Store runner callback and `Store.ensure` cleanup path.
It covers the earliest logging setup, nonzero failure, timeout, exact first
private stderr, public payload-free marker, and post-failure staging cleanup.

## Commands and results

- `TMPDIR=/tmp/w-b1978bcf91 PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v` — **44/44 passed**.
- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/install-prep/*.py` — **passed**.
- `bash -n ops-child-custody/make-child-venv ops-child-custody/install-prep/apply-reviewed-maker.sh` — **passed**.
- In-memory compile of 7 embedded Python blocks plus AST parse of scoped Python files — **passed**.
- Exact `STORE_PY` and `STORE_VERIFY` byte comparison with base `0c4170e42d2ff435ea855a54c940299619f6a285` — **passed**.
- `git diff --check` — **passed**.
- `PYTHONDONTWRITEBYTECODE=1 python3 -B ops-child-custody/install-prep/dry_run_controls.py` — **passed**.

Parent/candidate bounded control: parent returned the recorded
`stage_stderr_path: command not found` refusal; candidate returned the intended
stage exit 17 and retained its private stderr. No genuine request was retried.

## Scope and limits

The candidate is source-unit GREEN only. D137 fixture E2E remains
WITHDRAWN/NOTRUN. No package acquisition, whole make, live Store publication,
production install, child/core service, Farm run, or full suite was performed.
