# D141z validation

Exact shared acceptance: `bash ops-d141z-build-stop/check.sh` — PASS.

Also PASS:

- `python3 -m py_compile -q ops-d141z-build-stop/run-final-delivery.py ops-d141z-build-stop/delivery_lifecycle.py`
- `bash -n ops-d141z-build-stop/check.sh`
- `ruff check --select F ops-d141z-build-stop`
- `git diff --check`

The acceptance uses the candidate caller for the normal path and the same candidate lifecycle helper for controlled local wrapper/builder trees. It covers normal exit, early leader/descendant TERM+KILL and reaping, low disk before/during/after, invalid/frozen/missing samplers, timeout, SIGTERM/SIGINT/cancel, trace first/periodic/final rows, KEEP retention, and source/path/hash guards. The only real sampler run was the installed 5-second donor; no delivery-build was invoked.
