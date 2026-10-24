# Runtime farm-agent-full v2 source packet

This is a reviewable normal-route packet only. It does not install, provision,
initialize or reinitialize the Store, edit the live registry, or run the Agent
suite.

## Settled checkpoint facts

The checkpoint was run once against Agent commit
`9cd3dbe865a941c052bda04ae0d61306d18f8f26` (tree
`57f0231da0d7904ecd8778169973d6384e0ae141`), with Runtime `45c3a7f4` as the
backend. It returned 288 failures, 17,335 passes, 187 setup errors and 4
skips; no JUnit was produced. The failure and error node lists are retained in
the shared hub design area (281 failed lines, 187 setup error lines); seven
summary failures cannot be accounted for from those lines. This packet does
not relabel that result or call all failures environmental.

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

The returned normal receipt must supply the actual managed profile path,
Node v20.19.4/npm 10.8.2 carrier, requested Agent/Runtime SHAs and build origin.
Verify clean checkout SHA/tree and actual import origins separately. A path in
the request is not proof of installation. Runtime's declared `45c3` lock and
four client hashes remain unchanged; using reviewed `1d9dd` is source selection,
not an overlay or generated tuple adoption.

`registration-row.txt` is a rendering template. Replace `@MANAGED_PROFILE@`
and `@RUNTIME_CHECKOUT@` only with physical paths authenticated by those normal
receipts. The installed row contains literal paths and `PYTHONPATH="$PWD:<Runtime>"`
for the service's Agent snapshot. It never depends on an ambient receipt
variable. It includes `ASTRID_TEST_NODE_MODULES=<managed-profile>/node_modules`
and all existing required environment bindings. Pre-pytest checks execute
actual Node/npm version commands, peer resolution/imports and Python imports,
and verify origins, D40 source bytes, declared lock and canonical client hashes.

## Existing Store installation and private evidence

[FARM-CODEX-BRIEF.md](FARM-CODEX-BRIEF.md) contains the one reviewed normal
installer command and exact missing inputs. It opens the existing Store,
requires its normal managed registration, renders the template, and replaces
exactly one existing `agent full-farm` row under `store.mutex()` using the
installed atomic API. It uses a fresh post-maker baseline and UTC backup,
preserves the original `agent full` and every outside byte, refuses drift,
and rolls back only its unchanged post-image. It does not initialize,
reinitialize, adopt, append a duplicate, replace owner/index, or install a helper.
An interrupted Store transaction uses the existing recovery route.

The later installer needs this directory's six files: this README, the brief,
registration template, source-selection JSON, targeted test and manifest.
It also needs the predecessor's authentic `remotion-env-nodes` row/env
attachments and current normal checkout/runtime receipts. No current Farm
registry, source checkout receipt or managed profile receipt has been supplied
here; publication remains held. Do not substitute a selected historical pin
or `/home/user/work/runtime` for those inputs.

Private acceptance executes the brief's actual installer command body, then
production `test-run`'s exact line-15 awk extraction and its actual
`suite_lease` context manager (`names_for_suite`/`acquire`, lines 66, 70–73).
Only pytest's body is substituted with a bounded diagnostic; the rendered
recipe's environment/version/peer/import/hash checks still run. The diagnostic
and its subprocess inherit acquired lease descriptors; lock exclusion and
release are checked. Fixtures export exact Agent/Runtime Git objects and borrow
historical renderer peers read-only for imports. They do not authenticate the
current 0.0.14 managed graph, prove a Farm receipt, run a full suite or qualify
Farm. Negative cases cover pre-body refusal, Store/registry drift and guarded
rollback. No live service, Store or dispatcher is invoked.

A parameterized source packet PASS does not mean Farm READY. Independent
source review and a later genuine Farm preflight remain separate, before
Farm requests the one corrected checkpoint through the production caller.
