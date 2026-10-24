# Runtime farm-agent-full v2 source packet

This is a reviewable normal-route packet only. It does not install, provision,
initialize the live Store, edit the live registry, or run the Agent suite.

## Settled checkpoint facts

The checkpoint was run once against Agent commit
`9cd3dbe865a941c052bda04ae0d61306d18f8f26` (tree
`57f0231da0d7904ecd8778169973d6384e0ae141`), with Runtime `45c3a7f4` as the
backend. It returned 288 failures, 17,335 passes, 187 setup errors and 4
skips; no JUnit was produced. The failure and error node lists are retained in
the shared hub design area. This packet does not relabel that result or call
all failures environmental.

The old Runtime lock remains authoritative for the four canonical client
hashes and declares source `45c3a7f476e1c5f74fafc15956a58b9871eee21f`. That
checkout does not contain `runtime_protocol.external_pack_sources`, which the
tested Agent D40 code imports. The current Runtime base
`1d9ddba546f8fb1300f55ff62607ed492719cbaa` contains that module, has tree
`f56c396c4495547680b46e832565278d2c375e69`, and retains the same canonical
client bytes. These are separate identities: the packet never claims that
45c3 provides D40 and never changes the declared lock or backend receipt.

The selected Runtime checkout and a normal maker receipt are still missing.
The candidate row is therefore a bounded later projection, not an authorized
live append. Farm must refuse publication until the exact checkout, clean
status, normal runtime receipt, managed path, Agent/runtime SHAs and imported
module origins are recorded. Do not substitute `/home/user/work/runtime`, a
legacy graph, a stale pin, or a source overlay.

## Later normal requests

The manager/lead should issue these through the existing dispatcher only after
the current Store/registry preflight and after checking the Agent receipt
against the actual tested tree:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
"$ORCH/bin/request-checkout" agent 9cd3dbe865a941c052bda04ae0d61306d18f8f26 \
  "OPS farm full v2 exact tested Agent source"
"$ORCH/bin/request-checkout" runtime 1d9ddba546f8fb1300f55ff62607ed492719cbaa \
  "OPS farm full v2 D40 Runtime source carrier"
```

After both clean detached checkouts exist, and only if the maker’s normal
registration/template checks pass, use the supported eight-field request:

```bash
env -u RUNTIME_AGENT_CHECKOUT -u RUNTIME_RUNTIME_CHECKOUT \
  -u RUNTIME_RUNTIME_SHA -u RUNTIME_TEMPLATE_SUITE -u RUNTIME_NODE_BIN \
  "$ORCH/bin/request-runtime" agent-remotion-farm-v2-9cd \
  9cd3dbe865a941c052bda04ae0d61306d18f8f26 \
  f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d \
  /home/user/work/wt/agt-pin-9cd3dbe8 \
  /home/user/work/wt/rt-pin-1d9ddba5 \
  1d9ddba546f8fb1300f55ff62607ed492719cbaa \
  remotion-env-nodes \
  /home/user/work/toolchain/node-v20.19.4-linux-x64/bin
```

The returned receipt must be the source of the final managed profile path,
`ASTRID_REMOTION_PROJECT_DIR`, Node v20.19.4/npm 10.8.2 carrier, and actual
runtime/Agent/module origins. Do not handforge a managed identity from these
arguments.

## Safe installer sequence

1. Verify the packet manifest, the installed `bench_store.py` hash, the
   authentic `remotion-env-nodes` row/env attachments from the predecessor
   packet, the existing `agent full` row, and all current registry bytes.
2. Save a UTC private backup. Refuse if `/home/user/work/bench-store` exists,
   is partial, or is a symlink; refuse registry drift rather than replacing a
   stale whole config.
3. Call `Store.initialize(root, ORCH/tests)` once through the installed API,
   then use its public read. Do not initialize or adopt an existing store.
4. Let the normal maker create or authenticate the managed Runtime entry. A
   receipt with Runtime `45c3` or missing `external_pack_sources` is a source
   mismatch and stops the operation.
5. From a fresh post-maker baseline, append exactly `registration-row.txt`
   with the existing atomic API. Preserve the original full row and every
   byte outside the one new row. The new full-farm row is unmanaged; the
   maker’s Runtime row remains managed.
6. Return pre/post hashes, exact appended bytes, outside-byte comparison,
   Store owner/index validation, normal receipts, and actual source/module
   origins. Only Farm may then request the one later checkpoint.

Any refusal, drift, wrong source, partial initialization, or permission denial
stops the sequence. Use only the installed Store recovery route for an
interrupted transaction; never restore owner/index over a live Store.
