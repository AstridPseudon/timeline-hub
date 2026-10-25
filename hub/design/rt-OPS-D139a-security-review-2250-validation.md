# D139a validation

All commands below were run against this worktree. No full suite, install,
network acquisition, child request, Store mutation, provider, browser or live
socket was run.

| Command | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m unittest discover -s ops-child-custody/tests -p 'test_*.py'` | PASS, 57/57 |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m unittest discover -s ops-child-custody/tests -p 'test_custody.py'` | PASS, 33/33 |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m unittest discover -s ops-child-custody/tests -p 'test_inventory.py'` | PASS, 11/11 |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m unittest discover -s ops-child-custody/tests -p 'test_schema_distribution.py'` | PASS, 6/6 |
| `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/check-child-imports` | PASS |
| `bash -n ops-child-custody/make-child-venv ops-child-custody/install-prep/apply-reviewed-maker.sh` | PASS |
| seven embedded Python blocks compiled in memory with `/home/user/work/venv-agent/bin/python` | PASS |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B ops-child-custody/install-prep/dry_run_controls.py` | PASS |
| `python3 -m json.tool ops-child-custody/source-manifest.json` | PASS |
| `git diff --check` | PASS |

Additional private control: the real `/home/user/work/venv-agent` installed
schema distribution was admitted without installation or Store use. It produced
18 snapshot files, 18 RECORD rows, 12 hashed rows, and `tree_tie=UNAVAILABLE`.

One separate diagnostic run of the all-tests command under
`/home/user/work/venv-runtime/bin/python` failed one pre-existing checker test
because that venv lacks `typing_extensions`; the required venv-agent run above
passed 57/57.
