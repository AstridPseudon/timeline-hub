# Agent F joined-head final proof

PASS on the actual joined head `ef851b22c506245441b9a630c093b3460e39cbdc` / tree `b11eee891208d11e23c55950f8954ddd3377d5a8`. Runtime was the clean exact checkout `1365e4b17b31c4a7093d5943674637067fd2bab4` / tree `6c69c3dc47822fffbaf27cd63815d2895155ffaa`.

The exact local collection returned `25 tests collected in 2.66s`. Central targeted result `agt-F-joined-final-proof-1000-targeted-1023100048-24668` used the same snapshot tree and returned `25 passed in 16.46s`, exit 0.

| Group | Selected | Passed | Notes |
| --- | ---: | ---: | --- |
| Original provider nodes | 10 | 10 | Includes the seven previously failing nodes as meaningful new-source reruns |
| Original writer nodes | 12 | 12 | Explicitly excludes only D17 `test_duplicate_preflights_and_publication_are_core_only` |
| `d05` hydration controls | 2 | 2 | Exact first two nodes from `tests/sdk/test_timeline_sync.py` |
| Legacy admission control | 1 | 1 | Exact requested node |
| Total | 25 | 25 | Targeted selection only |

The omitted D17 node remains present and untouched; no writer-13 or full-suite claim is made. The two `d05` hydration tests prove exact revision/publication pair hydration and wrong-publication refusal without pending commands. The legacy node proves refusal before execution with artifacts retained.

The current `astrid/sdk/timeline/publish.py` retains the reviewed `f0af12f67` checkout/narration gating and `c2584a014` core-only validation. `d05fcc076` is an ancestor, and its exact `tests/sdk/test_timeline_sync.py` blob is unchanged at the joined head. R1 mirror `b8e507625` and R2 mirror `f7fcb7282` are also ancestors. Canonical schema SHA-256 remains `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`; `runtime.lock.json` retains normal producer `34eac0041b0891e9011966b39bcbd26053fde5bc`; protected P4 blobs are `afc9c112527692536a065de8cdbfc7a25c19bc26` and `192efbfa14607f0edfb362d47d5238645c64e984`.

Required quality checks all passed: Ruff `2149/2149`, type comparison `1912/1912`, vendor lock current, artifact manifest current, and `git diff --check`. No product/test/fixture/environment/pin files changed; no full or excluded heavy suites were run.

See the detailed worker report at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-joined-final-proof-1000/report.md`.

