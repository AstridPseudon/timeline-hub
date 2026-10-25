## Report

Implemented F-D86 exact22 evidence through the existing D73 route.

- Fresh immutable tuple captured: Agent `657bc2e8`, Runtime `6634a17f`, App `54651008`, Composition `635f4de0`.
- Runtime lock verified against `6634a17f`.
- Controls:
  - `bash -n` recipe: pass.
  - Positive control: exit 17, exactly 1 stub call.
  - Poison control: exit 1, 0 calls.
- Exact22 body executed once with `-n 3`, cache disabled, timeout 45s, no marker filter.
- Result: exit 1; 22 tests, 4 passed, 18 errors, 0 failures, 0 skipped.
- Automatic disposition: NO-GO due to `transition` being rejected by the pinned command schema during media setup. No independent review performed.
- No product, test, dependency, schema, or generated-source changes made.

Evidence: [fd86-next32-receive-0328](</home/user/work/wt/rt-D86-ready22-body-0333/evidence/fd86-next32-receive-0328>)

Commit message and `DONE` marker were created.