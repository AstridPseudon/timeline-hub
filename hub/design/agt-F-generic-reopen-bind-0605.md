Implemented the owned harnesses:

- `tools/run-generic-reopen-original-0605.py`
- `tools/run-generic-reopen-original-0605.sh`

The harness is preflight-only by default and fail-closed. It binds source/body hashes, managed child authority, markers, RECORD/direct URLs, runtime protocol origins, Node/profile locks, exact pytest argv, JUnit/output/exit evidence, and durable failure records. Original test body was not run.

Exact SHA256:

- Python: `d6c84a8311305a8a7964c7ac05e140bc8c5ddc94d286cbeaf301e3b99fa1b1d9`
- Shell: `b3865cb2d77a16ee0d65e6272e6ddb419f38631fb7299522b343e9b62976b7a5`

Checks passed:

- `python3 -m py_compile ...`
- `bash -n ...`
- Ruff
- `git diff --check`

Preflight result: refused existing `ba8f/f320` child because it does not bind `bb50` source; `body_runs: 0`.

Single suite row:

`tests/test_generic_host.py::test_structure_pack_members_survive_harvest_cleanup_and_reopen` — `preflight-refused`, exit `2`.

The requested `bb50/f320` candidate remains unavailable; provisioning was refused at pinned-requirements timeout. Commit message and `DONE` marker were created.