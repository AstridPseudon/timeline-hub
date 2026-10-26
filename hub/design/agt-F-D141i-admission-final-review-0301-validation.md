# Validation

Disposition: `FAIL_COMMAND` with one finite blocking finding, D141I-FINAL-001.

Commands and results:

- `bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141i-admission-return-sol-0253/evidence/measurement-command.sh` — PASS.
- Independent `admitted_dispatch.py` helper execution with the genuine receipt/brief — exit 0; witness `4821594112 >= 4700000000`, controller `agt-F-D141i-cut-controller-0249`, service `agent-agent-core-full-1026025151-24049`.
- The same helper with malformed, below-floor, copied-forged, and missing receipt inputs — each exit 78.
- Independent extracted source guard (`capture_sources`) — PASS: Agent `28e56cac` / tree `2ebe2ddf`, Runtime `6a011d58` / tree `ac5b8627`, App `867cb273` / tree `2b44a46c`, Composition `635f4de0` / tree `5ab5191a`; all exact paths and clean.
- Independent source-manifest physical/historical hash and origin validation — PASS.
- `/home/user/work/venv-agent/bin/ruff check --no-cache /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141i-admission-return-sol-0253/evidence/privatecontrols/drivers/admitted_dispatch.py` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/mypy --cache-dir=<private temporary cache> --follow-imports=skip --ignore-missing-imports /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141i-admission-return-sol-0253/evidence/privatecontrols/drivers/admitted_dispatch.py` — PASS.
- `/home/user/work/venv-agent/bin/ruff` and `mypy` were the only applicable operational-Python checks; no product code was changed.
- Packet `final_validate.py` — exit 0, `PASS_STATIC_FINAL_PACKET`; confirms exact 22 roots, `-q -n3 -o addopts= -p no:cacheprovider --timeout=45`, unchanged body argv, source/history hashes, row, manifests, and no production runroot.
- Independent exact post-body block simulation with readable disk `3999999999` — exit 0. This is the failure: the block records the value but does not enforce `>=4000000000`.

The author packet’s 20 tiny controls, fresh serialized positive/poison dry controls, original 0246 `PASS_COMMAND`, and actual 24049 `fail78`/body-zero evidence were read and preserved. This reviewer did not run pytest, collection, the measurement body, a service request, `request-test`, row installation, or any full suite.
