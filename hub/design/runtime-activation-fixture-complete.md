# Runtime activation fixture packaging

## Decision

Repair only `tests/test_astrid_activation_join.py`'s private `astrid_root`
fixture. Copy the current Agent checkout's root `pyproject.toml`, `astrid/`
package, and `astrid_runtime_client/` package into the test's own temporary
checkout. Preserve the existing pycache exclusions and all activation, join,
error, process, socket, and metadata assertions.

## Rationale

`astrid/version.py` falls back to source metadata when the child has no
installed Agent distribution, so the temporary checkout needs its
`pyproject.toml`. The joined host also imports the official vendored
`astrid_runtime_client/` package. These are the smallest current resources
identified by the triage; no full Agent snapshot, install, shared dependency
mutation, or product change is needed.

## Verification

The one permitted marked-integration run was queued against this worker's
snapshot and executed as:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -n 3 -m integration tests/test_astrid_activation_join.py
```

It stopped in fixture setup with two errors because the initial patch copied
`pyproject.toml` before creating the temporary checkout directory. The
directory-ordering correction (`root.mkdir()`) was made afterward. Per the
task instruction to run this marked file once, the corrected patch was not
resubmitted; no protocol or product failure is claimed.
