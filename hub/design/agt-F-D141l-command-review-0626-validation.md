# Validation

Result: FAIL. This was a source-only review; no product import, acceptance admission, body, collection, or installed mutation was performed.

Commands and results:

- `/home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-proof-return-0515/evidence/check-source.py` — PASS, but the script is incapable of validating executable controls; see F-D141L-006.
- `bash -n command-cut.sh command-pristine.sh positive-stub.sh` — PASS.
- Read-only `git rev-parse HEAD`, `HEAD^{tree}`, and clean-status checks on the four qualified homes and two pristine pins — PASS for the observed tuples recorded in `source-manifest.json`.
- Read-only existence check for every one of the 17 pristine roots — 16 OK, `tests/v10/timelines_create.py` MISSING; `tests/v10/test_timelines_create.py` exists.
- Existing positive stub with positive manifest — `rc=1`, `calls=0`, `D73 launcher: agent SHA mismatch`.
- Existing positive stub with agent-sha-only poison manifest — `rc=1`, `calls=0`, `D73 launcher: agent SHA mismatch`.
- Detached persistent reviewer disk monitor, sampled every 5 seconds before and during review — remained above the 4,000,000,000-byte stop floor; samples are in `disk-trace.txt`. It was not used as a retrospective production-run claim.

No full suite or localhost/browser/live-socket suite was run. Product types/lint are N/A because no product source was changed. The author packet's historical receipts and F009 trace disclosure were read but not retargeted or used as current behavioral proof.
