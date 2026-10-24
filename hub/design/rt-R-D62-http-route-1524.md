## Completed

Installed one unique row: `runtime rt-D62-integrated-1524`.

Command:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-D62-http-route-1524/evidence/integrated.xml
```

- Atomic install under `/home/user/work/.runtime.merge.lock`.
- Registration count: 1.
- Pre-hash: `40f1c34a...09c47a3`
- Post-hash: `b0557c15...39980d3`
- Backup: `evidence/suites.conf.before`, hash matches pre-hash.
- Registry mode: `0644`.
- Outside bytes preserved exactly.
- Qualified interpreter path: `/home/user/work/venv-runtime/bin/python` → `/usr/bin/python3.13`.
- Durable XML parent verified physically.
- Historical 1454 XML unchanged: `b5f52c06...df47c8`.

Verification passed:

- `bin/test-run` selector validation source check.
- Allowed selectors accepted; `--junitxml`, `-o`, and `-p` rejected as `--files` tokens.
- `bash -n bin/test-run`.
- Read-only registry lookup via `awk`.

No `request-test`, pytest body, HTTP, browser, full suite, or product tests were run. Selectors remain manager-owned for post-adoption execution.

Evidence: [registration-verification.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-D62-http-route-1524/evidence/registration-verification.json)

Worktree remains clean; `DONE` and commit message were created.