# OPS D141s validation

Result: PASS for source controls; no installation, live CAS, queue mutation, App body, or release claim.

Commands and results:

- `TMPDIR=/tmp/w-210f1cd415/d141s-controls PYTHONDONTWRITEBYTECODE=1 python3 -I ops-d141-measured-floor/controls/real-controls.py` — PASS, 74 cases; SEC001/SEC002 PASS; freeze2 NEEDS; release NOT_READY.
- `bash -n ops-d141-measured-floor/bin/test-run` — PASS.
- Python AST parse of `bin/d141-validate-receipt.py` and `controls/real-controls.py` — PASS.
- `ruff check ops-d141-measured-floor/bin/d141-validate-receipt.py ops-d141-measured-floor/controls/real-controls.py` — PASS.
- JSON parse, SHA-256, mode, and install-manifest output checks — PASS.
- `git diff --check` — PASS.

The private control publication copied the five manifest binaries through installed, hub/kit, and received locations and verified matching hashes/modes. The exact 5344 normal/preflight command and one-LF row hashes match the published App packet. The authentic 18617 request is refused before suite lookup and leaves only `request` and `why`.

The packet remains prospective (`registration=false`, `execution=none`), and the final source remains not installed. Runtime's later 95d98 producer was recorded as an observation and was not used to retarget the genuine 5344 packet bytes.

A bounded, unapplied replacement map records only the known old Runtime 6a011d58/ac5b8627 source to the observed 95d98f/78df31d6 source. It deliberately contains no inferred command or row hashes; a regenerated App packet is required before that map can be applied.
