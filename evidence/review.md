# D124 next Farm core packet independent review

## Verdict: FAIL

The packet commit under review is `e44c381062d36afe9ff0d285f5b14c05f4f987f`
with tree `cad65b21899eff6718544419023ee15a4d61129b`. It is source-only and
its three evidence files are the only changes from composition base
`635f4de06fda22a85fc2e4cfc764d0153a4c9f40`.

The requested Agent and Runtime source tuples are correct. The selector body
is also unchanged from the qualified 1336 core command: 22 argv roots,
including the live-scene composition root, against the 23-entry inventory,
with the existing `-n 3`, `-o addopts=`, `-p no:cacheprovider`, and
`--timeout=45` controls.

## Blocking findings

1. `evidence/next-farm-core-command.md:20-21` records incomplete parent lists
   while labeling the column `parents`. Read directly from the authoritative
   Git objects, App `d8a1cd40b866c49c0ab415682391f0ec87a7a8e7` has parents
   `34d4644589970274a5252c0f7c68b6288eb0b0b4` and
   `331a58363d1dc6ade1db2d2fa9d58688520c51bd`; Composition
   `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` has parents
   `7a95a40b07ea0d273e17afb69dbc3456b603f2bc` and
   `c05fdb171fe37c1d5817a060ecb716a329ee821a`. The packet records only the
   first parent for each and its shell guard does not verify either parent
   list. This fails the required source head/parent verification.

2. The qualified 1336 Farm core packet’s required parsed-row preflight controls
   were removed. Its `MAIN_POSITIVE_CONTROL`, `MAIN_POSITIVE_COUNTER`,
   `MAIN_POISON_CONTROL`, and `MAIN_POISON_COUNTER` block, including expected
   positive exit `17`/one counter line and poison nonzero/zero counter lines,
   has no equivalent in the next packet. The qualified launcher SHA-256 guard,
   Node `v20.19.4` guard, and stale-manifest rejection guards were also
   dropped. The packet therefore does not preserve every preexisting Farm
   control as required, even though it correctly makes no actual counter or
   receipt claim.

3. The child-maker refusal is recorded and no retry/substitution/overlay/bypass
   is specified, but the packet does not require the existing owner disposition
   for the refused unowned distribution metadata. That owner-disposition gate
   must remain explicit before Farm qualification can proceed.

## Passing checks

- Agent `a4e016b6a9f91fbe372672bdcf382c630bf59186`, tree
  `60d45288145414ee4702fcce61af7c7810c2a3df`, parents
  `61fefc6983f4413f1d1964b149bbaf5eadb8d2f0` and
  `96df3f5b4862b1c267e3816237bae8a64b5dc31f`.
- Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree
  `de2954a0ceadb4455903d9abdfec3b773318a50f`, parents
  `7070f1378d1917fcce69857ebd33cd2b3015568b` and
  `ef4728a1c07b7d3909d5027fbf1e673f6aec0030`.
- Agent source comparison: 3,563 old paths, 3,565 new paths, 10 changed
  paths, and 3,555 invariant non-target blobs; the changed-path list matches
  `evidence/input-map.json`.
- Launcher blob/SHA-256, D73 maker blob/SHA-256, schema-source blob, and
  Runtime lock blob match the packet’s declared Git-object identities.
- Qualified 1336 publication 1342 hashes match the three referenced qualified
  handoff files byte-for-byte.
- The full C0 request/reply seam is present in the packet prose, and Farm
  checkout/profile/child/D73 receipt/counter/execution results remain honestly
  unclaimed.

## Validation commands

- `python3 -m json.tool evidence/input-map.json` — PASS.
- Extracted the one `~~~sh` block from `evidence/next-farm-core-command.md`
  into `/tmp/w-cebab50eda/packet-block-1.sh`; `bash -n` — PASS.
- Compared the selector command line with the qualified 1336 command — PASS.
- Read source heads, trees, parents, blobs, and SHA-256 values with read-only
  `git cat-file`, `git rev-parse`, `git rev-list`, `git ls-tree`, `git show`,
  and `sha256sum` checks — requested Agent/Runtime and identity checks PASS;
  App/Composition parent completeness FAIL as above.
- `git diff --check` — PASS.

No Farm execution, child refusal re-attempt, profile/install action, sockets,
browser, pytest, or product suite was run.
