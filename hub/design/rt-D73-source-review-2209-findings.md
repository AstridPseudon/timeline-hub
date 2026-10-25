# D73 independent source/protected review

Verdict: **PASS** for the exact Composition source candidate at
`afda6c66a11608d8cb012df1a54bf2489d8c20b3` / tree
`67bd2d4ee1d50bd95ebb8b0de55d4d1ed1e3e87f`.

Receiving status remains **NOT_READY**, by design and by evidence:

- No receipt-rendered newline `key=value` manifest was supplied.
- The two candidate rows are present only in the private recipe; neither is installed in the central registry.
- Full interpreter/schema/profile dependency readiness is not qualified.
- No fresh per-central-ID XML/raw logs or submit/end disk witnesses exist.
- No real launcher preflight, provider/body, child request, network acquisition, live installation, full suite, or browser run occurred.

No blocking source finding remains. The retained Luna2120/2143 failures are resolved and independently verified:

1. `check.py` matches the immutable launcher’s first-`=` key/value parsing, preserves values containing `=`, rejects JSON, duplicates, malformed/empty entries, invalid tuple hashes, and emits the complete missing-key census.
2. `test_recipe.py` reads the unchanged central `test-run` named-row awk parser and `request-test` `*-nodes` guard, then invokes each private rendered row through `run --` with the exact `-m pytest -q` prefix. Both rows dispatch exactly once to the bounded stub with exit 17; poisoning only `agent_sha` returns nonzero with zero additional calls, zero preflight calls, and no body artifacts.

Protected inputs remain intact: Agent `2eca9a1d…` with Runtime `ab1e4f61…`, exact original 4+1 selectors, `integration`, cleared `addopts`, no cache provider, timeout 45, canonical source/origin/parent/tuple guards, original P4 hash, runtime lock and all 15 file hashes, schema/client/profile/node/composition guards, manifest poison guard, and separate per-ID output binding. The old Agent source recipe remains distinct from D139’s future merged-tuple child/core route; no old-venv overlay or fallback is used.

The source PASS must not be promoted to service qualification. The owner’s next step is to obtain genuine receipt-backed dependency/manifest inputs, install both rows through the normal central owner, and run the two exact named requests with durable per-ID artifacts.
