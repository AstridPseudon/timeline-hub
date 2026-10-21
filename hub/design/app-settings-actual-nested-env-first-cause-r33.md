# D01 Settings actual nested environment first cause

Status: HOLD; no actual retry authorized.

The r32 preflight was incomplete. It passed source/role/lock/graph checks,
resolver 10/10, and Settings discovery 1/1, but discovery does not run the
shot-name `beforeAll`. The actual child then failed at
`tests/e2e/local/shot-name-command.spec.ts:60` because
`TIMELINE_CURRENT013_AGENT_SHA` was absent. Assertions at the Settings body
were not reached.

The nested source guard in current App `33b4a86c` is also frozen to
`8130a401/2c4ac180/e700d23e`; the authorized Main95 tuple is
`6efc8150/95bd3c5f/091aa23e/76/public13/77/9412`. Supplying old values is
not acceptable, and supplying current values without the exact three-literal
source hunk is not coherent. The hunk is present in non-ancestor App
candidate `7db937df` and must receive custody review before any row is run.

Corrected-row source proposal: use the reviewed candidate after that exact
hunk, pin Agent execution 6efc81500a0e0688c2bb41e736503f0fc3e04abb, vendor
091aa23ec83ea05ffd3b0115a640230d51c8c429, Runtime/prod
95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c, 76 Runtime artifacts, public13
archive 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738,
77 members, and pass the three nested values as part of the child environment.
Retain all existing Main95 source, graph, resolver, discovery, browser, and
Settings behavior requirements. Do not submit this row until the App SHA/tree,
runner digest, nested guard, and row are independently reviewed together.

No product files were changed. No browser, build, full suite, install, tsc,
or actual retry was run by this worker.

