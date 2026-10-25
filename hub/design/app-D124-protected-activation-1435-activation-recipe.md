# D124/D126 protected activation recipe and result

The supported reviewed helper is copied byte-exactly to:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D124-protected-activation-1435/evidence/p2_commit_phase_capture.py`

It retains the required basename `p2_commit_phase_capture.py` and SHA256
`6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760`.

The normal control unsets both D66 and ASTRID helper path/hash overrides. The
reviewed control unsets ASTRID helper overrides and sets only the D66 helper
path/hash override. Both use the pinned Runtime and Agent checkouts, their
existing Python environments, Node v20.19.4, the unchanged test watchdog/waits,
and the exact two-test name pattern. See `commands-results.md` for the exact
commands and results.

The existing bootstrap basename guard was preserved. No source, guard,
environment-policy, package, profile, or test assertion was altered. The
normal and reviewed controls both passed with fresh endpoint/health and
registered-request lifecycle evidence. The reviewed evidence also passed the
bounded phase/sampler/privacy validation: no truncation, 102/102 retained
events, 20 ms sampler interval, bounded denominators, no sampler errors, and
explicit unsupported boundaries.

Raw captures remain private mode-0600 files under the harness-cleaned TMPDIR;
only safe structural facts and hashes are published. Public HTTP request IDs
and logged service diagnostic request IDs remain distinct; the existing
idempotency-key SHA is not treated as an error-log join.
