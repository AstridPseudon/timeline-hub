# Handoff — F D141z wholepath

**FAIL remains controlling. No independent acceptance credit.**

The actionable map is in `source-map.json`; the concise finding set is in
`findings.md`. The normal compatible heavy owner is the existing
`scratchpad/orch/bin/test-run` route with bench-store/`heavy` state, donor
binding, subreaper + parent-death handling, control-pipe process-group
tracking, and append-final descriptor custody. The candidate's private
`/tmp/timeline-final-delivery-heavy.lock` is not interoperable with it.

The candidate call chain is `run-final-delivery.py:run_wrapper` →
`delivery_lifecycle.run_delivery` → D68 process → in-process builder call.
It has local process-group TERM/KILL/reap, but no mounted parent-death or
control-pipe contract, and its terminal trace validation is pathname-based
with an opaque readiness string. `check.sh` exercises the helper directly for
nearly all cases and never calls `candidate.main`; its stub validator and
waited child do not qualify the real D68/builder path.

F1 is a receiving/host input gap: exact canonical Runtime paths and hashes are
listed in the map. The safe D68 copy under `design/` is not a canonical install
and no replacement is inferred. F2–F6 are intrinsic source/acceptance gaps.
The tracked `.pyc` files remain an install-scope discrepancy; nothing was
deleted or modified.

No C0 wire/schema change, new mechanism, admission exception, install, build,
rehearsal, service action, or original-0741 outcome correction is authorized
or claimed. Runtime remains the owner of receiving/install and later separate
acceptance review.
