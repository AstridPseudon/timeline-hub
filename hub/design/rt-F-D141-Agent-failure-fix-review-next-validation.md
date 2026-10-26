# Validation

Result: **PASS_EVIDENCE** for one independent protected, evidence-only review.

Commands and results:

- `python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141-Agent-failure-fix-next/evidence/check_join.py` — PASS; author checker reproduced the exact join, source hashes, current publication custody, and production `render_readme` hash.
- `python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141-Agent-failure-fix-review-next/evidence/tmp/independent_check.py` — PASS; independently recomputed the accounting, publication hashes and bindings, candidate prefixes/suffixes, and four-repo plus missing-gate renderer behavior.
- `python3 -m json.tool` on the author `source-manifest.json`, `controls.json`, and `sampler-lifecycle.json` — PASS.
- `python3 -m py_compile .../evidence/tmp/independent_check.py` — PASS.
- Private `ast.parse` of `independent_check.py` — PASS.
- `ruff check --select F --no-cache .../evidence/tmp/independent_check.py` — PASS (`All checks passed!`).
- Ordinary five-second available-byte sampler — PASS: five samples stayed above the 4,000,000,000-byte stop; sampler exited 0, was waited and reaped, and no uninterruptible processes were observed.

Not run by design: types, product tests, full suites, browser/live sockets, delivery-build CLI/main, services/bodies, staging/cloning, rehearsal, installation, CAS/request, canonical writes, and ZIP.
