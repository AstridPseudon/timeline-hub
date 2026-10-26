# F D141z independent review — FAIL

Result: **FAIL** for the actual final production caller.

The exact unmodified acceptance command passed once the full 41.4-second run was
allowed to finish. Static checks also passed. That is insufficient for PASS:
the real caller's default runner/wrapper paths are absent at this source venue,
trace custody is weaker than the installed donor, and the acceptance exercises
mostly the lifecycle helper rather than the production caller.

Findings are recorded in `findings.md` and `review.json`.

## What was reviewed

- Candidate base: `32bc911afcb2648e54be4432c5aa96cbdacf4eae`.
- Original final caller: safe input SHA-256
  `45a506394d2d0fd025809c921fd446d363bc0d624d7170a049d88b5c6704e191`.
- Candidate files: the four declared files plus two tracked `__pycache__/*.pyc`
  files omitted from the author manifest.
- D68 wrapper/source, installed donor `test-run`, donor disk sampler,
  validator, and append-final custody path.
- C0 request/reply examples were read; no lifecycle metadata was introduced
  into the Runtime commit wire.

## Findings

1. `run-final-delivery.py:25-35,220-223` hardcodes three worker-evidence
   dependency paths. The core runner, core inventory, and D68 wrapper paths are
   absent now; only the safe wrapper copy under `design/` exists. `main()` checks
   these before dispatch, so the actual caller refuses before running the
   lifecycle. The install map does not provide a receiving installation for
   them.
2. `delivery_lifecycle.py:156-165,240,331` retains the sampler's readiness line
   as an opaque string and validates the trace by pathname. It does not use the
   donor's immutable binding or `d141-append-final.py` descriptor path. The donor
   opens the bound file and invokes `d141-validate-trace.py --fd ... binding`.
   A same-user replacement of the trace pathname can therefore be observed and
   validated as a different file; this is not donor-level append/validator
   custody.
3. `delivery_lifecycle.py:31,203-210` implements only a private
   `/tmp/timeline-final-delivery-heavy.lock`. The normal production heavy
   service's installed `test-run` coordinates via its `$ORCH/tests/*/heavy` and
   `running` state (`test-run:50,58`), with no reference to this lock. The two
   systems can admit concurrent heavy work and do not share one admission slot.
4. `check.sh:132-135,172-187` runs the stop cases directly through
   `life.run_delivery`; only the normal case calls `candidate.run_wrapper`, and
   `candidate.main()` is never called. The real source tuple, gate tuple, D68
   wrapper construction, receipt path, and production source guards are not
   exercised by the claimed acceptance. The actual donor validator is also
   replaced by a permissive stub (`check.sh:60-67,125-126`).
5. The claimed early-leader control is absent: the stub builder always waits for
   its child (`check.sh:80-83`), so no case has a leader exit while a live
   descendant remains. The cancellation case writes a local file from a timer,
   not the installed mounted stop/caller semantics. The donor's subreaper,
   parent-death, control-pipe, and mounted stop contract is therefore not
   qualified by this acceptance.
6. The two tracked bytecode files
   `ops-d141z-build-stop/__pycache__/delivery_lifecycle.cpython-313.pyc` and
   `run-final-delivery.cpython-313.pyc` are absent from the author
   `source-manifest.json` and `install-map.json`. They are timestamp-based,
   interpreter-specific artifacts with no declared conservation rule. This is
   an install-scope/documentation mismatch; they were not deleted or modified.

## Limits and omissions

No delivery build, rehearsal, ZIP, canonical install, service/queue write,
network acquisition, or large suite was run. The first-tool review trace wrote
one sample but did not survive the terminal shell; its lifecycle is reported
honestly in `sampler-lifecycle.json`. No receiving inputs were fabricated, and
the historical 0741 unknown exit/reap was not backfilled.

