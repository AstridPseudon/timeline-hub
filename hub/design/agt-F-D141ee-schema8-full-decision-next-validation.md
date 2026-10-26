# Validation

Fresh bounded checker: `python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141ee-schema8-full-decision-next/evidence/check.py` -> `PASS 8 rows render assertions True installer exact [False, False]`.

It read frozen Agent Git blobs and ASTs, compared rendering assertions/body hashes, compared both installer originals against all four current installer candidates, parsed the raw cut/pristine XML, verified all eight pristine IDs and all six rendering/four installer current PASS candidates, and recorded source/XML hashes and absolute paths. No product tests or test-run route was invoked.

No pytest, provider/import-dependent execution, collection, request, test-run, wait, browser, dependency install, full/heavy suite, or body execution was run.
