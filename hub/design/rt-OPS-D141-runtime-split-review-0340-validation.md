# OPS D141h validation

## Verdict

FAIL due to `D141H-SEC-001`. The isolated admission controls pass, but the private kit is not security-qualified while terminal trace finalization can follow a replaced symlink or block on a replaced FIFO before trace validation.

## Source/dispatcher trace

- Read-only `request-test` source writes a generated full ID to `tests/<FULLID>/request` and `queue/pending/test-<FULLID>` (`bin/request-test:13-15`).
- Read-only normal dispatcher source consumes `TEST <FULLID>` and invokes `$O/bin/test-run <FULLID>` (`bin/dispatcher-daemon:19-20`).
- Private `test-run` computes the worktree HEAD/tree, invokes the private receipt validator before admission (`bin/test-run:30-59`), starts the body-owned heavy trace (`:92-100`), and runs the suite body (`:257-276`).
- Terminal finalization invokes the vulnerable append then trace validation (`bin/test-run:64-80`).

The isolated smoke deliberately did not run the live dispatcher, queue, product body, or gate. It copied the normal request-test shape into private roots and invoked the received runner with harmless subprocess bodies. Therefore this is source/control evidence, not a live dispatcher or product qualification claim.

## Exact checks and results

- `TMPDIR=/tmp/d141h-runtime-review-cases-s3E2Lw python3 -I privateops-d141-measured-floor/controls/real-controls.py` — PASS, exit 0; 37 cases: 15 positive/terminal-path and 22 refusal/poison; exact P5 and target15, normal generated full ID, App refusal, floors/defaults/stop, occupancy, failure/cancel/reaping, trace and receipt poison.
- `bash -n privateops-d141-measured-floor/bin/test-run` — PASS, exit 0.
- Python AST parse of all five private Python files — PASS, exit 0.
- `ruff check --no-cache privateops-d141-measured-floor/bin/*.py privateops-d141-measured-floor/controls/*.py` — PASS, exit 0.
- `python3 -m json.tool privateops-d141-measured-floor/install-manifest.json` — PASS, exit 0.
- `git diff --check` — PASS, exit 0.

The publication smoke verified installed-bin → published-bin → received-bin mode/hash parity and no `controls/` sibling dependency. The harness rewrites only private orchestration/snapshot/bench paths in its installed copy, so that isolated received `test-run` hash is expected to differ from the manifest source hash; the source hash itself was verified before rewrite.

## Scope limits

No real Runtime/App tests, imports, collection/preflight/registry, live request/queue/body, install/CAS, hub/network/package/env/Store activity, full suite, gate, or actual P5/target15 receipt was run.
